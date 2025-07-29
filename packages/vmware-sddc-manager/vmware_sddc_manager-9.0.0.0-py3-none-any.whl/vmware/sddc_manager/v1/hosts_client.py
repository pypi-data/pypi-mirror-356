# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.hosts.
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


class Tags(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.tags'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TagsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_tags_assigned_to_host(self,
                                  id,
                                  ):
        """
        Get Tags assigned to Host

        :type  id: :class:`str`
        :param id: Host ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTag` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_tags_assigned_to_host',
                            {
                            'id': id,
                            })

    def assign_tags_to_host(self,
                            id,
                            tags_spec,
                            ):
        """
        Assign tags to a host

        :type  id: :class:`str`
        :param id: Host ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: Assign tags to a host request body.
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('assign_tags_to_host',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def remove_tags_from_host(self,
                              id,
                              tags_spec,
                              ):
        """
        Remove Tags From Host

        :type  id: :class:`str`
        :param id: Host ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: Remove Tags From Host request body.
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('remove_tags_from_host',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def get_tags_assigned_to_hosts(self):
        """
        Get Tags assigned to Hosts


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTagsForResource` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_tags_assigned_to_hosts', None)
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.validations'
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


    def validate_host_commission_spec(self,
                                      validate_host_commission_spec_request_body,
                                      ):
        """
        

        :type  validate_host_commission_spec_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.HostCommissionSpec`
        :param validate_host_commission_spec_request_body: Perform validation of the HostCommissionSpec specification request
            body.
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_host_commission_spec',
                            {
                            'validate_host_commission_spec_request_body': validate_host_commission_spec_request_body,
                            })

    def get_host_commission_validation_by_id(self,
                                             id,
                                             ):
        """
        

        :type  id: :class:`str`
        :param id: The validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_host_commission_validation_by_ID',
                            {
                            'id': id,
                            })
class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.queries'
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


    def post_query(self,
                   host_criterion,
                   size=None,
                   page=None,
                   ):
        """
        Post a query

        :type  host_criterion: :class:`vmware.sddc_manager.model_client.HostCriterion`
        :param host_criterion: Post a query request body.
        :type  size: :class:`long` or ``None``
        :param size: Size of the page to retrieve. Default page size is 4000. Optional
        :type  page: :class:`long` or ``None``
        :param page: Page number to retrieve. Default page is 1. Optional
        :rtype: :class:`vmware.sddc_manager.model_client.HostQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('post_query',
                            {
                            'host_criterion': host_criterion,
                            'size': size,
                            'page': page,
                            })

    def get_host_query_response(self,
                                id,
                                ):
        """
        Get query response

        :type  id: :class:`str`
        :param id: 
        :rtype: :class:`vmware.sddc_manager.model_client.HostQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Query Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_host_query_response',
                            {
                            'id': id,
                            })
