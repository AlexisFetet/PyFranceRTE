#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains all functions dedicated to the big substations api
"""

import requests

from py_france_rte.base_application import BaseApplication
from py_france_rte.utils import (BASE_OPEN_API_URL, generate_header,
                                 verify_response_code)

ECOWATT_URL = BASE_OPEN_API_URL + "ecowatt/v4/signals"


def request_ecowatt_signals(self: BaseApplication) -> "dict":
    """
    Application function overwrite to request signals from Ecowatt
    """

    self.verify_token()
    header_ = generate_header(self.oauth_token)

    signal_response = requests.get(
        ECOWATT_URL,
        headers=header_,
        timeout=self.timeout)

    verify_response_code(signal_response.status_code, "Ecowatt")

    return signal_response.json()
