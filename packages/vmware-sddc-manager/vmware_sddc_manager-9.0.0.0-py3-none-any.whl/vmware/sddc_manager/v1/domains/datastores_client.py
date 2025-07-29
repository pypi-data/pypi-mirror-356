# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.datastores.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.datastores.queries'
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


    def post_datastore_query(self,
                             domain_id,
                             datastore_criterion,
                             ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  datastore_criterion: :class:`vmware.sddc_manager.model_client.DatastoreCriterion`
        :param datastore_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('post_datastore_query',
                            {
                            'domain_id': domain_id,
                            'datastore_criterion': datastore_criterion,
                            })

    def get_datastore_query_response(self,
                                     domain_id,
                                     query_id,
                                     ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Query Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_datastore_query_response',
                            {
                            'domain_id': domain_id,
                            'query_id': query_id,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.datastores.criteria'
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


    def get_datastores_criteria(self,
                                domain_id,
                                ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDatastoreCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_datastores_criteria',
                            {
                            'domain_id': domain_id,
                            })

    def get_datastore_criterion(self,
                                domain_id,
                                name,
                                ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  name: :class:`str`
        :param name: Criteria Name
        :rtype: :class:`vmware.sddc_manager.model_client.DatastoreCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Criterion Not Found
        """
        return self._invoke('get_datastore_criterion',
                            {
                            'domain_id': domain_id,
                            'name': name,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for post_datastore_query operation
        post_datastore_query_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'datastore_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreCriterion'),
        })
        post_datastore_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        post_datastore_query_input_value_validator_list = [
        ]
        post_datastore_query_output_validator_list = [
        ]
        post_datastore_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{domainId}/datastores/queries',
            request_body_parameter='datastore_criterion',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_datastore_query_response operation
        get_datastore_query_response_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'query_id': type.StringType(),
        })
        get_datastore_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_datastore_query_response_input_value_validator_list = [
        ]
        get_datastore_query_response_output_validator_list = [
        ]
        get_datastore_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/datastores/queries/{queryId}',
            path_variables={
                'domain_id': 'domainId',
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
            'post_datastore_query': {
                'input_type': post_datastore_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreQueryResponse')),
                'errors': post_datastore_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': post_datastore_query_input_value_validator_list,
                'output_validator_list': post_datastore_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_datastore_query_response': {
                'input_type': get_datastore_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreQueryResponse')),
                'errors': get_datastore_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_datastore_query_response_input_value_validator_list,
                'output_validator_list': get_datastore_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'post_datastore_query': post_datastore_query_rest_metadata,
            'get_datastore_query_response': get_datastore_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.datastores.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_datastores_criteria operation
        get_datastores_criteria_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        get_datastores_criteria_error_dict = {}
        get_datastores_criteria_input_value_validator_list = [
        ]
        get_datastores_criteria_output_validator_list = [
        ]
        get_datastores_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/datastores/criteria',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_datastore_criterion operation
        get_datastore_criterion_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'name': type.StringType(),
        })
        get_datastore_criterion_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_datastore_criterion_input_value_validator_list = [
        ]
        get_datastore_criterion_output_validator_list = [
        ]
        get_datastore_criterion_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/datastores/criteria/{name}',
            path_variables={
                'domain_id': 'domainId',
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
            'get_datastores_criteria': {
                'input_type': get_datastores_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDatastoreCriterion')),
                'errors': get_datastores_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_datastores_criteria_input_value_validator_list,
                'output_validator_list': get_datastores_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_datastore_criterion': {
                'input_type': get_datastore_criterion_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreCriterion')),
                'errors': get_datastore_criterion_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404]).build(),
                'input_value_validator_list': get_datastore_criterion_input_value_validator_list,
                'output_validator_list': get_datastore_criterion_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_datastores_criteria': get_datastores_criteria_rest_metadata,
            'get_datastore_criterion': get_datastore_criterion_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.datastores.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
        'Criteria': Criteria,
    }

