#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: disable-all

"""
@TODO more tests
This file contains the tests for py_france_rte.utils
"""

import pytest

from py_france_rte.utils import is_int_instance, is_str_instance


def test_is_str_instance():
    with pytest.raises(TypeError):
        is_int_instance("int", "mon_int")


def test_is_int_instance():
    with pytest.raises(TypeError):
        is_str_instance(0, "my_int")
