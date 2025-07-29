# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.users.
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


class Ui(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.users.ui'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UiStub)
        self._VAPI_OPERATION_IDS = {}


    def get_ui_users(self):
        """
        Retrieve a list of users assigned access via SDDC Manager


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUser` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_ui_users', None)
class _UiStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ui_users operation
        get_ui_users_input_type = type.StructType('operation-input', {})
        get_ui_users_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_ui_users_input_value_validator_list = [
        ]
        get_ui_users_output_validator_list = [
        ]
        get_ui_users_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/users/ui',
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
            'get_ui_users': {
                'input_type': get_ui_users_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUser')),
                'errors': get_ui_users_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': get_ui_users_input_value_validator_list,
                'output_validator_list': get_ui_users_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_ui_users': get_ui_users_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.users.ui',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Ui': Ui,
        'local': 'vmware.sddc_manager.v1.users.local_client.StubFactory',
    }

