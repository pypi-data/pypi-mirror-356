# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.vsan_hcl.
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


class Configuration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vsan_hcl.configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vsan_hcl_configuration(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.VsanHclConfiguration` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. vSAN HCL configuration not found
        """
        return self._invoke('get_vsan_hcl_configuration', None)

    def update_vsan_hcl_configuration(self,
                                      vsan_hcl_configuration,
                                      ):
        """
        

        :type  vsan_hcl_configuration: :class:`vmware.sddc_manager.model_client.VsanHclConfiguration`
        :param vsan_hcl_configuration: 
        :rtype: :class:`vmware.sddc_manager.model_client.VsanHclConfiguration` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. vSAN HCL configuration not found
        """
        return self._invoke('update_vsan_hcl_configuration',
                            {
                            'vsan_hcl_configuration': vsan_hcl_configuration,
                            })
class Attributes(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vsan_hcl.attributes'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AttributesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vsan_hcl_attributes(self):
        """
        Attributes of vSAN HCL data such as timestamp of last update


        :rtype: :class:`vmware.sddc_manager.model_client.VsanHclAttributes` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. vSAN HCL attributes not found
        """
        return self._invoke('get_vsan_hcl_attributes', None)
class _ConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vsan_hcl_configuration operation
        get_vsan_hcl_configuration_input_type = type.StructType('operation-input', {})
        get_vsan_hcl_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vsan_hcl_configuration_input_value_validator_list = [
        ]
        get_vsan_hcl_configuration_output_validator_list = [
        ]
        get_vsan_hcl_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vsan-hcl/configuration',
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

        # properties for update_vsan_hcl_configuration operation
        update_vsan_hcl_configuration_input_type = type.StructType('operation-input', {
            'vsan_hcl_configuration': type.ReferenceType('vmware.sddc_manager.model_client', 'VsanHclConfiguration'),
        })
        update_vsan_hcl_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_vsan_hcl_configuration_input_value_validator_list = [
        ]
        update_vsan_hcl_configuration_output_validator_list = [
        ]
        update_vsan_hcl_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/vsan-hcl/configuration',
            request_body_parameter='vsan_hcl_configuration',
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
            'get_vsan_hcl_configuration': {
                'input_type': get_vsan_hcl_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VsanHclConfiguration')),
                'errors': get_vsan_hcl_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_vsan_hcl_configuration_input_value_validator_list,
                'output_validator_list': get_vsan_hcl_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_vsan_hcl_configuration': {
                'input_type': update_vsan_hcl_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VsanHclConfiguration')),
                'errors': update_vsan_hcl_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': update_vsan_hcl_configuration_input_value_validator_list,
                'output_validator_list': update_vsan_hcl_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vsan_hcl_configuration': get_vsan_hcl_configuration_rest_metadata,
            'update_vsan_hcl_configuration': update_vsan_hcl_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vsan_hcl.configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _AttributesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vsan_hcl_attributes operation
        get_vsan_hcl_attributes_input_type = type.StructType('operation-input', {})
        get_vsan_hcl_attributes_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vsan_hcl_attributes_input_value_validator_list = [
        ]
        get_vsan_hcl_attributes_output_validator_list = [
        ]
        get_vsan_hcl_attributes_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vsan-hcl/attributes',
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
            'get_vsan_hcl_attributes': {
                'input_type': get_vsan_hcl_attributes_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VsanHclAttributes')),
                'errors': get_vsan_hcl_attributes_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_vsan_hcl_attributes_input_value_validator_list,
                'output_validator_list': get_vsan_hcl_attributes_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vsan_hcl_attributes': get_vsan_hcl_attributes_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vsan_hcl.attributes',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Configuration': Configuration,
        'Attributes': Attributes,
    }

