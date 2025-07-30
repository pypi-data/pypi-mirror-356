
from qm.qua import *
from qualang_tools.loops import from_array
from .gates import Gate, SNAP, Displacement, Rotation
import numpy as np 
from qm.qua.lib import Math, Cast

class measureMacro:
    _readout_el = "resonator"
    _readout_pulse = "readout"
    
    _I_mod_weights = ["cos", "sin"]
    _Q_mod_weights = ["minus_sin", "cos"]

    _demod_fn       = dual_demod.full
    _demod_args = ()

    _threshold  = 0

    def __new__(cls, *args, **kwargs):
        raise TypeError("This class cannot be instantiated and is meant to be used as a macro")

    @classmethod
    def set_threshold(cls, threshold):
        cls._threshold = threshold

    @classmethod
    def set_pulse(cls, readout_pulse):
        cls._readout_pulse = readout_pulse

    @classmethod
    def set_element(cls, element):
        cls._readout_el = element

    @classmethod
    def set_IQ_mod(cls, I_mod_weights=["cos", "sin"], Q_mod_weights=["minus_sin", "cos"]):
        cls._I_mod_weights = I_mod_weights
        cls._Q_mod_weights = Q_mod_weights

    @classmethod
    def get_IQ_mod(cls):
        return cls._I_mod_weights, cls._Q_mod_weights

    @classmethod
    def set_demodulator(cls, fn, *args):
        """
        fn: one of dual_demod.full, sliced, accumulated, moving_window
        args: *all* the positional arguments that go *between* (iw1,iw2)
              and the target.
        """
        cls._demod_fn   = fn
        cls._demod_args = args

    @classmethod
    def reset_weights(cls):
        cls._I_mod_weights = ["cos", "sin"]
        cls._Q_mod_weights = ["minus_sin", "cos"]
    
    @classmethod
    def reset_demodulator(cls):
        cls._demod_fn     = dual_demod.full
        cls._demod_args = ()
    
    @classmethod
    def reset_pulse(cls):
        cls._readout_pulse = "readout"

    @classmethod
    def reset(cls):
        cls.reset_weights()
        cls.reset_demodulator()
        cls.reset_pulse()

    @classmethod
    def measure(cls, *, with_state=False, gain=None,
                timestamp_stream=None, adc_stream=None,
                I=None, Q=None, state=None,
                conditional_r180=None, qb_el="qubit"):

        # --- variable allocation ------------------------------------------
        if I is None:  I = declare(fixed)
        if Q is None:  Q = declare(fixed)

        # binary discriminator wanted?
        make_state = with_state or state is not None
        if make_state:
            if cls._threshold is None:
                raise ValueError(
                    "measure(): binary state requested but no threshold set"
                )
            if state is None:
                state = declare(bool)

        # --- perform the measurement -------------------------------------
        pulse_handle = (cls._readout_pulse if gain is None
                        else cls._readout_pulse * amp(gain))

        measure(
            pulse_handle,
            cls._readout_el,
            None,
            cls._demod_fn(*cls._I_mod_weights, *cls._demod_args, I),
            cls._demod_fn(*cls._Q_mod_weights, *cls._demod_args, Q),
            timestamp_stream=timestamp_stream,
            adc_stream=adc_stream,
        )

        # --- run-time thresholding (optional) -----------------------------
        if conditional_r180 is not None:
            with if_(I > cls._threshold):
                play(conditional_r180, qb_el)
                align()
        if make_state:
            assign(state, I > cls._threshold)
            return I, Q, state

        return I, Q

def readout_raw_trace(ro_el, ro_pulse="readout", ro_gain=1.0, ro_if=-50e6, n_avg=1000):
    """
    Acquire and average raw ADC traces for a given readout resonator element.

    Parameters:
        ro_el     : QUA element label for the readout resonator
        ro_pulse  : Name of the readout pulse (default "readout")
        ro_gain   : Amplitude scaling for the readout pulse
        ro_if     : Intermediate frequency (in Hz) to set on the resonator
        n_avg     : Number of averages (iterations) to perform
    """
    with program() as raw_trace_prog:
        # Loop counter for averaging
        n = declare(int)
        # Stream that collects full ADC samples (both I and Q) at each measurement
        adc_st = declare_stream(adc_trace=True)
        # Stream to capture the iteration index
        n_st = declare_stream()

        # Update the local oscillator (IF) frequency of the readout element
        update_frequency(ro_el, ro_if)

        # Outer averaging loop: perform 'n_avg' measurements
        with for_(n, 0, n < n_avg, n + 1):
            # Perform a single-shot measurement:
            #   - Apply 'ro_pulse' scaled by 'ro_gain'
            #   - Route raw ADC data into 'adc_st' (samples from input1 and input2)
            measure(ro_pulse * amp(ro_gain), ro_el,
                    adc_stream=adc_st,
                    timestamp_stream='measure_timestamps')
            # Save the current iteration index into n_st for bookkeeping
            save(n, n_st)

        # Stream processing block: define how streams are post-processed and saved
        with stream_processing():
            adc_st.input1().average().save("adc1")
            adc_st.input2().average().save("adc2")
            adc_st.input1().save("adc1_single_run")
            adc_st.input2().save("adc2_single_run")
            n_st.save("iteration")

    return raw_trace_prog
