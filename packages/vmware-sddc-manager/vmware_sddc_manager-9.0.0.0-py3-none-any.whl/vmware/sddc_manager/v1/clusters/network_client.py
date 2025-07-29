# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.clusters.network.
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


class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.network.queries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _QueriesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cluster_network_configuration(self,
                                          id,
                                          cluster_network_configuration_criterion,
                                          ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  cluster_network_configuration_criterion: :class:`vmware.sddc_manager.model_client.ClusterNetworkConfigurationCriterion`
        :param cluster_network_configuration_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterNetworkConfigurationQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_network_configuration',
                            {
                            'id': id,
                            'cluster_network_configuration_criterion': cluster_network_configuration_criterion,
                            })

    def get_cluster_network_configuration_query_response(self,
                                                         id,
                                                         query_id,
                                                         ):
        """
        The response retrieved is only applicable for pure L2 domain clusters

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterNetworkConfigurationQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_network_configuration_query_response',
                            {
                            'id': id,
                            'query_id': query_id,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.network.criteria'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CriteriaStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cluster_network_configuration_criteria(self,
                                                   id,
                                                   ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfClusterNetworkConfigurationCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_cluster_network_configuration_criteria',
                            {
                            'id': id,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_network_configuration operation
        get_cluster_network_configuration_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'cluster_network_configuration_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterNetworkConfigurationCriterion'),
        })
        get_cluster_network_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_network_configuration_input_value_validator_list = [
        ]
        get_cluster_network_configuration_output_validator_list = [
        ]
        get_cluster_network_configuration_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{id}/network/queries',
            request_body_parameter='cluster_network_configuration_criterion',
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

        # properties for get_cluster_network_configuration_query_response operation
        get_cluster_network_configuration_query_response_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'query_id': type.StringType(),
        })
        get_cluster_network_configuration_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_network_configuration_query_response_input_value_validator_list = [
        ]
        get_cluster_network_configuration_query_response_output_validator_list = [
        ]
        get_cluster_network_configuration_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/network/queries/{queryId}',
            path_variables={
                'id': 'id',
                'query_id': 'queryId',
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
            'get_cluster_network_configuration': {
                'input_type': get_cluster_network_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterNetworkConfigurationQueryResponse')),
                'errors': get_cluster_network_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_cluster_network_configuration_input_value_validator_list,
                'output_validator_list': get_cluster_network_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster_network_configuration_query_response': {
                'input_type': get_cluster_network_configuration_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterNetworkConfigurationQueryResponse')),
                'errors': get_cluster_network_configuration_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_cluster_network_configuration_query_response_input_value_validator_list,
                'output_validator_list': get_cluster_network_configuration_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_network_configuration': get_cluster_network_configuration_rest_metadata,
            'get_cluster_network_configuration_query_response': get_cluster_network_configuration_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.network.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_network_configuration_criteria operation
        get_cluster_network_configuration_criteria_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_network_configuration_criteria_error_dict = {}
        get_cluster_network_configuration_criteria_input_value_validator_list = [
        ]
        get_cluster_network_configuration_criteria_output_validator_list = [
        ]
        get_cluster_network_configuration_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/network/criteria',
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
            'get_cluster_network_configuration_criteria': {
                'input_type': get_cluster_network_configuration_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfClusterNetworkConfigurationCriterion')),
                'errors': get_cluster_network_configuration_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_cluster_network_configuration_criteria_input_value_validator_list,
                'output_validator_list': get_cluster_network_configuration_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_network_configuration_criteria': get_cluster_network_configuration_criteria_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.network.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
        'Criteria': Criteria,
    }

