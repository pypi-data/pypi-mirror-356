"""
pulse_manager.py
────────────────
PulseOperationManager with a permanent + volatile resource split.

• persist=True   (default)  → store in _perm, is serialized to disk
• persist=False             → store in _volatile, lives only for the session

Public helpers:
    add_waveform(...)
    add_int_weight(...)
    add_pulse(...)
    register_pulse_op(...)

Persistence:
    save_json(path)          – writes ONLY the permanent objects
    load_json(path)          – loads permanent objects, clears volatile
    clear_temporary()        – empties the volatile store

QUA / QM config export:
    burn_to_config(cfg, include_volatile=True)

© 2025 – adapt freely
"""
from __future__ import annotations
import json, warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Union

# ────────────────── your project-wide constants ──────────────────
MAX_AMPLITUDE  = 0.48
BASE_AMPLITUDE = 0.24


# ═════════════════════════════════════════════════════════════════
#  Helpers
# ═════════════════════════════════════════════════════════════════
class _ResourceStore:
    """Container for waveforms, pulses, weights and element-op mappings."""

    def __init__(self) -> None:
        self.waveforms: Dict[str, Dict[str, Any]] = {}
        self.dig_waveforms: Dict[str, Dict[str, Any]] = {}
        self.pulses:    Dict[str, Dict[str, Any]] = {}
        self.weights:   Dict[str, Dict[str, Any]] = {}
        self.el_ops:    Dict[str, Dict[str, str]] = {}

    # ─── merge this store into an arbitrary QM config dict ────
    def merge_into(self, cfg: Dict[str, Any]) -> None:
        cfg.setdefault("waveforms",            {}).update(self.waveforms)
        cfg.setdefault("digital_waveforms",{}).update(self.dig_waveforms)
        cfg.setdefault("pulses",               {}).update(self.pulses)
        cfg.setdefault("integration_weights",  {}).update(self.weights)
        elems = cfg.setdefault("elements", {})
        for el, ops in self.el_ops.items():
            elems.setdefault(el, {}).setdefault("operations", {}).update(ops)

    # ─── serialization helpers (perm store only) ──────────────
    def as_dict(self):
        return dict(
            waveforms=self.waveforms,
            digital_waveforms=self.dig_waveforms,
            pulses=self.pulses,
            integration_weights=self.weights,
            element_operations=self.el_ops,
        )

    def load_from_dict(self, d: Dict[str, Any]):
        self.waveforms.update(d.get("waveforms", {}))
        self.pulses.update(d.get("pulses", {}))
        self.weights.update(d.get("integration_weights", {}))
        self.el_ops.update(d.get("element_operations", {}))

    def clear(self):
        self.waveforms.clear(); self.pulses.clear()
        self.weights.clear();   self.el_ops.clear()


# ═════════════════════════════════════════════════════════════════
@dataclass
class PulseOp:
    """Light wrapper for the information you pass into register_pulse_op."""
    element_name: str
    pulse_name:   str
    op_identifier: str
    op_type:      str | None = None          # "control"/"measurement"
    length:       int | None = None
    digital_marker: bool | str = True
    I_wf_name: str | None = None
    Q_wf_name: str | None = None
    I_wf:  Union[List[float], float, None] = None
    Q_wf:  Union[List[float], float, None] = None
    int_weights: Dict[str, str] | None = None


