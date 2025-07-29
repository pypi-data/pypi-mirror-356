# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.upgradables.domains.
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


class Nsxt(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgradables.domains.nsxt'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NsxtStub)
        self._VAPI_OPERATION_IDS = {}


    def get_nsx_upgrade_resources(self,
                                  domain_id,
                                  bundle_id=None,
                                  ):
        """
        Get the list NSX upgradable reosurce with resource metadata info

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: bundle Id of the upgrade bundle applicable on the domain
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtResources` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Bundle Not Found
        """
        return self._invoke('get_nsx_upgrade_resources',
                            {
                            'domain_id': domain_id,
                            'bundle_id': bundle_id,
                            })
class Clusters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgradables.domains.clusters'
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


    def get_upgradables_clusters(self,
                                 domain_id,
                                 ):
        """
        Fetches the list of available hardware support managers and configured
        hardware support managers for the give resource along with the hardware
        support packages and Software details.

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUpgradablesClusterResource` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain Not Found
        """
        return self._invoke('get_upgradables_clusters',
                            {
                            'domain_id': domain_id,
                            })
class _NsxtStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_nsx_upgrade_resources operation
        get_nsx_upgrade_resources_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'bundle_id': type.OptionalType(type.StringType()),
        })
        get_nsx_upgrade_resources_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_upgrade_resources_input_value_validator_list = [
        ]
        get_nsx_upgrade_resources_output_validator_list = [
        ]
        get_nsx_upgrade_resources_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgradables/domains/{domainId}/nsxt',
            path_variables={
                'domain_id': 'domainId',
            },
            query_parameters={
                'bundle_id': 'bundleId',
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
            'get_nsx_upgrade_resources': {
                'input_type': get_nsx_upgrade_resources_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtResources')),
                'errors': get_nsx_upgrade_resources_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_nsx_upgrade_resources_input_value_validator_list,
                'output_validator_list': get_nsx_upgrade_resources_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_nsx_upgrade_resources': get_nsx_upgrade_resources_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgradables.domains.nsxt',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_upgradables_clusters operation
        get_upgradables_clusters_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
        })
        get_upgradables_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgradables_clusters_input_value_validator_list = [
        ]
        get_upgradables_clusters_output_validator_list = [
        ]
        get_upgradables_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgradables/domains/{domainId}/clusters',
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
            'get_upgradables_clusters': {
                'input_type': get_upgradables_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgradablesClusterResource')),
                'errors': get_upgradables_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_upgradables_clusters_input_value_validator_list,
                'output_validator_list': get_upgradables_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_upgradables_clusters': get_upgradables_clusters_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgradables.domains.clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Nsxt': Nsxt,
        'Clusters': Clusters,
    }

