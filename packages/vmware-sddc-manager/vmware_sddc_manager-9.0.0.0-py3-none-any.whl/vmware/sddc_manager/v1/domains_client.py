# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.sddc_manager.v1.domains.
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


class Tags(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.tags'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TagsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_tags_assigned_to_domain(self,
                                    id,
                                    ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTag` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_tags_assigned_to_domain',
                            {
                            'id': id,
                            })

    def assign_tags_to_domain(self,
                              id,
                              tags_spec,
                              ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('assign_tags_to_domain',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def remove_tags_from_domain(self,
                                id,
                                tags_spec,
                                ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :type  tags_spec: :class:`vmware.sddc_manager.model_client.TagsSpec`
        :param tags_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.TagAssignmentResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('remove_tags_from_domain',
                            {
                            'id': id,
                            'tags_spec': tags_spec,
                            })

    def get_tags_assigned_to_domains(self):
        """
        


        :rtype: :class:`vmware.sddc_manager.model_client.PageOfTagsForResource` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_tags_assigned_to_domains', None)
class ResourceCertificates(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.resource_certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourceCertificatesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_certificates_by_domain(self,
                                   id,
                                   ):
        """
        View detailed metadata about the certificate(s) of all the resources in
        a domain

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCertificate` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_certificates_by_domain',
                            {
                            'id': id,
                            })

    def replace_resource_certificates(self,
                                      id,
                                      replace_resource_certificates_request_body,
                                      ):
        """
        Replace resource certificates

        :type  id: :class:`str`
        :param id: Domain ID
        :type  replace_resource_certificates_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.ResourceCertificateSpec`
        :param replace_resource_certificates_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('replace_resource_certificates',
                            {
                            'id': id,
                            'replace_resource_certificates_request_body': replace_resource_certificates_request_body,
                            })

    def set_auto_renew_configuration_for_domain(self,
                                                id,
                                                domain_resource_certificates_update_spec,
                                                ):
        """
        Accepted

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :type  domain_resource_certificates_update_spec: :class:`vmware.sddc_manager.model_client.DomainResourceCertificatesUpdateSpec`
        :param domain_resource_certificates_update_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('set_auto_renew_configuration_for_domain',
                            {
                            'id': id,
                            'domain_resource_certificates_update_spec': domain_resource_certificates_update_spec,
                            })

    def set_auto_renew_configuration(self,
                                     resource_certificates_update_spec,
                                     ):
        """
        Accepted

        :type  resource_certificates_update_spec: :class:`vmware.sddc_manager.model_client.ResourceCertificatesUpdateSpec`
        :param resource_certificates_update_spec: 
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('set_auto_renew_configuration',
                            {
                            'resource_certificates_update_spec': resource_certificates_update_spec,
                            })
class Csrs(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.csrs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CsrsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_cs_rs(self,
                  id,
                  ):
        """
        Get available CSR(s) in json format

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCsr` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_CS_rs',
                            {
                            'id': id,
                            })

    def generates_cs_rs(self,
                        id,
                        csrs_generation_spec,
                        ):
        """
        Generate CSR(s) for the selected resource(s) in the domain. 
        
        *Warning:* *Avoid using wildcard certificates. Instead, use
        subdomain-specific certificates that are rotated often. A compromised
        wildcard certificate can lead to security repercussions* 

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :type  csrs_generation_spec: :class:`vmware.sddc_manager.model_client.CsrsGenerationSpec`
        :param csrs_generation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        """
        return self._invoke('generates_CS_rs',
                            {
                            'id': id,
                            'csrs_generation_spec': csrs_generation_spec,
                            })
class Certificates(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CertificatesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_domain_certificates(self,
                                id,
                                ):
        """
        Get latest generated certificate(s) in a domain.

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfCertificate` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        """
        return self._invoke('get_domain_certificates',
                            {
                            'id': id,
                            })

    def generate_certificates(self,
                              id,
                              certificates_generation_spec,
                              ):
        """
        Generate certificate(s) for the selected resource(s) in a domain. CA
        must be configured and CSR must be generated beforehand.

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :type  certificates_generation_spec: :class:`vmware.sddc_manager.model_client.CertificatesGenerationSpec`
        :param certificates_generation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        """
        return self._invoke('generate_certificates',
                            {
                            'id': id,
                            'certificates_generation_spec': certificates_generation_spec,
                            })

    def replace_certificates(self,
                             id,
                             certificate_operation_spec,
                             ):
        """
        Replace certificate(s) for the selected resource(s) in a domain

        :type  id: :class:`str`
        :param id: Domain ID or Name
        :type  certificate_operation_spec: :class:`vmware.sddc_manager.model_client.CertificateOperationSpec`
        :param certificate_operation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 409. Conflict
        """
        return self._invoke('replace_certificates',
                            {
                            'id': id,
                            'certificate_operation_spec': certificate_operation_spec,
                            })
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.validations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ValidationsStub)
        self._VAPI_OPERATION_IDS = {}


    def validate_domain_update_spec(self,
                                    id,
                                    domain_update_spec,
                                    ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :type  domain_update_spec: :class:`vmware.sddc_manager.model_client.DomainUpdateSpec`
        :param domain_update_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_domain_update_spec',
                            {
                            'id': id,
                            'domain_update_spec': domain_update_spec,
                            })

    def validate_domain_creation_spec(self,
                                      domain_creation_spec,
                                      hosts_only=None,
                                      skip_host_switch_validation=None,
                                      ):
        """
        

        :type  domain_creation_spec: :class:`vmware.sddc_manager.model_client.DomainCreationSpec`
        :param domain_creation_spec: 
        :type  hosts_only: :class:`bool` or ``None``
        :param hosts_only: Validate hosts only
        :type  skip_host_switch_validation: :class:`bool` or ``None``
        :param skip_host_switch_validation: Skips host switch validation when hostOnly=true
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('validate_domain_creation_spec',
                            {
                            'domain_creation_spec': domain_creation_spec,
                            'hosts_only': hosts_only,
                            'skip_host_switch_validation': skip_host_switch_validation,
                            })

    def get_domain_update_validation(self,
                                     id,
                                     validation_id,
                                     ):
        """
        Gets the status of given domain update validation workflow by given
        validation id

        :type  id: :class:`str`
        :param id: Domain ID
        :type  validation_id: :class:`str`
        :param validation_id: Domain validation id
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_domain_update_validation',
                            {
                            'id': id,
                            'validation_id': validation_id,
                            })

    def domain_create_validation(self,
                                 id,
                                 ):
        """
        Gets the status of given domain create validation workflow by given
        validation id

        :type  id: :class:`str`
        :param id: Domain validation id
        :rtype: :class:`vmware.sddc_manager.model_client.Validation` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('domain_create_validation',
                            {
                            'id': id,
                            })
