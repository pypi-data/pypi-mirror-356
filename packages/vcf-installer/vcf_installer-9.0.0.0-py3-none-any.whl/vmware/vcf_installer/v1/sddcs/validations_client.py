# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.sddcs.validations.
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


class Latest(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddcs.validations.latest'
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


    def get_latest_sddc_spec_validation(self):
        """
        


        :rtype: :class:`vmware.vcf_installer.model_client.Validation` or ``None``
        :return: Success
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 404. Not Found
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal Server Error
        """
        return self._invoke('get_latest_sddc_spec_validation', None)
class _LatestStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_latest_sddc_spec_validation operation
        get_latest_sddc_spec_validation_input_type = type.StructType('operation-input', {})
        get_latest_sddc_spec_validation_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_latest_sddc_spec_validation_input_value_validator_list = [
        ]
        get_latest_sddc_spec_validation_output_validator_list = [
        ]
        get_latest_sddc_spec_validation_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddcs/validations/latest',
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
            'get_latest_sddc_spec_validation': {
                'input_type': get_latest_sddc_spec_validation_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'Validation')),
                'errors': get_latest_sddc_spec_validation_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [404,500]).build(),
                'input_value_validator_list': get_latest_sddc_spec_validation_input_value_validator_list,
                'output_validator_list': get_latest_sddc_spec_validation_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_latest_sddc_spec_validation': get_latest_sddc_spec_validation_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddcs.validations.latest',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Latest': Latest,
    }

