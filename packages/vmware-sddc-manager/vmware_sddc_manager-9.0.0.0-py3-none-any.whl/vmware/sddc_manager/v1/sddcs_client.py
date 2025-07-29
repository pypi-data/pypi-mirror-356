# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.sddcs.
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


class Imports(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.sddcs.imports'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ImportsStub)
        self._VAPI_OPERATION_IDS = {}


    def import_(self,
                brownfield_import_spec,
                ):
        """
        Import a vCenter as a VI domain

        :type  brownfield_import_spec: :class:`vmware.sddc_manager.model_client.BrownfieldImportSpec`
        :param brownfield_import_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.BrownfieldTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('import',
                            {
                            'brownfield_import_spec': brownfield_import_spec,
                            })

    def get_brownfield_import_task_by_id(self,
                                         task_id,
                                         ):
        """
        Get a Brownfield task of import operation by its ID

        :type  task_id: :class:`str`
        :param task_id: ID of the task to retrieve
        :rtype: :class:`vmware.sddc_manager.model_client.BrownfieldTask` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_brownfield_import_task_by_id',
                            {
                            'task_id': task_id,
                            })
class _ImportsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for import operation
        import_input_type = type.StructType('operation-input', {
            'brownfield_import_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldImportSpec'),
        })
        import_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        import_input_value_validator_list = [
        ]
        import_output_validator_list = [
        ]
        import_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/imports',
            request_body_parameter='brownfield_import_spec',
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

        # properties for get_brownfield_import_task_by_id operation
        get_brownfield_import_task_by_id_input_type = type.StructType('operation-input', {
            'task_id': type.StringType(),
        })
        get_brownfield_import_task_by_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_brownfield_import_task_by_id_input_value_validator_list = [
        ]
        get_brownfield_import_task_by_id_output_validator_list = [
        ]
        get_brownfield_import_task_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/imports/{taskId}',
            path_variables={
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
            'import': {
                'input_type': import_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldTask')),
                'errors': import_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': import_input_value_validator_list,
                'output_validator_list': import_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_brownfield_import_task_by_id': {
                'input_type': get_brownfield_import_task_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldTask')),
                'errors': get_brownfield_import_task_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_brownfield_import_task_by_id_input_value_validator_list,
                'output_validator_list': get_brownfield_import_task_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'import': import_rest_metadata,
            'get_brownfield_import_task_by_id': get_brownfield_import_task_by_id_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.sddcs.imports',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Imports': Imports,
        'imports': 'vmware.sddc_manager.v1.sddcs.imports_client.StubFactory',
    }

