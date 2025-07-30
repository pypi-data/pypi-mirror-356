
from qm.qua import *
from qualang_tools.loops import from_array
import numpy as np
from configuration import *
from .gates import Gate, SNAP, Displacement, Rotation

class measureMacro:
    __readout_el = "resonator"
    __readout_pulse = "readout"
    
    __I_mod_weights = ["cos", "sin"]
    __Q_mod_weights = ["minus_sin", "cos"]

    __demod_fn       = dual_demod.full
    __demod_args = ()
    def __new__(cls, *args, **kwargs):
        raise TypeError("This class cannot be instantiated and is meant to be used as a macro")

    @classmethod
    def set_pulse(cls, readout_pulse):
        cls.__readout_pulse = readout_pulse

    @classmethod
    def set_element(cls, element):
        cls.__readout_el = element

    @classmethod
    def set_IQ_mod(cls, I_mod_weights=["cos", "sin"], Q_mod_weights=["minus_sin", "cos"]):
        cls.__I_mod_weights = I_mod_weights
        cls.__Q_mod_weights = Q_mod_weights

    @classmethod
    def set_demodulator(cls, fn, *args):
        """
        fn: one of dual_demod.full, sliced, accumulated, moving_window
        args: *all* the positional arguments that go *between* (iw1,iw2)
              and the target.
        """
        cls.__demod_fn   = fn
        cls.__demod_args = args

    @classmethod
    def reset_weights(cls):
        cls.__I_mod_weights = ["cos", "sin"]
        cls.__Q_mod_weights = ["minus_sin", "cos"]
    
    @classmethod
    def reset_demodulator(cls):
        cls.__demod_fn     = dual_demod.full
        cls.__demod_args = ()
    
    @classmethod
    def reset_pulse(cls):
        cls.__readout_pulse = "readout"

    @classmethod
    def reset(cls):
        cls.reset_weights()
        cls.reset_demodulator()
        cls.reset_pulse()

    @classmethod
    def measure(cls, I=None, Q=None, gain=None, timestamp_stream=None, adc_stream=None):
        if I is None:
            I = declare(fixed)
        if Q is None:
            Q = declare(fixed)
        demod_I = cls.__demod_fn(*cls.__I_mod_weights, *cls.__demod_args, I)
        demod_Q = cls.__demod_fn(*cls.__Q_mod_weights, *cls.__demod_args, Q)
        if gain is None:
            measure(
                cls.__readout_pulse,
                cls.__readout_el,
                None,
                demod_I,
                demod_Q,
                timestamp_stream=timestamp_stream,
                adc_stream=adc_stream
            )
        else:
            measure(
                cls.__readout_pulse * amp(gain),
                cls.__readout_el,
                None,
                demod_I,
                demod_Q,
                timestamp_stream=timestamp_stream,
                adc_stream=adc_stream
            )
        return I, Q


class SweepExperiment:
    """
    Base class for QUA sweep experiments. Subclasses should override body().
    """
    def __init__(self,
                 pulse: str,
                 axes: list[tuple[str, np.ndarray]],
                 n_avg: int = 1):
        self.pulse = pulse
        self.axes = axes
        self.n_avg = n_avg

    def body(self, decl: dict):
        """
        Inner body executed at each sweep point. "decl" maps variable names to QUA declarations.
        """
        raise NotImplementedError

    def build(self):
        # set readout pulse
        measureMacro.set_pulse(self.pulse)
        with program() as prog:
            # 1. Declarations
            decl = {"n": declare(int)}
            for name, _ in self.axes:
                decl[name] = declare(int)
            decl["I"] = declare(fixed)
            decl["Q"] = declare(fixed)
            decl["I_st"] = declare_stream()
            decl["Q_st"] = declare_stream()
            decl["n_st"] = declare_stream()

            # 2. Nested loops
            def nest(level: int):
                var, arr = self.axes[level]
                with for_(*from_array(decl[var], arr)):
                    if level + 1 < len(self.axes):
                        nest(level + 1)
                    else:
                        # user-defined pulse/play/measure body
                        self.body(decl)
                        # save I/Q for this point
                        save(decl["I"], decl["I_st"])
                        save(decl["Q"], decl["Q_st"])

            with for_(decl["n"], 0, decl["n"] < self.n_avg, decl["n"] + 1):
                nest(0)
                # save iteration count
                save(decl["n"], decl["n_st"])

            # 3. Stream processing
            shape = tuple(len(arr) for _, arr in self.axes)
            with stream_processing():
                decl["I_st"].buffer(*shape).average().save("I")
                decl["Q_st"].buffer(*shape).average().save("Q")
                decl["n_st"].save("iteration")

        # reset macro state
        measureMacro.reset()
        return prog