class ComplianceAudits(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.compliance_audits'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ComplianceAuditsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_compliance_audit_history_fora_domain(self,
                                                 id,
                                                 ):
        """
        Get compliance audit history for a domain

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfComplianceAudit` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit_history_fora_domain',
                            {
                            'id': id,
                            })

    def compliance_audit(self,
                         id,
                         compliance_audit_spec,
                         ):
        """
        Compliance audit of resource

        :type  id: :class:`str`
        :param id: ID of the domain
        :type  compliance_audit_spec: :class:`vmware.sddc_manager.model_client.ComplianceAuditSpec`
        :param compliance_audit_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.ComplianceTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('compliance_audit',
                            {
                            'id': id,
                            'compliance_audit_spec': compliance_audit_spec,
                            })

    def get_compliance_audit_fora_domain(self,
                                         id,
                                         compliance_audit_id,
                                         ):
        """
        Get compliance audit for a domain

        :type  id: :class:`str`
        :param id: Domain ID
        :type  compliance_audit_id: :class:`str`
        :param compliance_audit_id: Compliance Audit ID
        :rtype: :class:`vmware.sddc_manager.model_client.ComplianceAudit` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 401. Unauthorized Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_compliance_audit_fora_domain',
                            {
                            'id': id,
                            'compliance_audit_id': compliance_audit_id,
                            })
class Synchronizations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.synchronizations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SynchronizationsStub)
        self._VAPI_OPERATION_IDS = {}


    def synchronization(self,
                        domain_id,
                        brownfield_sync_spec,
                        ):
        """
        Perform synchronization of SDDC Manager state with any changes
        performed out-of-band in the vSphere environment

        :type  domain_id: :class:`str`
        :param domain_id: ID of the domain to sync
        :type  brownfield_sync_spec: :class:`vmware.sddc_manager.model_client.BrownfieldSyncSpec`
        :param brownfield_sync_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.BrownfieldTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('synchronization',
                            {
                            'domain_id': domain_id,
                            'brownfield_sync_spec': brownfield_sync_spec,
                            })

    def get_brownfield_sync_task_by_id(self,
                                       domain_id,
                                       task_id,
                                       ):
        """
        Get a Brownfield task of synchronization operation by its ID

        :type  domain_id: :class:`str`
        :param domain_id: ID of the domain sync is performing for
        :type  task_id: :class:`str`
        :param task_id: ID of the task to retrieve
        :rtype: :class:`vmware.sddc_manager.model_client.BrownfieldTask` or ``None``
        :return: OK
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_brownfield_sync_task_by_id',
                            {
                            'domain_id': domain_id,
                            'task_id': task_id,
                            })
class IsolationPrechecks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.isolation_prechecks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _IsolationPrechecksStub)
        self._VAPI_OPERATION_IDS = {}


    def perform_domain_isolation_precheck(self,
                                          domain_id,
                                          isolation_spec,
                                          ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  isolation_spec: :class:`vmware.sddc_manager.model_client.IsolationSpec`
        :param isolation_spec: 
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('perform_domain_isolation_precheck',
                            {
                            'domain_id': domain_id,
                            'isolation_spec': isolation_spec,
                            })

    def get_domain_isolation_precheck_status(self,
                                             domain_id,
                                             precheck_id,
                                             ):
        """
        

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  precheck_id: :class:`str`
        :param precheck_id: Precheck ID
        :rtype: :class:`vmware.sddc_manager.model_client.IsolationPrecheckResult` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_domain_isolation_precheck_status',
                            {
                            'domain_id': domain_id,
                            'precheck_id': precheck_id,
                            })