# ═════════════════════════════════════════════════════════════════
class PulseOperationManager:
    # ─────────────────────────────────────────────────────────────
    #  Construction / persistence
    # ─────────────────────────────────────────────────────────────
    def __init__(self, elements: List[str] | None = None) -> None:
        self._perm      = _ResourceStore()
        self._volatile  = _ResourceStore()
        self.elements   = elements or []
        self._init_defaults()

    def _init_defaults(self):
        # default waveforms
        self.add_waveform("zero_wf",  "constant", 0.0)
        self.add_waveform("const_wf", "constant", BASE_AMPLITUDE)

        self.add_digital_waveform("ON",  [(1, 0)])
        self.add_digital_waveform("OFF", [(0, 0)])
        # default pulses
        self.add_pulse("const_pulse", "control", 1000, "const_wf", "zero_wf")
        self.add_pulse("zero_pulse",  "control", 1000, "zero_wf",  "zero_wf")
        # default weights (generic 1 µs)
        self.add_int_weight("cosine_weights",     1.0, 0.0, 1000)
        self.add_int_weight("sine_weights",       0.0, 1.0, 1000)
        self.add_int_weight("minus_sine_weights", 0.0, -1.0, 1000)
        # default op map
        self._perm.el_ops = {"*": {"const": "const_pulse", "zero": "zero_pulse"}}

    # ---------- save / load permanent part only -----------------
    def save_json(self, path: str):
        json.dump(self._perm.as_dict(), open(path, "w"), indent=2)

    @classmethod
    def from_json(cls, path: str) -> "PulseOperationManager":
        mgr = cls()
        mgr._perm.clear()
        mgr._perm.load_from_dict(json.load(open(path)))
        mgr._volatile.clear()
        print(f"Loaded pulse files from: {path}")
        return mgr

    def clear_temporary(self):                 # toss volatile store
        self._volatile.clear()

    # ─────────────────────────────────────────────────────────────
    #  Low-level validators
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def _validate_waveform(kind: str, sample):
        if kind not in ("constant", "arbitrary"):
            raise ValueError("Waveform kind must be 'constant' or 'arbitrary'.")
        if kind == "constant":
            if abs(sample) > MAX_AMPLITUDE:
                raise ValueError("Amplitude exceeds MAX_AMPLITUDE.")
        else:
            if not isinstance(sample, list):
                raise ValueError("Arbitrary waveform requires sample list.")
            if any(abs(x) > MAX_AMPLITUDE for x in sample):
                raise ValueError("Sample exceeds MAX_AMPLITUDE.")

    # ─────────────────────────────────────────────────────────────
    #  Public add-helpers  (persist = True ➜ permanent store)
    # ─────────────────────────────────────────────────────────────
    def add_waveform(self, name: str, kind: str, sample,
                     *, persist: bool = True):
        self._validate_waveform(kind, sample)
        target = self._perm if persist else self._volatile
        data = {"type": kind,
                "sample" if kind == "constant" else "samples": sample}
        target.waveforms[name] = data

    def add_digital_waveform(self, name: str, samples: List[tuple[int, int]],
                             *, persist: bool = True):
        """
        Register or overwrite a digital waveform.

        *samples* must be a list of (value, duration) tuples where *value*
        is 0 or 1.
        """
        for idx, (v, _) in enumerate(samples):
            if v not in (0, 1):
                raise ValueError(f"digital_waveform[{idx}] has value {v}; must be 0 or 1.")
        target = self._perm if persist else self._volatile
        target.dig_waveforms[name] = {"samples": samples}

    def add_int_weight(self, name: str, cos_w, sin_w, len, *, persist: bool = True):
        target = self._perm if persist else self._volatile
        target.weights[name] = {"cosine": [(cos_w, len)], "sine": [(sin_w, len)]}

    def add_pulse(
        self,
        name: str,
        op_type: str,
        length: int,
        I_wf_name: str,
        Q_wf_name: str,
        *,
        digital_marker: str | bool = "ON",
        int_weight: Dict[str, str] | str | None = None,
        persist: bool = True,
    ):
        target = self._perm if persist else self._volatile
        pulse = dict(operation=op_type,
                     length=length,
                     waveforms={"I": I_wf_name, "Q": Q_wf_name},
                     digital_marker=("ON" if digital_marker is True
                                     else "OFF" if digital_marker is False
                                     else digital_marker))
        if op_type == "measurement":
            if int_weight is None:
                # prefer generic triplet if present
                if "cosine_weights" in target.weights:
                    int_weight = {"cos": "cosine_weights",
                                  "sin": "sine_weights",
                                  "minus_sin": "minus_sine_weights"}
                else:
                    dur = length
                    int_weight = {"cos": f"cos{dur}_weights",
                                  "sin": f"sin{dur}_weights",
                                  "minus_sin": f"minus_sin{dur}_weights"}
                    for lbl, w_name in int_weight.items():
                        if w_name not in target.weights:
                            if lbl == "cos":
                                self.add_int_weight(w_name, 1.0, 0.0, dur, persist=persist)
                            elif lbl == "sin":
                                self.add_int_weight(w_name, 0.0, 1.0, dur, persist=persist)
                            else:
                                self.add_int_weight(w_name, 0.0, -1.0, dur, persist=persist)
            elif isinstance(int_weight, str):
                stem = int_weight.strip()
                int_weight = {"cos": f"cos{stem}_weights",
                              "sin": f"sin{stem}_weights",
                              "minus_sin": f"minus_sin{stem}_weights"}
            pulse["integration_weights"] = int_weight
        target.pulses[name] = pulse

    def add_operation(self, op_id: str, pulse_name: str):
        """
        Register or overwrite the global mapping  op_id → pulse_name.
        This lives in a single dictionary `self.operations` (created on-demand).
        """
        if not hasattr(self, "operations"):
            # create and seed with defaults only once
            self.operations: Dict[str, str] = {
                "const": "const_pulse",     # same as _init_defaults()
                "zero":  "zero_pulse",
            }
        self.operations[op_id] = pulse_name

    # ─────────────────────────────────────────────────────────────
    #  High-level helper  register_pulse_op
    # ─────────────────────────────────────────────────────────────
    def register_pulse_op(
        self,
        p: PulseOp,
        *,
        override: bool = False,
        persist: bool = False,
        warning_flag = True
    ):
        store = self._perm if persist else self._volatile

        # ── fast path ──────────────────────────────────────────────────
        if p.pulse_name in store.pulses and not override:
            op_id = p.op_identifier or p.pulse_name.split("_pulse")[0]
            store.el_ops.setdefault(p.element_name, {})[op_id] = p.pulse_name
            self.add_operation(op_id, p.pulse_name)          # global map
            return

        # sanity checks
        if p.op_type is None or p.length is None:
            raise ValueError("op_type and length are required.")
        if p.I_wf_name is None or p.Q_wf_name is None:
            raise ValueError("I_wf_name and Q_wf_name must be provided.")

        # create / update waveforms
        for ch, name, data in (
            ("I", p.I_wf_name, p.I_wf),
            ("Q", p.Q_wf_name, p.Q_wf),
        ):
            if data is None and name not in store.waveforms:
                raise ValueError(f"{ch}-waveform '{name}' missing samples.")
            if data is not None:     # create/overwrite only if user supplied
                kind = "constant" if isinstance(data, (int, float)) else "arbitrary"
                self.add_waveform(name, kind, data, persist=persist)

        if p.op_type == "measurement" and p.int_weights is None:
            if warning_flag:
                warnings.warn(f"Measurement pulse '{p.pulse_name}' has no "
                            "integration_weights; defaults will be used.",
                            RuntimeWarning)

        # (re)create the pulse
        self.add_pulse(
            p.pulse_name,
            p.op_type,
            p.length,
            p.I_wf_name,
            p.Q_wf_name,
            digital_marker=p.digital_marker,
            int_weight=p.int_weights,
            persist=persist,
        )
        # ---------- mappings -------------------------------------------
        op_id = p.op_identifier or p.pulse_name.split("_pulse")[0]
        self.add_operation(op_id, p.pulse_name)
        
        store.el_ops.setdefault(p.element_name, {})[op_id] = p.pulse_name

        print(f"pulse {p.pulse_name} with len {p.length} registered!")

    def get_pulse_waveforms(
        self,
        pulse_name: str,
        *,
        include_volatile: bool = False
    ) -> tuple[Union[float, List[float]] | None, Union[float, List[float]] | None]:
        """
        Return the (I, Q) waveform data for `pulse_name`, or (None, None) if not found.
        Prints a warning rather than raising if missing.
        """
        # 1) pick the right store
        if include_volatile and pulse_name in self._volatile.pulses:
            store = self._volatile
        elif pulse_name in self._perm.pulses:
            store = self._perm
        else:
            warnings.warn(f"Pulse '{pulse_name}' not found in any store; returning (None, None).")
            return None, None

        # 2) lookup the waveform names
        wf_map = store.pulses[pulse_name].get("waveforms", {})
        I_name = wf_map.get("I")
        Q_name = wf_map.get("Q")
        if I_name is None or Q_name is None:
            warnings.warn(f"Pulse '{pulse_name}' missing I/Q waveform assignment; returning (None, None).")
            return None, None

        # 3) fetch the actual waveform data
        def _get_wf_data(name):
            # search volatile first if allowed
            if include_volatile and name in self._volatile.waveforms:
                wf = self._volatile.waveforms[name]
            elif name in self._perm.waveforms:
                wf = self._perm.waveforms[name]
            else:
                warnings.warn(f"Waveform '{name}' not found; returning None.")
                return None
            if wf["type"] == "constant":
                return wf.get("sample")
            else:
                return wf.get("samples")

        I_wf = _get_wf_data(I_name)
        Q_wf = _get_wf_data(Q_name)
        return I_wf, Q_wf

    def get_op_waveforms(
        self,
        element_name: str,
        op_identifier: str,
        *,
        include_volatile: bool = True,
        fallback_global: bool = True,
    ) -> PulseOp | None:
        """
        Return a complete PulseOp dataclass for *op_identifier* on *element_name*,
        including waveform data and pulse attributes.
        """
        # 1) Resolve pulse_name as before
        pulse_name = None
        if include_volatile:
            pulse_name = (
                self._volatile.el_ops
                    .get(element_name, {})
                    .get(op_identifier)
            )
        if pulse_name is None:
            pulse_name = (
                self._perm.el_ops
                    .get(element_name, {})
                    .get(op_identifier)
            )
        if pulse_name is None and include_volatile:
            pulse_name = (
                self._volatile.el_ops
                    .get("*", {})
                    .get(op_identifier)
            )
        if pulse_name is None:
            pulse_name = (
                self._perm.el_ops
                    .get("*", {})
                    .get(op_identifier)
            )
        if pulse_name is None and fallback_global and hasattr(self, "operations"):
            pulse_name = self.operations.get(op_identifier)
        if pulse_name is None:
            warnings.warn(
                f"Operation '{op_identifier}' not found for element '{element_name}'; returning None."
            )
            return None

        # 2) Pick store where pulse lives
        if include_volatile and pulse_name in self._volatile.pulses:
            store = self._volatile
        else:
            store = self._perm

        # 3) Retrieve pulse definition
        pulse_def = store.pulses[pulse_name]

        # 4) Get waveform names
        I_name = pulse_def["waveforms"]["I"]
        Q_name = pulse_def["waveforms"]["Q"]

        # 5) Fetch waveform data
        I_wf, Q_wf = self.get_pulse_waveforms(pulse_name, include_volatile=include_volatile)

        # 6) Integration weights if measurement
        int_w = pulse_def.get("integration_weights")

        # 7) Build and return PulseOp
        return PulseOp(
            element_name=element_name,
            pulse_name=pulse_name,
            op_identifier=op_identifier,
            op_type=pulse_def.get("operation"),
            length=pulse_def.get("length"),
            digital_marker=pulse_def.get("digital_marker", True),
            I_wf_name=I_name,
            Q_wf_name=Q_name,
            I_wf=I_wf,
            Q_wf=Q_wf,
            int_weights=int_w,
        )
    
    def get_pulse_length(
        self,
        pulse_name: str,
        *,
        include_volatile: bool = True
    ) -> int | None:
        """
        Return the length of `pulse_name`, or None if not found.
        Prints a warning rather than raising if missing.
        """
        # 1) pick the right store
        if include_volatile and pulse_name in self._volatile.pulses:
            store = self._volatile
        elif pulse_name in self._perm.pulses:
            store = self._perm
        else:
            warnings.warn(f"Pulse '{pulse_name}' not found in any store; returning None.")
            return None

        # 2) extract the length
        pulse_def = store.pulses[pulse_name]
        length = pulse_def.get("length")
        if length is None:
            warnings.warn(f"Pulse '{pulse_name}' has no 'length' field; returning None.")
            return None

        return length
    
    # ─────────────────────────────────────────────────────────────
    #  High-level helper  modify_pulse_op  (partial-update version)
    # ─────────────────────────────────────────────────────────────
    def modify_pulse_op(
        self,
        p: PulseOp,
        *,
        persist: bool = False,
    ):
        """
        Update an existing pulse entry *partially*.

        Only the PulseOp fields you set to a NON-None value will overwrite the
        stored definition; everything else is kept unchanged.

        Examples
        --------
        >>> p = PulseOp(
        ...     element_name="resonator",
        ...     pulse_name="readout_pulse",
        ...     op_identifier="readout",
        ...     int_weights={"cos": "cosRD_w", "sin": "sinRD_w",
        ...                  "minus_sin": "minus_sinRD_w"}
        ... )                      # all other attrs are left as None
        >>> pulseOpMngr.modify_pulse_op(p, persist=True)
        """
        store = self._perm if persist else self._volatile

        if p.pulse_name not in store.pulses:
            raise KeyError(
                f"Pulse '{p.pulse_name}' not found in "
                f"{'permanent' if persist else 'volatile'} store. "
                "Use `register_pulse_op` to create it first."
            )

        old = store.pulses[p.pulse_name]          # ← existing dict

        # ---------- fill in missing fields from the stored entry ----------
        merged = PulseOp(
            element_name   = p.element_name,
            pulse_name     = p.pulse_name,
            op_identifier  = p.op_identifier
                             or next((k for k, v in getattr(self, "operations", {}).items()
                                      if v == p.pulse_name),
                                     p.pulse_name.split("_pulse")[0]),
            op_type        = p.op_type        or old["operation"],
            length         = p.length         or old["length"],
            digital_marker = (p.digital_marker
                              if p.digital_marker is not None
                              else old.get("digital_marker", "ON")),
            I_wf_name      = p.I_wf_name      or old["waveforms"]["I"],
            Q_wf_name      = p.Q_wf_name      or old["waveforms"]["Q"],
            I_wf           = p.I_wf,   # keep None → don’t touch samples
            Q_wf           = p.Q_wf,
            int_weights    = (p.int_weights
                              if p.int_weights is not None
                              else old.get("integration_weights")),
        )

        # Delegate to the normal creation path with override=True ➜
        # recreates / overwrites the pulse + updates all mappings
        self.register_pulse_op(merged, override=True, persist=persist)

    # ─────────────────────────────────────────────────────────────
    #  Export to QM and inspection helpers
    # ─────────────────────────────────────────────────────────────
    def burn_to_config(self, cfg: Dict[str, Any], *, include_volatile=True):
        self._perm.merge_into(cfg)
        if include_volatile:
            self._volatile.merge_into(cfg)
        return cfg

    def print_state(self, *, include_volatile=True):
        import pprint
        def head(tag): print("="*30, tag, "="*30)
        head("PERMANENT")
        pprint.pprint(self._perm.as_dict())
        if include_volatile and any(
            (self._volatile.waveforms, self._volatile.pulses)):
            head("VOLATILE")
            pprint.pprint(self._volatile.as_dict())


    # ─────────────────────────────────────────────────────────────
    #  Build a PulseOperationManager from an in-memory config dict
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def from_config(cls, config: dict) -> "PulseOperationManager":
        """
        Parse an existing QM-style configuration dictionary and return a
        PulseOperationManager whose *permanent* store reproduces that config.

        Everything found in the dict (waveforms, pulses, integration_weights,
        element-operation maps) is treated as PERMANENT.  The volatile store
        is cleared.

        Raises
        ------
        ValueError  – on any structural inconsistency.
        """
        mgr = cls()
        # start with a clean slate
        mgr._perm.clear()
        mgr._volatile.clear()

        # ── 1) Waveforms ────────────────────────────────────────────────
        wfs = config.get("waveforms")
        if wfs is None:
            raise ValueError("Configuration missing 'waveforms' key.")
        for wf_id, wf in wfs.items():
            if "type" not in wf:
                raise ValueError(f"Waveform '{wf_id}' missing 'type'.")
            kind = wf["type"]
            if kind == "constant":
                if "sample" not in wf:
                    raise ValueError(f"Constant waveform '{wf_id}' missing 'sample'.")
            elif kind == "arbitrary":
                if "samples" not in wf:
                    raise ValueError(f"Arbitrary waveform '{wf_id}' missing 'samples'.")
            else:
                raise ValueError(f"Waveform '{wf_id}' has invalid type '{kind}'.")
            mgr._perm.waveforms[wf_id] = wf

        digs = config.get("digital_waveforms", {})
        if not isinstance(digs, dict):
            raise ValueError("'digital_waveforms' must be a dictionary.")
        for dw_name, dw in digs.items():
            if "samples" not in dw or not isinstance(dw["samples"], list):
                raise ValueError(f"Digital waveform '{dw_name}' needs a 'samples' list.")
            for idx, (v, _) in enumerate(dw["samples"]):
                if v not in (0, 1):
                    raise ValueError(f"Digital waveform '{dw_name}' sample {idx} "
                                    f"has value {v}; must be 0/1.")
            mgr._perm.dig_waveforms[dw_name] = dw

        # ── 2) Integration weights ─────────────────────────────────────
        weights = config.get("integration_weights")
        if weights is None:
            raise ValueError("Configuration missing 'integration_weights' key.")
        for iw_id, iw in weights.items():
            if "cosine" not in iw or "sine" not in iw:
                raise ValueError(f"Integration-weight '{iw_id}' needs 'cosine' and 'sine'.")
            mgr._perm.weights[iw_id] = iw

        # ── 3) Pulses ──────────────────────────────────────────────────
        pls = config.get("pulses")
        if pls is None:
            raise ValueError("Configuration missing 'pulses' key.")
        for p_id, p in pls.items():
            for req in ("operation", "length", "waveforms", "digital_marker"):
                if req not in p:
                    raise ValueError(f"Pulse '{p_id}' missing '{req}'.")
            if p["operation"] not in ("control", "measurement"):
                raise ValueError(f"Pulse '{p_id}' has invalid op type '{p['operation']}'.")
            # waveform refs exist?
            for ch in ("I", "Q"):
                wf_name = p["waveforms"].get(ch)
                if wf_name not in mgr._perm.waveforms:
                    raise ValueError(f"Pulse '{p_id}' references unknown waveform '{wf_name}'.")
            # measurement → validate int-weights
            if p["operation"] == "measurement":
                iw_map = p.get("integration_weights")
                if not isinstance(iw_map, dict):
                    raise ValueError(f"Measurement pulse '{p_id}' needs 'integration_weights'.")
                for lbl, iw_name in iw_map.items():
                    if iw_name not in mgr._perm.weights:
                        raise ValueError(f"Pulse '{p_id}' references unknown weight '{iw_name}'.")
            mgr._perm.pulses[p_id] = p

        # ── 4) Element-specific operation maps ─────────────────────────
        mgr._perm.el_ops.clear()
        if "elements" in config:
            elems = config["elements"]
            if not isinstance(elems, dict):
                raise ValueError("'elements' must be a dictionary.")
            for el_id, el_cfg in elems.items():
                ops = el_cfg.get("operations", {})
                if not isinstance(ops, dict):
                    raise ValueError(f"Element '{el_id}' operations must be a dict.")
                for op_name, pulse_name in ops.items():
                    if pulse_name not in mgr._perm.pulses:
                        raise ValueError(f"Element '{el_id}' op '{op_name}' "
                                         f"references unknown pulse '{pulse_name}'.")
                mgr._perm.el_ops[el_id] = ops.copy()

        return mgr




