#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['KATE3_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['KATE3_MONGOALCHEMY_SERVER'] = ''
    os.environ['KATE3_MONGOALCHEMY_PORT'] = ''
    os.environ['KATE3_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.kate3 import kate3
    from qube.src.services.kate3service import kate3Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, kate3ServiceError


class Testkate3Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.kate3Service = kate3Service(context)
        self.kate3_api_model = self.createTestModelData()
        self.kate3_data = self.setupDatabaseRecords(self.kate3_api_model)
        self.kate3_someoneelses = \
            self.setupDatabaseRecords(self.kate3_api_model)
        self.kate3_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.kate3_someoneelses.save()
        self.kate3_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.kate3_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.kate3_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, kate3_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            kate3_data = kate3(name='test_record')
            for key in kate3_api_model:
                kate3_data.__setattr__(key, kate3_api_model[key])

            kate3_data.description = 'my short description'
            kate3_data.tenantId = "23432523452345"
            kate3_data.orgId = "987656789765670"
            kate3_data.createdBy = "1009009009988"
            kate3_data.modifiedBy = "1009009009988"
            kate3_data.createDate = str(int(time.time()))
            kate3_data.modifiedDate = str(int(time.time()))
            kate3_data.save()
            return kate3_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_kate3(self, *args, **kwargs):
        result = self.kate3Service.save(self.kate3_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.kate3_api_model['name'])
        kate3.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kate3(self, *args, **kwargs):
        self.kate3_api_model['name'] = 'modified for put'
        id_to_find = str(self.kate3_data.mongo_id)
        result = self.kate3Service.update(
            self.kate3_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.kate3_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_kate3_description(self, *args, **kwargs):
        self.kate3_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.kate3_data.mongo_id)
        result = self.kate3Service.update(
            self.kate3_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.kate3_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate3_item(self, *args, **kwargs):
        id_to_find = str(self.kate3_data.mongo_id)
        result = self.kate3Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate3_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(kate3ServiceError):
            self.kate3Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_kate3_list(self, *args, **kwargs):
        result_collection = self.kate3Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.kate3_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kate3_data.mongo_id)
        with self.assertRaises(kate3ServiceError) as ex:
            self.kate3Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.kate3_data.mongo_id)
        self.kate3Service.auth_context.is_system_user = True
        self.kate3Service.delete(id_to_delete)
        with self.assertRaises(kate3ServiceError) as ex:
            self.kate3Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.kate3Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.kate3_someoneelses.mongo_id)
        with self.assertRaises(kate3ServiceError):
            self.kate3Service.delete(id_to_delete)
