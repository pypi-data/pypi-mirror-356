# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.upgrades.
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


class Prechecks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgrades.prechecks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrechecksStub)
        self._VAPI_OPERATION_IDS = {}


    def start_upgrade_precheck(self,
                               upgrade_id,
                               ):
        """
        Perform Upgrade Prechecks

        :type  upgrade_id: :class:`str`
        :param upgrade_id: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Upgrade Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Operation not allowed
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('start_upgrade_precheck',
                            {
                            'upgrade_id': upgrade_id,
                            })

    def get_upgrade_precheck_by_id(self,
                                   upgrade_id,
                                   precheck_id,
                                   ):
        """
        Gets upgrade precheck details

        :type  upgrade_id: :class:`str`
        :param upgrade_id: 
        :type  precheck_id: :class:`str`
        :param precheck_id: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Operation not allowed
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_upgrade_precheck_by_ID',
                            {
                            'upgrade_id': upgrade_id,
                            'precheck_id': precheck_id,
                            })
class Preview(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgrades.preview'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PreviewStub)
        self._VAPI_OPERATION_IDS = {}


    def get_upgrade_preview(self,
                            bundle_id=None,
                            domain_id=None,
                            ):
        """
        Get the list of resources for a given domain which the bundle will be
        applied; Note: Domain ID is ignored for SDDC Manager (EVORACK) bundle
        type since the bundle is always applied to all the management domains

        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: Bundle Id
        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Domain Id
        :rtype: :class:`vmware.sddc_manager.model_client.UpgradePreview` or ``None``
        :return: Success
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Bundle or Domain Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request Error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_upgrade_preview',
                            {
                            'bundle_id': bundle_id,
                            'domain_id': domain_id,
                            })
class _PrechecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for start_upgrade_precheck operation
        start_upgrade_precheck_input_type = type.StructType('operation-input', {
            'upgrade_id': type.StringType(),
        })
        start_upgrade_precheck_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_upgrade_precheck_input_value_validator_list = [
        ]
        start_upgrade_precheck_output_validator_list = [
        ]
        start_upgrade_precheck_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/upgrades/{upgradeId}/prechecks',
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

        # properties for get_upgrade_precheck_by_ID operation
        get_upgrade_precheck_by_ID_input_type = type.StructType('operation-input', {
            'upgrade_id': type.StringType(),
            'precheck_id': type.StringType(),
        })
        get_upgrade_precheck_by_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgrade_precheck_by_ID_input_value_validator_list = [
        ]
        get_upgrade_precheck_by_ID_output_validator_list = [
        ]
        get_upgrade_precheck_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgrades/{upgradeId}/prechecks/{precheckId}',
            path_variables={
                'upgrade_id': 'upgradeId',
                'precheck_id': 'precheckId',
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
            'start_upgrade_precheck': {
                'input_type': start_upgrade_precheck_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': start_upgrade_precheck_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500,403,400]).build(),
                'input_value_validator_list': start_upgrade_precheck_input_value_validator_list,
                'output_validator_list': start_upgrade_precheck_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_upgrade_precheck_by_ID': {
                'input_type': get_upgrade_precheck_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': get_upgrade_precheck_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,403,404,400]).build(),
                'input_value_validator_list': get_upgrade_precheck_by_ID_input_value_validator_list,
                'output_validator_list': get_upgrade_precheck_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'start_upgrade_precheck': start_upgrade_precheck_rest_metadata,
            'get_upgrade_precheck_by_ID': get_upgrade_precheck_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgrades.prechecks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _PreviewStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_upgrade_preview operation
        get_upgrade_preview_input_type = type.StructType('operation-input', {
            'bundle_id': type.OptionalType(type.StringType()),
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_upgrade_preview_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgrade_preview_input_value_validator_list = [
        ]
        get_upgrade_preview_output_validator_list = [
        ]
        get_upgrade_preview_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgrades/preview',
            path_variables={
            },
            query_parameters={
                'bundle_id': 'bundleId',
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

        operations = {
            'get_upgrade_preview': {
                'input_type': get_upgrade_preview_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'UpgradePreview')),
                'errors': get_upgrade_preview_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_upgrade_preview_input_value_validator_list,
                'output_validator_list': get_upgrade_preview_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_upgrade_preview': get_upgrade_preview_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgrades.preview',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Prechecks': Prechecks,
        'Preview': Preview,
    }

