#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: disable-all

"""
This file contains the tests for py_france_rte.utils
"""

import pytest

from py_france_rte.utils import (generate_header, is_int_instance,
                                 is_str_instance)


def test_is_str_instance():
    with pytest.raises(TypeError):
        is_int_instance("int", "mon_int")
    assert not is_int_instance(0, "my_int")


def test_is_int_instance():
    with pytest.raises(TypeError):
        is_str_instance(0, "my_int")
    assert not is_str_instance("str", "my_int")


def test_generate_header():
    with pytest.raises(TypeError):
        generate_header(75467412)
    assert generate_header("My_super_token") == {
        "Host": "digital.iservices.rte-france.com",
        "Authorization": "Bearer My_super_token"}