def resonator_spectroscopy(ro_el, ro_pulse, ro_gain, if_frequencies, depletion_len, n_avg: int=1):
    """
    Sweep readout IF frequencies to perform 1D resonator spectroscopy.
    For each IF, perform a measurement (I/Q) and optionally deplete residual photons.

    Parameters:
        ro_el          : QUA element for readout resonator
        ro_pulse       : Name of the readout pulse to use
        ro_gain        : Gain (amplitude) for the readout measurement
        if_frequencies : Python array/list of IFs to step through (integers)
        depletion_len  : Time (in clock cycles) to wait for photon depletion
        n_avg          : Number of averaging iterations (default=1)
    """
    measureMacro.set_pulse(ro_pulse)
    with program() as resonator_spec:
        n = declare(int)
        f = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
            with for_(*from_array(f, if_frequencies)):  # QUA for_ loop for sweeping the frequency
                update_frequency(ro_el, f)
                I, Q = measureMacro.measure(I=I, Q=Q, gain=ro_gain)
                wait(int(depletion_len/4), ro_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            n_st.save("iteration")
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
    measureMacro.reset()
    return resonator_spec

def resonator_power_spectroscopy(ro_el, ro_pulse, if_frequencies, gains, depletion_len, n_avg:int=1):
    """
    Perform a 2D sweep of readout IF and readout gain to map out resonator response versus power.

    Parameters:
        ro_el          : QUA element label for the readout resonator
        ro_pulse       : Name of the readout pulse to use
        if_frequencies : Python array/list of IFs to step through
        gains          : Python array/list of gain (amplitude) settings to step through
        depletion_len  : Time in clock cycles for photon depletion after measurement
        n_avg          : Number of averaging iterations (default=1)
    """
    measureMacro.set_pulse(ro_pulse)
    with program() as resonator_spec_2D:
        n = declare(int)
        if_req = declare(int)
        g = declare(fixed)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()  
        Q_st = declare_stream()  
        n_st = declare_stream()  
        with for_(n, 0, n < n_avg, n + 1):  
            with for_(*from_array(if_req, if_frequencies)):  
                update_frequency(ro_el, if_req)
                with for_each_(g, gains): 
                    I, Q = measureMacro.measure(I=I, Q=Q, gain=g)
                    wait(int(depletion_len/4), ro_el)
                    save(I, I_st)
                    save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            n_st.save("iteration")
            I_st.buffer(len(gains)).buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(gains)).buffer(len(if_frequencies)).average().save("Q")
    measureMacro.reset()
    return resonator_spec_2D

def qubit_spectroscopy(ro_el, qb_el, if_frequencies, qb_gain, qb_len, qb_therm_clks:int=4, n_avg:int=1):
    """
    Perform spectroscopy on the qubit by sweeping drive IF and measuring readout response.

    Parameters:
        ro_el          : Readout resonator element label
        qb_el          : Qubit element label
        if_frequencies : Python array/list of IFs to sweep for the qubit drive
        qb_gain        : Gain for the qubit drive pulse
        qb_len         : Duration (in clock cycles) of the qubit drive pulse
        qb_therm_clks  : Number of clock cycles to wait for qubit thermalization (default=4)
        n_avg          : Number of averaging iterations (default=1)
    """
    with program() as qubit_spec:
        n = declare(int)
        if_freq = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(if_freq, if_frequencies)):
                update_frequency(qb_el, if_freq)
                play('saturation' * amp(qb_gain), qb_el, duration=qb_len)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks), ro_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
            n_st.save("iteration")
        return qubit_spec
    
def qubit_spectroscopy_ef(ro_el, qb_el, if_frequencies, qb_ge_if, qb_gain, qb_len, r180 , qb_therm_clks, n_avg:int=1):
    """
    Perform |e>→|f> spectroscopy by first preparing |e> via a π-pulse (r180), then sweeping drive IF.

    Parameters:
        ro_el          : Readout resonator element
        qb_el          : Qubit element
        if_frequencies : Python array/list of IFs for the spectroscopy sweep
        qb_ge_if       : IF at which to apply the π-pulse that drives |g>→|e>
        qb_gain        : Gain for the saturation pulse
        qb_len         : Duration of the saturation pulse
        r180           : Name of the π-pulse used to prepare |e>
        qb_therm_clks  : Thermalization wait time after readout
        n_avg          : Number of averaging iterations (default=1)
    """
    with program() as qubit_spec:
        n = declare(int)
        if_freq = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(if_freq, if_frequencies)):
                update_frequency(qb_el, qb_ge_if)
                play(r180, qb_el)                
                align()
                update_frequency(qb_el, if_freq)
                play('saturation' * amp(qb_gain), qb_el, duration=qb_len)
                align(ro_el, qb_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks), ro_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
            n_st.save("iteration")
        return qubit_spec
    
def temporal_rabi(ro_el, qb_el, qb_gain:int, qb_therm_clks, num_clock_cycles, pulse="gaussian_X", n_avg:int=1):
    """
    Perform Rabi oscillations in the time domain by varying the pulse duration (in clock cycles).

    Parameters:
        ro_el             : Readout resonator element
        qb_el             : Qubit element
        qb_gain           : Gain for the qubit drive pulse
        qb_therm_clks     : Thermalization wait after each measurement
        num_clock_cycles  : Array/list of pulse durations (in clock cycles) to use
        pulse             : Name of the qubit drive pulse (default "gaussian_X")
        n_avg             : Number of averaging iterations (default=1)
    """
    with program() as rabi_prog:
        num_cycles = declare(int)
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(num_cycles, num_clock_cycles)):
                play(pulse*amp(qb_gain), qb_el, duration=num_cycles)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(num_clock_cycles)).average().save("I")
            Q_st.buffer(len(num_clock_cycles)).average().save("Q")
            n_st.save("iteration")
    return rabi_prog

