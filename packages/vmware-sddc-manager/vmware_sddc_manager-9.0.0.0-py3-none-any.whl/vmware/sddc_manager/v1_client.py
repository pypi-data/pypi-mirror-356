# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.
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


class CompatibilityMatrices(VapiInterface):
    """
    The following API operation(s) are not included in the SDK yet, but can be
    accessed via HTTP requests to the REST API: 
    
    * /v1/compatibility-matrices PUT
    
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compatibility_matrices'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CompatibilityMatricesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compatibility_matrices(self):
        """
        Get Compatibility Matrices


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCompatibilityMatrix` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compatibility_matrices', None)

    def get_compatibility_matrix(self,
                                 compatibility_matrix_source,
                                 ):
        """
        Get Compatibility Matrix

        :type  compatibility_matrix_source: :class:`str`
        :param compatibility_matrix_source: Source of compatibility data
        :rtype: :class:`vmware.sddc_manager.model_client.CompatibilityMatrix` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compatibility_matrix',
                            {
                            'compatibility_matrix_source': compatibility_matrix_source,
                            })
class CertificateAuthorities(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.certificate_authorities'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CertificateAuthoritiesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_certificate_authorities(self):
        """
        Get certificate authorities information


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCertificateAuthority` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_certificate_authorities', None)

    def create_certificate_authority(self,
                                     certificate_authority_creation_spec,
                                     ):
        """
        Ok

        :type  certificate_authority_creation_spec: :class:`vmware.sddc_manager.model_client.CertificateAuthorityCreationSpec`
        :param certificate_authority_creation_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('create_certificate_authority',
                            {
                            'certificate_authority_creation_spec': certificate_authority_creation_spec,
                            })

    def configure_certificate_authority(self,
                                        certificate_authority_creation_spec,
                                        ):
        """
        Ok

        :type  certificate_authority_creation_spec: :class:`vmware.sddc_manager.model_client.CertificateAuthorityCreationSpec`
        :param certificate_authority_creation_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('configure_certificate_authority',
                            {
                            'certificate_authority_creation_spec': certificate_authority_creation_spec,
                            })

    def get_certificate_authority_by_id(self,
                                        id,
                                        ):
        """
        Get certificate authority information

        :type  id: :class:`str`
        :param id: The CA type
        :rtype: :class:`vmware.sddc_manager.model_client.CertificateAuthority` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_certificate_authority_by_id',
                            {
                            'id': id,
                            })

    def remove_certificate_authority(self,
                                     id,
                                     ):
        """
        No Content

        :type  id: :class:`str`
        :param id: The CA type
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('remove_certificate_authority',
                            {
                            'id': id,
                            })
class VcfManagementComponents(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_management_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcfManagementComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_management_components(self):
        """
        Get the details of VCF Management Components containing each
        component's FQDN, deployment type, and deployment status


        :rtype: :class:`vmware.sddc_manager.model_client.VcfManagementComponents` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_vcf_management_components', None)

    def deploy_vcf_management_components(self,
                                         vcf_management_components_spec,
                                         ):
        """
        Triggers VCF Management Components deployment workflow from SDDC
        Manager and returns a URL in the headers to track the operation status

        :type  vcf_management_components_spec: :class:`vmware.sddc_manager.model_client.VcfManagementComponentsSpec`
        :param vcf_management_components_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Task` 
            HTTP status code - 403. Forbidden
        """
        return self._invoke('deploy_vcf_management_components',
                            {
                            'vcf_management_components_spec': vcf_management_components_spec,
                            })
class VasaProviders(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vasa_providers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VasaProvidersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vasa_providers(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVasaProvider` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vasa_providers', None)

    def add_vasa_provider(self,
                          vasa_provider,
                          ):
        """
        

        :type  vasa_provider: :class:`vmware.sddc_manager.model_client.VasaProvider`
        :param vasa_provider: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('add_vasa_provider',
                            {
                            'vasa_provider': vasa_provider,
                            })

    def get_vasa_provider(self,
                          id,
                          ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        """
        return self._invoke('get_vasa_provider',
                            {
                            'id': id,
                            })

    def remove_vasa_provider(self,
                             id,
                             ):
        """
        No Content

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('remove_vasa_provider',
                            {
                            'id': id,
                            })

    def update_vasa_provider(self,
                             id,
                             vasa_provider_update_spec,
                             ):
        """
        

        :type  id: :class:`str`
        :param id: VASA Provider ID
        :type  vasa_provider_update_spec: :class:`vmware.sddc_manager.model_client.VasaProviderUpdateSpec`
        :param vasa_provider_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.VasaProvider` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VASA Provider not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_vasa_provider',
                            {
                            'id': id,
                            'vasa_provider_update_spec': vasa_provider_update_spec,
                            })
class Users(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.users'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UsersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_users(self):
        """
        Get a list of all users


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUser` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_users', None)

    def add_users(self,
                  add_users_request_body,
                  ):
        """
        Add list of users

        :type  add_users_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.User`
        :param add_users_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUser` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('add_users',
                            {
                            'add_users_request_body': add_users_request_body,
                            })

    def remove_user(self,
                    id,
                    ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of the user
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. User not found
        """
        return self._invoke('remove_user',
                            {
                            'id': id,
                            })
class Upgrades(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgrades'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UpgradesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_upgrades(self,
                     status=None,
                     bundle_id=None,
                     bundle_type=None,
                     ):
        """
        Retrieve a list of upgrades

        :type  status: :class:`str` or ``None``
        :param status: Status of the upgrades you want to retrieve
        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: Bundle Id for the upgrade
        :type  bundle_type: :class:`str` or ``None``
        :param bundle_type: Bundle type of the upgrades you want to retrieve
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUpgrade` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Upgrade Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Invalid State
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_upgrades',
                            {
                            'status': status,
                            'bundle_id': bundle_id,
                            'bundle_type': bundle_type,
                            })

    def perform_upgrade(self,
                        upgrade_spec,
                        ):
        """
        Schedule/Trigger Upgrade of a Resource. Ex: Resource can be DOMAIN,
        CLUSTER etc. Performing upgrades are supported on VMware Cloud
        Foundation BOM resources and above. Supports scheduling/triggering of
        only 'parallel' upgrades and only Resource 'cluster' that are managed
        using both vSphere Lifecycle Manager Baselines and vSphere Lifecycle
        Manager Images in the same request.

        :type  upgrade_spec: :class:`vmware.sddc_manager.model_client.UpgradeSpec`
        :param upgrade_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Operation not allowed
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 424. Failed Dependency
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('perform_upgrade',
                            {
                            'upgrade_spec': upgrade_spec,
                            })

    def get_upgrade_by_id(self,
                          upgrade_id,
                          ):
        """
        Retrieve an upgrade by ID

        :type  upgrade_id: :class:`str`
        :param upgrade_id: 
        :rtype: :class:`vmware.sddc_manager.model_client.Upgrade` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Upgrade Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_upgrade_by_id',
                            {
                            'upgrade_id': upgrade_id,
                            })

    def update_upgrade_schedule(self,
                                upgrade_id,
                                upgrade_commit_spec,
                                ):
        """
        Commit/Reschedule an existing upgrade. It moves the upgrade from DRAFT
        state to SCHEDULED state and/or changes the upgrade scheduled
        date/time.

        :type  upgrade_id: :class:`str`
        :param upgrade_id: 
        :type  upgrade_commit_spec: :class:`vmware.sddc_manager.model_client.UpgradeCommitSpec`
        :param upgrade_commit_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Upgrade` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Upgrade Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Invalid Input
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Invalid State
        """
        return self._invoke('update_upgrade_schedule',
                            {
                            'upgrade_id': upgrade_id,
                            'upgrade_commit_spec': upgrade_commit_spec,
                            })
class Tokens(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.tokens'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TokensStub)
        self._VAPI_OPERATION_IDS = {}


    def create_token(self,
                     token_creation_spec,
                     ):
        """
        Creates access token and refresh token for user access

        :type  token_creation_spec: :class:`vmware.sddc_manager.model_client.TokenCreationSpec`
        :param token_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.TokenPair` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('create_token',
                            {
                            'token_creation_spec': token_creation_spec,
                            })
class ResourceWarnings(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.resource_warnings'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceWarningsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_resource_warnings(self,
                              resource_type=None,
                              resource_ids=None,
                              resource_names=None,
                              ):
        """
        

        :type  resource_type: :class:`str` or ``None``
        :param resource_type: Resource type
        :type  resource_ids: :class:`list` of :class:`str` or ``None``
        :param resource_ids: Resource IDs
        :type  resource_names: :class:`list` of :class:`str` or ``None``
        :param resource_names: Resource Names
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfResourceWarning` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_resource_warnings',
                            {
                            'resource_type': resource_type,
                            'resource_ids': resource_ids,
                            'resource_names': resource_names,
                            })

    def create_resource_warning(self,
                                resource_warning_creation_spec,
                                ):
        """
        

        :type  resource_warning_creation_spec: :class:`vmware.sddc_manager.model_client.ResourceWarningCreationSpec`
        :param resource_warning_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ResourceWarning` or ``None``
        :return: Created
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('create_resource_warning',
                            {
                            'resource_warning_creation_spec': resource_warning_creation_spec,
                            })

    def get_resource_warning(self,
                             id,
                             ):
        """
        

        :type  id: :class:`str`
        :param id: 
        :rtype: :class:`vmware.sddc_manager.model_client.ResourceWarning` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Resource Warning not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_resource_warning',
                            {
                            'id': id,
                            })
class ProductVersionCatalogs(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.product_version_catalogs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProductVersionCatalogsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_product_version_catalog_content(self):
        """
        Get product version catalog content. There should be only one valid
        product version catalog in the System.


        :rtype: :class:`vmware.sddc_manager.model_client.ProductVersionCatalog` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_product_version_catalog_content', None)

    def upload_product_version_catalog_with_signature(self,
                                                      product_version_catalog_with_signature_spec,
                                                      ):
        """
        Upload product version catalog and corresponding signature file.

        :type  product_version_catalog_with_signature_spec: :class:`vmware.sddc_manager.model_client.ProductVersionCatalogWithSignatureSpec`
        :param product_version_catalog_with_signature_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ProductVersionCatalogUploadTask` or ``None``
        :return: Product version catalog upload operation has been accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('upload_product_version_catalog_with_signature',
                            {
                            'product_version_catalog_with_signature_spec': product_version_catalog_with_signature_spec,
                            })

    def update_product_version_catalog_patches(self,
                                               product_version_catalog_with_signature_spec,
                                               ):
        """
        Update product version catalog patches with a corresponding signature
        file.

        :type  product_version_catalog_with_signature_spec: :class:`vmware.sddc_manager.model_client.ProductVersionCatalogWithSignatureSpec`
        :param product_version_catalog_with_signature_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ProductVersionCatalogUploadTask` or ``None``
        :return: Product version catalog update operation has been accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_product_version_catalog_patches',
                            {
                            'product_version_catalog_with_signature_spec': product_version_catalog_with_signature_spec,
                            })
class ProductVersionCatalog(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.product_version_catalog'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProductVersionCatalogStub)
        self._VAPI_OPERATION_IDS = {}


    def get_product_version_catalog(self):
        """
        Get product version catalog. There should be only one valid product
        version catalog in the System.


        :rtype: :class:`vmware.sddc_manager.model_client.ProductVersionCatalog` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Product Version catalog Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 410. This API is no longer supported from VCF
            9.0.0.0+ releases. Please refer to /v1/product-version-catalogs
            instead.
        """
        return self._invoke('get_product_version_catalog', None)

    def upload_product_version_catalog(self,
                                       product_version_catalog,
                                       ):
        """
        Accepted

        :type  product_version_catalog: :class:`vmware.sddc_manager.model_client.ProductVersionCatalog`
        :param product_version_catalog: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 410. This API is no longer supported from VCF
            9.0.0.0+ releases. Please refer to /v1/product-version-catalogs
            instead.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('upload_product_version_catalog',
                            {
                            'product_version_catalog': product_version_catalog,
                            })
class ProductBinaries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.product_binaries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProductBinariesStub)
        self._VAPI_OPERATION_IDS = {}


    def upload_product_binary(self,
                              product_binary_upload_spec,
                              ):
        """
        Upload the product binaries to SDDC Manager. The API looks up the
        product binaries in the product version catalog based on provided
        inputs and updates the LCM database.

        :type  product_binary_upload_spec: :class:`vmware.sddc_manager.model_client.ProductBinaryUploadSpec`
        :param product_binary_upload_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 406. Product type is not supported
        """
        return self._invoke('upload_product_binary',
                            {
                            'product_binary_upload_spec': product_binary_upload_spec,
                            })
class Personalities(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.personalities'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PersonalitiesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_personalities(self,
                          base_os_version=None,
                          add_on_name=None,
                          add_on_vendor_name=None,
                          component_name=None,
                          component_vendor_name=None,
                          personality_name=None,
                          type=None,
                          size=None,
                          page=None,
                          sort=None,
                          ):
        """
        Get the Personalities which are available via depot access.

        :type  base_os_version: :class:`str` or ``None``
        :param base_os_version: Base OS version
        :type  add_on_name: :class:`str` or ``None``
        :param add_on_name: Add-on name
        :type  add_on_vendor_name: :class:`str` or ``None``
        :param add_on_vendor_name: Add-on vendor name
        :type  component_name: :class:`str` or ``None``
        :param component_name: Component name
        :type  component_vendor_name: :class:`str` or ``None``
        :param component_vendor_name: Component vendor name
        :type  personality_name: :class:`str` or ``None``
        :param personality_name: Personality name
        :type  type: :class:`str` or ``None``
        :param type: Personality type
        :type  size: :class:`long` or ``None``
        :param size: Size of the page to retrieve. Default page size is 2147483647.
            Optional
        :type  page: :class:`long` or ``None``
        :param page: Page number to retrieve. Default page is 1. Optional
        :type  sort: :class:`str` or ``None``
        :param sort: Optional sort to apply to result. List can contain values among:
            personalityName, addOnName, addOnVendorName, baseOSVersion.
            Multiple values supported (comma-separated) or multiple occurrences
            for different sort directions (asc/desc). Example:
            sort=personalityName,desc
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfPersonality` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_personalities',
                            {
                            'base_os_version': base_os_version,
                            'add_on_name': add_on_name,
                            'add_on_vendor_name': add_on_vendor_name,
                            'component_name': component_name,
                            'component_vendor_name': component_vendor_name,
                            'personality_name': personality_name,
                            'type': type,
                            'size': size,
                            'page': page,
                            'sort': sort,
                            })

    def upload_personality(self,
                           personality_upload_spec,
                           ):
        """
        Upload Personality to SDDC Manager.

        :type  personality_upload_spec: :class:`vmware.sddc_manager.model_client.PersonalityUploadSpec`
        :param personality_upload_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('upload_personality',
                            {
                            'personality_upload_spec': personality_upload_spec,
                            })

    def delete_personality(self,
                           personality_id=None,
                           personality_name=None,
                           ):
        """
        OK

        :type  personality_id: :class:`str` or ``None``
        :param personality_id: The personality id
        :type  personality_name: :class:`str` or ``None``
        :param personality_name: The personality name
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Personality by name or ID Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Invalid Input
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_personality',
                            {
                            'personality_id': personality_id,
                            'personality_name': personality_name,
                            })

    def get_personality(self,
                        personality_id,
                        ):
        """
        Get the Personality for id

        :type  personality_id: :class:`str`
        :param personality_id: Personality ID
        :rtype: :class:`vmware.sddc_manager.model_client.Personality` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Personality Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_personality',
                            {
                            'personality_id': personality_id,
                            })
class NsxAlbClusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsx_alb_clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NsxAlbClustersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_alb_clusters(self,
                         domain_id=None,
                         ):
        """
        

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Domain Id
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNsxALBCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_ALB_clusters',
                            {
                            'domain_id': domain_id,
                            })

    def create_alb_cluster(self,
                           nsx_alb_controller_cluster_spec,
                           skip_compatibility_check=None,
                           ):
        """
        

        :type  nsx_alb_controller_cluster_spec: :class:`vmware.sddc_manager.model_client.NsxAlbControllerClusterSpec`
        :param nsx_alb_controller_cluster_spec: 
        :type  skip_compatibility_check: :class:`bool` or ``None``
        :param skip_compatibility_check: Pass an optional Skip compatibility checks
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('create_ALB_cluster',
                            {
                            'nsx_alb_controller_cluster_spec': nsx_alb_controller_cluster_spec,
                            'skip_compatibility_check': skip_compatibility_check,
                            })

    def get_alb_cluster(self,
                        id,
                        ):
        """
        

        :type  id: :class:`str`
        :param id: ALB Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.NsxALBCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. ALB Cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_ALB_cluster',
                            {
                            'id': id,
                            })

    def delete_alb_cluster(self,
                           id,
                           force_delete=None,
                           ):
        """
        

        :type  id: :class:`str`
        :param id: ALB Cluster ID
        :type  force_delete: :class:`bool` or ``None``
        :param force_delete: Force Delete ALB Cluster
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. ALB Cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('delete_ALB_cluster',
                            {
                            'id': id,
                            'force_delete': force_delete,
                            })
