# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.settings.depot.
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


class DepotSyncInfo(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.settings.depot.depot_sync_info'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DepotSyncInfoStub)
        self._VAPI_OPERATION_IDS = {}


    def get_depot_sync_info(self):
        """
        Get the depot sync information.


        :rtype: :class:`vmware.sddc_manager.model_client.DepotSyncInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_depot_sync_info', None)

    def sync_depot_metadata(self):
        """
        Sync depot metadata such as bundle manifest, pvc.


        :rtype: :class:`vmware.sddc_manager.model_client.DepotSyncInfo` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('sync_depot_metadata', None)
class _DepotSyncInfoStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_depot_sync_info operation
        get_depot_sync_info_input_type = type.StructType('operation-input', {})
        get_depot_sync_info_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_depot_sync_info_input_value_validator_list = [
        ]
        get_depot_sync_info_output_validator_list = [
        ]
        get_depot_sync_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/settings/depot/depot-sync-info',
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

        # properties for sync_depot_metadata operation
        sync_depot_metadata_input_type = type.StructType('operation-input', {})
        sync_depot_metadata_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        sync_depot_metadata_input_value_validator_list = [
        ]
        sync_depot_metadata_output_validator_list = [
        ]
        sync_depot_metadata_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/settings/depot/depot-sync-info',
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
            'get_depot_sync_info': {
                'input_type': get_depot_sync_info_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DepotSyncInfo')),
                'errors': get_depot_sync_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_depot_sync_info_input_value_validator_list,
                'output_validator_list': get_depot_sync_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'sync_depot_metadata': {
                'input_type': sync_depot_metadata_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DepotSyncInfo')),
                'errors': sync_depot_metadata_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': sync_depot_metadata_input_value_validator_list,
                'output_validator_list': sync_depot_metadata_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_depot_sync_info': get_depot_sync_info_rest_metadata,
            'sync_depot_metadata': sync_depot_metadata_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.settings.depot.depot_sync_info',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'DepotSyncInfo': DepotSyncInfo,
    }