def power_rabi(ro_el, qb_el, qb_clock_len:int, gains, qb_therm_clks, pulse="gaussian_X", n_avg:int=1000):
    """
    Perform Rabi oscillations in the amplitude domain by sweeping pulse amplitude (gain).

    Parameters:
        ro_el          : Readout resonator element
        qb_el          : Qubit element
        qb_clock_len   : Fixed pulse duration (in clock cycles) for Rabi drive
        gains          : Python array/list of gain (amplitude) values to test
        qb_therm_clks  : Wait time (in clock cycles) for thermalization
        pulse          : Name of the qubit drive pulse (default "gaussian_X")
        n_avg          : Number of averaging iterations (default=1000)
    """
    with program() as power_rabi_prog:
        g = declare(float)
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_each_(g, gains):
                play(pulse*amp(g), qb_el, duration=qb_clock_len)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(gains)).average().save("I")
            Q_st.buffer(len(gains)).average().save("Q")
            n_st.save("iteration")
    return power_rabi_prog

def time_rabi_chevron(ro_el, qb_el, pulse, pulse_gain, qb_if, dfs, duration_clks, qb_therm_clks, n_avg:int=1):
    """
    Generate a Rabi chevron (time vs. frequency) by sweeping both pulse duration and detuning.

    Parameters:
        ro_el           : Readout resonator element
        qb_el           : Qubit element
        pulse           : Name of the qubit drive pulse
        pulse_gain      : Gain amplitude for the qubit pulse
        qb_if           : Base IF for the qubit drive
        dfs             : Python array/list of frequency detunings relative to qb_if
        duration_clks   : Python array/list of pulse durations (clock cycles)
        qb_therm_clks   : Thermalization wait time after readout
        n_avg           : Number of averaging iterations (default=1)
    """
    with program() as time_rabi_chevron_program:
        n = declare(int)
        f = declare(int)
        t = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, duration_clks)):
                with for_(*from_array(f, dfs)):
                    update_frequency(qb_el, f + qb_if)
                    play(pulse * amp(pulse_gain), qb_el, duration=t)
                    align(qb_el, ro_el)
                    I, Q = measureMacro.measure(I=I, Q=Q)
                    wait(int(qb_therm_clks), ro_el)
                    save(I, I_st)
                    save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(len(dfs)).buffer(len(duration_clks)).average().save("I")
            Q_st.buffer(len(dfs)).buffer(len(duration_clks)).average().save("Q")
            n_st.save("iteration")
    return time_rabi_chevron_program

def power_rabi_chevron(ro_el, qb_el, pulse, pulse_duration, qb_if, dfs, amplitudes, qb_therm_clks, n_avg:int=1):
    """
    Generate a Rabi chevron (power vs. frequency) by sweeping both pulse amplitude and detuning.

    Parameters:
        ro_el           : Readout resonator element
        qb_el           : Qubit element
        pulse           : Name of the qubit drive pulse
        pulse_duration  : Fixed duration (in clock cycles) for each pulse
        qb_if           : Base IF for the qubit drive
        dfs             : Python array/list of detunings relative to qb_if
        amplitudes      : Python array/list of gain amplitudes to sweep
        qb_therm_clks   : Thermalization wait after readout
        n_avg           : Number of averaging iterations (default=1)
    """
    with program() as rabi_chevron_prog:
        n = declare(int)
        df = declare(int)
        a = declare(fixed)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amplitudes)):
                with for_(*from_array(df, dfs)):
                    update_frequency(qb_el, df + qb_if)
                    play(pulse * amp(a), qb_el, duration=pulse_duration)
                    align(qb_el, ro_el)
                    I, Q = measureMacro.measure(I=I, Q=Q)
                    wait(int(qb_therm_clks), ro_el)
                    save(I, I_st)
                    save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(dfs)).buffer(len(amplitudes)).average().save("I")
            Q_st.buffer(len(dfs)).buffer(len(amplitudes)).average().save("Q")
            n_st.save("iteration")
    return rabi_chevron_prog

def ramsey_chevron(ro_el, qb_el, r90, qb_if, dfs, delay_clks, qb_therm_clks, n_avg:int=1):
    """
    Perform Ramsey chevron: sweep both delay time and detuning to map out Ramsey fringes.

    Parameters:
        ro_el           : Readout resonator element
        qb_el           : Qubit element
        r90             : Name of the π/2 pulse used to prepare/close Ramsey
        qb_if           : Base IF for qubit drive
        dfs             : Python array/list of detunings relative to qb_if
        delay_clks      : Python array/list of free-evolution delays (in clock cycles)
        qb_therm_clks   : Thermalization wait after readout
        n_avg           : Number of averaging iterations (default=1)
    """
    with program() as ramsey_chevron_prog:
        n = declare(int)
        df = declare(int)
        delay = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(delay, delay_clks)):
                with for_(*from_array(df, dfs)):
                    update_frequency(qb_el, df + qb_if)
                    with if_(delay >= 4):
                        play(r90, qb_el)
                        wait(delay, qb_el)
                        play(r90, qb_el)
                    with else_():
                        play(r90, qb_el)
                        play(r90, qb_el)
                    align(qb_el, ro_el)
                    I, Q = measureMacro.measure(I=I, Q=Q)
                    wait(int(qb_therm_clks), ro_el)
                    save(I, I_st)
                    save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(dfs)).buffer(len(delay_clks)).average().save("I")
            Q_st.buffer(len(dfs)).buffer(len(delay_clks)).average().save("Q")
            n_st.save("iteration")
    return ramsey_chevron_prog

