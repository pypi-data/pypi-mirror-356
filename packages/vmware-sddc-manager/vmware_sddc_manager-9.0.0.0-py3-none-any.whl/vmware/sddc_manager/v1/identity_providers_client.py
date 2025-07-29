# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.identity_providers.
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


class SyncClient(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.identity_providers.sync_client'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SyncClientStub)
        self._VAPI_OPERATION_IDS = {}


    def generate_sync_client_token(self,
                                   id,
                                   sync_client_token_ttl=None,
                                   ):
        """
        Generates a new sync client token

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :type  sync_client_token_ttl: :class:`long` or ``None``
        :param sync_client_token_ttl: TTL of the sync client token
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. IDP is not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        """
        return self._invoke('generate_sync_client_token',
                            {
                            'id': id,
                            'sync_client_token_ttl': sync_client_token_ttl,
                            })
class IdentitySources(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.identity_providers.identity_sources'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IdentitySourcesStub)
        self._VAPI_OPERATION_IDS = {}


    def add_embedded_identity_source(self,
                                     id,
                                     identity_source_spec,
                                     ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :type  identity_source_spec: :class:`vmware.sddc_manager.model_client.IdentitySourceSpec`
        :param identity_source_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Identity Provider not found
        """
        return self._invoke('add_embedded_identity_source',
                            {
                            'id': id,
                            'identity_source_spec': identity_source_spec,
                            })

    def delete_identity_source(self,
                               id,
                               domain_name,
                               ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :type  domain_name: :class:`str`
        :param domain_name: Domain Name associated with the identity source
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Identity Source not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('delete_identity_source',
                            {
                            'id': id,
                            'domain_name': domain_name,
                            })

    def update_embedded_identity_source(self,
                                        id,
                                        domain_name,
                                        identity_source_spec,
                                        ):
        """
        No content

        :type  id: :class:`str`
        :param id: ID of Identity Provider
        :type  domain_name: :class:`str`
        :param domain_name: Domain Name associated with the identity source
        :type  identity_source_spec: :class:`vmware.sddc_manager.model_client.IdentitySourceSpec`
        :param identity_source_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Identity Source not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_embedded_identity_source',
                            {
                            'id': id,
                            'domain_name': domain_name,
                            'identity_source_spec': identity_source_spec,
                            })
class _SyncClientStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for generate_sync_client_token operation
        generate_sync_client_token_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'sync_client_token_TTL': type.OptionalType(type.IntegerType()),
        })
        generate_sync_client_token_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        generate_sync_client_token_input_value_validator_list = [
        ]
        generate_sync_client_token_output_validator_list = [
        ]
        generate_sync_client_token_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/identity-providers/{id}/sync-client',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'sync_client_token_TTL': 'syncClientTokenTTL',
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
            'generate_sync_client_token': {
                'input_type': generate_sync_client_token_input_type,
                'output_type': type.VoidType(),
                'errors': generate_sync_client_token_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,401]).build(),
                'input_value_validator_list': generate_sync_client_token_input_value_validator_list,
                'output_validator_list': generate_sync_client_token_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'generate_sync_client_token': generate_sync_client_token_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.identity_providers.sync_client',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _IdentitySourcesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for add_embedded_identity_source operation
        add_embedded_identity_source_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'identity_source_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'IdentitySourceSpec'),
        })
        add_embedded_identity_source_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_embedded_identity_source_input_value_validator_list = [
        ]
        add_embedded_identity_source_output_validator_list = [
        ]
        add_embedded_identity_source_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/identity-providers/{id}/identity-sources',
            request_body_parameter='identity_source_spec',
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

        # properties for delete_identity_source operation
        delete_identity_source_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'domain_name': type.StringType(),
        })
        delete_identity_source_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_identity_source_input_value_validator_list = [
        ]
        delete_identity_source_output_validator_list = [
        ]
        delete_identity_source_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/identity-providers/{id}/identity-sources/{domainName}',
            path_variables={
                'id': 'id',
                'domain_name': 'domainName',
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

        # properties for update_embedded_identity_source operation
        update_embedded_identity_source_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'domain_name': type.StringType(),
            'identity_source_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'IdentitySourceSpec'),
        })
        update_embedded_identity_source_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_embedded_identity_source_input_value_validator_list = [
        ]
        update_embedded_identity_source_output_validator_list = [
        ]
        update_embedded_identity_source_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/identity-providers/{id}/identity-sources/{domainName}',
            request_body_parameter='identity_source_spec',
            path_variables={
                'id': 'id',
                'domain_name': 'domainName',
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
            'add_embedded_identity_source': {
                'input_type': add_embedded_identity_source_input_type,
                'output_type': type.VoidType(),
                'errors': add_embedded_identity_source_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400,404]).build(),
                'input_value_validator_list': add_embedded_identity_source_input_value_validator_list,
                'output_validator_list': add_embedded_identity_source_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_identity_source': {
                'input_type': delete_identity_source_input_type,
                'output_type': type.VoidType(),
                'errors': delete_identity_source_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': delete_identity_source_input_value_validator_list,
                'output_validator_list': delete_identity_source_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_embedded_identity_source': {
                'input_type': update_embedded_identity_source_input_type,
                'output_type': type.VoidType(),
                'errors': update_embedded_identity_source_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': update_embedded_identity_source_input_value_validator_list,
                'output_validator_list': update_embedded_identity_source_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'add_embedded_identity_source': add_embedded_identity_source_rest_metadata,
            'delete_identity_source': delete_identity_source_rest_metadata,
            'update_embedded_identity_source': update_embedded_identity_source_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.identity_providers.identity_sources',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'SyncClient': SyncClient,
        'IdentitySources': IdentitySources,
    }

