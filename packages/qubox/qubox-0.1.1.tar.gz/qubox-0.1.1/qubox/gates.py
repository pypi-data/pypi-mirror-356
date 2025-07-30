from abc import ABC, abstractmethod
from .pulse_manager import PulseOperationManager, PulseOp
from .analysis.analysis_tools import array_to_md5
from qm import qua
from dataclasses import dataclass
from typing import Optional
import numpy as np

import json, pathlib


_GATE_REGISTRY: dict[str, type["Gate"]] = {}   # class-name → class

@dataclass
class GateAttributes:
    r180_len:           Optional[int] = None
    x180_id:            Optional[str] = None
    y180_id:            Optional[str] = None
    disp_alpha_id:      Optional[str] = None
    disp_alpha:         Optional[float] = None
    chi:                Optional[float] = None
    chi2:               Optional[float] = None
    chi3:               Optional[float] = None
    K:                  Optional[float] = None
    K2:                 Optional[float] = None
    dt_s:               Optional[float] = 1e-9
    snap_phase_corr:    Optional[list] = None

class Gate(ABC):
    attributes: GateAttributes = GateAttributes()
    mgr: PulseOperationManager = None

    def __init__(self, name: str, target: str):
        self.name = name
        self.target = target

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        _GATE_REGISTRY[cls.__name__] = cls       

    def to_dict(self):
        return {
            "type"  : self.__class__.__name__,
            "name"  : self.name,           #  ← store it
            "target": self.target,
            "params": self._serialize_params(),
        }
    
    @classmethod
    def from_dict(cls, d, mgr=None):
        g_cls = _GATE_REGISTRY[d["type"]]
        obj   = g_cls.__new__(g_cls)
        obj.__dict__["target"] = d["target"]
        obj.__dict__["name"]   = d["name"]      #  ← restore it

        if mgr is not None:
            g_cls.set_attributes(mgr)
            obj._deserialize_params(d["params"])
            obj.build()
        else:
            obj._deserialize_params(d["params"])
        return obj
    
    @classmethod
    def set_attributes(cls,  mgr: PulseOperationManager, attributes: GateAttributes = None):
        if attributes is not None:
            cls.attributes = attributes
        else:
            if mgr:
                cls.attributes.r180_len = mgr.get_pulse_length("x180_pulse")
                cls.attributes.x180_id = "x180_pulse"
                cls.attributes.y180_id = "y180_pulse"
            else:
                raise ValueError("Either attributes or pulseOpManager must be provided.")
        cls.mgr = mgr 

    @abstractmethod
    def _serialize_params(self)   -> dict: ...

    @abstractmethod
    def _deserialize_params(self, P: dict): ...

    @abstractmethod
    def play(self): ...
    
    @abstractmethod
    def build(self, mgr: PulseOperationManager): ...

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name}>"

