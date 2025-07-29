# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.settings.
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


class VersionAliases(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.settings.version_aliases'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VersionAliasesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_version_alias_configuration(self):
        """
        Get the Version Alias Configuration.


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVersionAliasesForBundleComponentType` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_version_alias_configuration', None)

    def update_version_alias_configurations(self,
                                            version_aliases_for_bundle_component_type_spec,
                                            ):
        """
        Update Version Alias Configurations.

        :type  version_aliases_for_bundle_component_type_spec: :class:`vmware.sddc_manager.model_client.VersionAliasesForBundleComponentTypeSpec`
        :param version_aliases_for_bundle_component_type_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVersionAliasesForBundleComponentType` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_version_alias_configurations',
                            {
                            'version_aliases_for_bundle_component_type_spec': version_aliases_for_bundle_component_type_spec,
                            })

    def update_version_alias_configuration(self,
                                           bundle_component_type,
                                           version,
                                           alias_spec,
                                           ):
        """
        Update Version Alias Configuration.

        :type  bundle_component_type: :class:`str`
        :param bundle_component_type: Bundle Component Type
        :type  version: :class:`str`
        :param version: Version
        :type  alias_spec: :class:`vmware.sddc_manager.model_client.AliasSpec`
        :param alias_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfVersionAliasesForBundleComponentType` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_version_alias_configuration',
                            {
                            'bundle_component_type': bundle_component_type,
                            'version': version,
                            'alias_spec': alias_spec,
                            })

    def delete_alias_versions_by_software_type_and_base_version(self,
                                                                bundle_component_type,
                                                                version,
                                                                delete_alias_versions_by_software_type_and_base_version_request_body=None,
                                                                ):
        """
        No COntent

        :type  bundle_component_type: :class:`str`
        :param bundle_component_type: Bundle Component Type
        :type  version: :class:`str`
        :param version: Version
        :type  delete_alias_versions_by_software_type_and_base_version_request_body: :class:`list` of :class:`str` or ``None``
        :param delete_alias_versions_by_software_type_and_base_version_request_body: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('delete_alias_versions_by_software_type_and_base_version',
                            {
                            'bundle_component_type': bundle_component_type,
                            'version': version,
                            'delete_alias_versions_by_software_type_and_base_version_request_body': delete_alias_versions_by_software_type_and_base_version_request_body,
                            })

    def delete_version_alias_by_software_type(self,
                                              bundle_component_type,
                                              ):
        """
        No COntent

        :type  bundle_component_type: :class:`str`
        :param bundle_component_type: Bundle Component Type
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('delete_version_alias_by_software_type',
                            {
                            'bundle_component_type': bundle_component_type,
                            })
