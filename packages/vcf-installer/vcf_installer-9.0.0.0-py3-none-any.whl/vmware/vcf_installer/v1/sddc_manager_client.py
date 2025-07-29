# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.v1.sddc_manager.
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


class TrustedCertificates(VapiInterface):
    """
    
    """

    _VAPI_SERVICE_ID = 'vmware.vcf_installer.v1.sddc_manager.trusted_certificates'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TrustedCertificatesStub)
        self._VAPI_OPERATION_IDS = {}


    def get_trusted_certificates(self):
        """
        Retrieve all trusted certificates from the appliance.


        :rtype: :class:`vmware.vcf_installer.model_client.PageOfTrustedCertificate` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('get_trusted_certificates', None)

    def add_trusted_certificate(self,
                                trusted_certificate_spec,
                                ):
        """
        Add a trusted certificate to the appliance's trust store.

        :type  trusted_certificate_spec: :class:`vmware.vcf_installer.model_client.TrustedCertificateSpec`
        :param trusted_certificate_spec: 
        :rtype: :class:`vmware.vcf_installer.model_client.PageOfTrustedCertificate` or ``None``
        :return: OK
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 400. Bad request
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal server error
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 409. Trusted certificate already exists
        """
        return self._invoke('add_trusted_certificate',
                            {
                            'trusted_certificate_spec': trusted_certificate_spec,
                            })

    def delete_trusted_certificate(self,
                                   alias,
                                   ):
        """
        No Content

        :type  alias: :class:`str`
        :param alias: Certificate Alias
        :raise: :class:`vmware.vcf_installer.model_client.Error` 
            HTTP status code - 500. Internal server error
        """
        return self._invoke('delete_trusted_certificate',
                            {
                            'alias': alias,
                            })
class _TrustedCertificatesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get_trusted_certificates operation
        get_trusted_certificates_input_type = type.StructType('operation-input', {})
        get_trusted_certificates_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        get_trusted_certificates_input_value_validator_list = [
        ]
        get_trusted_certificates_output_validator_list = [
        ]
        get_trusted_certificates_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/v1/sddc-manager/trusted-certificates',
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

        # properties for add_trusted_certificate operation
        add_trusted_certificate_input_type = type.StructType('operation-input', {
            'trusted_certificate_spec': type.ReferenceType('vmware.vcf_installer.model_client', 'TrustedCertificateSpec'),
        })
        add_trusted_certificate_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        add_trusted_certificate_input_value_validator_list = [
        ]
        add_trusted_certificate_output_validator_list = [
        ]
        add_trusted_certificate_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/v1/sddc-manager/trusted-certificates',
            request_body_parameter='trusted_certificate_spec',
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

        # properties for delete_trusted_certificate operation
        delete_trusted_certificate_input_type = type.StructType('operation-input', {
            'alias': type.StringType(),
        })
        delete_trusted_certificate_error_dict = {
            'vmware.vcf_installer.model.error':
                type.ReferenceType('vmware.vcf_installer.model_client', 'Error'),

        }
        delete_trusted_certificate_input_value_validator_list = [
        ]
        delete_trusted_certificate_output_validator_list = [
        ]
        delete_trusted_certificate_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/v1/sddc-manager/trusted-certificates/{alias}',
            path_variables={
                'alias': 'alias',
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
            'get_trusted_certificates': {
                'input_type': get_trusted_certificates_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfTrustedCertificate')),
                'errors': get_trusted_certificates_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': get_trusted_certificates_input_value_validator_list,
                'output_validator_list': get_trusted_certificates_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add_trusted_certificate': {
                'input_type': add_trusted_certificate_input_type,
                'output_type': type.OptionalType(type.ReferenceType('vmware.vcf_installer.model_client', 'PageOfTrustedCertificate')),
                'errors': add_trusted_certificate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [400,500,409]).build(),
                'input_value_validator_list': add_trusted_certificate_input_value_validator_list,
                'output_validator_list': add_trusted_certificate_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete_trusted_certificate': {
                'input_type': delete_trusted_certificate_input_type,
                'output_type': type.VoidType(),
                'errors': delete_trusted_certificate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('vmware.vcf_installer.model_client', 'Error'), [500]).build(),
                'input_value_validator_list': delete_trusted_certificate_input_value_validator_list,
                'output_validator_list': delete_trusted_certificate_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get_trusted_certificates': get_trusted_certificates_rest_metadata,
            'add_trusted_certificate': add_trusted_certificate_rest_metadata,
            'delete_trusted_certificate': delete_trusted_certificate_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='vmware.vcf_installer.v1.sddc_manager.trusted_certificates',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=False)


class StubFactory(StubFactoryBase):
    _attrs = {
        'TrustedCertificates': TrustedCertificates,
    }

