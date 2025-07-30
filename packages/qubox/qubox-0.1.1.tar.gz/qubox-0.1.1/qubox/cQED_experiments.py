from . import cQED_programs
from .analysis.analysis_tools import Output, generalized_fit, plot_IQ, qm_unit
from .analysis.demodulator import qubit_demodulator
from .gates import Gate, Displacement, Rotation, SNAP

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import time, json
import numpy as np
import matplotlib.pyplot as plt
from .config_builder import ConfigBuilder, ConfigSettings
from .program_manager import QuaProgramManager
from .pulse_manager import PulseOperationManager, PulseOp
import numbers
from qualang_tools.analysis import two_state_discriminator

def _make_lo_segments(rf_begin: float, rf_end: float) -> list[float]:
    M, B = ConfigSettings.MAX_IF_BANDWIDTH, ConfigSettings.BASE_IF
    if M <= abs(B):
        raise ValueError("MAX_IF_BANDWIDTH must be greater than BASE_IF")
    span = M + B
    if (rf_end - rf_begin) <= span:
        return [rf_begin + M]
    los, LO, last = [], rf_begin + M, rf_end - B
    while LO < last:
        los.append(LO)
        LO += span
    if los[-1] < last:
        los.append(last)
    return los

def _if_frequencies_for_segment(LO: float, rf_end: float, df: float) -> np.ndarray:
    M, B = ConfigSettings.MAX_IF_BANDWIDTH, ConfigSettings.BASE_IF
    max_if = (rf_end - LO) if (rf_end - LO) < (M + B) else B
    return np.arange(-M, max_if + 1e-12, df, dtype=int)

def _merge_segments(outputs: list[Output], freqs: list[np.ndarray]) -> Output:
    merged = {}
    # stitch every key
    for key in outputs[0]:
        vals = [o[key] for o in outputs if key in o]
        if isinstance(vals[0], np.ndarray):
            try:
                merged[key] = np.concatenate(vals, axis=0)
            except Exception:
                merged[key] = vals
        elif isinstance(vals[0], list):
            merged[key] = sum(vals, [])
        else:
            merged[key] = vals[0] if all(v == vals[0] for v in vals) else vals
    # flatten freq axis
    merged["frequencies"] = np.concatenate(freqs, axis=0)
    return Output(merged)

def create_if_frequencies(el, start_fq, end_fq, df, lo_freq, base_if_freq=ConfigSettings.BASE_IF):
    up_converted_if = lo_freq + base_if_freq
    max_bandiwdth = np.abs(ConfigSettings.MAX_IF_BANDWIDTH - np.abs(base_if_freq))
    sweep_min_bound, sweep_max_bound = up_converted_if - max_bandiwdth, up_converted_if
    if sweep_min_bound <= start_fq <= end_fq <= sweep_max_bound:
        return np.arange(start_fq - lo_freq,  end_fq - lo_freq - 0.1, df, dtype=int)
    else:
        raise ValueError(f"Sweep range must be bounded by: [{sweep_min_bound},{sweep_max_bound}] \n for element: {el} which has LO, IF = {lo_freq*1e-6}, {base_if_freq*1e-6} MHz respectively")

def _complex_encoder(obj):
    """Encode complex numbers (including numpy.complex64/complex128) as a dict."""
    if isinstance(obj, (complex, np.complex64, np.complex128)):
        return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def _complex_decoder(d):
    """Decode a dict to a complex number if the marker is found."""
    if "__complex__" in d:
        return complex(d["real"], d["imag"])
    return d

