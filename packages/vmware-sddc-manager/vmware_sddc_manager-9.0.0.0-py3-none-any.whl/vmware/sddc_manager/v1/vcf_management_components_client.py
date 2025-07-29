# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.vcf_management_components.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_management_components.validations'
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


    def validate_vcf_management_components(self,
                                           vcf_management_components_spec,
                                           redo=None,
                                           ):
        """
        Validates the input spec to VCF Management Components deployment
        workflow from SDDC Manager and returns a URL in the headers to track
        the operation status

        :type  vcf_management_components_spec: :class:`vmware.sddc_manager.model_client.VcfManagementComponentsSpec`
        :param vcf_management_components_spec: 
        :type  redo: :class:`bool` or ``None``
        :param redo: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('validate_vcf_management_components',
                            {
                            'vcf_management_components_spec': vcf_management_components_spec,
                            'redo': redo,
                            })

    def get_vcf_management_components_validations_by_id(self,
                                                        validation_id,
                                                        ):
        """
        

        :type  validation_id: :class:`str`
        :param validation_id: VCF Management Components validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components_validations_by_id',
                            {
                            'validation_id': validation_id,
                            })
class Tasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_management_components.tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_management_components_tasks(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components_tasks', None)

    def get_vcf_management_components_task_by_id(self,
                                                 task_id,
                                                 ):
        """
        

        :type  task_id: :class:`str`
        :param task_id: VCF Management Components task ID
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components_task_by_ID',
                            {
                            'task_id': task_id,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_vcf_management_components operation
        validate_vcf_management_components_input_type = type.StructType('operation-input', {
            'vcf_management_components_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'VcfManagementComponentsSpec'),
            'redo': type.OptionalType(type.BooleanType()),
        })
        validate_vcf_management_components_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_vcf_management_components_input_value_validator_list = [
        ]
        validate_vcf_management_components_output_validator_list = [
        ]
        validate_vcf_management_components_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vcf-management-components/validations',
            request_body_parameter='vcf_management_components_spec',
            path_variables={
            },
            query_parameters={
                'redo': 'redo',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_vcf_management_components_validations_by_id operation
        get_vcf_management_components_validations_by_id_input_type = type.StructType('operation-input', {
            'validation_id': type.StringType(),
        })
        get_vcf_management_components_validations_by_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_validations_by_id_input_value_validator_list = [
        ]
        get_vcf_management_components_validations_by_id_output_validator_list = [
        ]
        get_vcf_management_components_validations_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components/validations/{validationId}',
            path_variables={
                'validation_id': 'validationId',
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
            'validate_vcf_management_components': {
                'input_type': validate_vcf_management_components_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_vcf_management_components_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,403,500]).build(),
                'input_value_validator_list': validate_vcf_management_components_input_value_validator_list,
                'output_validator_list': validate_vcf_management_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vcf_management_components_validations_by_id': {
                'input_type': get_vcf_management_components_validations_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_vcf_management_components_validations_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,404,500]).build(),
                'input_value_validator_list': get_vcf_management_components_validations_by_id_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_validations_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_vcf_management_components': validate_vcf_management_components_rest_metadata,
            'get_vcf_management_components_validations_by_id': get_vcf_management_components_validations_by_id_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_management_components.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_management_components_tasks operation
        get_vcf_management_components_tasks_input_type = type.StructType('operation-input', {})
        get_vcf_management_components_tasks_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_tasks_input_value_validator_list = [
        ]
        get_vcf_management_components_tasks_output_validator_list = [
        ]
        get_vcf_management_components_tasks_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components/tasks',
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

        # properties for get_vcf_management_components_task_by_ID operation
        get_vcf_management_components_task_by_ID_input_type = type.StructType('operation-input', {
            'task_id': type.StringType(),
        })
        get_vcf_management_components_task_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_task_by_ID_input_value_validator_list = [
        ]
        get_vcf_management_components_task_by_ID_output_validator_list = [
        ]
        get_vcf_management_components_task_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components/tasks/{taskId}',
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
            'get_vcf_management_components_tasks': {
                'input_type': get_vcf_management_components_tasks_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTask')),
                'errors': get_vcf_management_components_tasks_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_vcf_management_components_tasks_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_tasks_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vcf_management_components_task_by_ID': {
                'input_type': get_vcf_management_components_task_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': get_vcf_management_components_task_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,404,500]).build(),
                'input_value_validator_list': get_vcf_management_components_task_by_ID_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_task_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_management_components_tasks': get_vcf_management_components_tasks_rest_metadata,
            'get_vcf_management_components_task_by_ID': get_vcf_management_components_task_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_management_components.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
        'Tasks': Tasks,
        'tasks': 'vmware.sddc_manager.v1.vcf_management_components.tasks_client.StubFactory',
    }

