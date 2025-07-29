# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.upgradables.
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


class Domains(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.upgradables.domains'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DomainsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_upgradables_by_domain(self,
                                  domain_id,
                                  target_version=None,
                                  ):
        """
        Fetches the list of Upgradables for a given domain. If a target version
        is provided, Upgradables that are required for given target version
        become Available. The Upgradables providesinformation that can be use
        for Precheck API and also in the actual Upgrade API call.This API is
        used only for management domain, for all cases please use
        v1/system/upgradables.

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  target_version: :class:`str` or ``None``
        :param target_version: Target Version to get Upgradables for a given Target Release
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUpgradable` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain Not Found
        """
        return self._invoke('get_upgradables_by_domain',
                            {
                            'domain_id': domain_id,
                            'target_version': target_version,
                            })
class _DomainsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_upgradables_by_domain operation
        get_upgradables_by_domain_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'target_version': type.OptionalType(type.StringType()),
        })
        get_upgradables_by_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_upgradables_by_domain_input_value_validator_list = [
        ]
        get_upgradables_by_domain_output_validator_list = [
        ]
        get_upgradables_by_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/upgradables/domains/{domainId}',
            path_variables={
                'domain_id': 'domainId',
            },
            query_parameters={
                'target_version': 'targetVersion',
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
            'get_upgradables_by_domain': {
                'input_type': get_upgradables_by_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgradable')),
                'errors': get_upgradables_by_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_upgradables_by_domain_input_value_validator_list,
                'output_validator_list': get_upgradables_by_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_upgradables_by_domain': get_upgradables_by_domain_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.upgradables.domains',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Domains': Domains,
        'domains': 'vmware.sddc_manager.v1.upgradables.domains_client.StubFactory',
    }

