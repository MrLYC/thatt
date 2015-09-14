#!/usr/bin/env python
# encoding: utf-8

import logging
import json
from textwrap import dedent

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

import requests

logger = logging.getLogger(__name__)


class ThattProxyServer(LineReceiver):
    ResponseTemplate = dedent("""
        HTTP/1.1 {status} {reason}
        {headers}

        {content}
    """)
    ResponseExcludedHeaders = {
        'connection', 'keep-alive', 'proxy-authenticate',
        'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
        'content-encoding', 'content-length',
    }

    def connectionMade(self):
        logger.info("connection from: %s", self.transport.hostname)

    def connectionLost(self, reason):
        logger.info("connection lost: %s, %s", self.transport.hostname, reason)

    def lineReceived(self, data):
        try:
            json_data = json.loads(data)
        except ValueError as err:
            self.transport.abortConnection()
            return
        logger.debug(json_data)

        response = requests.get(
            json_data["url"],
            headers=json_data.get("headers", {}),
            timeout=json_data.get("timeout", 30),
        )

        self.transport.write(self.ResponseTemplate.format(
            status=response.status_code, reason=response.reason,
            headers="\r\n".join(
                "%s: %s" % (k.title(), v)
                for k, v in response.headers.items()
                if k not in self.ResponseExcludedHeaders
            ),
            content=response.content
        ))


class ThattProxyFactory(Factory):
    def buildProtocol(self, addr):
        return ThattProxyServer()