def T1_relaxation(ro_el, qb_el, r180, wait_cycles_list, qb_therm_clks, n_avg):
    """
    Measure T₁ (energy relaxation) by applying a π-pulse and then waiting variable times.

    Parameters:
        ro_el             : Readout resonator element
        qb_el             : Qubit element
        r180              : Name of the π-pulse that inverts |g>→|e>
        wait_cycles_list  : Python array/list of wait times (in clock cycles) before readout
        qb_therm_clks     : Thermalization wait after readout
        n_avg             : Number of averaging iterations
    """
    with program() as T1_prog:
        cycles_to_wait = declare(int)
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(cycles_to_wait, wait_cycles_list)):
                play(r180, qb_el)
                align(qb_el, ro_el)
                wait(cycles_to_wait)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(wait_cycles_list)).average().save("I")
            Q_st.buffer(len(wait_cycles_list)).average().save("Q")
            n_st.save("iteration")
    return T1_prog

def T2_ramesy(ro_el, qb_el,  r90, wait_cycles_list, qb_therm_clks, n_avg):
    """
    Measure T₂* (Ramsey dephasing) by applying two π/2 pulses separated by variable wait times.

    Parameters:
        ro_el             : Readout resonator element
        qb_el             : Qubit element
        r90               : Name of the π/2 pulse
        wait_cycles_list  : Python array/list of free-evolution delays (clock cycles)
        qb_therm_clks     : Thermalization wait after readout
        n_avg             : Number of averaging iterations
    """
    with program() as T2_ramsey_prog:
        cycles_to_wait = declare(int)
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(cycles_to_wait, wait_cycles_list)):
                play(r90, qb_el)
                wait(cycles_to_wait, qb_el)
                play(r90, qb_el)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(wait_cycles_list)).average().save("I")
            Q_st.buffer(len(wait_cycles_list)).average().save("Q")
            n_st.save("iteration")
    return T2_ramsey_prog

def T2_echo(ro_el, qb_el,  r180, r90,
            half_wait_cycles_list, qb_therm_clks, n_avg):
    """
    Measure T₂ (Hahn echo) by applying π/2 – wait – π – wait – π/2 sequence,
    with the wait time swept in half-intervals.

    Parameters:
        ro_el                : Readout resonator element
        qb_el                : Qubit element
        r180                 : Name of the π-pulse
        r90                  : Name of the π/2 pulse
        half_wait_cycles_list: Python array/list of half-wait times
        qb_therm_clks        : Thermalization wait after measurement
        n_avg                : Number of averaging iterations
    """
    with program() as T2_echo_prog:
        cycles_to_wait = declare(int)
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(cycles_to_wait, half_wait_cycles_list)):
                play(r90, qb_el)
                wait(cycles_to_wait, qb_el)
                play(r180, qb_el)
                wait(cycles_to_wait, qb_el)
                play(r90, qb_el)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(half_wait_cycles_list)).average().save("I")
            Q_st.buffer(len(half_wait_cycles_list)).average().save("Q")
            n_st.save("iteration")
    return T2_echo_prog

def readout_optimization(ro_el, qb_el, ro_pulse_list, ro_gains: int, r180, qb_therm_clks, n_avg:int=1):
    """
    Optimize readout fidelity by sweeping multiple readout pulses and gain settings,
    and measuring both ground (no π) and excited (with π from |g>→|e>) signals.

    Parameters:
        ro_el        : Readout resonator element
        qb_el        : Qubit element
        ro_pulse_list: List of candidate readout pulse names to evaluate
        ro_gains     : List/array of readout gains to test
        r180         : Name of the π-pulse that prepares |e>
        qb_therm_clks: Thermalization wait time after readout
        n_avg        : Number of averaging iterations per setting (default=1)
    """
    I_wts, Q_wts = measureMacro.get_IQ_mod()
    measureMacro.reset_weights()
    with program() as readout_optimization_prog:
        n = declare(int)
        I = declare(fixed) 
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        ro_g = declare(fixed)
        n_st = declare_stream()
        
        with for_(n, 0, n < n_avg, n + 1):
            for ro_pulse in ro_pulse_list:
                measureMacro.set_pulse(ro_pulse)
                with for_(*from_array(ro_g, ro_gains)):
                    I, Q = measureMacro.measure(I=I, Q=Q, gain=ro_g)
                    wait(int(qb_therm_clks), ro_el)
                    save(I, I_st)
                    save(Q, Q_st)

                    align()

                    play(r180, qb_el)
                    align(qb_el, ro_el)
                    I, Q = measureMacro.measure(I=I, Q=Q, gain=ro_g)
                    wait(int(qb_therm_clks), ro_el)

                    save(I, I_st)
                    save(Q, Q_st)
                save(n, n_st)
        with stream_processing():
            I_st.buffer(2).buffer(len(ro_gains)).buffer(len(ro_pulse_list)).save_all("I")
            Q_st.buffer(2).buffer(len(ro_gains)).buffer(len(ro_pulse_list)).save_all("Q")
            n_st.save("iteration")
    measureMacro.reset()
    measureMacro.set_IQ_mod(I_wts, Q_wts)
    return readout_optimization_prog

def pulsed_resonator_spectroscopy(ro_el, qb_el, if_frequencies,  pulse, pulse_gain, pulse_len, qb_therm_clks, n_avg):
    """
    Perform pulsed resonator spectroscopy by first driving the qubit with a dedicated pulse,
    then immediately measuring the readout resonator as a function of IF.

    Parameters:
        ro_el          : Readout resonator element
        qb_el          : Qubit element
        if_frequencies : Array/list of IF frequencies to sweep on the readout
        pulse          : Name of the qubit drive pulse to apply pre-measurement
        pulse_gain     : Gain amplitude for the qubit pulse
        pulse_len      : Duration of the qubit pulse (in clock cycles); divided by 4 for QUA
        qb_therm_clks  : Thermalization wait after measurement
        n_avg          : Number of averaging iterations
    """
    with program() as pulsed_ro_program:
        ro_if = declare(int) 
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(ro_if, if_frequencies)):
                update_frequency(ro_el, ro_if)
                play(pulse*amp(pulse_gain), qb_el, duration=int(pulse_len/4))
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
            n_st.save("iteration")
    return pulsed_ro_program

