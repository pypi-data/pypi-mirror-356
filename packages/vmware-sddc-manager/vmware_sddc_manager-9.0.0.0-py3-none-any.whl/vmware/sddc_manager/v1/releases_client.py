# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.releases.
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


class Domains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.domains'
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


    def get_release_by_domain(self,
                              domain_id,
                              ):
        """
        Get last selected upgrade version for the specified Domain ID.

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID to get target version of the domain
        :rtype: :class:`vmware.sddc_manager.model_client.DomainReleaseView` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_release_by_domain',
                            {
                            'domain_id': domain_id,
                            })

    def delete_release_by_domain_id(self,
                                    domain_id,
                                    ):
        """
        Ok

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_release_by_domain_ID',
                            {
                            'domain_id': domain_id,
                            })

    def update_release_by_domain_id(self,
                                    domain_id,
                                    domain_release=None,
                                    ):
        """
        Ok

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  domain_release: :class:`vmware.sddc_manager.model_client.DomainRelease` or ``None``
        :param domain_release: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Invalid Input
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain or VCF target release not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 422. Unprocessable Entity
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_release_by_domain_ID',
                            {
                            'domain_id': domain_id,
                            'domain_release': domain_release,
                            })

    def get_release_by_domains(self):
        """
        Get last selected upgrade version for all management and workload
        domains.


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDomainReleaseView` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_release_by_domains', None)
class ReleaseComponents(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.release_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ReleaseComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_release_components_by_sku(self,
                                      sku,
                                      release_version=None,
                                      image_type=None,
                                      automated_install=None,
                                      lifecycle_managed_by=None,
                                      release_type=None,
                                      match_with_release_type=None,
                                      ):
        """
        Gets a list of components, the SKU they are part of and the available
        patch versions,per release version. By default it provide release
        components of all the release equal and above 5.x

        :type  sku: :class:`str`
        :param sku: SKU filter, to retrieve only components associated with a specific
            SKU (VCF or VVF)
        :type  release_version: :class:`str` or ``None``
        :param release_version: VCF Release Version
        :type  image_type: :class:`str` or ``None``
        :param image_type: image type for the image you want to retrieve.
        :type  automated_install: :class:`bool` or ``None``
        :param automated_install: Automated Install. If true, list all automated Install product. if
            false or empty, filter will not be applied. Applicable only for VCF
            9.0.0.0 and above releases releases
        :type  lifecycle_managed_by: :class:`str` or ``None``
        :param lifecycle_managed_by: Lifecycle managed by
        :type  release_type: :class:`list` of :class:`str` or ``None``
        :param release_type: List of release types
        :type  match_with_release_type: :class:`str` or ``None``
        :param match_with_release_type: Match with release type for provided releaseVersion
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfReleaseComponentDetail` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_release_components_by_sku',
                            {
                            'sku': sku,
                            'release_version': release_version,
                            'image_type': image_type,
                            'automated_install': automated_install,
                            'lifecycle_managed_by': lifecycle_managed_by,
                            'release_type': release_type,
                            'match_with_release_type': match_with_release_type,
                            })
