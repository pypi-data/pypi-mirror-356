# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.vcf_management_components.tasks.
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


class Spec(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_management_components.tasks.spec'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SpecStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_management_components_task_spec(self,
                                                task_id,
                                                ):
        """
        

        :type  task_id: :class:`str`
        :param task_id: VCF Management Components task ID
        :rtype: :class:`vmware.sddc_manager.model_client.VcfManagementComponentsSpec` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components_task_spec',
                            {
                            'task_id': task_id,
                            })
class Latest(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_management_components.tasks.latest'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LatestStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_management_components_latest_task(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components_latest_task', None)
class _SpecStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_management_components_task_spec operation
        get_vcf_management_components_task_spec_input_type = type.StructType('operation-input', {
            'task_id': type.StringType(),
        })
        get_vcf_management_components_task_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_task_spec_input_value_validator_list = [
        ]
        get_vcf_management_components_task_spec_output_validator_list = [
        ]
        get_vcf_management_components_task_spec_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components/tasks/{taskId}/spec',
            path_variables={
                'task_id': 'taskId',
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
            'get_vcf_management_components_task_spec': {
                'input_type': get_vcf_management_components_task_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VcfManagementComponentsSpec')),
                'errors': get_vcf_management_components_task_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_vcf_management_components_task_spec_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_task_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_management_components_task_spec': get_vcf_management_components_task_spec_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_management_components.tasks.spec',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _LatestStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_management_components_latest_task operation
        get_vcf_management_components_latest_task_input_type = type.StructType('operation-input', {})
        get_vcf_management_components_latest_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_latest_task_input_value_validator_list = [
        ]
        get_vcf_management_components_latest_task_output_validator_list = [
        ]
        get_vcf_management_components_latest_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components/tasks/latest',
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
            'get_vcf_management_components_latest_task': {
                'input_type': get_vcf_management_components_latest_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': get_vcf_management_components_latest_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_vcf_management_components_latest_task_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_latest_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_management_components_latest_task': get_vcf_management_components_latest_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_management_components.tasks.latest',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Spec': Spec,
        'Latest': Latest,
    }

