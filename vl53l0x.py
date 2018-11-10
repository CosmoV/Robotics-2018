import pyb
import machine
import utime
import gc


class VL53L0X:
    def __init__(self, i2c, address):
        self.i2c = i2c
        self._address = address
        self.init(False)

    def init(self, io_2v8):
        self._set_reg8(0x88, 0x00)
        self._set_reg8(0x80, 0x01)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x00, 0x00)
        self.stop_variable = self._get_reg8(0x91)
        self._set_reg8(0x00, 0x01)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x80, 0x00)
        self._set_reg8(0x60, (self._get_reg8(0x60) | 0x12))
        self.set_signal_rate_limit(0.25)
        self._set_reg8(0x01, 0xFF)
        spad_count, spad_type_is_aperture, spad_test = self.get_spad_info()
        if not spad_test:
            return False
        ref_spad_map = self._read_multiple(0xB0, 6)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x4F, 0x00)
        self._set_reg8(0x4E, 0x2C)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0xB6, 0xB4)
        if spad_type_is_aperture:
            first_spad_to_enable = 12
        else:
            first_spad_to_enable = 0
        spads_enabled = 0

        for i in range(48):  # i = 0 ... 47
            if (i < first_spad_to_enable) or (spads_enabled == spad_count):
                ref_spad_map[i // 8] &= ~(1 << (i % 8))
            elif (ref_spad_map[i // 8] >> (i % 8)) & 0x1:
                spads_enabled += 1
        self._write_multiple(0xB0, ref_spad_map)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x00, 0x00)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x09, 0x00)
        self._set_reg8(0x10, 0x00)
        self._set_reg8(0x11, 0x00)
        self._set_reg8(0x24, 0x01)
        self._set_reg8(0x25, 0xFF)
        self._set_reg8(0x75, 0x00)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x4E, 0x2C)
        self._set_reg8(0x48, 0x00)
        self._set_reg8(0x30, 0x20)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x30, 0x09)
        self._set_reg8(0x54, 0x00)
        self._set_reg8(0x31, 0x04)
        self._set_reg8(0x32, 0x03)
        self._set_reg8(0x40, 0x83)
        self._set_reg8(0x46, 0x25)
        self._set_reg8(0x60, 0x00)
        self._set_reg8(0x27, 0x00)
        self._set_reg8(0x50, 0x06)
        self._set_reg8(0x51, 0x00)
        self._set_reg8(0x52, 0x96)
        self._set_reg8(0x56, 0x08)
        self._set_reg8(0x57, 0x30)
        self._set_reg8(0x61, 0x00)
        self._set_reg8(0x62, 0x00)
        self._set_reg8(0x64, 0x00)
        self._set_reg8(0x65, 0x00)
        self._set_reg8(0x66, 0xA0)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x22, 0x32)
        self._set_reg8(0x47, 0x14)
        self._set_reg8(0x49, 0xFF)
        self._set_reg8(0x4A, 0x00)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x7A, 0x0A)
        self._set_reg8(0x7B, 0x00)
        self._set_reg8(0x78, 0x21)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x23, 0x34)
        self._set_reg8(0x42, 0x00)
        self._set_reg8(0x44, 0xFF)
        self._set_reg8(0x45, 0x26)
        self._set_reg8(0x46, 0x05)
        self._set_reg8(0x40, 0x40)
        self._set_reg8(0x0E, 0x06)
        self._set_reg8(0x20, 0x1A)
        self._set_reg8(0x43, 0x40)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x34, 0x03)
        self._set_reg8(0x35, 0x44)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x31, 0x04)
        self._set_reg8(0x4B, 0x09)
        self._set_reg8(0x4C, 0x05)
        self._set_reg8(0x4D, 0x04)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x44, 0x00)
        self._set_reg8(0x45, 0x20)
        self._set_reg8(0x47, 0x08)
        self._set_reg8(0x48, 0x28)
        self._set_reg8(0x67, 0x00)
        self._set_reg8(0x70, 0x04)
        self._set_reg8(0x71, 0x01)
        self._set_reg8(0x72, 0xFE)
        self._set_reg8(0x76, 0x00)
        self._set_reg8(0x77, 0x00)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x0D, 0x01)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x80, 0x01)
        self._set_reg8(0x01, 0xF8)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x8E, 0x01)
        self._set_reg8(0x00, 0x01)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x80, 0x00)
        self._set_reg8(0x0A, 0x04)
        self._set_reg8(0x84, self._get_reg8(0x84) & ~0x10)  # active low
        self._set_reg8(0x0B, 0x01)
        self.measurement_timing_budget_us = self.get_measurement_timing_budget()
        self._set_reg8(0x01, 0xE8)
        self.set_measurement_timing_budget(self.measurement_timing_budget_us)
        self._set_reg8(0x01, 0x01)
        if self.perform_single_ref_calibration(0x40) == False:
            return False
        self._set_reg8(0x01, 0x02)
        if not self.perform_single_ref_calibration(0x00):
            return False
        self._set_reg8(0x01, 0xE8)
        return True

    def perform_single_ref_calibration(self, vhv_init_byte):
        self._set_reg8(0x00, 0x01 | vhv_init_byte)
        start_timeout = self.start_timeout()
        while (self._get_reg8(0x13) & 0x07) == 0:
            if self.check_timeout_expired(500, start_timeout):
                return False
        self._set_reg8(0x0B, 0x01)
        self._set_reg8(0x00, 0x00)
        return True

    def set_signal_rate_limit(self, limit_Mcps):
        if (limit_Mcps < 0) or (limit_Mcps > 511.99):
            return False
        self._set_reg16(0x44, int(limit_Mcps * (1 << 7)))  # ??????????
        return True

    def get_spad_info(self):
        self._set_reg8(0x80, 0x01)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x00, 0x00)
        self._set_reg8(0xFF, 0x06)
        self._set_reg8(0x83, self._get_reg8(0x83) | 0x04)
        self._set_reg8(0xFF, 0x07)
        self._set_reg8(0x81, 0x01)
        self._set_reg8(0x80, 0x01)
        self._set_reg8(0x94, 0x6b)
        self._set_reg8(0x83, 0x00)
        start_timeout = self.start_timeout()
        while self._get_reg8(0x83) == 0x00:
            if not self.check_timeout_expired(500, start_timeout):
                return False
        self._set_reg8(0x83, 0x01)
        tmp = self._get_reg8(0x92)
        count = tmp & 0x7f
        type_is_aperture = (tmp >> 7) & 0x01
        self._set_reg8(0x81, 0x00)
        self._set_reg8(0xFF, 0x06)
        self._set_reg8(0x83, self._get_reg8(0x83) & ~0x04)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x00, 0x01)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x80, 0x00)
        return count, type_is_aperture, True

    @staticmethod
    def start_timeout():
        timeout_start_ms = int(round(utime.ticks_ms()))
        return timeout_start_ms

    @staticmethod
    def check_timeout_expired(io_timeout, timeout_start_ms):
        if 0 < io_timeout < (utime.ticks_ms() - timeout_start_ms):
            return True
        else:
            return False

    def get_measurement_timing_budget(self):
        start_overhead = 1910  # note that this is different than the value in set_
        end_overhead = 960
        msrc_overhead = 660
        tcc_overhead = 590
        dss_overhead = 690
        pre_range_overhead = 660
        final_range_overhead = 550
        budget_us = start_overhead + end_overhead

        tcc, dss, msrc, pre_range, final_range = self.enables()
        pre_range_vcsel_period_pclks, msrc_dss_tcc_mclks, msrc_dss_tcc_us, pre_range_mclks, \
        pre_range_us, final_range_vcsel_period_pclks, final_range_mclks = self.timeouts()
        if pre_range:
            final_range_mclks -= pre_range_mclks
        final_range_us = self.timeout_mclks_to_microseconds(final_range_mclks, final_range_vcsel_period_pclks)
        if tcc:
            budget_us += msrc_dss_tcc_us + tcc_overhead
        if dss:
            budget_us += 2 * (msrc_dss_tcc_us + dss_overhead)
        elif msrc:
            budget_us += msrc_dss_tcc_us + msrc_overhead
        if pre_range:
            budget_us += pre_range_us + pre_range_overhead
        if final_range:
            budget_us += final_range_us + final_range_overhead
        self.measurement_timing_budget_us = budget_us  # store for internal reuse
        return budget_us

    def enables(self):
        sequence_config = self._get_reg8(0x01)
        tcc = (sequence_config >> 4) & 0x1
        dss = (sequence_config >> 3) & 0x1
        msrc = (sequence_config >> 2) & 0x1
        pre_range = (sequence_config >> 6) & 0x1
        final_range = (sequence_config >> 7) & 0x1
        return tcc, dss, msrc, pre_range, final_range

    def timeouts(self):
        a1 = self.get_vcsel_pulse_period(1)
        a2 = self._get_reg8(0x46) + 1
        a3 = self.timeout_mclks_to_microseconds(a2, a1)
        a4 = self.decode_timeout(self._get_reg16(0x51))
        a5 = self.timeout_mclks_to_microseconds(a4, a1)
        a6 = self.get_vcsel_pulse_period(2)
        a7 = self.decode_timeout(self._get_reg16(0x71))
        return a1, a2, a3, a4, a5, a6, a7

    def set_measurement_timing_budget(self, budget_us):
        start_overhead = 1320
        end_overhead = 960
        msrc_overhead = 660
        tcc_overhead = 590
        dss_overhead = 690
        pre_range_overhead = 660
        final_range_overhead = 550
        min_timing_budget = 20000
        if budget_us < min_timing_budget:
            return False
        used_budget_us = start_overhead + end_overhead
        budget_us = start_overhead + end_overhead
        tcc, dss, msrc, pre_range, final_range = self.enables()
        pre_range_vcsel_period_pclks, msrc_dss_tcc_mclks, msrc_dss_tcc_us, pre_range_mclks, \
        pre_range_us, final_range_vcsel_period_pclks, final_range_mclks = self.timeouts()
        if pre_range:
            final_range_mclks -= pre_range_mclks
        if tcc:
            used_budget_us += msrc_dss_tcc_us + tcc_overhead
        if dss:
            used_budget_us += 2 * (msrc_dss_tcc_us + dss_overhead)
        elif msrc:
            used_budget_us += msrc_dss_tcc_us + msrc_overhead
        if pre_range:
            used_budget_us += pre_range_us + pre_range_overhead
        if final_range:
            used_budget_us += final_range_overhead
            if used_budget_us > budget_us:
                return False
            final_range_timeout_us = budget_us - used_budget_us
            final_range_timeout_mclks = \
                self.timeout_microseconds_to_mclks(final_range_timeout_us, timeouts.final_range_vcsel_period_pclks)
            if pre_range:
                final_range_timeout_mclks = final_range_timeout_mclks + timeouts.pre_range_mclks
            self._set_reg16(0x71, self.encode_timeout(final_range_timeout_mclks))
        return True

    def timeout_microseconds_to_mclks(self, timeout_period_us, vcsel_period_pclks):
        macro_period_ns = self.calc_macro_period(vcsel_period_pclks)
        return ((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns

    @staticmethod
    def decode_timeout(reg_val):
        return ((reg_val & 0x00FF) <<
                ((reg_val & 0xFF00) >> 8)) + 1

    @staticmethod
    def encode_timeout(timeout_mclks):
        ms_byte = 0
        if timeout_mclks > 0:
            ls_byte = timeout_mclks - 1
            while (ls_byte & 0xFFFFFF00) > 0:
                ls_byte >>= 1
            return (ms_byte << 8) | (ls_byte & 0xFF)
        else:
            return 0

    def timeout_mclks_to_microseconds(self, timeout_period_mclks, vcsel_period_pclks):
        macro_period_ns = self.calc_macro_period(vcsel_period_pclks)
        return ((timeout_period_mclks * macro_period_ns) + (macro_period_ns / 2)) / 1000

    @staticmethod
    def calc_macro_period(vcsel_period_pclks):
        return ((2304 * vcsel_period_pclks * 1655) + 500) / 1000

    def get_vcsel_pulse_period(self, type):
        if type == 1:
            return self.decode_vcsel_period(self._get_reg8(0x50))
        elif type == 2:
            return self.decode_vcsel_period(self._get_reg8(0x70))
        else:
            return 255

    @staticmethod
    def decode_vcsel_period(reg_val):
        return (reg_val + 1) << 1

    def start_continuous(self, period_ms):
        self._set_reg8(0x80, 0x01)
        self._set_reg8(0xFF, 0x01)
        self._set_reg8(0x00, 0x00)
        self._set_reg8(0x91, self.stop_variable)
        self._set_reg8(0x00, 0x01)
        self._set_reg8(0xFF, 0x00)
        self._set_reg8(0x80, 0x00)
        if period_ms != 0:
            osc_calibrate_val = self._get_reg16(0xF8)
            if osc_calibrate_val != 0:
                period_ms *= osc_calibrate_val
            self._set_reg32(0x04, period_ms)
            self._set_reg8(0x00, 0x04)
        else:
            self._set_reg8(0x00, 0x02)
        return

    def read_range_continuous_mm(self):
        start_timeout = self.start_timeout()
        while (self._get_reg8(0x13) & 0x07) == 0:
            if self.check_timeout_expired(500, start_timeout):
                return 65535
        range = self._get_reg16(0x14 + 10)
        self._set_reg8(0x0B, 0x01)
        return range

    @staticmethod
    def from_bytes_big(b):
        n = 0
        for x in b:
            n <<= 8
            n |= x
        return n

    def _set_reg8(self, reg_address, value):
        data = bytearray(1)
        data[0] = value
        self.i2c.writeto_mem(self._address, reg_address, data)

    def _get_reg8(self, reg_address):
        data = self.i2c.readfrom_mem(self._address, reg_address, 1)
        return self.from_bytes_big(data)

    def _set_reg16(self, reg_address, value):
        dst = bytearray(2)
        dst[0] = (value >> 8) & 0xFF
        dst[1] = (value & 0xFF)
        self.i2c.writeto_mem(self._address, reg_address, dst)

    def _get_reg16(self, reg_address):
        data = bytearray(2)
        self.i2c.readfrom_mem_into(self._address, reg_address, data)
        value = (data[0]) << 8  # value high byte
        value |= data[1] & 0xFF  # value low byte
        return value

    def _set_reg32(self, reg_address, value):
        data = bytearray(4)
        data[0] = (value >> 24) & 0xFF  # value highest byte
        data[1] = (value >> 16) & 0xFF
        data[2] = (value >> 8) & 0xFF
        data[3] = (value >> 8) & 0xFF  # value lowest byte
        self.i2c.writeto_mem(self._address, reg_address, data)
        return

    def _get_reg32(self, reg_address):
        data = bytearray(4)
        self.i2c.readfrom_into(self._address, reg_address, data)
        value = data[0] << 24  # value highest byte
        value |= data[1] << 16
        value |= data[2] << 8
        value |= data[3]  # value lowest byte
        return value

    def _read_multiple(self, reg_address, count):
        dst = bytearray(count)
        self.i2c.readfrom_mem_into(self._address, reg_address, dst)
        return dst

    def _write_multiple(self, reg_address, dst):
        self.i2c.writeto_mem(self._address, reg_address, dst)
