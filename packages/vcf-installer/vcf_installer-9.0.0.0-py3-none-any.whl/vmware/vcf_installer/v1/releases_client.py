# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.releases.
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


class ReleaseComponents(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.releases.release_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ReleaseComponentsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_release_components_by_sku(self,
                                      sku,
                                      release_version=None,
                                      image_type=None,
                                      automated_install=None,
                                      lifecycle_managed_by=None,
                                      release_type=None,
                                      match_with_release_type=None,
                                      ):
        """
        Gets a list of components, the SKU they are part of and the available
        patch versions,per release version. By default it provide release
        components of all the release equal and above 5.x

        :type  sku: :class:`str`
        :param sku: SKU filter, to retrieve only components associated with a specific
            SKU (VCF or VVF)
        :type  release_version: :class:`str` or ``None``
        :param release_version: VCF Release Version
        :type  image_type: :class:`str` or ``None``
        :param image_type: image type for the image you want to retrieve.
        :type  automated_install: :class:`bool` or ``None``
        :param automated_install: Automated Install. If true, list all automated Install product. if
            false or empty, filter will not be applied. Applicable only for VCF
            9.0.0.0 and above releases releases
        :type  lifecycle_managed_by: :class:`str` or ``None``
        :param lifecycle_managed_by: Lifecycle managed by
        :type  release_type: :class:`list` of :class:`str` or ``None``
        :param release_type: List of release types
        :type  match_with_release_type: :class:`str` or ``None``
        :param match_with_release_type: Match with release type for provided releaseVersion
        :rtype: :class:`vmware.vcf_installer.model_client.PageOfReleaseComponentDetail` or ``None``
        :return: Ok
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_release_components_by_sku',
                            {
                            'sku': sku,
                            'release_version': release_version,
                            'image_type': image_type,
                            'automated_install': automated_install,
                            'lifecycle_managed_by': lifecycle_managed_by,
                            'release_type': release_type,
                            'match_with_release_type': match_with_release_type,
                            })
class System(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.releases.system'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SystemStub)
        self._VAPI_OPERATION_IDS = {}


    def get_system_release(self):
        """
        Returns release for the lowest deployed VCF version for a domain on the
        environment. If Management domain is ahead of WLD domain, VCF BOM
        version for the WLD domain will be returned. NOTE: This operation is
        not applicable if appliance is in VCF Installer mode.


        :rtype: :class:`vmware.vcf_installer.model_client.Release` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Release Not Found
        """
        return self._invoke('get_system_release', None)
class CustomPatches(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.releases.custom_patches'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CustomPatchesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_custom_patches_by_sku(self,
                                  sku=None,
                                  release_version=None,
                                  image_type=None,
                                  ):
        """
        Filter applicable patches (current/target VCF/VVF releases) per product
        type

        :type  sku: :class:`str` or ``None``
        :param sku: SKU (VCF or VVF)
        :type  release_version: :class:`str` or ``None``
        :param release_version: Release Version
        :type  image_type: :class:`str` or ``None``
        :param image_type: Image type for the image you want to retrieve.
        :rtype: :class:`vmware.vcf_installer.model_client.CustomPatches` or ``None``
        :return: Ok
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 422. Unprocessable Entity
        """
        return self._invoke('get_custom_patches_by_sku',
                            {
                            'sku': sku,
                            'release_version': release_version,
                            'image_type': image_type,
                            })
class _ReleaseComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_release_components_by_sku operation
        get_release_components_by_sku_input_type = type.StructType('operation-input', {
            'sku': type.StringType(),
            'release_version': type.OptionalType(type.StringType()),
            'image_type': type.OptionalType(type.StringType()),
            'automated_install': type.OptionalType(type.BooleanType()),
            'lifecycle_managed_by': type.OptionalType(type.StringType()),
            'release_type': type.OptionalType(type.ListType(type.StringType())),
            'match_with_release_type': type.OptionalType(type.StringType()),
        })
        get_release_components_by_sku_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_release_components_by_sku_input_value_validator_list = [
        ]
        get_release_components_by_sku_output_validator_list = [
        ]
        get_release_components_by_sku_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/{sku}/release-components',
            path_variables={
                'sku': 'sku',
            },
            query_parameters={
                'release_version': 'releaseVersion',
                'image_type': 'imageType',
                'automated_install': 'automatedInstall',
                'lifecycle_managed_by': 'lifecycleManagedBy',
                'release_type': 'releaseType',
                'match_with_release_type': 'matchWithReleaseType',
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
            'get_release_components_by_sku': {
                'input_type': get_release_components_by_sku_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfReleaseComponentDetail')),
                'errors': get_release_components_by_sku_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_release_components_by_sku_input_value_validator_list,
                'output_validator_list': get_release_components_by_sku_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_release_components_by_sku': get_release_components_by_sku_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.releases.release_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_release operation
        get_system_release_input_type = type.StructType('operation-input', {})
        get_system_release_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_system_release_input_value_validator_list = [
        ]
        get_system_release_output_validator_list = [
        ]
        get_system_release_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/system',
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
            'get_system_release': {
                'input_type': get_system_release_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Release')),
                'errors': get_system_release_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_system_release_input_value_validator_list,
                'output_validator_list': get_system_release_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_release': get_system_release_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.releases.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _CustomPatchesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_custom_patches_by_sku operation
        get_custom_patches_by_sku_input_type = type.StructType('operation-input', {
            'sku': type.OptionalType(type.StringType()),
            'release_version': type.OptionalType(type.StringType()),
            'image_type': type.OptionalType(type.StringType()),
        })
        get_custom_patches_by_sku_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_custom_patches_by_sku_input_value_validator_list = [
        ]
        get_custom_patches_by_sku_output_validator_list = [
        ]
        get_custom_patches_by_sku_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases/custom-patches',
            path_variables={
            },
            query_parameters={
                'sku': 'sku',
                'release_version': 'releaseVersion',
                'image_type': 'imageType',
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
            'get_custom_patches_by_sku': {
                'input_type': get_custom_patches_by_sku_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'CustomPatches')),
                'errors': get_custom_patches_by_sku_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,400,500,422]).build(),
                'input_value_validator_list': get_custom_patches_by_sku_input_value_validator_list,
                'output_validator_list': get_custom_patches_by_sku_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_custom_patches_by_sku': get_custom_patches_by_sku_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.releases.custom_patches',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ReleaseComponents': ReleaseComponents,
        'System': System,
        'CustomPatches': CustomPatches,
        'domains': 'vmware.vcf_installer.v1.releases.domains_client.StubFactory',
    }