class System(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.system'
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


    def get_system_release(self):
        """
        Returns release for the lowest deployed VCF version for a domain on the
        environment. If Management domain is ahead of WLD domain, VCF BOM
        version for the WLD domain will be returned. NOTE: This operation is
        not applicable if appliance is in VCF Installer mode.


        :rtype: :class:`vmware.sddc_manager.model_client.Release` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Release Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_system_release', None)
class CustomPatches(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases.custom_patches'
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


    def get_custom_patches_by_sku(self,
                                  sku=None,
                                  release_version=None,
                                  image_type=None,
                                  ):
        """
        Filter applicable patches (current/target VCF/VVF releases) per product
        type

        :type  sku: :class:`str` or ``None``
        :param sku: SKU (VCF or VVF)
        :type  release_version: :class:`str` or ``None``
        :param release_version: Release Version
        :type  image_type: :class:`str` or ``None``
        :param image_type: Image type for the image you want to retrieve.
        :rtype: :class:`vmware.sddc_manager.model_client.CustomPatches` or ``None``
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
        return self._invoke('get_custom_patches_by_sku',
                            {
                            'sku': sku,
                            'release_version': release_version,
                            'image_type': image_type,
                            })
class _DomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_release_by_domain operation
        get_release_by_domain_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        get_release_by_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_release_by_domain_input_value_validator_list = [
        ]
        get_release_by_domain_output_validator_list = [
        ]
        get_release_by_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/domains/{domainId}',
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

        # properties for delete_release_by_domain_ID operation
        delete_release_by_domain_ID_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        delete_release_by_domain_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_release_by_domain_ID_input_value_validator_list = [
        ]
        delete_release_by_domain_ID_output_validator_list = [
        ]
        delete_release_by_domain_ID_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/releases/domains/{domainId}',
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

        # properties for update_release_by_domain_ID operation
        update_release_by_domain_ID_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'domain_release': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DomainRelease')),
        })
        update_release_by_domain_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_release_by_domain_ID_input_value_validator_list = [
        ]
        update_release_by_domain_ID_output_validator_list = [
        ]
        update_release_by_domain_ID_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/releases/domains/{domainId}',
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

        # properties for get_release_by_domains operation
        get_release_by_domains_input_type = type.StructType('operation-input', {})
        get_release_by_domains_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_release_by_domains_input_value_validator_list = [
        ]
        get_release_by_domains_output_validator_list = [
        ]
        get_release_by_domains_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/domains',
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
            'get_release_by_domain': {
                'input_type': get_release_by_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DomainReleaseView')),
                'errors': get_release_by_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_release_by_domain_input_value_validator_list,
                'output_validator_list': get_release_by_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_release_by_domain_ID': {
                'input_type': delete_release_by_domain_ID_input_type,
                'output_type': type.VoidType(),
                'errors': delete_release_by_domain_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': delete_release_by_domain_ID_input_value_validator_list,
                'output_validator_list': delete_release_by_domain_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_release_by_domain_ID': {
                'input_type': update_release_by_domain_ID_input_type,
                'output_type': type.VoidType(),
                'errors': update_release_by_domain_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,422,500]).build(),
                'input_value_validator_list': update_release_by_domain_ID_input_value_validator_list,
                'output_validator_list': update_release_by_domain_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_release_by_domains': {
                'input_type': get_release_by_domains_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDomainReleaseView')),
                'errors': get_release_by_domains_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_release_by_domains_input_value_validator_list,
                'output_validator_list': get_release_by_domains_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_release_by_domain': get_release_by_domain_rest_metadata,
            'delete_release_by_domain_ID': delete_release_by_domain_ID_rest_metadata,
            'update_release_by_domain_ID': update_release_by_domain_ID_rest_metadata,
            'get_release_by_domains': get_release_by_domains_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ReleaseComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_release_components_by_sku operation
        get_release_components_by_sku_input_type = type.StructType('operation-input', {
            'sku': type.StringType(),
            'release_version': type.OptionalType(type.StringType()),
            'image_type': type.OptionalType(type.StringType()),
            'automated_install': type.OptionalType(type.BooleanType()),
            'lifecycle_managed_by': type.OptionalType(type.StringType()),
            'release_type': type.OptionalType(type.ListType(type.StringType())),
            'match_with_release_type': type.OptionalType(type.StringType()),
        })
        get_release_components_by_sku_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_release_components_by_sku_input_value_validator_list = [
        ]
        get_release_components_by_sku_output_validator_list = [
        ]
        get_release_components_by_sku_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/{sku}/release-components',
            path_variables={
                'sku': 'sku',
            },
            query_parameters={
                'release_version': 'releaseVersion',
                'image_type': 'imageType',
                'automated_install': 'automatedInstall',
                'lifecycle_managed_by': 'lifecycleManagedBy',
                'release_type': 'releaseType',
                'match_with_release_type': 'matchWithReleaseType',
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
            'get_release_components_by_sku': {
                'input_type': get_release_components_by_sku_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfReleaseComponentDetail')),
                'errors': get_release_components_by_sku_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': get_release_components_by_sku_input_value_validator_list,
                'output_validator_list': get_release_components_by_sku_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_release_components_by_sku': get_release_components_by_sku_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.release_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_release operation
        get_system_release_input_type = type.StructType('operation-input', {})
        get_system_release_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_system_release_input_value_validator_list = [
        ]
        get_system_release_output_validator_list = [
        ]
        get_system_release_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/system',
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
            'get_system_release': {
                'input_type': get_system_release_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Release')),
                'errors': get_system_release_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_system_release_input_value_validator_list,
                'output_validator_list': get_system_release_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_release': get_system_release_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CustomPatchesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_custom_patches_by_sku operation
        get_custom_patches_by_sku_input_type = type.StructType('operation-input', {
            'sku': type.OptionalType(type.StringType()),
            'release_version': type.OptionalType(type.StringType()),
            'image_type': type.OptionalType(type.StringType()),
        })
        get_custom_patches_by_sku_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_custom_patches_by_sku_input_value_validator_list = [
        ]
        get_custom_patches_by_sku_output_validator_list = [
        ]
        get_custom_patches_by_sku_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/custom-patches',
            path_variables={
            },
            query_parameters={
                'sku': 'sku',
                'release_version': 'releaseVersion',
                'image_type': 'imageType',
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
            'get_custom_patches_by_sku': {
                'input_type': get_custom_patches_by_sku_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CustomPatches')),
                'errors': get_custom_patches_by_sku_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,422,404,400]).build(),
                'input_value_validator_list': get_custom_patches_by_sku_input_value_validator_list,
                'output_validator_list': get_custom_patches_by_sku_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_custom_patches_by_sku': get_custom_patches_by_sku_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases.custom_patches',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Domains': Domains,
        'ReleaseComponents': ReleaseComponents,
        'System': System,
        'CustomPatches': CustomPatches,
        'domains': 'vmware.sddc_manager.v1.releases.domains_client.StubFactory',
    }

