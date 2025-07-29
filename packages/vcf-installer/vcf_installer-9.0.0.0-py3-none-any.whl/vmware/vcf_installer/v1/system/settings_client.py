# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.system.settings.
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


class Depot(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.system.settings.depot'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DepotStub)
        self._VAPI_OPERATION_IDS = {}


    def get_depot_settings(self):
        """
        Get the depot configuration. In a fresh setup, this would be empty.


        :rtype: :class:`vmware.vcf_installer.model_client.DepotSettings` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_depot_settings', None)

    def update_depot_settings(self,
                              depot_settings,
                              ):
        """
        Update depot settings. Depot settings can be updated with VMware Depot
        account

        :type  depot_settings: :class:`vmware.vcf_installer.model_client.DepotSettings`
        :param depot_settings: 
        :rtype: :class:`vmware.vcf_installer.model_client.DepotSettings` or ``None``
        :return: Accepted
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('update_depot_settings',
                            {
                            'depot_settings': depot_settings,
                            })

    def delete_depot_settings(self,
                              depot_type=None,
                              ):
        """
        No Content

        :type  depot_type: :class:`str` or ``None``
        :param depot_type: Depot Type
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad Request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('delete_depot_settings',
                            {
                            'depot_type': depot_type,
                            })
class _DepotStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_depot_settings operation
        get_depot_settings_input_type = type.StructType('operation-input', {})
        get_depot_settings_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_depot_settings_input_value_validator_list = [
        ]
        get_depot_settings_output_validator_list = [
        ]
        get_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/system/settings/depot',
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

        # properties for update_depot_settings operation
        update_depot_settings_input_type = type.StructType('operation-input', {
            'depot_settings': type.ReferenceType('vmware.vcf_installer.model_client', 'DepotSettings'),
        })
        update_depot_settings_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        update_depot_settings_input_value_validator_list = [
        ]
        update_depot_settings_output_validator_list = [
        ]
        update_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/v1/system/settings/depot',
            request_body_parameter='depot_settings',
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

        # properties for delete_depot_settings operation
        delete_depot_settings_input_type = type.StructType('operation-input', {
            'depot_type': type.OptionalType(type.StringType()),
        })
        delete_depot_settings_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        delete_depot_settings_input_value_validator_list = [
        ]
        delete_depot_settings_output_validator_list = [
        ]
        delete_depot_settings_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/system/settings/depot',
            path_variables={
            },
            query_parameters={
                'depot_type': 'depotType',
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
            'get_depot_settings': {
                'input_type': get_depot_settings_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'DepotSettings')),
                'errors': get_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_depot_settings_input_value_validator_list,
                'output_validator_list': get_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update_depot_settings': {
                'input_type': update_depot_settings_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'DepotSettings')),
                'errors': update_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': update_depot_settings_input_value_validator_list,
                'output_validator_list': update_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_depot_settings': {
                'input_type': delete_depot_settings_input_type,
                'output_type': type.VoidType(),
                'errors': delete_depot_settings_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500]).build(),
                'input_value_validator_list': delete_depot_settings_input_value_validator_list,
                'output_validator_list': delete_depot_settings_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_depot_settings': get_depot_settings_rest_metadata,
            'update_depot_settings': update_depot_settings_rest_metadata,
            'delete_depot_settings': delete_depot_settings_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.system.settings.depot',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Depot': Depot,
        'depot': 'vmware.vcf_installer.v1.system.settings.depot_client.StubFactory',
    }

