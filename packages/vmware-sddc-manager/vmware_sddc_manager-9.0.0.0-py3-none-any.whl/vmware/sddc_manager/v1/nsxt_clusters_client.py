# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.nsxt_clusters.
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


class ScaleOut(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.scale_out'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ScaleOutStub)
        self._VAPI_OPERATION_IDS = {}


    def scale_out_nsx(self,
                      nsxt_cluster_id,
                      nsx_deployment_spec,
                      ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :type  nsx_deployment_spec: :class:`vmware.sddc_manager.model_client.NsxDeploymentSpec`
        :param nsx_deployment_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('scale_out_nsx',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            'nsx_deployment_spec': nsx_deployment_spec,
                            })
class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.queries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _QueriesStub)
        self._VAPI_OPERATION_IDS = {}


    def start_nsx_criteria_query(self,
                                 nsxt_criterion,
                                 ):
        """
        

        :type  nsxt_criterion: :class:`vmware.sddc_manager.model_client.NsxtCriterion`
        :param nsxt_criterion: 
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtQueryResponse` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('start_nsx_criteria_query',
                            {
                            'nsxt_criterion': nsxt_criterion,
                            })

    def get_nsx_cluster_query_response(self,
                                       id,
                                       ):
        """
        

        :type  id: :class:`str`
        :param id: 
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtQueryResponse` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Query Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_cluster_query_response',
                            {
                            'id': id,
                            })
class Oidcs(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.oidcs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _OidcsStub)
        self._VAPI_OPERATION_IDS = {}


    def connect_open_id(self,
                        nsxt_oidc_spec,
                        ):
        """
        OK

        :type  nsxt_oidc_spec: :class:`vmware.sddc_manager.model_client.NsxtOidcSpec`
        :param nsxt_oidc_spec: 
        """
        return self._invoke('connect_open_id',
                            {
                            'nsxt_oidc_spec': nsxt_oidc_spec,
                            })
class Projects(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.projects'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProjectsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_projects(self,
                     nsxt_cluster_id,
                     is_compatible_with_supervisor=None,
                     ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :type  is_compatible_with_supervisor: :class:`bool` or ``None``
        :param is_compatible_with_supervisor: Query Param to fetch Projects compatible with Supervisor
            Enablement. Set it to true to filter Projects compatible with
            Supervisor Enablement. If this query param is not provided or set
            to false, then it will return all Projects for a given NSX-T
            Cluster.
        :rtype: :class:`vmware.sddc_manager.model_client.Page` or ``None``
        :return: OK
        """
        return self._invoke('get_projects',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            'is_compatible_with_supervisor': is_compatible_with_supervisor,
                            })
class VpcConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.vpc_configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VpcConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vpc_configuration(self,
                              nsxt_cluster_id,
                              ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.VpcConfiguration` or ``None``
        :return: OK
        """
        return self._invoke('get_vpc_configuration',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            })
class TransportZones(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.transport_zones'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TransportZonesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_nsx_transport_zones(self,
                                nsxt_cluster_id,
                                ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNsxtTransportZoneInfo` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_transport_zones',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            })
class IpAddressPools(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IpAddressPoolsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_nsx_ip_address_pools(self,
                                 nsxt_cluster_id,
                                 ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNsxtIpAddressPool` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. IP address pools not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_ip_address_pools',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            })

    def get_nsx_ip_address_pool(self,
                                nsxt_cluster_id,
                                name,
                                ):
        """
        

        :type  nsxt_cluster_id: :class:`str`
        :param nsxt_cluster_id: NSX cluster ID
        :type  name: :class:`str`
        :param name: IP address pool name
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtIpAddressPool` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. IP address pool not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_nsx_ip_address_pool',
                            {
                            'nsxt_cluster_id': nsxt_cluster_id,
                            'name': name,
                            })
class Criteria(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.nsxt_clusters.criteria'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CriteriaStub)
        self._VAPI_OPERATION_IDS = {}


    def get_nsx_criteria(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfNsxtCriterion` or ``None``
        :return: Ok
        """
        return self._invoke('get_nsx_criteria', None)

    def get_nsx_criterion(self,
                          name,
                          ):
        """
        

        :type  name: :class:`str`
        :param name: 
        :rtype: :class:`vmware.sddc_manager.model_client.NsxtCriterion` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Criterion Not Found
        """
        return self._invoke('get_nsx_criterion',
                            {
                            'name': name,
                            })
class _ScaleOutStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for scale_out_nsx operation
        scale_out_nsx_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
            'nsx_deployment_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxDeploymentSpec'),
        })
        scale_out_nsx_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        scale_out_nsx_input_value_validator_list = [
        ]
        scale_out_nsx_output_validator_list = [
        ]
        scale_out_nsx_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/scale-out',
            request_body_parameter='nsx_deployment_spec',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
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
            'scale_out_nsx': {
                'input_type': scale_out_nsx_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': scale_out_nsx_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': scale_out_nsx_input_value_validator_list,
                'output_validator_list': scale_out_nsx_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'scale_out_nsx': scale_out_nsx_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.scale_out',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for start_nsx_criteria_query operation
        start_nsx_criteria_query_input_type = type.StructType('operation-input', {
            'nsxt_criterion': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtCriterion'),
        })
        start_nsx_criteria_query_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_nsx_criteria_query_input_value_validator_list = [
        ]
        start_nsx_criteria_query_output_validator_list = [
        ]
        start_nsx_criteria_query_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsxt-clusters/queries',
            request_body_parameter='nsxt_criterion',
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

        # properties for get_nsx_cluster_query_response operation
        get_nsx_cluster_query_response_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_nsx_cluster_query_response_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_cluster_query_response_input_value_validator_list = [
        ]
        get_nsx_cluster_query_response_output_validator_list = [
        ]
        get_nsx_cluster_query_response_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/queries/{id}',
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
            'start_nsx_criteria_query': {
                'input_type': start_nsx_criteria_query_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtQueryResponse')),
                'errors': start_nsx_criteria_query_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': start_nsx_criteria_query_input_value_validator_list,
                'output_validator_list': start_nsx_criteria_query_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_nsx_cluster_query_response': {
                'input_type': get_nsx_cluster_query_response_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtQueryResponse')),
                'errors': get_nsx_cluster_query_response_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': get_nsx_cluster_query_response_input_value_validator_list,
                'output_validator_list': get_nsx_cluster_query_response_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'start_nsx_criteria_query': start_nsx_criteria_query_rest_metadata,
            'get_nsx_cluster_query_response': get_nsx_cluster_query_response_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _OidcsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for connect_open_id operation
        connect_open_id_input_type = type.StructType('operation-input', {
            'nsxt_oidc_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtOidcSpec'),
        })
        connect_open_id_error_dict = {}
        connect_open_id_input_value_validator_list = [
        ]
        connect_open_id_output_validator_list = [
        ]
        connect_open_id_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/nsxt-clusters/oidcs',
            request_body_parameter='nsxt_oidc_spec',
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
            'connect_open_id': {
                'input_type': connect_open_id_input_type,
                'output_type': type.VoidType(),
                'errors': connect_open_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': connect_open_id_input_value_validator_list,
                'output_validator_list': connect_open_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'connect_open_id': connect_open_id_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.oidcs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ProjectsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_projects operation
        get_projects_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
            'is_compatible_with_supervisor': type.OptionalType(type.BooleanType()),
        })
        get_projects_error_dict = {}
        get_projects_input_value_validator_list = [
        ]
        get_projects_output_validator_list = [
        ]
        get_projects_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/projects',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
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
            'get_projects': {
                'input_type': get_projects_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Page')),
                'errors': get_projects_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_projects_input_value_validator_list,
                'output_validator_list': get_projects_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_projects': get_projects_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.projects',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VpcConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vpc_configuration operation
        get_vpc_configuration_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
        })
        get_vpc_configuration_error_dict = {}
        get_vpc_configuration_input_value_validator_list = [
        ]
        get_vpc_configuration_output_validator_list = [
        ]
        get_vpc_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/vpc-configuration',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
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
            'get_vpc_configuration': {
                'input_type': get_vpc_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VpcConfiguration')),
                'errors': get_vpc_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_vpc_configuration_input_value_validator_list,
                'output_validator_list': get_vpc_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vpc_configuration': get_vpc_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.vpc_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TransportZonesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_nsx_transport_zones operation
        get_nsx_transport_zones_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
        })
        get_nsx_transport_zones_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_transport_zones_input_value_validator_list = [
        ]
        get_nsx_transport_zones_output_validator_list = [
        ]
        get_nsx_transport_zones_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/transport-zones',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
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
            'get_nsx_transport_zones': {
                'input_type': get_nsx_transport_zones_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNsxtTransportZoneInfo')),
                'errors': get_nsx_transport_zones_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_nsx_transport_zones_input_value_validator_list,
                'output_validator_list': get_nsx_transport_zones_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_nsx_transport_zones': get_nsx_transport_zones_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.transport_zones',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _IpAddressPoolsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_nsx_ip_address_pools operation
        get_nsx_ip_address_pools_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
        })
        get_nsx_ip_address_pools_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_ip_address_pools_input_value_validator_list = [
        ]
        get_nsx_ip_address_pools_output_validator_list = [
        ]
        get_nsx_ip_address_pools_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/ip-address-pools',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
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

        # properties for get_nsx_ip_address_pool operation
        get_nsx_ip_address_pool_input_type = type.StructType('operation-input', {
            'nsxt_cluster_id': type.StringType(),
            'name': type.StringType(),
        })
        get_nsx_ip_address_pool_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_ip_address_pool_input_value_validator_list = [
        ]
        get_nsx_ip_address_pool_output_validator_list = [
        ]
        get_nsx_ip_address_pool_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/{nsxtClusterId}/ip-address-pools/{name}',
            path_variables={
                'nsxt_cluster_id': 'nsxtClusterId',
                'name': 'name',
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
            'get_nsx_ip_address_pools': {
                'input_type': get_nsx_ip_address_pools_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNsxtIpAddressPool')),
                'errors': get_nsx_ip_address_pools_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_nsx_ip_address_pools_input_value_validator_list,
                'output_validator_list': get_nsx_ip_address_pools_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_nsx_ip_address_pool': {
                'input_type': get_nsx_ip_address_pool_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtIpAddressPool')),
                'errors': get_nsx_ip_address_pool_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_nsx_ip_address_pool_input_value_validator_list,
                'output_validator_list': get_nsx_ip_address_pool_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_nsx_ip_address_pools': get_nsx_ip_address_pools_rest_metadata,
            'get_nsx_ip_address_pool': get_nsx_ip_address_pool_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_nsx_criteria operation
        get_nsx_criteria_input_type = type.StructType('operation-input', {})
        get_nsx_criteria_error_dict = {}
        get_nsx_criteria_input_value_validator_list = [
        ]
        get_nsx_criteria_output_validator_list = [
        ]
        get_nsx_criteria_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/criteria',
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

        # properties for get_nsx_criterion operation
        get_nsx_criterion_input_type = type.StructType('operation-input', {
            'name': type.StringType(),
        })
        get_nsx_criterion_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_nsx_criterion_input_value_validator_list = [
        ]
        get_nsx_criterion_output_validator_list = [
        ]
        get_nsx_criterion_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/nsxt-clusters/criteria/{name}',
            path_variables={
                'name': 'name',
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
            'get_nsx_criteria': {
                'input_type': get_nsx_criteria_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfNsxtCriterion')),
                'errors': get_nsx_criteria_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_nsx_criteria_input_value_validator_list,
                'output_validator_list': get_nsx_criteria_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_nsx_criterion': {
                'input_type': get_nsx_criterion_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NsxtCriterion')),
                'errors': get_nsx_criterion_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404]).build(),
                'input_value_validator_list': get_nsx_criterion_input_value_validator_list,
                'output_validator_list': get_nsx_criterion_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_nsx_criteria': get_nsx_criteria_rest_metadata,
            'get_nsx_criterion': get_nsx_criterion_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.nsxt_clusters.criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ScaleOut': ScaleOut,
        'Queries': Queries,
        'Oidcs': Oidcs,
        'Projects': Projects,
        'VpcConfiguration': VpcConfiguration,
        'TransportZones': TransportZones,
        'IpAddressPools': IpAddressPools,
        'Criteria': Criteria,
        'ip_address_pools': 'vmware.sddc_manager.v1.nsxt_clusters.ip_address_pools_client.StubFactory',
        'projects': 'vmware.sddc_manager.v1.nsxt_clusters.projects_client.StubFactory',
    }

