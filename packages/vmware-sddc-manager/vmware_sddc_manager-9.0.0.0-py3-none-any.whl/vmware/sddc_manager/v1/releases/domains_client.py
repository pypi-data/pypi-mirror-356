# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.releases.domains.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.domains.validations'
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


    def validate_release_by_domain_id(self,
                                      domain_id,
                                      domain_release=None,
                                      ):
        """
        Validate the selected target upgrade release BOM or custom BOM for the
        specified Domain ID

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  domain_release: :class:`vmware.sddc_manager.model_client.DomainRelease` or ``None``
        :param domain_release: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('validate_release_by_domain_ID',
                            {
                            'domain_id': domain_id,
                            'domain_release': domain_release,
                            })

    def get_domain_release_view_validation(self,
                                           validation_id,
                                           ):
        """
        Monitor the progress of domain target state validation task by it's
        Validation ID.

        :type  validation_id: :class:`str`
        :param validation_id: Domain Target State Validation ID
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_domain_release_view_validation',
                            {
                            'validation_id': validation_id,
                            })
class FutureReleases(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.domains.future_releases'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FutureReleasesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_future_releases(self,
                            domain_id,
                            ):
        """
        Returns all known to the system future target versions for a domain. If
        some of them are not allowed (e.g. stepping stone), then message
        explains the reason. If the domain does not have a product configured
        at that point, then that product will not be included in the BOM or
        patch bundle list in each release. NOTE: This operation is not
        applicable if appliance is in VCF Installer mode.

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID to get all feature target versions for
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDomainFutureRelease` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain Not Found.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_future_releases',
                            {
                            'domain_id': domain_id,
                            })
class CustomPatches(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.domains.custom_patches'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CustomPatchesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_custom_patches(self,
                           domain_id,
                           vcf_release=None,
                           product_type=None,
                           ):
        """
        Filter applicable patches (current/target VCF releases) per product
        type per domain. NOTE: This operation is not applicable if appliance is
        in VCF Installer mode.

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  vcf_release: :class:`str` or ``None``
        :param vcf_release: VCF Release
        :type  product_type: :class:`str` or ``None``
        :param product_type: Product Type
        :rtype: :class:`vmware.sddc_manager.model_client.FlexibleProductPatches` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 422. Unprocessable Entity
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_custom_patches',
                            {
                            'domain_id': domain_id,
                            'vcf_release': vcf_release,
                            'product_type': product_type,
                            })
class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_release_by_domain_ID operation
        validate_release_by_domain_ID_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'domain_release': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DomainRelease')),
        })
        validate_release_by_domain_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_release_by_domain_ID_input_value_validator_list = [
        ]
        validate_release_by_domain_ID_output_validator_list = [
        ]
        validate_release_by_domain_ID_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/releases/domains/{domainId}/validations',
            request_body_parameter='domain_release',
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

        # properties for get_domain_release_view_validation operation
        get_domain_release_view_validation_input_type = type.StructType('operation-input', {
            'validation_id': type.StringType(),
        })
        get_domain_release_view_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_release_view_validation_input_value_validator_list = [
        ]
        get_domain_release_view_validation_output_validator_list = [
        ]
        get_domain_release_view_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/domains/validations/{validationId}',
            path_variables={
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
            'validate_release_by_domain_ID': {
                'input_type': validate_release_by_domain_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_release_by_domain_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_release_by_domain_ID_input_value_validator_list,
                'output_validator_list': validate_release_by_domain_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_domain_release_view_validation': {
                'input_type': get_domain_release_view_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_domain_release_view_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_domain_release_view_validation_input_value_validator_list,
                'output_validator_list': get_domain_release_view_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_release_by_domain_ID': validate_release_by_domain_ID_rest_metadata,
            'get_domain_release_view_validation': get_domain_release_view_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.domains.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _FutureReleasesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_future_releases operation
        get_future_releases_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        get_future_releases_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_future_releases_input_value_validator_list = [
        ]
        get_future_releases_output_validator_list = [
        ]
        get_future_releases_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/domains/{domainId}/future-releases',
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

        operations = {
            'get_future_releases': {
                'input_type': get_future_releases_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDomainFutureRelease')),
                'errors': get_future_releases_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_future_releases_input_value_validator_list,
                'output_validator_list': get_future_releases_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_future_releases': get_future_releases_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.domains.future_releases',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CustomPatchesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_custom_patches operation
        get_custom_patches_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'vcf_release': type.OptionalType(type.StringType()),
            'product_type': type.OptionalType(type.StringType()),
        })
        get_custom_patches_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_custom_patches_input_value_validator_list = [
        ]
        get_custom_patches_output_validator_list = [
        ]
        get_custom_patches_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/domains/{domainId}/custom-patches',
            path_variables={
                'domain_id': 'domainId',
            },
            query_parameters={
                'vcf_release': 'vcfRelease',
                'product_type': 'productType',
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
            'get_custom_patches': {
                'input_type': get_custom_patches_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'FlexibleProductPatches')),
                'errors': get_custom_patches_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,422,404,400]).build(),
                'input_value_validator_list': get_custom_patches_input_value_validator_list,
                'output_validator_list': get_custom_patches_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_custom_patches': get_custom_patches_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.domains.custom_patches',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Validations': Validations,
        'FutureReleases': FutureReleases,
        'CustomPatches': CustomPatches,
    }

