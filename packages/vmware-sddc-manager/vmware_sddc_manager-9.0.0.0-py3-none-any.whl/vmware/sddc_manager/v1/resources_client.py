# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.resources.
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


class LicensingInfos(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.resources.licensing_infos'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LicensingInfosStub)
        self._VAPI_OPERATION_IDS = {}


    def set_license_key_for_resource(self,
                                     licensing_spec,
                                     ):
        """
        

        :type  licensing_spec: :class:`vmware.sddc_manager.model_client.LicensingSpec`
        :param licensing_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('set_license_key_for_resource',
                            {
                            'licensing_spec': licensing_spec,
                            })
class LicenseChecks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.resources.license_checks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LicenseChecksStub)
        self._VAPI_OPERATION_IDS = {}


    def start_license_check_by_resource(self,
                                        resources_license_check_spec,
                                        ):
        """
        

        :type  resources_license_check_spec: :class:`vmware.sddc_manager.model_client.ResourcesLicenseCheckSpec`
        :param resources_license_check_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ResourcesLicenseCheckResult` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('start_license_check_by_resource',
                            {
                            'resources_license_check_spec': resources_license_check_spec,
                            })

    def get_license_check_result_by_id(self,
                                       id,
                                       ):
        """
        

        :type  id: :class:`str`
        :param id: The resources license check ID
        :rtype: :class:`vmware.sddc_manager.model_client.ResourcesLicenseCheckResult` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_license_check_result_by_ID',
                            {
                            'id': id,
                            })
class _LicensingInfosStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set_license_key_for_resource operation
        set_license_key_for_resource_input_type = type.StructType('operation-input', {
            'licensing_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'LicensingSpec'),
        })
        set_license_key_for_resource_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        set_license_key_for_resource_input_value_validator_list = [
        ]
        set_license_key_for_resource_output_validator_list = [
        ]
        set_license_key_for_resource_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/resources/licensing-infos',
            request_body_parameter='licensing_spec',
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
            'set_license_key_for_resource': {
                'input_type': set_license_key_for_resource_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': set_license_key_for_resource_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': set_license_key_for_resource_input_value_validator_list,
                'output_validator_list': set_license_key_for_resource_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set_license_key_for_resource': set_license_key_for_resource_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.resources.licensing_infos',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _LicenseChecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for start_license_check_by_resource operation
        start_license_check_by_resource_input_type = type.StructType('operation-input', {
            'resources_license_check_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ResourcesLicenseCheckSpec'),
        })
        start_license_check_by_resource_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_license_check_by_resource_input_value_validator_list = [
        ]
        start_license_check_by_resource_output_validator_list = [
        ]
        start_license_check_by_resource_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/resources/license-checks',
            request_body_parameter='resources_license_check_spec',
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

        # properties for get_license_check_result_by_ID operation
        get_license_check_result_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_license_check_result_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_license_check_result_by_ID_input_value_validator_list = [
        ]
        get_license_check_result_by_ID_output_validator_list = [
        ]
        get_license_check_result_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/resources/license-checks/{id}',
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
            'start_license_check_by_resource': {
                'input_type': start_license_check_by_resource_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourcesLicenseCheckResult')),
                'errors': start_license_check_by_resource_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': start_license_check_by_resource_input_value_validator_list,
                'output_validator_list': start_license_check_by_resource_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_license_check_result_by_ID': {
                'input_type': get_license_check_result_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourcesLicenseCheckResult')),
                'errors': get_license_check_result_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_license_check_result_by_ID_input_value_validator_list,
                'output_validator_list': get_license_check_result_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'start_license_check_by_resource': start_license_check_by_resource_rest_metadata,
            'get_license_check_result_by_ID': get_license_check_result_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.resources.license_checks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'LicensingInfos': LicensingInfos,
        'LicenseChecks': LicenseChecks,
    }

