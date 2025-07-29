# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.vcenters.repository_images.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcenters.repository_images.queries'
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


    def initiate_repository_images_query(self,
                                         repository_image_query_spec=None,
                                         ):
        """
        

        :type  repository_image_query_spec: :class:`vmware.sddc_manager.model_client.RepositoryImageQuerySpec` or ``None``
        :param repository_image_query_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.RepositoryImageQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 429. Too Many Requests
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('initiate_repository_images_query',
                            {
                            'repository_image_query_spec': repository_image_query_spec,
                            })

    def get_repository_images_query_response(self,
                                             query_id,
                                             ):
        """
        

        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.RepositoryImageQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Query Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_repository_images_query_response',
                            {
                            'query_id': query_id,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for initiate_repository_images_query operation
        initiate_repository_images_query_input_type = type.StructType('operation-input', {
            'repository_image_query_spec': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'RepositoryImageQuerySpec')),
        })
        initiate_repository_images_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        initiate_repository_images_query_input_value_validator_list = [
        ]
        initiate_repository_images_query_output_validator_list = [
        ]
        initiate_repository_images_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vcenters/repository-images/queries',
            request_body_parameter='repository_image_query_spec',
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

        # properties for get_repository_images_query_response operation
        get_repository_images_query_response_input_type = type.StructType('operation-input', {
            'query_id': type.StringType(),
        })
        get_repository_images_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_repository_images_query_response_input_value_validator_list = [
        ]
        get_repository_images_query_response_output_validator_list = [
        ]
        get_repository_images_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcenters/repository-images/queries/{queryId}',
            path_variables={
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
            'initiate_repository_images_query': {
                'input_type': initiate_repository_images_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'RepositoryImageQueryResponse')),
                'errors': initiate_repository_images_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [429,400,500]).build(),
                'input_value_validator_list': initiate_repository_images_query_input_value_validator_list,
                'output_validator_list': initiate_repository_images_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_repository_images_query_response': {
                'input_type': get_repository_images_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'RepositoryImageQueryResponse')),
                'errors': get_repository_images_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': get_repository_images_query_response_input_value_validator_list,
                'output_validator_list': get_repository_images_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'initiate_repository_images_query': initiate_repository_images_query_rest_metadata,
            'get_repository_images_query_response': get_repository_images_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcenters.repository_images.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
    }

