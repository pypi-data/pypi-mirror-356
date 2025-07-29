# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.hosts.validations.
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


class Commissions(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.hosts.validations.commissions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CommissionsStub)
        self._VAPI_OPERATION_IDS = {}


    def validate_commission_hosts(self,
                                  validate_commission_hosts_request_body,
                                  ):
        """
        

        :type  validate_commission_hosts_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.HostCommissionSpec`
        :param validate_commission_hosts_request_body: Validate the input specification to commission the Hosts request
            body.
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('validate_commission_hosts',
                            {
                            'validate_commission_hosts_request_body': validate_commission_hosts_request_body,
                            })
class _CommissionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_commission_hosts operation
        validate_commission_hosts_input_type = type.StructType('operation-input', {
            'validate_commission_hosts_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'HostCommissionSpec')),
        })
        validate_commission_hosts_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_commission_hosts_input_value_validator_list = [
        ]
        validate_commission_hosts_output_validator_list = [
        ]
        validate_commission_hosts_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/hosts/validations/commissions',
            request_body_parameter='validate_commission_hosts_request_body',
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
            'validate_commission_hosts': {
                'input_type': validate_commission_hosts_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_commission_hosts_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': validate_commission_hosts_input_value_validator_list,
                'output_validator_list': validate_commission_hosts_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_commission_hosts': validate_commission_hosts_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.hosts.validations.commissions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Commissions': Commissions,
    }

