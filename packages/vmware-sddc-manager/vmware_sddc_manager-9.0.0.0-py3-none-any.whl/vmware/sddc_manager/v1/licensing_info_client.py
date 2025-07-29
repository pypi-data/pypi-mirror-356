# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.licensing_info.
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


class System(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.licensing_info.system'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SystemStub)
        self._VAPI_OPERATION_IDS = {}


    def get_system_licensing_info(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.LicensingInfo` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_system_licensing_info', None)
class Domains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.licensing_info.domains'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DomainsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_domain_licensing_info(self,
                                  id,
                                  ):
        """
        

        :type  id: :class:`str`
        :param id: The domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.LicensingInfo` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_domain_licensing_info',
                            {
                            'id': id,
                            })
class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_licensing_info operation
        get_system_licensing_info_input_type = type.StructType('operation-input', {})
        get_system_licensing_info_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_system_licensing_info_input_value_validator_list = [
        ]
        get_system_licensing_info_output_validator_list = [
        ]
        get_system_licensing_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/licensing-info/system',
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
            'get_system_licensing_info': {
                'input_type': get_system_licensing_info_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'LicensingInfo')),
                'errors': get_system_licensing_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_system_licensing_info_input_value_validator_list,
                'output_validator_list': get_system_licensing_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_licensing_info': get_system_licensing_info_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.licensing_info.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domain_licensing_info operation
        get_domain_licensing_info_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_licensing_info_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_licensing_info_input_value_validator_list = [
        ]
        get_domain_licensing_info_output_validator_list = [
        ]
        get_domain_licensing_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/licensing-info/domains/{id}',
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
            'get_domain_licensing_info': {
                'input_type': get_domain_licensing_info_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'LicensingInfo')),
                'errors': get_domain_licensing_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_domain_licensing_info_input_value_validator_list,
                'output_validator_list': get_domain_licensing_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domain_licensing_info': get_domain_licensing_info_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.licensing_info.domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'System': System,
        'Domains': Domains,
    }

