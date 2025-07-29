# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.system.
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


class ProxyConfiguration(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system.proxy_configuration'
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


        :rtype: :class:`vmware.vcf_installer.model_client.ProxyConfiguration` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('get_proxy_configuration', None)

    def update_proxy_configuration(self,
                                   proxy_configuration,
                                   ):
        """
        Update Proxy configuration

        :type  proxy_configuration: :class:`vmware.vcf_installer.model_client.ProxyConfiguration`
        :param proxy_configuration: 
        :rtype: :class:`vmware.vcf_installer.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad request
        """
        return self._invoke('update_proxy_configuration',
                            {
                            'proxy_configuration': proxy_configuration,
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

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system.ceip'
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


        :rtype: :class:`vmware.vcf_installer.model_client.Ceip` or ``None``
        :return: Ok
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
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
        :rtype: :class:`vmware.vcf_installer.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. The request could not be completed due to a
            conflict with the current state
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('set_ceip_status',
                            {
                            'set_ceip_status_request_body': set_ceip_status_request_body,
                            })
class VcfManagementComponents(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system.vcf_management_components'
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


        :rtype: :class:`vmware.vcf_installer.model_client.VcfManagementComponents` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_system_vcf_management_components', None)
class ApplianceInfo(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system.appliance_info'
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


        :rtype: :class:`vmware.vcf_installer.model_client.ApplianceInfo` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_appliance_info', None)
class _ProxyConfigurationStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_proxy_configuration operation
        get_proxy_configuration_input_type = type.StructType('operation-input', {})
        get_proxy_configuration_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
            'proxy_configuration': type.ReferenceType('vmware.vcf_installer.model_client', 'ProxyConfiguration'),
        })
        update_proxy_configuration_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'ProxyConfiguration')),
                'errors': get_proxy_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400]).build(),
                'input_value_validator_list': get_proxy_configuration_input_value_validator_list,
                'output_validator_list': get_proxy_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_proxy_configuration': {
                'input_type': update_proxy_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Task')),
                'errors': update_proxy_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400]).build(),
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
            self, iface_name='vmware.vcf_installer.v1.system.proxy_configuration',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CeipStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_ceip_status operation
        get_ceip_status_input_type = type.StructType('operation-input', {})
        get_ceip_status_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Ceip')),
                'errors': get_ceip_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_ceip_status_input_value_validator_list,
                'output_validator_list': get_ceip_status_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set_ceip_status': {
                'input_type': set_ceip_status_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Task')),
                'errors': set_ceip_status_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [409,400,500]).build(),
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
            self, iface_name='vmware.vcf_installer.v1.system.ceip',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcfManagementComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_vcf_management_components operation
        get_system_vcf_management_components_input_type = type.StructType('operation-input', {})
        get_system_vcf_management_components_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'VcfManagementComponents')),
                'errors': get_system_vcf_management_components_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [403,500]).build(),
                'input_value_validator_list': get_system_vcf_management_components_input_value_validator_list,
                'output_validator_list': get_system_vcf_management_components_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_vcf_management_components': get_system_vcf_management_components_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.system.vcf_management_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ApplianceInfoStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_appliance_info operation
        get_appliance_info_input_type = type.StructType('operation-input', {})
        get_appliance_info_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

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
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'ApplianceInfo')),
                'errors': get_appliance_info_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_appliance_info_input_value_validator_list,
                'output_validator_list': get_appliance_info_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_appliance_info': get_appliance_info_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.system.appliance_info',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ProxyConfiguration': ProxyConfiguration,
        'Ceip': Ceip,
        'VcfManagementComponents': VcfManagementComponents,
        'ApplianceInfo': ApplianceInfo,
        'settings': 'vmware.vcf_installer.v1.system.settings_client.StubFactory',
    }

