# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.compliance_audits.
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


class ComplianceAuditItems(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.compliance_audits.compliance_audit_items'
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


    def get_compliance_audit_items(self,
                                   compliance_audit_id,
                                   ):
        """
        Get compliance audit items

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
        return self._invoke('get_compliance_audit_items',
                            {
                            'compliance_audit_id': compliance_audit_id,
                            })
class _ComplianceAuditItemsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_audit_items operation
        get_compliance_audit_items_input_type = type.StructType('operation-input', {
            'compliance_audit_id': type.StringType(),
        })
        get_compliance_audit_items_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_items_input_value_validator_list = [
        ]
        get_compliance_audit_items_output_validator_list = [
        ]
        get_compliance_audit_items_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/compliance-audits/{complianceAuditId}/compliance-audit-items',
            path_variables={
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
            'get_compliance_audit_items': {
                'input_type': get_compliance_audit_items_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceAuditItem')),
                'errors': get_compliance_audit_items_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_items_input_value_validator_list,
                'output_validator_list': get_compliance_audit_items_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_audit_items': get_compliance_audit_items_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.compliance_audits.compliance_audit_items',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ComplianceAuditItems': ComplianceAuditItems,
    }

