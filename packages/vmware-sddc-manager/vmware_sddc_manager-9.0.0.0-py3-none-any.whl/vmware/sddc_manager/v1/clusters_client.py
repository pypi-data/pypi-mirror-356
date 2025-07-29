# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.clusters.
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


class Tags(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.tags'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TagsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_tags_assigned_to_cluster(self,
                                     id,
                                     ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTag` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_tags_assigned_to_cluster',
                            {
                            'id': id,
                            })

    def assign_tags_to_cluster(self,
                               id,
                               tags_spec,
                               ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('assign_tags_to_cluster',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def remove_tags_from_cluster(self,
                                 id,
                                 tags_spec,
                                 ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('remove_tags_from_cluster',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def get_tags_assigned_to_clusters(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTagsForResource` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_tags_assigned_to_clusters', None)
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.validations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ValidationsStub)
        self._VAPI_OPERATION_IDS = {}


    def validate_cluster_update_spec(self,
                                     id,
                                     cluster_update_spec,
                                     use_async_validation=None,
                                     ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  cluster_update_spec: :class:`vmware.sddc_manager.model_client.ClusterUpdateSpec`
        :param cluster_update_spec: 
        :type  use_async_validation: :class:`bool` or ``None``
        :param use_async_validation: Cluster validations to be run async
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_cluster_update_spec',
                            {
                            'id': id,
                            'cluster_update_spec': cluster_update_spec,
                            'use_async_validation': use_async_validation,
                            })

    def validate_cluster_creation_spec(self,
                                       cluster_creation_spec,
                                       hosts_only=None,
                                       skip_host_switch_validation=None,
                                       ):
        """
        

        :type  cluster_creation_spec: :class:`vmware.sddc_manager.model_client.ClusterCreationSpec`
        :param cluster_creation_spec: 
        :type  hosts_only: :class:`bool` or ``None``
        :param hosts_only: Validate hosts only
        :type  skip_host_switch_validation: :class:`bool` or ``None``
        :param skip_host_switch_validation: Skips host switch validation when hostOnly=true
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_cluster_creation_spec',
                            {
                            'cluster_creation_spec': cluster_creation_spec,
                            'hosts_only': hosts_only,
                            'skip_host_switch_validation': skip_host_switch_validation,
                            })

    def get_cluster_update_validation(self,
                                      id,
                                      validation_id,
                                      use_async_validation=None,
                                      ):
        """
        Gets the status of given cluster updates validation workflow by given
        validation id

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  validation_id: :class:`str`
        :param validation_id: Cluster validation workflow id
        :type  use_async_validation: :class:`bool` or ``None``
        :param use_async_validation: Cluster validation result for async validations
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_cluster_update_validation',
                            {
                            'id': id,
                            'validation_id': validation_id,
                            'use_async_validation': use_async_validation,
                            })

    def get_cluster_create_validation(self,
                                      id,
                                      ):
        """
        Gets the status of given cluster create validation workflow by given
        validation id

        :type  id: :class:`str`
        :param id: Cluster validation workflow id
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_cluster_create_validation',
                            {
                            'id': id,
                            })
class Datastores(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.datastores'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DatastoresStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cluster_datastores(self,
                               id,
                               ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.Datastore` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Cluster Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_datastores',
                            {
                            'id': id,
                            })

    def add_datastore_to_cluster(self,
                                 id,
                                 datastore_mount_spec,
                                 ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  datastore_mount_spec: :class:`vmware.sddc_manager.model_client.DatastoreMountSpec`
        :param datastore_mount_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('add_datastore_to_cluster',
                            {
                            'id': id,
                            'datastore_mount_spec': datastore_mount_spec,
                            })

    def remove_datastore_from_cluster(self,
                                      id,
                                      datastore_id,
                                      ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :type  datastore_id: :class:`str`
        :param datastore_id: Datastore ID
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('remove_datastore_from_cluster',
                            {
                            'id': id,
                            'datastore_id': datastore_id,
                            })
class Vdses(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.vdses'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VdsesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vdses(self,
                  cluster_id,
                  ):
        """
        

        :type  cluster_id: :class:`str`
        :param cluster_id: Cluster ID
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.Vds` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Cluster Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_vdses',
                            {
                            'cluster_id': cluster_id,
                            })

    def import_vds_to_inventory(self,
                                cluster_id,
                                import_vds_spec,
                                ):
        """
        

        :type  cluster_id: :class:`str`
        :param cluster_id: Cluster ID
        :type  import_vds_spec: :class:`vmware.sddc_manager.model_client.ImportVdsSpec`
        :param import_vds_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('import_vds_to_inventory',
                            {
                            'cluster_id': cluster_id,
                            'import_vds_spec': import_vds_spec,
                            })
class ImageCompliance(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.image_compliance'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ImageComplianceStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cluster_image_compliance(self,
                                     id,
                                     ):
        """
        Get image compliance for a Cluster

        :type  id: :class:`str`
        :param id: Cluster Id
        :rtype: :class:`vmware.sddc_manager.model_client.ClusterImageCompliance` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Cluster image compliance not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_image_compliance',
                            {
                            'id': id,
                            })
class _TagsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_tags_assigned_to_cluster operation
        get_tags_assigned_to_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_tags_assigned_to_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_cluster_input_value_validator_list = [
        ]
        get_tags_assigned_to_cluster_output_validator_list = [
        ]
        get_tags_assigned_to_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/tags',
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

        # properties for assign_tags_to_cluster operation
        assign_tags_to_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        assign_tags_to_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        assign_tags_to_cluster_input_value_validator_list = [
        ]
        assign_tags_to_cluster_output_validator_list = [
        ]
        assign_tags_to_cluster_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/clusters/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for remove_tags_from_cluster operation
        remove_tags_from_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        remove_tags_from_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_tags_from_cluster_input_value_validator_list = [
        ]
        remove_tags_from_cluster_output_validator_list = [
        ]
        remove_tags_from_cluster_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/clusters/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for get_tags_assigned_to_clusters operation
        get_tags_assigned_to_clusters_input_type = type.StructType('operation-input', {})
        get_tags_assigned_to_clusters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_clusters_input_value_validator_list = [
        ]
        get_tags_assigned_to_clusters_output_validator_list = [
        ]
        get_tags_assigned_to_clusters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/tags',
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
            'get_tags_assigned_to_cluster': {
                'input_type': get_tags_assigned_to_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTag')),
                'errors': get_tags_assigned_to_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_cluster_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'assign_tags_to_cluster': {
                'input_type': assign_tags_to_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': assign_tags_to_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': assign_tags_to_cluster_input_value_validator_list,
                'output_validator_list': assign_tags_to_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_tags_from_cluster': {
                'input_type': remove_tags_from_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': remove_tags_from_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': remove_tags_from_cluster_input_value_validator_list,
                'output_validator_list': remove_tags_from_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_tags_assigned_to_clusters': {
                'input_type': get_tags_assigned_to_clusters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTagsForResource')),
                'errors': get_tags_assigned_to_clusters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_clusters_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_clusters_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_tags_assigned_to_cluster': get_tags_assigned_to_cluster_rest_metadata,
            'assign_tags_to_cluster': assign_tags_to_cluster_rest_metadata,
            'remove_tags_from_cluster': remove_tags_from_cluster_rest_metadata,
            'get_tags_assigned_to_clusters': get_tags_assigned_to_clusters_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.tags',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_cluster_update_spec operation
        validate_cluster_update_spec_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'cluster_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterUpdateSpec'),
            'use_async_validation': type.OptionalType(type.BooleanType()),
        })
        validate_cluster_update_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_cluster_update_spec_input_value_validator_list = [
        ]
        validate_cluster_update_spec_output_validator_list = [
        ]
        validate_cluster_update_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{id}/validations',
            request_body_parameter='cluster_update_spec',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'use_async_validation': 'useAsyncValidation',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for validate_cluster_creation_spec operation
        validate_cluster_creation_spec_input_type = type.StructType('operation-input', {
            'cluster_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterCreationSpec'),
            'hosts_only': type.OptionalType(type.BooleanType()),
            'skip_host_switch_validation': type.OptionalType(type.BooleanType()),
        })
        validate_cluster_creation_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_cluster_creation_spec_input_value_validator_list = [
        ]
        validate_cluster_creation_spec_output_validator_list = [
        ]
        validate_cluster_creation_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/validations',
            request_body_parameter='cluster_creation_spec',
            path_variables={
            },
            query_parameters={
                'hosts_only': 'hostsOnly',
                'skip_host_switch_validation': 'skipHostSwitchValidation',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_cluster_update_validation operation
        get_cluster_update_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'validation_id': type.StringType(),
            'use_async_validation': type.OptionalType(type.BooleanType()),
        })
        get_cluster_update_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_update_validation_input_value_validator_list = [
        ]
        get_cluster_update_validation_output_validator_list = [
        ]
        get_cluster_update_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/validations/{validationId}',
            path_variables={
                'id': 'id',
                'validation_id': 'validationId',
            },
            query_parameters={
                'use_async_validation': 'useAsyncValidation',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_cluster_create_validation operation
        get_cluster_create_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_create_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_create_validation_input_value_validator_list = [
        ]
        get_cluster_create_validation_output_validator_list = [
        ]
        get_cluster_create_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/validations/{id}',
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
            'validate_cluster_update_spec': {
                'input_type': validate_cluster_update_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_cluster_update_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': validate_cluster_update_spec_input_value_validator_list,
                'output_validator_list': validate_cluster_update_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate_cluster_creation_spec': {
                'input_type': validate_cluster_creation_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_cluster_creation_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_cluster_creation_spec_input_value_validator_list,
                'output_validator_list': validate_cluster_creation_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster_update_validation': {
                'input_type': get_cluster_update_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_cluster_update_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404]).build(),
                'input_value_validator_list': get_cluster_update_validation_input_value_validator_list,
                'output_validator_list': get_cluster_update_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_cluster_create_validation': {
                'input_type': get_cluster_create_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_cluster_create_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404]).build(),
                'input_value_validator_list': get_cluster_create_validation_input_value_validator_list,
                'output_validator_list': get_cluster_create_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_cluster_update_spec': validate_cluster_update_spec_rest_metadata,
            'validate_cluster_creation_spec': validate_cluster_creation_spec_rest_metadata,
            'get_cluster_update_validation': get_cluster_update_validation_rest_metadata,
            'get_cluster_create_validation': get_cluster_create_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DatastoresStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_datastores operation
        get_cluster_datastores_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_datastores_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_datastores_input_value_validator_list = [
        ]
        get_cluster_datastores_output_validator_list = [
        ]
        get_cluster_datastores_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/datastores',
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

        # properties for add_datastore_to_cluster operation
        add_datastore_to_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'datastore_mount_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DatastoreMountSpec'),
        })
        add_datastore_to_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        add_datastore_to_cluster_input_value_validator_list = [
        ]
        add_datastore_to_cluster_output_validator_list = [
        ]
        add_datastore_to_cluster_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{id}/datastores',
            request_body_parameter='datastore_mount_spec',
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

        # properties for remove_datastore_from_cluster operation
        remove_datastore_from_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'datastore_id': type.StringType(),
        })
        remove_datastore_from_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_datastore_from_cluster_input_value_validator_list = [
        ]
        remove_datastore_from_cluster_output_validator_list = [
        ]
        remove_datastore_from_cluster_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/clusters/{id}/datastores/{datastoreId}',
            path_variables={
                'id': 'id',
                'datastore_id': 'datastoreId',
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
            'get_cluster_datastores': {
                'input_type': get_cluster_datastores_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'Datastore'))),
                'errors': get_cluster_datastores_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_cluster_datastores_input_value_validator_list,
                'output_validator_list': get_cluster_datastores_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_datastore_to_cluster': {
                'input_type': add_datastore_to_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': add_datastore_to_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': add_datastore_to_cluster_input_value_validator_list,
                'output_validator_list': add_datastore_to_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_datastore_from_cluster': {
                'input_type': remove_datastore_from_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': remove_datastore_from_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': remove_datastore_from_cluster_input_value_validator_list,
                'output_validator_list': remove_datastore_from_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_datastores': get_cluster_datastores_rest_metadata,
            'add_datastore_to_cluster': add_datastore_to_cluster_rest_metadata,
            'remove_datastore_from_cluster': remove_datastore_from_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.datastores',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VdsesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vdses operation
        get_vdses_input_type = type.StructType('operation-input', {
            'cluster_id': type.StringType(),
        })
        get_vdses_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vdses_input_value_validator_list = [
        ]
        get_vdses_output_validator_list = [
        ]
        get_vdses_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{clusterId}/vdses',
            path_variables={
                'cluster_id': 'clusterId',
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

        # properties for import_vds_to_inventory operation
        import_vds_to_inventory_input_type = type.StructType('operation-input', {
            'cluster_id': type.StringType(),
            'import_vds_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ImportVdsSpec'),
        })
        import_vds_to_inventory_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        import_vds_to_inventory_input_value_validator_list = [
        ]
        import_vds_to_inventory_output_validator_list = [
        ]
        import_vds_to_inventory_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/clusters/{clusterId}/vdses',
            request_body_parameter='import_vds_spec',
            path_variables={
                'cluster_id': 'clusterId',
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
            'get_vdses': {
                'input_type': get_vdses_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'Vds'))),
                'errors': get_vdses_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_vdses_input_value_validator_list,
                'output_validator_list': get_vdses_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'import_vds_to_inventory': {
                'input_type': import_vds_to_inventory_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': import_vds_to_inventory_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': import_vds_to_inventory_input_value_validator_list,
                'output_validator_list': import_vds_to_inventory_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vdses': get_vdses_rest_metadata,
            'import_vds_to_inventory': import_vds_to_inventory_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.vdses',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ImageComplianceStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_image_compliance operation
        get_cluster_image_compliance_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_image_compliance_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_image_compliance_input_value_validator_list = [
        ]
        get_cluster_image_compliance_output_validator_list = [
        ]
        get_cluster_image_compliance_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/image-compliance',
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
            'get_cluster_image_compliance': {
                'input_type': get_cluster_image_compliance_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ClusterImageCompliance')),
                'errors': get_cluster_image_compliance_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_cluster_image_compliance_input_value_validator_list,
                'output_validator_list': get_cluster_image_compliance_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_image_compliance': get_cluster_image_compliance_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.image_compliance',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tags': Tags,
        'Validations': Validations,
        'Datastores': Datastores,
        'Vdses': Vdses,
        'ImageCompliance': ImageCompliance,
        'datastores': 'vmware.sddc_manager.v1.clusters.datastores_client.StubFactory',
        'hosts': 'vmware.sddc_manager.v1.clusters.hosts_client.StubFactory',
        'network': 'vmware.sddc_manager.v1.clusters.network_client.StubFactory',
        'tags': 'vmware.sddc_manager.v1.clusters.tags_client.StubFactory',
    }

