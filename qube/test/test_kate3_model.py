#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testkate3Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_kate3_model(self):
        from qube.src.models.kate3 import kate3
        kate3_data = kate3(name='testname')
        kate3_data.tenantId = "23432523452345"
        kate3_data.orgId = "987656789765670"
        kate3_data.createdBy = "1009009009988"
        kate3_data.modifiedBy = "1009009009988"
        kate3_data.createDate = str(int(time.time()))
        kate3_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kate3_data.save()
            self.assertIsNotNone(kate3_data.mongo_id)
            kate3_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
