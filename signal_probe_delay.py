# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: signal_probe_delay
# Author: zak
# Generated: Thu Dec 27 13:34:00 2018
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import threading
import time


class signal_probe_delay(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "signal_probe_delay",
            gr.io_signature(1, 1, gr.sizeof_float*1),
            gr.io_signature(1, 1, gr.sizeof_int*1),
        )

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e5
        self.flag_acq_est_0_0 = flag_acq_est_0_0 = 0
        self.flag_acq_est_0 = flag_acq_est_0 = 0
        self.once=0
        ##################################################
        # Blocks
        ##################################################

        self.blocks_probe_flag_nondelayed_0 = blocks.probe_signal_i()

        def _flag_acq_est_0_0_probe():
            while True:
                val = self.blocks_probe_flag_nondelayed_0.level()
                self.val0=val
                try:
                    self.set_flag_acq_est_0_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (16e3))
        _flag_acq_est_0_0_thread = threading.Thread(target=_flag_acq_est_0_0_probe)
        _flag_acq_est_0_0_thread.daemon = True
        _flag_acq_est_0_0_thread.start()  

        self.blocks_probe_flag_nondelayed = blocks.probe_signal_i()

        def _flag_acq_est_0_probe():
        
            while True:
                
                val = self.blocks_probe_flag_nondelayed.level()
                if self.once==0:
                 if self.val0!=val:
                     self.val1=val
                     print "hello"
                     self.once=1

                try:
                    self.set_flag_acq_est_0(self.val1)
                except AttributeError:
                    pass
                #time.sleep(1.0 / (1e6))
        _flag_acq_est_0_thread = threading.Thread(target=_flag_acq_est_0_probe)
        _flag_acq_est_0_thread.daemon = True
        _flag_acq_est_0_thread.start()

       

        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_int*1, 2)
        self.analog_const_source_x_0 = analog.sig_source_i(0, analog.GR_CONST_WAVE, 0, 0, flag_acq_est_0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_probe_flag_nondelayed_0, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.blocks_probe_flag_nondelayed, 0))
        self.connect((self, 0), (self.blocks_float_to_int_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_flag_acq_est_0_0(self):
        return self.flag_acq_est_0_0

    def set_flag_acq_est_0_0(self, flag_acq_est_0_0):
        self.flag_acq_est_0_0 = flag_acq_est_0_0

    def get_flag_acq_est_0(self):
        return self.flag_acq_est_0

    def set_flag_acq_est_0(self, flag_acq_est_0):
        self.flag_acq_est_0 = flag_acq_est_0
        self.analog_const_source_x_0.set_offset(self.flag_acq_est_0)
