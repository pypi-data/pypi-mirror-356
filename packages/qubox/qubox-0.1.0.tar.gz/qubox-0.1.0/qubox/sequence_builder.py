import qm.qua as qua
import numpy as np

class Primitive:                       # Gate or Protocol
    def build(self, pulse_mgr): pass   # ← only for things that need waveforms
    def declare(self):          pass   # ← declare vars/streams (runs 1-time)
    def body(self):             pass   # ← emit the main QUA statements
    def streams(self):          pass   # ← optional: stream_processing()

class MeasureAndSave(Primitive):
    def __init__(self, ro_el, buf_len):
        self.ro_el   = ro_el
        self.buf_len = buf_len

    # 1) declarations
    def declare(self):
        self.I   = qua.declare(qua.fixed)
        self.Q   = qua.declare(qua.fixed)
        self.I_st = qua.declare_stream()
        self.Q_st = qua.declare_stream()

    # 2) body (can be called inside loops)
    def body(self):
        self.I, self.Q = measure(self.ro_el)   # <- your macro
        qua.save(self.I, self.I_st)
        qua.save(self.Q, self.Q_st)

    # 3) stream processing (runs once at end)
    def streams(self):
        self.I_st.buffer(self.buf_len).average().save("I")
        self.Q_st.buffer(self.buf_len).average().save("Q")

class Sweep(Primitive):
    """
    Wraps `sub_sequence` in a QUA `for_` or `for_each_` loop.
    `iterable` should be a Python list or NumPy array.
    """
    def __init__(self, var_name, iterable, sub_sequence):
        self.var_name = var_name
        self.iterable = iterable
        self.sub_seq  = sub_sequence
        self.var_ref  = None  # gets filled during declare()

    # (i) propagate builds from the sub-sequence
    def build(self, pulse_mgr):
        for p in self.sub_seq:
            if hasattr(p, "build"):
                p.build(pulse_mgr)

    # (ii) declarations for loop variable + any children
    def declare(self):
        self.var_ref = qua.declare(int if np.issubdtype(type(self.iterable[0]), np.integer) else qua.fixed)

        for p in self.sub_seq:
            if hasattr(p, "declare"):
                p.declare()

    # (iii) body: create the loop, then replay children
    def body(self):
        with qua.for_each_(self.var_ref, self.iterable):
            for p in self.sub_seq:
                if hasattr(p, "body"):
                    p.body()

    # (iv) stream aggregation from children
    def streams(self):
        for p in self.sub_seq:
            if hasattr(p, "streams"):
                p.streams()


class SequenceBuilder:
    def __init__(self, seq, pulse_mgr):
        self.seq, self.pulse_mgr = seq, pulse_mgr

    def build_program(self):
        # ----- pre-flight waveforms -----
        for p in self.seq:
            if hasattr(p, "build"):
                p.build(self.pulse_mgr)

        # ----- QUA generation -----
        with qua.program() as prog:
            # (i) DECLARATIONS
            for p in self.seq:
                if hasattr(p, "declare"):
                    p.declare()

            # (ii) MAIN BODY
            for p in self.seq:
                if hasattr(p, "body"):
                    p.body()

            # (iii) STREAM PROCESSING
            with qua.stream_processing():
                for p in self.seq:
                    if hasattr(p, "streams"):
                        p.streams()

        return prog
