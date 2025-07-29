# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.
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


class Tokens(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.tokens'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TokensStub)
        self._VAPI_OPERATION_IDS = {}


    def create_token(self,
                     token_creation_spec,
                     ):
        """
        Creates access token and refresh token for user access

        :type  token_creation_spec: :class:`vmware.vcf_installer.model_client.TokenCreationSpec`
        :param token_creation_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.TokenPair` or ``None``
        :return: Created
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('create_token',
                            {
                            'token_creation_spec': token_creation_spec,
                            })
class Sddcs(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SddcsStub)
        self._VAPI_OPERATION_IDS = {}


    def get_sddc_tasks(self):
        """
        


        :rtype: :class:`vmware.vcf_installer.model_client.PageOfSddcTask` or ``None``
        :return: Success
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_tasks', None)

    def deploy_sddc(self,
                    sddc_spec,
                    skip_validations=None,
                    ):
        """
        Start the workflow to install VCF (or VVF) based on the given SDDC
        specification.

        :type  sddc_spec: :class:`vmware.vcf_installer.model_client.SddcSpec`
        :param sddc_spec: 
        :type  skip_validations: :class:`bool` or ``None``
        :param skip_validations: Skips validations
        :rtype: :class:`vmware.vcf_installer.model_client.SddcTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Installation already exists
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('deploy_sddc',
                            {
                            'sddc_spec': sddc_spec,
                            'skip_validations': skip_validations,
                            })

    def get_sddc_task_by_id(self,
                            id,
                            ):
        """
        

        :type  id: :class:`str`
        :param id: Installation task ID
        :rtype: :class:`vmware.vcf_installer.model_client.SddcTask` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_sddc_task_by_ID',
                            {
                            'id': id,
                            })

    def retry_sddc(self,
                   id,
                   sddc_spec=None,
                   skip_validations=None,
                   ):
        """
        

        :type  id: :class:`str`
        :param id: Failed installation task ID
        :type  sddc_spec: :class:`vmware.vcf_installer.model_client.SddcSpec` or ``None``
        :param sddc_spec: 
        :type  skip_validations: :class:`bool` or ``None``
        :param skip_validations: Skips validations
        :rtype: :class:`vmware.vcf_installer.model_client.SddcTask` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 405. Not allowed
        """
        return self._invoke('retry_sddc',
                            {
                            'id': id,
                            'sddc_spec': sddc_spec,
                            'skip_validations': skip_validations,
                            })
