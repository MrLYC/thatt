#!/usr/bin/env python
# encoding: utf-8

import os

DEBUG = bool(os.environ.get("THATTDEBUG", False))

if DEBUG:
    from ycyc.shortcuts import logger_quick_config
    logger_quick_config()
