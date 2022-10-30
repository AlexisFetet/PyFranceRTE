#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This file contains all py_france_rte related errors
"""


class NoAccessError(Exception):
    """
    Error to specify to the user that the application is
    not declared as having access to a specific API
    """


class ComError(Exception):
    """
    Basic communication error
    """


_ERROR_LOOKUP = {
    400: "Request error using %s, code %i",
    401: "Unauthorized application using %s, code %i",
    403: "Forbidden request for %s, code %i",
    404: "%s not found, code %i",
    407: "Request blocked using %s, code %i",
    408: "Request timed out using %s, code %i",
    413: "Response too large using %s, code %i",
    414: "Request url too long using %s, code %i",
    429: "Quota exceeded for %s, code %i",
    500: "Internal server error using %s, code %i",
    503: "Service %s unavailable, code %i",
    509: "BAndwidth limit exceeded using %s, code %i"
}