class Depot(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.settings.depot'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DepotStub)
        self._VAPI_OPERATION_IDS = {}


    def get_depot_settings(self):
        """
        Get the depot configuration. In a fresh setup, this would be empty.


        :rtype: :class:`vmware.sddc_manager.model_client.DepotSettings` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_depot_settings', None)

    def update_depot_settings(self,
                              depot_settings,
                              ):
        """
        Update depot settings. Depot settings can be updated with VMware Depot
        account

        :type  depot_settings: :class:`vmware.sddc_manager.model_client.DepotSettings`
        :param depot_settings: 
        :rtype: :class:`vmware.sddc_manager.model_client.DepotSettings` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_depot_settings',
                            {
                            'depot_settings': depot_settings,
                            })

    def delete_depot_settings(self,
                              depot_type=None,
                              ):
        """
        No Content

        :type  depot_type: :class:`str` or ``None``
        :param depot_type: Depot Type
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_depot_settings',
                            {
                            'depot_type': depot_type,
                            })
class _VersionAliasesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_version_alias_configuration operation
        get_version_alias_configuration_input_type = type.StructType('operation-input', {})
        get_version_alias_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_version_alias_configuration_input_value_validator_list = [
        ]
        get_version_alias_configuration_output_validator_list = [
        ]
        get_version_alias_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/settings/version-aliases',
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

        # properties for update_version_alias_configurations operation
        update_version_alias_configurations_input_type = type.StructType('operation-input', {
            'version_aliases_for_bundle_component_type_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'VersionAliasesForBundleComponentTypeSpec'),
        })
        update_version_alias_configurations_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_version_alias_configurations_input_value_validator_list = [
        ]
        update_version_alias_configurations_output_validator_list = [
        ]
        update_version_alias_configurations_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/settings/version-aliases',
            request_body_parameter='version_aliases_for_bundle_component_type_spec',
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

        # properties for update_version_alias_configuration operation
        update_version_alias_configuration_input_type = type.StructType('operation-input', {
            'bundle_component_type': type.StringType(),
            'version': type.StringType(),
            'alias_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'AliasSpec'),
        })
        update_version_alias_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_version_alias_configuration_input_value_validator_list = [
        ]
        update_version_alias_configuration_output_validator_list = [
        ]
        update_version_alias_configuration_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/settings/version-aliases/{bundleComponentType}/{version}',
            request_body_parameter='alias_spec',
            path_variables={
                'bundle_component_type': 'bundleComponentType',
                'version': 'version',
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

        # properties for delete_alias_versions_by_software_type_and_base_version operation
        delete_alias_versions_by_software_type_and_base_version_input_type = type.StructType('operation-input', {
            'bundle_component_type': type.StringType(),
            'version': type.StringType(),
            'delete_alias_versions_by_software_type_and_base_version_request_body': type.OptionalType(type.ListType(type.StringType())),
        })
        delete_alias_versions_by_software_type_and_base_version_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_alias_versions_by_software_type_and_base_version_input_value_validator_list = [
        ]
        delete_alias_versions_by_software_type_and_base_version_output_validator_list = [
        ]
        delete_alias_versions_by_software_type_and_base_version_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/system/settings/version-aliases/{bundleComponentType}/{version}',
            request_body_parameter='delete_alias_versions_by_software_type_and_base_version_request_body',
            path_variables={
                'bundle_component_type': 'bundleComponentType',
                'version': 'version',
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

        # properties for delete_version_alias_by_software_type operation
        delete_version_alias_by_software_type_input_type = type.StructType('operation-input', {
            'bundle_component_type': type.StringType(),
        })
        delete_version_alias_by_software_type_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_version_alias_by_software_type_input_value_validator_list = [
        ]
        delete_version_alias_by_software_type_output_validator_list = [
        ]
        delete_version_alias_by_software_type_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/system/settings/version-aliases/{bundleComponentType}',
            path_variables={
                'bundle_component_type': 'bundleComponentType',
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
            'get_version_alias_configuration': {
                'input_type': get_version_alias_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVersionAliasesForBundleComponentType')),
                'errors': get_version_alias_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_version_alias_configuration_input_value_validator_list,
                'output_validator_list': get_version_alias_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_version_alias_configurations': {
                'input_type': update_version_alias_configurations_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVersionAliasesForBundleComponentType')),
                'errors': update_version_alias_configurations_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': update_version_alias_configurations_input_value_validator_list,
                'output_validator_list': update_version_alias_configurations_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_version_alias_configuration': {
                'input_type': update_version_alias_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfVersionAliasesForBundleComponentType')),
                'errors': update_version_alias_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': update_version_alias_configuration_input_value_validator_list,
                'output_validator_list': update_version_alias_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_alias_versions_by_software_type_and_base_version': {
                'input_type': delete_alias_versions_by_software_type_and_base_version_input_type,
                'output_type': type.VoidType(),
                'errors': delete_alias_versions_by_software_type_and_base_version_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': delete_alias_versions_by_software_type_and_base_version_input_value_validator_list,
                'output_validator_list': delete_alias_versions_by_software_type_and_base_version_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_version_alias_by_software_type': {
                'input_type': delete_version_alias_by_software_type_input_type,
                'output_type': type.VoidType(),
                'errors': delete_version_alias_by_software_type_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': delete_version_alias_by_software_type_input_value_validator_list,
                'output_validator_list': delete_version_alias_by_software_type_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_version_alias_configuration': get_version_alias_configuration_rest_metadata,
            'update_version_alias_configurations': update_version_alias_configurations_rest_metadata,
            'update_version_alias_configuration': update_version_alias_configuration_rest_metadata,
            'delete_alias_versions_by_software_type_and_base_version': delete_alias_versions_by_software_type_and_base_version_rest_metadata,
            'delete_version_alias_by_software_type': delete_version_alias_by_software_type_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.settings.version_aliases',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DepotStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_depot_settings operation
        get_depot_settings_input_type = type.StructType('operation-input', {})
        get_depot_settings_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_depot_settings_input_value_validator_list = [
        ]
        get_depot_settings_output_validator_list = [
        ]
        get_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/settings/depot',
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

        # properties for update_depot_settings operation
        update_depot_settings_input_type = type.StructType('operation-input', {
            'depot_settings': type.ReferenceType('vmware.sddc_manager.model_client', 'DepotSettings'),
        })
        update_depot_settings_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_depot_settings_input_value_validator_list = [
        ]
        update_depot_settings_output_validator_list = [
        ]
        update_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/settings/depot',
            request_body_parameter='depot_settings',
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

        # properties for delete_depot_settings operation
        delete_depot_settings_input_type = type.StructType('operation-input', {
            'depot_type': type.OptionalType(type.StringType()),
        })
        delete_depot_settings_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        delete_depot_settings_input_value_validator_list = [
        ]
        delete_depot_settings_output_validator_list = [
        ]
        delete_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/system/settings/depot',
            path_variables={
            },
            query_parameters={
                'depot_type': 'depotType',
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
            'get_depot_settings': {
                'input_type': get_depot_settings_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DepotSettings')),
                'errors': get_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_depot_settings_input_value_validator_list,
                'output_validator_list': get_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_depot_settings': {
                'input_type': update_depot_settings_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DepotSettings')),
                'errors': update_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_depot_settings_input_value_validator_list,
                'output_validator_list': update_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_depot_settings': {
                'input_type': delete_depot_settings_input_type,
                'output_type': type.VoidType(),
                'errors': delete_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': delete_depot_settings_input_value_validator_list,
                'output_validator_list': delete_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_depot_settings': get_depot_settings_rest_metadata,
            'update_depot_settings': update_depot_settings_rest_metadata,
            'delete_depot_settings': delete_depot_settings_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.settings.depot',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'VersionAliases': VersionAliases,
        'Depot': Depot,
        'depot': 'vmware.sddc_manager.v1.system.settings.depot_client.StubFactory',
    }

