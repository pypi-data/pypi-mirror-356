# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.tokens.
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


class RefreshToken(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.tokens.refresh_token'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RefreshTokenStub)
        self._VAPI_OPERATION_IDS = {}


    def invalidate_refresh_token(self,
                                 invalidate_refresh_token_request_body,
                                 ):
        """
        No content

        :type  invalidate_refresh_token_request_body: :class:`str`
        :param invalidate_refresh_token_request_body: 
        """
        return self._invoke('invalidate_refresh_token',
                            {
                            'invalidate_refresh_token_request_body': invalidate_refresh_token_request_body,
                            })
class _RefreshTokenStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for invalidate_refresh_token operation
        invalidate_refresh_token_input_type = type.StructType('operation-input', {
            'invalidate_refresh_token_request_body': type.StringType(),
        })
        invalidate_refresh_token_error_dict = {}
        invalidate_refresh_token_input_value_validator_list = [
        ]
        invalidate_refresh_token_output_validator_list = [
        ]
        invalidate_refresh_token_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/tokens/refresh-token',
            request_body_parameter='invalidate_refresh_token_request_body',
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
            'invalidate_refresh_token': {
                'input_type': invalidate_refresh_token_input_type,
                'output_type': type.VoidType(),
                'errors': invalidate_refresh_token_error_dict,
                'throws_clause': ThrowsClauseBuilder().build(),
                'input_value_validator_list': invalidate_refresh_token_input_value_validator_list,
                'output_validator_list': invalidate_refresh_token_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'invalidate_refresh_token': invalidate_refresh_token_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.tokens.refresh_token',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'RefreshToken': RefreshToken,
        'access_token': 'vmware.vcf_installer.v1.tokens.access_token_client.StubFactory',
    }