class Rotation(Gate):
    def __init__(self, theta:float, phi:float, target: str = "qubit", build=False):
        super().__init__(name=f"Rotation_{theta}_{phi}", target=target)

        self.theta = theta
        self.phi = phi

        if build:
            self.build()

    def _serialize_params(self):
        return {"theta": float(self.theta), "phi": float(self.phi)}

    def _deserialize_params(self, P):
        self.theta = P["theta"]
        self.phi   = P["phi"]

    def play(self):
        qua.play(self.name, self.target) 
        qua.align()

    def build(self, xid=None, yid=None):
        # 1) fetch both the X180 and Y180 I/Q shapes
        mgr = type(self).mgr
        if not xid:
            xid = "x180_pulse"
        if not yid:
            yid = "y180_pulse"

        I_x, Q_x = mgr.get_pulse_waveforms(xid)
        I_y, Q_y = mgr.get_pulse_waveforms(yid)

        # 2) compute your mixing coefficients
        α = self.theta/np.pi
        cx = α * np.cos(self.phi)
        cy = α * np.sin(self.phi)

        # 3) mix & scale both X and Y shapes
        def mix(a, b, ca, cb):
            # a and b are floats or lists; ca, cb scalars
            if isinstance(a, (float,int)) and isinstance(b, (float,int)):
                return ca*a + cb*b
            # otherwise assume both are lists of same length
            return [ca*aa + cb*bb for aa,bb in zip(a, b)]

        I_new = mix(I_x, I_y, cx, cy)
        Q_new = mix(Q_x, Q_y, cx, cy)

        # 4) register these I/Q waveforms as before
        I_name = f"{self.name}_I"
        Q_name = f"{self.name}_Q"
        kind_I = "constant" if isinstance(I_new, (float,int)) else "arbitrary"
        kind_Q = "constant" if isinstance(Q_new, (float,int)) else "arbitrary"
        mgr.add_waveform(I_name, kind_I, I_new, persist=False)
        mgr.add_waveform(Q_name, kind_Q, Q_new, persist=False)

        # 5) grab length & marker from your base X pulse (or Y—they match)
        base = mgr._perm.pulses[xid]
        length = base["length"]
        marker = base.get("digital_marker","ON")

        # 6) register the new pulse
        p = PulseOp(
            element_name   = self.target,
            pulse_name     = f"{self.name}_pulse",
            op_identifier  = self.name,
            op_type        = "control",
            length         = length,
            digital_marker = marker,
            I_wf_name      = I_name,
            Q_wf_name      = Q_name,
            I_wf           = I_new,
            Q_wf           = Q_new,
        )
        mgr.register_pulse_op(p, override=True, persist=False)
        return self.name


class Displacement(Gate):
    def __init__(self, alpha: complex, target: str = "storage", build=False):
        name = f"Disp_{alpha.real:+.3f}_{alpha.imag:+.3f}"
        super().__init__(name=name, target=target)
        self.alpha = complex(alpha)            # ensure complex dtype
        
        if build:
            self.build()

    def _serialize_params(self):
        # JSON cannot handle complex numbers → store re / im separately
        return {
            "re": float(self.alpha.real),
            "im": float(self.alpha.imag),
        }

    def _deserialize_params(self, P):
        self.alpha = complex(P["re"], P["im"])

    def play(self):
        qua.play(self.name, self.target)
        qua.align()

    def build(self):
        mgr = type(self).mgr                   # PulseOperationManager

        # --- calibrated template --------------------------------------
        tpl_id      = self.attributes.disp_alpha_id   # e.g. "disp_alpha_1.0"
        I_tpl, Q_tpl = mgr.get_pulse_waveforms(tpl_id)

        base        = mgr._perm.pulses[tpl_id]
        length      = base["length"]
        marker      = base.get("digital_marker", "ON")

        # --- scaling & rotation ---------------------------------------
        alpha_ref   = complex(self.attributes.disp_alpha)  # template amplitude
        ratio       = self.alpha / alpha_ref               # complex scale
        c, s        = ratio.real, ratio.imag               # Re, Im

        # rotate IQ template:  (I+iQ)·ratio  →  (c·I - s·Q ,  s·I + c·Q)
        I_new = c * np.asarray(I_tpl) - s * np.asarray(Q_tpl)
        Q_new = s * np.asarray(I_tpl) + c * np.asarray(Q_tpl)

        # --- register waveforms ---------------------------------------
        I_name = f"{self.name}_I"
        Q_name = f"{self.name}_Q"

        kind_I = "constant"  if np.ndim(I_new)==0 else "arbitrary"
        kind_Q = "constant"  if np.ndim(Q_new)==0 else "arbitrary"

        mgr.add_waveform(I_name, kind_I, I_new.tolist(), persist=False)
        mgr.add_waveform(Q_name, kind_Q, Q_new.tolist(), persist=False)

        # --- register pulse -------------------------------------------
        pulse = PulseOp(
            element_name   = self.target,
            pulse_name     = f"{self.name}_pulse",
            op_identifier  = self.name,
            op_type        = "control",
            length         = length,
            digital_marker = marker,
            I_wf_name      = I_name,
            Q_wf_name      = Q_name,
            I_wf           = I_new.tolist(),
            Q_wf           = Q_new.tolist(),
        )
        mgr.register_pulse_op(pulse, override=True, persist=False)
        return self.name

