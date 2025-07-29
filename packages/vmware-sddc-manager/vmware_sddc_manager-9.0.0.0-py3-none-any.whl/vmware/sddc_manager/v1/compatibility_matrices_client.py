# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.compatibility_matrices.
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


class Metadata(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compatibility_matrices.metadata'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _MetadataStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compatibility_matrix_metadata(self,
                                          compatibility_matrix_source,
                                          ):
        """
        Get Compatibility Matrix Metadata

        :type  compatibility_matrix_source: :class:`str`
        :param compatibility_matrix_source: Source of compatibility data
        :rtype: :class:`vmware.sddc_manager.model_client.CompatibilityMatrixMetadata` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compatibility_matrix_metadata',
                            {
                            'compatibility_matrix_source': compatibility_matrix_source,
                            })
class Content(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compatibility_matrices.content'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ContentStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compatibility_matrix_content(self,
                                         compatibility_matrix_source,
                                         ):
        """
        Get Compatibility Matrix content

        :type  compatibility_matrix_source: :class:`str`
        :param compatibility_matrix_source: Source of compatibility data
        :rtype: :class:`str` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compatibility_matrix_content',
                            {
                            'compatibility_matrix_source': compatibility_matrix_source,
                            })
class _MetadataStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compatibility_matrix_metadata operation
        get_compatibility_matrix_metadata_input_type = type.StructType('operation-input', {
            'compatibility_matrix_source': type.StringType(),
        })
        get_compatibility_matrix_metadata_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compatibility_matrix_metadata_input_value_validator_list = [
        ]
        get_compatibility_matrix_metadata_output_validator_list = [
        ]
        get_compatibility_matrix_metadata_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compatibility-matrices/{compatibilityMatrixSource}/metadata',
            path_variables={
                'compatibility_matrix_source': 'compatibilityMatrixSource',
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
            'get_compatibility_matrix_metadata': {
                'input_type': get_compatibility_matrix_metadata_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CompatibilityMatrixMetadata')),
                'errors': get_compatibility_matrix_metadata_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_compatibility_matrix_metadata_input_value_validator_list,
                'output_validator_list': get_compatibility_matrix_metadata_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compatibility_matrix_metadata': get_compatibility_matrix_metadata_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compatibility_matrices.metadata',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ContentStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compatibility_matrix_content operation
        get_compatibility_matrix_content_input_type = type.StructType('operation-input', {
            'compatibility_matrix_source': type.StringType(),
        })
        get_compatibility_matrix_content_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compatibility_matrix_content_input_value_validator_list = [
        ]
        get_compatibility_matrix_content_output_validator_list = [
        ]
        get_compatibility_matrix_content_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compatibility-matrices/{compatibilityMatrixSource}/content',
            path_variables={
                'compatibility_matrix_source': 'compatibilityMatrixSource',
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
            'get_compatibility_matrix_content': {
                'input_type': get_compatibility_matrix_content_input_type,
                'output_type': type.OptionalType(type.StringType()),
                'errors': get_compatibility_matrix_content_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_compatibility_matrix_content_input_value_validator_list,
                'output_validator_list': get_compatibility_matrix_content_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compatibility_matrix_content': get_compatibility_matrix_content_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compatibility_matrices.content',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Metadata': Metadata,
        'Content': Content,
    }

