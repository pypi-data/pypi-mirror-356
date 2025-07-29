# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.sddcs.
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


class VcfopsDiscovery(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.vcfops_discovery'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcfopsDiscoveryStub)
        self._VAPI_OPERATION_IDS = {}


    def discover_vcf_ops(self,
                         vcf_operations_discovery_spec,
                         ):
        """
        Discover VCF Operations instance and its adjacent topology such as its
        cluster nodes, management node, vCenters, etc.

        :type  vcf_operations_discovery_spec: :class:`vmware.vcf_installer.model_client.VcfOperationsDiscoverySpec`
        :param vcf_operations_discovery_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.VcfOperationsDiscoveryResult` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('discover_vcf_ops',
                            {
                            'vcf_operations_discovery_spec': vcf_operations_discovery_spec,
                            })
class VcenterDiscovery(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.vcenter_discovery'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcenterDiscoveryStub)
        self._VAPI_OPERATION_IDS = {}


    def discover_vcenter(self,
                         vcenter_discovery_spec,
                         ):
        """
        Discover vCenter instance and its adjacent topology such as NSX
        instances associated with it.

        :type  vcenter_discovery_spec: :class:`vmware.vcf_installer.model_client.VcenterDiscoverySpec`
        :param vcenter_discovery_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.VcenterDiscoveryResult` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('discover_vcenter',
                            {
                            'vcenter_discovery_spec': vcenter_discovery_spec,
                            })
class Validations(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.validations'
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


    def get_sddc_spec_validations(self):
        """
        


        :rtype: :class:`vmware.vcf_installer.model_client.PageOfValidation` or ``None``
        :return: Success
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 501. Not Implemented
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_spec_validations', None)

    def validate_sddc_spec(self,
                           sddc_spec,
                           ):
        """
        VCF Installer specification incorporates all the client inputs
        regarding VCF (or VVF) components constituting the installation.

        :type  sddc_spec: :class:`vmware.vcf_installer.model_client.SddcSpec`
        :param sddc_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.Validation` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad user input
        """
        return self._invoke('validate_sddc_spec',
                            {
                            'sddc_spec': sddc_spec,
                            })

    def get_sddc_spec_validation(self,
                                 id,
                                 ):
        """
        

        :type  id: :class:`str`
        :param id: VCF (or VVF) installation validation ID
        :rtype: :class:`vmware.vcf_installer.model_client.Validation` or ``None``
        :return: Success
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 501. Not Implemented
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_spec_validation',
                            {
                            'id': id,
                            })
class NetworkConfigProfiles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.network_config_profiles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworkConfigProfilesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_network_config_profiles(self,
                                    sddc_network_config_profile_spec,
                                    ):
        """
        Get network profiles compatible with the storage type and hosts subject
        to installation.

        :type  sddc_network_config_profile_spec: :class:`vmware.vcf_installer.model_client.SddcNetworkConfigProfileSpec`
        :param sddc_network_config_profile_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.SddcNetworkConfigProfileResponse` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_network_config_profiles',
                            {
                            'sddc_network_config_profile_spec': sddc_network_config_profile_spec,
                            })
class InstallerMode(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.installer_mode'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _InstallerModeStub)
        self._VAPI_OPERATION_IDS = {}


    def get_installer_type(self,
                           sddc_installer_request,
                           ):
        """
        Get the VCF Installer mode that specifies whether the VCF Installer
        appliance is collocated with the VCF (or VVF) installation or is
        located externally.

        :type  sddc_installer_request: :class:`vmware.vcf_installer.model_client.SddcInstallerRequest`
        :param sddc_installer_request: 
        :rtype: :class:`vmware.vcf_installer.model_client.InstallerSpec` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_installer_type',
                            {
                            'sddc_installer_request': sddc_installer_request,
                            })
class Spec(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.spec'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SpecStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sddc_spec_by_id(self,
                            id,
                            ):
        """
        

        :type  id: :class:`str`
        :param id: Installation task ID
        :rtype: :class:`vmware.vcf_installer.model_client.SddcSpec` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_spec_by_ID',
                            {
                            'id': id,
                            })
class Latest(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.latest'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LatestStub)
        self._VAPI_OPERATION_IDS = {}


    def get_latest_sddc_task(self):
        """
        


        :rtype: :class:`vmware.vcf_installer.model_client.SddcTask` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_latest_sddc_task', None)