@dataclass
class cQED_attributes:
    ro_el:           Optional[str] = None
    qb_el:           Optional[str] = None
    st_el:           Optional[str] = None
    ro_fq:           Optional[int] = None
    qb_fq:           Optional[int] = None
    st_fq:           Optional[int] = None
    anharmonicity:   Optional[int] = None
    alpha :          Optional[float] = None
    st_chi:          Optional[float] = None
    st_chi2:         Optional[float] = None
    st_chi3:         Optional[float] = None
    st_K:            Optional[float] = None
    st_K2:           Optional[float] = None
    ro_therm_clks:   Optional[int] = None
    qb_therm_clks:   Optional[int] = None
    st_therm_clks:   Optional[int] = None
    proj_angle:      Optional[int] = None
    rotate_IQ:       Optional[int] = True    
    norm_IQ:         Optional[int] = None
    snap_phase_corr: Optional[list] = None

    def to_dict(self) -> dict:
        """
        Return all attributes as a dict.
        """
        return asdict(self)
    
    def to_json(self, filepath: str | Path) -> None:
        """Save this instance’s attributes to a JSON file."""
        data = asdict(self)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, default=_complex_encoder, indent=4)

    @classmethod
    def from_json(cls, filepath: str | Path) -> 'cQED_attributes':
        """Load an instance from a JSON file containing the same fields."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f, object_hook=_complex_decoder)
        return cls(**data)

    def get_fock_frequencies(self, fock_levels):
        qb_fq, chi, chi2, chi3 = self.qb_fq, self.st_chi, self.st_chi2, self.st_chi3
        if isinstance(fock_levels, numbers.Integral):
            if fock_levels < 0:
                raise ValueError("fock_levels must be non-negative")
            n_vals = range(fock_levels)

        elif isinstance(fock_levels, (list, tuple, np.ndarray)):
            iterable = (
                fock_levels.tolist() if isinstance(fock_levels, np.ndarray) else fock_levels
            )
            if not all(isinstance(n, numbers.Integral) for n in iterable):
                raise TypeError("All elements in fock_levels must be integers.")
            n_vals = iterable

        else:
            raise TypeError("fock_levels must be an integer or a list/array of integers.")

        fock_fqs = [qb_fq + chi*n + chi2*n*(n-1) + chi3*n*(n-1)*(n-2) for n in n_vals]
        return np.array(fock_fqs)

def load_exp_config(exp_path: str | Path):
    exp_path = Path(exp_path)
    try:
        builder = ConfigBuilder.from_json(exp_path/"config.json")
    except Exception as e:
        print(f"Warning, loading configuration files failed: {e}. Will build a default one")
        builder = ConfigBuilder.minimal_config()
        builder = ConfigBuilder.to_json(exp_path/"config.json")
    return builder
    
from pathlib import Path
import json, warnings

class cQED_Experiment:
    def __init__(self,
        experiment_path: str | Path,
        progMngr: QuaProgramManager | None = None,
        pulseOpMngr: PulseOperationManager | None = None,
        *,
        # only needed when we have to build a new QuaProgramManager
        qop_ip: str | None = None,
        cluster_name: str | None = None,
        oct_cal_path: str | Path | None = None,
        set_exp_config: bool = False
    ):
        self.base_path = Path(experiment_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        cfg_dir = self.base_path / "config"
        hw_file = cfg_dir / "hardware.json"
        pl_file = cfg_dir / "pulses.json"

        # ── 1)  QuaProgramManager  ──────────────────────────────────
        if progMngr is None:
            if not hw_file.exists():
                raise FileNotFoundError(
                    "You did not supply a QuaProgramManager and no "
                    f"hardware.json found at {hw_file}"
                )
            if None in (qop_ip, cluster_name, oct_cal_path):
                raise ValueError(
                    "When progMngr is omitted you must pass qop_ip, "
                    "cluster_name and oct_cal_path."
                )
            progMngr = QuaProgramManager(
                qop_ip, cluster_name, oct_cal_path,
                hardware_path=hw_file,
            )
        else:
            # ensure hardware loaded
            if progMngr.hardware is None:
                if hw_file.exists():
                    progMngr.load_hardware(hw_file)
                else:
                    raise FileNotFoundError(
                        "QuaProgramManager supplied without hardware and "
                        f"'{hw_file}' not found."
                    )

        self.quaProgMngr = progMngr

        # ── 2)  PulseOperationManager  ──────────────────────────────
        if pulseOpMngr is None:
            if pl_file.exists():
                pulseOpMngr = PulseOperationManager.from_json(pl_file)
            else:
                warnings.warn(f"No pulses.json found at {pl_file}; "
                              "starting with empty pulse library.")
                pulseOpMngr = PulseOperationManager()
        self.pulseOpMngr = pulseOpMngr

        # ── 3)  merge pulses → hardware and launch QM  ──────────────
        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr,
                                          include_volatile=True)
        # init_qm() with stored config_dict
        self.quaProgMngr.init_qm()

        # initialise default LO/IF settings
        self.quaProgMngr.init_default_config()

        # ── 4)  load or create experiment attributes  ───────────────
        attrs_file = self.base_path / "cqed_params.json"
        if attrs_file.exists():
            self.attributes = cQED_attributes.from_json(attrs_file)
        else:
            self.attributes = cQED_attributes()

        if set_exp_config:
            self.set_cQED_config()
            self.set_cQED_gate_attributes()
        
        self.save_unique_identifier = None
    def set_cQED_config(self):
        if self.attributes.rotate_IQ:
            cQED_programs.measureMacro.set_IQ_mod(I_mod_weights=["rot_cos", "rot_sin"], Q_mod_weights=["rot_m_sin", "rot_cos"])
        self.quaProgMngr.set_element_fq(self.attributes.ro_el, self.attributes.ro_fq)
        self.quaProgMngr.set_element_fq(self.attributes.qb_el, self.attributes.qb_fq)
        self.quaProgMngr.set_element_fq(self.attributes.st_el, self.attributes.st_fq)

    def set_cQED_gate_attributes(self):
        Gate.set_attributes(mgr=self.pulseOpMngr)
        Gate.attributes.disp_alpha_id = "const_alpha_pulse"
        Gate.attributes.disp_alpha = self.attributes.alpha
        Gate.attributes.chi = self.attributes.st_chi
        Gate.attributes.chi2 = self.attributes.st_chi2
        Gate.attributes.chi3 = self.attributes.st_chi3
        Gate.attributes.K = self.attributes.st_K
        Gate.attributes.K2 = self.attributes.st_K2
        Gate.attributes.snap_phase_corr = self.attributes.snap_phase_corr

    def register_pulse(
        self,
        pulse: PulseOp,
        *,
        override: bool   = False,
        persist:  bool   = False,
        save:     bool   = False,
        burn:     bool   = True,
        include_volatile: bool = True,
    ):
        """
        Wrapper around
            self.pulseOpMngr.register_pulse_op(...)
            self.quaProgMngr.burn_pulse_to_qm(...)

        Parameters
        ----------
        pulse : PulseOp
            The pulse description to register.
        override : bool, default False
            Forwarded to `register_pulse_op`.
        persist : bool, default False
            If True the pulse is saved in the permanent store.
        burn : bool, default True
            If True, immediately call `burn_pulse_to_qm()` so the QM is ready
            to play the new pulse.  Set False if you want to batch-register
            many pulses and burn once at the end.
        include_volatile : bool, default True
            Forwarded to `burn_pulse_to_qm` (ignored when *burn* is False).
        """
        # 1) add / update in the PulseOperationManager
        self.pulseOpMngr.register_pulse_op(
            pulse,
            override=override,
            persist=persist,
        )

        # 2) push to QM right away (optional)
        if burn:
            self.burn_pulses(include_volatile)

        if save:
            self.save_pulses()
    
    def burn_pulses(self, include_volatile: bool = True):
            self.quaProgMngr.burn_pulse_to_qm(
                self.pulseOpMngr,
                include_volatile=include_volatile,
            )

    def save_pulses(self, path: str | Path | None = None) -> Path:
        """
        Serialize the *permanent* part of ``self.pulseOpMngr`` to JSON.

        Parameters
        ----------
        path : str | Path | None, optional
            Destination file.  If omitted, the default is
            ``<base_path>/config/pulses.json``.

        Returns
        -------
        pathlib.Path
            The location of the saved file (useful for logging).
        """
        cfg_dir = self.base_path / "config"
        cfg_dir.mkdir(parents=True, exist_ok=True)

        dst = Path(path) if path is not None else cfg_dir / "pulses.json"
        self.pulseOpMngr.save_json(dst)

        print(f"[cQED] permanent pulses saved → {dst}")
        return dst
        
    def save_output(self, output: Output, target_folder: str, save_cqed_attributes=True):
        if save_cqed_attributes:
            output["cQED_params"] = self.attributes.to_dict()

        folder_path = self.base_path / target_folder
        
        folder_path.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        if self.save_unique_identifier:
            timestamp += f"_{self.save_unique_identifier}"
        filename_unique = f"{timestamp}.npz"
        save_path = folder_path / filename_unique
        output.save(save_path)

    def save_attributes(self):
        self.attributes.to_json(self.base_path / 'cqed_params.json')
         
    def readout_raw_trace(self, ro_gain, ro_if=-5e6,ro_el="resonator", ro_pulse_op="readout", n_avg=1000):
        ro_program = cQED_programs.readout_raw_trace(ro_el, ro_gain=ro_gain, ro_if=ro_if, ro_pulse=ro_pulse_op, n_avg=n_avg)
        def proc(output: Output):
            adc1, adc2, adc1_single, adc2_single = output.extract('adc1', 'adc2', 'adc1_single_run', 'adc2_single_run')
            output['adc1'], output['adc2'], output['adc1_single_run'], output['adc2_single_run'] = map(
                qm_unit.raw2volts, (adc1, adc2, adc1_single, adc2_single)
            )
            output['adc1_mean'], output['adc2_mean'] = np.average(output['adc1']), np.average(output['adc2'])
            return output
        output = self.quaProgMngr.run_program(ro_program, n_total=n_avg, processors=[proc])
        return output
            
    def resonator_spectroscopy(self, ro_gain, rf_begin, rf_end, df, ro_pulse="readout", n_avg: int = 1000) -> Output:
        attr = self.attributes
        if_frequencies = create_if_frequencies(attr.ro_el, rf_begin, rf_end, df,  self.quaProgMngr.get_element_lo(attr.ro_el))
        resonator_spec = cQED_programs.resonator_spectroscopy(attr.ro_el, ro_pulse, ro_gain, if_frequencies, attr.ro_therm_clks , n_avg)
        lo_freq = self.quaProgMngr.get_element_lo(attr.ro_el)
        output = self.quaProgMngr.run_program(resonator_spec, n_avg)
        output["frequencies"] = lo_freq + if_frequencies
        self.save_output(output, "cavitySpectroscopy")
        return output

    def resonator_power_spectroscopy(self, rf_begin, rf_end, df, g_min=1e-3, g_max=0.5, N_a=50, ro_pulse="readout", n_avg: int = 1000) -> Output:
        attr = self.attributes
        if_frequencies = create_if_frequencies(attr.ro_el, rf_begin, rf_end, df, self.quaProgMngr.get_element_lo(attr.ro_el))
        gains = np.geomspace(g_min, g_max, N_a)
        resonator_spec_2D = cQED_programs.resonator_power_spectroscopy(attr.ro_el, ro_pulse, if_frequencies, gains, attr.ro_therm_clks, n_avg)
        lo_freq = self.quaProgMngr.get_element_lo(attr.ro_el)
        output = self.quaProgMngr.run_program(resonator_spec_2D, n_avg)
        output["frequencies"] = lo_freq + if_frequencies
        output["gains"] = gains
        self.save_output(output, "cavityPowerSpectroscopy")
        return output

    def qubit_spectroscopy(self, rf_begin, rf_end, df, qb_gain, qb_len, n_avg: int = 1000):
        attr = self.attributes
        if_frequencies = create_if_frequencies(attr.qb_el, rf_begin, rf_end, df, lo_freq=self.quaProgMngr.get_element_lo(attr.qb_el))

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        qubit_spec_program = cQED_programs.qubit_spectroscopy(attr.ro_el, attr.qb_el, if_frequencies, qb_gain, qb_len, attr.qb_therm_clks, n_avg)
        output = self.quaProgMngr.run_program(qubit_spec_program, n_avg)
        lo_freq =  self.quaProgMngr.get_element_lo(attr.qb_el)
        output["frequencies"] = lo_freq + if_frequencies
        self.save_output(output, "qubitSpectroscopy")
        return output

    def qubit_spectroscopy_coarse(self, rf_begin, rf_end, df, qb_gain, qb_len, n_avg=1000):
        attr = self.attributes

        lo_list = _make_lo_segments(rf_begin, rf_end)
        results, all_freqs = [], []
        for LO in lo_list:
            self.quaProgMngr.set_element_lo(attr.qb_el, LO)
            if_freqs = _if_frequencies_for_segment(LO, rf_end, df)
            prog = cQED_programs.qubit_spectroscopy(
                attr.ro_el, attr.qb_el, if_freqs, qb_gain, qb_len, attr.qb_therm_clks, n_avg
            )
            out = self.quaProgMngr.run_program(prog, n_avg)
            freqs = LO + if_freqs
            out["frequencies"] = freqs
            results.append(out)
            all_freqs.append(freqs)

        final = _merge_segments(results, all_freqs)
        self.save_output(final, "qubitSpectroscopy")
        return final

    def qubit_spectroscopy_ef(self, rf_begin, rf_end, df, qb_gain, qb_len, n_avg):
        attr = self.attributes
        qb_if = self.quaProgMngr.get_element_if(attr.qb_el, attr.qb_fq)
        if_frequencies = create_if_frequencies(attr.qb_el, rf_begin, rf_end, df)

        qubit_spec_program = cQED_programs.qubit_spectroscopy_ef(attr.ro_el, attr.qb_el, 
                                                                 if_frequencies, qb_if, 
                                                                 qb_gain, qb_len, "x180", attr.qb_therm_clks, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(qubit_spec_program, n_avg)
        lo_freq =  self.quaProgMngr.get_element_lo(attr.qb_el)
        output["frequencies"] = lo_freq + if_frequencies
        self.save_output(output, "qubit_efSpectroscopy")
        return output

    def temporal_rabi(self, qb_gain: int, max_pulse_len: int = 1000, dt: int = 4, pulse="gaussian_X", n_avg: int = 1000):
        attr = self.attributes
        dcycle = int(np.ceil(dt / 4))
        num_clock_cycles = np.arange(dcycle, max_pulse_len / 4 + 0.1, dcycle, dtype=int)

        rabi_program = cQED_programs.temporal_rabi(attr.ro_el, attr.qb_el, qb_gain, attr.qb_therm_clks, num_clock_cycles, pulse, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(rabi_program, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["pulse_durations"] = num_clock_cycles * 4
        self.save_output(output, "temporalRabi")
        return output

    def power_rabi(self, max_gain: int, dg: int = 1e-3, pulse="x180", length:int=None, n_avg: int = 1000):
        attr = self.attributes
        gains = np.arange(-max_gain, max_gain + 1e-12, dg, dtype=float)

        if not length:
            pulseInfo = self.pulseOpMngr.get_op_waveforms(attr.qb_el, pulse)
            length = pulseInfo.length
        pulse_clock_len = round(length / 4)
        power_rabi_prog = cQED_programs.power_rabi(attr.ro_el, attr.qb_el, pulse_clock_len, gains, attr.qb_therm_clks, pulse, n_avg)
        
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(power_rabi_prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["gains"] = gains
        self.save_output(output, "powerRabi")
        return output

    def single_qb_rotations(self, rotations: list[str]=["x180"], n_avg=1000):
        attr = self.attributes

        qb_rot_prog = cQED_programs.single_qb_rotations(attr.ro_el, attr.qb_el, rotations, attr.qb_therm_clks, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(qb_rot_prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        return output
    
    def T1_relaxation(self, max_delay_time: int, dt: int, r180="x180", n_avg: int = 1000):
        attr = self.attributes
        dcycle = int(np.ceil(dt / 4))
        wait_cycles_list = np.arange(4, max_delay_time / 4 + 1, dcycle, dtype=int)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        T1_prog = cQED_programs.T1_relaxation(attr.ro_el, attr.qb_el, r180, wait_cycles_list, attr.qb_therm_clks, n_avg)

        output = self.quaProgMngr.run_program(T1_prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["delays"] = wait_cycles_list * 4
        self.save_output(output, "T1Relaxation")
        return output

    def T2_ramesy(self, qb_detune: int, max_delay_time: int, dt: int, r90="x90", n_avg: int = 1000):
        attr = self.attributes
        dcycle = int(np.ceil(dt / 4))
        wait_cycles_list = np.arange(dcycle, max_delay_time / 4 + 1, dcycle, dtype=int)
        if qb_detune > ConfigSettings.MAX_IF_BANDWIDTH:
            raise ValueError("qb detune can't exceed maximum IF bandwidth")
        else:
            self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq + qb_detune)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        T2_ramsey_prog = cQED_programs.T2_ramesy(attr.ro_el, attr.qb_el, r90, wait_cycles_list, attr.qb_therm_clks, n_avg)
        output = self.quaProgMngr.run_program(T2_ramsey_prog, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["delays"] = wait_cycles_list * 4
        self.save_output(output, "T2Ramsey")
        return output

    def T2_echo(self, max_delay_time: int, dt: int, r180="x180", r90="x90", n_avg: int = 1000):
        attr = self.attributes
        dcycle = int(np.ceil(dt / 8))
        half_wait_cycles_list = np.arange(dcycle, max_delay_time / 8 + 1, dcycle, dtype=int)
        T2_echo_prog = cQED_programs.T2_echo(attr.ro_el, attr.qb_el, r180, r90, half_wait_cycles_list, attr.qb_therm_clks, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(T2_echo_prog, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["delays"] = half_wait_cycles_list * 8
        self.save_output(output, "T2Echo")
        return output

    def time_rabi_chevron(self, if_span, df, max_pulse_duration, dt, pulse="gaussian_X", pulse_gain=1.0, n_avg: int = 1000):
        attr = self.attributes
        qb_if = self.quaProgMngr.get_element_if(attr.qb_el, attr.qb_fq,  self.quaProgMngr.get_element_lo(attr.qb_el))

        if_dfs = np.arange(-if_span/2, if_span/2 + 0.1, df, dtype=int)
        duration_clks = np.arange(4, max_pulse_duration / 4 + 1, dt, dtype=int)
        rabi_chevron_duration = cQED_programs.time_rabi_chevron(attr.ro_el, attr.qb_el, pulse, pulse_gain, qb_if, if_dfs, duration_clks, attr.qb_therm_clks, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(rabi_chevron_duration, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["durations"] = duration_clks*4
        output["detunings"] = if_dfs
        self.save_output(output, "rabiChevronTime")
        return output
    
    def power_rabi_chevron(self, if_span, df, max_gain, dg, pulse="gaussian_X", pulse_duration=100, n_avg: int = 1000):
        attr = self.attributes
        qb_if = self.quaProgMngr.get_element_if(attr.qb_el, attr.qb_fq,  self.quaProgMngr.get_element_lo(attr.qb_el))
        if_dfs = np.arange(-if_span/2, if_span/2 + 0.1, df, dtype=int)

        gains = np.arange(-max_gain, max_gain + 1e-12, dg, dtype=float)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        rabi_chevron_amplitude = cQED_programs.power_rabi_chevron(attr.ro_el, attr.qb_el, pulse, pulse_duration, qb_if, if_dfs, gains, attr.qb_therm_clks, n_avg)
        output = self.quaProgMngr.run_program(rabi_chevron_amplitude, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["gains"] = gains
        output["detunings"] = if_dfs
        self.save_output(output, "rabiChevronAmplitude")
        return output

    def ramsey_chevron(self, if_span, df, max_delay_duration, dt, r90="x90", n_avg: int = 1000):
        attr = self.attributes
        qb_if = self.quaProgMngr.get_element_if(attr.qb_el, attr.qb_fq,  self.quaProgMngr.get_element_lo(attr.qb_el))

        if_dfs = np.arange(-if_span/2, if_span/2 + 0.1, df, dtype=int)
        delay_clks = np.arange(0, max_delay_duration / 4 + 1, dt, dtype=int)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        ramsey_chevron_duration = cQED_programs.ramsey_chevron(attr.ro_el, attr.qb_el, r90, qb_if, if_dfs, delay_clks, attr.qb_therm_clks, n_avg)

        output = self.quaProgMngr.run_program(ramsey_chevron_duration, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["delays"] = delay_clks*4
        output["detunings"] = if_dfs
        self.save_output(output, "ramseyChevronAmplitude")
        return output
    
    def all_XY(self, n_avg=1000):
        attr = self.attributes
        ops = (
            ["zero", "zero"], ["x180", "x180"], ["y180", "y180"], ["x180", "y180"], ["y180", "x180"],

            ["x90", "zero"],["y90", "zero"],
            ["x90", "y90"], ["y90", "x90"], ["x90", "y180"], ["y90", "x180"], ["x180", "y90"], ["y180", "x90"],
            ["x90", "x180"],["x180", "x90"],["y90", "y180"], ["y180", "y90"],

            ["x180", "zero"], ["y180", "zero"],["x90", "x90"], ["y90", "y90"]
        )
        all_xy_program = cQED_programs.all_xy(attr.ro_el, attr.qb_el, ops, attr.qb_therm_clks, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(all_xy_program, n_total=n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["ops"] = ops
        self.save_output(output, "allXY")
        return output

    def IQ_proj_calibration(self, r180, pulse_len=1000, n_samples=10000):
        output = self.iq_blob(r180, n_runs=n_samples)
        cQED_programs.measureMacro.set_IQ_mod(I_mod_weights=["cos", "sin"], Q_mod_weights=["minus_sin", "cos"])
        S_g, S_e = output.extract("S_g", "S_e")

        angle, threshold, fidelity, gg, ge, eg, ee = two_state_discriminator(S_g.real, S_g.imag, S_e.real, S_e.imag, b_plot=False)

        pulse_len = 1000
        w_plus_cos = np.cos(-angle)
        w_minus_cos = -np.cos(-angle)
        w_plus_sin = np.sin(-angle)
        w_minus_sin = -np.sin(-angle) 

        self.pulseOpMngr.add_int_weight("rot_cosine", w_plus_cos, w_minus_sin, pulse_len, persist=True)
        self.pulseOpMngr.add_int_weight("rot_sine", w_plus_sin, w_plus_cos, pulse_len, persist=True)
        self.pulseOpMngr.add_int_weight("rot_m_sine", w_minus_sin, w_minus_cos, pulse_len, persist=True)
        pulseOp = PulseOp("resonator", "readout_pulse", "readout", int_weights={"rot_cos": "rot_cosine", 
                                                                                "rot_sin": "rot_sine", 
                                                                                "rot_m_sin": "rot_m_sine",
                                                                                "cos": "cosine_weights",
                                                                                "sin": "sine_weights",
                                                                                "minus_sin": "minus_sine_weights"                                                                        
                                                                                })

        self.pulseOpMngr.modify_pulse_op(pulseOp, persist=True)
        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr)

        cQED_programs.measureMacro.set_IQ_mod(I_mod_weights=["rot_cos", "rot_sin"], Q_mod_weights=["rot_m_sin", "rot_cos"])
        cQED_programs.measureMacro.set_threshold(threshold)
        print("Runnig Validation...")
        output = self.iq_blob(r180, n_runs=int(n_samples/10))
        S_g, S_e = output.extract("S_g", "S_e")
        
        plot_IQ([S_g, S_e],["|g>", "|e>"], s=1)

        Q_diff = np.average(S_e.imag) - np.average(S_g.imag)
        Q_std_avg = (np.std(S_e.imag) + np.std(S_g.imag))/2

        if abs(Q_diff) < abs(0.1*Q_std_avg):
            self.save_pulses()
        else:
            print("Calibration failed, please check the results: Q_diff = ", np.abs(Q_diff), "Q_diff_var = ", Q_std_avg)
        return output

    def calibrate_qb_experiment(self, S_volts):
        def line_func(x, m, b):
            return m*x + b

        fit_params_line = generalized_fit(S_volts.real, S_volts.imag, line_func, [0,0], plotting=False)
        m, b = fit_params_line[0]
        z_rotation = np.exp(-1j*np.arctan(m))
        
        I_min = min((S_volts * z_rotation).real)
        I_max = max((S_volts * z_rotation).real)

        scale = 2.0 / (I_max - I_min)
        rotation_op = z_rotation * scale
        offset = (I_max+I_min) / (I_max-I_min) 
        amplitudes = (S_volts * rotation_op).real - offset
        
        plot_IQ(S_volts.real, S_volts.real, "pre-scaled amplitude (S_volts)")
        plot_IQ([S_volts.real* scale, amplitudes.real], 
            [S_volts.imag* scale, amplitudes.imag],
            ["scaled amplitude (S_volts*scale)", "calibrated amplitude"])
        
        print(f"calibrated rotation_op, offset={rotation_op},{offset}")
        self.set_cQED_param("qb_calibration", [rotation_op, offset])

        plt.show()
  
    def readout_opt(self, min_len, max_len, dlen, g_span, dg, r180="x180", base_voltage=0.01,  n_avg: int = 100):
        attr = self.attributes

        ro_gains = np.arange(0, g_span + 1e-12, dg, dtype=float)
        ro_lens = np.arange(min_len, max_len + 1e-12, dlen, dtype=int)
        
        ro_pulses = [f"readout_{pulse_len}_pulses" for pulse_len in ro_lens]
        ro_ops = [f"readout_{pulse_len}" for pulse_len in ro_lens]
        for pulse_len, ro_pulse, ro_op, in zip(ro_lens, ro_pulses, ro_ops):

            self.pulseOpMngr.add_int_weight(f"cosine_{pulse_len}", 1.0, 0.0, pulse_len, persist=False)
            self.pulseOpMngr.add_int_weight(f"sine_{pulse_len}", 0.0, 1.0, pulse_len, persist=False)
            self.pulseOpMngr.add_int_weight(f"m_sine_{pulse_len}", 0.0, -1.0, pulse_len, persist=False)

            pulseOp = PulseOp(attr.ro_el, ro_pulse, ro_op, "measurement", length=pulse_len, 
                              I_wf_name=f"readout_I_wf_{pulse_len}" , Q_wf_name=f"readout_Q_wf_{pulse_len}", I_wf=base_voltage, Q_wf=0,
                              int_weights={f"cos": f"cosine_{pulse_len}", 
                                           f"sin": f"sine_{pulse_len}", 
                                           f"minus_sin": f"m_sine_{pulse_len}"})

            self.pulseOpMngr.register_pulse_op(pulseOp, override=True, persist=False)
            
        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr, include_volatile=True)
        
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)  
        ro_opt_program = cQED_programs.readout_optimization(attr.ro_el, attr.qb_el, ro_ops, ro_gains, r180, attr.qb_therm_clks, n_avg)
        output = self.quaProgMngr.run_program(ro_opt_program, n_avg, demod_len=ro_lens, axis=1)
        #output = self.program_manager.run_program(ro_opt_program, n_avg, demodulate=True)
        output["ro_lens"] = ro_lens
        output["amplitudes"] = base_voltage*ro_gains
        self.save_output(output, "readoutOpt")
        return output
    
    def qubit_readout_leakage_benchmarking(self, control_bits, r180="x180", num_sequences=10, n_avg=1000):
        attr = self.attributes
        rlb_prog = cQED_programs.readout_leakage_benchmarking(attr.ro_el, attr.qb_el, r180, control_bits, attr.qb_therm_clks, num_sequences, n_avg)
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)  
        output = self.quaProgMngr.run_program(rlb_prog, num_sequences, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["control_bits"] = control_bits
        
        self.save_output(output, "qubitReadoutLeakage")
        return output
    
    def calibrate_drag_coeff(self, coeff_amp_list, n_avg):
        attr = self.attributes
        x180, y90 = ["x180", "y90"]
        y180, x90 = ["y180", "x90"]
        drag_prog = cQED_programs.drag_calibration(attr.ro_el, attr.qb_el, coeff_amp_list, x180, x90, y180, y90, 
                                                   attr.qb_therm_clks, n_avg)
        
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(drag_prog, 2*len(coeff_amp_list), )
        return output
    
    def pulsed_resonator_spectroscopy(self, start_freq, end_freq, df, 
                                      pulse_gain, pulse_len, pulse="gaussian_X", n_avg:int=1000):
        attr = self.attributes
        if_frequencies = create_if_frequencies(attr.ro_el, start_freq, end_freq, df)
        pulsed_ro_program = cQED_programs.pulsed_resonator_spectroscopy(attr.ro_el, attr.qb_el, if_frequencies, 
                                                                        pulse, pulse_gain, pulse_len, 
                                                                        attr.qb_therm_clks, n_avg)
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(pulsed_ro_program, n_avg, )
        lo_freq =  self.quaProgMngr.get_element_lo(attr.qb_el)
        output["frequencies"] = lo_freq + if_frequencies
        self.save_output(output, "excitedRoSpectroscopy")
        return output

    def storage_spectroscopy(self, rf_begin, rf_end, df, storage_therm_time, n_avg=1000):
        attr = self.attributes
        if_frequencies = create_if_frequencies(attr.st_el, rf_begin, rf_end, df, lo_freq=self.quaProgMngr.get_element_lo(attr.st_el))
        lo_freq =  self.quaProgMngr.get_element_lo(attr.st_el)

        storage_spec_prog = cQED_programs.storage_spectroscopy(attr.ro_el, attr.qb_el, attr.st_el, if_frequencies, storage_therm_time, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(storage_spec_prog, n_avg,  processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["frequencies"] = lo_freq + if_frequencies
        return output

    def storage_spectroscopy_coarse(self, rf_begin: float, rf_end: float, df: float, storage_therm_time: int, n_avg: int = 1000):
        attr = self.attributes
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        lo_list = _make_lo_segments(rf_begin, rf_end)
        results, all_freqs = [], []
        for LO in lo_list:
            self.quaProgMngr.set_element_lo(attr.st_el, LO)
            if_freqs = _if_frequencies_for_segment(LO, rf_end, df)
            prog = cQED_programs.storage_spectroscopy(
                attr.ro_el,
                attr.qb_el,
                attr.st_el,
                if_freqs,
                storage_therm_time,
                n_avg
            )

            out = self.quaProgMngr.run_program(prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
            freqs = LO + if_freqs
            out["frequencies"] = freqs
            results.append(out)
            all_freqs.append(freqs)
        final = _merge_segments(results, all_freqs)
        self.save_output(final, "storageWideSpectroscopy")
        return final

    def time_storage_displacement(self, t_begin, t_end, dt=1000, qb_frequency=None, disp_pulse="const_disp", sel_r180_pulse="x180_long", n_avg: int = 1000):
        attr = self.attributes
        if qb_frequency:
            qb_fq = qb_frequency
        TIME_PER_CLOCK_CYCLE = ConfigSettings.TIME_PER_CLOCK_CYCLE
        duration_clks = np.arange(t_begin, t_end + 1, dt, dtype=int) // TIME_PER_CLOCK_CYCLE
        storage_displacement_prog = cQED_programs.time_storage_displacement(attr.ro_el, attr.qb_el, attr.st_el, disp_pulse, sel_r180_pulse, duration_clks, attr.st_therm_clks, n_avg)
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(storage_displacement_prog, n_avg, )
        output["durations"] = duration_clks * TIME_PER_CLOCK_CYCLE
        self.save_output(output, "storageDisplacement")
        return output
    
    def num_splitting_spectroscopy(self, rf_centers, rf_spans, df, disp_pulse="const_alpha", sel_r180_pulse="sel_x180" ,n_avg: int = 1000):
        if not isinstance(rf_centers, (list, tuple, np.ndarray)):
            rf_centers = [rf_centers]
        if not isinstance(rf_spans, (list, tuple, np.ndarray)):
            rf_spans = [rf_spans]

        if len(rf_centers) != len(rf_spans):
            raise ValueError("rf_centers and rf_spans must have the same length")
        attr = self.attributes

        qb_lo_frequency = self.quaProgMngr.get_element_lo(attr.qb_el)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq) 
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)    

        all_outputs = []
        for rf_center, rf_span in zip(rf_centers, rf_spans):
            self.quaProgMngr.set_element_fq(attr.qb_el, rf_center)
            rf_begin, rf_end = rf_center-rf_span/2, rf_center+rf_span/2
            qb_ifs = create_if_frequencies(attr.qb_el, rf_begin, rf_end, df, lo_freq= self.quaProgMngr.get_element_lo(attr.qb_el))

            num_split_spec_prog = cQED_programs.num_splitting_spectroscopy(attr.ro_el, attr.qb_el, attr.st_el, disp_pulse, sel_r180_pulse, qb_ifs, attr.st_therm_clks, n_avg)
            output = self.quaProgMngr.run_program(num_split_spec_prog, n_avg,  processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
            output["frequencies"] = qb_ifs + qb_lo_frequency
            all_outputs.append(Output(output))
        final_output = Output.merge(all_outputs)
        self.save_output(final_output, "numSplitSpecSpectroscopy")
        return final_output
    

    def iq_blob(self, r180, n_runs: int = 1000):
        attr = self.attributes
        iq_blob_prog = cQED_programs.iq_blobs(attr.ro_el, attr.qb_el, r180, attr.qb_therm_clks, n_runs)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        output = self.quaProgMngr.run_program(iq_blob_prog, n_runs)

        S = output["S"]
        output["S_g"] = S[:, 0]
        output["S_e"] = S[:, 1]

        return output

    def storage_power_rabi(self, probe_qb_fq, max_gain: int, dg: int = 1e-3, disp_pulse="const_alpha", s_r180_pulse="sel_x180", n_avg: int = 1000):
        attr = self.attributes
        gains = np.arange(-max_gain, max_gain + 1e-12, dg, dtype=float)
        storage_power_rabi_prog = cQED_programs.storage_power_rabi(attr.ro_el, attr.qb_el, attr.st_el, s_r180_pulse, disp_pulse, attr.qb_therm_clks, gains, n_avg)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, probe_qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)
        output = self.quaProgMngr.run_program(storage_power_rabi_prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["gains"] = gains
        self.save_output(output, "storagePowerRabi")
        return output


    def storage_gates_num_splitting(self, gates: list[Gate], probe_fqs, sel_r180="sel_x180", n_avg: int = 100):
        attr = self.attributes

        qb_lo_frequency = self.quaProgMngr.get_element_lo(attr.qb_el)


        fock_ifs = self.quaProgMngr.calculate_el_if_fq(attr.qb_el, probe_fqs, lo_freq=qb_lo_frequency)

        qb_if = self.quaProgMngr.calculate_el_if_fq(attr.qb_el, attr.qb_fq, lo_freq=qb_lo_frequency)

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)   

        gates_num_split_prog = cQED_programs.storage_gates_num_splitting(attr.ro_el, attr.st_el, attr.qb_el, gates, qb_if, fock_ifs, sel_r180, attr.st_therm_clks, n_avg)
        output = self.quaProgMngr.run_program(gates_num_split_prog, n_avg, processors=[qubit_demodulator], normalize_params=attr.norm_IQ)
        output["probe_fqs"] = probe_fqs
        output["gates"] = [gate.name for gate in gates]
        return output
    
    def storage_phase_evolution(self, n, fock_probe_fqs, theta_np_array, snap_np_list, delay_clks, max_n_drive=12,
                                disp_alpha=None, disp_epsilon=None, sel_r180_pulse="sel_x180", n_avg=200):
        
        def choose_displacements(n: int,
                                alpha_cap: float = 6.0,    # upper-bound for |α|
                                eps_abs: float  = 0.10):   # fixed |ε|  (linear regime)
            alpha_amp = np.sqrt(n + 0.5)
            alpha_amp = min(alpha_amp, alpha_cap)
            return alpha_amp, eps_abs

        alpha_amp, eps_amp = choose_displacements(n)
        if disp_alpha is None:
            disp_alpha   = Displacement(alpha = alpha_amp)
            print(f"[info] |α| = {alpha_amp:.3f}")
        if disp_epsilon is None:
            disp_epsilon = Displacement(alpha = eps_amp)
            print(f"[info] |ε| = {eps_amp:.3f}")

        if not snap_np_list:
            snap_np_list = []
            for theta_np in theta_np_array:
                theta_np_vec = np.zeros(max_n_drive)

                theta_np_vec[n+1] = theta_np
                snap_np = SNAP(theta_np_vec, kerr_correction=False)
                snap_np_list.append(snap_np.name)

        attr = self.attributes

        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr)

        fock0_if = self.quaProgMngr.calculate_el_if_fq(attr.qb_el, attr.qb_fq)
        fock_probe_ifs = self.quaProgMngr.calculate_el_if_fq(attr.qb_el, fock_probe_fqs)
        
        prog = cQED_programs.phase_evolution_prog(attr.ro_el, attr.qb_el, attr.st_el,
                                    disp_alpha.name, disp_epsilon.name, sel_r180_pulse, 
                                    fock0_if, fock_probe_ifs,
                                    delay_clks, snap_np_list, attr.st_therm_clks, n_avg)
        
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)     
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)

        output = self.quaProgMngr.run_program(
                prog, n_avg,
                processors=[qubit_demodulator],
                normalize_params=attr.norm_IQ)

        output["delays"] = np.array(delay_clks)*4
        output["thetas"] = np.array(theta_np_array)
        output["fock_probe_fqs"] = fock_probe_fqs
        output["fock_n"] = n
        output["max_n_drive"] = max_n_drive
        self.save_output(output, "phaseEvolution")
        return output

    def storage_wigner_tomography(self, gates: list[Gate], x_vals, p_vals, base_alpha=10, r90_pulse="x90",n_avg=200):
        attr = self.attributes
         

        base_disp = Displacement(base_alpha).build()

        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr)

        parity_wait_clks = np.pi/(abs(attr.st_chi))*1e9/4
        parity_wait_clks = 4 * round(parity_wait_clks/4)
        prog = cQED_programs.storage_wigner_tomography(gates, attr.st_el, attr.qb_el, attr.ro_el, base_disp, 
                                                       x_vals, p_vals, base_alpha, r90_pulse, parity_wait_clks, 
                                                       attr.st_therm_clks, n_avg)
        
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)

        output = self.quaProgMngr.run_program(
                prog, n_avg,
                processors=[qubit_demodulator],
                normalize_params=attr.norm_IQ)
        
        output["x_vals"] = x_vals
        output["p_vals"] = p_vals

        gate_names = [gate.name for gate in gates]
        output["gates"] = gate_names
        self.save_output(output, "storageWignerTomography")
        return output 
    
    def storage_chi_ramsey(
        self,
        fock_fq,
        delay_ticks,
        disp_pulse: str = "const_alpha",
        x90_pulse: str = "x90",
        n_avg: int = 200
    ):
        """
        Wrapper for the Ramsey‐based χ measurement.

        Parameters
        ----------
        qb_fq : float
            Qubit frequency (Hz) to set before the experiment.
        disp_pulse : str, optional
            Name of the cavity displacement pulse to inject photons.
        x90_pulse : str, optional
            Name of the π/2 qubit pulse.
        delay_ticks : Sequence[int]
            List or array of wait‐times (in clock ticks) for the Ramsey τ sweep.
        n_avg : int, optional
            Number of averages (repetitions) per τ point.
        """
        attr = self.attributes

        # build the QUA program
        prog = cQED_programs.storage_chi_ramsey(
            attr.ro_el,
            attr.qb_el,
            attr.st_el,
            disp_pulse,
            x90_pulse,
            delay_ticks,
            attr.st_therm_clks,
            n_avg
        )

        # set element frequencies
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, fock_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)

        # run and demodulate
        output = self.quaProgMngr.run_program(
            prog,
            n_avg,
            processors=[qubit_demodulator],
            normalize_params=attr.norm_IQ
        )

        # annotate and save
        output["delay_ticks"] = np.array(delay_ticks)
        self.save_output(output, "storageChiRamsey")

        return output
    
    def storage_ramsey(
        self,
        delay_ticks,
        st_detune = 0,
        disp_pulse: str = "const_alpha",
        sel_r180: str = "sel_x180",
        n_avg: int = 200
    ):

        attr = self.attributes
        prog = cQED_programs.storage_ramsey(
            attr.ro_el,
            attr.qb_el,
            attr.st_el,
            disp_pulse,
            sel_r180,
            delay_ticks,
            attr.st_therm_clks,
            n_avg
        )

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq + st_detune)

        output = self.quaProgMngr.run_program(
            prog,
            n_avg,
            processors=[qubit_demodulator],
            normalize_params=attr.norm_IQ
        )

        output["delay_ticks"] = np.array(delay_ticks)
        self.save_output(output, "storageRamsey")

        return output
    
    def storage_kerr_ramsey(
        self,
        delay_ticks,
        alpha_list,
        st_detune = 0,
        base_alpha = 10,
        sel_r180: str = "sel_x180",
        n_avg: int = 200
    ):

        base_disp = Displacement(base_alpha).build()
        self.quaProgMngr.burn_pulse_to_qm(self.pulseOpMngr)

        attr = self.attributes

        gain_list = alpha_list/base_alpha
        prog = cQED_programs.storage_kerr_ramsey(
            attr.ro_el,
            attr.qb_el,
            attr.st_el,
            base_disp,
            gain_list,
            sel_r180,
            delay_ticks,
            attr.st_therm_clks,
            n_avg
        )

        # set element frequencies
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq + st_detune)

        output = self.quaProgMngr.run_program(
            prog,
            n_avg,
            processors=[qubit_demodulator],
            normalize_params=attr.norm_IQ
        )
        output["delays"] = np.array(delay_ticks)*4
        output["alphas"] = alpha_list
        self.save_output(output, "storageKerrRamsey")

        return output
    
    def continous_waveform(self, pulse, element, truncate):
        attr = self.attributes
        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)

        truncate_clks = truncate // 4
        prog = cQED_programs.continuous_wave(element, pulse, truncate_clks)

        output = self.quaProgMngr.run_program(
            prog
        )

        return output
    
    def storage_selective_ramsey_phase(
            self,
            snap_gate_name: str,          # e.g. "SNAP_theta0_0_0"
            sel_fock_fqs,                      
            ramsey_phases,
            disp_pulse = "const_alpha",
            sel_pi_pulse: str = "sel_x180",
            x90_pulse: str   = "x90",
            n_avg: int       = 200,
    ):
        attr = self.attributes

        self.burn_pulses()

        sel_IFs = self.quaProgMngr.calculate_el_if_fq(attr.qb_el, sel_fock_fqs)
        prog = cQED_programs.selective_ramsey_phase(
                attr.st_el,
                attr.qb_el,
                attr.ro_el,
                sel_pi_pulse,
                sel_IFs,
                snap_gate_name,
                disp_pulse,
                ramsey_phases,
                x90_pulse,
                attr.st_therm_clks,
                n_avg          = n_avg,
            )

        self.quaProgMngr.set_element_fq(attr.ro_el, attr.ro_fq)
        self.quaProgMngr.set_element_fq(attr.qb_el, attr.qb_fq)   # base qb freq
        self.quaProgMngr.set_element_fq(attr.st_el, attr.st_fq)

        output = self.quaProgMngr.run_program(
                    prog,
                    n_avg,
                    processors=[qubit_demodulator],
                    normalize_params=attr.norm_IQ,
                )

        output["sel_IFs"]       = np.array(sel_IFs)
        output["ramsey_phases"] = np.array(ramsey_phases)
        output["snap_gate"]     = snap_gate_name
        output["displacement"] = disp_pulse

        self.save_output(output, "selectiveRamseyPhase")
        return output
    