def two_gate_operation(ro_el, qb_el,  pulse1, pulse1_gain, pulse1_len, pulse2, pulse2_gain, pulse2_len, qb_therm_clks, n_avg):
    with program() as two_gate_program:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            play(pulse1*amp(pulse1_gain), qb_el, duration=int(pulse1_len/4))
            play(pulse2*amp(pulse2_gain), qb_el, duration=int(pulse2_len/4))
            align()
            I, Q = measureMacro.measure(I=I, Q=Q)
            wait(int(qb_therm_clks))
            save(I, I_st)
            save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.average().save("I")
            Q_st.average().save("Q")
            n_st.save("iteration")
        
    return two_gate_program
    
def single_qb_rotations(ro_el, qb_el,  rotations:list[str], qb_therm_clks, n_avg):
    with program() as single_rot_prog:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            for rotation in rotations:
                play(rotation, qb_el)
            align()
            I, Q = measureMacro.measure(I=I, Q=Q)
            wait(int(qb_therm_clks))
            save(I, I_st)
            save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(n_avg).save("I")
            Q_st.buffer(n_avg).save("Q")
            n_st.save("iteration")
    return single_rot_prog

def iq_blobs(ro_el, qb_el,  r180, qb_therm_clks, n_runs):
    with program() as IQ_blobs_program:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_runs, n + 1):
            I, Q = measureMacro.measure(I=I, Q=Q)
            wait(int(qb_therm_clks), ro_el)
            save(I, I_st)
            save(Q, Q_st)

            align()
            play(r180, qb_el)
            align(qb_el, ro_el)

            I, Q = measureMacro.measure(I=I, Q=Q)
            wait(int(qb_therm_clks), ro_el)
            save(I, I_st)
            save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(2).save_all("I")
            Q_st.buffer(2).save_all("Q")
            n_st.save("iteration")
    return IQ_blobs_program

def readout_leakage_benchmarking(ro_el, qb_el, r180, control_bits, qb_therm_clks, num_sequences, n_avg):
    bit_rows, num_bits = control_bits.shape
    num_bits += 1
    with program() as ro_leakage_bm:
        sequence_num = declare(int)
        n = declare(int)
        i_mem = declare(int)

        I     = declare(fixed)
        Q     = declare(fixed)
        state = declare(bool)

        I_st = declare_stream()
        Q_st = declare_stream()
        state_st = declare_stream() 
        sequence_num_st = declare_stream()

        for sequence_idx, bit_row in enumerate(control_bits):
            assign(sequence_num, sequence_idx)
            with for_(n, 0, n < n_avg, n + 1):
                I, Q, state = measureMacro.measure(with_state=True,
                                                I=I, Q=Q, state=state)
                align(ro_el, qb_el)

                save(I, I_st)
                save(Q, Q_st)
                save(state, state_st)                    
                with for_each_(i_mem, bit_row):
                    with if_(i_mem == 1):
                        play(r180, qb_el)                          # π-pulse
                    with else_():
                        play(r180*amp(0), qb_el)                   # identity
                    #wait(tau_buffer, qb_el)
                    align(qb_el, ro_el)

                    I, Q, state = measureMacro.measure(with_state=True,
                                                    I=I, Q=Q, state=state)
                    save(I, I_st)
                    save(Q, Q_st)
                    save(state, state_st)

                wait(int(qb_therm_clks), qb_el, ro_el)
            save(sequence_num, sequence_num_st)

        with stream_processing():
            I_st.buffer(num_bits).buffer(n_avg).buffer(bit_rows).save("I")
            Q_st.buffer(num_bits).buffer(n_avg).buffer(bit_rows).save("Q")
            state_st.buffer(num_bits).buffer(n_avg).buffer(bit_rows).save("state_flag")
            sequence_num_st.save("iteration")
    return ro_leakage_bm

def all_xy(ro_el, qb_el,  allxy_rotation_sequences, qb_therm_clks, n_avg):
    with program() as all_xy:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            for gate_num, (rot1, rot2) in enumerate(allxy_rotation_sequences):
                
                play(rot1, qb_el)
                play(rot2, qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(qb_therm_clks))
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(allxy_rotation_sequences)).average().save("I")
            Q_st.buffer(len(allxy_rotation_sequences)).average().save("Q")
            n_st.save("iteration")
    return all_xy

