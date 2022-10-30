#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains the BaseApplication class, to be overloaded with Application
"""


from time import time
from typing import Optional

import requests

from py_france_rte.errors import NoAccessError
from py_france_rte.key import Key
from py_france_rte.utils import (OAUTH_TOKEN_REQ_URL, is_int_instance,
                                 is_str_instance)


def request_oauth_token(key: Key, timeout: int = 10) -> "tuple[str, int]":
    """
    Request an oauth_token for a given application
    """

    token_request = requests.post(
        OAUTH_TOKEN_REQ_URL,
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {key.key_b64}"},
        timeout=timeout)

    if token_request.status_code != 200:
        raise RuntimeError("Unable to request oauth token")

    token_request_content = token_request.json()

    return (token_request_content["access_token"],
            token_request_content["expires_in"])


class BaseApplication():
    """
    This is an application instance, to be overloaded by Application
    """

    def __init__(self, id_client: str, id_secret: str,
                 timeout: Optional[int] = 10) -> None:

        is_str_instance(id_client, "id_client")
        is_str_instance(id_secret, "id_secret")
        is_int_instance(timeout, "timeout")

        self.key = Key(id_client, id_secret)
        self.oauth_token = "None"
        self.oauth_token_expire = 0.
        self.timeout = timeout
        self.generate_oauth_token()

    def generate_oauth_token(self) -> None:
        """
        generate an oauth token for the application
        """

        (oauth_token, validity_duration_) = request_oauth_token(
            self.key, timeout=self.timeout)

        self.oauth_token = oauth_token
        self.oauth_token_expire = time() + validity_duration_

    def verify_token(self) -> None:
        """
        Verify oauth_token time validity, generates new oauth_token if needed
        """

        if time() > self.oauth_token_expire:
            self.generate_oauth_token()

    # Declare all API funstions to be overloaded if access is declared

    # Ecowatt

    def request_ecowatt_signals(self,) -> "dict":
        """
        function to be overwritten
        """
        raise NoAccessError("No access declared to Ecowatt API")

    # Actual Generation

    def request_actual_generation_per_type(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None) -> "dict":
        """
        function to be overwritten
        """
        raise NoAccessError("No access declared to Actual Generation API")

    def request_actual_generation_per_unit(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            unit_eic_code: Optional[str] = None) -> "dict":
        """
        function to be overwritten
        """
        raise NoAccessError("No access declared to Actual Generation API")

    def request_water_reserves(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None) -> "dict":
        """
        function to be overwritten
        """
        raise NoAccessError("No access declared to Actual Generation API")

    def request_generation_mix_15min_time_scale(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            production_type: Optional[str] = None,
            production_subtype: Optional[str] = None) -> "dict":
        """
        function to be overwritten
        """
        raise NoAccessError("No access declared to Actual Generation")
