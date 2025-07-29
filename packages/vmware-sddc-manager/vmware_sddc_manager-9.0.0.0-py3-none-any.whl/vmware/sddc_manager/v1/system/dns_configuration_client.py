# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.dns_configuration.
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


class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.dns_configuration.validations'
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


    def get_validations_of_dns_configuration(self,
                                             execution_status=None,
                                             ):
        """
        

        :type  execution_status: :class:`str` or ``None``
        :param execution_status: executionStatus
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_validations_of_DNS_configuration',
                            {
                            'execution_status': execution_status,
                            })

    def validate_dns_configuration(self,
                                   dns_configuration,
                                   ):
        """
        

        :type  dns_configuration: :class:`vmware.sddc_manager.model_client.DnsConfiguration`
        :param dns_configuration: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('validate_dns_configuration',
                            {
                            'dns_configuration': dns_configuration,
                            })

    def get_validation_of_dns_configuration(self,
                                            id,
                                            ):
        """
        

        :type  id: :class:`str`
        :param id: The validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_validation_of_dns_configuration',
                            {
                            'id': id,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_validations_of_DNS_configuration operation
        get_validations_of_DNS_configuration_input_type = type.StructType('operation-input', {
            'execution_status': type.OptionalType(type.StringType()),
        })
        get_validations_of_DNS_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_validations_of_DNS_configuration_input_value_validator_list = [
        ]
        get_validations_of_DNS_configuration_output_validator_list = [
        ]
        get_validations_of_DNS_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/dns-configuration/validations',
            path_variables={
            },
            query_parameters={
                'execution_status': 'executionStatus',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for validate_dns_configuration operation
        validate_dns_configuration_input_type = type.StructType('operation-input', {
            'dns_configuration': type.ReferenceType('vmware.sddc_manager.model_client', 'DnsConfiguration'),
        })
        validate_dns_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_dns_configuration_input_value_validator_list = [
        ]
        validate_dns_configuration_output_validator_list = [
        ]
        validate_dns_configuration_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/dns-configuration/validations',
            request_body_parameter='dns_configuration',
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

        # properties for get_validation_of_dns_configuration operation
        get_validation_of_dns_configuration_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_validation_of_dns_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_validation_of_dns_configuration_input_value_validator_list = [
        ]
        get_validation_of_dns_configuration_output_validator_list = [
        ]
        get_validation_of_dns_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/dns-configuration/validations/{id}',
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
            'get_validations_of_DNS_configuration': {
                'input_type': get_validations_of_DNS_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_validations_of_DNS_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_validations_of_DNS_configuration_input_value_validator_list,
                'output_validator_list': get_validations_of_DNS_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate_dns_configuration': {
                'input_type': validate_dns_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_dns_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_dns_configuration_input_value_validator_list,
                'output_validator_list': validate_dns_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_validation_of_dns_configuration': {
                'input_type': get_validation_of_dns_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_validation_of_dns_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_validation_of_dns_configuration_input_value_validator_list,
                'output_validator_list': get_validation_of_dns_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_validations_of_DNS_configuration': get_validations_of_DNS_configuration_rest_metadata,
            'validate_dns_configuration': validate_dns_configuration_rest_metadata,
            'get_validation_of_dns_configuration': get_validation_of_dns_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.dns_configuration.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
    }

