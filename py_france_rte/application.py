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
    Application(
            id_client: str,
            id_secret: str,
            subscribed_apis: "list[str]",
            timeout: Optional[int] = 10) -> Application:

    This is the class representing an application to communicate with RTE APIs.
    You need to create the applications on data.rte-france.com first in order to
    get access to the API. Your application identifiers can be found on
    data.rte-france.fr

    Parameters
    ----------
    id_client : str
        The application client ID
    id_secret : str
        The application secret ID
    subscribed_apis : list[str]
        The list of all APIs the application is subscribed to and can use
    timeout : int, default: 10
        The timeout value for http requests, defaults to 10s

    Returns
    -------
    Application
        An application instance

    Raises
    ------
    RuntimeError
        If an error occurs at run time, like methods parameters not
        following the APIs specifications
    ValueError
        If a provided parameter is of unexpected type
    ComError
        If an error occurs when requesting data from an API,
        may happen if you reached your quota
    NoAccessError
        If the application tries to access an API it
        was not declared to be registered to
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
        register_apis(self, subscribed_apis: "list[str]") -> None

        Overwrite all application instance methods for provided supported APIs

        Parameters
        ----------
        subscribed_apis : list[str]
            List of all APIs the application can use, require prior subscription on
            data.rte-france.com

        Raises
        ------
        RuntimeError
            If a provided API is not supported
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