class Prechecks(VapiInterface):
    """
    The following API operation(s) are not included in the SDK yet, but can be
    accessed via HTTP requests to the REST API: 
    
    * /v1/hosts/prechecks POST
    
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.prechecks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrechecksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_hosts_prechecks_response(self,
                                     id,
                                     ):
        """
        Get host(s) prechecks response

        :type  id: :class:`str`
        :param id: Execution ID returned by post hostsprecheks
        :rtype: :class:`vmware.sddc_manager.model_client.HostsPrechecksResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Resource Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_hosts_prechecks_response',
                            {
                            'id': id,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.criteria'
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


    def get_criteria(self):
        """
        Get all criteria


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfHostCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_criteria', None)

    def get_criterion(self,
                      name,
                      ):
        """
        Get a criterion

        :type  name: :class:`str`
        :param name: 
        :rtype: :class:`vmware.sddc_manager.model_client.HostCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Criterion Not Found
        """
        return self._invoke('get_criterion',
                            {
                            'name': name,
                            })
class _TagsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_tags_assigned_to_host operation
        get_tags_assigned_to_host_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_tags_assigned_to_host_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_host_input_value_validator_list = [
        ]
        get_tags_assigned_to_host_output_validator_list = [
        ]
        get_tags_assigned_to_host_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/{id}/tags',
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

        # properties for assign_tags_to_host operation
        assign_tags_to_host_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        assign_tags_to_host_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        assign_tags_to_host_input_value_validator_list = [
        ]
        assign_tags_to_host_output_validator_list = [
        ]
        assign_tags_to_host_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/hosts/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for remove_tags_from_host operation
        remove_tags_from_host_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        remove_tags_from_host_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_tags_from_host_input_value_validator_list = [
        ]
        remove_tags_from_host_output_validator_list = [
        ]
        remove_tags_from_host_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/hosts/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for get_tags_assigned_to_hosts operation
        get_tags_assigned_to_hosts_input_type = type.StructType('operation-input', {})
        get_tags_assigned_to_hosts_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_hosts_input_value_validator_list = [
        ]
        get_tags_assigned_to_hosts_output_validator_list = [
        ]
        get_tags_assigned_to_hosts_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/tags',
            path_variables={
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
            'get_tags_assigned_to_host': {
                'input_type': get_tags_assigned_to_host_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTag')),
                'errors': get_tags_assigned_to_host_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_host_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_host_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'assign_tags_to_host': {
                'input_type': assign_tags_to_host_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': assign_tags_to_host_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': assign_tags_to_host_input_value_validator_list,
                'output_validator_list': assign_tags_to_host_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_tags_from_host': {
                'input_type': remove_tags_from_host_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': remove_tags_from_host_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': remove_tags_from_host_input_value_validator_list,
                'output_validator_list': remove_tags_from_host_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_tags_assigned_to_hosts': {
                'input_type': get_tags_assigned_to_hosts_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTagsForResource')),
                'errors': get_tags_assigned_to_hosts_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_hosts_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_hosts_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_tags_assigned_to_host': get_tags_assigned_to_host_rest_metadata,
            'assign_tags_to_host': assign_tags_to_host_rest_metadata,
            'remove_tags_from_host': remove_tags_from_host_rest_metadata,
            'get_tags_assigned_to_hosts': get_tags_assigned_to_hosts_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.tags',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_host_commission_spec operation
        validate_host_commission_spec_input_type = type.StructType('operation-input', {
            'validate_host_commission_spec_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostCommissionSpec')),
        })
        validate_host_commission_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_host_commission_spec_input_value_validator_list = [
        ]
        validate_host_commission_spec_output_validator_list = [
        ]
        validate_host_commission_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/hosts/validations',
            request_body_parameter='validate_host_commission_spec_request_body',
            path_variables={
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

        # properties for get_host_commission_validation_by_ID operation
        get_host_commission_validation_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_host_commission_validation_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_host_commission_validation_by_ID_input_value_validator_list = [
        ]
        get_host_commission_validation_by_ID_output_validator_list = [
        ]
        get_host_commission_validation_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/validations/{id}',
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

        operations = {
            'validate_host_commission_spec': {
                'input_type': validate_host_commission_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_host_commission_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': validate_host_commission_spec_input_value_validator_list,
                'output_validator_list': validate_host_commission_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_host_commission_validation_by_ID': {
                'input_type': get_host_commission_validation_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_host_commission_validation_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': get_host_commission_validation_by_ID_input_value_validator_list,
                'output_validator_list': get_host_commission_validation_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_host_commission_spec': validate_host_commission_spec_rest_metadata,
            'get_host_commission_validation_by_ID': get_host_commission_validation_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for post_query operation
        post_query_input_type = type.StructType('operation-input', {
            'host_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'HostCriterion'),
            'size': type.OptionalType(type.IntegerType()),
            'page': type.OptionalType(type.IntegerType()),
        })
        post_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        post_query_input_value_validator_list = [
        ]
        post_query_output_validator_list = [
        ]
        post_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/hosts/queries',
            request_body_parameter='host_criterion',
            path_variables={
            },
            query_parameters={
                'size': 'size',
                'page': 'page',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_host_query_response operation
        get_host_query_response_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_host_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_host_query_response_input_value_validator_list = [
        ]
        get_host_query_response_output_validator_list = [
        ]
        get_host_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/queries/{id}',
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

        operations = {
            'post_query': {
                'input_type': post_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostQueryResponse')),
                'errors': post_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': post_query_input_value_validator_list,
                'output_validator_list': post_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_host_query_response': {
                'input_type': get_host_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostQueryResponse')),
                'errors': get_host_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': get_host_query_response_input_value_validator_list,
                'output_validator_list': get_host_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'post_query': post_query_rest_metadata,
            'get_host_query_response': get_host_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _PrechecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_hosts_prechecks_response operation
        get_hosts_prechecks_response_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_hosts_prechecks_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_hosts_prechecks_response_input_value_validator_list = [
        ]
        get_hosts_prechecks_response_output_validator_list = [
        ]
        get_hosts_prechecks_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/prechecks/{id}',
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

        operations = {
            'get_hosts_prechecks_response': {
                'input_type': get_hosts_prechecks_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostsPrechecksResponse')),
                'errors': get_hosts_prechecks_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_hosts_prechecks_response_input_value_validator_list,
                'output_validator_list': get_hosts_prechecks_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_hosts_prechecks_response': get_hosts_prechecks_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.prechecks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_criteria operation
        get_criteria_input_type = type.StructType('operation-input', {})
        get_criteria_error_dict = {}
        get_criteria_input_value_validator_list = [
        ]
        get_criteria_output_validator_list = [
        ]
        get_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/criteria',
            path_variables={
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

        # properties for get_criterion operation
        get_criterion_input_type = type.StructType('operation-input', {
            'name': type.StringType(),
        })
        get_criterion_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_criterion_input_value_validator_list = [
        ]
        get_criterion_output_validator_list = [
        ]
        get_criterion_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/criteria/{name}',
            path_variables={
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
            'get_criteria': {
                'input_type': get_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfHostCriterion')),
                'errors': get_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_criteria_input_value_validator_list,
                'output_validator_list': get_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_criterion': {
                'input_type': get_criterion_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostCriterion')),
                'errors': get_criterion_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404]).build(),
                'input_value_validator_list': get_criterion_input_value_validator_list,
                'output_validator_list': get_criterion_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_criteria': get_criteria_rest_metadata,
            'get_criterion': get_criterion_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tags': Tags,
        'Validations': Validations,
        'Queries': Queries,
        'Prechecks': Prechecks,
        'Criteria': Criteria,
        'tags': 'vmware.sddc_manager.v1.hosts.tags_client.StubFactory',
        'validations': 'vmware.sddc_manager.v1.hosts.validations_client.StubFactory',
    }