def drag_calibration(ro_el, qb_el,  drag_amp_list, x180, x90, y180, y90, qb_therm_clks, n_avg):
    with program() as drag_calibration:
        n = declare(int)
        drag_amp = declare(fixed)
        I1 = declare(fixed)
        Q1 = declare(fixed)
        I2 = declare(fixed)
        Q2 = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        iter_st = declare_stream()
        iter = declare(int, 0)
        with for_(*from_array(drag_amp, drag_amp_list)):
            with for_(n, 0, n < n_avg, n + 1):                
                play(x180*amp(1, 0, 0, drag_amp), qb_el)
                play(y90*amp(drag_amp, 0, 0, 1), qb_el)
                align()
                I1, Q1 = measureMacro.measure(I1, Q1)
                wait(int(qb_therm_clks))
                save(I1, I_st)
                save(Q1, Q_st)
            assign(iter, iter+1)
            save(iter, iter_st)
        
        wait(int(qb_therm_clks))
        with for_(*from_array(drag_amp, drag_amp_list)):
            with for_(n, 0, n < n_avg, n + 1):
                play(y180*amp(drag_amp, 0, 0, 1), qb_el)
                play(x90*amp(1, 0, 0, drag_amp), qb_el)
                align()
                I2, Q2 = measureMacro.measure(I2, Q2)
                wait(int(qb_therm_clks))
                save(I2, I_st)
                save(Q2, Q_st)
            assign(iter, iter+1)
            save(iter, iter_st)
        with stream_processing():
            I_st.buffer(n_avg).buffer(len(drag_amp_list)).buffer(2).save("I")
            Q_st.buffer(n_avg).buffer(len(drag_amp_list)).buffer(2).save("Q")
            iter_st.save("iteration")
    return drag_calibration

def storage_spectroscopy(ro_el, qb_el, st_el, if_frequencies, st_therm_clks, n_avg):
    with program() as storage_spec:
        n = declare(int)
        f = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(f, if_frequencies)):
                update_frequency(st_el, f)
                play("const_disp", st_el)
                align()
                play("sel_x180", qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
            n_st.save("iteration")
    return storage_spec

def time_storage_displacement(ro_el, qb_el, st_el, disp_pulse, sel_r180_pulse, duration_clks, st_therm_clks, n_avg):
    with program() as storage_displacement:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        t = declare(int)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, duration_clks)):
                play(disp_pulse, st_el, duration=t)
                align(qb_el, st_el)
                play(sel_r180_pulse, qb_el)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                align(st_el, ro_el)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(len(duration_clks)).average().save("I")
            Q_st.buffer(len(duration_clks)).average().save("Q")
            n_st.save("iteration")
    return storage_displacement

def power_storage_displacement(ro_el, qb_el, st_el, disp_pulse, sel_r180_pulse, gains, st_therm_clks, n_avg):
    with program() as storage_displacement:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        g = declare(int)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(g, gains)):
                play(disp_pulse*amp(g), st_el)
                align(qb_el, st_el)
                play(sel_r180_pulse, qb_el)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                align(st_el, ro_el)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(len(gains)).average().save("I")
            Q_st.buffer(len(gains)).average().save("Q")
            n_st.save("iteration")
    return storage_displacement

def num_splitting_spectroscopy(ro_el, qb_el, st_el, disp_pulse, sel_r180_pulse, if_frequencies, st_therm_clks, n_avg):
    with program() as num_splitting_spectroscopy_program:
        n = declare(int)
        f = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(f, if_frequencies)):
                update_frequency(qb_el, f)
                play(disp_pulse, st_el)
                align()
                play(sel_r180_pulse, qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(if_frequencies)).average().save("I")
            Q_st.buffer(len(if_frequencies)).average().save("Q")
            n_st.save("iteration")
    return num_splitting_spectroscopy_program


def fock_population_measurement(ro_el, qb_el, st_el, disp_pulse, center_if_frequencies, sel_r180_pulse, st_therm_clks, n_avg):
    with program() as fock_population_measurement:
        n = declare(int)
        f = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            for center_f in center_if_frequencies:
                update_frequency(qb_el, center_f)
                play(disp_pulse, st_el)
                align()
                play(sel_r180_pulse, qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(center_if_frequencies)).average().save("I")
            Q_st.buffer(len(center_if_frequencies)).average().save("Q")
            n_st.save("iteration")
    return fock_population_measurement

def ramsey_interferometry(ro_el, qb_el, st_el, disp_pulse, delays, sel_r90_pulse, st_therm_clks, n_avg):
    with program() as ramsey_interferometry:
        n = declare(int)
        t = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(t, delays)):
                play(disp_pulse, st_el)
                align()
                play(sel_r90_pulse, qb_el)
                wait(t, qb_el, ro_el)
                play(sel_r90_pulse, qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
                save(n, n_st)
        with stream_processing():
            I_st.buffer(len(delays)).average().save("I")
            Q_st.buffer(len(delays)).average().save("Q")
            n_st.save("iteration")
    return ramsey_interferometry

def storage_power_rabi(ro_el, qb_el, st_el, sel_r180_pulse, disp_pulse, st_therm_clks, gains, n_avg):
    with program() as storage_power_rabi:
        n = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        g = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(g, gains)):
                play(disp_pulse, st_el)
                align(qb_el, st_el)
                play(sel_r180_pulse*amp(g), qb_el)
                align(qb_el, ro_el)
                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)

        with stream_processing():
            I_st.buffer(len(gains)).average().save("I")
            Q_st.buffer(len(gains)).average().save("Q")
            n_st.save("iteration")
    return storage_power_rabi

def storage_gates_num_splitting(
        ro_el, st_el, qb_el,
        gates: list[Gate],
        qb_if,         
        probe_ifs,                  
        sel_r180,
        st_therm_clks,              
        n_avg                       
):
    
    probe_ifs = np.array(probe_ifs, dtype=int)
    with program() as prog:
        n = declare(int)
        f = declare(int)
        I = declare(fixed)
        Q = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_each_(f, probe_ifs):
                update_frequency(qb_el, qb_if)
                for gate in gates:
                    gate.play()
                
                # probe the state on the selective frequency
                update_frequency(qb_el, f)
                align(qb_el, st_el)
                play(sel_r180, qb_el)
                align(qb_el, ro_el)

                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)
                save(I, I_st)
                save(Q, Q_st)
            save(n, n_st)
        with stream_processing():
            I_st.buffer(len(probe_ifs)).average().save("I")
            Q_st.buffer(len(probe_ifs)).average().save("Q")
            n_st.save("iteration")
    return prog


