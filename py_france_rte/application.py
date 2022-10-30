#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: disable=C0415

"""
This file contains the Application class, to use when interracting with the France RTE APIs
"""

import types
from typing import Optional

from py_france_rte.base_application import BaseApplication
from py_france_rte.utils import SUPPORTED_APIS


class Application(BaseApplication):

    """
    An application class to interract with the France RTE APIs
    """

    def __init__(
            self,
            id_client: str,
            id_secret: str,
            subscribed_apis: "list[str]",
            timeout: Optional[int] = 10) -> None:
        super().__init__(id_client, id_secret, timeout)

        self.register_apis(subscribed_apis)

    def register_apis(self, subscribed_apis: "list[str]") -> None:
        """
        Register access to APIs
        """

        for api_ in subscribed_apis:
            if api_ not in SUPPORTED_APIS:
                raise RuntimeError(f"Unsupported API declared : {api_}")
            # Load API functions
            # Ecowatt
            if api_ == "Ecowatt":
                from py_france_rte.modules.ecowatt import \
                    request_ecowatt_signals
                self.request_ecowatt_signals = types.MethodType(
                    request_ecowatt_signals, self)
            # Actual Generation
            elif api_ == "Actual Generation":
                from py_france_rte.modules.actual_generation import (
                    request_actual_generation_per_type,
                    request_actual_generation_per_unit,
                    request_generation_mix_15min_time_scale,
                    request_water_reserves)
                self.request_actual_generation_per_unit = types.MethodType(
                    request_actual_generation_per_unit, self)
                self.request_actual_generation_per_type = types.MethodType(
                    request_actual_generation_per_type, self)
                self.request_generation_mix_15min_time_scale = types.MethodType(
                    request_generation_mix_15min_time_scale, self)
                self.request_water_reserves = types.MethodType(
                    request_water_reserves, self)
