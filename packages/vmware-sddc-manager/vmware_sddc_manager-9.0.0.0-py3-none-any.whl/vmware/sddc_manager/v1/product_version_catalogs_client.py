# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.product_version_catalogs.
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


class UploadTasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.product_version_catalogs.upload_tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UploadTasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_product_version_catalog_upload_task(self,
                                                task_id,
                                                ):
        """
        Monitor the progress of a product version catalog upload operation
        given it's upload task ID.

        :type  task_id: :class:`str`
        :param task_id: Product Version Catalog Upload ID
        :rtype: :class:`vmware.sddc_manager.model_client.ProductVersionCatalogUploadTask` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_product_version_catalog_upload_task',
                            {
                            'task_id': task_id,
                            })
class _UploadTasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_product_version_catalog_upload_task operation
        get_product_version_catalog_upload_task_input_type = type.StructType('operation-input', {
            'task_id': type.StringType(),
        })
        get_product_version_catalog_upload_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_product_version_catalog_upload_task_input_value_validator_list = [
        ]
        get_product_version_catalog_upload_task_output_validator_list = [
        ]
        get_product_version_catalog_upload_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/product-version-catalogs/upload-tasks/{taskId}',
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
            'get_product_version_catalog_upload_task': {
                'input_type': get_product_version_catalog_upload_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProductVersionCatalogUploadTask')),
                'errors': get_product_version_catalog_upload_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_product_version_catalog_upload_task_input_value_validator_list,
                'output_validator_list': get_product_version_catalog_upload_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_product_version_catalog_upload_task': get_product_version_catalog_upload_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.product_version_catalogs.upload_tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'UploadTasks': UploadTasks,
    }

