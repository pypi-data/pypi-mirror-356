from __future__ import annotations
from qm import QuantumMachinesManager, QuantumMachine, SimulationConfig, qua
from qm.jobs.running_qm_job import RunningQmJob
from .analysis.analysis_tools import Output, demod2volts
from .analysis.demodulator import default_demodulator
from .config_builder import ConfigBuilder
from grpclib.exceptions import StreamTerminatedError
from qubox.pulse_manager import PulseOperationManager
from tqdm import tqdm 
import numpy as np
import os, json
from pathlib import Path
from dataclasses import dataclass
from time import sleep

def launch_qm_devices(qop_ip, cluster_name, oct_cal_path, config_dict):
    qmm = QuantumMachinesManager(host=qop_ip, cluster_name=cluster_name, octave_calibration_db_path=oct_cal_path)
    qm = qmm.open_qm(config_dict)
    return qmm, qm

# ------------------------------------------------------------------
# helper (place it once in the file, as shown earlier)
def _numeric_keys_to_ints(obj):
    if isinstance(obj, dict):
        return {
            (int(k) if isinstance(k, str) and k.isdigit() else k):
                _numeric_keys_to_ints(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_numeric_keys_to_ints(v) for v in obj]
    return obj
# ------------------------------------------------------------------

def cast_to_float(x):
    """
    Safely casts x to float or array of floats.
    Supports scalar or numpy array input.
    Raises ValueError on invalid conversion.
    """
    try:
        if isinstance(x, np.ndarray):
            return x.astype(float)
        else:
            return float(x)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot cast {x} to float: {e}")
    
class QuaProgramManager:
    # ───────────────────────────── init ─────────────────────────────
    def __init__(self,
                 qop_ip: str,
                 cluster_name: str,
                 oct_cal_path: str,
                 *,
                 hardware_path: str | Path | None = None,
                 config_dict:  dict | None = None):

        self._qmm = QuantumMachinesManager(host=qop_ip,
                                           cluster_name=cluster_name,
                                           octave_calibration_db_path=oct_cal_path)
        self.qm = None

        # ---- hardware ---------------------------------------------------
        self.hardware_path: Path | None = Path(hardware_path) if hardware_path else None
        self.hardware: dict | None = None
        if self.hardware_path and self.hardware_path.exists():
            raw = json.loads(self.hardware_path.read_text())
            self.hardware = _numeric_keys_to_ints(raw)          # ← convert here

        # ---- config (hardware ⊕ pulses) -------------------------------
        if config_dict is not None:                              # user supplied full cfg
            self.config_dict = _numeric_keys_to_ints(config_dict)  # ← convert too
        elif self.hardware is not None:                          # only hardware known
            self.config_dict = self.hardware.copy()
        else:
            self.config_dict = None

        # ---- book-keeping --------------------------------------------
        self.config_exists = False
        self.elements = {}
        self.processors = [default_demodulator]

        # ---- spin up if we already have a full cfg --------------------
        if self.config_dict:
            self.init_qm(self.config_dict)


    # ─────────────────────────── I/O helpers ──────────────────────────
    def load_hardware(self, hardware_path: str | Path) -> None:
        """Load *hardware.json* and attach it as the hardware block."""
        self.hardware_path = Path(hardware_path)
        raw = json.loads(self.hardware_path.read_text())
        self.hardware = _numeric_keys_to_ints(raw)        # ← convert here

        # rebuild or create working config
        if self.config_dict:
            for key in ("controllers", "octaves", "elements", "version"):
                self.config_dict[key] = self.hardware[key]
        else:
            self.config_dict = self.hardware.copy()

        self.config_exists = False 

    def save_hardware(self, path: str | Path | None = None):
        """Write the *hardware-only* dictionary back to disk."""
        if self.hardware is None:
            raise RuntimeError("No hardware dictionary loaded.")
        dst = Path(path) if path else (self.hardware_path or Path("hardware.json"))
        dst.write_text(json.dumps(self.hardware, indent=2))
        print(f"[QuaProgramManager] hardware saved → {dst}")

    # ────────────────────── Pulses merger entry point ───────────────────
    def merge_pulses(self, pom: "PulseOperationManager", *,
                    include_volatile: bool = True):

        if self.hardware is None:
            raise RuntimeError("Hardware block is unknown; call load_hardware().")

        cfg = json.loads(json.dumps(self.hardware))       # fresh copy of HW
        cfg = _numeric_keys_to_ints(cfg)                  # ensure ints (deep)

        pom.burn_to_config(cfg, include_volatile=include_volatile)
        self.config_dict = cfg
        print("[QuaProgramManager] pulses merged into config_dict")

    # ───────────────────────── existing API (unchanged) ────────────────
    #   init_qm, launch_qm, burn_config_to_qm …
    #   (no code changes needed in those methods)


    def init_qm(self, config_dict: dict | None = None, *, init_elements=True):
        """
        Launch QM with the provided configuration.  If no config_dict is given,
        use the one stored in self.config_dict (e.g. produced by merge_pulses()).
        """
        if config_dict is None:
            if self.config_dict is None:
                raise RuntimeError("No configuration available; call merge_pulses() first.")
            config_dict = self.config_dict

        self.launch_qm(config_dict)

        if init_elements:
            self.elements = self._init_elements()
    
    def launch_qm(self, config_dict):
        self.qm = self._qmm.open_qm(config_dict)
        self.config_dict = config_dict
        self.config_exists = True

    def burn_pulse_to_qm(self,
                        pom: "PulseOperationManager" | None = None,
                        *,
                        include_volatile: bool = True):
        """
        Convenience wrapper:
        • If a PulseOperationManager is given, merge its pulses into the
            hardware block first.
        • Then (re)open a QM with the resulting configuration.
        """
        if pom is not None:
            if self.hardware is None:
                raise RuntimeError("Hardware block not loaded.")
            cfg = json.loads(json.dumps(self.hardware))
            pom.burn_to_config(cfg, include_volatile=include_volatile)
            self.config_dict = cfg

        if self.config_dict is None:
            raise RuntimeError("No configuration to burn.")
        self.launch_qm(self.config_dict)

    def init_default_config(self):
        print("Initializing Default Element Configurations")
        for el in self.qm.get_config()["elements"]:
            if el.startswith("__"):
                continue
            default_el_lo = self.get_element_lo(el)
            self.set_element_lo(el, default_el_lo)
            print("-"*37)

    def save_config(self, base_path):
        builder = ConfigBuilder.from_dict(self.config_dict)
        hardware_path = os.path.join(base_path, "hardware.json")
        controls_path = os.path.join(base_path, "controls.py")
        mapping_path = os.path.join(base_path, "op_mappings.json")
        builder.to_split_sources(hardware_path, controls_path, mapping_path)

    def _init_elements(self):
        cfg = self.qm.get_config()
        elems = {}
        for el, info in cfg["elements"].items():
            if el.startswith("__"):
                continue
            lo_freq = info['mixInputs']["lo_frequency"]
            if_freq = info["intermediate_frequency"]
            elems[el] = {"LO": lo_freq, "IF": if_freq}
        return elems

    def register_processor(self, processor):
        """Add a function(Output, **kwargs) -> Output to the pipeline"""
        self.processors.append(processor)

    def set_element_lo(self, el, el_lo):
        self.qm.octave.set_lo_frequency(el, el_lo)
        self.elements[el]["LO"] = el_lo
        print("" * 37 + f"set LO for element {el} to {el_lo*1e-6} MHz")

    def set_element_fq(self, el, freq):
        if_freq = self.calculate_el_if_fq(el, freq)
        self.qm.set_intermediate_frequency(el, if_freq)
        self.elements[el]["IF"] = if_freq
        print("" * 37 + f"Set element {el} to freqeuncy : {freq*1e-6} -> if : {if_freq*1e-6} (MHz)")

    def get_element_lo(self, el):
        return self.elements[el]["LO"]
    
    def get_element_if(self, el):
        return self.elements[el]["IF"]

    def calculate_el_if_fq(self, el, freq, lo_freq=None):
        if lo_freq is None:
            lo_freq = self.elements[el]["LO"]
        downconverted_if = lo_freq - freq
        if np.any(np.abs(downconverted_if) > 500e6):
            raise ValueError(f"Conversion Error: downconverted frequency out of bound for element {el} with frequency {freq}")
        result = freq - lo_freq
        return cast_to_float(result)
    
    def calibration_el_octave(self, el=None, target_LO=None, target_IF=None, save_to_db=True):
        if el is None:
            print("No element specified, calibrating all elements")
            for key, value in self.elements.items():
                deafult_lo = value["LO"]
                default_if = value["IF"]
                self.calibration_el_octave(key, deafult_lo, default_if, save_to_db)
        if not target_LO:
            target_LO = self.get_element_lo(el)
        if not target_IF:
            target_IF = self.get_element_if(el)
        print("-" * 37 + f"calibrating: {el} with LO, IF = {target_LO}, {target_IF}")
        self.qm.calibrate_element(el, {target_LO: (target_IF,)}, save_to_db=save_to_db)

    def run_program(self, qua_prog, n_total: int, print_report: bool = True, show_progress: bool = True, 
                    processors: list = None, progress_handle: str = 'iteration', **kwargs) -> Output:
        job = self.qm.execute(qua_prog)
        if show_progress:
            self._report_progress(job, n_total, progress_handle)
        if print_report:
            print(job.execution_report())

        out = Output()
        for name, handle in job.result_handles.items():
            out[name] = handle.fetch_all()
        try:
            job.halt()
        except StreamTerminatedError:
            print("Idle too long! Connection lost")
        except Exception as e:
            print(f"attempting to halt job failed: {e}")

        for proc in (processors or self.processors):
            out = proc(out, **kwargs)
        return out

    def _report_progress(self, job: RunningQmJob, n_total: int, handle: str):
        if not n_total:
            print("n_total not passed, will not report progress...")
            return
        if handle in job.result_handles.keys():
            progress_bar = tqdm(total=n_total, desc="Running Program...")
            while job.result_handles.is_processing():
                if job.result_handles.get(handle):
                    progress_bar.n = job.result_handles.get(handle).fetch_all()
                    progress_bar.refresh()
            progress_bar.n = job.result_handles.get(handle).fetch_all()
            progress_bar.refresh()
        else:
            print("Warning: variable iteration does not exists, will not report progress!")
            while job.result_handles.is_processing():
                pass 

    def program_simulate(self, program, simulate_duration=4000, analog_ports=None, digital_ports=None):
        simulation_config = SimulationConfig(duration=int(simulate_duration/4))  
        job = self.qmm.simulate(self.qm.get_config(), program, simulation_config)
        job.get_simulated_samples().con1.plot(analog_ports, digital_ports)
        return 0

    def run_continuous_wave(self, elements: list, el_freqs: list, gain=1.0):
        if len(elements) != len(el_freqs):
            raise ValueError(f"elements and frequencies number don't match up!")   
        for i, el in enumerate(elements):
            if el not in self.elements:
                raise ValueError(f"unrecognized element by class object {el}")
            else:
                if_freq = el_freqs[i]      
                self.qm.set_intermediate_frequency(el, if_freq)
        with qua.program() as continous_wave:
            with qua.infinite_loop_():
                for el in elements:
                    qua.play("const" * qua.amp(gain), el)
        job = self.qm.execute(continous_wave)
        return job

    def close_OPX_System(self):
        self.qmm.close_all_qms()