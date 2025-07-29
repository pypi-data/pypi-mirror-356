# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.system.
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


class NtpConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.ntp_configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NtpConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_ntp_configuration(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.NtpConfiguration` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_ntp_configuration', None)

    def configure_ntp(self,
                      ntp_configuration,
                      ):
        """
        

        :type  ntp_configuration: :class:`vmware.sddc_manager.model_client.NtpConfiguration`
        :param ntp_configuration: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('configure_ntp',
                            {
                            'ntp_configuration': ntp_configuration,
                            })
class DnsConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.dns_configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DnsConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_dns_configuration(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.DnsConfiguration` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_dns_configuration', None)

    def configure_dns(self,
                      dns_configuration,
                      ):
        """
        

        :type  dns_configuration: :class:`vmware.sddc_manager.model_client.DnsConfiguration`
        :param dns_configuration: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('configure_dns',
                            {
                            'dns_configuration': dns_configuration,
                            })
class BackupConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.backup_configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BackupConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_backup_configuration(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.BackupConfiguration` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_backup_configuration', None)

    def set_backup_configuration(self,
                                 backup_configuration_spec,
                                 ):
        """
        

        :type  backup_configuration_spec: :class:`vmware.sddc_manager.model_client.BackupConfigurationSpec`
        :param backup_configuration_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('set_backup_configuration',
                            {
                            'backup_configuration_spec': backup_configuration_spec,
                            })

    def update_backup_configuration(self,
                                    backup_configuration_spec,
                                    ):
        """
        

        :type  backup_configuration_spec: :class:`vmware.sddc_manager.model_client.BackupConfigurationSpec`
        :param backup_configuration_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_backup_configuration',
                            {
                            'backup_configuration_spec': backup_configuration_spec,
                            })
class SupportBundles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.support_bundles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SupportBundlesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_support_bundle_task(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfSupportBundle` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('get_support_bundle_task', None)

    def start_support_bundle(self,
                             support_bundle_spec,
                             ):
        """
        

        :type  support_bundle_spec: :class:`vmware.sddc_manager.model_client.SupportBundleSpec`
        :param support_bundle_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.SupportBundle` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Operation is in progress for Id {id}. Wait
            for the operation to complete.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('start_support_bundle',
                            {
                            'support_bundle_spec': support_bundle_spec,
                            })

    def get_support_bundle_status(self,
                                  id,
                                  ):
        """
        

        :type  id: :class:`str`
        :param id: The Support Bundle ID
        :rtype: :class:`vmware.sddc_manager.model_client.SupportBundle` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('get_support_bundle_status',
                            {
                            'id': id,
                            })
class HealthSummary(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.health_summary'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HealthSummaryStub)
        self._VAPI_OPERATION_IDS = {}


    def get_health_check_task(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfHealthSummary` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('get_health_check_task', None)

    def start_health_check(self,
                           health_summary_spec,
                           ):
        """
        

        :type  health_summary_spec: :class:`vmware.sddc_manager.model_client.HealthSummarySpec`
        :param health_summary_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.HealthSummary` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Operation is in progress for Id {id}. Wait
            for the operation to complete.
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('start_health_check',
                            {
                            'health_summary_spec': health_summary_spec,
                            })

    def get_health_check_status(self,
                                id,
                                ):
        """
        

        :type  id: :class:`str`
        :param id: The Health Summary Id
        :rtype: :class:`vmware.sddc_manager.model_client.HealthSummary` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request! Invalid Headers or Data.
            Error: {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Something went wrong. Internal server error
            occurred. Error {error}
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Bad request! Authorization Header is
            missing or not in correct format.
        """
        return self._invoke('get_health_check_status',
                            {
                            'id': id,
                            })
class CheckSets(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.check_sets'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CheckSetsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_last_assessment_run_info(self,
                                     domain_id=None,
                                     ):
        """
        Get information about the last assessment run

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Id of the domain to filter tasks for, accepts multiple values as
            comma separated
        :rtype: :class:`list` of :class:`vmware.sddc_manager.model_client.AssessmentTaskInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_last_assessment_run_info',
                            {
                            'domain_id': domain_id,
                            })

    def trigger_check_run(self,
                          check_set_run_input,
                          ):
        """
        Trigger a run of the selected checks. Use returned run ID to check the
        status.

        :type  check_set_run_input: :class:`vmware.sddc_manager.model_client.CheckSetRunInput`
        :param check_set_run_input: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('trigger_check_run',
                            {
                            'check_set_run_input': check_set_run_input,
                            })

    def get_result(self,
                   run_id,
                   ):
        """
        Get the result for a given check run

        :type  run_id: :class:`str`
        :param run_id: UUID of the task
        :rtype: :class:`vmware.sddc_manager.model_client.AssessmentOutput` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Task Not Found
        """
        return self._invoke('get_result',
                            {
                            'run_id': run_id,
                            })

    def trigger_partial_retry_of_check_run(self,
                                           run_id,
                                           assessment_partial_retry_input,
                                           ):
        """
        Trigger partial retry of a completed check run

        :type  run_id: :class:`str`
        :param run_id: UUID of the assessment to retry
        :type  assessment_partial_retry_input: :class:`vmware.sddc_manager.model_client.AssessmentPartialRetryInput`
        :param assessment_partial_retry_input: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('trigger_partial_retry_of_check_run',
                            {
                            'run_id': run_id,
                            'assessment_partial_retry_input': assessment_partial_retry_input,
                            })
class ProxyConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.proxy_configuration'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProxyConfigurationStub)
        self._VAPI_OPERATION_IDS = {}


    def get_proxy_configuration(self):
        """
        Get the current Proxy configuration


        :rtype: :class:`vmware.sddc_manager.model_client.ProxyConfiguration` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_proxy_configuration', None)

    def update_proxy_configuration(self,
                                   proxy_configuration,
                                   ):
        """
        Update Proxy configuration

        :type  proxy_configuration: :class:`vmware.sddc_manager.model_client.ProxyConfiguration`
        :param proxy_configuration: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('update_proxy_configuration',
                            {
                            'proxy_configuration': proxy_configuration,
                            })
class HostBundleDepot(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.host_bundle_depot'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HostBundleDepotStub)
        self._VAPI_OPERATION_IDS = {}


    def sync_umds(self,
                  host_bundle_depot_update_spec,
                  ):
        """
        Sync UMDS

        :type  host_bundle_depot_update_spec: :class:`vmware.sddc_manager.model_client.HostBundleDepotUpdateSpec`
        :param host_bundle_depot_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        """
        return self._invoke('sync_UMDS',
                            {
                            'host_bundle_depot_update_spec': host_bundle_depot_update_spec,
                            })
class Ceip(VapiInterface):
    """
    
    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_ENABLED = "ENABLED"
    """
    Required action for CEIP.

    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_DISABLED = "DISABLED"
    """
    Required action for CEIP.

    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_DISABLING = "DISABLING"
    """
    Required action for CEIP.

    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_ENABLING = "ENABLING"
    """
    Required action for CEIP.

    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_ENABLING_FAILED = "ENABLING_FAILED"
    """
    Required action for CEIP.

    """
    SET_CEIP_STATUS_SET_CEIP_STATUS_REQUEST_BODY_DISABLING_FAILED = "DISABLING_FAILED"
    """
    Required action for CEIP.

    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.ceip'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CeipStub)
        self._VAPI_OPERATION_IDS = {}


    def get_ceip_status(self):
        """
        Get CEIP status and instance id


        :rtype: :class:`vmware.sddc_manager.model_client.Ceip` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_ceip_status', None)

    def set_ceip_status(self,
                        set_ceip_status_request_body,
                        ):
        """
        Opt-in or Opt-out of CEIP

        :type  set_ceip_status_request_body: :class:`str`
        :param set_ceip_status_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. The request could not be completed due to a
            conflict with the current state
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('set_ceip_status',
                            {
                            'set_ceip_status_request_body': set_ceip_status_request_body,
                            })
class VcfManagementComponents(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.vcf_management_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcfManagementComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_system_vcf_management_components(self):
        """
        Get the details of VCF Management Components containing each
        component's FQDN, deployment type, and deployment status


        :rtype: :class:`vmware.sddc_manager.model_client.VcfManagementComponents` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_system_vcf_management_components', None)
class Upgradables(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.upgradables'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UpgradablesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_upgradables(self):
        """
        Fetches the list of Upgradables in the System. Only one Upgradable
        becomes AVAILABLE for Upgrade. The Upgradables provides information
        that can be use for Precheck API and also in the actual Upgrade API
        call. Conflict (409) error can return if inventory cache is not seeded.


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfUpgradable` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.sddc_manager.model_client.PageOfUpgradable` 
            HTTP status code - 408. Internal Request Time Out
        """
        return self._invoke('get_upgradables', None)
class ApplianceInfo(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.system.appliance_info'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ApplianceInfoStub)
        self._VAPI_OPERATION_IDS = {}


    def get_appliance_info(self):
        """
        Get appliance information such as the version and the appliance's role.


        :rtype: :class:`vmware.sddc_manager.model_client.ApplianceInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_appliance_info', None)
class _NtpConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ntp_configuration operation
        get_ntp_configuration_input_type = type.StructType('operation-input', {})
        get_ntp_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_ntp_configuration_input_value_validator_list = [
        ]
        get_ntp_configuration_output_validator_list = [
        ]
        get_ntp_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/ntp-configuration',
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

        # properties for configure_ntp operation
        configure_ntp_input_type = type.StructType('operation-input', {
            'ntp_configuration': type.ReferenceType('vmware.sddc_manager.model_client', 'NtpConfiguration'),
        })
        configure_ntp_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        configure_ntp_input_value_validator_list = [
        ]
        configure_ntp_output_validator_list = [
        ]
        configure_ntp_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/ntp-configuration',
            request_body_parameter='ntp_configuration',
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
            'get_ntp_configuration': {
                'input_type': get_ntp_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'NtpConfiguration')),
                'errors': get_ntp_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_ntp_configuration_input_value_validator_list,
                'output_validator_list': get_ntp_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'configure_ntp': {
                'input_type': configure_ntp_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': configure_ntp_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': configure_ntp_input_value_validator_list,
                'output_validator_list': configure_ntp_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_ntp_configuration': get_ntp_configuration_rest_metadata,
            'configure_ntp': configure_ntp_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.ntp_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DnsConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_dns_configuration operation
        get_dns_configuration_input_type = type.StructType('operation-input', {})
        get_dns_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_dns_configuration_input_value_validator_list = [
        ]
        get_dns_configuration_output_validator_list = [
        ]
        get_dns_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/dns-configuration',
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

        # properties for configure_dns operation
        configure_dns_input_type = type.StructType('operation-input', {
            'dns_configuration': type.ReferenceType('vmware.sddc_manager.model_client', 'DnsConfiguration'),
        })
        configure_dns_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        configure_dns_input_value_validator_list = [
        ]
        configure_dns_output_validator_list = [
        ]
        configure_dns_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/dns-configuration',
            request_body_parameter='dns_configuration',
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
            'get_dns_configuration': {
                'input_type': get_dns_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DnsConfiguration')),
                'errors': get_dns_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_dns_configuration_input_value_validator_list,
                'output_validator_list': get_dns_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'configure_dns': {
                'input_type': configure_dns_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': configure_dns_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': configure_dns_input_value_validator_list,
                'output_validator_list': configure_dns_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_dns_configuration': get_dns_configuration_rest_metadata,
            'configure_dns': configure_dns_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.dns_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _BackupConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_backup_configuration operation
        get_backup_configuration_input_type = type.StructType('operation-input', {})
        get_backup_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_backup_configuration_input_value_validator_list = [
        ]
        get_backup_configuration_output_validator_list = [
        ]
        get_backup_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/backup-configuration',
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

        # properties for set_backup_configuration operation
        set_backup_configuration_input_type = type.StructType('operation-input', {
            'backup_configuration_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BackupConfigurationSpec'),
        })
        set_backup_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        set_backup_configuration_input_value_validator_list = [
        ]
        set_backup_configuration_output_validator_list = [
        ]
        set_backup_configuration_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/backup-configuration',
            request_body_parameter='backup_configuration_spec',
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

        # properties for update_backup_configuration operation
        update_backup_configuration_input_type = type.StructType('operation-input', {
            'backup_configuration_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BackupConfigurationSpec'),
        })
        update_backup_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_backup_configuration_input_value_validator_list = [
        ]
        update_backup_configuration_output_validator_list = [
        ]
        update_backup_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/backup-configuration',
            request_body_parameter='backup_configuration_spec',
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
            'get_backup_configuration': {
                'input_type': get_backup_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BackupConfiguration')),
                'errors': get_backup_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_backup_configuration_input_value_validator_list,
                'output_validator_list': get_backup_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set_backup_configuration': {
                'input_type': set_backup_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': set_backup_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': set_backup_configuration_input_value_validator_list,
                'output_validator_list': set_backup_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_backup_configuration': {
                'input_type': update_backup_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_backup_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': update_backup_configuration_input_value_validator_list,
                'output_validator_list': update_backup_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_backup_configuration': get_backup_configuration_rest_metadata,
            'set_backup_configuration': set_backup_configuration_rest_metadata,
            'update_backup_configuration': update_backup_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.backup_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SupportBundlesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_support_bundle_task operation
        get_support_bundle_task_input_type = type.StructType('operation-input', {})
        get_support_bundle_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_support_bundle_task_input_value_validator_list = [
        ]
        get_support_bundle_task_output_validator_list = [
        ]
        get_support_bundle_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/support-bundles',
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

        # properties for start_support_bundle operation
        start_support_bundle_input_type = type.StructType('operation-input', {
            'support_bundle_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'SupportBundleSpec'),
        })
        start_support_bundle_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_support_bundle_input_value_validator_list = [
        ]
        start_support_bundle_output_validator_list = [
        ]
        start_support_bundle_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/support-bundles',
            request_body_parameter='support_bundle_spec',
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

        # properties for get_support_bundle_status operation
        get_support_bundle_status_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_support_bundle_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_support_bundle_status_input_value_validator_list = [
        ]
        get_support_bundle_status_output_validator_list = [
        ]
        get_support_bundle_status_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/support-bundles/{id}',
            path_variables={
                'id': 'id',
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
            'get_support_bundle_task': {
                'input_type': get_support_bundle_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfSupportBundle')),
                'errors': get_support_bundle_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,401]).build(),
                'input_value_validator_list': get_support_bundle_task_input_value_validator_list,
                'output_validator_list': get_support_bundle_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start_support_bundle': {
                'input_type': start_support_bundle_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'SupportBundle')),
                'errors': start_support_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,409,500,401]).build(),
                'input_value_validator_list': start_support_bundle_input_value_validator_list,
                'output_validator_list': start_support_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_support_bundle_status': {
                'input_type': get_support_bundle_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'SupportBundle')),
                'errors': get_support_bundle_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,401]).build(),
                'input_value_validator_list': get_support_bundle_status_input_value_validator_list,
                'output_validator_list': get_support_bundle_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_support_bundle_task': get_support_bundle_task_rest_metadata,
            'start_support_bundle': start_support_bundle_rest_metadata,
            'get_support_bundle_status': get_support_bundle_status_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.support_bundles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _HealthSummaryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_health_check_task operation
        get_health_check_task_input_type = type.StructType('operation-input', {})
        get_health_check_task_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_health_check_task_input_value_validator_list = [
        ]
        get_health_check_task_output_validator_list = [
        ]
        get_health_check_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/health-summary',
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

        # properties for start_health_check operation
        start_health_check_input_type = type.StructType('operation-input', {
            'health_summary_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'HealthSummarySpec'),
        })
        start_health_check_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        start_health_check_input_value_validator_list = [
        ]
        start_health_check_output_validator_list = [
        ]
        start_health_check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/health-summary',
            request_body_parameter='health_summary_spec',
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

        # properties for get_health_check_status operation
        get_health_check_status_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_health_check_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_health_check_status_input_value_validator_list = [
        ]
        get_health_check_status_output_validator_list = [
        ]
        get_health_check_status_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/health-summary/{id}',
            path_variables={
                'id': 'id',
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
            'get_health_check_task': {
                'input_type': get_health_check_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfHealthSummary')),
                'errors': get_health_check_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,401]).build(),
                'input_value_validator_list': get_health_check_task_input_value_validator_list,
                'output_validator_list': get_health_check_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start_health_check': {
                'input_type': start_health_check_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthSummary')),
                'errors': start_health_check_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,409,500,401]).build(),
                'input_value_validator_list': start_health_check_input_value_validator_list,
                'output_validator_list': start_health_check_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_health_check_status': {
                'input_type': get_health_check_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthSummary')),
                'errors': get_health_check_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,401]).build(),
                'input_value_validator_list': get_health_check_status_input_value_validator_list,
                'output_validator_list': get_health_check_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_health_check_task': get_health_check_task_rest_metadata,
            'start_health_check': start_health_check_rest_metadata,
            'get_health_check_status': get_health_check_status_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.health_summary',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CheckSetsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_last_assessment_run_info operation
        get_last_assessment_run_info_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
        })
        get_last_assessment_run_info_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_last_assessment_run_info_input_value_validator_list = [
        ]
        get_last_assessment_run_info_output_validator_list = [
        ]
        get_last_assessment_run_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/check-sets',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for trigger_check_run operation
        trigger_check_run_input_type = type.StructType('operation-input', {
            'check_set_run_input': type.ReferenceType('vmware.sddc_manager.model_client', 'CheckSetRunInput'),
        })
        trigger_check_run_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        trigger_check_run_input_value_validator_list = [
        ]
        trigger_check_run_output_validator_list = [
        ]
        trigger_check_run_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/system/check-sets',
            request_body_parameter='check_set_run_input',
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

        # properties for get_result operation
        get_result_input_type = type.StructType('operation-input', {
            'run_id': type.StringType(),
        })
        get_result_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_result_input_value_validator_list = [
        ]
        get_result_output_validator_list = [
        ]
        get_result_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/check-sets/{runId}',
            path_variables={
                'run_id': 'runId',
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

        # properties for trigger_partial_retry_of_check_run operation
        trigger_partial_retry_of_check_run_input_type = type.StructType('operation-input', {
            'run_id': type.StringType(),
            'assessment_partial_retry_input': type.ReferenceType('vmware.sddc_manager.model_client', 'AssessmentPartialRetryInput'),
        })
        trigger_partial_retry_of_check_run_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        trigger_partial_retry_of_check_run_input_value_validator_list = [
        ]
        trigger_partial_retry_of_check_run_output_validator_list = [
        ]
        trigger_partial_retry_of_check_run_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/check-sets/{runId}',
            request_body_parameter='assessment_partial_retry_input',
            path_variables={
                'run_id': 'runId',
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
            'get_last_assessment_run_info': {
                'input_type': get_last_assessment_run_info_input_type,
                'output_type': type.OptionalType(type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'AssessmentTaskInfo'))),
                'errors': get_last_assessment_run_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_last_assessment_run_info_input_value_validator_list,
                'output_validator_list': get_last_assessment_run_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'trigger_check_run': {
                'input_type': trigger_check_run_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': trigger_check_run_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': trigger_check_run_input_value_validator_list,
                'output_validator_list': trigger_check_run_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_result': {
                'input_type': get_result_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'AssessmentOutput')),
                'errors': get_result_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500,404]).build(),
                'input_value_validator_list': get_result_input_value_validator_list,
                'output_validator_list': get_result_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'trigger_partial_retry_of_check_run': {
                'input_type': trigger_partial_retry_of_check_run_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': trigger_partial_retry_of_check_run_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': trigger_partial_retry_of_check_run_input_value_validator_list,
                'output_validator_list': trigger_partial_retry_of_check_run_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_last_assessment_run_info': get_last_assessment_run_info_rest_metadata,
            'trigger_check_run': trigger_check_run_rest_metadata,
            'get_result': get_result_rest_metadata,
            'trigger_partial_retry_of_check_run': trigger_partial_retry_of_check_run_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.check_sets',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ProxyConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_proxy_configuration operation
        get_proxy_configuration_input_type = type.StructType('operation-input', {})
        get_proxy_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_proxy_configuration_input_value_validator_list = [
        ]
        get_proxy_configuration_output_validator_list = [
        ]
        get_proxy_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/proxy-configuration',
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

        # properties for update_proxy_configuration operation
        update_proxy_configuration_input_type = type.StructType('operation-input', {
            'proxy_configuration': type.ReferenceType('vmware.sddc_manager.model_client', 'ProxyConfiguration'),
        })
        update_proxy_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_proxy_configuration_input_value_validator_list = [
        ]
        update_proxy_configuration_output_validator_list = [
        ]
        update_proxy_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/proxy-configuration',
            request_body_parameter='proxy_configuration',
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
            'get_proxy_configuration': {
                'input_type': get_proxy_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ProxyConfiguration')),
                'errors': get_proxy_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': get_proxy_configuration_input_value_validator_list,
                'output_validator_list': get_proxy_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_proxy_configuration': {
                'input_type': update_proxy_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': update_proxy_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': update_proxy_configuration_input_value_validator_list,
                'output_validator_list': update_proxy_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_proxy_configuration': get_proxy_configuration_rest_metadata,
            'update_proxy_configuration': update_proxy_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.proxy_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _HostBundleDepotStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for sync_UMDS operation
        sync_UMDS_input_type = type.StructType('operation-input', {
            'host_bundle_depot_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'HostBundleDepotUpdateSpec'),
        })
        sync_UMDS_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        sync_UMDS_input_value_validator_list = [
        ]
        sync_UMDS_output_validator_list = [
        ]
        sync_UMDS_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/host-bundle-depot',
            request_body_parameter='host_bundle_depot_update_spec',
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
            'sync_UMDS': {
                'input_type': sync_UMDS_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': sync_UMDS_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400,409]).build(),
                'input_value_validator_list': sync_UMDS_input_value_validator_list,
                'output_validator_list': sync_UMDS_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'sync_UMDS': sync_UMDS_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.host_bundle_depot',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CeipStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ceip_status operation
        get_ceip_status_input_type = type.StructType('operation-input', {})
        get_ceip_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_ceip_status_input_value_validator_list = [
        ]
        get_ceip_status_output_validator_list = [
        ]
        get_ceip_status_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/ceip',
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

        # properties for set_ceip_status operation
        set_ceip_status_input_type = type.StructType('operation-input', {
            'set_ceip_status_request_body': type.StringType(),
        })
        set_ceip_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        set_ceip_status_input_value_validator_list = [
        ]
        set_ceip_status_output_validator_list = [
        ]
        set_ceip_status_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system/ceip',
            request_body_parameter='set_ceip_status_request_body',
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
            'get_ceip_status': {
                'input_type': get_ceip_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Ceip')),
                'errors': get_ceip_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_ceip_status_input_value_validator_list,
                'output_validator_list': get_ceip_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set_ceip_status': {
                'input_type': set_ceip_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': set_ceip_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,409,400]).build(),
                'input_value_validator_list': set_ceip_status_input_value_validator_list,
                'output_validator_list': set_ceip_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_ceip_status': get_ceip_status_rest_metadata,
            'set_ceip_status': set_ceip_status_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.ceip',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcfManagementComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_vcf_management_components operation
        get_system_vcf_management_components_input_type = type.StructType('operation-input', {})
        get_system_vcf_management_components_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_system_vcf_management_components_input_value_validator_list = [
        ]
        get_system_vcf_management_components_output_validator_list = [
        ]
        get_system_vcf_management_components_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/vcf-management-components',
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
            'get_system_vcf_management_components': {
                'input_type': get_system_vcf_management_components_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'VcfManagementComponents')),
                'errors': get_system_vcf_management_components_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_system_vcf_management_components_input_value_validator_list,
                'output_validator_list': get_system_vcf_management_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_vcf_management_components': get_system_vcf_management_components_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.vcf_management_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _UpgradablesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_upgradables operation
        get_upgradables_input_type = type.StructType('operation-input', {})
        get_upgradables_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),
            'vmware.sddc_manager.model.page_of_upgradable':
                type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgradable'),

        }
        get_upgradables_input_value_validator_list = [
        ]
        get_upgradables_output_validator_list = [
        ]
        get_upgradables_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/upgradables',
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
            'get_upgradables': {
                'input_type': get_upgradables_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgradable')),
                'errors': get_upgradables_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [409,500]).add(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfUpgradable'), [408]).build(),
                'input_value_validator_list': get_upgradables_input_value_validator_list,
                'output_validator_list': get_upgradables_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_upgradables': get_upgradables_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.upgradables',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ApplianceInfoStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_appliance_info operation
        get_appliance_info_input_type = type.StructType('operation-input', {})
        get_appliance_info_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_appliance_info_input_value_validator_list = [
        ]
        get_appliance_info_output_validator_list = [
        ]
        get_appliance_info_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/appliance-info',
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
            'get_appliance_info': {
                'input_type': get_appliance_info_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ApplianceInfo')),
                'errors': get_appliance_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_appliance_info_input_value_validator_list,
                'output_validator_list': get_appliance_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_appliance_info': get_appliance_info_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.system.appliance_info',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'NtpConfiguration': NtpConfiguration,
        'DnsConfiguration': DnsConfiguration,
        'BackupConfiguration': BackupConfiguration,
        'SupportBundles': SupportBundles,
        'HealthSummary': HealthSummary,
        'CheckSets': CheckSets,
        'ProxyConfiguration': ProxyConfiguration,
        'HostBundleDepot': HostBundleDepot,
        'Ceip': Ceip,
        'VcfManagementComponents': VcfManagementComponents,
        'Upgradables': Upgradables,
        'ApplianceInfo': ApplianceInfo,
        'backup_configuration': 'vmware.sddc_manager.v1.system.backup_configuration_client.StubFactory',
        'check_sets': 'vmware.sddc_manager.v1.system.check_sets_client.StubFactory',
        'dns_configuration': 'vmware.sddc_manager.v1.system.dns_configuration_client.StubFactory',
        'health_summary': 'vmware.sddc_manager.v1.system.health_summary_client.StubFactory',
        'ntp_configuration': 'vmware.sddc_manager.v1.system.ntp_configuration_client.StubFactory',
        'security': 'vmware.sddc_manager.v1.system.security_client.StubFactory',
        'settings': 'vmware.sddc_manager.v1.system.settings_client.StubFactory',
        'support_bundles': 'vmware.sddc_manager.v1.system.support_bundles_client.StubFactory',
    }

