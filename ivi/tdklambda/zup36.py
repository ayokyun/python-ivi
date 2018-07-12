# -*- coding: utf8 -*-

from .. import dcpwr
from .. import ivi

CurrentLimitBehavior = set(['regulate', 'trip'])


class ZUP36(ivi.Driver, dcpwr.Base, dcpwr.Measurement):

    def __init__(self, *args, **kwargs):
        super(ZUP36, self).__init__(*args, **kwargs)

        self._output_count = 32

        self._output_spec = [
                                {
                                    'range': {
                                        'P36V': (36.0, 6.0),
                                        'P36V': (36.0, 6.0)
                                    },
                                    'ovp_max': 36.0,
                                    'voltage_max': 36.0,
                                    'current_max': 6.0
                                }
                            ] * self._output_count

        self._init_outputs()

    def _select_address(self, index):
        self._write(':ADR%02d;' % (index + 1), encoding='ascii')

    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if (value < 0) or (value > self._output_spec[index]['voltage_max']):
            raise ivi.OutOfRangeException()

        self._select_address(index)
        self._write(':VOL%05.2f;' % (value), encoding='ascii')

    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)

        self._select_address(index)
        value = self._ask(':VOL!;', encoding='ascii')

        return float(value[2:])

    def _get_output_current_limit(self, index):
        self._select_address(index)

        value = self._ask(':CUR!;', encoding='ascii')
        return float(value[2:])

    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()

        self._select_address(index)
        self._write(':CUR{0};'.format(value), encoding='ascii')

    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)

        self._select_address(index)
        value = self._ask(':OUT?;', encoding='ascii')
        return int(value[2:]) == 1

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)

        self._select_address(index)
        self._write(':OUT{0};'.format(1 if value else 0), encoding='ascii')

    def _get_output_ovp_limit(self, index):
        index = ivi.get_index(self._output_name, index)

        self._select_address(index)
        value = self._ask(':OVP?;', encoding='ascii')
        return float(value[2:])

    def _set_output_ovp_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['ovp_max']:
            raise ivi.OutOfRangeException()

        self._select_address(index)
        self._write(':OVP{0};'.format(value), encoding='ascii')
