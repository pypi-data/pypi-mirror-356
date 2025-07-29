# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.security.
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


class Fips(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.security.fips'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FipsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_fips_configuration(self):
        """
        Retrieve VCF security FIPS mode.


        :rtype: :class:`vmware.sddc_manager.model_client.Fips` or ``None``
        :return: OK
        """
        return self._invoke('get_FIPS_configuration', None)
class _FipsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_FIPS_configuration operation
        get_FIPS_configuration_input_type = type.StructType('operation-input', {})
        get_FIPS_configuration_error_dict = {}
        get_FIPS_configuration_input_value_validator_list = [
        ]
        get_FIPS_configuration_output_validator_list = [
        ]
        get_FIPS_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/security/fips',
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
            'get_FIPS_configuration': {
                'input_type': get_FIPS_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Fips')),
                'errors': get_FIPS_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': get_FIPS_configuration_input_value_validator_list,
                'output_validator_list': get_FIPS_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_FIPS_configuration': get_FIPS_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.security.fips',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Fips': Fips,
    }

