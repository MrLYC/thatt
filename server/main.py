#!/usr/bin/env python
# encoding: utf-8

import logging

from twisted.internet import reactor, endpoints

from ycyc.base.adapter import main_entry

from server import settings
from server.handlers import ThattProxyFactory


@main_entry
def main():
    logger = logging.getLogger(__name__)

    logger.info("[+] server is ready")
    endpoints.serverFromString(reactor, "tcp:9274").listen(ThattProxyFactory())
    reactor.run()  # pylint: disable=no-member
