# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.identity_broker.
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


class SddcManagerOidc(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.identity_broker.sddc_manager_oidc'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SddcManagerOidcStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sddc_ws1b_oidc_info(self):
        """
        Get the SDDC Manager WS1B OIDC Information


        :rtype: :class:`vmware.sddc_manager.model_client.SDDCManagerOidcInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_ws1b_oidc_info', None)
class Prechecks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.identity_broker.prechecks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrechecksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_identity_precheck_result(self,
                                     type=None,
                                     ):
        """
        Get a list precheck result with warnings/errors

        :type  type: :class:`str` or ``None``
        :param type: IDP type for which Precheck needs to be run
        :rtype: :class:`vmware.sddc_manager.model_client.IdentityProviderPrecheckResult` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_identity_precheck_result',
                            {
                            'type': type,
                            })
class _SddcManagerOidcStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_sddc_ws1b_oidc_info operation
        get_sddc_ws1b_oidc_info_input_type = type.StructType('operation-input', {})
        get_sddc_ws1b_oidc_info_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_sddc_ws1b_oidc_info_input_value_validator_list = [
        ]
        get_sddc_ws1b_oidc_info_output_validator_list = [
        ]
        get_sddc_ws1b_oidc_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/identity-broker/sddc-manager-oidc',
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
            'get_sddc_ws1b_oidc_info': {
                'input_type': get_sddc_ws1b_oidc_info_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'SDDCManagerOidcInfo')),
                'errors': get_sddc_ws1b_oidc_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,400,500]).build(),
                'input_value_validator_list': get_sddc_ws1b_oidc_info_input_value_validator_list,
                'output_validator_list': get_sddc_ws1b_oidc_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_sddc_ws1b_oidc_info': get_sddc_ws1b_oidc_info_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.identity_broker.sddc_manager_oidc',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _PrechecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_identity_precheck_result operation
        get_identity_precheck_result_input_type = type.StructType('operation-input', {
            'type': type.OptionalType(type.StringType()),
        })
        get_identity_precheck_result_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_identity_precheck_result_input_value_validator_list = [
        ]
        get_identity_precheck_result_output_validator_list = [
        ]
        get_identity_precheck_result_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/identity-broker/prechecks',
            path_variables={
            },
            query_parameters={
                'type': 'type',
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
            'get_identity_precheck_result': {
                'input_type': get_identity_precheck_result_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'IdentityProviderPrecheckResult')),
                'errors': get_identity_precheck_result_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [500,404]).build(),
                'input_value_validator_list': get_identity_precheck_result_input_value_validator_list,
                'output_validator_list': get_identity_precheck_result_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_identity_precheck_result': get_identity_precheck_result_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.identity_broker.prechecks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'SddcManagerOidc': SddcManagerOidc,
        'Prechecks': Prechecks,
    }