class NetworkPools(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.network_pools'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworkPoolsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_network_pool(self):
        """
        Get the Network Pools


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNetworkPool` or ``None``
        :return: Referenced network pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Referenced network pool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_network_pool', None)

    def create_network_pool(self,
                            network_pool,
                            ):
        """
        Create a Network Pool

        :type  network_pool: :class:`vmware.sddc_manager.model_client.NetworkPool`
        :param network_pool: 
        :rtype: :class:`vmware.sddc_manager.model_client.NetworkPool` or ``None``
        :return: The newly created network pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Errors due to network pool validations
            failures
        """
        return self._invoke('create_network_pool',
                            {
                            'network_pool': network_pool,
                            })

    def get_network_pool_by_id(self,
                               id,
                               ):
        """
        Get a Network Pool by ID, if it exists

        :type  id: :class:`str`
        :param id: ID of the network pool to fetch
        :rtype: :class:`vmware.sddc_manager.model_client.NetworkPool` or ``None``
        :return: Referenced network pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Referenced network pool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_network_pool_by_ID',
                            {
                            'id': id,
                            })

    def delete_network_pool(self,
                            id,
                            force=None,
                            ):
        """
        The specification of the deleted network pool

        :type  id: :class:`str`
        :param id: ID of the network pool
        :type  force: :class:`bool` or ``None``
        :param force: Force removal of Network Pool
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Referenced network pool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Hosts are still associated with NetworkPool
        """
        return self._invoke('delete_network_pool',
                            {
                            'id': id,
                            'force': force,
                            })

    def update_network_pool(self,
                            id,
                            network_pool_update_spec,
                            ):
        """
        Update a Network Pool by ID, if it exists

        :type  id: :class:`str`
        :param id: Network Pool ID
        :type  network_pool_update_spec: :class:`vmware.sddc_manager.model_client.NetworkPoolUpdateSpec`
        :param network_pool_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.NetworkPool` or ``None``
        :return: Network Pool update completed
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Network Pool not found
        """
        return self._invoke('update_network_pool',
                            {
                            'id': id,
                            'network_pool_update_spec': network_pool_update_spec,
                            })
class Manifests(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.manifests'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ManifestsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_manifest(self):
        """
        Get manifest. There should be only one valid manifest in the System.


        :rtype: :class:`vmware.sddc_manager.model_client.Manifest` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Manifest Not Found
        """
        return self._invoke('get_manifest', None)

    def save_manifest(self,
                      manifest,
                      ):
        """
        Accepted

        :type  manifest: :class:`vmware.sddc_manager.model_client.Manifest`
        :param manifest: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Invalid State
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('save_manifest',
                            {
                            'manifest': manifest,
                            })
class LicenseKeys(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.license_keys'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LicenseKeysStub)
        self._VAPI_OPERATION_IDS = {}


    def get_license_keys(self,
                         product_type=None,
                         license_key_status=None,
                         license_unit=None,
                         product_version=None,
                         ):
        """
        

        :type  product_type: :class:`list` of :class:`str` or ``None``
        :param product_type: Type of a Product
        :type  license_key_status: :class:`list` of :class:`str` or ``None``
        :param license_key_status: Status of a License Key
        :type  license_unit: :class:`list` of :class:`str` or ``None``
        :param license_unit: Unit of a license
        :type  product_version: :class:`str` or ``None``
        :param product_version: Product Version, gets the license keys matching the major version
            of the product version
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfLicenseKey` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_license_keys',
                            {
                            'product_type': product_type,
                            'license_key_status': license_key_status,
                            'license_unit': license_unit,
                            'product_version': product_version,
                            })

    def add_license_key(self,
                        license_key,
                        ):
        """
        Created

        :type  license_key: :class:`vmware.sddc_manager.model_client.LicenseKey`
        :param license_key: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('add_license_key',
                            {
                            'license_key': license_key,
                            })

    def update_license_key(self,
                           license_key_or_id,
                           license_key_update_spec,
                           ):
        """
        Ok

        :type  license_key_or_id: :class:`str`
        :param license_key_or_id: license key or ID of the LicenseKey
        :type  license_key_update_spec: :class:`vmware.sddc_manager.model_client.LicenseKeyUpdateSpec`
        :param license_key_update_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. License key with ID / LicenseKey does not
            exist
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_license_key',
                            {
                            'license_key_or_id': license_key_or_id,
                            'license_key_update_spec': license_key_update_spec,
                            })

    def get_license_key(self,
                        key,
                        ):
        """
        

        :type  key: :class:`str`
        :param key: The 29 alpha numeric character license key with hyphens
        :rtype: :class:`vmware.sddc_manager.model_client.LicenseKey` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. License key not found
        """
        return self._invoke('get_license_key',
                            {
                            'key': key,
                            })

    def remove_license_key(self,
                           key,
                           ):
        """
        No content

        :type  key: :class:`str`
        :param key: The 29 alpha numeric character license key with hyphens
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('remove_license_key',
                            {
                            'key': key,
                            })
class IdentityProviders(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.identity_providers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IdentityProvidersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_identity_providers(self):
        """
        Get a list of all identity providers


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfIdentityProvider` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_identity_providers', None)

    def add_external_identity_provider(self,
                                       identity_provider_spec,
                                       ):
        """
        Created

        :type  identity_provider_spec: :class:`vmware.sddc_manager.model_client.IdentityProviderSpec`
        :param identity_provider_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('add_external_identity_provider',
                            {
                            'identity_provider_spec': identity_provider_spec,
                            })

    def get_identity_provider_by_id(self,
                                    id,
                                    ):
        """
        Get a specific identity provider using its id

        :type  id: :class:`str`
        :param id: ID of the Identity Provider
        :rtype: :class:`vmware.sddc_manager.model_client.IdentityProvider` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_identity_provider_by_id',
                            {
                            'id': id,
                            })

    def delete_external_identity_provider(self,
                                          id,
                                          ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Identity Provider not found
        """
        return self._invoke('delete_external_identity_provider',
                            {
                            'id': id,
                            })

    def update_external_identity_provider(self,
                                          id,
                                          identity_provider_spec,
                                          ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :type  identity_provider_spec: :class:`vmware.sddc_manager.model_client.IdentityProviderSpec`
        :param identity_provider_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Identity Provider not found
        """
        return self._invoke('update_external_identity_provider',
                            {
                            'id': id,
                            'identity_provider_spec': identity_provider_spec,
                            })
class Hosts(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HostsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_hosts(self,
                  fqdn=None,
                  status=None,
                  domain_id=None,
                  cluster_id=None,
                  networkpool_id=None,
                  storage_type=None,
                  datastore_name=None,
                  size=None,
                  page=None,
                  ):
        """
        

        :type  fqdn: :class:`str` or ``None``
        :param fqdn: Filter by: fully qualified host name. Optional
        :type  status: :class:`str` or ``None``
        :param status: Filter by: status of the Host. List can contain values among:
            ASSIGNED, UNASSIGNED_USEABLE, UNASSIGNED_UNUSEABLE. Optional
        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Filter by: ID of the Domain. Optional
        :type  cluster_id: :class:`str` or ``None``
        :param cluster_id: Filter by: ID of the Cluster. Optional
        :type  networkpool_id: :class:`str` or ``None``
        :param networkpool_id: Filter by: ID of the Network Pool. Optional
        :type  storage_type: :class:`str` or ``None``
        :param storage_type: Filter by: type of the Storage. List can contain values among:
            VSAN, VSAN_ESA, VSAN_REMOTE, VSAN_MAX, NFS, VMFS_FC, VVOL, VMFS.
            Optional
        :type  datastore_name: :class:`str` or ``None``
        :param datastore_name: Filter by: name of Datastore. Optional
        :type  size: :class:`long` or ``None``
        :param size: Size of the page to retrieve.
        :type  page: :class:`long` or ``None``
        :param page: Page number to retrieve.
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfHost` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_hosts',
                            {
                            'fqdn': fqdn,
                            'status': status,
                            'domain_id': domain_id,
                            'cluster_id': cluster_id,
                            'networkpool_id': networkpool_id,
                            'storage_type': storage_type,
                            'datastore_name': datastore_name,
                            'size': size,
                            'page': page,
                            })

    def commission_hosts(self,
                         commission_hosts_request_body,
                         ):
        """
        

        :type  commission_hosts_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.HostCommissionSpec`
        :param commission_hosts_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('commission_hosts',
                            {
                            'commission_hosts_request_body': commission_hosts_request_body,
                            })

    def decommission_hosts(self,
                           decommission_hosts_request_body,
                           ):
        """
        

        :type  decommission_hosts_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.HostDecommissionSpec`
        :param decommission_hosts_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('decommission_hosts',
                            {
                            'decommission_hosts_request_body': decommission_hosts_request_body,
                            })

    def get_host(self,
                 id,
                 ):
        """
        

        :type  id: :class:`str`
        :param id: 
        :rtype: :class:`vmware.sddc_manager.model_client.Host` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_host',
                            {
                            'id': id,
                            })
class EdgeClusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.edge_clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EdgeClustersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_edge_clusters(self,
                          cluster_id=None,
                          ):
        """
        

        :type  cluster_id: :class:`str` or ``None``
        :param cluster_id: Pass an optional vSphere Cluster ID to fetch edge clusters
            associated with the vSphere Cluster
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfEdgeCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_edge_clusters',
                            {
                            'cluster_id': cluster_id,
                            })

    def create_edge_cluster(self,
                            edge_cluster_creation_spec,
                            ):
        """
        

        :type  edge_cluster_creation_spec: :class:`vmware.sddc_manager.model_client.EdgeClusterCreationSpec`
        :param edge_cluster_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('create_edge_cluster',
                            {
                            'edge_cluster_creation_spec': edge_cluster_creation_spec,
                            })

    def get_edge_cluster(self,
                         id,
                         ):
        """
        

        :type  id: :class:`str`
        :param id: Edge Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.EdgeCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Edge Cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_edge_cluster',
                            {
                            'id': id,
                            })

    def update_edge_cluster(self,
                            id,
                            edge_cluster_update_spec,
                            ):
        """
        

        :type  id: :class:`str`
        :param id: Edge Cluster ID
        :type  edge_cluster_update_spec: :class:`vmware.sddc_manager.model_client.EdgeClusterUpdateSpec`
        :param edge_cluster_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 501. Not Implemented
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_edge_cluster',
                            {
                            'id': id,
                            'edge_cluster_update_spec': edge_cluster_update_spec,
                            })
class Domains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains'
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


    def get_domains(self,
                    type=None,
                    ):
        """
        

        :type  type: :class:`str` or ``None``
        :param type: The type of the domain
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDomain` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_domains',
                            {
                            'type': type,
                            })

    def create_domain(self,
                      domain_creation_spec,
                      ):
        """
        

        :type  domain_creation_spec: :class:`vmware.sddc_manager.model_client.DomainCreationSpec`
        :param domain_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('create_domain',
                            {
                            'domain_creation_spec': domain_creation_spec,
                            })

    def get_domain(self,
                   id,
                   ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.Domain` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_domain',
                            {
                            'id': id,
                            })

    def delete_domain(self,
                      id,
                      ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('delete_domain',
                            {
                            'id': id,
                            })

    def update_domain(self,
                      id,
                      domain_update_spec,
                      ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :type  domain_update_spec: :class:`vmware.sddc_manager.model_client.DomainUpdateSpec`
        :param domain_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('update_domain',
                            {
                            'id': id,
                            'domain_update_spec': domain_update_spec,
                            })
class ConfigDriftReconciliations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.config_drift_reconciliations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConfigDriftReconciliationsStub)
        self._VAPI_OPERATION_IDS = {}


    def reconcile_configs(self,
                          config_drift_apply_spec,
                          ):
        """
        For selective reconciliation, provide a config spec.

        :type  config_drift_apply_spec: :class:`vmware.sddc_manager.model_client.ConfigDriftApplySpec`
        :param config_drift_apply_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('reconcile_configs',
                            {
                            'config_drift_apply_spec': config_drift_apply_spec,
                            })

    def get_reconciliation_task(self,
                                task_id,
                                ):
        """
        Get config reconciliation task associated with the given task Id

        :type  task_id: :class:`str`
        :param task_id: Task Id
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Reconciliation task not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_reconciliation_task',
                            {
                            'task_id': task_id,
                            })
class Clusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClustersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_clusters(self,
                     is_stretched=None,
                     is_image_based=None,
                     domain_id=None,
                     ):
        """
        

        :type  is_stretched: :class:`bool` or ``None``
        :param is_stretched: Is cluster vSAN stretched
        :type  is_image_based: :class:`bool` or ``None``
        :param is_image_based: Is cluster managed using vSphere lifecycle Manager Images
        :type  domain_id: :class:`str` or ``None``
        :param domain_id: ID of the Domain
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_clusters',
                            {
                            'is_stretched': is_stretched,
                            'is_image_based': is_image_based,
                            'domain_id': domain_id,
                            })

    def create_cluster(self,
                       cluster_creation_spec,
                       ):
        """
        

        :type  cluster_creation_spec: :class:`vmware.sddc_manager.model_client.ClusterCreationSpec`
        :param cluster_creation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('create_cluster',
                            {
                            'cluster_creation_spec': cluster_creation_spec,
                            })

    def get_cluster(self,
                    id,
                    ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.Cluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster',
                            {
                            'id': id,
                            })

    def delete_cluster(self,
                       id,
                       force=None,
                       ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  force: :class:`bool` or ``None``
        :param force: Force deletion of the cluster. Please note when passed true,
            deletion will ignore vCenter Server connection issues and could
            possible leave cluster related resources in the vCenter Server if a
            connection cannot be established.
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('delete_cluster',
                            {
                            'id': id,
                            'force': force,
                            })

    def update_cluster(self,
                       id,
                       cluster_update_spec,
                       ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  cluster_update_spec: :class:`vmware.sddc_manager.model_client.ClusterUpdateSpec`
        :param cluster_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('update_cluster',
                            {
                            'id': id,
                            'cluster_update_spec': cluster_update_spec,
                            })
class Bundles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.bundles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BundlesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_bundles(self,
                    product_type=None,
                    is_compliant=None,
                    bundle_type=None,
                    ):
        """
        Get all Bundles. Returns uploaded bundles and bundles available via
        depot access.

        :type  product_type: :class:`str` or ``None``
        :param product_type: The type of the product
        :type  is_compliant: :class:`bool` or ``None``
        :param is_compliant: Is compliant with the current VCF version?
        :type  bundle_type: :class:`str` or ``None``
        :param bundle_type: The type of the bundle
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfBundle` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_bundles',
                            {
                            'product_type': product_type,
                            'is_compliant': is_compliant,
                            'bundle_type': bundle_type,
                            })

    def upload_bundle(self,
                      bundle_upload_spec,
                      ):
        """
        Upload Bundle to SDDC Manager or VCF Installer. This is useful when you
        do not have internet connectivity for downloading bundles from the
        online depot to SDDC Manager or VCF Installer. The Bundles are manually
        downloaded from Depot using Bundle Transfer utility. This API is no
        longer supported from VCF 9.0. Please refer to POST v1/product-binaries
        instead.

        :type  bundle_upload_spec: :class:`vmware.sddc_manager.model_client.BundleUploadSpec`
        :param bundle_upload_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 410. This API is no longer supported from VCF
            9.0. Please refer to POST v1/product-binaries instead.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('upload_bundle',
                            {
                            'bundle_upload_spec': bundle_upload_spec,
                            })

    def get_bundle(self,
                   id,
                   ):
        """
        Get a Bundle

        :type  id: :class:`str`
        :param id: Bundle ID
        :rtype: :class:`vmware.sddc_manager.model_client.Bundle` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Bundle Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_bundle',
                            {
                            'id': id,
                            })

    def delete_bundle(self,
                      id,
                      binary_files_only=None,
                      ):
        """
        No Content

        :type  id: :class:`str`
        :param id: Bundle ID
        :type  binary_files_only: :class:`bool` or ``None``
        :param binary_files_only: binaryFilesOnly, if true, only binary files from storage will be
            deleted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_bundle',
                            {
                            'id': id,
                            'binary_files_only': binary_files_only,
                            })

    def start_bundle_download_by_id(self,
                                    id,
                                    bundle_update_spec,
                                    ):
        """
        Update a Bundle for scheduling/triggering download. If download is
        started, this can be used to cancel a download. Only one download can
        triggered for a Bundle.

        :type  id: :class:`str`
        :param id: Bundle ID
        :type  bundle_update_spec: :class:`vmware.sddc_manager.model_client.BundleUpdateSpec`
        :param bundle_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('start_bundle_download_by_ID',
                            {
                            'id': id,
                            'bundle_update_spec': bundle_update_spec,
                            })
class AlbClusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.alb_clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AlbClustersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_avi_lb_clusters(self,
                            domain_id=None,
                            ):
        """
        

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Domain Id
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfALBCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_avi_LB_clusters',
                            {
                            'domain_id': domain_id,
                            })

    def deploy_alb_cluster(self,
                           alb_controller_cluster_spec,
                           skip_compatibility_check=None,
                           ):
        """
        

        :type  alb_controller_cluster_spec: :class:`vmware.sddc_manager.model_client.AlbControllerClusterSpec`
        :param alb_controller_cluster_spec: 
        :type  skip_compatibility_check: :class:`bool` or ``None``
        :param skip_compatibility_check: Pass an optional Skip compatibility checks
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('deploy_ALB_cluster',
                            {
                            'alb_controller_cluster_spec': alb_controller_cluster_spec,
                            'skip_compatibility_check': skip_compatibility_check,
                            })

    def get_avi_lb_cluster(self,
                           id,
                           ):
        """
        

        :type  id: :class:`str`
        :param id: ALB Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.NsxALBCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. ALB Cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_avi_LB_cluster',
                            {
                            'id': id,
                            })

    def undeploy_alb_cluster(self,
                             id,
                             force_delete=None,
                             ):
        """
        

        :type  id: :class:`str`
        :param id: ALB Cluster ID
        :type  force_delete: :class:`bool` or ``None``
        :param force_delete: Force Delete ALB Cluster
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. ALB Cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('undeploy_ALB_cluster',
                            {
                            'id': id,
                            'force_delete': force_delete,
                            })
class VsanHcl(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vsan_hcl'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VsanHclStub)
        self._VAPI_OPERATION_IDS = {}


    def download_vsan_hcl(self):
        """
        Download vSAN HCL if online connectivity is available. Timestamp of
        vSAN HCL on SDDC Manager is checked with what is available online
        before download. vSAN HCL is downloaded only if new data is available.


        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('download_vsan_hcl', None)
class Tasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_task(self,
                 id,
                 ):
        """
        Get a Task by ID, if it exists

        :type  id: :class:`str`
        :param id: Task id to retrieve
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: A task object.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Task not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_task',
                            {
                            'id': id,
                            })

    def cancel_task(self,
                    id,
                    ):
        """
        Task was cancelled successfully.

        :type  id: :class:`str`
        :param id: Task id for cancelling
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Task not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Task can not be cancelled. Only a
            IN_PROGRESS task can be cancelled.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('cancel_task',
                            {
                            'id': id,
                            })

    def retry_task(self,
                   id,
                   ):
        """
        Task was retried successfully.

        :type  id: :class:`str`
        :param id: Task id retry
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Task not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Task can not be retried. Only a failed Task
            can be retried.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('retry_task',
                            {
                            'id': id,
                            })

    def get_tasks(self,
                  limit=None,
                  task_status=None,
                  task_type=None,
                  resource_id=None,
                  resource_type=None,
                  completed_after=None,
                  page_number=None,
                  page_size=None,
                  order_direction=None,
                  order_by=None,
                  task_name=None,
                  do_live_refresh=None,
                  ):
        """
        Get the tasks

        :type  limit: :class:`long` or ``None``
        :param limit: The number of elements to be returned in the result
        :type  task_status: :class:`str` or ``None``
        :param task_status: 
        :type  task_type: :class:`str` or ``None``
        :param task_type: 
        :type  resource_id: :class:`str` or ``None``
        :param resource_id: 
        :type  resource_type: :class:`str` or ``None``
        :param resource_type: 
        :type  completed_after: :class:`long` or ``None``
        :param completed_after: A time based filter to get tasks which are completed after the
            given timestamp. A task is completed if its status is 'Successful'
            or 'Failed'. Time is in milliseconds.
        :type  page_number: :class:`long` or ``None``
        :param page_number: Page number.
        :type  page_size: :class:`long` or ``None``
        :param page_size: Size of the page you want to retrieve. Max page size allowed is
            100.
        :type  order_direction: :class:`str` or ``None``
        :param order_direction: 
        :type  order_by: :class:`str` or ``None``
        :param order_by: 
        :type  task_name: :class:`str` or ``None``
        :param task_name: Search filter when task name contains text.
        :type  do_live_refresh: :class:`bool` or ``None``
        :param do_live_refresh: 
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTask` or ``None``
        :return: Returns the list of tasks.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_tasks',
                            {
                            'limit': limit,
                            'task_status': task_status,
                            'task_type': task_type,
                            'resource_id': resource_id,
                            'resource_type': resource_type,
                            'completed_after': completed_after,
                            'page_number': page_number,
                            'page_size': page_size,
                            'order_direction': order_direction,
                            'order_by': order_by,
                            'task_name': task_name,
                            'do_live_refresh': do_live_refresh,
                            })
class System(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system'
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


    def get_system_configuration(self):
        """
        Retrieve the system configuration.


        :rtype: :class:`vmware.sddc_manager.model_client.System` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_system_configuration', None)

    def update_system_configuration(self,
                                    system_update_spec,
                                    ):
        """
        OK

        :type  system_update_spec: :class:`vmware.sddc_manager.model_client.SystemUpdateSpec`
        :param system_update_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_system_configuration',
                            {
                            'system_update_spec': system_update_spec,
                            })
class ResourceFunctionalities(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.resource_functionalities'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceFunctionalitiesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_resource_functionalities(self,
                                     resource_type=None,
                                     functionality_type=None,
                                     resource_ids=None,
                                     is_allowed=None,
                                     parent_resource_type=None,
                                     ):
        """
        

        :type  resource_type: :class:`str` or ``None``
        :param resource_type: Resource type
        :type  functionality_type: :class:`str` or ``None``
        :param functionality_type: Functionality type
        :type  resource_ids: :class:`list` of :class:`str` or ``None``
        :param resource_ids: Resource IDs
        :type  is_allowed: :class:`bool` or ``None``
        :param is_allowed: Allowed or disallowed resource functionalities
        :type  parent_resource_type: :class:`str` or ``None``
        :param parent_resource_type: Parent resource type
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfResourceFunctionalities` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_resource_functionalities',
                            {
                            'resource_type': resource_type,
                            'functionality_type': functionality_type,
                            'resource_ids': resource_ids,
                            'is_allowed': is_allowed,
                            'parent_resource_type': parent_resource_type,
                            })

    def update_resources_functionalities(self,
                                         resource_functionalities_update_spec,
                                         ):
        """
        

        :type  resource_functionalities_update_spec: :class:`vmware.sddc_manager.model_client.ResourceFunctionalitiesUpdateSpec`
        :param resource_functionalities_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ResourceFunctionalitiesCaller` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_resources_functionalities',
                            {
                            'resource_functionalities_update_spec': resource_functionalities_update_spec,
                            })
class Credentials(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.credentials'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CredentialsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_credentials(self,
                        resource_name=None,
                        resource_ip=None,
                        resource_type=None,
                        domain_name=None,
                        page_number=None,
                        page_size=None,
                        account_type=None,
                        ):
        """
        Retrieve a list of credentials

        :type  resource_name: :class:`str` or ``None``
        :param resource_name: The name of the resource
        :type  resource_ip: :class:`str` or ``None``
        :param resource_ip: The IP address of the resource
        :type  resource_type: :class:`str` or ``None``
        :param resource_type: The type of the resource. One among: ESXI, VCENTER, PSC,
            NSXT_MANAGER, NSXT_EDGE, NSX_ALB, BACKUP
        :type  domain_name: :class:`str` or ``None``
        :param domain_name: The name of the domain to which the resource belongs to (may be
            null in case there is no associated domain)
        :type  page_number: :class:`str` or ``None``
        :param page_number: The page number (must be a positive number), starts with 0
        :type  page_size: :class:`str` or ``None``
        :param page_size: The page size (must be a positive number, 0 as page size returns
            all records in one page
        :type  account_type: :class:`str` or ``None``
        :param account_type: Type of the account that needs to be fetched by filtering
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCredential` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credentials',
                            {
                            'resource_name': resource_name,
                            'resource_ip': resource_ip,
                            'resource_type': resource_type,
                            'domain_name': domain_name,
                            'page_number': page_number,
                            'page_size': page_size,
                            'account_type': account_type,
                            })

    def update_or_rotate_passwords(self,
                                   credentials_update_spec,
                                   ):
        """
        Update passwords for given list of resources by supplying new passwords
        or rotate the passwords using system generated passwords

        :type  credentials_update_spec: :class:`vmware.sddc_manager.model_client.CredentialsUpdateSpec`
        :param credentials_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_or_rotate_passwords',
                            {
                            'credentials_update_spec': credentials_update_spec,
                            })

    def get_credential(self,
                       id,
                       ):
        """
        Retrieve a credential by its ID

        :type  id: :class:`str`
        :param id: The ID of the credential
        :rtype: :class:`vmware.sddc_manager.model_client.Credential` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_credential',
                            {
                            'id': id,
                            })
class VcfServices(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcf_services'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcfServicesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_services(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVcfService` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vcf_services', None)

    def get_vcf_service(self,
                        id,
                        ):
        """
        

        :type  id: :class:`str`
        :param id: VcfService ID
        :rtype: :class:`vmware.sddc_manager.model_client.VcfService` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. VcfService not found
        """
        return self._invoke('get_vcf_service',
                            {
                            'id': id,
                            })
class Vcenters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.vcenters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcentersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcenters(self,
                     domain_id=None,
                     ):
        """
        

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: ID of the domain
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVcenter` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vcenters',
                            {
                            'domain_id': domain_id,
                            })

    def get_vcenter(self,
                    id,
                    ):
        """
        

        :type  id: :class:`str`
        :param id: vCenter ID
        :rtype: :class:`vmware.sddc_manager.model_client.Vcenter` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. vCenter not found
        """
        return self._invoke('get_vcenter',
                            {
                            'id': id,
                            })
class SsoDomains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.sso_domains'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SsoDomainsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sso_domains(self):
        """
        Get a list of all SSO domains


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfString` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 403. Forbidden request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_SSO_domains', None)
class SddcManagers(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.sddc_managers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SddcManagersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sddc_managers(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfSddcManager` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_sddc_managers', None)

    def get_sddc_manager(self,
                         id,
                         ):
        """
        

        :type  id: :class:`str`
        :param id: Sddc Manager ID
        :rtype: :class:`vmware.sddc_manager.model_client.SddcManager` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Sddc Manager not found
        """
        return self._invoke('get_sddc_manager',
                            {
                            'id': id,
                            })
class Roles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.roles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RolesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_roles(self):
        """
        Get a list of all roles


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfRole` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_roles', None)
class Releases(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.releases'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ReleasesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_releases(self,
                     domain_id=None,
                     version_eq=None,
                     version_gt=None,
                     version_ge=None,
                     applicable_for_version=None,
                     min_installer_version_le=None,
                     get_future_releases=None,
                     include_only_compatible=None,
                     ):
        """
        Get all Releases, with option to get current release for a domain, get
        release by version or get future releases for a versionor get all the
        applicable target release.

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Domain ID to get current release of the domain
        :type  version_eq: :class:`str` or ``None``
        :param version_eq: Release version to get its release
        :type  version_gt: :class:`str` or ``None``
        :param version_gt: Release version to get its future releases
        :type  version_ge: :class:`str` or ``None``
        :param version_ge: Release version to get its current & future releases
        :type  applicable_for_version: :class:`str` or ``None``
        :param applicable_for_version: Release version to get applicable releases
        :type  min_installer_version_le: :class:`str` or ``None``
        :param min_installer_version_le: Releases with minInstallerVersion less than given
            minInstallerVersion
        :type  get_future_releases: :class:`bool` or ``None``
        :param get_future_releases: [Deprecated] Get all future releases for a given domain
        :type  include_only_compatible: :class:`bool` or ``None``
        :param include_only_compatible: Filter only compatible releases on the system
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfRelease` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Release Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_releases',
                            {
                            'domain_id': domain_id,
                            'version_eq': version_eq,
                            'version_gt': version_gt,
                            'version_ge': version_ge,
                            'applicable_for_version': applicable_for_version,
                            'min_installer_version_le': min_installer_version_le,
                            'get_future_releases': get_future_releases,
                            'include_only_compatible': include_only_compatible,
                            })
class Pscs(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.pscs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PscsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_pscs(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfPsc` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_pscs', None)

    def get_psc(self,
                id,
                ):
        """
        

        :type  id: :class:`str`
        :param id: PSC ID
        :rtype: :class:`vmware.sddc_manager.model_client.Psc` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Psc not found
        """
        return self._invoke('get_psc',
                            {
                            'id': id,
                            })
class NsxtClusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NsxtClustersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_nsx_clusters(self,
                         is_shareable=None,
                         v_center_version=None,
                         ):
        """
        

        :type  is_shareable: :class:`bool` or ``None``
        :param is_shareable: filter NSX clusters which can be shared for domain creation
        :type  v_center_version: :class:`str` or ``None``
        :param v_center_version: vCenter Product Version to filter compatible NSX Product Version
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNsxtCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_clusters',
                            {
                            'is_shareable': is_shareable,
                            'v_center_version': v_center_version,
                            })

    def get_nsx_cluster(self,
                        id,
                        ):
        """
        

        :type  id: :class:`str`
        :param id: NSX cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtCluster` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. NSX cluster not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_cluster',
                            {
                            'id': id,
                            })
class Notifications(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.notifications'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NotificationsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_notifications(self):
        """
        Get Notifications


        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.Notification` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_notifications', None)
class LicensingInfo(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.licensing_info'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LicensingInfoStub)
        self._VAPI_OPERATION_IDS = {}


    def get_license_information(self,
                                resource_type=None,
                                resource_ids=None,
                                ):
        """
        

        :type  resource_type: :class:`str` or ``None``
        :param resource_type: Resource type
        :type  resource_ids: :class:`list` of :class:`str` or ``None``
        :param resource_ids: Resource IDs
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.LicensingInfo` or ``None``
        :return: Successful
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_license_information',
                            {
                            'resource_type': resource_type,
                            'resource_ids': resource_ids,
                            })
class ConfigDrifts(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.config_drifts'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ConfigDriftsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_configs(self,
                    resource_id=None,
                    resource_type=None,
                    config_id=None,
                    drift_type=None,
                    include_failed=None,
                    size=None,
                    page=None,
                    ):
        """
        Get configs associated with the given criteria, all if no criteria is
        provided

        :type  resource_id: :class:`str` or ``None``
        :param resource_id: Resource Id
        :type  resource_type: :class:`str` or ``None``
        :param resource_type: Resource Type
        :type  config_id: :class:`str` or ``None``
        :param config_id: Config Id
        :type  drift_type: :class:`str` or ``None``
        :param drift_type: Drift Type
        :type  include_failed: :class:`bool` or ``None``
        :param include_failed: Include drifts with failed applicability computation
        :type  size: :class:`long` or ``None``
        :param size: Size of the page to retrieve. Default page size is 10. Optional
        :type  page: :class:`long` or ``None``
        :param page: Page number to retrieve. Default page 0 will retrieve all elements.
            Optional
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfConfigDriftSpec` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 503. Internal Service Unavailable
        """
        return self._invoke('get_configs',
                            {
                            'resource_id': resource_id,
                            'resource_type': resource_type,
                            'config_id': config_id,
                            'drift_type': drift_type,
                            'include_failed': include_failed,
                            'size': size,
                            'page': page,
                            })
class ComplianceStandards(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compliance_standards'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComplianceStandardsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compliance_standards(self):
        """
        Get a list of all compliance standards


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfComplianceStandard` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_standards', None)
class ComplianceConfigurations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compliance_configurations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComplianceConfigurationsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compliance_configurations(self,
                                      standard_type=None,
                                      standard_version=None,
                                      resource_type=None,
                                      resource_version=None,
                                      ):
        """
        Get a list of all compliance configurations

        :type  standard_type: :class:`str` or ``None``
        :param standard_type: The standard type
        :type  standard_version: :class:`str` or ``None``
        :param standard_version: The standard version, use in combination with standardType
        :type  resource_type: :class:`str` or ``None``
        :param resource_type: The resource type One among: SDDC_MANAGER
        :type  resource_version: :class:`str` or ``None``
        :param resource_version: The resource version, use in combination with resourceType)
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfComplianceConfiguration` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_configurations',
                            {
                            'standard_type': standard_type,
                            'standard_version': standard_version,
                            'resource_type': resource_type,
                            'resource_version': resource_version,
                            })
class ComplianceAudits(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compliance_audits'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComplianceAuditsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compliance_audit_history(self):
        """
        Get compliance audit history


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfComplianceAudit` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit_history', None)

    def get_compliance_audit(self,
                             compliance_audit_id,
                             ):
        """
        Get compliance audit

        :type  compliance_audit_id: :class:`str`
        :param compliance_audit_id: Compliance Audit ID
        :rtype: :class:`vmware.sddc_manager.model_client.ComplianceAudit` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit',
                            {
                            'compliance_audit_id': compliance_audit_id,
                            })
class _CompatibilityMatricesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compatibility_matrices operation
        get_compatibility_matrices_input_type = type.StructType('operation-input', {})
        get_compatibility_matrices_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compatibility_matrices_input_value_validator_list = [
        ]
        get_compatibility_matrices_output_validator_list = [
        ]
        get_compatibility_matrices_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compatibility-matrices',
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

        # properties for get_compatibility_matrix operation
        get_compatibility_matrix_input_type = type.StructType('operation-input', {
            'compatibility_matrix_source': type.StringType(),
        })
        get_compatibility_matrix_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compatibility_matrix_input_value_validator_list = [
        ]
        get_compatibility_matrix_output_validator_list = [
        ]
        get_compatibility_matrix_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compatibility-matrices/{compatibilityMatrixSource}',
            path_variables={
                'compatibility_matrix_source': 'compatibilityMatrixSource',
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
            'get_compatibility_matrices': {
                'input_type': get_compatibility_matrices_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCompatibilityMatrix')),
                'errors': get_compatibility_matrices_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_compatibility_matrices_input_value_validator_list,
                'output_validator_list': get_compatibility_matrices_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_compatibility_matrix': {
                'input_type': get_compatibility_matrix_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CompatibilityMatrix')),
                'errors': get_compatibility_matrix_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_compatibility_matrix_input_value_validator_list,
                'output_validator_list': get_compatibility_matrix_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compatibility_matrices': get_compatibility_matrices_rest_metadata,
            'get_compatibility_matrix': get_compatibility_matrix_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compatibility_matrices',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CertificateAuthoritiesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_certificate_authorities operation
        get_certificate_authorities_input_type = type.StructType('operation-input', {})
        get_certificate_authorities_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_certificate_authorities_input_value_validator_list = [
        ]
        get_certificate_authorities_output_validator_list = [
        ]
        get_certificate_authorities_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/certificate-authorities',
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

        # properties for create_certificate_authority operation
        create_certificate_authority_input_type = type.StructType('operation-input', {
            'certificate_authority_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CertificateAuthorityCreationSpec'),
        })
        create_certificate_authority_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_certificate_authority_input_value_validator_list = [
        ]
        create_certificate_authority_output_validator_list = [
        ]
        create_certificate_authority_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/certificate-authorities',
            request_body_parameter='certificate_authority_creation_spec',
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

        # properties for configure_certificate_authority operation
        configure_certificate_authority_input_type = type.StructType('operation-input', {
            'certificate_authority_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CertificateAuthorityCreationSpec'),
        })
        configure_certificate_authority_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        configure_certificate_authority_input_value_validator_list = [
        ]
        configure_certificate_authority_output_validator_list = [
        ]
        configure_certificate_authority_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/certificate-authorities',
            request_body_parameter='certificate_authority_creation_spec',
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

        # properties for get_certificate_authority_by_id operation
        get_certificate_authority_by_id_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_certificate_authority_by_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_certificate_authority_by_id_input_value_validator_list = [
        ]
        get_certificate_authority_by_id_output_validator_list = [
        ]
        get_certificate_authority_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/certificate-authorities/{id}',
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

        # properties for remove_certificate_authority operation
        remove_certificate_authority_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        remove_certificate_authority_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_certificate_authority_input_value_validator_list = [
        ]
        remove_certificate_authority_output_validator_list = [
        ]
        remove_certificate_authority_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/certificate-authorities/{id}',
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
            'get_certificate_authorities': {
                'input_type': get_certificate_authorities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCertificateAuthority')),
                'errors': get_certificate_authorities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_certificate_authorities_input_value_validator_list,
                'output_validator_list': get_certificate_authorities_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_certificate_authority': {
                'input_type': create_certificate_authority_input_type,
                'output_type': type.VoidType(),
                'errors': create_certificate_authority_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': create_certificate_authority_input_value_validator_list,
                'output_validator_list': create_certificate_authority_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'configure_certificate_authority': {
                'input_type': configure_certificate_authority_input_type,
                'output_type': type.VoidType(),
                'errors': configure_certificate_authority_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': configure_certificate_authority_input_value_validator_list,
                'output_validator_list': configure_certificate_authority_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_certificate_authority_by_id': {
                'input_type': get_certificate_authority_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CertificateAuthority')),
                'errors': get_certificate_authority_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_certificate_authority_by_id_input_value_validator_list,
                'output_validator_list': get_certificate_authority_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_certificate_authority': {
                'input_type': remove_certificate_authority_input_type,
                'output_type': type.VoidType(),
                'errors': remove_certificate_authority_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': remove_certificate_authority_input_value_validator_list,
                'output_validator_list': remove_certificate_authority_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_certificate_authorities': get_certificate_authorities_rest_metadata,
            'create_certificate_authority': create_certificate_authority_rest_metadata,
            'configure_certificate_authority': configure_certificate_authority_rest_metadata,
            'get_certificate_authority_by_id': get_certificate_authority_by_id_rest_metadata,
            'remove_certificate_authority': remove_certificate_authority_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.certificate_authorities',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcfManagementComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_management_components operation
        get_vcf_management_components_input_type = type.StructType('operation-input', {})
        get_vcf_management_components_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_management_components_input_value_validator_list = [
        ]
        get_vcf_management_components_output_validator_list = [
        ]
        get_vcf_management_components_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-management-components',
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

        # properties for deploy_vcf_management_components operation
        deploy_vcf_management_components_input_type = type.StructType('operation-input', {
            'vcf_management_components_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'VcfManagementComponentsSpec'),
        })
        deploy_vcf_management_components_error_dict = {
            'vmware.sddc_manager.model.task':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Task'),

        }
        deploy_vcf_management_components_input_value_validator_list = [
        ]
        deploy_vcf_management_components_output_validator_list = [
        ]
        deploy_vcf_management_components_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vcf-management-components',
            request_body_parameter='vcf_management_components_spec',
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
            'get_vcf_management_components': {
                'input_type': get_vcf_management_components_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VcfManagementComponents')),
                'errors': get_vcf_management_components_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_vcf_management_components_input_value_validator_list,
                'output_validator_list': get_vcf_management_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'deploy_vcf_management_components': {
                'input_type': deploy_vcf_management_components_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': deploy_vcf_management_components_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Task'), [403]).build(),
                'input_value_validator_list': deploy_vcf_management_components_input_value_validator_list,
                'output_validator_list': deploy_vcf_management_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_management_components': get_vcf_management_components_rest_metadata,
            'deploy_vcf_management_components': deploy_vcf_management_components_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_management_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VasaProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vasa_providers operation
        get_vasa_providers_input_type = type.StructType('operation-input', {})
        get_vasa_providers_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vasa_providers_input_value_validator_list = [
        ]
        get_vasa_providers_output_validator_list = [
        ]
        get_vasa_providers_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vasa-providers',
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

        # properties for add_vasa_provider operation
        add_vasa_provider_input_type = type.StructType('operation-input', {
            'vasa_provider': type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider'),
        })
        add_vasa_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_vasa_provider_input_value_validator_list = [
        ]
        add_vasa_provider_output_validator_list = [
        ]
        add_vasa_provider_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/vasa-providers',
            request_body_parameter='vasa_provider',
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

        # properties for get_vasa_provider operation
        get_vasa_provider_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vasa_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vasa_provider_input_value_validator_list = [
        ]
        get_vasa_provider_output_validator_list = [
        ]
        get_vasa_provider_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vasa-providers/{id}',
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

        # properties for remove_vasa_provider operation
        remove_vasa_provider_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        remove_vasa_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_vasa_provider_input_value_validator_list = [
        ]
        remove_vasa_provider_output_validator_list = [
        ]
        remove_vasa_provider_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/vasa-providers/{id}',
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

        # properties for update_vasa_provider operation
        update_vasa_provider_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'vasa_provider_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProviderUpdateSpec'),
        })
        update_vasa_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_vasa_provider_input_value_validator_list = [
        ]
        update_vasa_provider_output_validator_list = [
        ]
        update_vasa_provider_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/vasa-providers/{id}',
            request_body_parameter='vasa_provider_update_spec',
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
            'get_vasa_providers': {
                'input_type': get_vasa_providers_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVasaProvider')),
                'errors': get_vasa_providers_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_vasa_providers_input_value_validator_list,
                'output_validator_list': get_vasa_providers_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_vasa_provider': {
                'input_type': add_vasa_provider_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': add_vasa_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': add_vasa_provider_input_value_validator_list,
                'output_validator_list': add_vasa_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vasa_provider': {
                'input_type': get_vasa_provider_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': get_vasa_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_vasa_provider_input_value_validator_list,
                'output_validator_list': get_vasa_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_vasa_provider': {
                'input_type': remove_vasa_provider_input_type,
                'output_type': type.VoidType(),
                'errors': remove_vasa_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': remove_vasa_provider_input_value_validator_list,
                'output_validator_list': remove_vasa_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_vasa_provider': {
                'input_type': update_vasa_provider_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VasaProvider')),
                'errors': update_vasa_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': update_vasa_provider_input_value_validator_list,
                'output_validator_list': update_vasa_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vasa_providers': get_vasa_providers_rest_metadata,
            'add_vasa_provider': add_vasa_provider_rest_metadata,
            'get_vasa_provider': get_vasa_provider_rest_metadata,
            'remove_vasa_provider': remove_vasa_provider_rest_metadata,
            'update_vasa_provider': update_vasa_provider_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vasa_providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _UsersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_users operation
        get_users_input_type = type.StructType('operation-input', {})
        get_users_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_users_input_value_validator_list = [
        ]
        get_users_output_validator_list = [
        ]
        get_users_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/users',
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

        # properties for add_users operation
        add_users_input_type = type.StructType('operation-input', {
            'add_users_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'User')),
        })
        add_users_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        add_users_input_value_validator_list = [
        ]
        add_users_output_validator_list = [
        ]
        add_users_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/users',
            request_body_parameter='add_users_request_body',
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

        # properties for remove_user operation
        remove_user_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        remove_user_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_user_input_value_validator_list = [
        ]
        remove_user_output_validator_list = [
        ]
        remove_user_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/users/{id}',
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
            'get_users': {
                'input_type': get_users_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUser')),
                'errors': get_users_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': get_users_input_value_validator_list,
                'output_validator_list': get_users_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_users': {
                'input_type': add_users_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUser')),
                'errors': add_users_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': add_users_input_value_validator_list,
                'output_validator_list': add_users_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_user': {
                'input_type': remove_user_input_type,
                'output_type': type.VoidType(),
                'errors': remove_user_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': remove_user_input_value_validator_list,
                'output_validator_list': remove_user_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_users': get_users_rest_metadata,
            'add_users': add_users_rest_metadata,
            'remove_user': remove_user_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.users',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _UpgradesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_upgrades operation
        get_upgrades_input_type = type.StructType('operation-input', {
            'status': type.OptionalType(type.StringType()),
            'bundle_id': type.OptionalType(type.StringType()),
            'bundle_type': type.OptionalType(type.StringType()),
        })
        get_upgrades_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgrades_input_value_validator_list = [
        ]
        get_upgrades_output_validator_list = [
        ]
        get_upgrades_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgrades',
            path_variables={
            },
            query_parameters={
                'status': 'status',
                'bundle_id': 'bundleId',
                'bundle_type': 'bundleType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for perform_upgrade operation
        perform_upgrade_input_type = type.StructType('operation-input', {
            'upgrade_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'UpgradeSpec'),
        })
        perform_upgrade_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        perform_upgrade_input_value_validator_list = [
        ]
        perform_upgrade_output_validator_list = [
        ]
        perform_upgrade_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/upgrades',
            request_body_parameter='upgrade_spec',
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

        # properties for get_upgrade_by_id operation
        get_upgrade_by_id_input_type = type.StructType('operation-input', {
            'upgrade_id': type.StringType(),
        })
        get_upgrade_by_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgrade_by_id_input_value_validator_list = [
        ]
        get_upgrade_by_id_output_validator_list = [
        ]
        get_upgrade_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgrades/{upgradeId}',
            path_variables={
                'upgrade_id': 'upgradeId',
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

        # properties for update_upgrade_schedule operation
        update_upgrade_schedule_input_type = type.StructType('operation-input', {
            'upgrade_id': type.StringType(),
            'upgrade_commit_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'UpgradeCommitSpec'),
        })
        update_upgrade_schedule_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_upgrade_schedule_input_value_validator_list = [
        ]
        update_upgrade_schedule_output_validator_list = [
        ]
        update_upgrade_schedule_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/upgrades/{upgradeId}',
            request_body_parameter='upgrade_commit_spec',
            path_variables={
                'upgrade_id': 'upgradeId',
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
            'get_upgrades': {
                'input_type': get_upgrades_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgrade')),
                'errors': get_upgrades_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,409,400]).build(),
                'input_value_validator_list': get_upgrades_input_value_validator_list,
                'output_validator_list': get_upgrades_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'perform_upgrade': {
                'input_type': perform_upgrade_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': perform_upgrade_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,403,404,424,400]).build(),
                'input_value_validator_list': perform_upgrade_input_value_validator_list,
                'output_validator_list': perform_upgrade_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_upgrade_by_id': {
                'input_type': get_upgrade_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Upgrade')),
                'errors': get_upgrade_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_upgrade_by_id_input_value_validator_list,
                'output_validator_list': get_upgrade_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_upgrade_schedule': {
                'input_type': update_upgrade_schedule_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Upgrade')),
                'errors': update_upgrade_schedule_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,400,409]).build(),
                'input_value_validator_list': update_upgrade_schedule_input_value_validator_list,
                'output_validator_list': update_upgrade_schedule_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_upgrades': get_upgrades_rest_metadata,
            'perform_upgrade': perform_upgrade_rest_metadata,
            'get_upgrade_by_id': get_upgrade_by_id_rest_metadata,
            'update_upgrade_schedule': update_upgrade_schedule_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgrades',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TokensStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create_token operation
        create_token_input_type = type.StructType('operation-input', {
            'token_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TokenCreationSpec'),
        })
        create_token_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_token_input_value_validator_list = [
        ]
        create_token_output_validator_list = [
        ]
        create_token_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/tokens',
            request_body_parameter='token_creation_spec',
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
            'create_token': {
                'input_type': create_token_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TokenPair')),
                'errors': create_token_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': create_token_input_value_validator_list,
                'output_validator_list': create_token_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create_token': create_token_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.tokens',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ResourceWarningsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_resource_warnings operation
        get_resource_warnings_input_type = type.StructType('operation-input', {
            'resource_type': type.OptionalType(type.StringType()),
            'resource_ids': type.OptionalType(type.ListType(type.StringType())),
            'resource_names': type.OptionalType(type.ListType(type.StringType())),
        })
        get_resource_warnings_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_resource_warnings_input_value_validator_list = [
        ]
        get_resource_warnings_output_validator_list = [
        ]
        get_resource_warnings_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/resource-warnings',
            path_variables={
            },
            query_parameters={
                'resource_type': 'resourceType',
                'resource_ids': 'resourceIds',
                'resource_names': 'resourceNames',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create_resource_warning operation
        create_resource_warning_input_type = type.StructType('operation-input', {
            'resource_warning_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceWarningCreationSpec'),
        })
        create_resource_warning_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_resource_warning_input_value_validator_list = [
        ]
        create_resource_warning_output_validator_list = [
        ]
        create_resource_warning_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/resource-warnings',
            request_body_parameter='resource_warning_creation_spec',
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

        # properties for get_resource_warning operation
        get_resource_warning_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_resource_warning_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_resource_warning_input_value_validator_list = [
        ]
        get_resource_warning_output_validator_list = [
        ]
        get_resource_warning_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/resource-warnings/{id}',
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
            'get_resource_warnings': {
                'input_type': get_resource_warnings_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfResourceWarning')),
                'errors': get_resource_warnings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_resource_warnings_input_value_validator_list,
                'output_validator_list': get_resource_warnings_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_resource_warning': {
                'input_type': create_resource_warning_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceWarning')),
                'errors': create_resource_warning_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': create_resource_warning_input_value_validator_list,
                'output_validator_list': create_resource_warning_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_resource_warning': {
                'input_type': get_resource_warning_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceWarning')),
                'errors': get_resource_warning_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_resource_warning_input_value_validator_list,
                'output_validator_list': get_resource_warning_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_resource_warnings': get_resource_warnings_rest_metadata,
            'create_resource_warning': create_resource_warning_rest_metadata,
            'get_resource_warning': get_resource_warning_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.resource_warnings',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ProductVersionCatalogsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_product_version_catalog_content operation
        get_product_version_catalog_content_input_type = type.StructType('operation-input', {})
        get_product_version_catalog_content_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_product_version_catalog_content_input_value_validator_list = [
        ]
        get_product_version_catalog_content_output_validator_list = [
        ]
        get_product_version_catalog_content_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/product-version-catalogs',
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

        # properties for upload_product_version_catalog_with_signature operation
        upload_product_version_catalog_with_signature_input_type = type.StructType('operation-input', {
            'product_version_catalog_with_signature_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalogWithSignatureSpec'),
        })
        upload_product_version_catalog_with_signature_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        upload_product_version_catalog_with_signature_input_value_validator_list = [
        ]
        upload_product_version_catalog_with_signature_output_validator_list = [
        ]
        upload_product_version_catalog_with_signature_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/product-version-catalogs',
            request_body_parameter='product_version_catalog_with_signature_spec',
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

        # properties for update_product_version_catalog_patches operation
        update_product_version_catalog_patches_input_type = type.StructType('operation-input', {
            'product_version_catalog_with_signature_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalogWithSignatureSpec'),
        })
        update_product_version_catalog_patches_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_product_version_catalog_patches_input_value_validator_list = [
        ]
        update_product_version_catalog_patches_output_validator_list = [
        ]
        update_product_version_catalog_patches_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/product-version-catalogs',
            request_body_parameter='product_version_catalog_with_signature_spec',
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
            'get_product_version_catalog_content': {
                'input_type': get_product_version_catalog_content_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalog')),
                'errors': get_product_version_catalog_content_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_product_version_catalog_content_input_value_validator_list,
                'output_validator_list': get_product_version_catalog_content_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upload_product_version_catalog_with_signature': {
                'input_type': upload_product_version_catalog_with_signature_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalogUploadTask')),
                'errors': upload_product_version_catalog_with_signature_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': upload_product_version_catalog_with_signature_input_value_validator_list,
                'output_validator_list': upload_product_version_catalog_with_signature_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_product_version_catalog_patches': {
                'input_type': update_product_version_catalog_patches_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalogUploadTask')),
                'errors': update_product_version_catalog_patches_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': update_product_version_catalog_patches_input_value_validator_list,
                'output_validator_list': update_product_version_catalog_patches_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_product_version_catalog_content': get_product_version_catalog_content_rest_metadata,
            'upload_product_version_catalog_with_signature': upload_product_version_catalog_with_signature_rest_metadata,
            'update_product_version_catalog_patches': update_product_version_catalog_patches_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.product_version_catalogs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ProductVersionCatalogStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_product_version_catalog operation
        get_product_version_catalog_input_type = type.StructType('operation-input', {})
        get_product_version_catalog_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_product_version_catalog_input_value_validator_list = [
        ]
        get_product_version_catalog_output_validator_list = [
        ]
        get_product_version_catalog_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/product-version-catalog',
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

        # properties for upload_product_version_catalog operation
        upload_product_version_catalog_input_type = type.StructType('operation-input', {
            'product_version_catalog': type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalog'),
        })
        upload_product_version_catalog_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        upload_product_version_catalog_input_value_validator_list = [
        ]
        upload_product_version_catalog_output_validator_list = [
        ]
        upload_product_version_catalog_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/product-version-catalog',
            request_body_parameter='product_version_catalog',
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
            'get_product_version_catalog': {
                'input_type': get_product_version_catalog_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalog')),
                'errors': get_product_version_catalog_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,410]).build(),
                'input_value_validator_list': get_product_version_catalog_input_value_validator_list,
                'output_validator_list': get_product_version_catalog_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upload_product_version_catalog': {
                'input_type': upload_product_version_catalog_input_type,
                'output_type': type.VoidType(),
                'errors': upload_product_version_catalog_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,410,400]).build(),
                'input_value_validator_list': upload_product_version_catalog_input_value_validator_list,
                'output_validator_list': upload_product_version_catalog_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_product_version_catalog': get_product_version_catalog_rest_metadata,
            'upload_product_version_catalog': upload_product_version_catalog_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.product_version_catalog',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ProductBinariesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for upload_product_binary operation
        upload_product_binary_input_type = type.StructType('operation-input', {
            'product_binary_upload_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ProductBinaryUploadSpec'),
        })
        upload_product_binary_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        upload_product_binary_input_value_validator_list = [
        ]
        upload_product_binary_output_validator_list = [
        ]
        upload_product_binary_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/product-binaries',
            request_body_parameter='product_binary_upload_spec',
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
            'upload_product_binary': {
                'input_type': upload_product_binary_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': upload_product_binary_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,406]).build(),
                'input_value_validator_list': upload_product_binary_input_value_validator_list,
                'output_validator_list': upload_product_binary_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'upload_product_binary': upload_product_binary_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.product_binaries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _PersonalitiesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_personalities operation
        get_personalities_input_type = type.StructType('operation-input', {
            'base_OS_version': type.OptionalType(type.StringType()),
            'add_on_name': type.OptionalType(type.StringType()),
            'add_on_vendor_name': type.OptionalType(type.StringType()),
            'component_name': type.OptionalType(type.StringType()),
            'component_vendor_name': type.OptionalType(type.StringType()),
            'personality_name': type.OptionalType(type.StringType()),
            'type': type.OptionalType(type.StringType()),
            'size': type.OptionalType(type.IntegerType()),
            'page': type.OptionalType(type.IntegerType()),
            'sort': type.OptionalType(type.StringType()),
        })
        get_personalities_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_personalities_input_value_validator_list = [
        ]
        get_personalities_output_validator_list = [
        ]
        get_personalities_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/personalities',
            path_variables={
            },
            query_parameters={
                'base_OS_version': 'baseOSVersion',
                'add_on_name': 'addOnName',
                'add_on_vendor_name': 'addOnVendorName',
                'component_name': 'componentName',
                'component_vendor_name': 'componentVendorName',
                'personality_name': 'personalityName',
                'type': 'type',
                'size': 'size',
                'page': 'page',
                'sort': 'sort',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for upload_personality operation
        upload_personality_input_type = type.StructType('operation-input', {
            'personality_upload_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'PersonalityUploadSpec'),
        })
        upload_personality_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        upload_personality_input_value_validator_list = [
        ]
        upload_personality_output_validator_list = [
        ]
        upload_personality_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/personalities',
            request_body_parameter='personality_upload_spec',
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

        # properties for delete_personality operation
        delete_personality_input_type = type.StructType('operation-input', {
            'personality_id': type.OptionalType(type.StringType()),
            'personality_name': type.OptionalType(type.StringType()),
        })
        delete_personality_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_personality_input_value_validator_list = [
        ]
        delete_personality_output_validator_list = [
        ]
        delete_personality_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/personalities',
            path_variables={
            },
            query_parameters={
                'personality_id': 'personalityId',
                'personality_name': 'personalityName',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_personality operation
        get_personality_input_type = type.StructType('operation-input', {
            'personality_id': type.StringType(),
        })
        get_personality_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_personality_input_value_validator_list = [
        ]
        get_personality_output_validator_list = [
        ]
        get_personality_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/personalities/{personalityId}',
            path_variables={
                'personality_id': 'personalityId',
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
            'get_personalities': {
                'input_type': get_personalities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfPersonality')),
                'errors': get_personalities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_personalities_input_value_validator_list,
                'output_validator_list': get_personalities_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upload_personality': {
                'input_type': upload_personality_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': upload_personality_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': upload_personality_input_value_validator_list,
                'output_validator_list': upload_personality_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_personality': {
                'input_type': delete_personality_input_type,
                'output_type': type.VoidType(),
                'errors': delete_personality_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': delete_personality_input_value_validator_list,
                'output_validator_list': delete_personality_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_personality': {
                'input_type': get_personality_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Personality')),
                'errors': get_personality_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_personality_input_value_validator_list,
                'output_validator_list': get_personality_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_personalities': get_personalities_rest_metadata,
            'upload_personality': upload_personality_rest_metadata,
            'delete_personality': delete_personality_rest_metadata,
            'get_personality': get_personality_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.personalities',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _NsxAlbClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ALB_clusters operation
        get_ALB_clusters_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_ALB_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_ALB_clusters_input_value_validator_list = [
        ]
        get_ALB_clusters_output_validator_list = [
        ]
        get_ALB_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsx-alb-clusters',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create_ALB_cluster operation
        create_ALB_cluster_input_type = type.StructType('operation-input', {
            'nsx_alb_controller_cluster_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxAlbControllerClusterSpec'),
            'skip_compatibility_check': type.OptionalType(type.BooleanType()),
        })
        create_ALB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_ALB_cluster_input_value_validator_list = [
        ]
        create_ALB_cluster_output_validator_list = [
        ]
        create_ALB_cluster_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsx-alb-clusters',
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

        # properties for get_ALB_cluster operation
        get_ALB_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_ALB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_ALB_cluster_input_value_validator_list = [
        ]
        get_ALB_cluster_output_validator_list = [
        ]
        get_ALB_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsx-alb-clusters/{id}',
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

        # properties for delete_ALB_cluster operation
        delete_ALB_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'force_delete': type.OptionalType(type.BooleanType()),
        })
        delete_ALB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_ALB_cluster_input_value_validator_list = [
        ]
        delete_ALB_cluster_output_validator_list = [
        ]
        delete_ALB_cluster_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/nsx-alb-clusters/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'force_delete': 'forceDelete',
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
            'get_ALB_clusters': {
                'input_type': get_ALB_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNsxALBCluster')),
                'errors': get_ALB_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_ALB_clusters_input_value_validator_list,
                'output_validator_list': get_ALB_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_ALB_cluster': {
                'input_type': create_ALB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': create_ALB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': create_ALB_cluster_input_value_validator_list,
                'output_validator_list': create_ALB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_ALB_cluster': {
                'input_type': get_ALB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxALBCluster')),
                'errors': get_ALB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_ALB_cluster_input_value_validator_list,
                'output_validator_list': get_ALB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_ALB_cluster': {
                'input_type': delete_ALB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': delete_ALB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': delete_ALB_cluster_input_value_validator_list,
                'output_validator_list': delete_ALB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_ALB_clusters': get_ALB_clusters_rest_metadata,
            'create_ALB_cluster': create_ALB_cluster_rest_metadata,
            'get_ALB_cluster': get_ALB_cluster_rest_metadata,
            'delete_ALB_cluster': delete_ALB_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsx_alb_clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _NetworkPoolsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_network_pool operation
        get_network_pool_input_type = type.StructType('operation-input', {})
        get_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_network_pool_input_value_validator_list = [
        ]
        get_network_pool_output_validator_list = [
        ]
        get_network_pool_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/network-pools',
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

        # properties for create_network_pool operation
        create_network_pool_input_type = type.StructType('operation-input', {
            'network_pool': type.ReferenceType('vmware.sddc_manager.model_client', 'NetworkPool'),
        })
        create_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_network_pool_input_value_validator_list = [
        ]
        create_network_pool_output_validator_list = [
        ]
        create_network_pool_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/network-pools',
            request_body_parameter='network_pool',
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

        # properties for get_network_pool_by_ID operation
        get_network_pool_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_network_pool_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_network_pool_by_ID_input_value_validator_list = [
        ]
        get_network_pool_by_ID_output_validator_list = [
        ]
        get_network_pool_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/network-pools/{id}',
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

        # properties for delete_network_pool operation
        delete_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'force': type.OptionalType(type.BooleanType()),
        })
        delete_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_network_pool_input_value_validator_list = [
        ]
        delete_network_pool_output_validator_list = [
        ]
        delete_network_pool_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/network-pools/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'force': 'force',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update_network_pool operation
        update_network_pool_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'network_pool_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NetworkPoolUpdateSpec'),
        })
        update_network_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_network_pool_input_value_validator_list = [
        ]
        update_network_pool_output_validator_list = [
        ]
        update_network_pool_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/network-pools/{id}',
            request_body_parameter='network_pool_update_spec',
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
            'get_network_pool': {
                'input_type': get_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNetworkPool')),
                'errors': get_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_network_pool_input_value_validator_list,
                'output_validator_list': get_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_network_pool': {
                'input_type': create_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NetworkPool')),
                'errors': create_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': create_network_pool_input_value_validator_list,
                'output_validator_list': create_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_network_pool_by_ID': {
                'input_type': get_network_pool_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NetworkPool')),
                'errors': get_network_pool_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_network_pool_by_ID_input_value_validator_list,
                'output_validator_list': get_network_pool_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_network_pool': {
                'input_type': delete_network_pool_input_type,
                'output_type': type.VoidType(),
                'errors': delete_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,400]).build(),
                'input_value_validator_list': delete_network_pool_input_value_validator_list,
                'output_validator_list': delete_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_network_pool': {
                'input_type': update_network_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NetworkPool')),
                'errors': update_network_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': update_network_pool_input_value_validator_list,
                'output_validator_list': update_network_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_network_pool': get_network_pool_rest_metadata,
            'create_network_pool': create_network_pool_rest_metadata,
            'get_network_pool_by_ID': get_network_pool_by_ID_rest_metadata,
            'delete_network_pool': delete_network_pool_rest_metadata,
            'update_network_pool': update_network_pool_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.network_pools',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ManifestsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_manifest operation
        get_manifest_input_type = type.StructType('operation-input', {})
        get_manifest_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_manifest_input_value_validator_list = [
        ]
        get_manifest_output_validator_list = [
        ]
        get_manifest_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/manifests',
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

        # properties for save_manifest operation
        save_manifest_input_type = type.StructType('operation-input', {
            'manifest': type.ReferenceType('vmware.sddc_manager.model_client', 'Manifest'),
        })
        save_manifest_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        save_manifest_input_value_validator_list = [
        ]
        save_manifest_output_validator_list = [
        ]
        save_manifest_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/manifests',
            request_body_parameter='manifest',
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
            'get_manifest': {
                'input_type': get_manifest_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Manifest')),
                'errors': get_manifest_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_manifest_input_value_validator_list,
                'output_validator_list': get_manifest_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'save_manifest': {
                'input_type': save_manifest_input_type,
                'output_type': type.VoidType(),
                'errors': save_manifest_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,409,400]).build(),
                'input_value_validator_list': save_manifest_input_value_validator_list,
                'output_validator_list': save_manifest_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_manifest': get_manifest_rest_metadata,
            'save_manifest': save_manifest_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.manifests',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _LicenseKeysStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_license_keys operation
        get_license_keys_input_type = type.StructType('operation-input', {
            'product_type': type.OptionalType(type.ListType(type.StringType())),
            'license_key_status': type.OptionalType(type.ListType(type.StringType())),
            'license_unit': type.OptionalType(type.ListType(type.StringType())),
            'product_version': type.OptionalType(type.StringType()),
        })
        get_license_keys_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_license_keys_input_value_validator_list = [
        ]
        get_license_keys_output_validator_list = [
        ]
        get_license_keys_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/license-keys',
            path_variables={
            },
            query_parameters={
                'product_type': 'productType',
                'license_key_status': 'licenseKeyStatus',
                'license_unit': 'licenseUnit',
                'product_version': 'productVersion',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for add_license_key operation
        add_license_key_input_type = type.StructType('operation-input', {
            'license_key': type.ReferenceType('vmware.sddc_manager.model_client', 'LicenseKey'),
        })
        add_license_key_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_license_key_input_value_validator_list = [
        ]
        add_license_key_output_validator_list = [
        ]
        add_license_key_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/license-keys',
            request_body_parameter='license_key',
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

        # properties for update_license_key operation
        update_license_key_input_type = type.StructType('operation-input', {
            'license_key_or_id': type.StringType(),
            'license_key_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'LicenseKeyUpdateSpec'),
        })
        update_license_key_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_license_key_input_value_validator_list = [
        ]
        update_license_key_output_validator_list = [
        ]
        update_license_key_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/license-keys/{licenseKeyOrId}',
            request_body_parameter='license_key_update_spec',
            path_variables={
                'license_key_or_id': 'licenseKeyOrId',
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

        # properties for get_license_key operation
        get_license_key_input_type = type.StructType('operation-input', {
            'key': type.StringType(),
        })
        get_license_key_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_license_key_input_value_validator_list = [
        ]
        get_license_key_output_validator_list = [
        ]
        get_license_key_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/license-keys/{key}',
            path_variables={
                'key': 'key',
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

        # properties for remove_license_key operation
        remove_license_key_input_type = type.StructType('operation-input', {
            'key': type.StringType(),
        })
        remove_license_key_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_license_key_input_value_validator_list = [
        ]
        remove_license_key_output_validator_list = [
        ]
        remove_license_key_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/license-keys/{key}',
            path_variables={
                'key': 'key',
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
            'get_license_keys': {
                'input_type': get_license_keys_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfLicenseKey')),
                'errors': get_license_keys_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_license_keys_input_value_validator_list,
                'output_validator_list': get_license_keys_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_license_key': {
                'input_type': add_license_key_input_type,
                'output_type': type.VoidType(),
                'errors': add_license_key_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': add_license_key_input_value_validator_list,
                'output_validator_list': add_license_key_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_license_key': {
                'input_type': update_license_key_input_type,
                'output_type': type.VoidType(),
                'errors': update_license_key_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': update_license_key_input_value_validator_list,
                'output_validator_list': update_license_key_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_license_key': {
                'input_type': get_license_key_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'LicenseKey')),
                'errors': get_license_key_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_license_key_input_value_validator_list,
                'output_validator_list': get_license_key_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_license_key': {
                'input_type': remove_license_key_input_type,
                'output_type': type.VoidType(),
                'errors': remove_license_key_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': remove_license_key_input_value_validator_list,
                'output_validator_list': remove_license_key_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_license_keys': get_license_keys_rest_metadata,
            'add_license_key': add_license_key_rest_metadata,
            'update_license_key': update_license_key_rest_metadata,
            'get_license_key': get_license_key_rest_metadata,
            'remove_license_key': remove_license_key_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.license_keys',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _IdentityProvidersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_identity_providers operation
        get_identity_providers_input_type = type.StructType('operation-input', {})
        get_identity_providers_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_identity_providers_input_value_validator_list = [
        ]
        get_identity_providers_output_validator_list = [
        ]
        get_identity_providers_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/identity-providers',
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

        # properties for add_external_identity_provider operation
        add_external_identity_provider_input_type = type.StructType('operation-input', {
            'identity_provider_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'IdentityProviderSpec'),
        })
        add_external_identity_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_external_identity_provider_input_value_validator_list = [
        ]
        add_external_identity_provider_output_validator_list = [
        ]
        add_external_identity_provider_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/identity-providers',
            request_body_parameter='identity_provider_spec',
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

        # properties for get_identity_provider_by_id operation
        get_identity_provider_by_id_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_identity_provider_by_id_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_identity_provider_by_id_input_value_validator_list = [
        ]
        get_identity_provider_by_id_output_validator_list = [
        ]
        get_identity_provider_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/identity-providers/{id}',
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

        # properties for delete_external_identity_provider operation
        delete_external_identity_provider_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        delete_external_identity_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_external_identity_provider_input_value_validator_list = [
        ]
        delete_external_identity_provider_output_validator_list = [
        ]
        delete_external_identity_provider_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/identity-providers/{id}',
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

        # properties for update_external_identity_provider operation
        update_external_identity_provider_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'identity_provider_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'IdentityProviderSpec'),
        })
        update_external_identity_provider_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_external_identity_provider_input_value_validator_list = [
        ]
        update_external_identity_provider_output_validator_list = [
        ]
        update_external_identity_provider_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/identity-providers/{id}',
            request_body_parameter='identity_provider_spec',
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
            'get_identity_providers': {
                'input_type': get_identity_providers_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfIdentityProvider')),
                'errors': get_identity_providers_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': get_identity_providers_input_value_validator_list,
                'output_validator_list': get_identity_providers_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_external_identity_provider': {
                'input_type': add_external_identity_provider_input_type,
                'output_type': type.VoidType(),
                'errors': add_external_identity_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': add_external_identity_provider_input_value_validator_list,
                'output_validator_list': add_external_identity_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_identity_provider_by_id': {
                'input_type': get_identity_provider_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'IdentityProvider')),
                'errors': get_identity_provider_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401]).add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_identity_provider_by_id_input_value_validator_list,
                'output_validator_list': get_identity_provider_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_external_identity_provider': {
                'input_type': delete_external_identity_provider_input_type,
                'output_type': type.VoidType(),
                'errors': delete_external_identity_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': delete_external_identity_provider_input_value_validator_list,
                'output_validator_list': delete_external_identity_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_external_identity_provider': {
                'input_type': update_external_identity_provider_input_type,
                'output_type': type.VoidType(),
                'errors': update_external_identity_provider_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400,404]).build(),
                'input_value_validator_list': update_external_identity_provider_input_value_validator_list,
                'output_validator_list': update_external_identity_provider_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_identity_providers': get_identity_providers_rest_metadata,
            'add_external_identity_provider': add_external_identity_provider_rest_metadata,
            'get_identity_provider_by_id': get_identity_provider_by_id_rest_metadata,
            'delete_external_identity_provider': delete_external_identity_provider_rest_metadata,
            'update_external_identity_provider': update_external_identity_provider_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.identity_providers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _HostsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_hosts operation
        get_hosts_input_type = type.StructType('operation-input', {
            'fqdn': type.OptionalType(type.StringType()),
            'status': type.OptionalType(type.StringType()),
            'domain_id': type.OptionalType(type.StringType()),
            'cluster_id': type.OptionalType(type.StringType()),
            'networkpool_id': type.OptionalType(type.StringType()),
            'storage_type': type.OptionalType(type.StringType()),
            'datastore_name': type.OptionalType(type.StringType()),
            'size': type.OptionalType(type.IntegerType()),
            'page': type.OptionalType(type.IntegerType()),
        })
        get_hosts_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_hosts_input_value_validator_list = [
        ]
        get_hosts_output_validator_list = [
        ]
        get_hosts_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts',
            path_variables={
            },
            query_parameters={
                'fqdn': 'fqdn',
                'status': 'status',
                'domain_id': 'domainId',
                'cluster_id': 'clusterId',
                'networkpool_id': 'networkpoolId',
                'storage_type': 'storageType',
                'datastore_name': 'datastoreName',
                'size': 'size',
                'page': 'page',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for commission_hosts operation
        commission_hosts_input_type = type.StructType('operation-input', {
            'commission_hosts_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostCommissionSpec')),
        })
        commission_hosts_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        commission_hosts_input_value_validator_list = [
        ]
        commission_hosts_output_validator_list = [
        ]
        commission_hosts_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/hosts',
            request_body_parameter='commission_hosts_request_body',
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

        # properties for decommission_hosts operation
        decommission_hosts_input_type = type.StructType('operation-input', {
            'decommission_hosts_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostDecommissionSpec')),
        })
        decommission_hosts_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        decommission_hosts_input_value_validator_list = [
        ]
        decommission_hosts_output_validator_list = [
        ]
        decommission_hosts_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/hosts',
            request_body_parameter='decommission_hosts_request_body',
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

        # properties for get_host operation
        get_host_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_host_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_host_input_value_validator_list = [
        ]
        get_host_output_validator_list = [
        ]
        get_host_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/hosts/{id}',
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
            'get_hosts': {
                'input_type': get_hosts_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfHost')),
                'errors': get_hosts_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_hosts_input_value_validator_list,
                'output_validator_list': get_hosts_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'commission_hosts': {
                'input_type': commission_hosts_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': commission_hosts_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': commission_hosts_input_value_validator_list,
                'output_validator_list': commission_hosts_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'decommission_hosts': {
                'input_type': decommission_hosts_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': decommission_hosts_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': decommission_hosts_input_value_validator_list,
                'output_validator_list': decommission_hosts_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_host': {
                'input_type': get_host_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Host')),
                'errors': get_host_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_host_input_value_validator_list,
                'output_validator_list': get_host_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_hosts': get_hosts_rest_metadata,
            'commission_hosts': commission_hosts_rest_metadata,
            'decommission_hosts': decommission_hosts_rest_metadata,
            'get_host': get_host_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _EdgeClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_edge_clusters operation
        get_edge_clusters_input_type = type.StructType('operation-input', {
            'cluster_id': type.OptionalType(type.StringType()),
        })
        get_edge_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_edge_clusters_input_value_validator_list = [
        ]
        get_edge_clusters_output_validator_list = [
        ]
        get_edge_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/edge-clusters',
            path_variables={
            },
            query_parameters={
                'cluster_id': 'clusterId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create_edge_cluster operation
        create_edge_cluster_input_type = type.StructType('operation-input', {
            'edge_cluster_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'EdgeClusterCreationSpec'),
        })
        create_edge_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_edge_cluster_input_value_validator_list = [
        ]
        create_edge_cluster_output_validator_list = [
        ]
        create_edge_cluster_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/edge-clusters',
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

        # properties for get_edge_cluster operation
        get_edge_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_edge_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_edge_cluster_input_value_validator_list = [
        ]
        get_edge_cluster_output_validator_list = [
        ]
        get_edge_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/edge-clusters/{id}',
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

        # properties for update_edge_cluster operation
        update_edge_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'edge_cluster_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'EdgeClusterUpdateSpec'),
        })
        update_edge_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_edge_cluster_input_value_validator_list = [
        ]
        update_edge_cluster_output_validator_list = [
        ]
        update_edge_cluster_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/edge-clusters/{id}',
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

        operations = {
            'get_edge_clusters': {
                'input_type': get_edge_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfEdgeCluster')),
                'errors': get_edge_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_edge_clusters_input_value_validator_list,
                'output_validator_list': get_edge_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_edge_cluster': {
                'input_type': create_edge_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': create_edge_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': create_edge_cluster_input_value_validator_list,
                'output_validator_list': create_edge_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_edge_cluster': {
                'input_type': get_edge_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'EdgeCluster')),
                'errors': get_edge_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_edge_cluster_input_value_validator_list,
                'output_validator_list': get_edge_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_edge_cluster': {
                'input_type': update_edge_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_edge_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,501,400]).build(),
                'input_value_validator_list': update_edge_cluster_input_value_validator_list,
                'output_validator_list': update_edge_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_edge_clusters': get_edge_clusters_rest_metadata,
            'create_edge_cluster': create_edge_cluster_rest_metadata,
            'get_edge_cluster': get_edge_cluster_rest_metadata,
            'update_edge_cluster': update_edge_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.edge_clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domains operation
        get_domains_input_type = type.StructType('operation-input', {
            'type': type.OptionalType(type.StringType()),
        })
        get_domains_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domains_input_value_validator_list = [
        ]
        get_domains_output_validator_list = [
        ]
        get_domains_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains',
            path_variables={
            },
            query_parameters={
                'type': 'type',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create_domain operation
        create_domain_input_type = type.StructType('operation-input', {
            'domain_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DomainCreationSpec'),
        })
        create_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_domain_input_value_validator_list = [
        ]
        create_domain_output_validator_list = [
        ]
        create_domain_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains',
            request_body_parameter='domain_creation_spec',
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

        # properties for get_domain operation
        get_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_input_value_validator_list = [
        ]
        get_domain_output_validator_list = [
        ]
        get_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}',
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

        # properties for delete_domain operation
        delete_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        delete_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_domain_input_value_validator_list = [
        ]
        delete_domain_output_validator_list = [
        ]
        delete_domain_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/domains/{id}',
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

        # properties for update_domain operation
        update_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'domain_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DomainUpdateSpec'),
        })
        update_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_domain_input_value_validator_list = [
        ]
        update_domain_output_validator_list = [
        ]
        update_domain_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{id}',
            request_body_parameter='domain_update_spec',
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
            'get_domains': {
                'input_type': get_domains_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDomain')),
                'errors': get_domains_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_domains_input_value_validator_list,
                'output_validator_list': get_domains_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_domain': {
                'input_type': create_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': create_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': create_domain_input_value_validator_list,
                'output_validator_list': create_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_domain': {
                'input_type': get_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Domain')),
                'errors': get_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_domain_input_value_validator_list,
                'output_validator_list': get_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_domain': {
                'input_type': delete_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': delete_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': delete_domain_input_value_validator_list,
                'output_validator_list': delete_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_domain': {
                'input_type': update_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': update_domain_input_value_validator_list,
                'output_validator_list': update_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domains': get_domains_rest_metadata,
            'create_domain': create_domain_rest_metadata,
            'get_domain': get_domain_rest_metadata,
            'delete_domain': delete_domain_rest_metadata,
            'update_domain': update_domain_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ConfigDriftReconciliationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for reconcile_configs operation
        reconcile_configs_input_type = type.StructType('operation-input', {
            'config_drift_apply_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ConfigDriftApplySpec'),
        })
        reconcile_configs_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        reconcile_configs_input_value_validator_list = [
        ]
        reconcile_configs_output_validator_list = [
        ]
        reconcile_configs_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/config-drift-reconciliations',
            request_body_parameter='config_drift_apply_spec',
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

        # properties for get_reconciliation_task operation
        get_reconciliation_task_input_type = type.StructType('operation-input', {
            'task_id': type.StringType(),
        })
        get_reconciliation_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_reconciliation_task_input_value_validator_list = [
        ]
        get_reconciliation_task_output_validator_list = [
        ]
        get_reconciliation_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/config-drift-reconciliations/{taskId}',
            path_variables={
                'task_id': 'taskId',
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
            'reconcile_configs': {
                'input_type': reconcile_configs_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': reconcile_configs_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': reconcile_configs_input_value_validator_list,
                'output_validator_list': reconcile_configs_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_reconciliation_task': {
                'input_type': get_reconciliation_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': get_reconciliation_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_reconciliation_task_input_value_validator_list,
                'output_validator_list': get_reconciliation_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'reconcile_configs': reconcile_configs_rest_metadata,
            'get_reconciliation_task': get_reconciliation_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.config_drift_reconciliations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_clusters operation
        get_clusters_input_type = type.StructType('operation-input', {
            'is_stretched': type.OptionalType(type.BooleanType()),
            'is_image_based': type.OptionalType(type.BooleanType()),
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_clusters_input_value_validator_list = [
        ]
        get_clusters_output_validator_list = [
        ]
        get_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters',
            path_variables={
            },
            query_parameters={
                'is_stretched': 'isStretched',
                'is_image_based': 'isImageBased',
                'domain_id': 'domainId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create_cluster operation
        create_cluster_input_type = type.StructType('operation-input', {
            'cluster_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterCreationSpec'),
        })
        create_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        create_cluster_input_value_validator_list = [
        ]
        create_cluster_output_validator_list = [
        ]
        create_cluster_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters',
            request_body_parameter='cluster_creation_spec',
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

        # properties for get_cluster operation
        get_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_input_value_validator_list = [
        ]
        get_cluster_output_validator_list = [
        ]
        get_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}',
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

        # properties for delete_cluster operation
        delete_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'force': type.OptionalType(type.BooleanType()),
        })
        delete_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_cluster_input_value_validator_list = [
        ]
        delete_cluster_output_validator_list = [
        ]
        delete_cluster_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/clusters/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'force': 'force',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update_cluster operation
        update_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'cluster_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterUpdateSpec'),
        })
        update_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_cluster_input_value_validator_list = [
        ]
        update_cluster_output_validator_list = [
        ]
        update_cluster_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/clusters/{id}',
            request_body_parameter='cluster_update_spec',
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
            'get_clusters': {
                'input_type': get_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCluster')),
                'errors': get_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_clusters_input_value_validator_list,
                'output_validator_list': get_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_cluster': {
                'input_type': create_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': create_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': create_cluster_input_value_validator_list,
                'output_validator_list': create_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster': {
                'input_type': get_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Cluster')),
                'errors': get_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_cluster_input_value_validator_list,
                'output_validator_list': get_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_cluster': {
                'input_type': delete_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': delete_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': delete_cluster_input_value_validator_list,
                'output_validator_list': delete_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_cluster': {
                'input_type': update_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': update_cluster_input_value_validator_list,
                'output_validator_list': update_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_clusters': get_clusters_rest_metadata,
            'create_cluster': create_cluster_rest_metadata,
            'get_cluster': get_cluster_rest_metadata,
            'delete_cluster': delete_cluster_rest_metadata,
            'update_cluster': update_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _BundlesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_bundles operation
        get_bundles_input_type = type.StructType('operation-input', {
            'product_type': type.OptionalType(type.StringType()),
            'is_compliant': type.OptionalType(type.BooleanType()),
            'bundle_type': type.OptionalType(type.StringType()),
        })
        get_bundles_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_bundles_input_value_validator_list = [
        ]
        get_bundles_output_validator_list = [
        ]
        get_bundles_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles',
            path_variables={
            },
            query_parameters={
                'product_type': 'productType',
                'is_compliant': 'isCompliant',
                'bundle_type': 'bundleType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for upload_bundle operation
        upload_bundle_input_type = type.StructType('operation-input', {
            'bundle_upload_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BundleUploadSpec'),
        })
        upload_bundle_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        upload_bundle_input_value_validator_list = [
        ]
        upload_bundle_output_validator_list = [
        ]
        upload_bundle_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/bundles',
            request_body_parameter='bundle_upload_spec',
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

        # properties for get_bundle operation
        get_bundle_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_bundle_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_bundle_input_value_validator_list = [
        ]
        get_bundle_output_validator_list = [
        ]
        get_bundle_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles/{id}',
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

        # properties for delete_bundle operation
        delete_bundle_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'binary_files_only': type.OptionalType(type.BooleanType()),
        })
        delete_bundle_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_bundle_input_value_validator_list = [
        ]
        delete_bundle_output_validator_list = [
        ]
        delete_bundle_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/bundles/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'binary_files_only': 'binaryFilesOnly',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for start_bundle_download_by_ID operation
        start_bundle_download_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'bundle_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BundleUpdateSpec'),
        })
        start_bundle_download_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_bundle_download_by_ID_input_value_validator_list = [
        ]
        start_bundle_download_by_ID_output_validator_list = [
        ]
        start_bundle_download_by_ID_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/bundles/{id}',
            request_body_parameter='bundle_update_spec',
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
            'get_bundles': {
                'input_type': get_bundles_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfBundle')),
                'errors': get_bundles_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_bundles_input_value_validator_list,
                'output_validator_list': get_bundles_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upload_bundle': {
                'input_type': upload_bundle_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': upload_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,410,500]).build(),
                'input_value_validator_list': upload_bundle_input_value_validator_list,
                'output_validator_list': upload_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_bundle': {
                'input_type': get_bundle_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Bundle')),
                'errors': get_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_bundle_input_value_validator_list,
                'output_validator_list': get_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_bundle': {
                'input_type': delete_bundle_input_type,
                'output_type': type.VoidType(),
                'errors': delete_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,409,500]).build(),
                'input_value_validator_list': delete_bundle_input_value_validator_list,
                'output_validator_list': delete_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start_bundle_download_by_ID': {
                'input_type': start_bundle_download_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': start_bundle_download_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,409,500]).build(),
                'input_value_validator_list': start_bundle_download_by_ID_input_value_validator_list,
                'output_validator_list': start_bundle_download_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_bundles': get_bundles_rest_metadata,
            'upload_bundle': upload_bundle_rest_metadata,
            'get_bundle': get_bundle_rest_metadata,
            'delete_bundle': delete_bundle_rest_metadata,
            'start_bundle_download_by_ID': start_bundle_download_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.bundles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _AlbClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_avi_LB_clusters operation
        get_avi_LB_clusters_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_avi_LB_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_avi_LB_clusters_input_value_validator_list = [
        ]
        get_avi_LB_clusters_output_validator_list = [
        ]
        get_avi_LB_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/alb-clusters',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for deploy_ALB_cluster operation
        deploy_ALB_cluster_input_type = type.StructType('operation-input', {
            'alb_controller_cluster_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'AlbControllerClusterSpec'),
            'skip_compatibility_check': type.OptionalType(type.BooleanType()),
        })
        deploy_ALB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        deploy_ALB_cluster_input_value_validator_list = [
        ]
        deploy_ALB_cluster_output_validator_list = [
        ]
        deploy_ALB_cluster_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/alb-clusters',
            request_body_parameter='alb_controller_cluster_spec',
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

        # properties for get_avi_LB_cluster operation
        get_avi_LB_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_avi_LB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_avi_LB_cluster_input_value_validator_list = [
        ]
        get_avi_LB_cluster_output_validator_list = [
        ]
        get_avi_LB_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/alb-clusters/{id}',
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

        # properties for undeploy_ALB_cluster operation
        undeploy_ALB_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'force_delete': type.OptionalType(type.BooleanType()),
        })
        undeploy_ALB_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        undeploy_ALB_cluster_input_value_validator_list = [
        ]
        undeploy_ALB_cluster_output_validator_list = [
        ]
        undeploy_ALB_cluster_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/alb-clusters/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'force_delete': 'forceDelete',
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
            'get_avi_LB_clusters': {
                'input_type': get_avi_LB_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfALBCluster')),
                'errors': get_avi_LB_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_avi_LB_clusters_input_value_validator_list,
                'output_validator_list': get_avi_LB_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'deploy_ALB_cluster': {
                'input_type': deploy_ALB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': deploy_ALB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': deploy_ALB_cluster_input_value_validator_list,
                'output_validator_list': deploy_ALB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_avi_LB_cluster': {
                'input_type': get_avi_LB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxALBCluster')),
                'errors': get_avi_LB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_avi_LB_cluster_input_value_validator_list,
                'output_validator_list': get_avi_LB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'undeploy_ALB_cluster': {
                'input_type': undeploy_ALB_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': undeploy_ALB_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': undeploy_ALB_cluster_input_value_validator_list,
                'output_validator_list': undeploy_ALB_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_avi_LB_clusters': get_avi_LB_clusters_rest_metadata,
            'deploy_ALB_cluster': deploy_ALB_cluster_rest_metadata,
            'get_avi_LB_cluster': get_avi_LB_cluster_rest_metadata,
            'undeploy_ALB_cluster': undeploy_ALB_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.alb_clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VsanHclStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for download_vsan_hcl operation
        download_vsan_hcl_input_type = type.StructType('operation-input', {})
        download_vsan_hcl_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        download_vsan_hcl_input_value_validator_list = [
        ]
        download_vsan_hcl_output_validator_list = [
        ]
        download_vsan_hcl_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/vsan-hcl',
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
            'download_vsan_hcl': {
                'input_type': download_vsan_hcl_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': download_vsan_hcl_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': download_vsan_hcl_input_value_validator_list,
                'output_validator_list': download_vsan_hcl_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'download_vsan_hcl': download_vsan_hcl_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vsan_hcl',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_task operation
        get_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_task_input_value_validator_list = [
        ]
        get_task_output_validator_list = [
        ]
        get_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/tasks/{id}',
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

        # properties for cancel_task operation
        cancel_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        cancel_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        cancel_task_input_value_validator_list = [
        ]
        cancel_task_output_validator_list = [
        ]
        cancel_task_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/tasks/{id}',
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

        # properties for retry_task operation
        retry_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        retry_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        retry_task_input_value_validator_list = [
        ]
        retry_task_output_validator_list = [
        ]
        retry_task_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/tasks/{id}',
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

        # properties for get_tasks operation
        get_tasks_input_type = type.StructType('operation-input', {
            'limit': type.OptionalType(type.IntegerType()),
            'task_status': type.OptionalType(type.StringType()),
            'task_type': type.OptionalType(type.StringType()),
            'resource_id': type.OptionalType(type.StringType()),
            'resource_type': type.OptionalType(type.StringType()),
            'completed_after': type.OptionalType(type.IntegerType()),
            'page_number': type.OptionalType(type.IntegerType()),
            'page_size': type.OptionalType(type.IntegerType()),
            'order_direction': type.OptionalType(type.StringType()),
            'order_by': type.OptionalType(type.StringType()),
            'task_name': type.OptionalType(type.StringType()),
            'do_live_refresh': type.OptionalType(type.BooleanType()),
        })
        get_tasks_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tasks_input_value_validator_list = [
        ]
        get_tasks_output_validator_list = [
        ]
        get_tasks_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/tasks',
            path_variables={
            },
            query_parameters={
                'limit': 'limit',
                'task_status': 'taskStatus',
                'task_type': 'taskType',
                'resource_id': 'resourceId',
                'resource_type': 'resourceType',
                'completed_after': 'completedAfter',
                'page_number': 'pageNumber',
                'page_size': 'pageSize',
                'order_direction': 'orderDirection',
                'order_by': 'orderBy',
                'task_name': 'taskName',
                'do_live_refresh': 'doLiveRefresh',
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
            'get_task': {
                'input_type': get_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': get_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_task_input_value_validator_list,
                'output_validator_list': get_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel_task': {
                'input_type': cancel_task_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,409,500]).build(),
                'input_value_validator_list': cancel_task_input_value_validator_list,
                'output_validator_list': cancel_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'retry_task': {
                'input_type': retry_task_input_type,
                'output_type': type.VoidType(),
                'errors': retry_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,409,500]).build(),
                'input_value_validator_list': retry_task_input_value_validator_list,
                'output_validator_list': retry_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_tasks': {
                'input_type': get_tasks_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTask')),
                'errors': get_tasks_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_tasks_input_value_validator_list,
                'output_validator_list': get_tasks_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_task': get_task_rest_metadata,
            'cancel_task': cancel_task_rest_metadata,
            'retry_task': retry_task_rest_metadata,
            'get_tasks': get_tasks_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_configuration operation
        get_system_configuration_input_type = type.StructType('operation-input', {})
        get_system_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_system_configuration_input_value_validator_list = [
        ]
        get_system_configuration_output_validator_list = [
        ]
        get_system_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system',
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

        # properties for update_system_configuration operation
        update_system_configuration_input_type = type.StructType('operation-input', {
            'system_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'SystemUpdateSpec'),
        })
        update_system_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_system_configuration_input_value_validator_list = [
        ]
        update_system_configuration_output_validator_list = [
        ]
        update_system_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system',
            request_body_parameter='system_update_spec',
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
            'get_system_configuration': {
                'input_type': get_system_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'System')),
                'errors': get_system_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_system_configuration_input_value_validator_list,
                'output_validator_list': get_system_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_system_configuration': {
                'input_type': update_system_configuration_input_type,
                'output_type': type.VoidType(),
                'errors': update_system_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_system_configuration_input_value_validator_list,
                'output_validator_list': update_system_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_configuration': get_system_configuration_rest_metadata,
            'update_system_configuration': update_system_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ResourceFunctionalitiesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_resource_functionalities operation
        get_resource_functionalities_input_type = type.StructType('operation-input', {
            'resource_type': type.OptionalType(type.StringType()),
            'functionality_type': type.OptionalType(type.StringType()),
            'resource_ids': type.OptionalType(type.ListType(type.StringType())),
            'is_allowed': type.OptionalType(type.BooleanType()),
            'parent_resource_type': type.OptionalType(type.StringType()),
        })
        get_resource_functionalities_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_resource_functionalities_input_value_validator_list = [
        ]
        get_resource_functionalities_output_validator_list = [
        ]
        get_resource_functionalities_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/resource-functionalities',
            path_variables={
            },
            query_parameters={
                'resource_type': 'resourceType',
                'functionality_type': 'functionalityType',
                'resource_ids': 'resourceIds',
                'is_allowed': 'isAllowed',
                'parent_resource_type': 'parentResourceType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update_resources_functionalities operation
        update_resources_functionalities_input_type = type.StructType('operation-input', {
            'resource_functionalities_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceFunctionalitiesUpdateSpec'),
        })
        update_resources_functionalities_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_resources_functionalities_input_value_validator_list = [
        ]
        update_resources_functionalities_output_validator_list = [
        ]
        update_resources_functionalities_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/resource-functionalities',
            request_body_parameter='resource_functionalities_update_spec',
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
            'get_resource_functionalities': {
                'input_type': get_resource_functionalities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfResourceFunctionalities')),
                'errors': get_resource_functionalities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_resource_functionalities_input_value_validator_list,
                'output_validator_list': get_resource_functionalities_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_resources_functionalities': {
                'input_type': update_resources_functionalities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceFunctionalitiesCaller')),
                'errors': update_resources_functionalities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_resources_functionalities_input_value_validator_list,
                'output_validator_list': update_resources_functionalities_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_resource_functionalities': get_resource_functionalities_rest_metadata,
            'update_resources_functionalities': update_resources_functionalities_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.resource_functionalities',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CredentialsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_credentials operation
        get_credentials_input_type = type.StructType('operation-input', {
            'resource_name': type.OptionalType(type.StringType()),
            'resource_ip': type.OptionalType(type.StringType()),
            'resource_type': type.OptionalType(type.StringType()),
            'domain_name': type.OptionalType(type.StringType()),
            'page_number': type.OptionalType(type.StringType()),
            'page_size': type.OptionalType(type.StringType()),
            'account_type': type.OptionalType(type.StringType()),
        })
        get_credentials_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credentials_input_value_validator_list = [
        ]
        get_credentials_output_validator_list = [
        ]
        get_credentials_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials',
            path_variables={
            },
            query_parameters={
                'resource_name': 'resourceName',
                'resource_ip': 'resourceIp',
                'resource_type': 'resourceType',
                'domain_name': 'domainName',
                'page_number': 'pageNumber',
                'page_size': 'pageSize',
                'account_type': 'accountType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update_or_rotate_passwords operation
        update_or_rotate_passwords_input_type = type.StructType('operation-input', {
            'credentials_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CredentialsUpdateSpec'),
        })
        update_or_rotate_passwords_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_or_rotate_passwords_input_value_validator_list = [
        ]
        update_or_rotate_passwords_output_validator_list = [
        ]
        update_or_rotate_passwords_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/credentials',
            request_body_parameter='credentials_update_spec',
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

        # properties for get_credential operation
        get_credential_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_credential_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_credential_input_value_validator_list = [
        ]
        get_credential_output_validator_list = [
        ]
        get_credential_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/credentials/{id}',
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
            'get_credentials': {
                'input_type': get_credentials_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCredential')),
                'errors': get_credentials_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,403,400]).build(),
                'input_value_validator_list': get_credentials_input_value_validator_list,
                'output_validator_list': get_credentials_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_or_rotate_passwords': {
                'input_type': update_or_rotate_passwords_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_or_rotate_passwords_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,403,400]).build(),
                'input_value_validator_list': update_or_rotate_passwords_input_value_validator_list,
                'output_validator_list': update_or_rotate_passwords_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_credential': {
                'input_type': get_credential_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Credential')),
                'errors': get_credential_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,404,403,400]).build(),
                'input_value_validator_list': get_credential_input_value_validator_list,
                'output_validator_list': get_credential_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_credentials': get_credentials_rest_metadata,
            'update_or_rotate_passwords': update_or_rotate_passwords_rest_metadata,
            'get_credential': get_credential_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.credentials',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcfServicesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_services operation
        get_vcf_services_input_type = type.StructType('operation-input', {})
        get_vcf_services_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_services_input_value_validator_list = [
        ]
        get_vcf_services_output_validator_list = [
        ]
        get_vcf_services_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-services',
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

        # properties for get_vcf_service operation
        get_vcf_service_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vcf_service_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcf_service_input_value_validator_list = [
        ]
        get_vcf_service_output_validator_list = [
        ]
        get_vcf_service_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-services/{id}',
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
            'get_vcf_services': {
                'input_type': get_vcf_services_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVcfService')),
                'errors': get_vcf_services_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_vcf_services_input_value_validator_list,
                'output_validator_list': get_vcf_services_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vcf_service': {
                'input_type': get_vcf_service_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VcfService')),
                'errors': get_vcf_service_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_vcf_service_input_value_validator_list,
                'output_validator_list': get_vcf_service_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_services': get_vcf_services_rest_metadata,
            'get_vcf_service': get_vcf_service_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcf_services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcentersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcenters operation
        get_vcenters_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_vcenters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcenters_input_value_validator_list = [
        ]
        get_vcenters_output_validator_list = [
        ]
        get_vcenters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcenters',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_vcenter operation
        get_vcenter_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vcenter_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vcenter_input_value_validator_list = [
        ]
        get_vcenter_output_validator_list = [
        ]
        get_vcenter_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcenters/{id}',
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
            'get_vcenters': {
                'input_type': get_vcenters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVcenter')),
                'errors': get_vcenters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_vcenters_input_value_validator_list,
                'output_validator_list': get_vcenters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vcenter': {
                'input_type': get_vcenter_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Vcenter')),
                'errors': get_vcenter_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_vcenter_input_value_validator_list,
                'output_validator_list': get_vcenter_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcenters': get_vcenters_rest_metadata,
            'get_vcenter': get_vcenter_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.vcenters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SsoDomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_SSO_domains operation
        get_SSO_domains_input_type = type.StructType('operation-input', {})
        get_SSO_domains_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_SSO_domains_input_value_validator_list = [
        ]
        get_SSO_domains_output_validator_list = [
        ]
        get_SSO_domains_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sso-domains',
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
            'get_SSO_domains': {
                'input_type': get_SSO_domains_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfString')),
                'errors': get_SSO_domains_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,403,500]).build(),
                'input_value_validator_list': get_SSO_domains_input_value_validator_list,
                'output_validator_list': get_SSO_domains_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_SSO_domains': get_SSO_domains_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.sso_domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SddcManagersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_sddc_managers operation
        get_sddc_managers_input_type = type.StructType('operation-input', {})
        get_sddc_managers_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_sddc_managers_input_value_validator_list = [
        ]
        get_sddc_managers_output_validator_list = [
        ]
        get_sddc_managers_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddc-managers',
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

        # properties for get_sddc_manager operation
        get_sddc_manager_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_sddc_manager_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_sddc_manager_input_value_validator_list = [
        ]
        get_sddc_manager_output_validator_list = [
        ]
        get_sddc_manager_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddc-managers/{id}',
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
            'get_sddc_managers': {
                'input_type': get_sddc_managers_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfSddcManager')),
                'errors': get_sddc_managers_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_sddc_managers_input_value_validator_list,
                'output_validator_list': get_sddc_managers_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_sddc_manager': {
                'input_type': get_sddc_manager_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'SddcManager')),
                'errors': get_sddc_manager_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_sddc_manager_input_value_validator_list,
                'output_validator_list': get_sddc_manager_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_sddc_managers': get_sddc_managers_rest_metadata,
            'get_sddc_manager': get_sddc_manager_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.sddc_managers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _RolesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_roles operation
        get_roles_input_type = type.StructType('operation-input', {})
        get_roles_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_roles_input_value_validator_list = [
        ]
        get_roles_output_validator_list = [
        ]
        get_roles_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/roles',
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
            'get_roles': {
                'input_type': get_roles_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfRole')),
                'errors': get_roles_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,500,400]).build(),
                'input_value_validator_list': get_roles_input_value_validator_list,
                'output_validator_list': get_roles_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_roles': get_roles_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.roles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ReleasesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_releases operation
        get_releases_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
            'version_eq': type.OptionalType(type.StringType()),
            'version_gt': type.OptionalType(type.StringType()),
            'version_ge': type.OptionalType(type.StringType()),
            'applicable_for_version': type.OptionalType(type.StringType()),
            'min_installer_version_le': type.OptionalType(type.StringType()),
            'get_future_releases': type.OptionalType(type.BooleanType()),
            'include_only_compatible': type.OptionalType(type.BooleanType()),
        })
        get_releases_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_releases_input_value_validator_list = [
        ]
        get_releases_output_validator_list = [
        ]
        get_releases_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
                'version_eq': 'versionEq',
                'version_gt': 'versionGt',
                'version_ge': 'versionGe',
                'applicable_for_version': 'applicableForVersion',
                'min_installer_version_le': 'minInstallerVersionLe',
                'get_future_releases': 'getFutureReleases',
                'include_only_compatible': 'includeOnlyCompatible',
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
            'get_releases': {
                'input_type': get_releases_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfRelease')),
                'errors': get_releases_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,403,500]).build(),
                'input_value_validator_list': get_releases_input_value_validator_list,
                'output_validator_list': get_releases_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_releases': get_releases_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.releases',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _PscsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_pscs operation
        get_pscs_input_type = type.StructType('operation-input', {})
        get_pscs_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_pscs_input_value_validator_list = [
        ]
        get_pscs_output_validator_list = [
        ]
        get_pscs_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/pscs',
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

        # properties for get_psc operation
        get_psc_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_psc_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_psc_input_value_validator_list = [
        ]
        get_psc_output_validator_list = [
        ]
        get_psc_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/pscs/{id}',
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
            'get_pscs': {
                'input_type': get_pscs_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfPsc')),
                'errors': get_pscs_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_pscs_input_value_validator_list,
                'output_validator_list': get_pscs_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_psc': {
                'input_type': get_psc_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Psc')),
                'errors': get_psc_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_psc_input_value_validator_list,
                'output_validator_list': get_psc_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_pscs': get_pscs_rest_metadata,
            'get_psc': get_psc_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.pscs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _NsxtClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_nsx_clusters operation
        get_nsx_clusters_input_type = type.StructType('operation-input', {
            'is_shareable': type.OptionalType(type.BooleanType()),
            'v_center_version': type.OptionalType(type.StringType()),
        })
        get_nsx_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_clusters_input_value_validator_list = [
        ]
        get_nsx_clusters_output_validator_list = [
        ]
        get_nsx_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters',
            path_variables={
            },
            query_parameters={
                'is_shareable': 'isShareable',
                'v_center_version': 'vCenterVersion',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_nsx_cluster operation
        get_nsx_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_nsx_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_cluster_input_value_validator_list = [
        ]
        get_nsx_cluster_output_validator_list = [
        ]
        get_nsx_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{id}',
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
            'get_nsx_clusters': {
                'input_type': get_nsx_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNsxtCluster')),
                'errors': get_nsx_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_nsx_clusters_input_value_validator_list,
                'output_validator_list': get_nsx_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_nsx_cluster': {
                'input_type': get_nsx_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtCluster')),
                'errors': get_nsx_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_nsx_cluster_input_value_validator_list,
                'output_validator_list': get_nsx_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_nsx_clusters': get_nsx_clusters_rest_metadata,
            'get_nsx_cluster': get_nsx_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _NotificationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_notifications operation
        get_notifications_input_type = type.StructType('operation-input', {})
        get_notifications_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_notifications_input_value_validator_list = [
        ]
        get_notifications_output_validator_list = [
        ]
        get_notifications_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/notifications',
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
            'get_notifications': {
                'input_type': get_notifications_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'Notification'))),
                'errors': get_notifications_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_notifications_input_value_validator_list,
                'output_validator_list': get_notifications_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_notifications': get_notifications_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.notifications',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _LicensingInfoStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_license_information operation
        get_license_information_input_type = type.StructType('operation-input', {
            'resource_type': type.OptionalType(type.StringType()),
            'resource_ids': type.OptionalType(type.ListType(type.StringType())),
        })
        get_license_information_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_license_information_input_value_validator_list = [
        ]
        get_license_information_output_validator_list = [
        ]
        get_license_information_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/licensing-info',
            path_variables={
            },
            query_parameters={
                'resource_type': 'resourceType',
                'resource_ids': 'resourceIds',
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
            'get_license_information': {
                'input_type': get_license_information_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'LicensingInfo'))),
                'errors': get_license_information_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_license_information_input_value_validator_list,
                'output_validator_list': get_license_information_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_license_information': get_license_information_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.licensing_info',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ConfigDriftsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_configs operation
        get_configs_input_type = type.StructType('operation-input', {
            'resource_id': type.OptionalType(type.StringType()),
            'resource_type': type.OptionalType(type.StringType()),
            'config_id': type.OptionalType(type.StringType()),
            'drift_type': type.OptionalType(type.StringType()),
            'include_failed': type.OptionalType(type.BooleanType()),
            'size': type.OptionalType(type.IntegerType()),
            'page': type.OptionalType(type.IntegerType()),
        })
        get_configs_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_configs_input_value_validator_list = [
        ]
        get_configs_output_validator_list = [
        ]
        get_configs_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/config-drifts',
            path_variables={
            },
            query_parameters={
                'resource_id': 'resourceId',
                'resource_type': 'resourceType',
                'config_id': 'configId',
                'drift_type': 'driftType',
                'include_failed': 'includeFailed',
                'size': 'size',
                'page': 'page',
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
            'get_configs': {
                'input_type': get_configs_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfConfigDriftSpec')),
                'errors': get_configs_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,503]).build(),
                'input_value_validator_list': get_configs_input_value_validator_list,
                'output_validator_list': get_configs_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_configs': get_configs_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.config_drifts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ComplianceStandardsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_standards operation
        get_compliance_standards_input_type = type.StructType('operation-input', {})
        get_compliance_standards_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_standards_input_value_validator_list = [
        ]
        get_compliance_standards_output_validator_list = [
        ]
        get_compliance_standards_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compliance-standards',
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
            'get_compliance_standards': {
                'input_type': get_compliance_standards_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceStandard')),
                'errors': get_compliance_standards_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,500]).build(),
                'input_value_validator_list': get_compliance_standards_input_value_validator_list,
                'output_validator_list': get_compliance_standards_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_standards': get_compliance_standards_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compliance_standards',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ComplianceConfigurationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_configurations operation
        get_compliance_configurations_input_type = type.StructType('operation-input', {
            'standard_type': type.OptionalType(type.StringType()),
            'standard_version': type.OptionalType(type.StringType()),
            'resource_type': type.OptionalType(type.StringType()),
            'resource_version': type.OptionalType(type.StringType()),
        })
        get_compliance_configurations_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_configurations_input_value_validator_list = [
        ]
        get_compliance_configurations_output_validator_list = [
        ]
        get_compliance_configurations_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compliance-configurations',
            path_variables={
            },
            query_parameters={
                'standard_type': 'standardType',
                'standard_version': 'standardVersion',
                'resource_type': 'resourceType',
                'resource_version': 'resourceVersion',
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
            'get_compliance_configurations': {
                'input_type': get_compliance_configurations_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceConfiguration')),
                'errors': get_compliance_configurations_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,400,500]).build(),
                'input_value_validator_list': get_compliance_configurations_input_value_validator_list,
                'output_validator_list': get_compliance_configurations_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_configurations': get_compliance_configurations_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compliance_configurations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ComplianceAuditsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_audit_history operation
        get_compliance_audit_history_input_type = type.StructType('operation-input', {})
        get_compliance_audit_history_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_history_input_value_validator_list = [
        ]
        get_compliance_audit_history_output_validator_list = [
        ]
        get_compliance_audit_history_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compliance-audits',
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

        # properties for get_compliance_audit operation
        get_compliance_audit_input_type = type.StructType('operation-input', {
            'compliance_audit_id': type.StringType(),
        })
        get_compliance_audit_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_input_value_validator_list = [
        ]
        get_compliance_audit_output_validator_list = [
        ]
        get_compliance_audit_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compliance-audits/{complianceAuditId}',
            path_variables={
                'compliance_audit_id': 'complianceAuditId',
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
            'get_compliance_audit_history': {
                'input_type': get_compliance_audit_history_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceAudit')),
                'errors': get_compliance_audit_history_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_history_input_value_validator_list,
                'output_validator_list': get_compliance_audit_history_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_compliance_audit': {
                'input_type': get_compliance_audit_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceAudit')),
                'errors': get_compliance_audit_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_input_value_validator_list,
                'output_validator_list': get_compliance_audit_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_audit_history': get_compliance_audit_history_rest_metadata,
            'get_compliance_audit': get_compliance_audit_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compliance_audits',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CompatibilityMatrices': CompatibilityMatrices,
        'CertificateAuthorities': CertificateAuthorities,
        'VcfManagementComponents': VcfManagementComponents,
        'VasaProviders': VasaProviders,
        'Users': Users,
        'Upgrades': Upgrades,
        'Tokens': Tokens,
        'ResourceWarnings': ResourceWarnings,
        'ProductVersionCatalogs': ProductVersionCatalogs,
        'ProductVersionCatalog': ProductVersionCatalog,
        'ProductBinaries': ProductBinaries,
        'Personalities': Personalities,
        'NsxAlbClusters': NsxAlbClusters,
        'NetworkPools': NetworkPools,
        'Manifests': Manifests,
        'LicenseKeys': LicenseKeys,
        'IdentityProviders': IdentityProviders,
        'Hosts': Hosts,
        'EdgeClusters': EdgeClusters,
        'Domains': Domains,
        'ConfigDriftReconciliations': ConfigDriftReconciliations,
        'Clusters': Clusters,
        'Bundles': Bundles,
        'AlbClusters': AlbClusters,
        'VsanHcl': VsanHcl,
        'Tasks': Tasks,
        'System': System,
        'ResourceFunctionalities': ResourceFunctionalities,
        'Credentials': Credentials,
        'VcfServices': VcfServices,
        'Vcenters': Vcenters,
        'SsoDomains': SsoDomains,
        'SddcManagers': SddcManagers,
        'Roles': Roles,
        'Releases': Releases,
        'Pscs': Pscs,
        'NsxtClusters': NsxtClusters,
        'Notifications': Notifications,
        'LicensingInfo': LicensingInfo,
        'ConfigDrifts': ConfigDrifts,
        'ComplianceStandards': ComplianceStandards,
        'ComplianceConfigurations': ComplianceConfigurations,
        'ComplianceAudits': ComplianceAudits,
        'alb_clusters': 'vmware.sddc_manager.v1.alb_clusters_client.StubFactory',
        'backups': 'vmware.sddc_manager.v1.backups_client.StubFactory',
        'bundles': 'vmware.sddc_manager.v1.bundles_client.StubFactory',
        'clusters': 'vmware.sddc_manager.v1.clusters_client.StubFactory',
        'compatibility_matrices': 'vmware.sddc_manager.v1.compatibility_matrices_client.StubFactory',
        'compliance_audits': 'vmware.sddc_manager.v1.compliance_audits_client.StubFactory',
        'credentials': 'vmware.sddc_manager.v1.credentials_client.StubFactory',
        'domains': 'vmware.sddc_manager.v1.domains_client.StubFactory',
        'edge_clusters': 'vmware.sddc_manager.v1.edge_clusters_client.StubFactory',
        'hosts': 'vmware.sddc_manager.v1.hosts_client.StubFactory',
        'identity_broker': 'vmware.sddc_manager.v1.identity_broker_client.StubFactory',
        'identity_providers': 'vmware.sddc_manager.v1.identity_providers_client.StubFactory',
        'license_keys': 'vmware.sddc_manager.v1.license_keys_client.StubFactory',
        'licensing_info': 'vmware.sddc_manager.v1.licensing_info_client.StubFactory',
        'network_pools': 'vmware.sddc_manager.v1.network_pools_client.StubFactory',
        'nsx_alb_clusters': 'vmware.sddc_manager.v1.nsx_alb_clusters_client.StubFactory',
        'nsxt_clusters': 'vmware.sddc_manager.v1.nsxt_clusters_client.StubFactory',
        'personalities': 'vmware.sddc_manager.v1.personalities_client.StubFactory',
        'product_version_catalogs': 'vmware.sddc_manager.v1.product_version_catalogs_client.StubFactory',
        'releases': 'vmware.sddc_manager.v1.releases_client.StubFactory',
        'resource_functionalities': 'vmware.sddc_manager.v1.resource_functionalities_client.StubFactory',
        'resources': 'vmware.sddc_manager.v1.resources_client.StubFactory',
        'restores': 'vmware.sddc_manager.v1.restores_client.StubFactory',
        'sddc_manager': 'vmware.sddc_manager.v1.sddc_manager_client.StubFactory',
        'sddc_managers': 'vmware.sddc_manager.v1.sddc_managers_client.StubFactory',
        'sddcs': 'vmware.sddc_manager.v1.sddcs_client.StubFactory',
        'sso_domains': 'vmware.sddc_manager.v1.sso_domains_client.StubFactory',
        'system': 'vmware.sddc_manager.v1.system_client.StubFactory',
        'tokens': 'vmware.sddc_manager.v1.tokens_client.StubFactory',
        'upgradables': 'vmware.sddc_manager.v1.upgradables_client.StubFactory',
        'upgrades': 'vmware.sddc_manager.v1.upgrades_client.StubFactory',
        'users': 'vmware.sddc_manager.v1.users_client.StubFactory',
        'vasa_providers': 'vmware.sddc_manager.v1.vasa_providers_client.StubFactory',
        'vcf_management_components': 'vmware.sddc_manager.v1.vcf_management_components_client.StubFactory',
        'vsan_hcl': 'vmware.sddc_manager.v1.vsan_hcl_client.StubFactory',
    }

