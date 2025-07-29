# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.resource_certificates.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.resource_certificates.validations'
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


    def validate_resource_certificates(self,
                                       id,
                                       validate_resource_certificates_request_body,
                                       ):
        """
        Validate resource certificates

        :type  id: :class:`str`
        :param id: Domain ID
        :type  validate_resource_certificates_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.ResourceCertificateSpec`
        :param validate_resource_certificates_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.CertificateValidationTask` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('validate_resource_certificates',
                            {
                            'id': id,
                            'validate_resource_certificates_request_body': validate_resource_certificates_request_body,
                            })

    def get_resource_certificates_validation_by_id(self,
                                                   id,
                                                   validation_id,
                                                   ):
        """
        Get the resource certificate validation result

        :type  id: :class:`str`
        :param id: Domain ID
        :type  validation_id: :class:`str`
        :param validation_id: Validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCertificate` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_resource_certificates_validation_by_ID',
                            {
                            'id': id,
                            'validation_id': validation_id,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_resource_certificates operation
        validate_resource_certificates_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'validate_resource_certificates_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceCertificateSpec')),
        })
        validate_resource_certificates_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_resource_certificates_input_value_validator_list = [
        ]
        validate_resource_certificates_output_validator_list = [
        ]
        validate_resource_certificates_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/domains/{id}/resource-certificates/validations',
            request_body_parameter='validate_resource_certificates_request_body',
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

        # properties for get_resource_certificates_validation_by_ID operation
        get_resource_certificates_validation_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'validation_id': type.StringType(),
        })
        get_resource_certificates_validation_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_resource_certificates_validation_by_ID_input_value_validator_list = [
        ]
        get_resource_certificates_validation_by_ID_output_validator_list = [
        ]
        get_resource_certificates_validation_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/resource-certificates/validations/{validationId}',
            path_variables={
                'id': 'id',
                'validation_id': 'validationId',
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
            'validate_resource_certificates': {
                'input_type': validate_resource_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CertificateValidationTask')),
                'errors': validate_resource_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': validate_resource_certificates_input_value_validator_list,
                'output_validator_list': validate_resource_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_resource_certificates_validation_by_ID': {
                'input_type': get_resource_certificates_validation_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCertificate')),
                'errors': get_resource_certificates_validation_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_resource_certificates_validation_by_ID_input_value_validator_list,
                'output_validator_list': get_resource_certificates_validation_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_resource_certificates': validate_resource_certificates_rest_metadata,
            'get_resource_certificates_validation_by_ID': get_resource_certificates_validation_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.resource_certificates.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
    }

