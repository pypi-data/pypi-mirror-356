# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.check_sets.
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


class Queries(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.check_sets.queries'
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


    def query_check_sets(self,
                         check_set_query_input,
                         ):
        """
        Query for check-sets for the given resources

        :type  check_set_query_input: :class:`vmware.sddc_manager.model_client.CheckSetQueryInput`
        :param check_set_query_input: 
        :rtype: :class:`vmware.sddc_manager.model_client.CheckSetQueryResult` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('query_check_sets',
                            {
                            'check_set_query_input': check_set_query_input,
                            })
class _QueriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for query_check_sets operation
        query_check_sets_input_type = type.StructType('operation-input', {
            'check_set_query_input': type.ReferenceType('vmware.sddc_manager.model_client', 'CheckSetQueryInput'),
        })
        query_check_sets_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        query_check_sets_input_value_validator_list = [
        ]
        query_check_sets_output_validator_list = [
        ]
        query_check_sets_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/check-sets/queries',
            request_body_parameter='check_set_query_input',
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
            'query_check_sets': {
                'input_type': query_check_sets_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'CheckSetQueryResult')),
                'errors': query_check_sets_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': query_check_sets_input_value_validator_list,
                'output_validator_list': query_check_sets_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'query_check_sets': query_check_sets_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.check_sets.queries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Queries': Queries,
    }

