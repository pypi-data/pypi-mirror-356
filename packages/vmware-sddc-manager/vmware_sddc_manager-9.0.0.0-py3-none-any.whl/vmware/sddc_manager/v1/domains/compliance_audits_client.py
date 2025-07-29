# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.compliance_audits.
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

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.compliance_audits.tasks'
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


    def get_compliance_audit_task(self,
                                  id,
                                  task_id,
                                  ):
        """
        Get compliance audit task

        :type  id: :class:`str`
        :param id: Domain ID
        :type  task_id: :class:`str`
        :param task_id: Audit task ID
        :rtype: :class:`vmware.sddc_manager.model_client.ComplianceTask` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit_task',
                            {
                            'id': id,
                            'task_id': task_id,
                            })

    def retry_compliance_audit_task(self,
                                    id,
                                    task_id,
                                    ):
        """
        Retry compliance audit task

        :type  id: :class:`str`
        :param id: Domain ID
        :type  task_id: :class:`str`
        :param task_id: Audit task ID
        :rtype: :class:`vmware.sddc_manager.model_client.ComplianceTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('retry_compliance_audit_task',
                            {
                            'id': id,
                            'task_id': task_id,
                            })
class ComplianceAuditItems(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.compliance_audits.compliance_audit_items'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComplianceAuditItemsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compliance_audit_items_fora_domain(self,
                                               id,
                                               compliance_audit_id,
                                               ):
        """
        Get compliance audit items for a domain

        :type  id: :class:`str`
        :param id: Domain ID
        :type  compliance_audit_id: :class:`str`
        :param compliance_audit_id: Compliance Audit ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfComplianceAuditItem` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit_items_fora_domain',
                            {
                            'id': id,
                            'compliance_audit_id': compliance_audit_id,
                            })
class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_audit_task operation
        get_compliance_audit_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'task_id': type.StringType(),
        })
        get_compliance_audit_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_task_input_value_validator_list = [
        ]
        get_compliance_audit_task_output_validator_list = [
        ]
        get_compliance_audit_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/compliance-audits/tasks/{taskId}',
            path_variables={
                'id': 'id',
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

        # properties for retry_compliance_audit_task operation
        retry_compliance_audit_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'task_id': type.StringType(),
        })
        retry_compliance_audit_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        retry_compliance_audit_task_input_value_validator_list = [
        ]
        retry_compliance_audit_task_output_validator_list = [
        ]
        retry_compliance_audit_task_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{id}/compliance-audits/tasks/{taskId}',
            path_variables={
                'id': 'id',
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
            'get_compliance_audit_task': {
                'input_type': get_compliance_audit_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceTask')),
                'errors': get_compliance_audit_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_task_input_value_validator_list,
                'output_validator_list': get_compliance_audit_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'retry_compliance_audit_task': {
                'input_type': retry_compliance_audit_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceTask')),
                'errors': retry_compliance_audit_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': retry_compliance_audit_task_input_value_validator_list,
                'output_validator_list': retry_compliance_audit_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_audit_task': get_compliance_audit_task_rest_metadata,
            'retry_compliance_audit_task': retry_compliance_audit_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.compliance_audits.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ComplianceAuditItemsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_audit_items_fora_domain operation
        get_compliance_audit_items_fora_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'compliance_audit_id': type.StringType(),
        })
        get_compliance_audit_items_fora_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_items_fora_domain_input_value_validator_list = [
        ]
        get_compliance_audit_items_fora_domain_output_validator_list = [
        ]
        get_compliance_audit_items_fora_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/compliance-audits/{complianceAuditId}/compliance-audit-items',
            path_variables={
                'id': 'id',
                'compliance_audit_id': 'complianceAuditId',
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
            'get_compliance_audit_items_fora_domain': {
                'input_type': get_compliance_audit_items_fora_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceAuditItem')),
                'errors': get_compliance_audit_items_fora_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_items_fora_domain_input_value_validator_list,
                'output_validator_list': get_compliance_audit_items_fora_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_audit_items_fora_domain': get_compliance_audit_items_fora_domain_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.compliance_audits.compliance_audit_items',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tasks': Tasks,
        'ComplianceAuditItems': ComplianceAuditItems,
    }