class _VcfopsDiscoveryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for discover_vcf_ops operation
        discover_vcf_ops_input_type = type.StructType('operation-input', {
            'vcf_operations_discovery_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'VcfOperationsDiscoverySpec'),
        })
        discover_vcf_ops_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        discover_vcf_ops_input_value_validator_list = [
        ]
        discover_vcf_ops_output_validator_list = [
        ]
        discover_vcf_ops_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/vcfops-discovery',
            request_body_parameter='vcf_operations_discovery_spec',
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
            'discover_vcf_ops': {
                'input_type': discover_vcf_ops_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'VcfOperationsDiscoveryResult')),
                'errors': discover_vcf_ops_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': discover_vcf_ops_input_value_validator_list,
                'output_validator_list': discover_vcf_ops_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'discover_vcf_ops': discover_vcf_ops_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.vcfops_discovery',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcenterDiscoveryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for discover_vcenter operation
        discover_vcenter_input_type = type.StructType('operation-input', {
            'vcenter_discovery_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'VcenterDiscoverySpec'),
        })
        discover_vcenter_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        discover_vcenter_input_value_validator_list = [
        ]
        discover_vcenter_output_validator_list = [
        ]
        discover_vcenter_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/vcenter-discovery',
            request_body_parameter='vcenter_discovery_spec',
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
            'discover_vcenter': {
                'input_type': discover_vcenter_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'VcenterDiscoveryResult')),
                'errors': discover_vcenter_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': discover_vcenter_input_value_validator_list,
                'output_validator_list': discover_vcenter_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'discover_vcenter': discover_vcenter_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.vcenter_discovery',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ValidationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_sddc_spec_validations operation
        get_sddc_spec_validations_input_type = type.StructType('operation-input', {})
        get_sddc_spec_validations_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_sddc_spec_validations_input_value_validator_list = [
        ]
        get_sddc_spec_validations_output_validator_list = [
        ]
        get_sddc_spec_validations_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/validations',
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

        # properties for validate_sddc_spec operation
        validate_sddc_spec_input_type = type.StructType('operation-input', {
            'sddc_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'SddcSpec'),
        })
        validate_sddc_spec_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        validate_sddc_spec_input_value_validator_list = [
        ]
        validate_sddc_spec_output_validator_list = [
        ]
        validate_sddc_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/validations',
            request_body_parameter='sddc_spec',
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

        # properties for get_sddc_spec_validation operation
        get_sddc_spec_validation_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_sddc_spec_validation_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_sddc_spec_validation_input_value_validator_list = [
        ]
        get_sddc_spec_validation_output_validator_list = [
        ]
        get_sddc_spec_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/validations/{id}',
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
            'get_sddc_spec_validations': {
                'input_type': get_sddc_spec_validations_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfValidation')),
                'errors': get_sddc_spec_validations_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [501,404,500]).build(),
                'input_value_validator_list': get_sddc_spec_validations_input_value_validator_list,
                'output_validator_list': get_sddc_spec_validations_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate_sddc_spec': {
                'input_type': validate_sddc_spec_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Validation')),
                'errors': validate_sddc_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [403,404,500,400]).build(),
                'input_value_validator_list': validate_sddc_spec_input_value_validator_list,
                'output_validator_list': validate_sddc_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_sddc_spec_validation': {
                'input_type': get_sddc_spec_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Validation')),
                'errors': get_sddc_spec_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [501,404,500]).build(),
                'input_value_validator_list': get_sddc_spec_validation_input_value_validator_list,
                'output_validator_list': get_sddc_spec_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_sddc_spec_validations': get_sddc_spec_validations_rest_metadata,
            'validate_sddc_spec': validate_sddc_spec_rest_metadata,
            'get_sddc_spec_validation': get_sddc_spec_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.validations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _NetworkConfigProfilesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_network_config_profiles operation
        get_network_config_profiles_input_type = type.StructType('operation-input', {
            'sddc_network_config_profile_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'SddcNetworkConfigProfileSpec'),
        })
        get_network_config_profiles_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_network_config_profiles_input_value_validator_list = [
        ]
        get_network_config_profiles_output_validator_list = [
        ]
        get_network_config_profiles_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/network-config-profiles',
            request_body_parameter='sddc_network_config_profile_spec',
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
            'get_network_config_profiles': {
                'input_type': get_network_config_profiles_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcNetworkConfigProfileResponse')),
                'errors': get_network_config_profiles_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_network_config_profiles_input_value_validator_list,
                'output_validator_list': get_network_config_profiles_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_network_config_profiles': get_network_config_profiles_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.network_config_profiles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _InstallerModeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_installer_type operation
        get_installer_type_input_type = type.StructType('operation-input', {
            'sddc_installer_request': type.ReferenceType('vmware.vcf_installer.model_client', 'SddcInstallerRequest'),
        })
        get_installer_type_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_installer_type_input_value_validator_list = [
        ]
        get_installer_type_output_validator_list = [
        ]
        get_installer_type_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs/installer-mode',
            request_body_parameter='sddc_installer_request',
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
            'get_installer_type': {
                'input_type': get_installer_type_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'InstallerSpec')),
                'errors': get_installer_type_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_installer_type_input_value_validator_list,
                'output_validator_list': get_installer_type_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_installer_type': get_installer_type_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.installer_mode',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SpecStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_sddc_spec_by_ID operation
        get_sddc_spec_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_sddc_spec_by_ID_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_sddc_spec_by_ID_input_value_validator_list = [
        ]
        get_sddc_spec_by_ID_output_validator_list = [
        ]
        get_sddc_spec_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/{id}/spec',
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
            'get_sddc_spec_by_ID': {
                'input_type': get_sddc_spec_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcSpec')),
                'errors': get_sddc_spec_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_sddc_spec_by_ID_input_value_validator_list,
                'output_validator_list': get_sddc_spec_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_sddc_spec_by_ID': get_sddc_spec_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.spec',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _LatestStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_latest_sddc_task operation
        get_latest_sddc_task_input_type = type.StructType('operation-input', {})
        get_latest_sddc_task_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_latest_sddc_task_input_value_validator_list = [
        ]
        get_latest_sddc_task_output_validator_list = [
        ]
        get_latest_sddc_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/latest',
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
            'get_latest_sddc_task': {
                'input_type': get_latest_sddc_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcTask')),
                'errors': get_latest_sddc_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_latest_sddc_task_input_value_validator_list,
                'output_validator_list': get_latest_sddc_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_latest_sddc_task': get_latest_sddc_task_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.latest',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'VcfopsDiscovery': VcfopsDiscovery,
        'VcenterDiscovery': VcenterDiscovery,
        'Validations': Validations,
        'NetworkConfigProfiles': NetworkConfigProfiles,
        'InstallerMode': InstallerMode,
        'Spec': Spec,
        'Latest': Latest,
        'validations': 'vmware.vcf_installer.v1.sddcs.validations_client.StubFactory',
    }