class SNAP(Gate):
    def __init__(self, angles, target="qubit", apply_corrections=True, build=False):
        self.apply_corrections = bool(apply_corrections)
        self.raw_angles        = np.asarray(angles, dtype=float)
        self.angles            = self.raw_angles.copy()
  

        flag    = 1.0 if self.apply_corrections else 0.0
        name_payload = np.concatenate([self.angles, [flag]])
        super().__init__(name=f"SNAP_{array_to_md5(name_payload)}", target=target)

        if build:
            self.build()

    def _refresh_name(self):
        flag = 1.0 if self.apply_corrections else 0.0
        payload = np.concatenate([self.angles, [flag]])
        self.name = f"SNAP_{array_to_md5(payload)}"

    def _serialize_params(self) -> dict:
        """
        Keep only the info required to rebuild the gate:
        • raw angle list (already padded if corrections were applied)
        • whether those corrections were applied
        """
        return {
            "angles"           : self.raw_angles.tolist(),   # NOT padded
            "apply_corrections": self.apply_corrections,
        }

    def _deserialize_params(self, P: dict) -> None:
        """
        Restore internal state *exactly* as it was at save-time, then
        regenerate the `name` hash that depends on (angles + flag).
        """
        # 1) core parameters ----------------------------------------------
        self.apply_corrections = bool(P["apply_corrections"])
        self.raw_angles        = np.asarray(P["angles"], dtype=float)
        self.angles            = self.raw_angles.copy()  # build() will pad if needed

        flag    = 1.0 if self.apply_corrections else 0.0
        payload = np.concatenate([self.raw_angles, [flag]])
        self.name = f"SNAP_{array_to_md5(payload)}"

    # ------------------------------------------------------------------
    def play(self):
        qua.play(self.name, self.target)
        qua.align()

    # ------------------------------------------------------------------
    def build(self):
        """Construct and register the multiplexed 2‑π SNAP waveform."""
            
        mgr  = type(self).mgr
        att  = type(self).attributes     # to shorten lines

        # ------- dispersive frequencies of the cavity Fock ladder -----------
        chi  = float(att.chi)            # Hz   (line-to-line spacing)
        chi2 = float(att.chi2)
        chi3 = float(att.chi3)

        # ------- Kerr coefficients (optionally disabled) --------------------
        
        #K = float(att.K)              # Hz
        #K2 = float(att.K2)
        K = K2 = 0.0

        dt   = float(att.dt_s)           # AWG sampling period (s)

        # ---------- fetch the calibrated selective π templates ----------
        xid, yid = "sel_x180_pulse", "sel_y180_pulse"
        I_x0, Q_x0 = mgr.get_pulse_waveforms(xid)
        I_y0, Q_y0 = mgr.get_pulse_waveforms(yid)

        # ensure a 4-sample multiple for HW timing
        pad = (-len(I_x0)) % 4
        if pad:
            I_x0 = np.pad(I_x0, (0, pad))
            Q_x0 = np.pad(Q_x0, (0, pad))
            I_y0 = np.pad(I_y0, (0, pad))
            Q_y0 = np.pad(Q_y0, (0, pad))

        len_pi  = len(I_x0)              # samples in one π
        win_len = 2 * len_pi             # total 2-π window
        marker  = mgr._perm.pulses[xid].get("digital_marker", "ON")

        I_tot = np.zeros(win_len)
        Q_tot = np.zeros(win_len)

        # ---------- helpers ---------------------------------------------
        def rot(I, Q, ω):
            t = np.arange(1, len(I)+1) * dt
            c, s = np.cos(ω*t), np.sin(ω*t)
            return I*c - Q*s, I*s + Q*c

        def mix(phi, I_x, Q_x, I_y, Q_y):
            c, s = np.cos(phi), np.sin(phi)
            return c*I_x + s*I_y, c*Q_x + s*Q_y

        T_gate = win_len * dt            # physical gate duration (s)
        
        # ---------- build multiplexed SNAP ------------------------------
        if self.apply_corrections:
            corr = getattr(type(self).attributes, "snap_phase_corr", None)
            if corr is not None:
                L = len(corr)
                if len(self.angles) > L:
                    raise ValueError(f"Too many angles ({len(self.angles)}) > {L}")
                if len(self.angles) < L:
                    self.angles = np.pad(self.angles,
                                        (0, L - len(self.angles)),
                                        mode="constant")
            else:
                corr = np.zeros(len(self.angles))
                print("Warning, snap apply correction set to true but correction array is missing!")
        else:
            corr = np.zeros(len(self.angles))
                    
        for n, (eta, delta_eta) in enumerate(zip(self.angles, corr)):
            if np.isnan(eta):            # treat NaN as η = 0  (still apply!)
                eta = 0.0

            # Manual tweak is *added before* Kerr compensation ---------------
            eta_tot = eta + delta_eta

            # Kerr phase gathered during the first π ------------------------
            dphi_K1 = 0.5 * K  * n * (n - 1) * T_gate * 2 * np.pi
            dphi_K2 = (K2 / 6.0) * n * (n - 1) * (n - 2) * T_gate * 2 * np.pi
            dphi_K  = dphi_K1 + dphi_K2

            # Axis for the second π ----------------------------------------
            phi2   = eta_tot - dphi_K        # axis for 2nd π

            # Selective rotation frequency ----------------------------------
            ω_n = 2 * np.pi * (n*chi + chi2 * n * (n - 1) + chi3 * n * (n - 1) * (n - 2))
            Ix, Qx = rot(I_x0, Q_x0, ω_n)
            Iy, Qy = rot(I_y0, Q_y0, ω_n)

            # Assemble the two π rotations ---------------------------------
            I1, Q1 = mix(0.0,  Ix, Qx, Iy, Qy)
            I2, Q2 = mix(phi2, Ix, Qx, Iy, Qy)

            I_tot[:len_pi]        += I1
            Q_tot[:len_pi]        += Q1
            I_tot[len_pi:win_len] -= I2
            Q_tot[len_pi:win_len] -= Q2


        # ---------- register pulse & waveforms --------------------------
        I_name = f"{self.name}_I"
        Q_name = f"{self.name}_Q"
        mgr.add_waveform(I_name, "arbitrary", I_tot.tolist(), persist=False)
        mgr.add_waveform(Q_name, "arbitrary", Q_tot.tolist(), persist=False)
        
        self._refresh_name()
        pulse = PulseOp(element_name   = self.target,
                        pulse_name     = f"{self.name}_2pi",
                        op_identifier  = self.name,
                        op_type        = "control",
                        length         = win_len,
                        digital_marker = marker,
                        I_wf_name      = I_name,  Q_wf_name = Q_name,
                        I_wf           = I_tot.tolist(),
                        Q_wf           = Q_tot.tolist())
        mgr.register_pulse_op(pulse, override=True, persist=False)
        
        return self.name

class Idle(Gate):
    def __init__(self, wait_time, target=None):
        super().__init__(name=f"IDLE_{wait_time}", target=target)
        self.wait_clks = (int(wait_time) - (int(wait_time) % 4)) // 4

    def play(self):
        qua.wait(self.wait_clks)

    def build(self):
        pass


def save_gates(path: str | pathlib.Path, gates: list[Gate]) -> None:
    with open(path, "w") as fp:
        json.dump([g.to_dict() for g in gates], fp, indent=2)

def load_gates(path: str | pathlib.Path,
               mgr : PulseOperationManager) -> list[Gate]:
    with open(path) as fp:
        gate_dicts = json.load(fp)
    return [Gate.from_dict(d, mgr) for d in gate_dicts]
