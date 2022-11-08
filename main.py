#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: disable=E1102

"""
This file is an exemple on how to use the Application class
"""

if __name__ == "__main__":
    import os

    import dotenv

    from py_france_rte.application import Application

    dotenv.load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    secret_id = os.getenv("SECRET_ID")

    APIS = [
        "Ecowatt",
        "Actual Generation"
    ]

    test = Application(client_id, secret_id, APIS)

    START_DATE = "2017-06-05T00:00:00+02:00"
    END_DATE = "2017-06-12T00:00:00+02:00"
    PRODUCTION_TYPE = "HYDRO"
    PRODUCTION_SUBTYPE = "HYDRO_PUMPED_STORAGE"

    # test ecowatt
    test.request_ecowatt_signals()

    # test actual generation
    test.request_actual_generation_per_type(START_DATE, END_DATE)
    test.request_actual_generation_per_unit(
        START_DATE, END_DATE, PRODUCTION_SUBTYPE)
    test.request_water_reserves(START_DATE, END_DATE)
    test.request_generation_mix_15min(START_DATE, END_DATE)
