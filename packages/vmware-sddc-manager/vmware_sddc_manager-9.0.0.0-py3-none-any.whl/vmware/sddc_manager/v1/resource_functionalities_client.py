# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.resource_functionalities.
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


class Global(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.resource_functionalities.global'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _GlobalStub)
        self._VAPI_OPERATION_IDS = {}


    def get_resources_functionalities_allowed_global(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.ResourceFunctionalitiesGlobalConfiguration` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_resources_functionalities_allowed_global', None)

    def update_resources_functionalities1(self,
                                          resource_functionalities_global_update_spec,
                                          ):
        """
        

        :type  resource_functionalities_global_update_spec: :class:`vmware.sddc_manager.model_client.ResourceFunctionalitiesGlobalUpdateSpec`
        :param resource_functionalities_global_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ResourceFunctionalitiesGlobalConfigurationCaller` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_resources_functionalities1',
                            {
                            'resource_functionalities_global_update_spec': resource_functionalities_global_update_spec,
                            })
class _GlobalStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_resources_functionalities_allowed_global operation
        get_resources_functionalities_allowed_global_input_type = type.StructType('operation-input', {})
        get_resources_functionalities_allowed_global_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_resources_functionalities_allowed_global_input_value_validator_list = [
        ]
        get_resources_functionalities_allowed_global_output_validator_list = [
        ]
        get_resources_functionalities_allowed_global_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/resource-functionalities/global',
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

        # properties for update_resources_functionalities1 operation
        update_resources_functionalities1_input_type = type.StructType('operation-input', {
            'resource_functionalities_global_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceFunctionalitiesGlobalUpdateSpec'),
        })
        update_resources_functionalities1_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_resources_functionalities1_input_value_validator_list = [
        ]
        update_resources_functionalities1_output_validator_list = [
        ]
        update_resources_functionalities1_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/resource-functionalities/global',
            request_body_parameter='resource_functionalities_global_update_spec',
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
            'get_resources_functionalities_allowed_global': {
                'input_type': get_resources_functionalities_allowed_global_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceFunctionalitiesGlobalConfiguration')),
                'errors': get_resources_functionalities_allowed_global_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_resources_functionalities_allowed_global_input_value_validator_list,
                'output_validator_list': get_resources_functionalities_allowed_global_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_resources_functionalities1': {
                'input_type': update_resources_functionalities1_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceFunctionalitiesGlobalConfigurationCaller')),
                'errors': update_resources_functionalities1_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_resources_functionalities1_input_value_validator_list,
                'output_validator_list': update_resources_functionalities1_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_resources_functionalities_allowed_global': get_resources_functionalities_allowed_global_rest_metadata,
            'update_resources_functionalities1': update_resources_functionalities1_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.resource_functionalities.global',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Global': Global,
    }

