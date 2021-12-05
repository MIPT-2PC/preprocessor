# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.table import Table  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInteractionController(BaseTestCase):
    """InteractionController integration test stubs"""

    def test_get_table(self):
        """Test case for get_table

        hello message to get preprocessed data
        """
        response = self.client.open(
            '/MIPT-2PC/preprocessor/1.0.0/getTable',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start2_pc(self):
        """Test case for start2_pc

        start preprocessing procedure
        """
        body = Table()
        response = self.client.open(
            '/MIPT-2PC/preprocessor/1.0.0/start2PC',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
