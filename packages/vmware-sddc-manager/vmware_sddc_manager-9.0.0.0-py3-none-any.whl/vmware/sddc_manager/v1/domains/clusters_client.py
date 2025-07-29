# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.clusters.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.clusters.queries'
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


    def post_cluster_query(self,
                           domain_id,
                           cluster_name,
                           cluster_criterion,
                           ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  cluster_name: :class:`str`
        :param cluster_name: Cluster Name
        :type  cluster_criterion: :class:`vmware.sddc_manager.model_client.ClusterCriterion`
        :param cluster_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('post_cluster_query',
                            {
                            'domain_id': domain_id,
                            'cluster_name': cluster_name,
                            'cluster_criterion': cluster_criterion,
                            })

    def post_clusters_query(self,
                            domain_id,
                            cluster_criterion,
                            ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  cluster_criterion: :class:`vmware.sddc_manager.model_client.ClusterCriterion`
        :param cluster_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('post_clusters_query',
                            {
                            'domain_id': domain_id,
                            'cluster_criterion': cluster_criterion,
                            })

    def get_cluster_query_response(self,
                                   domain_id,
                                   cluster_name,
                                   query_id,
                                   ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  cluster_name: :class:`str`
        :param cluster_name: Cluster Name
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_query_response',
                            {
                            'domain_id': domain_id,
                            'cluster_name': cluster_name,
                            'query_id': query_id,
                            })

    def get_clusters_query_response(self,
                                    domain_id,
                                    query_id,
                                    ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Query Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_clusters_query_response',
                            {
                            'domain_id': domain_id,
                            'query_id': query_id,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.clusters.criteria'
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


    def get_cluster_criteria(self,
                             domain_id,
                             ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfClusterCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_cluster_criteria',
                            {
                            'domain_id': domain_id,
                            })

    def get_cluster_criterion(self,
                              domain_id,
                              name,
                              ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  name: :class:`str`
        :param name: Criteria Name
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Criterion Not Found
        """
        return self._invoke('get_cluster_criterion',
                            {
                            'domain_id': domain_id,
                            'name': name,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for post_cluster_query operation
        post_cluster_query_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'cluster_name': type.StringType(),
            'cluster_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterCriterion'),
        })
        post_cluster_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        post_cluster_query_input_value_validator_list = [
        ]
        post_cluster_query_output_validator_list = [
        ]
        post_cluster_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{domainId}/clusters/{clusterName}/queries',
            request_body_parameter='cluster_criterion',
            path_variables={
                'domain_id': 'domainId',
                'cluster_name': 'clusterName',
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

        # properties for post_clusters_query operation
        post_clusters_query_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'cluster_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterCriterion'),
        })
        post_clusters_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        post_clusters_query_input_value_validator_list = [
        ]
        post_clusters_query_output_validator_list = [
        ]
        post_clusters_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{domainId}/clusters/queries',
            request_body_parameter='cluster_criterion',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_cluster_query_response operation
        get_cluster_query_response_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'cluster_name': type.StringType(),
            'query_id': type.StringType(),
        })
        get_cluster_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_query_response_input_value_validator_list = [
        ]
        get_cluster_query_response_output_validator_list = [
        ]
        get_cluster_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/clusters/{clusterName}/queries/{queryId}',
            path_variables={
                'domain_id': 'domainId',
                'cluster_name': 'clusterName',
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

        # properties for get_clusters_query_response operation
        get_clusters_query_response_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'query_id': type.StringType(),
        })
        get_clusters_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_clusters_query_response_input_value_validator_list = [
        ]
        get_clusters_query_response_output_validator_list = [
        ]
        get_clusters_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/clusters/queries/{queryId}',
            path_variables={
                'domain_id': 'domainId',
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
            'post_cluster_query': {
                'input_type': post_cluster_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterQueryResponse')),
                'errors': post_cluster_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': post_cluster_query_input_value_validator_list,
                'output_validator_list': post_cluster_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'post_clusters_query': {
                'input_type': post_clusters_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterQueryResponse')),
                'errors': post_clusters_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': post_clusters_query_input_value_validator_list,
                'output_validator_list': post_clusters_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster_query_response': {
                'input_type': get_cluster_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterQueryResponse')),
                'errors': get_cluster_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_cluster_query_response_input_value_validator_list,
                'output_validator_list': get_cluster_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_clusters_query_response': {
                'input_type': get_clusters_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterQueryResponse')),
                'errors': get_clusters_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': get_clusters_query_response_input_value_validator_list,
                'output_validator_list': get_clusters_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'post_cluster_query': post_cluster_query_rest_metadata,
            'post_clusters_query': post_clusters_query_rest_metadata,
            'get_cluster_query_response': get_cluster_query_response_rest_metadata,
            'get_clusters_query_response': get_clusters_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.clusters.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_criteria operation
        get_cluster_criteria_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        get_cluster_criteria_error_dict = {}
        get_cluster_criteria_input_value_validator_list = [
        ]
        get_cluster_criteria_output_validator_list = [
        ]
        get_cluster_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/clusters/criteria',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_cluster_criterion operation
        get_cluster_criterion_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'name': type.StringType(),
        })
        get_cluster_criterion_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_criterion_input_value_validator_list = [
        ]
        get_cluster_criterion_output_validator_list = [
        ]
        get_cluster_criterion_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/clusters/criteria/{name}',
            path_variables={
                'domain_id': 'domainId',
                'name': 'name',
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
            'get_cluster_criteria': {
                'input_type': get_cluster_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfClusterCriterion')),
                'errors': get_cluster_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_cluster_criteria_input_value_validator_list,
                'output_validator_list': get_cluster_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster_criterion': {
                'input_type': get_cluster_criterion_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterCriterion')),
                'errors': get_cluster_criterion_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404]).build(),
                'input_value_validator_list': get_cluster_criterion_input_value_validator_list,
                'output_validator_list': get_cluster_criterion_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_criteria': get_cluster_criteria_rest_metadata,
            'get_cluster_criterion': get_cluster_criterion_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.clusters.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
        'Criteria': Criteria,
    }

