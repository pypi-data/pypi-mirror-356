# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.nsx_alb_clusters.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsx_alb_clusters.validations'
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


    def validate_alb_cluster_creation_spec(self,
                                           nsx_alb_controller_cluster_spec,
                                           skip_compatibility_check=None,
                                           ):
        """
        

        :type  nsx_alb_controller_cluster_spec: :class:`vmware.sddc_manager.model_client.NsxAlbControllerClusterSpec`
        :param nsx_alb_controller_cluster_spec: 
        :type  skip_compatibility_check: :class:`bool` or ``None``
        :param skip_compatibility_check: Pass an optional Skip compatibility checks
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_ALB_cluster_creation_spec',
                            {
                            'nsx_alb_controller_cluster_spec': nsx_alb_controller_cluster_spec,
                            'skip_compatibility_check': skip_compatibility_check,
                            })
class FormFactors(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsx_alb_clusters.form_factors'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FormFactorsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_alb_clusters_form_factors(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.ALBControllerNodeFormFactors` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_ALB_clusters_form_factors', None)
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_ALB_cluster_creation_spec operation
        validate_ALB_cluster_creation_spec_input_type = type.StructType('operation-input', {
            'nsx_alb_controller_cluster_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxAlbControllerClusterSpec'),
            'skip_compatibility_check': type.OptionalType(type.BooleanType()),
        })
        validate_ALB_cluster_creation_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_ALB_cluster_creation_spec_input_value_validator_list = [
        ]
        validate_ALB_cluster_creation_spec_output_validator_list = [
        ]
        validate_ALB_cluster_creation_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsx-alb-clusters/validations',
            request_body_parameter='nsx_alb_controller_cluster_spec',
            path_variables={
            },
            query_parameters={
                'skip_compatibility_check': 'skipCompatibilityCheck',
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
            'validate_ALB_cluster_creation_spec': {
                'input_type': validate_ALB_cluster_creation_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_ALB_cluster_creation_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': validate_ALB_cluster_creation_spec_input_value_validator_list,
                'output_validator_list': validate_ALB_cluster_creation_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_ALB_cluster_creation_spec': validate_ALB_cluster_creation_spec_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsx_alb_clusters.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _FormFactorsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ALB_clusters_form_factors operation
        get_ALB_clusters_form_factors_input_type = type.StructType('operation-input', {})
        get_ALB_clusters_form_factors_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_ALB_clusters_form_factors_input_value_validator_list = [
        ]
        get_ALB_clusters_form_factors_output_validator_list = [
        ]
        get_ALB_clusters_form_factors_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsx-alb-clusters/form-factors',
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
            'get_ALB_clusters_form_factors': {
                'input_type': get_ALB_clusters_form_factors_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ALBControllerNodeFormFactors')),
                'errors': get_ALB_clusters_form_factors_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_ALB_clusters_form_factors_input_value_validator_list,
                'output_validator_list': get_ALB_clusters_form_factors_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_ALB_clusters_form_factors': get_ALB_clusters_form_factors_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsx_alb_clusters.form_factors',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
        'FormFactors': FormFactors,
        'validations': 'vmware.sddc_manager.v1.nsx_alb_clusters.validations_client.StubFactory',
    }

