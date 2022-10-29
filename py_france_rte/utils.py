#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains all utilities for the pyFranceRTE package.
"""

import base64

import requests

OAUTH_TOKEN_REQ_URL = "https://digital.iservices.rte-france.com/token/oauth/"


class Key():

    """
    This Class is your application key for the API.
    """

    def __init__(self, id_client: str, id_secret: str) -> None:

        if not isinstance(id_client, str):
            raise TypeError(
                f"Invalid data type for id_client, must be str and is {type(id_client)}.")
        if not isinstance(id_secret, str):
            raise TypeError(
                f"Invalid data type for id_secret, must be str and is {type(id_secret)}.")

        self.id_client = id_client
        self.id_secret = id_secret
        key_b64 = base64.b64encode(f"{id_client}:{id_secret}".encode("utf-8"))
        self.key_b64 = str(key_b64)[1:].replace('\'', "")


def request_oauth_token(key: Key) -> "tuple[str, int]":
    """
    Request an oauth token for a given application
    """

    token_request = requests.post(
        OAUTH_TOKEN_REQ_URL,
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {key.key_b64}"})

    if not token_request.status_code == 200:
        raise RuntimeError("Unable to request oauth token")

    token_request_content = token_request.json()

    return (token_request_content["access_token"],
            token_request_content["expires_in"])
