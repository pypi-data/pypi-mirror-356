# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.nsxt_clusters.projects.
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


class VpcConnectivityProfiles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.projects.vpc_connectivity_profiles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VpcConnectivityProfilesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vpc_connectivity_profiles(self,
                                      nsxt_cluster_id,
                                      project_id,
                                      is_compatible_with_supervisor=None,
                                      ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :type  project_id: :class:`str`
        :param project_id: Project ID
        :type  is_compatible_with_supervisor: :class:`bool` or ``None``
        :param is_compatible_with_supervisor: Query Param to fetch VPC Connectivity Profiles compatible with
            Supervisor Enablement. Set it to true to filter VPC Connectivity
            Profiles compatible with Supervisor Enablement. If this query param
            is not provided or set to false, then it will return all VPC
            Connectivity Profiles for a given NSX-T cluster and Project
        :rtype: :class:`vmware.sddc_manager.model_client.Page` or ``None``
        :return: OK
        """
        return self._invoke('get_vpc_connectivity_profiles',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            'project_id': project_id,
                            'is_compatible_with_supervisor': is_compatible_with_supervisor,
                            })
class _VpcConnectivityProfilesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vpc_connectivity_profiles operation
        get_vpc_connectivity_profiles_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
            'project_id': type.StringType(),
            'is_compatible_with_supervisor': type.OptionalType(type.BooleanType()),
        })
        get_vpc_connectivity_profiles_error_dict = {}
        get_vpc_connectivity_profiles_input_value_validator_list = [
        ]
        get_vpc_connectivity_profiles_output_validator_list = [
        ]
        get_vpc_connectivity_profiles_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/projects/{projectId}/vpc-connectivity-profiles',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
                'project_id': 'projectId',
            },
            query_parameters={
                'is_compatible_with_supervisor': 'isCompatibleWithSupervisor',
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
            'get_vpc_connectivity_profiles': {
                'input_type': get_vpc_connectivity_profiles_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Page')),
                'errors': get_vpc_connectivity_profiles_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_vpc_connectivity_profiles_input_value_validator_list,
                'output_validator_list': get_vpc_connectivity_profiles_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vpc_connectivity_profiles': get_vpc_connectivity_profiles_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.projects.vpc_connectivity_profiles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'VpcConnectivityProfiles': VpcConnectivityProfiles,
    }