# === Subclasses for each experiment ===

class ResonatorSpectroscopy(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 ro_pulse: str,
                 ro_gain: float,
                 if_frequencies: np.ndarray,
                 depletion_len: int,
                 n_avg: int = 1):
        super().__init__(pulse=ro_pulse,
                         axes=[("f", if_frequencies)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.ro_gain = ro_gain
        self.depletion_len = depletion_len

    def body(self, d: dict):
        update_frequency(self.ro_el, d["f"])
        I, Q = measureMacro.measure(d["I"], d["Q"], gain=self.ro_gain)
        wait(int(self.depletion_len / 4), self.ro_el)


class ResonatorPowerSpectroscopy(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 ro_pulse: str,
                 if_frequencies: np.ndarray,
                 gains: np.ndarray,
                 depletion_len: int,
                 n_avg: int = 1):
        super().__init__(pulse=ro_pulse,
                         axes=[("f", if_frequencies), ("g", gains)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.depletion_len = depletion_len

    def body(self, d: dict):
        update_frequency(self.ro_el, d["f"])
        I, Q = measureMacro.measure(d["I"], d["Q"], gain=d["g"])
        wait(int(self.depletion_len / 4), self.ro_el)


class QubitSpectroscopy(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 if_frequencies: np.ndarray,
                 qb_gain: float,
                 qb_len: int,
                 qb_therm_clks: int = 4,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("f", if_frequencies)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.qb_gain = qb_gain
        self.qb_len = qb_len
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        update_frequency(self.qb_el, d["f"])
        play('saturation' * amp(self.qb_gain), self.qb_el, duration=self.qb_len)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class QubitSpectroscopyEF(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 if_frequencies: np.ndarray,
                 qb_ge_if: int,
                 qb_gain: float,
                 qb_len: int,
                 r180: str,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("f", if_frequencies)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.qb_ge_if = qb_ge_if
        self.qb_gain = qb_gain
        self.qb_len = qb_len
        self.r180 = r180
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        # prep pulse on |e>--|f>
        update_frequency(self.qb_el, self.qb_ge_if)
        play(self.r180, self.qb_el)
        align()
        # main spectroscopy pulse
        update_frequency(self.qb_el, d["f"])
        play('saturation' * amp(self.qb_gain), self.qb_el, duration=self.qb_len)
        align(self.ro_el, self.qb_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class TemporalRabi(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 qb_gain: float,
                 qb_therm_clks: int,
                 num_clock_cycles: np.ndarray,
                 pulse: str = "gaussian_X",
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("t", num_clock_cycles)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.qb_gain = qb_gain
        self.qb_therm_clks = qb_therm_clks
        self.pulse = pulse

    def body(self, d: dict):
        play(self.pulse * amp(self.qb_gain), self.qb_el, duration=d["t"])
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks))


class PowerRabi(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 qb_clock_len: int,
                 gains: np.ndarray,
                 qb_therm_clks: int,
                 pulse: str = "gaussian_X",
                 n_avg: int = 1000):
        super().__init__(pulse="readout",
                         axes=[("g", gains)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.qb_clock_len = qb_clock_len
        self.qb_therm_clks = qb_therm_clks
        self.pulse = pulse

    def body(self, d: dict):
        play(self.pulse * amp(d["g"]), self.qb_el, duration=self.qb_clock_len)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks))


class TimeRabiChevron(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 pulse: str,
                 pulse_gain: float,
                 qb_if: int,
                 dfs: np.ndarray,
                 duration_clks: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("t", duration_clks), ("f", dfs)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.pulse = pulse
        self.pulse_gain = pulse_gain
        self.qb_if = qb_if
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        update_frequency(self.qb_el, d["f"] + self.qb_if)
        play(self.pulse * amp(self.pulse_gain), self.qb_el, duration=d["t"])
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class PowerRabiChevron(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 pulse: str,
                 pulse_duration: int,
                 qb_if: int,
                 dfs: np.ndarray,
                 amplitudes: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("a", amplitudes), ("f", dfs)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.pulse = pulse
        self.pulse_duration = pulse_duration
        self.qb_if = qb_if
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        update_frequency(self.qb_el, d["f"] + self.qb_if)
        play(self.pulse * amp(d["a"]), self.qb_el, duration=self.pulse_duration)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class RamseyChevron(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 r90: str,
                 qb_if: int,
                 dfs: np.ndarray,
                 delay_clks: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("delay", delay_clks), ("f", dfs)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.r90 = r90
        self.qb_if = qb_if
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        update_frequency(self.qb_el, d["f"] + self.qb_if)
        if d["delay"] >= 4:
            play(self.r90, self.qb_el)
            wait(d["delay"], self.qb_el)
            play(self.r90, self.qb_el)
        else:
            play(self.r90, self.qb_el)
            play(self.r90, self.qb_el)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)

class T1Relaxation(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 r180: str,
                 wait_cycles: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("w", wait_cycles)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.r180 = r180
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        play(self.r180, self.qb_el)
        align(self.qb_el, self.ro_el)
        wait(d["w"], self.qb_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class T2Ramsey(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 r90: str,
                 wait_cycles: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("w", wait_cycles)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.r90 = r90
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        play(self.r90, self.qb_el)
        wait(d["w"], self.qb_el)
        play(self.r90, self.qb_el)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class T2Echo(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 r180: str,
                 r90: str,
                 half_wait_cycles: np.ndarray,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse="readout",
                         axes=[("w", half_wait_cycles)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.r180 = r180
        self.r90 = r90
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        play(self.r90, self.qb_el)
        wait(d["w"], self.qb_el)
        play(self.r180, self.qb_el)
        wait(d["w"], self.qb_el)
        play(self.r90, self.qb_el)
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)


class ReadoutOptimization(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 ro_pulses: list[str],
                 ro_ifs: np.ndarray,
                 ro_gains: np.ndarray,
                 r180: str,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        # axes: pulse index, IF, gain
        super().__init__(pulse=None,
                         axes=[("p", np.arange(len(ro_pulses))),
                               ("f", ro_ifs),
                               ("g", ro_gains)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.ro_pulses = ro_pulses
        self.r180 = r180
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        # select pulse
        measureMacro.set_pulse(self.ro_pulses[d["p"]])
        update_frequency(self.ro_el, d["f"])
        # first measure
        I, Q = measureMacro.measure(d["I"], d["Q"], gain=d["g"])
        wait(int(self.qb_therm_clks), self.ro_el)
        save(I, d["I_st"]); save(Q, d["Q_st"])
        # second measure after qubit pi
        align()
        play(self.r180, self.qb_el)
        align(self.qb_el, self.ro_el)
        I2, Q2 = measureMacro.measure(d["I"], d["Q"], gain=d["g"])
        wait(int(self.qb_therm_clks), self.ro_el)
        save(I2, d["I_st"]); save(Q2, d["Q_st"])


class PulsedResonatorSpectroscopy(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 if_freqs: np.ndarray,
                 pulse: str,
                 pulse_gain: float,
                 pulse_len: int,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse=pulse,
                         axes=[("f", if_freqs)],
                         n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.pulse_gain = pulse_gain
        self.pulse_len = pulse_len
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        update_frequency(self.ro_el, d["f"])
        play(self.pulse * amp(self.pulse_gain), self.qb_el, duration=int(self.pulse_len/4))
        align(self.qb_el, self.ro_el)
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks))


class TwoGateOperation(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 pulse1: str,
                 gain1: float,
                 len1: int,
                 pulse2: str,
                 gain2: float,
                 len2: int,
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse=None, axes=[("n", np.array([0]))], n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.p1, self.g1, self.l1 = pulse1, gain1, len1
        self.p2, self.g2, self.l2 = pulse2, gain2, len2
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        play(self.p1 * amp(self.g1), self.qb_el, duration=int(self.l1/4))
        play(self.p2 * amp(self.g2), self.qb_el, duration=int(self.l2/4))
        align()
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks))

class SingleQubitRotations(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 rotations: list[str],
                 qb_therm_clks: int,
                 n_avg: int = 1):
        super().__init__(pulse=None, axes=[("idx", np.arange(len(rotations)))], n_avg=n_avg)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.rotations = rotations
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        play(self.rotations[d["idx"]], self.qb_el)
        align()
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks))


class IQBlobs(SweepExperiment):
    def __init__(self,
                 ro_el: str,
                 qb_el: str,
                 r180: str,
                 qb_therm_clks: int,
                 n_runs: int = 1):
        super().__init__(pulse=None, axes=[("run", np.arange(n_runs))], n_avg=1)
        self.ro_el = ro_el
        self.qb_el = qb_el
        self.r180 = r180
        self.qb_therm_clks = qb_therm_clks

    def body(self, d: dict):
        I, Q = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)
        align()
        play(self.r180, self.qb_el)
        align(self.qb_el, self.ro_el)
        I2, Q2 = measureMacro.measure(d["I"], d["Q"])
        wait(int(self.qb_therm_clks), self.ro_el)
        # saving handled by base; just measure twice per iteration

