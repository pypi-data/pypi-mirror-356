# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.sso_domains.
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


class Entities(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.sso_domains.entities'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EntitiesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sso_domain_entities(self,
                                sso_domain,
                                entity_name=None,
                                ):
        """
        Get a list of all entities in the SSO domain

        :type  sso_domain: :class:`str`
        :param sso_domain: SSO Domain Name
        :type  entity_name: :class:`str` or ``None``
        :param entity_name: Search Criteria for the users and groups
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfSsoDomainEntity` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 403. Forbidden request
        :raise: :class:`vmware.sddc_manager.model_client.ErrorResponse` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_SSO_domain_entities',
                            {
                            'sso_domain': sso_domain,
                            'entity_name': entity_name,
                            })
class _EntitiesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_SSO_domain_entities operation
        get_SSO_domain_entities_input_type = type.StructType('operation-input', {
            'sso_domain': type.StringType(),
            'entity_name': type.OptionalType(type.StringType()),
        })
        get_SSO_domain_entities_error_dict = {
            'vmware.sddc_manager.model.error_response':
                type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'),

        }
        get_SSO_domain_entities_input_value_validator_list = [
        ]
        get_SSO_domain_entities_output_validator_list = [
        ]
        get_SSO_domain_entities_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sso-domains/{ssoDomain}/entities',
            path_variables={
                'sso_domain': 'ssoDomain',
            },
            query_parameters={
                'entity_name': 'entityName',
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
            'get_SSO_domain_entities': {
                'input_type': get_SSO_domain_entities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfSsoDomainEntity')),
                'errors': get_SSO_domain_entities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'ErrorResponse'), [401,403,500]).build(),
                'input_value_validator_list': get_SSO_domain_entities_input_value_validator_list,
                'output_validator_list': get_SSO_domain_entities_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_SSO_domain_entities': get_SSO_domain_entities_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.sso_domains.entities',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Entities': Entities,
    }

