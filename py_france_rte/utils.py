#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains all utilities for the pyFranceRTE package.
"""
import datetime
from typing import Any

from py_france_rte.errors import _ERROR_LOOKUP, ComError

OAUTH_TOKEN_REQ_URL = "https://digital.iservices.rte-france.com/token/oauth/"
BASE_PRIVATE_API_URL = "https://digital.iservices.rte-france.com/private_api/"
BASE_OPEN_API_URL = "https://digital.iservices.rte-france.com/open_api/"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

SUPPORTED_APIS = [
    "Ecowatt",
    "Actual Generation"
]


def generate_header(token: str) -> "dict[str:str]":
    """
    generate a header using a given token
    """
    return {
        "Host": "digital.iservices.rte-france.com",
        "Authorization": f"Bearer {token}"}


def verify_response_code(code: int, api: str) -> None:
    """
    Raise a ComError if response code is not 200, with an error explanation
    """
    if code != 200:
        error_ = _ERROR_LOOKUP.get(
            code,
            "Unable to perform request with %s, code %i") % (api,
                                                             code)
        raise ComError(error_)


def is_str_instance(variable: Any, name: str) -> None:
    """
    Raise TypeError if variable is not a string
    """
    if not isinstance(variable, str):
        raise TypeError(
            f"Invalid data type for {name}, must be str and is {type(variable)}.")


def is_int_instance(variable: Any, name: str) -> None:
    """
    Raise TypeError if variable is not an integer
    """
    if not isinstance(variable, int):
        raise TypeError(
            f"Invalid data type for {name}, must be int and is {type(variable)}.")


def verify_dates(
        start_date: Any,
        end_date: Any,
        max_days: int,
        min_days: int,
        min_date: str) -> None:
    """
    Verify dates formating if provided
    Verify that if a date is provided, the secod is as well
    Verify that duration between dates does not exceed max_days,
    Verify that duration between dates is at least min_days
    """

    if start_date:
        is_str_instance(start_date, "start_date")
        try:
            datetime.datetime.strptime(start_date, DATE_FORMAT)
        except ValueError as err:
            raise ValueError(
                f"Invalid date format for start_date, requires {DATE_FORMAT}") from err

    if end_date:
        is_str_instance(end_date, "end_date")
        try:
            datetime.datetime.strptime(end_date, DATE_FORMAT)
        except ValueError as err:
            raise ValueError(
                f"Invalid date format for end_date, requires {DATE_FORMAT}") from err

    if start_date and not end_date or end_date and not start_date:
        raise RuntimeError(
            "You provided only a start date or only an end date")

    if start_date:
        is_int_instance(max_days, "max_days")
        is_int_instance(min_days, "min_days")
        is_str_instance(min_date, "min_date")

        start_ = datetime.datetime.fromisoformat(start_date)
        end_ = datetime.datetime.fromisoformat(end_date)
        min_date_ = datetime.datetime.fromisoformat(
            min_date + "T00:00:00+00:00")
        now_ = datetime.datetime.now(
            end_.tzinfo).replace(
            minute=0,
            second=0,
            microsecond=0)

        if start_ < min_date_:
            raise ValueError(
                f"start_date ({start_date}) is earlier than min_date {min_date}")
        if end_ > now_:
            raise ValueError(
                f"end_date ({end_date})is later than current supported time {now_}")
        if start_ > end_:
            raise ValueError(
                f"start_date ({start_date}) is later than end_date {end_date}")

        duration_ = end_ - start_

        if duration_.days > max_days:
            raise ValueError(
                f"Duration between start_date ({start_date}) and"
                f"end_date ({end_date}) exceeds max_days ({max_days} days)")

        if duration_.days < min_days:
            raise ValueError(
                f"Duration between start_date ({start_date}) and "
                f"end_date ({end_date}) is less than min_days ({min_days} days)")


def prepare_date_request(start_date: str, end_date: str) -> str:
    """
    Return the string to request data between two dates
    """
    return f"start_date={start_date}&end_date={end_date}".replace("+", "%2B")


def prepare_url_with_options(base_url: str, options: "list[str]") -> str:
    """
    Apply options to url
    """
    if len(options) != 0:
        base_url += "?"
        base_url += "&".join(options)
    return base_url
