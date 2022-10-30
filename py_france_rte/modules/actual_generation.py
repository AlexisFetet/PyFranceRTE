#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains all functions dedicated to the actual generation api
"""

from typing import Optional

import requests

from py_france_rte.base_application import BaseApplication
from py_france_rte.utils import (BASE_OPEN_API_URL, generate_header,
                                 is_str_instance, prepare_date_request,
                                 prepare_url_with_options, verify_dates,
                                 verify_response_code)

ACTUAL_GENERATION_PER_TYPE_URL = BASE_OPEN_API_URL + \
    "actual_generation/v1/actual_generations_per_production_type"
ACTUAL_GENERATION_PER_UNIT_URL = BASE_OPEN_API_URL + \
    "actual_generation/v1/actual_generations_per_unit"
WATER_RESERVES_URL = BASE_OPEN_API_URL + \
    "actual_generation/v1/water_reserves"
GENRATION_MIX_15MIN_URL = BASE_OPEN_API_URL + \
    "actual_generation/v1/generation_mix_15min_time_scale"
PRODUCTION_TYPES = [
    "FOSSIL_OIL",
    "FOSSIL_GAS",
    "HYDRO",
    "BIOENERGY",
    "NUCLEAR",
    "FOSSIL_HARD_COAL",
    "WIND",
    "EXCHANGE",
    "PUMPING",
    "SOLAR",
]
PRODUCTION_SUBTYPES = {
    "FOSSIL_OIL": [
        "FOSSIL_OIL_OTHER",
        "FOSSIL_OIL_CHP",
        "FOSSIL_OIL_CT",
    ],
    "FOSSIL_GAS": [
        "FOSSIL_GAS_OTHER",
        "FOSSIL_GAS_CCGT",
        "FOSSIL_GAS_CHP",
        "FOSSIL_GAS_CT"
    ],
    "HYDRO": [
        "HYDRO_PUMPED_STORAGE",
        "HYDRO_WATER_RESERVOIR",
        "HYDRO_RUN_OF_RIVER_AND_POUNDAGE"
    ],
    "BIOENERGY": [
        "BIOGAS",
        "BIOMASS",
        "WASTE"
    ]
}


def request_actual_generation_per_type(
        self: BaseApplication,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None) -> "dict":
    """
    Application function overwrite to request actual generation per type
    """

    verify_dates(start_date, end_date, 155, 1, "2014-12-15")

    self.verify_token()
    header_ = generate_header(self.oauth_token)

    options_ = []

    if start_date:
        options_.append(prepare_date_request(start_date, end_date))

    url_ = prepare_url_with_options(ACTUAL_GENERATION_PER_TYPE_URL, options_)

    signal_response = requests.get(
        url=url_,
        headers=header_,
        timeout=self.timeout)

    verify_response_code(
        code=signal_response.status_code,
        api="actual_generation")

    return signal_response.json()


def request_actual_generation_per_unit(
        self: BaseApplication,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        unit_eic_code: Optional[str] = None) -> "dict":
    """
    Application function overwrite to request actual generation per unit
    """

    verify_dates(start_date, end_date, 7, 1, "2011-12-13")

    self.verify_token()
    header_ = generate_header(self.oauth_token)

    options_ = []

    if start_date:
        options_.append(prepare_date_request(start_date, end_date))
    if unit_eic_code:
        options_.append(f"unit_eic_code={unit_eic_code}")

    url_ = prepare_url_with_options(ACTUAL_GENERATION_PER_UNIT_URL, options_)

    signal_response = requests.get(
        url=url_,
        headers=header_,
        timeout=self.timeout)

    verify_response_code(
        code=signal_response.status_code,
        api="actual_generation")

    return signal_response.json()


def request_water_reserves(
        self: BaseApplication,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None) -> "dict":
    """
    Application function overwrite to request water reserves
    """

    verify_dates(start_date, end_date, 366, 1, "2014-12-08")

    self.verify_token()
    header_ = generate_header(self.oauth_token)

    options_ = []

    if start_date:
        options_.append(prepare_date_request(start_date, end_date))

    url_ = prepare_url_with_options(WATER_RESERVES_URL, options_)
    print(url_)

    signal_response = requests.get(
        url=url_,
        headers=header_,
        timeout=self.timeout)

    print(signal_response.json())

    verify_response_code(
        code=signal_response.status_code,
        api="actual_generation")

    return signal_response.json()


def request_generation_mix_15min_time_scale(
        self: BaseApplication,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        production_type: Optional[str] = None,
        production_subtype: Optional[str] = None) -> "dict":
    """
    Application function overwrite to request actual generation mix with 15min scale
    """

    verify_dates(start_date, end_date, 14, 1, "2017-01-01")
    self.verify_token()
    header_ = generate_header(self.oauth_token)

    options_ = []

    if start_date:
        options_.append(prepare_date_request(start_date, end_date))
    if production_type or production_subtype:
        options_ += prepare_type_request(
            production_type,
            production_subtype)

    url_ = prepare_url_with_options(GENRATION_MIX_15MIN_URL, options_)

    signal_response = requests.get(
        url=url_,
        headers=header_,
        timeout=self.timeout)

    verify_response_code(
        code=signal_response.status_code,
        api="actual_generation")

    return signal_response.json()


def prepare_type_request(
        production_type: Optional[str] = None,
        production_subtype: Optional[str] = None) -> "list[str]":
    """
    Prepare options for type requests
    """

    options_ = []

    if production_type:
        is_str_instance(production_type, "production_type")
        if production_type not in PRODUCTION_TYPES:
            raise ValueError(
                f"You provided unknown type production {production_type} "
                f"to API Actual Generation")
        options_.append(f"production_type={production_type}")

    if production_subtype:
        is_str_instance(production_subtype, "production_subtype")
        if production_type:
            # Verifying subtype is ok with given type
            if production_subtype not in PRODUCTION_SUBTYPES[production_type]:
                raise ValueError(
                    f"You provided invalid subtype production {production_subtype} "
                    f"with type {production_type} "
                    f"to API Actual Generation")
            options_.append(f"production_subtype={production_subtype}")
        else:
            # Trying to detect production type
            known_subtype_ = False
            for (type_, subtype_list_) in PRODUCTION_SUBTYPES.items():
                if production_subtype in subtype_list_:
                    known_subtype_ = True
                    production_type = type_
                    break
            if not known_subtype_:
                raise ValueError(
                    f"You provided unknown subtype production {production_subtype} "
                    f"to API Actual Generation")
            options_.append(f"production_type={production_type}")
            options_.append(f"production_subtype={production_subtype}")

    return options_