def storage_wigner_tomography(
        prep_gates: list[Gate],             # Python list of Gate instances to prepare ρ
        st_el, qb_el, ro_el,
        base_disp,
        x_vals, p_vals, base_alpha,
        x90_pulse,              # fast π/2 on the qubit
        parity_wait_clks,       # ≃ π/χ, in clock ticks
        st_therm_clks,          # storage cooldown
        n_avg                   # number of repeats
):
    m00_list, m01_list, m10_list, m11_list = [], [], [], []
    for p in p_vals:         
        for x in x_vals:      
            ratio  = -(x + 1j*p) / base_alpha
            norm   = abs(ratio)
            c, s   = ratio.real / norm, ratio.imag / norm   if norm else (0.0, 0.0)
            m00_list.append(norm*c)
            m01_list.append(-norm*s)
            m10_list.append(norm*s)
            m11_list.append(norm*c)

    m_matrix = (m00_list, m01_list, m10_list, m11_list)

    with program() as prog:
        rep = declare(int) 
        I, Q = declare(fixed), declare(fixed)
        m00 = declare(fixed)
        m01 = declare(fixed)
        m10 = declare(fixed)
        m11 = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(rep, 0, rep < n_avg, rep + 1):
            with for_each_((m00, m01, m10, m11), m_matrix):
                for gate in prep_gates:
                    gate.play()
                align(st_el, qb_el)

                play(base_disp * amp(m00, m01, m10, m11), st_el)

                play(x90_pulse, qb_el)
                wait(int(parity_wait_clks), qb_el)
                play(x90_pulse, qb_el)
                align(qb_el, ro_el)

                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)

                save(I, I_st)
                save(Q, Q_st)

            save(rep, n_st)

        with stream_processing():
            I_st.buffer(len(x_vals)).buffer(len(p_vals)).average().save("I")
            Q_st.buffer(len(x_vals)).buffer(len(p_vals)).average().save("Q")
            n_st.save("iteration")

    return prog

def phase_evolution_prog(ro_el, qb_el, st_el,
                         disp_alpha_pulse, disp_eps_pulse,
                         sel_r180_pulse,
                         fock0_if, 
                         fock_probe_ifs,
                         delay_clks,
                         snap_list,
                         st_therm_clks, n_avg):

    fock_probe_ifs = np.array(fock_probe_ifs, dtype=int)
    fock_dim = len(fock_probe_ifs)
    delay_dim = len(delay_clks)
    theta_dim = len(snap_list)
    with program() as prog:
        rep   = declare(int)
        d_idx = declare(int)
        I, Q  = declare(fixed), declare(fixed)
        I_st, Q_st, n_st = declare_stream(), declare_stream(), declare_stream()

        fock_n_if = declare(int)
        with for_(rep, 0, rep < n_avg, rep + 1):
            with for_(*from_array(d_idx, delay_clks)):
                for snap in snap_list:
                    with for_each_(fock_n_if, fock_probe_ifs):
                        reset_frame(st_el)
                        reset_frame(qb_el)
                        update_frequency(qb_el, fock0_if)

                        play(disp_alpha_pulse, st_el)
                        align(qb_el, st_el)
                        
                        with if_(d_idx>0):
                            wait(d_idx, st_el, qb_el)  

                        play(snap, qb_el)
                        align(qb_el, st_el)

                        play(disp_eps_pulse, st_el)

                        align()

                        update_frequency(qb_el, fock_n_if)
                        play(sel_r180_pulse, qb_el) 
                        align(qb_el, ro_el)                        
                        I, Q = measureMacro.measure(I=I, Q=Q)
                        wait(int(st_therm_clks), st_el)

                        save(I, I_st)
                        save(Q, Q_st)
            save(rep, n_st)
        with stream_processing():
            I_st.buffer(fock_dim).buffer(theta_dim).buffer(delay_dim).average().save("I")
            Q_st.buffer(fock_dim).buffer(theta_dim).buffer(delay_dim).average().save("Q")
            n_st.save("iteration")

    return prog


def storage_chi_ramsey(
    ro_el, qb_el, st_el,
    disp_pulse,           # displacement pulse to put n photons in the cavity
    x90_pulse,            # π/2 pulse on the qubit
    delay_ticks,          # list/ndarray of waiting‐time values (in clock ticks)
    st_therm_clks,        # cooldown for storage (in clock ticks)
    n_avg                 # number of averages
):
    with program() as prog:
        rep = declare(int)
        tau   = declare(int)
        I   = declare(fixed)
        Q   = declare(fixed)

        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(rep, 0, rep < n_avg, rep + 1):

            # sweep Ramsey waiting time
            with for_(*from_array(tau, delay_ticks)):
                play(disp_pulse, st_el)
                align(st_el, qb_el)
                play(x90_pulse, qb_el)
                wait(tau, qb_el)
                play(x90_pulse, qb_el)
                align(qb_el, ro_el)

                I, Q = measureMacro.measure(I=I, Q=Q)
                wait(int(st_therm_clks), st_el)

                save(I, I_st)
                save(Q, Q_st)
            save(rep, n_st)
        with stream_processing():
            I_st.buffer(len(delay_ticks)).average().save("I")
            Q_st.buffer(len(delay_ticks)).average().save("Q")
            n_st.save("iteration")

    return prog

