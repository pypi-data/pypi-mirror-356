# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.backup_configuration.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.backup_configuration.validations'
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


    def validate_backup_configurations_operations(self,
                                                  backup_configuration_spec,
                                                  ):
        """
        

        :type  backup_configuration_spec: :class:`vmware.sddc_manager.model_client.BackupConfigurationSpec`
        :param backup_configuration_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_backup_configurations_operations',
                            {
                            'backup_configuration_spec': backup_configuration_spec,
                            })
class BackupLocations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.backup_configuration.backup_locations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BackupLocationsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_backup_location(self,
                            server_ip=None,
                            port=None,
                            ):
        """
        

        :type  server_ip: :class:`str` or ``None``
        :param server_ip: Backup server IP
        :type  port: :class:`str` or ``None``
        :param port: Backup server port
        :rtype: :class:`vmware.sddc_manager.model_client.BackupLocation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_backup_location',
                            {
                            'server_ip': server_ip,
                            'port': port,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_backup_configurations_operations operation
        validate_backup_configurations_operations_input_type = type.StructType('operation-input', {
            'backup_configuration_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BackupConfigurationSpec'),
        })
        validate_backup_configurations_operations_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_backup_configurations_operations_input_value_validator_list = [
        ]
        validate_backup_configurations_operations_output_validator_list = [
        ]
        validate_backup_configurations_operations_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/backup-configuration/validations',
            request_body_parameter='backup_configuration_spec',
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
            'validate_backup_configurations_operations': {
                'input_type': validate_backup_configurations_operations_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_backup_configurations_operations_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': validate_backup_configurations_operations_input_value_validator_list,
                'output_validator_list': validate_backup_configurations_operations_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_backup_configurations_operations': validate_backup_configurations_operations_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.backup_configuration.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _BackupLocationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_backup_location operation
        get_backup_location_input_type = type.StructType('operation-input', {
            'server_ip': type.OptionalType(type.StringType()),
            'port': type.OptionalType(type.StringType()),
        })
        get_backup_location_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_backup_location_input_value_validator_list = [
        ]
        get_backup_location_output_validator_list = [
        ]
        get_backup_location_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/backup-configuration/backup-locations',
            path_variables={
            },
            query_parameters={
                'server_ip': 'serverIp',
                'port': 'port',
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
            'get_backup_location': {
                'input_type': get_backup_location_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BackupLocation')),
                'errors': get_backup_location_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_backup_location_input_value_validator_list,
                'output_validator_list': get_backup_location_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_backup_location': get_backup_location_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.backup_configuration.backup_locations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
        'BackupLocations': BackupLocations,
    }

