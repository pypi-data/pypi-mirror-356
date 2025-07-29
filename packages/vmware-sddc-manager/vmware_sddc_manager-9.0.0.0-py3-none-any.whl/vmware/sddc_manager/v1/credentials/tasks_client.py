# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.credentials.tasks.
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


class Subtasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.credentials.tasks.subtasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SubtasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_credentials_sub_task(self,
                                 id,
                                 subtask_id,
                                 ):
        """
        Retrieve a credential sub task by its ID

        :type  id: :class:`str`
        :param id: The ID of the credentials task
        :type  subtask_id: :class:`str`
        :param subtask_id: The ID of the credentials sub-task
        :rtype: :class:`vmware.sddc_manager.model_client.CredentialsTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credentials_sub_task',
                            {
                            'id': id,
                            'subtask_id': subtask_id,
                            })
class ResourceCredentials(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.credentials.tasks.resource_credentials'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceCredentialsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_credential_task_by_resource_id(self,
                                           id,
                                           ):
        """
        Retriece a credential taks by resource ID

        :type  id: :class:`str`
        :param id: The ID of the credentials task
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.ResourceCredentials` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credential_task_by_resource_ID',
                            {
                            'id': id,
                            })
class _SubtasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_credentials_sub_task operation
        get_credentials_sub_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'subtask_id': type.StringType(),
        })
        get_credentials_sub_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credentials_sub_task_input_value_validator_list = [
        ]
        get_credentials_sub_task_output_validator_list = [
        ]
        get_credentials_sub_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/tasks/{id}/subtasks/{subtaskId}',
            path_variables={
                'id': 'id',
                'subtask_id': 'subtaskId',
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
            'get_credentials_sub_task': {
                'input_type': get_credentials_sub_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsTask')),
                'errors': get_credentials_sub_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_credentials_sub_task_input_value_validator_list,
                'output_validator_list': get_credentials_sub_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_credentials_sub_task': get_credentials_sub_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.credentials.tasks.subtasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ResourceCredentialsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_credential_task_by_resource_ID operation
        get_credential_task_by_resource_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_credential_task_by_resource_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credential_task_by_resource_ID_input_value_validator_list = [
        ]
        get_credential_task_by_resource_ID_output_validator_list = [
        ]
        get_credential_task_by_resource_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/tasks/{id}/resource-credentials',
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
            'get_credential_task_by_resource_ID': {
                'input_type': get_credential_task_by_resource_ID_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceCredentials'))),
                'errors': get_credential_task_by_resource_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_credential_task_by_resource_ID_input_value_validator_list,
                'output_validator_list': get_credential_task_by_resource_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_credential_task_by_resource_ID': get_credential_task_by_resource_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.credentials.tasks.resource_credentials',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Subtasks': Subtasks,
        'ResourceCredentials': ResourceCredentials,
    }