class Bundles(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.bundles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BundlesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_bundles(self,
                    product_type=None,
                    is_compliant=None,
                    bundle_type=None,
                    ):
        """
        Get all Bundles. Returns uploaded bundles and bundles available via
        depot access.

        :type  product_type: :class:`str` or ``None``
        :param product_type: The type of the product
        :type  is_compliant: :class:`bool` or ``None``
        :param is_compliant: Is compliant with the current VCF version?
        :type  bundle_type: :class:`str` or ``None``
        :param bundle_type: The type of the bundle
        :rtype: :class:`vmware.vcf_installer.model_client.PageOfBundle` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_bundles',
                            {
                            'product_type': product_type,
                            'is_compliant': is_compliant,
                            'bundle_type': bundle_type,
                            })

    def upload_bundle(self,
                      bundle_upload_spec,
                      ):
        """
        Upload Bundle to SDDC Manager or VCF Installer. This is useful when you
        do not have internet connectivity for downloading bundles from the
        online depot to SDDC Manager or VCF Installer. The Bundles are manually
        downloaded from Depot using Bundle Transfer utility. This API is no
        longer supported from VCF 9.0. Please refer to POST v1/product-binaries
        instead.

        :type  bundle_upload_spec: :class:`vmware.vcf_installer.model_client.BundleUploadSpec`
        :param bundle_upload_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 410. This API is no longer supported from VCF
            9.0. Please refer to POST v1/product-binaries instead.
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('upload_bundle',
                            {
                            'bundle_upload_spec': bundle_upload_spec,
                            })

    def get_bundle(self,
                   id,
                   ):
        """
        Get a Bundle

        :type  id: :class:`str`
        :param id: Bundle ID
        :rtype: :class:`vmware.vcf_installer.model_client.Bundle` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Bundle Not Found
        """
        return self._invoke('get_bundle',
                            {
                            'id': id,
                            })

    def delete_bundle(self,
                      id,
                      binary_files_only=None,
                      ):
        """
        No Content

        :type  id: :class:`str`
        :param id: Bundle ID
        :type  binary_files_only: :class:`bool` or ``None``
        :param binary_files_only: binaryFilesOnly, if true, only binary files from storage will be
            deleted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. Conflict
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_bundle',
                            {
                            'id': id,
                            'binary_files_only': binary_files_only,
                            })

    def start_bundle_download_by_id(self,
                                    id,
                                    bundle_update_spec,
                                    ):
        """
        Update a Bundle for scheduling/triggering download. If download is
        started, this can be used to cancel a download. Only one download can
        triggered for a Bundle.

        :type  id: :class:`str`
        :param id: Bundle ID
        :type  bundle_update_spec: :class:`vmware.vcf_installer.model_client.BundleUpdateSpec`
        :param bundle_update_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.Task` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. Conflict
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('start_bundle_download_by_ID',
                            {
                            'id': id,
                            'bundle_update_spec': bundle_update_spec,
                            })
class Tasks(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TasksStub)
        self._VAPI_OPERATION_IDS = {}


    def get_task(self,
                 id,
                 ):
        """
        Get a Task by ID, if it exists

        :type  id: :class:`str`
        :param id: Task id to retrieve
        :rtype: :class:`vmware.vcf_installer.model_client.Task` or ``None``
        :return: A task object.
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Task not found
        """
        return self._invoke('get_task',
                            {
                            'id': id,
                            })

    def cancel_task(self,
                    id,
                    ):
        """
        Task was cancelled successfully.

        :type  id: :class:`str`
        :param id: Task id for cancelling
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Task not found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. Task can not be cancelled. Only a
            IN_PROGRESS task can be cancelled.
        """
        return self._invoke('cancel_task',
                            {
                            'id': id,
                            })

    def retry_task(self,
                   id,
                   ):
        """
        Task was retried successfully.

        :type  id: :class:`str`
        :param id: Task id retry
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. Task can not be retried. Only a failed Task
            can be retried.
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Unexpected error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Task not found
        """
        return self._invoke('retry_task',
                            {
                            'id': id,
                            })

    def get_tasks(self,
                  limit=None,
                  task_status=None,
                  task_type=None,
                  resource_id=None,
                  resource_type=None,
                  completed_after=None,
                  page_number=None,
                  page_size=None,
                  order_direction=None,
                  order_by=None,
                  task_name=None,
                  do_live_refresh=None,
                  ):
        """
        Get the tasks

        :type  limit: :class:`long` or ``None``
        :param limit: The number of elements to be returned in the result
        :type  task_status: :class:`str` or ``None``
        :param task_status: 
        :type  task_type: :class:`str` or ``None``
        :param task_type: 
        :type  resource_id: :class:`str` or ``None``
        :param resource_id: 
        :type  resource_type: :class:`str` or ``None``
        :param resource_type: 
        :type  completed_after: :class:`long` or ``None``
        :param completed_after: A time based filter to get tasks which are completed after the
            given timestamp. A task is completed if its status is 'Successful'
            or 'Failed'. Time is in milliseconds.
        :type  page_number: :class:`long` or ``None``
        :param page_number: Page number.
        :type  page_size: :class:`long` or ``None``
        :param page_size: Size of the page you want to retrieve. Max page size allowed is
            100.
        :type  order_direction: :class:`str` or ``None``
        :param order_direction: 
        :type  order_by: :class:`str` or ``None``
        :param order_by: 
        :type  task_name: :class:`str` or ``None``
        :param task_name: Search filter when task name contains text.
        :type  do_live_refresh: :class:`bool` or ``None``
        :param do_live_refresh: 
        :rtype: :class:`vmware.vcf_installer.model_client.PageOfTask` or ``None``
        :return: Returns the list of tasks.
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Unexpected error
        """
        return self._invoke('get_tasks',
                            {
                            'limit': limit,
                            'task_status': task_status,
                            'task_type': task_type,
                            'resource_id': resource_id,
                            'resource_type': resource_type,
                            'completed_after': completed_after,
                            'page_number': page_number,
                            'page_size': page_size,
                            'order_direction': order_direction,
                            'order_by': order_by,
                            'task_name': task_name,
                            'do_live_refresh': do_live_refresh,
                            })
class System(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system'
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


    def get_system_configuration(self):
        """
        Retrieve the system configuration.


        :rtype: :class:`vmware.vcf_installer.model_client.System` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_system_configuration', None)

    def update_system_configuration(self,
                                    system_update_spec,
                                    ):
        """
        OK

        :type  system_update_spec: :class:`vmware.vcf_installer.model_client.SystemUpdateSpec`
        :param system_update_spec: 
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_system_configuration',
                            {
                            'system_update_spec': system_update_spec,
                            })
class VcfServices(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.vcf_services'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcfServicesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_vcf_services(self):
        """
        


        :rtype: :class:`vmware.vcf_installer.model_client.PageOfVcfService` or ``None``
        :return: Ok
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_vcf_services', None)

    def get_vcf_service(self,
                        id,
                        ):
        """
        

        :type  id: :class:`str`
        :param id: VcfService ID
        :rtype: :class:`vmware.vcf_installer.model_client.VcfService` or ``None``
        :return: Ok
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. VcfService not found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. InternalServerError
        """
        return self._invoke('get_vcf_service',
                            {
                            'id': id,
                            })
class Releases(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.releases'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ReleasesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_releases(self,
                     domain_id=None,
                     version_eq=None,
                     version_gt=None,
                     version_ge=None,
                     applicable_for_version=None,
                     min_installer_version_le=None,
                     get_future_releases=None,
                     include_only_compatible=None,
                     ):
        """
        Get all Releases, with option to get current release for a domain, get
        release by version or get future releases for a versionor get all the
        applicable target release.

        :type  domain_id: :class:`str` or ``None``
        :param domain_id: Domain ID to get current release of the domain
        :type  version_eq: :class:`str` or ``None``
        :param version_eq: Release version to get its release
        :type  version_gt: :class:`str` or ``None``
        :param version_gt: Release version to get its future releases
        :type  version_ge: :class:`str` or ``None``
        :param version_ge: Release version to get its current & future releases
        :type  applicable_for_version: :class:`str` or ``None``
        :param applicable_for_version: Release version to get applicable releases
        :type  min_installer_version_le: :class:`str` or ``None``
        :param min_installer_version_le: Releases with minInstallerVersion less than given
            minInstallerVersion
        :type  get_future_releases: :class:`bool` or ``None``
        :param get_future_releases: [Deprecated] Get all future releases for a given domain
        :type  include_only_compatible: :class:`bool` or ``None``
        :param include_only_compatible: Filter only compatible releases on the system
        :rtype: :class:`vmware.vcf_installer.model_client.PageOfRelease` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 403. Forbidden
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Release Not Found
        """
        return self._invoke('get_releases',
                            {
                            'domain_id': domain_id,
                            'version_eq': version_eq,
                            'version_gt': version_gt,
                            'version_ge': version_ge,
                            'applicable_for_version': applicable_for_version,
                            'min_installer_version_le': min_installer_version_le,
                            'get_future_releases': get_future_releases,
                            'include_only_compatible': include_only_compatible,
                            })
class _TokensStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create_token operation
        create_token_input_type = type.StructType('operation-input', {
            'token_creation_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'TokenCreationSpec'),
        })
        create_token_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        create_token_input_value_validator_list = [
        ]
        create_token_output_validator_list = [
        ]
        create_token_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/tokens',
            request_body_parameter='token_creation_spec',
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
            'create_token': {
                'input_type': create_token_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'TokenPair')),
                'errors': create_token_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': create_token_input_value_validator_list,
                'output_validator_list': create_token_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create_token': create_token_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.tokens',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SddcsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_sddc_tasks operation
        get_sddc_tasks_input_type = type.StructType('operation-input', {})
        get_sddc_tasks_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_sddc_tasks_input_value_validator_list = [
        ]
        get_sddc_tasks_output_validator_list = [
        ]
        get_sddc_tasks_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs',
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

        # properties for deploy_sddc operation
        deploy_sddc_input_type = type.StructType('operation-input', {
            'sddc_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'SddcSpec'),
            'skip_validations': type.OptionalType(type.BooleanType()),
        })
        deploy_sddc_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        deploy_sddc_input_value_validator_list = [
        ]
        deploy_sddc_output_validator_list = [
        ]
        deploy_sddc_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddcs',
            request_body_parameter='sddc_spec',
            path_variables={
            },
            query_parameters={
                'skip_validations': 'skipValidations',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get_sddc_task_by_ID operation
        get_sddc_task_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_sddc_task_by_ID_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_sddc_task_by_ID_input_value_validator_list = [
        ]
        get_sddc_task_by_ID_output_validator_list = [
        ]
        get_sddc_task_by_ID_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/{id}',
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

        # properties for retry_sddc operation
        retry_sddc_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'sddc_spec': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcSpec')),
            'skip_validations': type.OptionalType(type.BooleanType()),
        })
        retry_sddc_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        retry_sddc_input_value_validator_list = [
        ]
        retry_sddc_output_validator_list = [
        ]
        retry_sddc_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/sddcs/{id}',
            request_body_parameter='sddc_spec',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'skip_validations': 'skipValidations',
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
            'get_sddc_tasks': {
                'input_type': get_sddc_tasks_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfSddcTask')),
                'errors': get_sddc_tasks_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_sddc_tasks_input_value_validator_list,
                'output_validator_list': get_sddc_tasks_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'deploy_sddc': {
                'input_type': deploy_sddc_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcTask')),
                'errors': deploy_sddc_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': deploy_sddc_input_value_validator_list,
                'output_validator_list': deploy_sddc_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_sddc_task_by_ID': {
                'input_type': get_sddc_task_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcTask')),
                'errors': get_sddc_task_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,400,500]).build(),
                'input_value_validator_list': get_sddc_task_by_ID_input_value_validator_list,
                'output_validator_list': get_sddc_task_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'retry_sddc': {
                'input_type': retry_sddc_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'SddcTask')),
                'errors': retry_sddc_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,400,500,405]).build(),
                'input_value_validator_list': retry_sddc_input_value_validator_list,
                'output_validator_list': retry_sddc_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_sddc_tasks': get_sddc_tasks_rest_metadata,
            'deploy_sddc': deploy_sddc_rest_metadata,
            'get_sddc_task_by_ID': get_sddc_task_by_ID_rest_metadata,
            'retry_sddc': retry_sddc_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _BundlesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_bundles operation
        get_bundles_input_type = type.StructType('operation-input', {
            'product_type': type.OptionalType(type.StringType()),
            'is_compliant': type.OptionalType(type.BooleanType()),
            'bundle_type': type.OptionalType(type.StringType()),
        })
        get_bundles_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_bundles_input_value_validator_list = [
        ]
        get_bundles_output_validator_list = [
        ]
        get_bundles_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles',
            path_variables={
            },
            query_parameters={
                'product_type': 'productType',
                'is_compliant': 'isCompliant',
                'bundle_type': 'bundleType',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for upload_bundle operation
        upload_bundle_input_type = type.StructType('operation-input', {
            'bundle_upload_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'BundleUploadSpec'),
        })
        upload_bundle_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        upload_bundle_input_value_validator_list = [
        ]
        upload_bundle_output_validator_list = [
        ]
        upload_bundle_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/bundles',
            request_body_parameter='bundle_upload_spec',
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

        # properties for get_bundle operation
        get_bundle_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_bundle_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_bundle_input_value_validator_list = [
        ]
        get_bundle_output_validator_list = [
        ]
        get_bundle_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/bundles/{id}',
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

        # properties for delete_bundle operation
        delete_bundle_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'binary_files_only': type.OptionalType(type.BooleanType()),
        })
        delete_bundle_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        delete_bundle_input_value_validator_list = [
        ]
        delete_bundle_output_validator_list = [
        ]
        delete_bundle_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/bundles/{id}',
            path_variables={
                'id': 'id',
            },
            query_parameters={
                'binary_files_only': 'binaryFilesOnly',
            },
            dispatch_parameters={
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for start_bundle_download_by_ID operation
        start_bundle_download_by_ID_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
            'bundle_update_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'BundleUpdateSpec'),
        })
        start_bundle_download_by_ID_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        start_bundle_download_by_ID_input_value_validator_list = [
        ]
        start_bundle_download_by_ID_output_validator_list = [
        ]
        start_bundle_download_by_ID_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/bundles/{id}',
            request_body_parameter='bundle_update_spec',
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
            'get_bundles': {
                'input_type': get_bundles_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfBundle')),
                'errors': get_bundles_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_bundles_input_value_validator_list,
                'output_validator_list': get_bundles_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'upload_bundle': {
                'input_type': upload_bundle_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Task')),
                'errors': upload_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [410,400,500]).build(),
                'input_value_validator_list': upload_bundle_input_value_validator_list,
                'output_validator_list': upload_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_bundle': {
                'input_type': get_bundle_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Bundle')),
                'errors': get_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_bundle_input_value_validator_list,
                'output_validator_list': get_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_bundle': {
                'input_type': delete_bundle_input_type,
                'output_type': type.VoidType(),
                'errors': delete_bundle_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [409,400,500]).build(),
                'input_value_validator_list': delete_bundle_input_value_validator_list,
                'output_validator_list': delete_bundle_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'start_bundle_download_by_ID': {
                'input_type': start_bundle_download_by_ID_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Task')),
                'errors': start_bundle_download_by_ID_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [409,400,500]).build(),
                'input_value_validator_list': start_bundle_download_by_ID_input_value_validator_list,
                'output_validator_list': start_bundle_download_by_ID_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_bundles': get_bundles_rest_metadata,
            'upload_bundle': upload_bundle_rest_metadata,
            'get_bundle': get_bundle_rest_metadata,
            'delete_bundle': delete_bundle_rest_metadata,
            'start_bundle_download_by_ID': start_bundle_download_by_ID_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.bundles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_task operation
        get_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_task_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_task_input_value_validator_list = [
        ]
        get_task_output_validator_list = [
        ]
        get_task_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/tasks/{id}',
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

        # properties for cancel_task operation
        cancel_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        cancel_task_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        cancel_task_input_value_validator_list = [
        ]
        cancel_task_output_validator_list = [
        ]
        cancel_task_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/tasks/{id}',
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

        # properties for retry_task operation
        retry_task_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        retry_task_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        retry_task_input_value_validator_list = [
        ]
        retry_task_output_validator_list = [
        ]
        retry_task_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/tasks/{id}',
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

        # properties for get_tasks operation
        get_tasks_input_type = type.StructType('operation-input', {
            'limit': type.OptionalType(type.IntegerType()),
            'task_status': type.OptionalType(type.StringType()),
            'task_type': type.OptionalType(type.StringType()),
            'resource_id': type.OptionalType(type.StringType()),
            'resource_type': type.OptionalType(type.StringType()),
            'completed_after': type.OptionalType(type.IntegerType()),
            'page_number': type.OptionalType(type.IntegerType()),
            'page_size': type.OptionalType(type.IntegerType()),
            'order_direction': type.OptionalType(type.StringType()),
            'order_by': type.OptionalType(type.StringType()),
            'task_name': type.OptionalType(type.StringType()),
            'do_live_refresh': type.OptionalType(type.BooleanType()),
        })
        get_tasks_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_tasks_input_value_validator_list = [
        ]
        get_tasks_output_validator_list = [
        ]
        get_tasks_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/tasks',
            path_variables={
            },
            query_parameters={
                'limit': 'limit',
                'task_status': 'taskStatus',
                'task_type': 'taskType',
                'resource_id': 'resourceId',
                'resource_type': 'resourceType',
                'completed_after': 'completedAfter',
                'page_number': 'pageNumber',
                'page_size': 'pageSize',
                'order_direction': 'orderDirection',
                'order_by': 'orderBy',
                'task_name': 'taskName',
                'do_live_refresh': 'doLiveRefresh',
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
            'get_task': {
                'input_type': get_task_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Task')),
                'errors': get_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500,404]).build(),
                'input_value_validator_list': get_task_input_value_validator_list,
                'output_validator_list': get_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel_task': {
                'input_type': cancel_task_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500,404,409]).build(),
                'input_value_validator_list': cancel_task_input_value_validator_list,
                'output_validator_list': cancel_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'retry_task': {
                'input_type': retry_task_input_type,
                'output_type': type.VoidType(),
                'errors': retry_task_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [409,500,404]).build(),
                'input_value_validator_list': retry_task_input_value_validator_list,
                'output_validator_list': retry_task_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_tasks': {
                'input_type': get_tasks_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfTask')),
                'errors': get_tasks_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_tasks_input_value_validator_list,
                'output_validator_list': get_tasks_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_task': get_task_rest_metadata,
            'cancel_task': cancel_task_rest_metadata,
            'retry_task': retry_task_rest_metadata,
            'get_tasks': get_tasks_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_system_configuration operation
        get_system_configuration_input_type = type.StructType('operation-input', {})
        get_system_configuration_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_system_configuration_input_value_validator_list = [
        ]
        get_system_configuration_output_validator_list = [
        ]
        get_system_configuration_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system',
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

        # properties for update_system_configuration operation
        update_system_configuration_input_type = type.StructType('operation-input', {
            'system_update_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'SystemUpdateSpec'),
        })
        update_system_configuration_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        update_system_configuration_input_value_validator_list = [
        ]
        update_system_configuration_output_validator_list = [
        ]
        update_system_configuration_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/v1/system',
            request_body_parameter='system_update_spec',
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
            'get_system_configuration': {
                'input_type': get_system_configuration_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'System')),
                'errors': get_system_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_system_configuration_input_value_validator_list,
                'output_validator_list': get_system_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_system_configuration': {
                'input_type': update_system_configuration_input_type,
                'output_type': type.VoidType(),
                'errors': update_system_configuration_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_system_configuration_input_value_validator_list,
                'output_validator_list': update_system_configuration_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_system_configuration': get_system_configuration_rest_metadata,
            'update_system_configuration': update_system_configuration_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _VcfServicesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_vcf_services operation
        get_vcf_services_input_type = type.StructType('operation-input', {})
        get_vcf_services_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_vcf_services_input_value_validator_list = [
        ]
        get_vcf_services_output_validator_list = [
        ]
        get_vcf_services_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-services',
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

        # properties for get_vcf_service operation
        get_vcf_service_input_type = type.StructType('operation-input', {
            'id': type.StringType(),
        })
        get_vcf_service_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_vcf_service_input_value_validator_list = [
        ]
        get_vcf_service_output_validator_list = [
        ]
        get_vcf_service_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/vcf-services/{id}',
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
            'get_vcf_services': {
                'input_type': get_vcf_services_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfVcfService')),
                'errors': get_vcf_services_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': get_vcf_services_input_value_validator_list,
                'output_validator_list': get_vcf_services_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get_vcf_service': {
                'input_type': get_vcf_service_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'VcfService')),
                'errors': get_vcf_service_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_vcf_service_input_value_validator_list,
                'output_validator_list': get_vcf_service_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_vcf_services': get_vcf_services_rest_metadata,
            'get_vcf_service': get_vcf_service_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.vcf_services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)

class _ReleasesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_releases operation
        get_releases_input_type = type.StructType('operation-input', {
            'domain_id': type.OptionalType(type.StringType()),
            'version_eq': type.OptionalType(type.StringType()),
            'version_gt': type.OptionalType(type.StringType()),
            'version_ge': type.OptionalType(type.StringType()),
            'applicable_for_version': type.OptionalType(type.StringType()),
            'min_installer_version_le': type.OptionalType(type.StringType()),
            'get_future_releases': type.OptionalType(type.BooleanType()),
            'include_only_compatible': type.OptionalType(type.BooleanType()),
        })
        get_releases_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_releases_input_value_validator_list = [
        ]
        get_releases_output_validator_list = [
        ]
        get_releases_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/releases',
            path_variables={
            },
            query_parameters={
                'domain_id': 'domainId',
                'version_eq': 'versionEq',
                'version_gt': 'versionGt',
                'version_ge': 'versionGe',
                'applicable_for_version': 'applicableForVersion',
                'min_installer_version_le': 'minInstallerVersionLe',
                'get_future_releases': 'getFutureReleases',
                'include_only_compatible': 'includeOnlyCompatible',
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
            'get_releases': {
                'input_type': get_releases_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfRelease')),
                'errors': get_releases_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [403,500,404]).build(),
                'input_value_validator_list': get_releases_input_value_validator_list,
                'output_validator_list': get_releases_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_releases': get_releases_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.releases',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Tokens': Tokens,
        'Sddcs': Sddcs,
        'Bundles': Bundles,
        'Tasks': Tasks,
        'System': System,
        'VcfServices': VcfServices,
        'Releases': Releases,
        'bundles': 'vmware.vcf_installer.v1.bundles_client.StubFactory',
        'releases': 'vmware.vcf_installer.v1.releases_client.StubFactory',
        'sddc_manager': 'vmware.vcf_installer.v1.sddc_manager_client.StubFactory',
        'sddcs': 'vmware.vcf_installer.v1.sddcs_client.StubFactory',
        'system': 'vmware.vcf_installer.v1.system_client.StubFactory',
        'tokens': 'vmware.vcf_installer.v1.tokens_client.StubFactory',
    }