def print_config(config: dict) -> None:
    """
    Print the complete configuration in a predefined order matching the typical
    configuration structure. The keys are printed in the following order if they exist:
    
        1. version
        2. controllers
        3. elements
        4. octaves
        5. pulses
        6. waveforms
        7. digital_waveforms
        8. integration_weights
    
    Any additional keys not in the ordering are printed in an additional section.
    
    NumPy scalar types (e.g. int32, float64) are converted via their .item() method.
    """
    # helper for numpy scalars
    default = lambda o: o.item() if hasattr(o, "item") else None

    ordered_keys = [
        "version",
        "controllers",
        "elements",
        "octaves",
        "pulses",
        "waveforms",
        "digital_waveforms",
        "integration_weights"
    ]
    
    print("=" * 80)
    print("FULL CONFIGURATION")
    print("=" * 80)
    
    for key in ordered_keys:
        if key in config:
            print(f"\n===== {key.upper()} =====\n")
            print(json.dumps(config[key], indent=4, default=default))
    
    remaining_keys = [k for k in config if k not in ordered_keys]
    if remaining_keys:
        print("\n===== OTHER CONFIGURATION KEYS =====\n")
        for key in remaining_keys:
            print(f"\n----- {key} -----\n")
            print(json.dumps(config[key], indent=4, default=default))
    
    print("=" * 80)


if __name__ == "__main__":
    pass

    