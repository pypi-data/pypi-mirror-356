# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools.validations'
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


    def validate_ip_pool(self,
                         nsxt_ip_address_pool_validation_spec,
                         ):
        """
        

        :type  nsxt_ip_address_pool_validation_spec: :class:`vmware.sddc_manager.model_client.NsxtIpAddressPoolValidationSpec`
        :param nsxt_ip_address_pool_validation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        """
        return self._invoke('validate_ip_pool',
                            {
                            'nsxt_ip_address_pool_validation_spec': nsxt_ip_address_pool_validation_spec,
                            })

    def get_validation_result(self,
                              id,
                              ):
        """
        

        :type  id: :class:`str`
        :param id: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        """
        return self._invoke('get_validation_result',
                            {
                            'id': id,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_ip_pool operation
        validate_ip_pool_input_type = type.StructType('operation-input', {
            'nsxt_ip_address_pool_validation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtIpAddressPoolValidationSpec'),
        })
        validate_ip_pool_error_dict = {}
        validate_ip_pool_input_value_validator_list = [
        ]
        validate_ip_pool_output_validator_list = [
        ]
        validate_ip_pool_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsxt-clusters/ip-address-pools/validations',
            request_body_parameter='nsxt_ip_address_pool_validation_spec',
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

        # properties for get_validation_result operation
        get_validation_result_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_validation_result_error_dict = {}
        get_validation_result_input_value_validator_list = [
        ]
        get_validation_result_output_validator_list = [
        ]
        get_validation_result_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/ip-address-pools/validations/{id}',
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
            'validate_ip_pool': {
                'input_type': validate_ip_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_ip_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': validate_ip_pool_input_value_validator_list,
                'output_validator_list': validate_ip_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_validation_result': {
                'input_type': get_validation_result_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_validation_result_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_validation_result_input_value_validator_list,
                'output_validator_list': get_validation_result_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_ip_pool': validate_ip_pool_rest_metadata,
            'get_validation_result': get_validation_result_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
    }

