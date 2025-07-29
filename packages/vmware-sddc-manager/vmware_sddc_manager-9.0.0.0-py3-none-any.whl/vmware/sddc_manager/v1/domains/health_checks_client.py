# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.health_checks.
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


class Tasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.health_checks.tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vsan_health_check_by_task_id(self,
                                         domain_id,
                                         task_id,
                                         ):
        """
        Get vSAN health check update task status for a given task Id

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  task_id: :class:`str`
        :param task_id: Health check task id
        :rtype: :class:`vmware.sddc_manager.model_client.HealthCheckTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vsan_health_check_by_task_ID',
                            {
                            'domain_id': domain_id,
                            'task_id': task_id,
                            })
class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.health_checks.queries'
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


    def get_vsan_health_check_by_query_id(self,
                                          domain_id,
                                          query_id,
                                          ):
        """
        Get vSAN health check status for a given Query Id

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  query_id: :class:`str`
        :param query_id: Query ID
        :rtype: :class:`vmware.sddc_manager.model_client.HealthCheckQueryResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_vsan_health_check_by_query_ID',
                            {
                            'domain_id': domain_id,
                            'query_id': query_id,
                            })
class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vsan_health_check_by_task_ID operation
        get_vsan_health_check_by_task_ID_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'task_id': type.StringType(),
        })
        get_vsan_health_check_by_task_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vsan_health_check_by_task_ID_input_value_validator_list = [
        ]
        get_vsan_health_check_by_task_ID_output_validator_list = [
        ]
        get_vsan_health_check_by_task_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/health-checks/tasks/{taskId}',
            path_variables={
                'domain_id': 'domainId',
                'task_id': 'taskId',
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
            'get_vsan_health_check_by_task_ID': {
                'input_type': get_vsan_health_check_by_task_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthCheckTask')),
                'errors': get_vsan_health_check_by_task_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_vsan_health_check_by_task_ID_input_value_validator_list,
                'output_validator_list': get_vsan_health_check_by_task_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vsan_health_check_by_task_ID': get_vsan_health_check_by_task_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.health_checks.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vsan_health_check_by_query_ID operation
        get_vsan_health_check_by_query_ID_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'query_id': type.StringType(),
        })
        get_vsan_health_check_by_query_ID_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vsan_health_check_by_query_ID_input_value_validator_list = [
        ]
        get_vsan_health_check_by_query_ID_output_validator_list = [
        ]
        get_vsan_health_check_by_query_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/health-checks/queries/{queryId}',
            path_variables={
                'domain_id': 'domainId',
                'query_id': 'queryId',
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
            'get_vsan_health_check_by_query_ID': {
                'input_type': get_vsan_health_check_by_query_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthCheckQueryResult')),
                'errors': get_vsan_health_check_by_query_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_vsan_health_check_by_query_ID_input_value_validator_list,
                'output_validator_list': get_vsan_health_check_by_query_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vsan_health_check_by_query_ID': get_vsan_health_check_by_query_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.health_checks.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tasks': Tasks,
        'Queries': Queries,
    }

