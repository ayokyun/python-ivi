# -*- coding: utf8 -*-

from ..scpi.dcpwr import Base


class Z36(Base):
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')

        # early define of _do_scpi_init
        self.__dict__.setdefault('_do_scpi_init', True)

        super(Base, self).__init__(*args, **kwargs)

        self._self_test_delay = 5

        self._output_count = 4
        self._driver_operation_cache = False

        self._output_spec = [
            {
                'range': {
                    'P36V': (36.0, 12.0),
                    'P36V': (36.0, 12.0)
                },
                'ovp_max': 36.0,
                'voltage_max': 36.0,
                'current_max': 12.0
            },
            {
                'range': {
                    'P36V': (36.0, 12.0),
                    'P36V': (36.0, 12.0)
                },
                'ovp_max': 36.0,
                'voltage_max': 36.0,
                'current_max': 12.0
            },
            {
                'range': {
                    'P36V': (36.0, 12.0),
                    'P36V': (36.0, 12.0)
                },
                'ovp_max': 36.0,
                'voltage_max': 36.0,
                'current_max': 12.0
            },
            {
                'range': {
                    'P36V': (36.0, 12.0),
                    'P36V': (36.0, 12.0)
                },
                'ovp_max': 36.0,
                'voltage_max': 36.0,
                'current_max': 12.0
            }
        ]

        self._identity_description = "TDK-Lambda Z+ Series DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = ""
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PSU']

        self._init_outputs()

        if self._interface: 
            self._interface.term_char = '\n'

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        """Opens an I/O session to the instrument."""

        super(Base, self)._initialize(resource, id_query, reset, **keywargs)

        if not self._do_scpi_init:
            return

        # interface clear - Z+ does not support interface clear
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()
