# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.clusters.datastores.
#---------------------------------------------------------------------------

"""


"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from vmware.vapi.bindings import type
from vmware.vapi.bindings.converter import TypeConverter
from vmware.vapi.bindings.enum import Enum
from vmware.vapi.bindings.error import VapiError, ThrowsClauseBuilder
from vmware.vapi.bindings.struct import VapiStruct
from vmware.vapi.bindings.stub import (
    ApiInterfaceStub, StubFactoryBase, VapiInterface)
from vmware.vapi.bindings.common import raise_core_exception
from vmware.vapi.data.validator import (UnionValidator, HasFieldsOfValidator)
from vmware.vapi.exception import CoreException
from vmware.vapi.lib.constants import TaskType
from vmware.vapi.lib.rest import OperationRestMetadata


class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.datastores.queries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _QueriesStub)
        self._VAPI_OPERATION_IDS = {}


    def post_datastore_query1(self,
                              id,
                              datastore_criterion,
                              ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  datastore_criterion: :class:`vmware.sddc_manager.model_client.DatastoreCriterion`
        :param datastore_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('post_datastore_query1',
                            {
                            'id': id,
                            'datastore_criterion': datastore_criterion,
                            })

    def get_datastore_query_response1(self,
                                      cluster_id,
                                      query_id,
                                      ):
        """
        

        :type  cluster_id: :class:`str`
        :param cluster_id: Cluster ID
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_datastore_query_response1',
                            {
                            'cluster_id': cluster_id,
                            'query_id': query_id,
                            })
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.datastores.validations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ValidationsStub)
        self._VAPI_OPERATION_IDS = {}


    def validate_vsan_remote_datastore_mount_spec(self,
                                                  cluster_id,
                                                  datastore_mount_spec,
                                                  ):
        """
        

        :type  cluster_id: :class:`str`
        :param cluster_id: Cluster ID
        :type  datastore_mount_spec: :class:`vmware.sddc_manager.model_client.DatastoreMountSpec`
        :param datastore_mount_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_vsan_remote_datastore_mount_spec',
                            {
                            'cluster_id': cluster_id,
                            'datastore_mount_spec': datastore_mount_spec,
                            })
class Validation(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.datastores.validation'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ValidationStub)
        self._VAPI_OPERATION_IDS = {}


    def validate_vsan_remote_datastore_spec(self,
                                            cluster_id,
                                            datastore_mount_spec,
                                            ):
        """
        

        :type  cluster_id: :class:`str`
        :param cluster_id: Cluster ID
        :type  datastore_mount_spec: :class:`vmware.sddc_manager.model_client.DatastoreMountSpec`
        :param datastore_mount_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_vsan_remote_datastore_spec',
                            {
                            'cluster_id': cluster_id,
                            'datastore_mount_spec': datastore_mount_spec,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.datastores.criteria'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CriteriaStub)
        self._VAPI_OPERATION_IDS = {}


    def get_datastores_criteria1(self,
                                 id,
                                 ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDatastoreCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_datastores_criteria1',
                            {
                            'id': id,
                            })

    def get_datastore_criterion1(self,
                                 id,
                                 name,
                                 ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  name: :class:`str`
        :param name: Criteria Name
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Criterion Not Found
        """
        return self._invoke('get_datastore_criterion1',
                            {
                            'id': id,
                            'name': name,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for post_datastore_query1 operation
        post_datastore_query1_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'datastore_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreCriterion'),
        })
        post_datastore_query1_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        post_datastore_query1_input_value_validator_list = [
        ]
        post_datastore_query1_output_validator_list = [
        ]
        post_datastore_query1_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{id}/datastores/queries',
            request_body_parameter='datastore_criterion',
            path_variables={
                'id': 'id',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_datastore_query_response1 operation
        get_datastore_query_response1_input_type = type.StructType('operation-input', {
            'cluster_id': type.StringType(),
            'query_id': type.StringType(),
        })
        get_datastore_query_response1_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_datastore_query_response1_input_value_validator_list = [
        ]
        get_datastore_query_response1_output_validator_list = [
        ]
        get_datastore_query_response1_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{clusterId}/datastores/queries/{queryId}',
            path_variables={
                'cluster_id': 'clusterId',
                'query_id': 'queryId',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'post_datastore_query1': {
                'input_type': post_datastore_query1_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreQueryResponse')),
                'errors': post_datastore_query1_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': post_datastore_query1_input_value_validator_list,
                'output_validator_list': post_datastore_query1_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_datastore_query_response1': {
                'input_type': get_datastore_query_response1_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreQueryResponse')),
                'errors': get_datastore_query_response1_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_datastore_query_response1_input_value_validator_list,
                'output_validator_list': get_datastore_query_response1_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'post_datastore_query1': post_datastore_query1_rest_metadata,
            'get_datastore_query_response1': get_datastore_query_response1_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.datastores.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_vsan_remote_datastore_mount_spec operation
        validate_vsan_remote_datastore_mount_spec_input_type = type.StructType('operation-input', {
            'cluster_id': type.StringType(),
            'datastore_mount_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreMountSpec'),
        })
        validate_vsan_remote_datastore_mount_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_vsan_remote_datastore_mount_spec_input_value_validator_list = [
        ]
        validate_vsan_remote_datastore_mount_spec_output_validator_list = [
        ]
        validate_vsan_remote_datastore_mount_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{clusterId}/datastores/validations',
            request_body_parameter='datastore_mount_spec',
            path_variables={
                'cluster_id': 'clusterId',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'validate_vsan_remote_datastore_mount_spec': {
                'input_type': validate_vsan_remote_datastore_mount_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_vsan_remote_datastore_mount_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_vsan_remote_datastore_mount_spec_input_value_validator_list,
                'output_validator_list': validate_vsan_remote_datastore_mount_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_vsan_remote_datastore_mount_spec': validate_vsan_remote_datastore_mount_spec_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.datastores.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_vsan_remote_datastore_spec operation
        validate_vsan_remote_datastore_spec_input_type = type.StructType('operation-input', {
            'cluster_id': type.StringType(),
            'datastore_mount_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreMountSpec'),
        })
        validate_vsan_remote_datastore_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_vsan_remote_datastore_spec_input_value_validator_list = [
        ]
        validate_vsan_remote_datastore_spec_output_validator_list = [
        ]
        validate_vsan_remote_datastore_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{clusterId}/datastores/validation',
            request_body_parameter='datastore_mount_spec',
            path_variables={
                'cluster_id': 'clusterId',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'validate_vsan_remote_datastore_spec': {
                'input_type': validate_vsan_remote_datastore_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_vsan_remote_datastore_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_vsan_remote_datastore_spec_input_value_validator_list,
                'output_validator_list': validate_vsan_remote_datastore_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_vsan_remote_datastore_spec': validate_vsan_remote_datastore_spec_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.datastores.validation',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_datastores_criteria1 operation
        get_datastores_criteria1_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_datastores_criteria1_error_dict = {}
        get_datastores_criteria1_input_value_validator_list = [
        ]
        get_datastores_criteria1_output_validator_list = [
        ]
        get_datastores_criteria1_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/datastores/criteria',
            path_variables={
                'id': 'id',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_datastore_criterion1 operation
        get_datastore_criterion1_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'name': type.StringType(),
        })
        get_datastore_criterion1_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_datastore_criterion1_input_value_validator_list = [
        ]
        get_datastore_criterion1_output_validator_list = [
        ]
        get_datastore_criterion1_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/datastores/criteria/{name}',
            path_variables={
                'id': 'id',
                'name': 'name',
            },
            query_parameters={
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'get_datastores_criteria1': {
                'input_type': get_datastores_criteria1_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDatastoreCriterion')),
                'errors': get_datastores_criteria1_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_datastores_criteria1_input_value_validator_list,
                'output_validator_list': get_datastores_criteria1_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_datastore_criterion1': {
                'input_type': get_datastore_criterion1_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreCriterion')),
                'errors': get_datastore_criterion1_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404]).build(),
                'input_value_validator_list': get_datastore_criterion1_input_value_validator_list,
                'output_validator_list': get_datastore_criterion1_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_datastores_criteria1': get_datastores_criteria1_rest_metadata,
            'get_datastore_criterion1': get_datastore_criterion1_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.datastores.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
        'Validations': Validations,
        'Validation': Validation,
        'Criteria': Criteria,
    }

