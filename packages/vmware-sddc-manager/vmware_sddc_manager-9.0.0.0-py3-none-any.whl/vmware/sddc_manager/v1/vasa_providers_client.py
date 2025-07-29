# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.vasa_providers.
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


class Users(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vasa_providers.users'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UsersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vasa_provider_user(self,
                               id,
                               ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.VasaUser` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vasa_provider_user',
                            {
                            'id': id,
                            })

    def add_vasa_provider_user(self,
                               id,
                               add_vasa_provider_user_request_body,
                               ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  add_vasa_provider_user_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.VasaUser`
        :param add_vasa_provider_user_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('add_vasa_provider_user',
                            {
                            'id': id,
                            'add_vasa_provider_user_request_body': add_vasa_provider_user_request_body,
                            })

    def update_vasa_provider_user(self,
                                  id,
                                  user_id,
                                  vasa_user_update_spec,
                                  ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  user_id: :class:`str`
        :param user_id: User ID
        :type  vasa_user_update_spec: :class:`vmware.sddc_manager.model_client.VasaUserUpdateSpec`
        :param vasa_user_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. User not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_vasa_provider_user',
                            {
                            'id': id,
                            'user_id': user_id,
                            'vasa_user_update_spec': vasa_user_update_spec,
                            })
class StorageContainers(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vasa_providers.storage_containers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _StorageContainersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vasa_provider_storage_containers(self,
                                             id,
                                             protocol_type=None,
                                             ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  protocol_type: :class:`str` or ``None``
        :param protocol_type: Pass an optional Storage Protocol type
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.StorageContainer` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vasa_provider_storage_containers',
                            {
                            'id': id,
                            'protocol_type': protocol_type,
                            })

    def add_vasa_provider_storage_container(self,
                                            id,
                                            add_vasa_provider_storage_container_request_body,
                                            ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  add_vasa_provider_storage_container_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.StorageContainer`
        :param add_vasa_provider_storage_container_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('add_vasa_provider_storage_container',
                            {
                            'id': id,
                            'add_vasa_provider_storage_container_request_body': add_vasa_provider_storage_container_request_body,
                            })

    def remove_vasa_provider_storage_container(self,
                                               id,
                                               storage_container_id,
                                               ):
        """
        No Content

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  storage_container_id: :class:`str`
        :param storage_container_id: Storage container ID
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Storage container not found
        """
        return self._invoke('remove_vasa_provider_storage_container',
                            {
                            'id': id,
                            'storage_container_id': storage_container_id,
                            })

    def update_vasa_provider_storage_container(self,
                                               id,
                                               storage_container_id,
                                               storage_container_update_spec,
                                               ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  storage_container_id: :class:`str`
        :param storage_container_id: Storage container ID
        :type  storage_container_update_spec: :class:`vmware.sddc_manager.model_client.StorageContainerUpdateSpec`
        :param storage_container_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Storage container not found
        """
        return self._invoke('update_vasa_provider_storage_container',
                            {
                            'id': id,
                            'storage_container_id': storage_container_id,
                            'storage_container_update_spec': storage_container_update_spec,
                            })
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vasa_providers.validations'
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


    def validate_vasa_provider_spec(self,
                                    vasa_provider,
                                    ):
        """
        

        :type  vasa_provider: :class:`vmware.sddc_manager.model_client.VasaProvider`
        :param vasa_provider: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_vasa_provider_spec',
                            {
                            'vasa_provider': vasa_provider,
                            })

    def get_vasa_provider_validation(self,
                                     id,
                                     ):
        """
        

        :type  id: :class:`str`
        :param id: The validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Validation ID not found
        """
        return self._invoke('get_vasa_provider_validation',
                            {
                            'id': id,
                            })
class _UsersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vasa_provider_user operation
        get_vasa_provider_user_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vasa_provider_user_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vasa_provider_user_input_value_validator_list = [
        ]
        get_vasa_provider_user_output_validator_list = [
        ]
        get_vasa_provider_user_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vasa-providers/{id}/users',
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

        # properties for add_vasa_provider_user operation
        add_vasa_provider_user_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'add_vasa_provider_user_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaUser')),
        })
        add_vasa_provider_user_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_vasa_provider_user_input_value_validator_list = [
        ]
        add_vasa_provider_user_output_validator_list = [
        ]
        add_vasa_provider_user_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vasa-providers/{id}/users',
            request_body_parameter='add_vasa_provider_user_request_body',
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

        # properties for update_vasa_provider_user operation
        update_vasa_provider_user_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'user_id': type.StringType(),
            'vasa_user_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'VasaUserUpdateSpec'),
        })
        update_vasa_provider_user_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_vasa_provider_user_input_value_validator_list = [
        ]
        update_vasa_provider_user_output_validator_list = [
        ]
        update_vasa_provider_user_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/vasa-providers/{id}/users/{userId}',
            request_body_parameter='vasa_user_update_spec',
            path_variables={
                'id': 'id',
                'user_id': 'userId',
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
            'get_vasa_provider_user': {
                'input_type': get_vasa_provider_user_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaUser'))),
                'errors': get_vasa_provider_user_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': get_vasa_provider_user_input_value_validator_list,
                'output_validator_list': get_vasa_provider_user_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_vasa_provider_user': {
                'input_type': add_vasa_provider_user_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': add_vasa_provider_user_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': add_vasa_provider_user_input_value_validator_list,
                'output_validator_list': add_vasa_provider_user_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_vasa_provider_user': {
                'input_type': update_vasa_provider_user_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': update_vasa_provider_user_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': update_vasa_provider_user_input_value_validator_list,
                'output_validator_list': update_vasa_provider_user_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vasa_provider_user': get_vasa_provider_user_rest_metadata,
            'add_vasa_provider_user': add_vasa_provider_user_rest_metadata,
            'update_vasa_provider_user': update_vasa_provider_user_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vasa_providers.users',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _StorageContainersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vasa_provider_storage_containers operation
        get_vasa_provider_storage_containers_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'protocol_type': type.OptionalType(type.StringType()),
        })
        get_vasa_provider_storage_containers_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vasa_provider_storage_containers_input_value_validator_list = [
        ]
        get_vasa_provider_storage_containers_output_validator_list = [
        ]
        get_vasa_provider_storage_containers_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vasa-providers/{id}/storage-containers',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'protocol_type': 'protocolType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for add_vasa_provider_storage_container operation
        add_vasa_provider_storage_container_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'add_vasa_provider_storage_container_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'StorageContainer')),
        })
        add_vasa_provider_storage_container_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_vasa_provider_storage_container_input_value_validator_list = [
        ]
        add_vasa_provider_storage_container_output_validator_list = [
        ]
        add_vasa_provider_storage_container_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vasa-providers/{id}/storage-containers',
            request_body_parameter='add_vasa_provider_storage_container_request_body',
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

        # properties for remove_vasa_provider_storage_container operation
        remove_vasa_provider_storage_container_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'storage_container_id': type.StringType(),
        })
        remove_vasa_provider_storage_container_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_vasa_provider_storage_container_input_value_validator_list = [
        ]
        remove_vasa_provider_storage_container_output_validator_list = [
        ]
        remove_vasa_provider_storage_container_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/vasa-providers/{id}/storage-containers/{storageContainerId}',
            path_variables={
                'id': 'id',
                'storage_container_id': 'storageContainerId',
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

        # properties for update_vasa_provider_storage_container operation
        update_vasa_provider_storage_container_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'storage_container_id': type.StringType(),
            'storage_container_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'StorageContainerUpdateSpec'),
        })
        update_vasa_provider_storage_container_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_vasa_provider_storage_container_input_value_validator_list = [
        ]
        update_vasa_provider_storage_container_output_validator_list = [
        ]
        update_vasa_provider_storage_container_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/vasa-providers/{id}/storage-containers/{storageContainerId}',
            request_body_parameter='storage_container_update_spec',
            path_variables={
                'id': 'id',
                'storage_container_id': 'storageContainerId',
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
            'get_vasa_provider_storage_containers': {
                'input_type': get_vasa_provider_storage_containers_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'StorageContainer'))),
                'errors': get_vasa_provider_storage_containers_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': get_vasa_provider_storage_containers_input_value_validator_list,
                'output_validator_list': get_vasa_provider_storage_containers_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_vasa_provider_storage_container': {
                'input_type': add_vasa_provider_storage_container_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': add_vasa_provider_storage_container_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': add_vasa_provider_storage_container_input_value_validator_list,
                'output_validator_list': add_vasa_provider_storage_container_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_vasa_provider_storage_container': {
                'input_type': remove_vasa_provider_storage_container_input_type,
                'output_type': type.VoidType(),
                'errors': remove_vasa_provider_storage_container_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400,404]).build(),
                'input_value_validator_list': remove_vasa_provider_storage_container_input_value_validator_list,
                'output_validator_list': remove_vasa_provider_storage_container_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_vasa_provider_storage_container': {
                'input_type': update_vasa_provider_storage_container_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': update_vasa_provider_storage_container_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400,404]).build(),
                'input_value_validator_list': update_vasa_provider_storage_container_input_value_validator_list,
                'output_validator_list': update_vasa_provider_storage_container_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vasa_provider_storage_containers': get_vasa_provider_storage_containers_rest_metadata,
            'add_vasa_provider_storage_container': add_vasa_provider_storage_container_rest_metadata,
            'remove_vasa_provider_storage_container': remove_vasa_provider_storage_container_rest_metadata,
            'update_vasa_provider_storage_container': update_vasa_provider_storage_container_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vasa_providers.storage_containers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_vasa_provider_spec operation
        validate_vasa_provider_spec_input_type = type.StructType('operation-input', {
            'vasa_provider': type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider'),
        })
        validate_vasa_provider_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_vasa_provider_spec_input_value_validator_list = [
        ]
        validate_vasa_provider_spec_output_validator_list = [
        ]
        validate_vasa_provider_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vasa-providers/validations',
            request_body_parameter='vasa_provider',
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

        # properties for get_vasa_provider_validation operation
        get_vasa_provider_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vasa_provider_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vasa_provider_validation_input_value_validator_list = [
        ]
        get_vasa_provider_validation_output_validator_list = [
        ]
        get_vasa_provider_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vasa-providers/validations/{id}',
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
            'validate_vasa_provider_spec': {
                'input_type': validate_vasa_provider_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_vasa_provider_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': validate_vasa_provider_spec_input_value_validator_list,
                'output_validator_list': validate_vasa_provider_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vasa_provider_validation': {
                'input_type': get_vasa_provider_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_vasa_provider_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404]).build(),
                'input_value_validator_list': get_vasa_provider_validation_input_value_validator_list,
                'output_validator_list': get_vasa_provider_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_vasa_provider_spec': validate_vasa_provider_spec_rest_metadata,
            'get_vasa_provider_validation': get_vasa_provider_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vasa_providers.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Users': Users,
        'StorageContainers': StorageContainers,
        'Validations': Validations,
    }

