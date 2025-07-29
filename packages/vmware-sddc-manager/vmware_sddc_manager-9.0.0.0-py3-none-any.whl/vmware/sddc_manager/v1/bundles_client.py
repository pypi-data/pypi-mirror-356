# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.bundles.
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


class DownloadStatus(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.bundles.download_status'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DownloadStatusStub)
        self._VAPI_OPERATION_IDS = {}


    def get_bundle_download_status(self,
                                   release_version=None,
                                   bundle_id=None,
                                   image_type=None,
                                   ):
        """
        Get all download status for all bundles matching the criteria. Returns
        the download information (status, error, taskId) for all bundles
        matching the criteria (release version, bundle Id, image type).

        :type  release_version: :class:`str` or ``None``
        :param release_version: Get download status for bundles that are associated with a specific
            release.
        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: Get the download status for a specific bundle by bundleId.
        :type  image_type: :class:`str` or ``None``
        :param image_type: The image type of the bundle, either INSTALL or PATCH
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfBundleDownloadStatusInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_bundle_download_status',
                            {
                            'release_version': release_version,
                            'bundle_id': bundle_id,
                            'image_type': image_type,
                            })
class Domains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.bundles.domains'
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


    def get_bundles_for_skip_upgrade(self,
                                     id,
                                     target_version=None,
                                     ):
        """
        Get bundles for skip upgrade a domain from current version to target
        version (for SDDC Manager only). NOTE: This operation is not applicable
        if appliance is in VCF Installer mode.

        :type  id: :class:`str`
        :param id: Domain ID
        :type  target_version: :class:`str` or ``None``
        :param target_version: [Deprecated] Target domain VCF version
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfBundle` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_bundles_for_skip_upgrade',
                            {
                            'id': id,
                            'target_version': target_version,
                            })
class _DownloadStatusStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_bundle_download_status operation
        get_bundle_download_status_input_type = type.StructType('operation-input', {
            'release_version': type.OptionalType(type.StringType()),
            'bundle_id': type.OptionalType(type.StringType()),
            'image_type': type.OptionalType(type.StringType()),
        })
        get_bundle_download_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_bundle_download_status_input_value_validator_list = [
        ]
        get_bundle_download_status_output_validator_list = [
        ]
        get_bundle_download_status_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles/download-status',
            path_variables={
            },
            query_parameters={
                'release_version': 'releaseVersion',
                'bundle_id': 'bundleId',
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
            'get_bundle_download_status': {
                'input_type': get_bundle_download_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfBundleDownloadStatusInfo')),
                'errors': get_bundle_download_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_bundle_download_status_input_value_validator_list,
                'output_validator_list': get_bundle_download_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_bundle_download_status': get_bundle_download_status_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.bundles.download_status',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_bundles_for_skip_upgrade operation
        get_bundles_for_skip_upgrade_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'target_version': type.OptionalType(type.StringType()),
        })
        get_bundles_for_skip_upgrade_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_bundles_for_skip_upgrade_input_value_validator_list = [
        ]
        get_bundles_for_skip_upgrade_output_validator_list = [
        ]
        get_bundles_for_skip_upgrade_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles/domains/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'target_version': 'targetVersion',
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
            'get_bundles_for_skip_upgrade': {
                'input_type': get_bundles_for_skip_upgrade_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfBundle')),
                'errors': get_bundles_for_skip_upgrade_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_bundles_for_skip_upgrade_input_value_validator_list,
                'output_validator_list': get_bundles_for_skip_upgrade_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_bundles_for_skip_upgrade': get_bundles_for_skip_upgrade_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.bundles.domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'DownloadStatus': DownloadStatus,
        'Domains': Domains,
    }

