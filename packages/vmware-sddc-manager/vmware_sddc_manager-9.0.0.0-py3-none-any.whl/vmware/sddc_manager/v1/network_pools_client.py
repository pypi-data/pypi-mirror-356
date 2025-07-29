# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.network_pools.
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


class Networks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.network_pools.networks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_networks_of_network_pool(self,
                                     id,
                                     ):
        """
        Get the Networks that are part of a Network Pool

        :type  id: :class:`str`
        :param id: ID for Networkpool to get the networks from
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNetwork` or ``None``
        :return: Networks for referenced network pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Network pool not found
        """
        return self._invoke('get_networks_of_network_pool',
                            {
                            'id': id,
                            })

    def get_network_of_network_pool(self,
                                    id,
                                    network_id,
                                    ):
        """
        Get a Network that is part of a Network Pool

        :type  id: :class:`str`
        :param id: Id of the Network pool
        :type  network_id: :class:`str`
        :param network_id: Id of the Network
        :rtype: :class:`vmware.sddc_manager.model_client.Network` or ``None``
        :return: Network for referenced network pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Networkpool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_network_of_network_pool',
                            {
                            'id': id,
                            'network_id': network_id,
                            })
class _NetworksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_networks_of_network_pool operation
        get_networks_of_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_networks_of_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_networks_of_network_pool_input_value_validator_list = [
        ]
        get_networks_of_network_pool_output_validator_list = [
        ]
        get_networks_of_network_pool_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/network-pools/{id}/networks',
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

        # properties for get_network_of_network_pool operation
        get_network_of_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'network_id': type.StringType(),
        })
        get_network_of_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_network_of_network_pool_input_value_validator_list = [
        ]
        get_network_of_network_pool_output_validator_list = [
        ]
        get_network_of_network_pool_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/network-pools/{id}/networks/{networkId}',
            path_variables={
                'id': 'id',
                'network_id': 'networkId',
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
            'get_networks_of_network_pool': {
                'input_type': get_networks_of_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNetwork')),
                'errors': get_networks_of_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_networks_of_network_pool_input_value_validator_list,
                'output_validator_list': get_networks_of_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_network_of_network_pool': {
                'input_type': get_network_of_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Network')),
                'errors': get_network_of_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_network_of_network_pool_input_value_validator_list,
                'output_validator_list': get_network_of_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_networks_of_network_pool': get_networks_of_network_pool_rest_metadata,
            'get_network_of_network_pool': get_network_of_network_pool_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.network_pools.networks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Networks': Networks,
        'networks': 'vmware.sddc_manager.v1.network_pools.networks_client.StubFactory',
    }

