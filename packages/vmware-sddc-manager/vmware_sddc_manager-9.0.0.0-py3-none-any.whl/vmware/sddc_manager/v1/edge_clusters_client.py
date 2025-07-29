# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.edge_clusters.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.edge_clusters.validations'
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


    def validate_edge_cluster_update_spec(self,
                                          id,
                                          edge_cluster_update_spec,
                                          ):
        """
        

        :type  id: :class:`str`
        :param id: NSX Edge cluster id
        :type  edge_cluster_update_spec: :class:`vmware.sddc_manager.model_client.EdgeClusterUpdateSpec`
        :param edge_cluster_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_edge_cluster_update_spec',
                            {
                            'id': id,
                            'edge_cluster_update_spec': edge_cluster_update_spec,
                            })

    def validate_edge_cluster_creation_spec(self,
                                            edge_cluster_creation_spec,
                                            ):
        """
        

        :type  edge_cluster_creation_spec: :class:`vmware.sddc_manager.model_client.EdgeClusterCreationSpec`
        :param edge_cluster_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_edge_cluster_creation_spec',
                            {
                            'edge_cluster_creation_spec': edge_cluster_creation_spec,
                            })

    def get_edge_cluster_validation_by_id(self,
                                          id,
                                          ):
        """
        

        :type  id: :class:`str`
        :param id: The validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_edge_cluster_validation_by_ID',
                            {
                            'id': id,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.edge_clusters.criteria'
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


    def get_edge_cluster_query_criteria(self,
                                        edge_cluster_id,
                                        ):
        """
        

        :type  edge_cluster_id: :class:`str`
        :param edge_cluster_id: Edge Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfEdgeClusterNsxtEntityCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Page` 
            HTTP status code - 404. Resource Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_edge_cluster_query_criteria',
                            {
                            'edge_cluster_id': edge_cluster_id,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_edge_cluster_update_spec operation
        validate_edge_cluster_update_spec_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'edge_cluster_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'EdgeClusterUpdateSpec'),
        })
        validate_edge_cluster_update_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_edge_cluster_update_spec_input_value_validator_list = [
        ]
        validate_edge_cluster_update_spec_output_validator_list = [
        ]
        validate_edge_cluster_update_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/edge-clusters/{id}/validations',
            request_body_parameter='edge_cluster_update_spec',
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

        # properties for validate_edge_cluster_creation_spec operation
        validate_edge_cluster_creation_spec_input_type = type.StructType('operation-input', {
            'edge_cluster_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'EdgeClusterCreationSpec'),
        })
        validate_edge_cluster_creation_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_edge_cluster_creation_spec_input_value_validator_list = [
        ]
        validate_edge_cluster_creation_spec_output_validator_list = [
        ]
        validate_edge_cluster_creation_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/edge-clusters/validations',
            request_body_parameter='edge_cluster_creation_spec',
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

        # properties for get_edge_cluster_validation_by_ID operation
        get_edge_cluster_validation_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_edge_cluster_validation_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_edge_cluster_validation_by_ID_input_value_validator_list = [
        ]
        get_edge_cluster_validation_by_ID_output_validator_list = [
        ]
        get_edge_cluster_validation_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/edge-clusters/validations/{id}',
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
            'validate_edge_cluster_update_spec': {
                'input_type': validate_edge_cluster_update_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_edge_cluster_update_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': validate_edge_cluster_update_spec_input_value_validator_list,
                'output_validator_list': validate_edge_cluster_update_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate_edge_cluster_creation_spec': {
                'input_type': validate_edge_cluster_creation_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_edge_cluster_creation_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': validate_edge_cluster_creation_spec_input_value_validator_list,
                'output_validator_list': validate_edge_cluster_creation_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_edge_cluster_validation_by_ID': {
                'input_type': get_edge_cluster_validation_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_edge_cluster_validation_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': get_edge_cluster_validation_by_ID_input_value_validator_list,
                'output_validator_list': get_edge_cluster_validation_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_edge_cluster_update_spec': validate_edge_cluster_update_spec_rest_metadata,
            'validate_edge_cluster_creation_spec': validate_edge_cluster_creation_spec_rest_metadata,
            'get_edge_cluster_validation_by_ID': get_edge_cluster_validation_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.edge_clusters.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_edge_cluster_query_criteria operation
        get_edge_cluster_query_criteria_input_type = type.StructType('operation-input', {
            'edge_cluster_id': type.StringType(),
        })
        get_edge_cluster_query_criteria_error_dict = {
            'vmware.sddc_manager.model.page':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Page'),
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_edge_cluster_query_criteria_input_value_validator_list = [
        ]
        get_edge_cluster_query_criteria_output_validator_list = [
        ]
        get_edge_cluster_query_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/edge-clusters/{edgeClusterId}/criteria',
            path_variables={
                'edge_cluster_id': 'edgeClusterId',
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
            'get_edge_cluster_query_criteria': {
                'input_type': get_edge_cluster_query_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfEdgeClusterNsxtEntityCriterion')),
                'errors': get_edge_cluster_query_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Page'), [404]).add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_edge_cluster_query_criteria_input_value_validator_list,
                'output_validator_list': get_edge_cluster_query_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_edge_cluster_query_criteria': get_edge_cluster_query_criteria_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.edge_clusters.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
        'Criteria': Criteria,
    }