class Overlay(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.overlay'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _OverlayStub)
        self._VAPI_OPERATION_IDS = {}


    def enable_overlay_over_management_network(self,
                                               id,
                                               ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.Task` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('enable_overlay_over_management_network',
                            {
                            'id': id,
                            })
class HealthChecks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.health_checks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HealthChecksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vsan_health_check_by_domain(self,
                                        domain_id,
                                        status=None,
                                        ):
        """
        Get vSAN health check status for all cluster on the domain

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  status: :class:`str` or ``None``
        :param status: Status of health check to filter by
        :rtype: :class:`vmware.sddc_manager.model_client.HealthCheckQueryResult` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_vsan_health_check_by_domain',
                            {
                            'domain_id': domain_id,
                            'status': status,
                            })

    def update_vsan_health_check_by_domain(self,
                                           domain_id,
                                           update_vsan_health_check_by_domain_request_body,
                                           ):
        """
        Update vSAN health check status for domain

        :type  domain_id: :class:`str`
        :param domain_id: Domain ID
        :type  update_vsan_health_check_by_domain_request_body: :class:`list` of :class:`vmware.sddc_manager.model_client.HealthCheckSpec`
        :param update_vsan_health_check_by_domain_request_body: 
        :rtype: :class:`vmware.sddc_manager.model_client.HealthCheckTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('update_vsan_health_check_by_domain',
                            {
                            'domain_id': domain_id,
                            'update_vsan_health_check_by_domain_request_body': update_vsan_health_check_by_domain_request_body,
                            })
class Endpoints(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.endpoints'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EndpointsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_domain_endpoints(self,
                             id,
                             ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfEndpoint` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain Not Found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_domain_endpoints',
                            {
                            'id': id,
                            })
class Datacenters(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.datacenters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DatacentersStub)
        self._VAPI_OPERATION_IDS = {}


    def get_domain_datacenters(self,
                               id,
                               ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.PageOfDatacenter` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_domain_datacenters',
                            {
                            'id': id,
                            })
class Capabilities(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.sddc_manager.v1.domains.capabilities'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CapabilitiesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_domain_capabilities_by_domain_id(self,
                                             id,
                                             ):
        """
        

        :type  id: :class:`str`
        :param id: Domain ID
        :rtype: :class:`vmware.sddc_manager.model_client.DomainCapabilities` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 404. Domain not found
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_domain_capabilities_by_domain_id',
                            {
                            'id': id,
                            })

    def get_domain_capabilities(self,
                                capabilities=None,
                                ):
        """
        

        :type  capabilities: :class:`list` of :class:`str` or ``None``
        :param capabilities: Capabilities separated by comma. Filters DomainCapabilities where
            each domain has all given capabilities
        :rtype: :class:`vmware.sddc_manager.model_client.DomainsWithCapabilities` or ``None``
        :return: Ok
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.sddc_manager.model_client.Error` 
            HTTP status code - 400. Bad Request
        """
        return self._invoke('get_domain_capabilities',
                            {
                            'capabilities': capabilities,
                            })
class _TagsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_tags_assigned_to_domain operation
        get_tags_assigned_to_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_tags_assigned_to_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_domain_input_value_validator_list = [
        ]
        get_tags_assigned_to_domain_output_validator_list = [
        ]
        get_tags_assigned_to_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/tags',
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

        # properties for assign_tags_to_domain operation
        assign_tags_to_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        assign_tags_to_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        assign_tags_to_domain_input_value_validator_list = [
        ]
        assign_tags_to_domain_output_validator_list = [
        ]
        assign_tags_to_domain_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/domains/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for remove_tags_from_domain operation
        remove_tags_from_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'tags_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'TagsSpec'),
        })
        remove_tags_from_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        remove_tags_from_domain_input_value_validator_list = [
        ]
        remove_tags_from_domain_output_validator_list = [
        ]
        remove_tags_from_domain_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/domains/{id}/tags',
            request_body_parameter='tags_spec',
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

        # properties for get_tags_assigned_to_domains operation
        get_tags_assigned_to_domains_input_type = type.StructType('operation-input', {})
        get_tags_assigned_to_domains_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_tags_assigned_to_domains_input_value_validator_list = [
        ]
        get_tags_assigned_to_domains_output_validator_list = [
        ]
        get_tags_assigned_to_domains_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/tags',
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
            'get_tags_assigned_to_domain': {
                'input_type': get_tags_assigned_to_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTag')),
                'errors': get_tags_assigned_to_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_domain_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'assign_tags_to_domain': {
                'input_type': assign_tags_to_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': assign_tags_to_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': assign_tags_to_domain_input_value_validator_list,
                'output_validator_list': assign_tags_to_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'remove_tags_from_domain': {
                'input_type': remove_tags_from_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'TagAssignmentResult')),
                'errors': remove_tags_from_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': remove_tags_from_domain_input_value_validator_list,
                'output_validator_list': remove_tags_from_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_tags_assigned_to_domains': {
                'input_type': get_tags_assigned_to_domains_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfTagsForResource')),
                'errors': get_tags_assigned_to_domains_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_tags_assigned_to_domains_input_value_validator_list,
                'output_validator_list': get_tags_assigned_to_domains_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_tags_assigned_to_domain': get_tags_assigned_to_domain_rest_metadata,
            'assign_tags_to_domain': assign_tags_to_domain_rest_metadata,
            'remove_tags_from_domain': remove_tags_from_domain_rest_metadata,
            'get_tags_assigned_to_domains': get_tags_assigned_to_domains_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.tags',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ResourceCertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_certificates_by_domain operation
        get_certificates_by_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_certificates_by_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_certificates_by_domain_input_value_validator_list = [
        ]
        get_certificates_by_domain_output_validator_list = [
        ]
        get_certificates_by_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/resource-certificates',
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

        # properties for replace_resource_certificates operation
        replace_resource_certificates_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'replace_resource_certificates_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceCertificateSpec')),
        })
        replace_resource_certificates_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        replace_resource_certificates_input_value_validator_list = [
        ]
        replace_resource_certificates_output_validator_list = [
        ]
        replace_resource_certificates_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/domains/{id}/resource-certificates',
            request_body_parameter='replace_resource_certificates_request_body',
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

        # properties for set_auto_renew_configuration_for_domain operation
        set_auto_renew_configuration_for_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'domain_resource_certificates_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DomainResourceCertificatesUpdateSpec'),
        })
        set_auto_renew_configuration_for_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        set_auto_renew_configuration_for_domain_input_value_validator_list = [
        ]
        set_auto_renew_configuration_for_domain_output_validator_list = [
        ]
        set_auto_renew_configuration_for_domain_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{id}/resource-certificates',
            request_body_parameter='domain_resource_certificates_update_spec',
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

        # properties for set_auto_renew_configuration operation
        set_auto_renew_configuration_input_type = type.StructType('operation-input', {
            'resource_certificates_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ResourceCertificatesUpdateSpec'),
        })
        set_auto_renew_configuration_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        set_auto_renew_configuration_input_value_validator_list = [
        ]
        set_auto_renew_configuration_output_validator_list = [
        ]
        set_auto_renew_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/resource-certificates',
            request_body_parameter='resource_certificates_update_spec',
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
            'get_certificates_by_domain': {
                'input_type': get_certificates_by_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCertificate')),
                'errors': get_certificates_by_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_certificates_by_domain_input_value_validator_list,
                'output_validator_list': get_certificates_by_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'replace_resource_certificates': {
                'input_type': replace_resource_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': replace_resource_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': replace_resource_certificates_input_value_validator_list,
                'output_validator_list': replace_resource_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set_auto_renew_configuration_for_domain': {
                'input_type': set_auto_renew_configuration_for_domain_input_type,
                'output_type': type.VoidType(),
                'errors': set_auto_renew_configuration_for_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,404,403,400]).build(),
                'input_value_validator_list': set_auto_renew_configuration_for_domain_input_value_validator_list,
                'output_validator_list': set_auto_renew_configuration_for_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set_auto_renew_configuration': {
                'input_type': set_auto_renew_configuration_input_type,
                'output_type': type.VoidType(),
                'errors': set_auto_renew_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,401,404,403,400]).build(),
                'input_value_validator_list': set_auto_renew_configuration_input_value_validator_list,
                'output_validator_list': set_auto_renew_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_certificates_by_domain': get_certificates_by_domain_rest_metadata,
            'replace_resource_certificates': replace_resource_certificates_rest_metadata,
            'set_auto_renew_configuration_for_domain': set_auto_renew_configuration_for_domain_rest_metadata,
            'set_auto_renew_configuration': set_auto_renew_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.resource_certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CsrsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_CS_rs operation
        get_CS_rs_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_CS_rs_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_CS_rs_input_value_validator_list = [
        ]
        get_CS_rs_output_validator_list = [
        ]
        get_CS_rs_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/csrs',
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

        # properties for generates_CS_rs operation
        generates_CS_rs_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'csrs_generation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CsrsGenerationSpec'),
        })
        generates_CS_rs_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        generates_CS_rs_input_value_validator_list = [
        ]
        generates_CS_rs_output_validator_list = [
        ]
        generates_CS_rs_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/domains/{id}/csrs',
            request_body_parameter='csrs_generation_spec',
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
            'get_CS_rs': {
                'input_type': get_CS_rs_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCsr')),
                'errors': get_CS_rs_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_CS_rs_input_value_validator_list,
                'output_validator_list': get_CS_rs_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'generates_CS_rs': {
                'input_type': generates_CS_rs_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': generates_CS_rs_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400,409]).build(),
                'input_value_validator_list': generates_CS_rs_input_value_validator_list,
                'output_validator_list': generates_CS_rs_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_CS_rs': get_CS_rs_rest_metadata,
            'generates_CS_rs': generates_CS_rs_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.csrs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domain_certificates operation
        get_domain_certificates_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_certificates_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_certificates_input_value_validator_list = [
        ]
        get_domain_certificates_output_validator_list = [
        ]
        get_domain_certificates_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/certificates',
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

        # properties for generate_certificates operation
        generate_certificates_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'certificates_generation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CertificatesGenerationSpec'),
        })
        generate_certificates_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        generate_certificates_input_value_validator_list = [
        ]
        generate_certificates_output_validator_list = [
        ]
        generate_certificates_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/domains/{id}/certificates',
            request_body_parameter='certificates_generation_spec',
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

        # properties for replace_certificates operation
        replace_certificates_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'certificate_operation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'CertificateOperationSpec'),
        })
        replace_certificates_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        replace_certificates_input_value_validator_list = [
        ]
        replace_certificates_output_validator_list = [
        ]
        replace_certificates_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{id}/certificates',
            request_body_parameter='certificate_operation_spec',
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
            'get_domain_certificates': {
                'input_type': get_domain_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfCertificate')),
                'errors': get_domain_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_domain_certificates_input_value_validator_list,
                'output_validator_list': get_domain_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'generate_certificates': {
                'input_type': generate_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': generate_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400,409]).build(),
                'input_value_validator_list': generate_certificates_input_value_validator_list,
                'output_validator_list': generate_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'replace_certificates': {
                'input_type': replace_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': replace_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,403,400,409]).build(),
                'input_value_validator_list': replace_certificates_input_value_validator_list,
                'output_validator_list': replace_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domain_certificates': get_domain_certificates_rest_metadata,
            'generate_certificates': generate_certificates_rest_metadata,
            'replace_certificates': replace_certificates_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for validate_domain_update_spec operation
        validate_domain_update_spec_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'domain_update_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DomainUpdateSpec'),
        })
        validate_domain_update_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_domain_update_spec_input_value_validator_list = [
        ]
        validate_domain_update_spec_output_validator_list = [
        ]
        validate_domain_update_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{id}/validations',
            request_body_parameter='domain_update_spec',
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

        # properties for validate_domain_creation_spec operation
        validate_domain_creation_spec_input_type = type.StructType('operation-input', {
            'domain_creation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'DomainCreationSpec'),
            'hosts_only': type.OptionalType(type.BooleanType()),
            'skip_host_switch_validation': type.OptionalType(type.BooleanType()),
        })
        validate_domain_creation_spec_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        validate_domain_creation_spec_input_value_validator_list = [
        ]
        validate_domain_creation_spec_output_validator_list = [
        ]
        validate_domain_creation_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/validations',
            request_body_parameter='domain_creation_spec',
            path_variables={
            },
            query_parameters={
                'hosts_only': 'hostsOnly',
                'skip_host_switch_validation': 'skipHostSwitchValidation',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_domain_update_validation operation
        get_domain_update_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'validation_id': type.StringType(),
        })
        get_domain_update_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_update_validation_input_value_validator_list = [
        ]
        get_domain_update_validation_output_validator_list = [
        ]
        get_domain_update_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/validations/{validationId}',
            path_variables={
                'id': 'id',
                'validation_id': 'validationId',
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

        # properties for domain_create_validation operation
        domain_create_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        domain_create_validation_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        domain_create_validation_input_value_validator_list = [
        ]
        domain_create_validation_output_validator_list = [
        ]
        domain_create_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/validations/{id}',
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
            'validate_domain_update_spec': {
                'input_type': validate_domain_update_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_domain_update_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_domain_update_spec_input_value_validator_list,
                'output_validator_list': validate_domain_update_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate_domain_creation_spec': {
                'input_type': validate_domain_creation_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': validate_domain_creation_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': validate_domain_creation_spec_input_value_validator_list,
                'output_validator_list': validate_domain_creation_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_domain_update_validation': {
                'input_type': get_domain_update_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': get_domain_update_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400]).build(),
                'input_value_validator_list': get_domain_update_validation_input_value_validator_list,
                'output_validator_list': get_domain_update_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'domain_create_validation': {
                'input_type': domain_create_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Validation')),
                'errors': domain_create_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,400]).build(),
                'input_value_validator_list': domain_create_validation_input_value_validator_list,
                'output_validator_list': domain_create_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'validate_domain_update_spec': validate_domain_update_spec_rest_metadata,
            'validate_domain_creation_spec': validate_domain_creation_spec_rest_metadata,
            'get_domain_update_validation': get_domain_update_validation_rest_metadata,
            'domain_create_validation': domain_create_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ComplianceAuditsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_compliance_audit_history_fora_domain operation
        get_compliance_audit_history_fora_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_compliance_audit_history_fora_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_history_fora_domain_input_value_validator_list = [
        ]
        get_compliance_audit_history_fora_domain_output_validator_list = [
        ]
        get_compliance_audit_history_fora_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/compliance-audits',
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

        # properties for compliance_audit operation
        compliance_audit_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'compliance_audit_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceAuditSpec'),
        })
        compliance_audit_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        compliance_audit_input_value_validator_list = [
        ]
        compliance_audit_output_validator_list = [
        ]
        compliance_audit_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{id}/compliance-audits',
            request_body_parameter='compliance_audit_spec',
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

        # properties for get_compliance_audit_fora_domain operation
        get_compliance_audit_fora_domain_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'compliance_audit_id': type.StringType(),
        })
        get_compliance_audit_fora_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_compliance_audit_fora_domain_input_value_validator_list = [
        ]
        get_compliance_audit_fora_domain_output_validator_list = [
        ]
        get_compliance_audit_fora_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/compliance-audits/{complianceAuditId}',
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
            'get_compliance_audit_history_fora_domain': {
                'input_type': get_compliance_audit_history_fora_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfComplianceAudit')),
                'errors': get_compliance_audit_history_fora_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_history_fora_domain_input_value_validator_list,
                'output_validator_list': get_compliance_audit_history_fora_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'compliance_audit': {
                'input_type': compliance_audit_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceTask')),
                'errors': compliance_audit_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': compliance_audit_input_value_validator_list,
                'output_validator_list': compliance_audit_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_compliance_audit_fora_domain': {
                'input_type': get_compliance_audit_fora_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'ComplianceAudit')),
                'errors': get_compliance_audit_fora_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [401,404,500]).build(),
                'input_value_validator_list': get_compliance_audit_fora_domain_input_value_validator_list,
                'output_validator_list': get_compliance_audit_fora_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_compliance_audit_history_fora_domain': get_compliance_audit_history_fora_domain_rest_metadata,
            'compliance_audit': compliance_audit_rest_metadata,
            'get_compliance_audit_fora_domain': get_compliance_audit_fora_domain_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.compliance_audits',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SynchronizationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for synchronization operation
        synchronization_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'brownfield_sync_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldSyncSpec'),
        })
        synchronization_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        synchronization_input_value_validator_list = [
        ]
        synchronization_output_validator_list = [
        ]
        synchronization_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{domainId}/synchronizations',
            request_body_parameter='brownfield_sync_spec',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_brownfield_sync_task_by_id operation
        get_brownfield_sync_task_by_id_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'task_id': type.StringType(),
        })
        get_brownfield_sync_task_by_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_brownfield_sync_task_by_id_input_value_validator_list = [
        ]
        get_brownfield_sync_task_by_id_output_validator_list = [
        ]
        get_brownfield_sync_task_by_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/synchronizations/{taskId}',
            path_variables={
                'domain_id': 'domainId',
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
            'synchronization': {
                'input_type': synchronization_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldTask')),
                'errors': synchronization_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': synchronization_input_value_validator_list,
                'output_validator_list': synchronization_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_brownfield_sync_task_by_id': {
                'input_type': get_brownfield_sync_task_by_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'BrownfieldTask')),
                'errors': get_brownfield_sync_task_by_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_brownfield_sync_task_by_id_input_value_validator_list,
                'output_validator_list': get_brownfield_sync_task_by_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'synchronization': synchronization_rest_metadata,
            'get_brownfield_sync_task_by_id': get_brownfield_sync_task_by_id_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.synchronizations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _IsolationPrechecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for perform_domain_isolation_precheck operation
        perform_domain_isolation_precheck_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'isolation_spec': type.ReferenceType('vmware.sddc_manager.model_client', 'IsolationSpec'),
        })
        perform_domain_isolation_precheck_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        perform_domain_isolation_precheck_input_value_validator_list = [
        ]
        perform_domain_isolation_precheck_output_validator_list = [
        ]
        perform_domain_isolation_precheck_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/domains/{domainId}/isolation-prechecks',
            request_body_parameter='isolation_spec',
            path_variables={
                'domain_id': 'domainId',
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

        # properties for get_domain_isolation_precheck_status operation
        get_domain_isolation_precheck_status_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'precheck_id': type.StringType(),
        })
        get_domain_isolation_precheck_status_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_isolation_precheck_status_input_value_validator_list = [
        ]
        get_domain_isolation_precheck_status_output_validator_list = [
        ]
        get_domain_isolation_precheck_status_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/isolation-prechecks/{precheckId}',
            path_variables={
                'domain_id': 'domainId',
                'precheck_id': 'precheckId',
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
            'perform_domain_isolation_precheck': {
                'input_type': perform_domain_isolation_precheck_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': perform_domain_isolation_precheck_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': perform_domain_isolation_precheck_input_value_validator_list,
                'output_validator_list': perform_domain_isolation_precheck_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_domain_isolation_precheck_status': {
                'input_type': get_domain_isolation_precheck_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'IsolationPrecheckResult')),
                'errors': get_domain_isolation_precheck_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_domain_isolation_precheck_status_input_value_validator_list,
                'output_validator_list': get_domain_isolation_precheck_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'perform_domain_isolation_precheck': perform_domain_isolation_precheck_rest_metadata,
            'get_domain_isolation_precheck_status': get_domain_isolation_precheck_status_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.isolation_prechecks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _OverlayStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for enable_overlay_over_management_network operation
        enable_overlay_over_management_network_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        enable_overlay_over_management_network_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        enable_overlay_over_management_network_input_value_validator_list = [
        ]
        enable_overlay_over_management_network_output_validator_list = [
        ]
        enable_overlay_over_management_network_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{id}/overlay',
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
            'enable_overlay_over_management_network': {
                'input_type': enable_overlay_over_management_network_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'Task')),
                'errors': enable_overlay_over_management_network_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [400,404,500]).build(),
                'input_value_validator_list': enable_overlay_over_management_network_input_value_validator_list,
                'output_validator_list': enable_overlay_over_management_network_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'enable_overlay_over_management_network': enable_overlay_over_management_network_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.overlay',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _HealthChecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vsan_health_check_by_domain operation
        get_vsan_health_check_by_domain_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'status': type.OptionalType(type.StringType()),
        })
        get_vsan_health_check_by_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_vsan_health_check_by_domain_input_value_validator_list = [
        ]
        get_vsan_health_check_by_domain_output_validator_list = [
        ]
        get_vsan_health_check_by_domain_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{domainId}/health-checks',
            path_variables={
                'domain_id': 'domainId',
            },
            query_parameters={
                'status': 'status',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update_vsan_health_check_by_domain operation
        update_vsan_health_check_by_domain_input_type = type.StructType('operation-input', {
            'domain_id': type.StringType(),
            'update_vsan_health_check_by_domain_request_body': type.ListType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthCheckSpec')),
        })
        update_vsan_health_check_by_domain_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        update_vsan_health_check_by_domain_input_value_validator_list = [
        ]
        update_vsan_health_check_by_domain_output_validator_list = [
        ]
        update_vsan_health_check_by_domain_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/domains/{domainId}/health-checks',
            request_body_parameter='update_vsan_health_check_by_domain_request_body',
            path_variables={
                'domain_id': 'domainId',
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
            'get_vsan_health_check_by_domain': {
                'input_type': get_vsan_health_check_by_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthCheckQueryResult')),
                'errors': get_vsan_health_check_by_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_vsan_health_check_by_domain_input_value_validator_list,
                'output_validator_list': get_vsan_health_check_by_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_vsan_health_check_by_domain': {
                'input_type': update_vsan_health_check_by_domain_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'HealthCheckTask')),
                'errors': update_vsan_health_check_by_domain_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': update_vsan_health_check_by_domain_input_value_validator_list,
                'output_validator_list': update_vsan_health_check_by_domain_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vsan_health_check_by_domain': get_vsan_health_check_by_domain_rest_metadata,
            'update_vsan_health_check_by_domain': update_vsan_health_check_by_domain_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.health_checks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _EndpointsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domain_endpoints operation
        get_domain_endpoints_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_endpoints_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_endpoints_input_value_validator_list = [
        ]
        get_domain_endpoints_output_validator_list = [
        ]
        get_domain_endpoints_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/endpoints',
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
            'get_domain_endpoints': {
                'input_type': get_domain_endpoints_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfEndpoint')),
                'errors': get_domain_endpoints_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_domain_endpoints_input_value_validator_list,
                'output_validator_list': get_domain_endpoints_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domain_endpoints': get_domain_endpoints_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.endpoints',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _DatacentersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domain_datacenters operation
        get_domain_datacenters_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_datacenters_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_datacenters_input_value_validator_list = [
        ]
        get_domain_datacenters_output_validator_list = [
        ]
        get_domain_datacenters_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/datacenters',
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
            'get_domain_datacenters': {
                'input_type': get_domain_datacenters_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'PageOfDatacenter')),
                'errors': get_domain_datacenters_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_domain_datacenters_input_value_validator_list,
                'output_validator_list': get_domain_datacenters_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domain_datacenters': get_domain_datacenters_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.datacenters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CapabilitiesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_domain_capabilities_by_domain_id operation
        get_domain_capabilities_by_domain_id_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_domain_capabilities_by_domain_id_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_capabilities_by_domain_id_input_value_validator_list = [
        ]
        get_domain_capabilities_by_domain_id_output_validator_list = [
        ]
        get_domain_capabilities_by_domain_id_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/{id}/capabilities',
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

        # properties for get_domain_capabilities operation
        get_domain_capabilities_input_type = type.StructType('operation-input', {
            'capabilities': type.OptionalType(type.ListType(type.StringType())),
        })
        get_domain_capabilities_error_dict = {
            'vmware.sddc_manager.model.error':
                type.ReferenceType('vmware.sddc_manager.model_client', 'Error'),

        }
        get_domain_capabilities_input_value_validator_list = [
        ]
        get_domain_capabilities_output_validator_list = [
        ]
        get_domain_capabilities_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/domains/capabilities',
            path_variables={
            },
            query_parameters={
                'capabilities': 'capabilities',
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
            'get_domain_capabilities_by_domain_id': {
                'input_type': get_domain_capabilities_by_domain_id_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DomainCapabilities')),
                'errors': get_domain_capabilities_by_domain_id_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,404,400]).build(),
                'input_value_validator_list': get_domain_capabilities_by_domain_id_input_value_validator_list,
                'output_validator_list': get_domain_capabilities_by_domain_id_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_domain_capabilities': {
                'input_type': get_domain_capabilities_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.sddc_manager.model_client', 'DomainsWithCapabilities')),
                'errors': get_domain_capabilities_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.sddc_manager.model_client', 'Error'), [500,400]).build(),
                'input_value_validator_list': get_domain_capabilities_input_value_validator_list,
                'output_validator_list': get_domain_capabilities_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_domain_capabilities_by_domain_id': get_domain_capabilities_by_domain_id_rest_metadata,
            'get_domain_capabilities': get_domain_capabilities_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.sddc_manager.v1.domains.capabilities',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tags': Tags,
        'ResourceCertificates': ResourceCertificates,
        'Csrs': Csrs,
        'Certificates': Certificates,
        'Validations': Validations,
        'ComplianceAudits': ComplianceAudits,
        'Synchronizations': Synchronizations,
        'IsolationPrechecks': IsolationPrechecks,
        'Overlay': Overlay,
        'HealthChecks': HealthChecks,
        'Endpoints': Endpoints,
        'Datacenters': Datacenters,
        'Capabilities': Capabilities,
        'clusters': 'vmware.sddc_manager.v1.domains.clusters_client.StubFactory',
        'compliance_audits': 'vmware.sddc_manager.v1.domains.compliance_audits_client.StubFactory',
        'csrs': 'vmware.sddc_manager.v1.domains.csrs_client.StubFactory',
        'datastores': 'vmware.sddc_manager.v1.domains.datastores_client.StubFactory',
        'health_checks': 'vmware.sddc_manager.v1.domains.health_checks_client.StubFactory',
        'resource_certificates': 'vmware.sddc_manager.v1.domains.resource_certificates_client.StubFactory',
        'tags': 'vmware.sddc_manager.v1.domains.tags_client.StubFactory',
    }

