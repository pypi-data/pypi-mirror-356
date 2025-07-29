# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.users.local.
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


class Admin(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.users.local.admin'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AdminStub)
        self._VAPI_OPERATION_IDS = {}


    def get_local_account(self):
        """
        Get information on the local account


        :rtype: :class:`vmware.sddc_manager.model_client.LocalUser` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_local_account', None)

    def disable_local_account(self):
        """
        No content


        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('disable_local_account', None)

    def update_local_user_password(self,
                                   local_account_password_info,
                                   ):
        """
        No content

        :type  local_account_password_info: :class:`vmware.sddc_manager.model_client.LocalAccountPasswordInfo`
        :param local_account_password_info: 
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('update_local_user_password',
                            {
                            'local_account_password_info': local_account_password_info,
                            })
class _AdminStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_local_account operation
        get_local_account_input_type = type.StructType('operation-input', {})
        get_local_account_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_local_account_input_value_validator_list = [
        ]
        get_local_account_output_validator_list = [
        ]
        get_local_account_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/users/local/admin',
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

        # properties for disable_local_account operation
        disable_local_account_input_type = type.StructType('operation-input', {})
        disable_local_account_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        disable_local_account_input_value_validator_list = [
        ]
        disable_local_account_output_validator_list = [
        ]
        disable_local_account_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/users/local/admin',
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

        # properties for update_local_user_password operation
        update_local_user_password_input_type = type.StructType('operation-input', {
            'local_account_password_info': type.ReferenceType('vmware.sddc_manager.model_client', 'LocalAccountPasswordInfo'),
        })
        update_local_user_password_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        update_local_user_password_input_value_validator_list = [
        ]
        update_local_user_password_output_validator_list = [
        ]
        update_local_user_password_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/users/local/admin',
            request_body_parameter='local_account_password_info',
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
            'get_local_account': {
                'input_type': get_local_account_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'LocalUser')),
                'errors': get_local_account_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': get_local_account_input_value_validator_list,
                'output_validator_list': get_local_account_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'disable_local_account': {
                'input_type': disable_local_account_input_type,
                'output_type': type.VoidType(),
                'errors': disable_local_account_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500]).build(),
                'input_value_validator_list': disable_local_account_input_value_validator_list,
                'output_validator_list': disable_local_account_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_local_user_password': {
                'input_type': update_local_user_password_input_type,
                'output_type': type.VoidType(),
                'errors': update_local_user_password_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [500]).build(),
                'input_value_validator_list': update_local_user_password_input_value_validator_list,
                'output_validator_list': update_local_user_password_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_local_account': get_local_account_rest_metadata,
            'disable_local_account': disable_local_account_rest_metadata,
            'update_local_user_password': update_local_user_password_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.users.local.admin',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Admin': Admin,
    }

