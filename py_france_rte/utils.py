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
    generate_header(token: str) -> "dict[str:str]"

    Generates a request header with the provided token.

    Parameters
    ----------
    token : str
        A token provided to the application by the oauth authentication service

    Returns
    -------
    dict[str:str]
        A header to use to request data from an authorized API
    """
    return {
        "Host": "digital.iservices.rte-france.com",
        "Authorization": f"Bearer {token}"}


def verify_response_code(code: int, api: str) -> None:
    """
    verify_response_code(code: int, api: str) -> None:

    Review response code from service response.

    Parameters
    ----------
    code : int
        The response status code to review
    api : str
        The API requesting the review

    Raises
    ------
    ComError
        If the status code corresponds to an error
    """
    if code != 200:
        error_ = _ERROR_LOOKUP.get(
            code,
            "Unable to perform request with %s, code %i") % (api,
                                                             code)
        raise ComError(error_)


def is_str_instance(variable: Any, name: str) -> None:
    """
    is_str_instance(variable: Any, name: str) -> None:

    Verifies if the provided variable is of type str.

    Parameters
    ----------
    variable : Any
        The provided variable to review
    name : str
        The name of the variable

    Raises
    ------
    TypeError
        If the variable is not a str
    """
    if not isinstance(variable, str):
        raise TypeError(
            f"Invalid data type for {name}, "
            f"must be str and is {type(variable)}.")


def is_int_instance(variable: Any, name: str) -> None:
    """
    is_int_instance(variable: Any, name: str) -> None:

    Verifies if the provided variable is of type int.

    Parameters
    ----------
    variable : Any
        The provided variable to review
    name : str
        The name of the variable

    Raises
    ------
    TypeError
        If the variable is not an int
    """
    if not isinstance(variable, int):
        raise TypeError(
            f"Invalid data type for {name}, "
            f"must be int and is {type(variable)}.")


def verify_dates(
        start_date: Any,
        end_date: Any,
        max_days: int,
        min_days: int,
        min_date: str) -> None:
    """
    verify_dates(start_date: Any,
        end_date: Any,
        max_days: int,
        min_days: int,
        min_date: str) -> None:

    Verifies if the provided dates have the correct format.
    Verifies if the duration between the given dates is within given interval.
    Verifies if start_date is after min_date.

    Parameters
    ----------
    start_date : Any
        The start date of the request, must be a str
        at format "YYYY-MM-DDThh:mm:sszzzzzz"
        exemple : "2015-06-08T00:00:00+02:00"
    end_date : Any
        The end date of the request, must be a str
        at format "YYYY-MM-DDThh:mm:sszzzzzz"
        exemple : "2015-06-08T00:00:00+02:00"
    max_days : int
        The maximum duration between start_date and end_date, in day(s)
    min_days : int
        The minimum duration between start_date and end_date, in day(s)
    min_date : str
        The minimum date for start_date, must be of format "YYYY-MM-DD"

    Raises
    ------
    ValueError
        If a parameter is not of expected type,
        or dates are invalid given the parameters
    RuntimeError
        If only start_date or end_date was provided
    """
    if start_date:
        is_str_instance(start_date, "start_date")
        try:
            datetime.datetime.strptime(start_date, DATE_FORMAT)
        except ValueError as err:
            raise ValueError(
                f"Invalid date format for start_date, requires {DATE_FORMAT}"
            ) from err

    if end_date:
        is_str_instance(end_date, "end_date")
        try:
            datetime.datetime.strptime(end_date, DATE_FORMAT)
        except ValueError as err:
            raise ValueError(
                f"Invalid date format for end_date, requires {DATE_FORMAT}"
            ) from err

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
                f"start_date ({start_date}) is earlier "
                f"than min_date {min_date}")
        if end_ > now_:
            raise ValueError(
                f"end_date ({end_date})is later "
                f"than current supported time {now_}")
        if start_ > end_:
            raise ValueError(
                f"start_date ({start_date}) is later than end_date {end_date}")

        duration_ = end_ - start_

        if duration_.days > max_days:
            raise ValueError(
                f"Duration between start_date ({start_date}) and "
                f"end_date ({end_date}) exceeds max_days ({max_days} days)")

        if duration_.days < min_days:
            raise ValueError(
                f"Duration between start_date ({start_date}) and "
                f"end_date ({end_date}) "
                f"is less than min_days ({min_days} days)")


def prepare_date_request(start_date: str, end_date: str) -> str:
    """
    prepare_date_request(start_date: str, end_date: str) -> str

    Generates request url substring related to dated requests

    Parameters
    ----------
    start_date : str
        The start date of the request,
        must be at format "YYYY-MM-DDThh:mm:sszzzzzz"
        exemple : "2015-06-08T00:00:00+02:00"
    end_date : str
        The end date of the request,
        must be at format "YYYY-MM-DDThh:mm:sszzzzzz"
        exemple : "2015-06-08T00:00:00+02:00"

    Returns
    -------
    str
        A url request substring related to dated requests
    """
    return f"start_date={start_date}&end_date={end_date}".replace("+", "%2B")


def prepare_url_with_options(base_url: str, options: "list[str]") -> str:
    """
    prepare_url_with_options(base_url: str, options: "list[str]") -> str

    Generates request url with provided options if any

    Parameters
    ----------
    base_url : str
        The base url of the request
    options : list[str]
        List of string options to add to the url

    Returns
    -------
    base_url_ : str
        The base url completed with provided options if any
    """
    base_url_ = base_url
    if len(options) != 0:
        base_url_ += "?"
        base_url_ += "&".join(options)
    return base_url_
