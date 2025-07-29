# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.network_pools.networks.
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


class IpPools(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.network_pools.networks.ip_pools'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IpPoolsStub)
        self._VAPI_OPERATION_IDS = {}


    def add_ip_pool_to_network_of_network_pool(self,
                                               id,
                                               network_id,
                                               ip_pool,
                                               ):
        """
        Add an IP Pool to a Network of a Network Pool

        :type  id: :class:`str`
        :param id: Id of the networkpoolk
        :type  network_id: :class:`str`
        :param network_id: Id of the network
        :type  ip_pool: :class:`vmware.sddc_manager.model_client.IpPool`
        :param ip_pool: 
        :rtype: :class:`vmware.sddc_manager.model_client.Network` or ``None``
        :return: Add the IP Pool associated with a Network of a Network Pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Either Network Pool ID or Network ID not
            found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. IP range validation failed error
        """
        return self._invoke('add_ip_pool_to_network_of_network_pool',
                            {
                            'id': id,
                            'network_id': network_id,
                            'ip_pool': ip_pool,
                            })

    def delete_ip_pool_from_network_of_network_pool(self,
                                                    id,
                                                    network_id,
                                                    ip_pool,
                                                    ):
        """
        No Content

        :type  id: :class:`str`
        :param id: ID of the networkpool
        :type  network_id: :class:`str`
        :param network_id: ID of the network
        :type  ip_pool: :class:`vmware.sddc_manager.model_client.IpPool`
        :param ip_pool: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Either network or Network pool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Errors due to network/networkpool
            validations failures
        """
        return self._invoke('delete_ip_pool_from_network_of_network_pool',
                            {
                            'id': id,
                            'network_id': network_id,
                            'ip_pool': ip_pool,
                            })
class _IpPoolsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for add_ip_pool_to_network_of_network_pool operation
        add_ip_pool_to_network_of_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'network_id': type.StringType(),
            'ip_pool': type.ReferenceType('vmware.sddc_manager.model_client', 'IpPool'),
        })
        add_ip_pool_to_network_of_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_ip_pool_to_network_of_network_pool_input_value_validator_list = [
        ]
        add_ip_pool_to_network_of_network_pool_output_validator_list = [
        ]
        add_ip_pool_to_network_of_network_pool_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/network-pools/{id}/networks/{networkId}/ip-pools',
            request_body_parameter='ip_pool',
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

        # properties for delete_ip_pool_from_network_of_network_pool operation
        delete_ip_pool_from_network_of_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'network_id': type.StringType(),
            'ip_pool': type.ReferenceType('vmware.sddc_manager.model_client', 'IpPool'),
        })
        delete_ip_pool_from_network_of_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_ip_pool_from_network_of_network_pool_input_value_validator_list = [
        ]
        delete_ip_pool_from_network_of_network_pool_output_validator_list = [
        ]
        delete_ip_pool_from_network_of_network_pool_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/network-pools/{id}/networks/{networkId}/ip-pools',
            request_body_parameter='ip_pool',
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
            'add_ip_pool_to_network_of_network_pool': {
                'input_type': add_ip_pool_to_network_of_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Network')),
                'errors': add_ip_pool_to_network_of_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,400]).build(),
                'input_value_validator_list': add_ip_pool_to_network_of_network_pool_input_value_validator_list,
                'output_validator_list': add_ip_pool_to_network_of_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_ip_pool_from_network_of_network_pool': {
                'input_type': delete_ip_pool_from_network_of_network_pool_input_type,
                'output_type': type.VoidType(),
                'errors': delete_ip_pool_from_network_of_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,400]).build(),
                'input_value_validator_list': delete_ip_pool_from_network_of_network_pool_input_value_validator_list,
                'output_validator_list': delete_ip_pool_from_network_of_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'add_ip_pool_to_network_of_network_pool': add_ip_pool_to_network_of_network_pool_rest_metadata,
            'delete_ip_pool_from_network_of_network_pool': delete_ip_pool_from_network_of_network_pool_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.network_pools.networks.ip_pools',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'IpPools': IpPools,
    }