def storage_ramsey(
    ro_el, qb_el, st_el,
    disp_pulse,           # displacement pulse to put n photons in the cavity
    sel_r180,            # π/2 pulse on the qubit
    delay_ticks,          # list/ndarray of waiting‐time values (in clock ticks)
    st_therm_clks,        # cooldown for storage (in clock ticks)
    n_avg                 # number of averages
):
    with program() as prog:
        rep = declare(int)
        tau   = declare(int)
        I   = declare(fixed)
        Q   = declare(fixed)

        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        # average loop
        with for_(rep, 0, rep < n_avg, rep + 1):

            # sweep Ramsey waiting time
            with for_(*from_array(tau, delay_ticks)):

                # prepare one‐photon (or coherent) state in storage
                play(disp_pulse, st_el)
                wait(tau)
                align(st_el)
                play(disp_pulse*amp(0, 1, 1, 0), st_el)
                align(st_el)
                play(sel_r180, qb_el)
                align()
                I, Q = measureMacro.measure(I=I, Q=Q)

                # re‐thermalize storage
                wait(int(st_therm_clks), st_el)

                save(I, I_st)
                save(Q, Q_st)

            # progress counter
            save(rep, n_st)

        # stream processing: buffer over τ, then average over reps
        with stream_processing():
            I_st.buffer(len(delay_ticks)).average().save("I")
            Q_st.buffer(len(delay_ticks)).average().save("Q")
            n_st.save("iteration")

    return prog


def storage_kerr_ramsey(
    ro_el, qb_el, st_el,
    disp_pulse,           # displacement pulse to put n photons in the cavity
    gain_list,
    sel_r180,            # π/2 pulse on the qubit
    delay_ticks,          # list/ndarray of waiting‐time values (in clock ticks)
    st_therm_clks,        # cooldown for storage (in clock ticks)
    n_avg                 # number of averages
):
    with program() as prog:
        rep = declare(int)
        τ   = declare(int)
        g   = declare(fixed)
        I   = declare(fixed)
        Q   = declare(fixed)

        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(rep, 0, rep < n_avg, rep + 1):
            with for_(*from_array(g, gain_list)):
                with for_(*from_array(τ, delay_ticks)):
                    play(disp_pulse*amp(g, 0, 0, g), st_el)
                    wait(τ, st_el)
                    play(disp_pulse*amp(-g, 0, 0, -g), st_el)

                    align(st_el, qb_el)
                    play(sel_r180, qb_el)
                    align(qb_el, ro_el)

                    I, Q = measureMacro.measure(I=I, Q=Q)
                    wait(int(st_therm_clks), st_el)

                    save(I, I_st)
                    save(Q, Q_st)
            save(rep, n_st)

        with stream_processing():
            I_st.buffer(len(delay_ticks)).buffer(len(gain_list)).average().save("I")
            Q_st.buffer(len(delay_ticks)).buffer(len(gain_list)).average().save("Q")
            n_st.save("iteration")

    return prog

def selective_ramsey_phase(
        st_el, qb_el, ro_el,
        sel_r180,          # name (str) of the calibrated selective π on |n>
        sel_IFs,               # list / ndarray of IFs  (one per n you want)
        snap_name,             # SNAP gate under test  (string, already in cfg)
        disp_pulse,
        ramsey_phases,         # list / ndarray of Z-frame angles φ  [rad]
        r90,             # fast π/2 (or y90) analyser on the qubit
        st_therm_clks,         # cooldown for storage [clock ticks]
        n_avg                  # number of averages
):
    sel_IFs = np.array(sel_IFs, dtype=int)
    with program() as prog:

        rep  = declare(int)
        phi  = declare(fixed) 
        f_if = declare(int)

        I   = declare(fixed)
        Q   = declare(fixed)
        I_st = declare_stream()
        Q_st = declare_stream()
        n_st = declare_stream()

        with for_(rep, 0, rep < n_avg, rep + 1):
            with for_each_(f_if, sel_IFs):
                update_frequency(qb_el, f_if)
                with for_(*from_array(phi, ramsey_phases)):
                    play(disp_pulse, st_el)
                    align(st_el, qb_el)

                    play(sel_r180, qb_el) 
                    play(snap_name, qb_el)              
                    play(sel_r180, qb_el)              
                    align(st_el, qb_el)

                    frame_rotation(phi, qb_el)     
                    play(r90, qb_el)                 
                    align(qb_el, ro_el)

                    I, Q = measureMacro.measure(I=I, Q=Q)
                    wait(int(st_therm_clks), st_el)       

                    save(I, I_st)
                    save(Q, Q_st)
            save(rep, n_st)                              
        with stream_processing():
            I_st.buffer(len(ramsey_phases)).buffer(len(sel_IFs)).average().save("I")
            Q_st.buffer(len(ramsey_phases)).buffer(len(sel_IFs)).average().save("Q")
            n_st.save("iteration")

    return prog

    

def continuous_wave(target_el, pulse, truncate_clks):
    with program() as prog:
        with infinite_loop_():
            play(pulse, target_el, truncate=truncate_clks)

    return prog

""" 
                update_frequency(qb_el, f_if)
                with for_(*from_array(phi, ramsey_phases)):

                    play(sel_pi_pulse, qb_el)               # first π_sel(n)
                    play(snap_name,     qb_el)              # SNAP under test
                    align(st_el, qb_el)
                    play(sel_pi_pulse, qb_el)               # second π_sel(n)

                    frame_rotation(phi, qb_el)     
                    play(x90_pulse, qb_el)                  # π/2 analyser
                    align(qb_el, ro_el)

                    I, Q = measureMacro.measure(I=I, Q=Q)   # qubit readout
                    wait(int(st_therm_clks), st_el)         # cavity cool-down

                    save(I, I_st)
                    save(Q, Q_st)

"""