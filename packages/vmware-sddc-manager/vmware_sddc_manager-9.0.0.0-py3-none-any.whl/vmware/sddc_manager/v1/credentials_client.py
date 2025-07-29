# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.credentials.
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


class Expirations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.credentials.expirations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ExpirationsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_password_expiration(self,
                                credentials_expiration_spec,
                                ):
        """
        Fetch expiration details of passwords for a list of credentials

        :type  credentials_expiration_spec: :class:`vmware.sddc_manager.model_client.CredentialsExpirationSpec`
        :param credentials_expiration_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.CredentialsExpiration` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 429. Too many requests
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_password_expiration',
                            {
                            'credentials_expiration_spec': credentials_expiration_spec,
                            })

    def get_password_expiration_by_task_id(self,
                                           id,
                                           ):
        """
        Retrive a password expiration task by ID

        :type  id: :class:`str`
        :param id: The expiration fetch workflow ID
        :rtype: :class:`vmware.sddc_manager.model_client.CredentialsExpiration` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_password_expiration_by_task_ID',
                            {
                            'id': id,
                            })
class Tasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.credentials.tasks'
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


    def get_credentials_task(self,
                             id,
                             ):
        """
        Retrieve a credential task by ID

        :type  id: :class:`str`
        :param id: The ID of the credentials task
        :rtype: :class:`vmware.sddc_manager.model_client.CredentialsTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credentials_task',
                            {
                            'id': id,
                            })

    def cancel_credentials_task(self,
                                id,
                                ):
        """
        Cancel a failed credential task by its ID

        :type  id: :class:`str`
        :param id: Task ID of the failed operation required to be cancelled
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('cancel_credentials_task',
                            {
                            'id': id,
                            })

    def retry_credentials_task(self,
                               id,
                               credentials_update_spec,
                               ):
        """
        Retry a failed credentials task for a given ID

        :type  id: :class:`str`
        :param id: Task ID of the failed operation that is to be retried
        :type  credentials_update_spec: :class:`vmware.sddc_manager.model_client.CredentialsUpdateSpec`
        :param credentials_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('retry_credentials_task',
                            {
                            'id': id,
                            'credentials_update_spec': credentials_update_spec,
                            })

    def get_credentials_tasks(self,
                              limit=None,
                              ):
        """
        Retrieve a list of credential tasks

        :type  limit: :class:`long` or ``None``
        :param limit: The number of elements to be returned in the result
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCredentialsTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credentials_tasks',
                            {
                            'limit': limit,
                            })
class _ExpirationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_password_expiration operation
        get_password_expiration_input_type = type.StructType('operation-input', {
            'credentials_expiration_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsExpirationSpec'),
        })
        get_password_expiration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_password_expiration_input_value_validator_list = [
        ]
        get_password_expiration_output_validator_list = [
        ]
        get_password_expiration_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/credentials/expirations',
            request_body_parameter='credentials_expiration_spec',
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

        # properties for get_password_expiration_by_task_ID operation
        get_password_expiration_by_task_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_password_expiration_by_task_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_password_expiration_by_task_ID_input_value_validator_list = [
        ]
        get_password_expiration_by_task_ID_output_validator_list = [
        ]
        get_password_expiration_by_task_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/expirations/{id}',
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
            'get_password_expiration': {
                'input_type': get_password_expiration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsExpiration')),
                'errors': get_password_expiration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,429,401,403,400]).build(),
                'input_value_validator_list': get_password_expiration_input_value_validator_list,
                'output_validator_list': get_password_expiration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_password_expiration_by_task_ID': {
                'input_type': get_password_expiration_by_task_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsExpiration')),
                'errors': get_password_expiration_by_task_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': get_password_expiration_by_task_ID_input_value_validator_list,
                'output_validator_list': get_password_expiration_by_task_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_password_expiration': get_password_expiration_rest_metadata,
            'get_password_expiration_by_task_ID': get_password_expiration_by_task_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.credentials.expirations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_credentials_task operation
        get_credentials_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_credentials_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credentials_task_input_value_validator_list = [
        ]
        get_credentials_task_output_validator_list = [
        ]
        get_credentials_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/tasks/{id}',
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

        # properties for cancel_credentials_task operation
        cancel_credentials_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        cancel_credentials_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        cancel_credentials_task_input_value_validator_list = [
        ]
        cancel_credentials_task_output_validator_list = [
        ]
        cancel_credentials_task_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/credentials/tasks/{id}',
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

        # properties for retry_credentials_task operation
        retry_credentials_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'credentials_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsUpdateSpec'),
        })
        retry_credentials_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        retry_credentials_task_input_value_validator_list = [
        ]
        retry_credentials_task_output_validator_list = [
        ]
        retry_credentials_task_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/credentials/tasks/{id}',
            request_body_parameter='credentials_update_spec',
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

        # properties for get_credentials_tasks operation
        get_credentials_tasks_input_type = type.StructType('operation-input', {
            'limit': type.OptionalType(type.IntegerType()),
        })
        get_credentials_tasks_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credentials_tasks_input_value_validator_list = [
        ]
        get_credentials_tasks_output_validator_list = [
        ]
        get_credentials_tasks_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/tasks',
            path_variables={
            },
            query_parameters={
                'limit': 'limit',
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
            'get_credentials_task': {
                'input_type': get_credentials_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsTask')),
                'errors': get_credentials_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_credentials_task_input_value_validator_list,
                'output_validator_list': get_credentials_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel_credentials_task': {
                'input_type': cancel_credentials_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': cancel_credentials_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': cancel_credentials_task_input_value_validator_list,
                'output_validator_list': cancel_credentials_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'retry_credentials_task': {
                'input_type': retry_credentials_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': retry_credentials_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,403,400]).build(),
                'input_value_validator_list': retry_credentials_task_input_value_validator_list,
                'output_validator_list': retry_credentials_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_credentials_tasks': {
                'input_type': get_credentials_tasks_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCredentialsTask')),
                'errors': get_credentials_tasks_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_credentials_tasks_input_value_validator_list,
                'output_validator_list': get_credentials_tasks_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_credentials_task': get_credentials_task_rest_metadata,
            'cancel_credentials_task': cancel_credentials_task_rest_metadata,
            'retry_credentials_task': retry_credentials_task_rest_metadata,
            'get_credentials_tasks': get_credentials_tasks_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.credentials.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Expirations': Expirations,
        'Tasks': Tasks,
        'tasks': 'vmware.sddc_manager.v1.credentials.tasks_client.StubFactory',
    }

