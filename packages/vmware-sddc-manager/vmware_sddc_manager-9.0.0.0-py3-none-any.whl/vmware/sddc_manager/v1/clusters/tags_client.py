# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.clusters.tags.
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


class TagManager(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.tags.tag_manager'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TagManagerStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cluster_tag_manager_url(self,
                                    id,
                                    ):
        """
        

        :type  id: :class:`str`
        :param id: Cluster ID
        :rtype: :class:`vmware.sddc_manager.model_client.TagManagerModel` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_cluster_tag_manager_url',
                            {
                            'id': id,
                            })
class AssignableTags(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.clusters.tags.assignable_tags'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AssignableTagsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_tag_assignable_for_cluster(self,
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
        return self._invoke('get_tag_assignable_for_cluster',
                            {
                            'id': id,
                            })
class _TagManagerStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_cluster_tag_manager_url operation
        get_cluster_tag_manager_url_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_cluster_tag_manager_url_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_cluster_tag_manager_url_input_value_validator_list = [
        ]
        get_cluster_tag_manager_url_output_validator_list = [
        ]
        get_cluster_tag_manager_url_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/tags/tag-manager',
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
            'get_cluster_tag_manager_url': {
                'input_type': get_cluster_tag_manager_url_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagManagerModel')),
                'errors': get_cluster_tag_manager_url_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_cluster_tag_manager_url_input_value_validator_list,
                'output_validator_list': get_cluster_tag_manager_url_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_cluster_tag_manager_url': get_cluster_tag_manager_url_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.tags.tag_manager',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _AssignableTagsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_tag_assignable_for_cluster operation
        get_tag_assignable_for_cluster_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_tag_assignable_for_cluster_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tag_assignable_for_cluster_input_value_validator_list = [
        ]
        get_tag_assignable_for_cluster_output_validator_list = [
        ]
        get_tag_assignable_for_cluster_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/clusters/{id}/tags/assignable-tags',
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
            'get_tag_assignable_for_cluster': {
                'input_type': get_tag_assignable_for_cluster_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTag')),
                'errors': get_tag_assignable_for_cluster_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tag_assignable_for_cluster_input_value_validator_list,
                'output_validator_list': get_tag_assignable_for_cluster_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_tag_assignable_for_cluster': get_tag_assignable_for_cluster_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.clusters.tags.assignable_tags',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'TagManager': TagManager,
        'AssignableTags': AssignableTags,
    }

