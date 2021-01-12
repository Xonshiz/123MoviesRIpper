#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cust_utils
import json

BASE_URL = 'https://discover.hulu.com/content/v3/entity'


def get_xml_http_request(movie_url):
    response = cust_utils.browser_instance.get_request(url=movie_url, xml_http_request=True)
    return response


def get_http_request(movie_url, text_only=False):
    response = cust_utils.browser_instance.get_request(url=movie_url, text_only=text_only)
    return response
