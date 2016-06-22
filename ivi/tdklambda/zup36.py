# -*- coding: utf8 -*-

from .. import ivi
from .. import dcpwr
from .. import scpi

CurrentLimitBehavior = set(['regulate', 'trip'])  # TODO: 확인 필요. foldback / disable


class ZUP36(ivi.Driver, dcpwr.Base, dcpwr.Measurement):

    def __init__(self, *args, **kwargs):
        super(ZUP36, self).__init__(*args, **kwargs)

        self._output_spec[0]['voltage_max'] = 36.0

    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if (value < 0) or (value > self._output_spec[index]['voltage_max']):
            raise ivi.OutOfRangeException()

        self._write(':ADR{0};'.format(index))
        self._write(':VOL{0};'.format(value))

    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)

        self._write(':ADR{0};'.format(index))
        value = self._ask(':VOL!;')
        return float(value[2:])

    def _get_output_current_limit(self, index):
        self._write(':ADR{0};'.format(index))
        value = self._ask(':CUR!;')
        return float(value[2:])

    def _set_output_current_limit():
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()

        self._write(':ADR{0};'.format(index))
        self._write(':CUR{0};'.format(value))

    def _get_output_current_limit_behavior(self, index):
        index = ivi.get_index(self._output_name, index)
        return self._output_current_limit_behavior[index]

    def _set_output_current_limit_behavior():
        index = ivi.get_index(self._output_name, index)
        if value not in CurrentLimitBehavior:
            raise ivi.ValueNotSupportedException()
        self._output_current_limit_behavior[index] = value

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)

        self._write(':ADR{0};'.format(index))
        value = self._ask(':OUT?;')
        return int(value[2:]) == 1

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)

        self._write(':ADR{0};'.format(index))
        self._write(':OUT{0};'.format(1 if value else 0))

    def _get_output_ovp_enabled():
        pass

    def _set_output_ovp_enabled():
        pass

    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)

        self._write(':ADR{0};'.format(index))
        value = self._ask(':OVP?;')
        return float(value[2:])

    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()

        self._write(':ADR{0};'.format(index))
        self._write(':OVP{0};'.format(value))


def _main():
    psu = ZUP36('ASRL::COM1,9600::INSTR')
    psu._set_driver_operation_simulate(True)  # 테스트 용도로만
    psu.outputs[0].voltage_level = 2
    print psu.outputs[0].voltage_level

if __name__ == '__main__':
    _main()
