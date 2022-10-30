#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: disable=R0903

"""
This file contains all utilities for the pyFranceRTE package.
"""

import base64

from py_france_rte.utils import is_str_instance


class Key():

    """
    This class is your application key for the API.
    """

    def __init__(self, id_client: str, id_secret: str) -> None:

        is_str_instance(id_client, "id_client")
        is_str_instance(id_secret, "id_secret")

        self.id_client = id_client
        self.id_secret = id_secret
        key_b64_ = base64.b64encode(f"{id_client}:{id_secret}".encode("utf-8"))
        self.key_b64 = str(key_b64_)[1:].replace('\'', "")

    def __repr__(self) -> str:
        return self.key_b64
