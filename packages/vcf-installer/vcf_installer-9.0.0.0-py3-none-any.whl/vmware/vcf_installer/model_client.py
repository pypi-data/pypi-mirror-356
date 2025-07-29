# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package vmware.vcf_installer.model.
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


class DepotAccount(VapiStruct):
    """
    VMware Depot Account Information

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'username': 'username',
                            'password': 'password',
                            'status': 'status',
                            'message': 'message',
                            'downloadToken': 'download_token',
                            }

    def __init__(self,
                 username=None,
                 password=None,
                 status=None,
                 message=None,
                 download_token=None,
                ):
        """
        :type  username: :class:`str` or ``None``
        :param username: Depot Username for Access. This field is optional when
            downloadToken is used for online depot authentication and
            authorization.
        :type  password: :class:`str` or ``None``
        :param password: Depot Password for Access. This field is optional when
            downloadToken is used for online depot authentication and
            authorization.
        :type  status: :class:`str` or ``None``
        :param status: Depot Status
        :type  message: :class:`str` or ``None``
        :param message: Message explaining depot status
        :type  download_token: :class:`str` or ``None``
        :param download_token: This field is mandatory when downloadToken is used for online depot
            authentication and authorization. downloadToken should be generated
            from the broadcom support portal https://support.broadcom.com
        """
        self.username = username
        self.password = password
        self.status = status
        self.message = message
        self.download_token = download_token
        VapiStruct.__init__(self)


DepotAccount._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.depot_account', {
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'message': type.OptionalType(type.StringType()),
        'downloadToken': type.OptionalType(type.StringType()),
    },
    DepotAccount,
    False,
    None))



class DepotConfiguration(VapiStruct):
    """
    Depot Configuration

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'isOfflineDepot': 'is_offline_depot',
                            'hostname': 'hostname',
                            'port': 'port',
                            }

    def __init__(self,
                 is_offline_depot=None,
                 hostname=None,
                 port=None,
                ):
        """
        :type  is_offline_depot: :class:`bool` or ``None``
        :param is_offline_depot: Flag indicating if the depot is in offline mode
        :type  hostname: :class:`str` or ``None``
        :param hostname: IP/Hostname of the depot
        :type  port: :class:`long` or ``None``
        :param port: Port of the depot
        """
        self.is_offline_depot = is_offline_depot
        self.hostname = hostname
        self.port = port
        VapiStruct.__init__(self)


DepotConfiguration._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.depot_configuration', {
        'isOfflineDepot': type.OptionalType(type.BooleanType()),
        'hostname': type.OptionalType(type.StringType()),
        'port': type.OptionalType(type.IntegerType()),
    },
    DepotConfiguration,
    False,
    None))



class DepotSettings(VapiStruct):
    """
    VMware Depot Settings. At least one of vmwareAccount, dellEmcSupportAccount
    or offlineAccount value must be provided

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'vmwareAccount': 'vmware_account',
                            'dellEmcSupportAccount': 'dell_emc_support_account',
                            'offlineAccount': 'offline_account',
                            'depotConfiguration': 'depot_configuration',
                            }

    def __init__(self,
                 vmware_account=None,
                 dell_emc_support_account=None,
                 offline_account=None,
                 depot_configuration=None,
                ):
        """
        :type  vmware_account: :class:`DepotAccount` or ``None``
        :param vmware_account:         :type  dell_emc_support_account: :class:`DepotAccount` or ``None``
        :param dell_emc_support_account:         :type  offline_account: :class:`DepotAccount` or ``None``
        :param offline_account:         :type  depot_configuration: :class:`DepotConfiguration` or ``None``
        :param depot_configuration:         """
        self.vmware_account = vmware_account
        self.dell_emc_support_account = dell_emc_support_account
        self.offline_account = offline_account
        self.depot_configuration = depot_configuration
        VapiStruct.__init__(self)


DepotSettings._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.depot_settings', {
        'vmwareAccount': type.OptionalType(type.ReferenceType(__name__, 'DepotAccount')),
        'dellEmcSupportAccount': type.OptionalType(type.ReferenceType(__name__, 'DepotAccount')),
        'offlineAccount': type.OptionalType(type.ReferenceType(__name__, 'DepotAccount')),
        'depotConfiguration': type.OptionalType(type.ReferenceType(__name__, 'DepotConfiguration')),
    },
    DepotSettings,
    False,
    None))



class ErrorCause(VapiStruct):
    """
    Describes a single error cause

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'type': 'type',
                            'message': 'message',
                            }

    def __init__(self,
                 type=None,
                 message=None,
                ):
        """
        :type  type: :class:`str` or ``None``
        :param type: The type of the error cause 
            
            * Property is read-only.
            
            
        :type  message: :class:`str` or ``None``
        :param message: The message describing the reason for the error 
            
            * Property is read-only.
            
            
        """
        self.type = type
        self.message = message
        VapiStruct.__init__(self)


ErrorCause._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.error_cause', {
        'type': type.OptionalType(type.StringType()),
        'message': type.OptionalType(type.StringType()),
    },
    ErrorCause,
    False,
    None))



class TokenCreationSpec(VapiStruct):
    """
    The spec used to sign the token

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'username': 'username',
                            'password': 'password',
                            'apiKey': 'api_key',
                            'idToken': 'id_token',
                            }

    def __init__(self,
                 username=None,
                 password=None,
                 api_key=None,
                 id_token=None,
                ):
        """
        :type  username: :class:`str` or ``None``
        :param username: Username
        :type  password: :class:`str` or ``None``
        :param password: User Password
        :type  api_key: :class:`str` or ``None``
        :param api_key: API Key
        :type  id_token: :class:`str` or ``None``
        :param id_token: Id Token
        """
        self.username = username
        self.password = password
        self.api_key = api_key
        self.id_token = id_token
        VapiStruct.__init__(self)


TokenCreationSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.token_creation_spec', {
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.StringType()),
        'apiKey': type.OptionalType(type.StringType()),
        'idToken': type.OptionalType(type.StringType()),
    },
    TokenCreationSpec,
    False,
    None))



class RefreshToken(VapiStruct):
    """
    This contains refresh token id for the user API access.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            }

    def __init__(self,
                 id=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Refresh token id that can be used to request new access token
        """
        self.id = id
        VapiStruct.__init__(self)


RefreshToken._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.refresh_token', {
        'id': type.OptionalType(type.StringType()),
    },
    RefreshToken,
    False,
    None))



class TokenPair(VapiStruct):
    """
    This contains the access token and the refresh token for the user API
    access.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'accessToken': 'access_token',
                            'refreshToken': 'refresh_token',
                            }

    def __init__(self,
                 access_token=None,
                 refresh_token=None,
                ):
        """
        :type  access_token: :class:`str` or ``None``
        :param access_token: Bearer token that can be used to make public API calls
        :type  refresh_token: :class:`RefreshToken` or ``None``
        :param refresh_token:         """
        self.access_token = access_token
        self.refresh_token = refresh_token
        VapiStruct.__init__(self)


TokenPair._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.token_pair', {
        'accessToken': type.OptionalType(type.StringType()),
        'refreshToken': type.OptionalType(type.ReferenceType(__name__, 'RefreshToken')),
    },
    TokenPair,
    False,
    None))



class DnsSpec(VapiStruct):
    """
    Spec contains parameters of Domain Name System

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'subdomain': 'subdomain',
                            'nameservers': 'nameservers',
                            }

    def __init__(self,
                 subdomain=None,
                 nameservers=None,
                ):
        """
        :type  subdomain: :class:`str` or ``None``
        :param subdomain: Tenant Sub domain. Includes the full domain suffix
        :type  nameservers: :class:`list` of :class:`str` or ``None``
        :param nameservers: Nameservers to be configured for vCenter/ESXi's/NSX. The first is
            the primary nameserver. Maximum allowed is two entries
        """
        self.subdomain = subdomain
        self.nameservers = nameservers
        VapiStruct.__init__(self)


DnsSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.dns_spec', {
        'subdomain': type.OptionalType(type.StringType()),
        'nameservers': type.OptionalType(type.ListType(type.StringType())),
    },
    DnsSpec,
    False,
    None))



class DvsSpec(VapiStruct):
    """
    Spec contains parameters for DVS

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'dvsName': 'dvs_name',
                            'networks': 'networks',
                            'mtu': 'mtu',
                            'nsxtSwitchConfig': 'nsxt_switch_config',
                            'vmnicsToUplinks': 'vmnics_to_uplinks',
                            'nsxTeamings': 'nsx_teamings',
                            'lagSpecs': 'lag_specs',
                            }

    def __init__(self,
                 dvs_name=None,
                 networks=None,
                 mtu=None,
                 nsxt_switch_config=None,
                 vmnics_to_uplinks=None,
                 nsx_teamings=None,
                 lag_specs=None,
                ):
        """
        :type  dvs_name: :class:`str` or ``None``
        :param dvs_name: vSphere Distributed Switch Name. It will be auto-generated if blank
        :type  networks: :class:`list` of :class:`str` or ``None``
        :param networks: Types of networks in this Distributed vSphere Switch. One among:
            VSAN, VMOTION, MANAGEMENT, VM_MANAGEMENT, NFS or any custom network
            types defined in networkSpecs
        :type  mtu: :class:`long` or ``None``
        :param mtu: Distributed vSphere Switch MTU (default value is 9000)
        :type  nsxt_switch_config: :class:`NsxtSwitchConfig` or ``None``
        :param nsxt_switch_config:         :type  vmnics_to_uplinks: :class:`list` of :class:`VmnicToUplink` or ``None``
        :param vmnics_to_uplinks: List of vmnic to uplink mapping
        :type  nsx_teamings: :class:`list` of :class:`TeamingSpec` or ``None``
        :param nsx_teamings: The teaming policies to be associated with the uplink profile in
            NSX
        :type  lag_specs: :class:`list` of :class:`LagSpec` or ``None``
        :param lag_specs: List of LAGs to be associated with the vSphere Distributed Switch
        """
        self.dvs_name = dvs_name
        self.networks = networks
        self.mtu = mtu
        self.nsxt_switch_config = nsxt_switch_config
        self.vmnics_to_uplinks = vmnics_to_uplinks
        self.nsx_teamings = nsx_teamings
        self.lag_specs = lag_specs
        VapiStruct.__init__(self)


DvsSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.dvs_spec', {
        'dvsName': type.OptionalType(type.StringType()),
        'networks': type.OptionalType(type.ListType(type.StringType())),
        'mtu': type.OptionalType(type.IntegerType()),
        'nsxtSwitchConfig': type.OptionalType(type.ReferenceType(__name__, 'NsxtSwitchConfig')),
        'vmnicsToUplinks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VmnicToUplink'))),
        'nsxTeamings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'TeamingSpec'))),
        'lagSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'LagSpec'))),
    },
    DvsSpec,
    False,
    None))



class FcSpec(VapiStruct):
    """
    Cluster storage configuration for VMFS on FC

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'datastoreName': 'datastore_name',
                            }

    def __init__(self,
                 datastore_name=None,
                ):
        """
        :type  datastore_name: :class:`str` or ``None``
        :param datastore_name: Datastore name used for cluster creation
        """
        self.datastore_name = datastore_name
        VapiStruct.__init__(self)


FcSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.fc_spec', {
        'datastoreName': type.OptionalType(type.StringType()),
    },
    FcSpec,
    False,
    None))



class IpAddressPoolRangeSpec(VapiStruct):
    """
    This specification contains the parameters required to create an IP address
    range

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'start': 'start',
                            'end': 'end',
                            }

    def __init__(self,
                 start=None,
                 end=None,
                ):
        """
        :type  start: :class:`str` or ``None``
        :param start: The first IP Address of the IP Address Range
        :type  end: :class:`str` or ``None``
        :param end: The last IP Address of the IP Address Range
        """
        self.start = start
        self.end = end
        VapiStruct.__init__(self)


IpAddressPoolRangeSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.ip_address_pool_range_spec', {
        'start': type.OptionalType(type.StringType()),
        'end': type.OptionalType(type.StringType()),
    },
    IpAddressPoolRangeSpec,
    False,
    None))



class IpAddressPoolSpec(VapiStruct):
    """
    This specification contains the parameters required to create or reuse an
    IP address pool.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'description': 'description',
                            'ignoreUnavailableNsxtCluster': 'ignore_unavailable_nsxt_cluster',
                            'subnets': 'subnets',
                            }

    def __init__(self,
                 name=None,
                 description=None,
                 ignore_unavailable_nsxt_cluster=None,
                 subnets=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Name of the IP address pool
        :type  description: :class:`str` or ``None``
        :param description: Description of the IP address pool
        :type  ignore_unavailable_nsxt_cluster: :class:`bool` or ``None``
        :param ignore_unavailable_nsxt_cluster: Ignore unavailable NSX cluster(s) during IP pool spec validation
        :type  subnets: :class:`list` of :class:`IpAddressPoolSubnetSpec` or ``None``
        :param subnets: List of IP address pool subnet specification
        """
        self.name = name
        self.description = description
        self.ignore_unavailable_nsxt_cluster = ignore_unavailable_nsxt_cluster
        self.subnets = subnets
        VapiStruct.__init__(self)


IpAddressPoolSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.ip_address_pool_spec', {
        'name': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'ignoreUnavailableNsxtCluster': type.OptionalType(type.BooleanType()),
        'subnets': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'IpAddressPoolSubnetSpec'))),
    },
    IpAddressPoolSpec,
    False,
    None))



class IpAddressPoolSubnetSpec(VapiStruct):
    """
    This specification contains the parameters required to create an IP address
    pool subnet

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'ipAddressPoolRanges': 'ip_address_pool_ranges',
                            'cidr': 'cidr',
                            'gateway': 'gateway',
                            }

    def __init__(self,
                 ip_address_pool_ranges=None,
                 cidr=None,
                 gateway=None,
                ):
        """
        :type  ip_address_pool_ranges: :class:`list` of :class:`IpAddressPoolRangeSpec` or ``None``
        :param ip_address_pool_ranges: List of the IP allocation ranges. Atleast 1 IP address range has to
            be specified
        :type  cidr: :class:`str` or ``None``
        :param cidr: The subnet representation, contains the network address and the
            prefix length
        :type  gateway: :class:`str` or ``None``
        :param gateway: The default gateway address of the network
        """
        self.ip_address_pool_ranges = ip_address_pool_ranges
        self.cidr = cidr
        self.gateway = gateway
        VapiStruct.__init__(self)


IpAddressPoolSubnetSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.ip_address_pool_subnet_spec', {
        'ipAddressPoolRanges': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'IpAddressPoolRangeSpec'))),
        'cidr': type.OptionalType(type.StringType()),
        'gateway': type.OptionalType(type.StringType()),
    },
    IpAddressPoolSubnetSpec,
    False,
    None))



class IpRange(VapiStruct):
    """
    Spec contains parameters for range of IP addresses

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'startIpAddress': 'start_ip_address',
                            'endIpAddress': 'end_ip_address',
                            }

    def __init__(self,
                 start_ip_address=None,
                 end_ip_address=None,
                ):
        """
        :type  start_ip_address: :class:`str` or ``None``
        :param start_ip_address: Start IP Address
        :type  end_ip_address: :class:`str` or ``None``
        :param end_ip_address: End IP Address
        """
        self.start_ip_address = start_ip_address
        self.end_ip_address = end_ip_address
        VapiStruct.__init__(self)


IpRange._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.ip_range', {
        'startIpAddress': type.OptionalType(type.StringType()),
        'endIpAddress': type.OptionalType(type.StringType()),
    },
    IpRange,
    False,
    None))



class LagSpec(VapiStruct):
    """
    This specification contains VDS (vSphere distributed switch) LAG
    configurations

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'uplinksCount': 'uplinks_count',
                            'lacpMode': 'lacp_mode',
                            'loadBalancingMode': 'load_balancing_mode',
                            'lacpTimeoutMode': 'lacp_timeout_mode',
                            }

    def __init__(self,
                 name=None,
                 uplinks_count=None,
                 lacp_mode=None,
                 load_balancing_mode=None,
                 lacp_timeout_mode=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: LAG name
        :type  uplinks_count: :class:`long` or ``None``
        :param uplinks_count: Number of uplinks/ports in this LAG
        :type  lacp_mode: :class:`str` or ``None``
        :param lacp_mode: LACP mode of this LAG
        :type  load_balancing_mode: :class:`str` or ``None``
        :param load_balancing_mode: Load balancing mode of this LAG
        :type  lacp_timeout_mode: :class:`str` or ``None``
        :param lacp_timeout_mode: LACP timeout mode of this LAG
        """
        self.name = name
        self.uplinks_count = uplinks_count
        self.lacp_mode = lacp_mode
        self.load_balancing_mode = load_balancing_mode
        self.lacp_timeout_mode = lacp_timeout_mode
        VapiStruct.__init__(self)


LagSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.lag_spec', {
        'name': type.OptionalType(type.StringType()),
        'uplinksCount': type.OptionalType(type.IntegerType()),
        'lacpMode': type.OptionalType(type.StringType()),
        'loadBalancingMode': type.OptionalType(type.StringType()),
        'lacpTimeoutMode': type.OptionalType(type.StringType()),
    },
    LagSpec,
    False,
    None))



class NasVolumeSpec(VapiStruct):
    """
    NAS configuration for NFS based cluster

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'serverName': 'server_name',
                            'path': 'path',
                            'readOnly': 'read_only',
                            'userTag': 'user_tag',
                            'enableBindToVmknic': 'enable_bind_to_vmknic',
                            }

    def __init__(self,
                 server_name=None,
                 path=None,
                 read_only=None,
                 user_tag=None,
                 enable_bind_to_vmknic=None,
                ):
        """
        :type  server_name: :class:`list` of :class:`str` or ``None``
        :param server_name: NFS Server name used for cluster creation
        :type  path: :class:`str` or ``None``
        :param path: Shared directory path used for NFS based cluster creation
        :type  read_only: :class:`bool` or ``None``
        :param read_only: Readonly is used to identify whether to mount the directory as
            readOnly or not
        :type  user_tag: :class:`str` or ``None``
        :param user_tag: User tag used to annotate NFS share
        :type  enable_bind_to_vmknic: :class:`bool` or ``None``
        :param enable_bind_to_vmknic: Indicates whether to bind the created NFS datastore to the VMkernel
            NIC created based on NFS Network Spec. This is to prevent
            unintentional flow of NFS traffic through any other VMkernel NIC,
            if such connectivity exists.
        """
        self.server_name = server_name
        self.path = path
        self.read_only = read_only
        self.user_tag = user_tag
        self.enable_bind_to_vmknic = enable_bind_to_vmknic
        VapiStruct.__init__(self)


NasVolumeSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.nas_volume_spec', {
        'serverName': type.OptionalType(type.ListType(type.StringType())),
        'path': type.OptionalType(type.StringType()),
        'readOnly': type.OptionalType(type.BooleanType()),
        'userTag': type.OptionalType(type.StringType()),
        'enableBindToVmknic': type.OptionalType(type.BooleanType()),
    },
    NasVolumeSpec,
    False,
    None))



class NfsDatastoreSpec(VapiStruct):
    """
    This specification contains cluster storage configuration for NFS

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'datastoreName': 'datastore_name',
                            'nasVolume': 'nas_volume',
                            }

    def __init__(self,
                 datastore_name=None,
                 nas_volume=None,
                ):
        """
        :type  datastore_name: :class:`str` or ``None``
        :param datastore_name: Datastore name used for cluster creation
        :type  nas_volume: :class:`NasVolumeSpec` or ``None``
        :param nas_volume:         """
        self.datastore_name = datastore_name
        self.nas_volume = nas_volume
        VapiStruct.__init__(self)


NfsDatastoreSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.nfs_datastore_spec', {
        'datastoreName': type.OptionalType(type.StringType()),
        'nasVolume': type.OptionalType(type.ReferenceType(__name__, 'NasVolumeSpec')),
    },
    NfsDatastoreSpec,
    False,
    None))



class NsxtManagerSpec(VapiStruct):
    """
    Spec contains parameters for NSX manager

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            }

    def __init__(self,
                 hostname=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: NSX Manager hostname
        """
        self.hostname = hostname
        VapiStruct.__init__(self)


NsxtManagerSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.nsxt_manager_spec', {
        'hostname': type.OptionalType(type.StringType()),
    },
    NsxtManagerSpec,
    False,
    None))



class NsxtSwitchConfig(VapiStruct):
    """
    This specification contains the configurations to be associated with the
    vSphere Distributed Switch managed by NSX

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'transportZones': 'transport_zones',
                            'hostSwitchOperationalMode': 'host_switch_operational_mode',
                            'ipAssignmentType': 'ip_assignment_type',
                            }

    def __init__(self,
                 transport_zones=None,
                 host_switch_operational_mode=None,
                 ip_assignment_type=None,
                ):
        """
        :type  transport_zones: :class:`list` of :class:`TransportZone` or ``None``
        :param transport_zones: The list of transport zones to be associated with the vSphere
            Distributed Switch managed by NSX
        :type  host_switch_operational_mode: :class:`str` or ``None``
        :param host_switch_operational_mode: Operational mode type of a Host Switch. Applicable only for the VI
            Workload Domains.
        :type  ip_assignment_type: :class:`str` or ``None``
        :param ip_assignment_type: Ip Assignment Type of a Host Switch
        """
        self.transport_zones = transport_zones
        self.host_switch_operational_mode = host_switch_operational_mode
        self.ip_assignment_type = ip_assignment_type
        VapiStruct.__init__(self)


NsxtSwitchConfig._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.nsxt_switch_config', {
        'transportZones': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'TransportZone'))),
        'hostSwitchOperationalMode': type.OptionalType(type.StringType()),
        'ipAssignmentType': type.OptionalType(type.StringType()),
    },
    NsxtSwitchConfig,
    False,
    None))



class ResourcePoolSpec(VapiStruct):
    """
    Spec contains parameters for Resource Pool

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    TYPE_MANAGEMENT = "management"
    """
    Type of resource pool. One among: management, compute, network

    """
    TYPE_COMPUTE = "compute"
    """
    Type of resource pool. One among: management, compute, network

    """
    TYPE_NETWORK = "network"
    """
    Type of resource pool. One among: management, compute, network

    """
    CPU_SHARES_LEVEL_CUSTOM_HIGH_LOW_NORMAL = "custom,high,low,normal"
    """
    CPU shares level, default 'normal'

    """
    MEMORY_SHARES_LEVEL_CUSTOM_HIGH_LOW_NORMAL = "custom,high,low,normal"
    """
    Memory shares level. default 'normal'

    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'type': 'type',
                            'cpuReservationPercentage': 'cpu_reservation_percentage',
                            'cpuReservationMhz': 'cpu_reservation_mhz',
                            'cpuLimit': 'cpu_limit',
                            'cpuReservationExpandable': 'cpu_reservation_expandable',
                            'cpuSharesLevel': 'cpu_shares_level',
                            'cpuSharesValue': 'cpu_shares_value',
                            'memoryReservationPercentage': 'memory_reservation_percentage',
                            'memoryReservationMb': 'memory_reservation_mb',
                            'memoryLimit': 'memory_limit',
                            'memoryReservationExpandable': 'memory_reservation_expandable',
                            'memorySharesLevel': 'memory_shares_level',
                            'memorySharesValue': 'memory_shares_value',
                            }

    def __init__(self,
                 name=None,
                 type=None,
                 cpu_reservation_percentage=None,
                 cpu_reservation_mhz=None,
                 cpu_limit=None,
                 cpu_reservation_expandable=None,
                 cpu_shares_level=None,
                 cpu_shares_value=None,
                 memory_reservation_percentage=None,
                 memory_reservation_mb=None,
                 memory_limit=None,
                 memory_reservation_expandable=None,
                 memory_shares_level=None,
                 memory_shares_value=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Resource Pool name. It will be auto-generated if blank
        :type  type: :class:`str` or ``None``
        :param type: Type of resource pool. One among: management, compute, network
        :type  cpu_reservation_percentage: :class:`long` or ``None``
        :param cpu_reservation_percentage: CPU reservation percentage, from 0 to 100, default 0
        :type  cpu_reservation_mhz: :class:`long` or ``None``
        :param cpu_reservation_mhz: CPU reservation in Mhz, default 0
        :type  cpu_limit: :class:`long` or ``None``
        :param cpu_limit: CPU limit, default -1 (unlimited)
        :type  cpu_reservation_expandable: :class:`bool` or ``None``
        :param cpu_reservation_expandable: Is CPU reservation expandable, default true
        :type  cpu_shares_level: :class:`str` or ``None``
        :param cpu_shares_level: CPU shares level, default 'normal'
        :type  cpu_shares_value: :class:`long` or ``None``
        :param cpu_shares_value: CPU shares value, only relevant when shares level is 'custom',
            default 0
        :type  memory_reservation_percentage: :class:`long` or ``None``
        :param memory_reservation_percentage: Memory reservation percentage, from 0 to 100, default 0
        :type  memory_reservation_mb: :class:`long` or ``None``
        :param memory_reservation_mb: Memory reservation in MB, default 0
        :type  memory_limit: :class:`long` or ``None``
        :param memory_limit: Memory limit, default -1 (unlimited)
        :type  memory_reservation_expandable: :class:`bool` or ``None``
        :param memory_reservation_expandable: Is Memory reservation expandable, default true
        :type  memory_shares_level: :class:`str` or ``None``
        :param memory_shares_level: Memory shares level. default 'normal'
        :type  memory_shares_value: :class:`long` or ``None``
        :param memory_shares_value: Memory shares value, only relevant when shares level is 'custom',
            default 0
        """
        self.name = name
        self.type = type
        self.cpu_reservation_percentage = cpu_reservation_percentage
        self.cpu_reservation_mhz = cpu_reservation_mhz
        self.cpu_limit = cpu_limit
        self.cpu_reservation_expandable = cpu_reservation_expandable
        self.cpu_shares_level = cpu_shares_level
        self.cpu_shares_value = cpu_shares_value
        self.memory_reservation_percentage = memory_reservation_percentage
        self.memory_reservation_mb = memory_reservation_mb
        self.memory_limit = memory_limit
        self.memory_reservation_expandable = memory_reservation_expandable
        self.memory_shares_level = memory_shares_level
        self.memory_shares_value = memory_shares_value
        VapiStruct.__init__(self)


ResourcePoolSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.resource_pool_spec', {
        'name': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'cpuReservationPercentage': type.OptionalType(type.IntegerType()),
        'cpuReservationMhz': type.OptionalType(type.IntegerType()),
        'cpuLimit': type.OptionalType(type.IntegerType()),
        'cpuReservationExpandable': type.OptionalType(type.BooleanType()),
        'cpuSharesLevel': type.OptionalType(type.StringType()),
        'cpuSharesValue': type.OptionalType(type.IntegerType()),
        'memoryReservationPercentage': type.OptionalType(type.IntegerType()),
        'memoryReservationMb': type.OptionalType(type.IntegerType()),
        'memoryLimit': type.OptionalType(type.IntegerType()),
        'memoryReservationExpandable': type.OptionalType(type.BooleanType()),
        'memorySharesLevel': type.OptionalType(type.StringType()),
        'memorySharesValue': type.OptionalType(type.IntegerType()),
    },
    ResourcePoolSpec,
    False,
    None))



class RootCaCerts(VapiStruct):
    """
    Spec contains Root Certificate Authority parameters

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'alias': 'alias',
                            'certChain': 'cert_chain',
                            }

    def __init__(self,
                 alias=None,
                 cert_chain=None,
                ):
        """
        :type  alias: :class:`str` or ``None``
        :param alias: Certificate alias
        :type  cert_chain: :class:`list` of :class:`str` or ``None``
        :param cert_chain: List of Base64 encoded certificates
        """
        self.alias = alias
        self.cert_chain = cert_chain
        VapiStruct.__init__(self)


RootCaCerts._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.root_ca_certs', {
        'alias': type.OptionalType(type.StringType()),
        'certChain': type.OptionalType(type.ListType(type.StringType())),
    },
    RootCaCerts,
    False,
    None))



class SddcClusterSpec(VapiStruct):
    """
    Spec contains parameters for vCenter Cluster

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'datacenterName': 'datacenter_name',
                            'clusterName': 'cluster_name',
                            'clusterEvcMode': 'cluster_evc_mode',
                            'resourcePoolSpecs': 'resource_pool_specs',
                            }

    def __init__(self,
                 datacenter_name=None,
                 cluster_name=None,
                 cluster_evc_mode=None,
                 resource_pool_specs=None,
                ):
        """
        :type  datacenter_name: :class:`str` or ``None``
        :param datacenter_name: vCenter Datacenter Name. It will be auto-generated if blank.
        :type  cluster_name: :class:`str` or ``None``
        :param cluster_name: vCenter Cluster Name. It will be auto-generated if blank.
        :type  cluster_evc_mode: :class:`str` or ``None``
        :param cluster_evc_mode: EVC mode for vSphere cluster, if needed
        :type  resource_pool_specs: :class:`list` of :class:`ResourcePoolSpec` or ``None``
        :param resource_pool_specs: List of Resource Pool Specification. If blank, no resource pools
            will be created. However, if you want to create resource pool,
            Management Resource Pool is required to be present in the list.
        """
        self.datacenter_name = datacenter_name
        self.cluster_name = cluster_name
        self.cluster_evc_mode = cluster_evc_mode
        self.resource_pool_specs = resource_pool_specs
        VapiStruct.__init__(self)


SddcClusterSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_cluster_spec', {
        'datacenterName': type.OptionalType(type.StringType()),
        'clusterName': type.OptionalType(type.StringType()),
        'clusterEvcMode': type.OptionalType(type.StringType()),
        'resourcePoolSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ResourcePoolSpec'))),
    },
    SddcClusterSpec,
    False,
    None))



class SddcCredentials(VapiStruct):
    """
    Credentials contains the username and password

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'username': 'username',
                            'password': 'password',
                            }

    def __init__(self,
                 username=None,
                 password=None,
                ):
        """
        :type  username: :class:`str` or ``None``
        :param username: Username
        :type  password: :class:`str` or ``None``
        :param password: Password
        """
        self.username = username
        self.password = password
        VapiStruct.__init__(self)


SddcCredentials._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_credentials', {
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.StringType()),
    },
    SddcCredentials,
    False,
    None))



class SddcDatastoreSpec(VapiStruct):
    """
    This specification contains cluster storage configuration

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'nfsDatastoreSpec': 'nfs_datastore_spec',
                            'vmfsDatastoreSpec': 'vmfs_datastore_spec',
                            'vsanSpec': 'vsan_spec',
                            'existingDatastoreName': 'existing_datastore_name',
                            }

    def __init__(self,
                 nfs_datastore_spec=None,
                 vmfs_datastore_spec=None,
                 vsan_spec=None,
                 existing_datastore_name=None,
                ):
        """
        :type  nfs_datastore_spec: :class:`NfsDatastoreSpec` or ``None``
        :param nfs_datastore_spec:         :type  vmfs_datastore_spec: :class:`VmfsDatastoreSpec` or ``None``
        :param vmfs_datastore_spec:         :type  vsan_spec: :class:`VsanSpec` or ``None``
        :param vsan_spec:         :type  existing_datastore_name: :class:`str` or ``None``
        :param existing_datastore_name: Name of an existing datastore that is to be used when converting an
            existing environment.
        """
        self.nfs_datastore_spec = nfs_datastore_spec
        self.vmfs_datastore_spec = vmfs_datastore_spec
        self.vsan_spec = vsan_spec
        self.existing_datastore_name = existing_datastore_name
        VapiStruct.__init__(self)


SddcDatastoreSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_datastore_spec', {
        'nfsDatastoreSpec': type.OptionalType(type.ReferenceType(__name__, 'NfsDatastoreSpec')),
        'vmfsDatastoreSpec': type.OptionalType(type.ReferenceType(__name__, 'VmfsDatastoreSpec')),
        'vsanSpec': type.OptionalType(type.ReferenceType(__name__, 'VsanSpec')),
        'existingDatastoreName': type.OptionalType(type.StringType()),
    },
    SddcDatastoreSpec,
    False,
    None))



class SddcHostSpec(VapiStruct):
    """
    Spec contains parameters for Host

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            'credentials': 'credentials',
                            'sshThumbprint': 'ssh_thumbprint',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 hostname=None,
                 credentials=None,
                 ssh_thumbprint=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: ESX hostname. This value will be prefixed to the DNS subdomain name
            and should not include the domain name itself. Must also adhere to
            RFC 1123 naming conventions
        :type  credentials: :class:`SddcCredentials` or ``None``
        :param credentials:         :type  ssh_thumbprint: :class:`str` or ``None``
        :param ssh_thumbprint: ESX host SSH thumbprint (RSA SHA256) in new deployment scenario or
            ESX host SSH key (RSA, ECDSA) in reuse existing deployment scenario
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: ESX host SSL thumbprint (SHA256)
        """
        self.hostname = hostname
        self.credentials = credentials
        self.ssh_thumbprint = ssh_thumbprint
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


SddcHostSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_host_spec', {
        'hostname': type.OptionalType(type.StringType()),
        'credentials': type.OptionalType(type.ReferenceType(__name__, 'SddcCredentials')),
        'sshThumbprint': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    SddcHostSpec,
    False,
    None))



class SddcManagerSpec(VapiStruct):
    """
    Client input parameters for SDDC Manager Virtual Machine

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'rootPassword': 'root_password',
                            'hostname': 'hostname',
                            'sshPassword': 'ssh_password',
                            'localUserPassword': 'local_user_password',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 root_password=None,
                 hostname=None,
                 ssh_password=None,
                 local_user_password=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  root_password: :class:`str` or ``None``
        :param root_password: Password for the 'root' user on SDDC Manager appliance. It needs to
            be a strong password with at least one alphabet and one special
            character and at least 8 characters in length. If blank, the SDDC
            Local Admin Password will be used (if provided) or password will be
            auto-generated.
        :type  hostname: :class:`str` or ``None``
        :param hostname: SDDC Manager Hostname.
        :type  ssh_password: :class:`str` or ``None``
        :param ssh_password: Password for the 'vcf' user on SDDC Manager appliance. It needs to
            be a strong password with at least one alphabet and one special
            character and at least 8 characters in length. If blank, the SDDC
            Local Admin Password will be used (if provided) or password will be
            auto-generated.
        :type  local_user_password: :class:`str` or ``None``
        :param local_user_password: The local account is a built-in admin account in VCF that can be
            used in emergency scenarios. The password of this account must be
            at least 12 characters long. It also must contain at-least 1
            uppercase, 1 lowercase, 1 special character specified in braces
            [!%\\\\@$^#?] and 1 digit. In addition, a character cannot be
            repeated more than 3 times consecutively. If blank, the password
            will be auto-generated.
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.root_password = root_password
        self.hostname = hostname
        self.ssh_password = ssh_password
        self.local_user_password = local_user_password
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


SddcManagerSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_manager_spec', {
        'rootPassword': type.OptionalType(type.StringType()),
        'hostname': type.OptionalType(type.StringType()),
        'sshPassword': type.OptionalType(type.StringType()),
        'localUserPassword': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    SddcManagerSpec,
    False,
    None))



class SddcNetworkSpec(VapiStruct):
    """
    Defines a network spec

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'networkType': 'network_type',
                            'subnet': 'subnet',
                            'gateway': 'gateway',
                            'subnetMask': 'subnet_mask',
                            'includeIpAddress': 'include_ip_address',
                            'includeIpAddressRanges': 'include_ip_address_ranges',
                            'vlanId': 'vlan_id',
                            'mtu': 'mtu',
                            'teamingPolicy': 'teaming_policy',
                            'activeUplinks': 'active_uplinks',
                            'standbyUplinks': 'standby_uplinks',
                            'portGroupKey': 'port_group_key',
                            }

    def __init__(self,
                 network_type=None,
                 subnet=None,
                 gateway=None,
                 subnet_mask=None,
                 include_ip_address=None,
                 include_ip_address_ranges=None,
                 vlan_id=None,
                 mtu=None,
                 teaming_policy=None,
                 active_uplinks=None,
                 standby_uplinks=None,
                 port_group_key=None,
                ):
        """
        :type  network_type: :class:`str` or ``None``
        :param network_type: Network Type. One among: VSAN, VMOTION, MANAGEMENT, VM_MANAGEMENT,
            NFS or any custom network type
        :type  subnet: :class:`str` or ``None``
        :param subnet: Subnet
        :type  gateway: :class:`str` or ``None``
        :param gateway: Gateway
        :type  subnet_mask: :class:`str` or ``None``
        :param subnet_mask: Subnet Mask
        :type  include_ip_address: :class:`list` of :class:`str` or ``None``
        :param include_ip_address: IP Addresses to be included
        :type  include_ip_address_ranges: :class:`list` of :class:`IpRange` or ``None``
        :param include_ip_address_ranges: IP Address ranges to be included
        :type  vlan_id: :class:`long` or ``None``
        :param vlan_id: VLAN ID
        :type  mtu: :class:`long` or ``None``
        :param mtu: MTU size
        :type  teaming_policy: :class:`str` or ``None``
        :param teaming_policy: Teaming Policy for VSAN and VMOTION network types, Default is
            loadbalance_loadbased. One among:loadbalance_ip,
            loadbalance_srcmac, loadbalance_srcid, failover_explicit,
            loadbalance_loadbased
        :type  active_uplinks: :class:`list` of :class:`str` or ``None``
        :param active_uplinks: Active Uplinks for teaming policy, specify uplink1 for
            failover_explicit VSAN Teaming Policy
        :type  standby_uplinks: :class:`list` of :class:`str` or ``None``
        :param standby_uplinks: Standby Uplinks for teaming policy, specify uplink2 for
            failover_explicit VSAN Teaming Policy
        :type  port_group_key: :class:`str` or ``None``
        :param port_group_key: Name of the Distributed Portgroup to be created. It will be
            autogenerated if null
        """
        self.network_type = network_type
        self.subnet = subnet
        self.gateway = gateway
        self.subnet_mask = subnet_mask
        self.include_ip_address = include_ip_address
        self.include_ip_address_ranges = include_ip_address_ranges
        self.vlan_id = vlan_id
        self.mtu = mtu
        self.teaming_policy = teaming_policy
        self.active_uplinks = active_uplinks
        self.standby_uplinks = standby_uplinks
        self.port_group_key = port_group_key
        VapiStruct.__init__(self)


SddcNetworkSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_network_spec', {
        'networkType': type.OptionalType(type.StringType()),
        'subnet': type.OptionalType(type.StringType()),
        'gateway': type.OptionalType(type.StringType()),
        'subnetMask': type.OptionalType(type.StringType()),
        'includeIpAddress': type.OptionalType(type.ListType(type.StringType())),
        'includeIpAddressRanges': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'IpRange'))),
        'vlanId': type.OptionalType(type.IntegerType()),
        'mtu': type.OptionalType(type.IntegerType()),
        'teamingPolicy': type.OptionalType(type.StringType()),
        'activeUplinks': type.OptionalType(type.ListType(type.StringType())),
        'standbyUplinks': type.OptionalType(type.ListType(type.StringType())),
        'portGroupKey': type.OptionalType(type.StringType()),
    },
    SddcNetworkSpec,
    False,
    None))



class SddcNsxtSpec(VapiStruct):
    """
    Spec contains parameters for NSX deployment and configurations

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'nsxtManagers': 'nsxt_managers',
                            'nsxtManagerSize': 'nsxt_manager_size',
                            'vipFqdn': 'vip_fqdn',
                            'rootNsxtManagerPassword': 'root_nsxt_manager_password',
                            'nsxtAdminPassword': 'nsxt_admin_password',
                            'nsxtAuditPassword': 'nsxt_audit_password',
                            'transportVlanId': 'transport_vlan_id',
                            'ipAddressPoolSpec': 'ip_address_pool_spec',
                            'skipNsxOverlayOverManagementNetwork': 'skip_nsx_overlay_over_management_network',
                            'enableEdgeClusterSync': 'enable_edge_cluster_sync',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 nsxt_managers=None,
                 nsxt_manager_size=None,
                 vip_fqdn=None,
                 root_nsxt_manager_password=None,
                 nsxt_admin_password=None,
                 nsxt_audit_password=None,
                 transport_vlan_id=None,
                 ip_address_pool_spec=None,
                 skip_nsx_overlay_over_management_network=None,
                 enable_edge_cluster_sync=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  nsxt_managers: :class:`list` of :class:`NsxtManagerSpec` or ``None``
        :param nsxt_managers: NSX Managers
        :type  nsxt_manager_size: :class:`str` or ``None``
        :param nsxt_manager_size: NSX Manager size. One among: medium, large,xlarge. Default value if
            not provided is medium
        :type  vip_fqdn: :class:`str` or ``None``
        :param vip_fqdn: Hostname for VIP so that common SSL certificates can be installed
            across all managers.
        :type  root_nsxt_manager_password: :class:`str` or ``None``
        :param root_nsxt_manager_password: NSX root password. The password must be at least 12 characters
            long. Must contain at-least 1 uppercase, 1 lowercase, 1 special
            character and 1 digit. In addition, a character cannot be repeated
            3 or more times consectively. If blank, the SDDC Local Admin
            Password will be used (if provided) or password will be
            auto-generated.
        :type  nsxt_admin_password: :class:`str` or ``None``
        :param nsxt_admin_password: NSX admin password. The password must be at least 12 characters
            long. Must contain at-least 1 uppercase, 1 lowercase, 1 special
            character and 1 digit. In addition, a character cannot be repeated
            3 or more times consectively. If blank, the SDDC Local Admin
            Password will be used (if provided) or password will be
            auto-generated.
        :type  nsxt_audit_password: :class:`str` or ``None``
        :param nsxt_audit_password: NSX audit password. The password must be at least 12 characters
            long. Must contain at-least 1 uppercase, 1 lowercase, 1 special
            character and 1 digit. In addition, a character cannot be repeated
            3 or more times consectively. If blank, the SDDC Local Admin
            Password will be used (if provided) or password will be
            auto-generated.
        :type  transport_vlan_id: :class:`long` or ``None``
        :param transport_vlan_id: Transport VLAN ID. Default '0' if not specified
        :type  ip_address_pool_spec: :class:`IpAddressPoolSpec` or ``None``
        :param ip_address_pool_spec:         :type  skip_nsx_overlay_over_management_network: :class:`bool` or ``None``
        :param skip_nsx_overlay_over_management_network: Flag that indicates if the Overlay over Management Network
            configuration will be skipped. Applicable only when vCenter is
            existing and being converted.
        :type  enable_edge_cluster_sync: :class:`bool` or ``None``
        :param enable_edge_cluster_sync: Enable NSX Edge Cluster synchronization. Applicable only when NSX
            exists and is being imported. If enabled and your NSX deployment
            has one or more Edge clusters, the import process will add the
            discovered Edge node VMs to the VCF inventory, including their user
            credentials. As part of this process, a one-time reset of the Edge
            node credential passwords will be done. The updated passwords may
            be retrieved from the VCF credential store if desired. Once an Edge
            cluster's node VMs have been imported, any node VMs added to that
            Edge cluster will also be imported and subject to the same one-time
            password reset.
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.nsxt_managers = nsxt_managers
        self.nsxt_manager_size = nsxt_manager_size
        self.vip_fqdn = vip_fqdn
        self.root_nsxt_manager_password = root_nsxt_manager_password
        self.nsxt_admin_password = nsxt_admin_password
        self.nsxt_audit_password = nsxt_audit_password
        self.transport_vlan_id = transport_vlan_id
        self.ip_address_pool_spec = ip_address_pool_spec
        self.skip_nsx_overlay_over_management_network = skip_nsx_overlay_over_management_network
        self.enable_edge_cluster_sync = enable_edge_cluster_sync
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


SddcNsxtSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_nsxt_spec', {
        'nsxtManagers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'NsxtManagerSpec'))),
        'nsxtManagerSize': type.OptionalType(type.StringType()),
        'vipFqdn': type.OptionalType(type.StringType()),
        'rootNsxtManagerPassword': type.OptionalType(type.StringType()),
        'nsxtAdminPassword': type.OptionalType(type.StringType()),
        'nsxtAuditPassword': type.OptionalType(type.StringType()),
        'transportVlanId': type.OptionalType(type.IntegerType()),
        'ipAddressPoolSpec': type.OptionalType(type.ReferenceType(__name__, 'IpAddressPoolSpec')),
        'skipNsxOverlayOverManagementNetwork': type.OptionalType(type.BooleanType()),
        'enableEdgeClusterSync': type.OptionalType(type.BooleanType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    SddcNsxtSpec,
    False,
    None))



class SddcSpec(VapiStruct):
    """
    VCF Installer specification

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'sddcId': 'sddc_id',
                            'workflowType': 'workflow_type',
                            'hostSpecs': 'host_specs',
                            'version': 'version',
                            'vcenterSpec': 'vcenter_spec',
                            'clusterSpec': 'cluster_spec',
                            'dvsSpecs': 'dvs_specs',
                            'nsxtSpec': 'nsxt_spec',
                            'networkSpecs': 'network_specs',
                            'dnsSpec': 'dns_spec',
                            'ntpServers': 'ntp_servers',
                            'sddcManagerSpec': 'sddc_manager_spec',
                            'managementPoolName': 'management_pool_name',
                            'ceipEnabled': 'ceip_enabled',
                            'skipEsxThumbprintValidation': 'skip_esx_thumbprint_validation',
                            'skipGatewayPingValidation': 'skip_gateway_ping_validation',
                            'securitySpec': 'security_spec',
                            'datastoreSpec': 'datastore_spec',
                            'vcfOperationsFleetManagementSpec': 'vcf_operations_fleet_management_spec',
                            'vcfOperationsSpec': 'vcf_operations_spec',
                            'vcfOperationsCollectorSpec': 'vcf_operations_collector_spec',
                            'vcfAutomationSpec': 'vcf_automation_spec',
                            'vcfInstanceName': 'vcf_instance_name',
                            }

    def __init__(self,
                 sddc_id=None,
                 workflow_type=None,
                 host_specs=None,
                 version=None,
                 vcenter_spec=None,
                 cluster_spec=None,
                 dvs_specs=None,
                 nsxt_spec=None,
                 network_specs=None,
                 dns_spec=None,
                 ntp_servers=None,
                 sddc_manager_spec=None,
                 management_pool_name=None,
                 ceip_enabled=None,
                 skip_esx_thumbprint_validation=None,
                 skip_gateway_ping_validation=None,
                 security_spec=None,
                 datastore_spec=None,
                 vcf_operations_fleet_management_spec=None,
                 vcf_operations_spec=None,
                 vcf_operations_collector_spec=None,
                 vcf_automation_spec=None,
                 vcf_instance_name=None,
                ):
        """
        :type  sddc_id: :class:`str` or ``None``
        :param sddc_id: Client string that identifies an SDDC by name or instance name.
            Used for management domain name. Can contain only letters, numbers
            and the following symbols: '-'. Minimum length 3, maximum length
            20.
        :type  workflow_type: :class:`str` or ``None``
        :param workflow_type: Type of workflow to initiate creation and/or validation of SDDC
        :type  host_specs: :class:`list` of :class:`SddcHostSpec` or ``None``
        :param host_specs: List of ESXi to be added to the Management Cluster
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  vcenter_spec: :class:`SddcVcenterSpec` or ``None``
        :param vcenter_spec:         :type  cluster_spec: :class:`SddcClusterSpec` or ``None``
        :param cluster_spec:         :type  dvs_specs: :class:`list` of :class:`DvsSpec` or ``None``
        :param dvs_specs: List of vSphere Distributed Switches to be created. For VCF only:
            if blank, a default single one will be created for all types of
            traffic connected to vmnic0 and vmnic1
        :type  nsxt_spec: :class:`SddcNsxtSpec` or ``None``
        :param nsxt_spec:         :type  network_specs: :class:`list` of :class:`SddcNetworkSpec` or ``None``
        :param network_specs: List of Networks which be created and used for Management Cluster
        :type  dns_spec: :class:`DnsSpec` or ``None``
        :param dns_spec:         :type  ntp_servers: :class:`list` of :class:`str` or ``None``
        :param ntp_servers: List of NTP servers to be used for configuring Management
            Appliances
        :type  sddc_manager_spec: :class:`SddcManagerSpec` or ``None``
        :param sddc_manager_spec:         :type  management_pool_name: :class:`str` or ``None``
        :param management_pool_name: Name for the network pool to be created and associated with the
            Management Cluster
        :type  ceip_enabled: :class:`bool` or ``None``
        :param ceip_enabled: Enable VCF Customer Experience Improvement Program
        :type  skip_esx_thumbprint_validation: :class:`bool` or ``None``
        :param skip_esx_thumbprint_validation: Skip ESXi thumbprint validation. Applies to both converting an
            existing environment and deploying a new one
        :type  skip_gateway_ping_validation: :class:`bool` or ``None``
        :param skip_gateway_ping_validation: Skip networks gateway connectivity validation
        :type  security_spec: :class:`SecuritySpec` or ``None``
        :param security_spec:         :type  datastore_spec: :class:`SddcDatastoreSpec` or ``None``
        :param datastore_spec:         :type  vcf_operations_fleet_management_spec: :class:`VcfOperationsFleetManagementSpec` or ``None``
        :param vcf_operations_fleet_management_spec:         :type  vcf_operations_spec: :class:`VcfOperationsSpec` or ``None``
        :param vcf_operations_spec:         :type  vcf_operations_collector_spec: :class:`VcfOperationsCollectorSpec` or ``None``
        :param vcf_operations_collector_spec:         :type  vcf_automation_spec: :class:`VcfAutomationSpec` or ``None``
        :param vcf_automation_spec:         :type  vcf_instance_name: :class:`str` or ``None``
        :param vcf_instance_name: VCF Instance name. Minumum length 3, maximum length 300
        """
        self.sddc_id = sddc_id
        self.workflow_type = workflow_type
        self.host_specs = host_specs
        self.version = version
        self.vcenter_spec = vcenter_spec
        self.cluster_spec = cluster_spec
        self.dvs_specs = dvs_specs
        self.nsxt_spec = nsxt_spec
        self.network_specs = network_specs
        self.dns_spec = dns_spec
        self.ntp_servers = ntp_servers
        self.sddc_manager_spec = sddc_manager_spec
        self.management_pool_name = management_pool_name
        self.ceip_enabled = ceip_enabled
        self.skip_esx_thumbprint_validation = skip_esx_thumbprint_validation
        self.skip_gateway_ping_validation = skip_gateway_ping_validation
        self.security_spec = security_spec
        self.datastore_spec = datastore_spec
        self.vcf_operations_fleet_management_spec = vcf_operations_fleet_management_spec
        self.vcf_operations_spec = vcf_operations_spec
        self.vcf_operations_collector_spec = vcf_operations_collector_spec
        self.vcf_automation_spec = vcf_automation_spec
        self.vcf_instance_name = vcf_instance_name
        VapiStruct.__init__(self)


SddcSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_spec', {
        'sddcId': type.OptionalType(type.StringType()),
        'workflowType': type.OptionalType(type.StringType()),
        'hostSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcHostSpec'))),
        'version': type.OptionalType(type.StringType()),
        'vcenterSpec': type.OptionalType(type.ReferenceType(__name__, 'SddcVcenterSpec')),
        'clusterSpec': type.OptionalType(type.ReferenceType(__name__, 'SddcClusterSpec')),
        'dvsSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'DvsSpec'))),
        'nsxtSpec': type.OptionalType(type.ReferenceType(__name__, 'SddcNsxtSpec')),
        'networkSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcNetworkSpec'))),
        'dnsSpec': type.OptionalType(type.ReferenceType(__name__, 'DnsSpec')),
        'ntpServers': type.OptionalType(type.ListType(type.StringType())),
        'sddcManagerSpec': type.OptionalType(type.ReferenceType(__name__, 'SddcManagerSpec')),
        'managementPoolName': type.OptionalType(type.StringType()),
        'ceipEnabled': type.OptionalType(type.BooleanType()),
        'skipEsxThumbprintValidation': type.OptionalType(type.BooleanType()),
        'skipGatewayPingValidation': type.OptionalType(type.BooleanType()),
        'securitySpec': type.OptionalType(type.ReferenceType(__name__, 'SecuritySpec')),
        'datastoreSpec': type.OptionalType(type.ReferenceType(__name__, 'SddcDatastoreSpec')),
        'vcfOperationsFleetManagementSpec': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsFleetManagementSpec')),
        'vcfOperationsSpec': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsSpec')),
        'vcfOperationsCollectorSpec': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsCollectorSpec')),
        'vcfAutomationSpec': type.OptionalType(type.ReferenceType(__name__, 'VcfAutomationSpec')),
        'vcfInstanceName': type.OptionalType(type.StringType()),
    },
    SddcSpec,
    False,
    None))



class SddcVcenterSpec(VapiStruct):
    """
    Spec contains parameters for vCenter

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'vcenterHostname': 'vcenter_hostname',
                            'rootVcenterPassword': 'root_vcenter_password',
                            'vmSize': 'vm_size',
                            'storageSize': 'storage_size',
                            'ssoDomain': 'sso_domain',
                            'adminUserSsoUsername': 'admin_user_sso_username',
                            'adminUserSsoPassword': 'admin_user_sso_password',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 vcenter_hostname=None,
                 root_vcenter_password=None,
                 vm_size=None,
                 storage_size=None,
                 sso_domain=None,
                 admin_user_sso_username=None,
                 admin_user_sso_password=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  vcenter_hostname: :class:`str` or ``None``
        :param vcenter_hostname: vCenter hostname address.
        :type  root_vcenter_password: :class:`str` or ``None``
        :param root_vcenter_password: vCenter root password. The password must be between 15 characters
            and 20 characters long. It must also contain at least one uppercase
            and lowercase letter, one number, and one character from '! " # $ %
            & ' ( ) \* + , - . / : ; < = > ? \\\\@ [ \ ] ^ _ \\\\` { Ι } ~' and
            all characters must be ASCII. Space is not allowed in password. For
            VCF only: if blank, the SDDC Local Admin Password will be used (if
            provided) or password will be auto-generated.
        :type  vm_size: :class:`str` or ``None``
        :param vm_size: vCenter Virtual Machine size. One among:xlarge, large, medium,
            small, tiny
        :type  storage_size: :class:`str` or ``None``
        :param storage_size: vCenter Virtual Machine Storage size. One among:lstorage, xlstorage
        :type  sso_domain: :class:`str` or ``None``
        :param sso_domain: PSC SSO Domain
        :type  admin_user_sso_username: :class:`str` or ``None``
        :param admin_user_sso_username: Admin user sso username. If blank, administrator username will be
            used.
        :type  admin_user_sso_password: :class:`str` or ``None``
        :param admin_user_sso_password: Admin user sso password. Password needs to be a strong password
            with at least one Uppercase character, one lowercase character, one
            digit and one special character specified in braces [!$%^] and 8-20
            characters in length,and 3 maximum identical adjacent characters!.
            If blank, the SDDC Local Admin Password will be used (if provided)
            or password will be auto-generated.
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.vcenter_hostname = vcenter_hostname
        self.root_vcenter_password = root_vcenter_password
        self.vm_size = vm_size
        self.storage_size = storage_size
        self.sso_domain = sso_domain
        self.admin_user_sso_username = admin_user_sso_username
        self.admin_user_sso_password = admin_user_sso_password
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


SddcVcenterSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_vcenter_spec', {
        'vcenterHostname': type.OptionalType(type.StringType()),
        'rootVcenterPassword': type.OptionalType(type.StringType()),
        'vmSize': type.OptionalType(type.StringType()),
        'storageSize': type.OptionalType(type.StringType()),
        'ssoDomain': type.OptionalType(type.StringType()),
        'adminUserSsoUsername': type.OptionalType(type.StringType()),
        'adminUserSsoPassword': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    SddcVcenterSpec,
    False,
    None))



class SecuritySpec(VapiStruct):
    """
    Spec contains security settings

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'esxiCertsMode': 'esxi_certs_mode',
                            'rootCaCerts': 'root_ca_certs',
                            }

    def __init__(self,
                 esxi_certs_mode=None,
                 root_ca_certs=None,
                ):
        """
        :type  esxi_certs_mode: :class:`str` or ``None``
        :param esxi_certs_mode: ESXi certificates mode. One among:Custom, VMCA
        :type  root_ca_certs: :class:`list` of :class:`RootCaCerts` or ``None``
        :param root_ca_certs: Root Certificate Authority certificate list
        """
        self.esxi_certs_mode = esxi_certs_mode
        self.root_ca_certs = root_ca_certs
        VapiStruct.__init__(self)


SecuritySpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.security_spec', {
        'esxiCertsMode': type.OptionalType(type.StringType()),
        'rootCaCerts': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'RootCaCerts'))),
    },
    SecuritySpec,
    False,
    None))



class TeamingSpec(VapiStruct):
    """
    This specification contains the teaming policies associated with the uplink
    profile.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'policy': 'policy',
                            'activeUplinks': 'active_uplinks',
                            'standByUplinks': 'stand_by_uplinks',
                            }

    def __init__(self,
                 policy=None,
                 active_uplinks=None,
                 stand_by_uplinks=None,
                ):
        """
        :type  policy: :class:`str` or ``None``
        :param policy: The teaming policy associated with the uplink profile
        :type  active_uplinks: :class:`list` of :class:`str` or ``None``
        :param active_uplinks: The list of active uplinks
        :type  stand_by_uplinks: :class:`list` of :class:`str` or ``None``
        :param stand_by_uplinks: The list of stand by uplinks
        """
        self.policy = policy
        self.active_uplinks = active_uplinks
        self.stand_by_uplinks = stand_by_uplinks
        VapiStruct.__init__(self)


TeamingSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.teaming_spec', {
        'policy': type.OptionalType(type.StringType()),
        'activeUplinks': type.OptionalType(type.ListType(type.StringType())),
        'standByUplinks': type.OptionalType(type.ListType(type.StringType())),
    },
    TeamingSpec,
    False,
    None))



class TransportZone(VapiStruct):
    """
    The transport zone to be associated with the vSphere Distributed Switch
    managed by NSX

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'transportType': 'transport_type',
                            }

    def __init__(self,
                 name=None,
                 transport_type=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: The name of the transport zone
        :type  transport_type: :class:`str` or ``None``
        :param transport_type: The type of the transport zone
        """
        self.name = name
        self.transport_type = transport_type
        VapiStruct.__init__(self)


TransportZone._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.transport_zone', {
        'name': type.OptionalType(type.StringType()),
        'transportType': type.OptionalType(type.StringType()),
    },
    TransportZone,
    False,
    None))



class VcfAutomationSpec(VapiStruct):
    """
    Specification for VCF Automation

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            'adminUserPassword': 'admin_user_password',
                            'ipPool': 'ip_pool',
                            'internalClusterCidr': 'internal_cluster_cidr',
                            'nodePrefix': 'node_prefix',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 hostname=None,
                 admin_user_password=None,
                 ip_pool=None,
                 internal_cluster_cidr=None,
                 node_prefix=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: Host name
        :type  admin_user_password: :class:`str` or ``None``
        :param admin_user_password: Admin user password. If blank the password will be auto-generated.
        :type  ip_pool: :class:`list` of :class:`str` or ``None``
        :param ip_pool: List of IP addresses. For Standard deployment model two IP
            addresses need to be specified and for High Availability four IP
            addresses need to be specified
        :type  internal_cluster_cidr: :class:`str` or ``None``
        :param internal_cluster_cidr: Internal Cluster CIDR. One among: 198.18.0.0/15, 240.0.0.0/15,
            250.0.0.0/15
        :type  node_prefix: :class:`str` or ``None``
        :param node_prefix: Node Prefix. It cannot be blank and must begin and end with an
            alphanumeric character, and can only contain lowercase alphanumeric
            characters or hyphens.
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.hostname = hostname
        self.admin_user_password = admin_user_password
        self.ip_pool = ip_pool
        self.internal_cluster_cidr = internal_cluster_cidr
        self.node_prefix = node_prefix
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcfAutomationSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_automation_spec', {
        'hostname': type.OptionalType(type.StringType()),
        'adminUserPassword': type.OptionalType(type.StringType()),
        'ipPool': type.OptionalType(type.ListType(type.StringType())),
        'internalClusterCidr': type.OptionalType(type.StringType()),
        'nodePrefix': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcfAutomationSpec,
    False,
    None))



class VcfOperationsCollectorSpec(VapiStruct):
    """
    Specification for VCF Operations collector

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            'rootUserPassword': 'root_user_password',
                            'applianceSize': 'appliance_size',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 hostname=None,
                 root_user_password=None,
                 appliance_size=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: Host name
        :type  root_user_password: :class:`str` or ``None``
        :param root_user_password: Root user password.
        :type  appliance_size: :class:`str` or ``None``
        :param appliance_size: VCF Operations collector appliance size. One among: small,
            standard. Default value if not provided is small
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.hostname = hostname
        self.root_user_password = root_user_password
        self.appliance_size = appliance_size
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcfOperationsCollectorSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_collector_spec', {
        'hostname': type.OptionalType(type.StringType()),
        'rootUserPassword': type.OptionalType(type.StringType()),
        'applianceSize': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcfOperationsCollectorSpec,
    False,
    None))



class VcfOperationsFleetManagementSpec(VapiStruct):
    """
    Specification for VCF Operations fleet management

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            'rootUserPassword': 'root_user_password',
                            'adminUserPassword': 'admin_user_password',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 hostname=None,
                 root_user_password=None,
                 admin_user_password=None,
                 use_existing_deployment=None,
                 version=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: Host name
        :type  root_user_password: :class:`str` or ``None``
        :param root_user_password: Root user password. Password should be at least 15 characters in
            length. If blank the password will be auto-generated.
        :type  admin_user_password: :class:`str` or ``None``
        :param admin_user_password: Admin user password. If blank the password will be auto-generated.
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the product's certificate. Need to be
            populated when using existing deployment in order to establish
            trust with the existing product.
        """
        self.hostname = hostname
        self.root_user_password = root_user_password
        self.admin_user_password = admin_user_password
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcfOperationsFleetManagementSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_fleet_management_spec', {
        'hostname': type.OptionalType(type.StringType()),
        'rootUserPassword': type.OptionalType(type.StringType()),
        'adminUserPassword': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcfOperationsFleetManagementSpec,
    False,
    None))



class VcfOperationsNode(VapiStruct):
    """
    Specification for VCF Operations Node

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'hostname': 'hostname',
                            'rootUserPassword': 'root_user_password',
                            'type': 'type',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 hostname=None,
                 root_user_password=None,
                 type=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  hostname: :class:`str` or ``None``
        :param hostname: Host name
        :type  root_user_password: :class:`str` or ``None``
        :param root_user_password: Root user password.
        :type  type: :class:`str` or ``None``
        :param type: Node type. One among: master, replica, data
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: SSL thumbprint (SHA256) of the node certificate. Need to be
            populated when using existing VCF Ops deployment.
        """
        self.hostname = hostname
        self.root_user_password = root_user_password
        self.type = type
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcfOperationsNode._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_node', {
        'hostname': type.OptionalType(type.StringType()),
        'rootUserPassword': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcfOperationsNode,
    False,
    None))



class VcfOperationsSpec(VapiStruct):
    """
    Specification for VCF Operations

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'nodes': 'nodes',
                            'adminUserPassword': 'admin_user_password',
                            'applianceSize': 'appliance_size',
                            'loadBalancerFqdn': 'load_balancer_fqdn',
                            'useExistingDeployment': 'use_existing_deployment',
                            'version': 'version',
                            }

    def __init__(self,
                 nodes=None,
                 admin_user_password=None,
                 appliance_size=None,
                 load_balancer_fqdn=None,
                 use_existing_deployment=None,
                 version=None,
                ):
        """
        :type  nodes: :class:`list` of :class:`VcfOperationsNode` or ``None``
        :param nodes: List of nodes
        :type  admin_user_password: :class:`str` or ``None``
        :param admin_user_password: Admin user password. If blank the password will be auto-generated.
        :type  appliance_size: :class:`str` or ``None``
        :param appliance_size: VCF Operations appliance size. One among: xsmall, small, medium,
            large, xlarge for Simple deployment model and one among: medium,
            large, xlarge for High Availability. Default value if not provided
            is medium for both deployment models.
        :type  load_balancer_fqdn: :class:`str` or ``None``
        :param load_balancer_fqdn: Load Balancer FQDN
        :type  use_existing_deployment: :class:`bool` or ``None``
        :param use_existing_deployment: Import existing deployment or deploy one.
        :type  version: :class:`str` or ``None``
        :param version: Version
        """
        self.nodes = nodes
        self.admin_user_password = admin_user_password
        self.appliance_size = appliance_size
        self.load_balancer_fqdn = load_balancer_fqdn
        self.use_existing_deployment = use_existing_deployment
        self.version = version
        VapiStruct.__init__(self)


VcfOperationsSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_spec', {
        'nodes': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcfOperationsNode'))),
        'adminUserPassword': type.OptionalType(type.StringType()),
        'applianceSize': type.OptionalType(type.StringType()),
        'loadBalancerFqdn': type.OptionalType(type.StringType()),
        'useExistingDeployment': type.OptionalType(type.BooleanType()),
        'version': type.OptionalType(type.StringType()),
    },
    VcfOperationsSpec,
    False,
    None))



class VmfsDatastoreSpec(VapiStruct):
    """
    Cluster storage configuration for VMFS

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'fcSpec': 'fc_spec',
                            }

    def __init__(self,
                 fc_spec=None,
                ):
        """
        :type  fc_spec: :class:`list` of :class:`FcSpec` or ``None``
        :param fc_spec: Cluster storage configuration for VMFS on FC
        """
        self.fc_spec = fc_spec
        VapiStruct.__init__(self)


VmfsDatastoreSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vmfs_datastore_spec', {
        'fcSpec': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FcSpec'))),
    },
    VmfsDatastoreSpec,
    False,
    None))



class VmnicToUplink(VapiStruct):
    """
    This specification contains vmnic to uplink configurations for vSphere
    host.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'uplink': 'uplink',
                            }

    def __init__(self,
                 id=None,
                 uplink=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: VmNic ID of vSphere host to be associated with VDS, once added to
            cluster
        :type  uplink: :class:`str` or ``None``
        :param uplink: The uplink name of the vSphere Distributed Switch to be associated
        """
        self.id = id
        self.uplink = uplink
        VapiStruct.__init__(self)


VmnicToUplink._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vmnic_to_uplink', {
        'id': type.OptionalType(type.StringType()),
        'uplink': type.OptionalType(type.StringType()),
    },
    VmnicToUplink,
    False,
    None))



class VsanEsaConfig(VapiStruct):
    """
    This spec contains cluster vSAN ESA configuration

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'enabled': 'enabled',
                            }

    def __init__(self,
                 enabled=None,
                ):
        """
        :type  enabled: :class:`bool` or ``None``
        :param enabled: Whether the vSAN ESA is enabled.
        """
        self.enabled = enabled
        VapiStruct.__init__(self)


VsanEsaConfig._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vsan_esa_config', {
        'enabled': type.OptionalType(type.BooleanType()),
    },
    VsanEsaConfig,
    False,
    None))



class VsanSpec(VapiStruct):
    """
    Spec contains parameters of Virtual SAN

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'datastoreName': 'datastore_name',
                            'vsanDedup': 'vsan_dedup',
                            'esaConfig': 'esa_config',
                            'failuresToTolerate': 'failures_to_tolerate',
                            }

    def __init__(self,
                 datastore_name=None,
                 vsan_dedup=None,
                 esa_config=None,
                 failures_to_tolerate=None,
                ):
        """
        :type  datastore_name: :class:`str` or ``None``
        :param datastore_name: Datastore Name. It will be auto-generated if blank
        :type  vsan_dedup: :class:`bool` or ``None``
        :param vsan_dedup: VSAN feature Deduplication and Compression flag, one flag for both
            features
        :type  esa_config: :class:`VsanEsaConfig` or ``None``
        :param esa_config:         :type  failures_to_tolerate: :class:`long` or ``None``
        :param failures_to_tolerate: Host failures to tolerate
        """
        self.datastore_name = datastore_name
        self.vsan_dedup = vsan_dedup
        self.esa_config = esa_config
        self.failures_to_tolerate = failures_to_tolerate
        VapiStruct.__init__(self)


VsanSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vsan_spec', {
        'datastoreName': type.OptionalType(type.StringType()),
        'vsanDedup': type.OptionalType(type.BooleanType()),
        'esaConfig': type.OptionalType(type.ReferenceType(__name__, 'VsanEsaConfig')),
        'failuresToTolerate': type.OptionalType(type.IntegerType()),
    },
    VsanSpec,
    False,
    None))



class MessagePack(VapiStruct):
    """
    A message pack representing a localizable message and suitable for machine
    processing. Contains a message key unique in the scope of the specified
    component, as well as the arguments needed to generate the localized
    message.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'component': 'component',
                            'messageKey': 'message_key',
                            'arguments': 'arguments',
                            'message': 'message',
                            'bundle': 'bundle',
                            }

    def __init__(self,
                 component=None,
                 message_key=None,
                 arguments=None,
                 message=None,
                 bundle=None,
                ):
        """
        :type  component: :class:`str` or ``None``
        :param component: The component the message belongs to
        :type  message_key: :class:`str` or ``None``
        :param message_key: The machine-readable key of the message
        :type  arguments: :class:`list` of :class:`str` or ``None``
        :param arguments: The arguments used to localize the message. Can be used by scripts
            to automate the response processing.
        :type  message: :class:`str` or ``None``
        :param message: The localized message (if not provided by another property)
        :type  bundle: :class:`str` or ``None``
        :param bundle: The local resource bundle details
        """
        self.component = component
        self.message_key = message_key
        self.arguments = arguments
        self.message = message
        self.bundle = bundle
        VapiStruct.__init__(self)


MessagePack._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.message_pack', {
        'component': type.OptionalType(type.StringType()),
        'messageKey': type.OptionalType(type.StringType()),
        'arguments': type.OptionalType(type.ListType(type.StringType())),
        'message': type.OptionalType(type.StringType()),
        'bundle': type.OptionalType(type.StringType()),
    },
    MessagePack,
    False,
    None))



class SddcMilestoneTask(VapiStruct):
    """
    Represents a SDDC Milestone

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'description': 'description',
                            'status': 'status',
                            'creationTimestamp': 'creation_timestamp',
                            'updateTimestamp': 'update_timestamp',
                            }

    def __init__(self,
                 name=None,
                 description=None,
                 status=None,
                 creation_timestamp=None,
                 update_timestamp=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: SDDC Milestone Name
        :type  description: :class:`str` or ``None``
        :param description: SDDC Milestone Description
        :type  status: :class:`str` or ``None``
        :param status: SDDC Milestone Task Status
        :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp: SDDC Milestone Creation Time
        :type  update_timestamp: :class:`str` or ``None``
        :param update_timestamp: Last Update Time of SDDC Milestone
        """
        self.name = name
        self.description = description
        self.status = status
        self.creation_timestamp = creation_timestamp
        self.update_timestamp = update_timestamp
        VapiStruct.__init__(self)


SddcMilestoneTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_milestone_task', {
        'name': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'updateTimestamp': type.OptionalType(type.StringType()),
    },
    SddcMilestoneTask,
    False,
    None))



class SddcSubTask(VapiStruct):
    """
    Represents a SDDC sub-task

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'sddcId': 'sddc_id',
                            'processingStateName': 'processing_state_name',
                            'processingStateDescription': 'processing_state_description',
                            'name': 'name',
                            'description': 'description',
                            'localizableNamePack': 'localizable_name_pack',
                            'localizableDescriptionPack': 'localizable_description_pack',
                            'status': 'status',
                            'creationTimestamp': 'creation_timestamp',
                            'updateTimestamp': 'update_timestamp',
                            'errors': 'errors',
                            }

    def __init__(self,
                 sddc_id=None,
                 processing_state_name=None,
                 processing_state_description=None,
                 name=None,
                 description=None,
                 localizable_name_pack=None,
                 localizable_description_pack=None,
                 status=None,
                 creation_timestamp=None,
                 update_timestamp=None,
                 errors=None,
                ):
        """
        :type  sddc_id: :class:`str` or ``None``
        :param sddc_id: SDDC ID
        :type  processing_state_name: :class:`str` or ``None``
        :param processing_state_name: Processing category name, e.g., VC Deployment, VSAN configuration
            etc
        :type  processing_state_description: :class:`str` or ``None``
        :param processing_state_description: Processing category description, e.g., VC Deployment, VSAN
            configuration etc
        :type  name: :class:`str` or ``None``
        :param name: Sub-Task Name
        :type  description: :class:`str` or ``None``
        :param description: Sub-Task Description
        :type  localizable_name_pack: :class:`MessagePack` or ``None``
        :param localizable_name_pack:         :type  localizable_description_pack: :class:`MessagePack` or ``None``
        :param localizable_description_pack:         :type  status: :class:`str` or ``None``
        :param status: Task Status
        :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp: Sub-Task Creation Time
        :type  update_timestamp: :class:`str` or ``None``
        :param update_timestamp: Last Update Time of Sub-Task
        :type  errors: :class:`list` of :class:`Error` or ``None``
        :param errors: List of errors in case of a failure 
            
            * Property is read-only.
            
            
        """
        self.sddc_id = sddc_id
        self.processing_state_name = processing_state_name
        self.processing_state_description = processing_state_description
        self.name = name
        self.description = description
        self.localizable_name_pack = localizable_name_pack
        self.localizable_description_pack = localizable_description_pack
        self.status = status
        self.creation_timestamp = creation_timestamp
        self.update_timestamp = update_timestamp
        self.errors = errors
        VapiStruct.__init__(self)


SddcSubTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_sub_task', {
        'sddcId': type.OptionalType(type.StringType()),
        'processingStateName': type.OptionalType(type.StringType()),
        'processingStateDescription': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'localizableNamePack': type.OptionalType(type.ReferenceType(__name__, 'MessagePack')),
        'localizableDescriptionPack': type.OptionalType(type.ReferenceType(__name__, 'MessagePack')),
        'status': type.OptionalType(type.StringType()),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'updateTimestamp': type.OptionalType(type.StringType()),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Error'))),
    },
    SddcSubTask,
    False,
    None))



class SddcTask(VapiStruct):
    """
    Represents a SDDC task

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'status': 'status',
                            'localizableNamePack': 'localizable_name_pack',
                            'creationTimestamp': 'creation_timestamp',
                            'sddcSubTasks': 'sddc_sub_tasks',
                            'milestones': 'milestones',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 status=None,
                 localizable_name_pack=None,
                 creation_timestamp=None,
                 sddc_sub_tasks=None,
                 milestones=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: SDDC ID 
            
            * Property is read-only.
            
            
        :type  name: :class:`str` or ``None``
        :param name: Task name 
            
            * Property is read-only.
            
            
        :type  status: :class:`str` or ``None``
        :param status: SDDC Task status. One among: IN_PROGRESS, COMPLETED_WITH_SUCCESS,
            ROLLBACK_SUCCESS, COMPLETED_WITH_FAILURE 
            
            * Property is read-only.
            
            
        :type  localizable_name_pack: :class:`MessagePack` or ``None``
        :param localizable_name_pack:         :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp: SDDC Task creation timestamp 
            
            * Property is read-only.
            
            
        :type  sddc_sub_tasks: :class:`list` of :class:`SddcSubTask` or ``None``
        :param sddc_sub_tasks: All SDDC Sub-Tasks
        :type  milestones: :class:`list` of :class:`SddcMilestoneTask` or ``None``
        :param milestones: Milestones of the workflow
        """
        self.id = id
        self.name = name
        self.status = status
        self.localizable_name_pack = localizable_name_pack
        self.creation_timestamp = creation_timestamp
        self.sddc_sub_tasks = sddc_sub_tasks
        self.milestones = milestones
        VapiStruct.__init__(self)


SddcTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_task', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'localizableNamePack': type.OptionalType(type.ReferenceType(__name__, 'MessagePack')),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'sddcSubTasks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcSubTask'))),
        'milestones': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcMilestoneTask'))),
    },
    SddcTask,
    False,
    None))



class VcfOperationsDiscoverySpec(VapiStruct):
    """
    VCF Operations specification holding endpoint information which to query
    for topology/discovery data.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'address': 'address',
                            'adminUsername': 'admin_username',
                            'adminPassword': 'admin_password',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 address=None,
                 admin_username=None,
                 admin_password=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  address: :class:`str` or ``None``
        :param address: VCF Operations instance address.
        :type  admin_username: :class:`str` or ``None``
        :param admin_username: Admin username. Can be omitted.
        :type  admin_password: :class:`str` or ``None``
        :param admin_password: Admin password.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: VCF Operations SSL thumbprint (SHA256).
        """
        self.address = address
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcfOperationsDiscoverySpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_discovery_spec', {
        'address': type.OptionalType(type.StringType()),
        'adminUsername': type.OptionalType(type.StringType()),
        'adminPassword': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcfOperationsDiscoverySpec,
    False,
    None))



class NodeAddress(VapiStruct):
    """
    Node address.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'type': 'type',
                            'value': 'value',
                            }

    def __init__(self,
                 type=None,
                 value=None,
                ):
        """
        :type  type: :class:`str` or ``None``
        :param type: Address type. One among: fqdn, ipv4
        :type  value: :class:`str` or ``None``
        :param value: Address value.
        """
        self.type = type
        self.value = value
        VapiStruct.__init__(self)


NodeAddress._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.node_address', {
        'type': type.OptionalType(type.StringType()),
        'value': type.OptionalType(type.StringType()),
    },
    NodeAddress,
    False,
    None))



class NsxAdapterInfo(VapiStruct):
    """
    NSX Adapter information registered in Vcf Operations instance.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'address': 'address',
                            'vcenterAddress': 'vcenter_address',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 address=None,
                 vcenter_address=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Adapter ID.
        :type  name: :class:`str` or ``None``
        :param name: Adapter name.
        :type  address: :class:`str` or ``None``
        :param address: NSX address.
        :type  vcenter_address: :class:`str` or ``None``
        :param vcenter_address: vCenter address.
        """
        self.id = id
        self.name = name
        self.address = address
        self.vcenter_address = vcenter_address
        VapiStruct.__init__(self)


NsxAdapterInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.nsx_adapter_info', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'address': type.OptionalType(type.StringType()),
        'vcenterAddress': type.OptionalType(type.StringType()),
    },
    NsxAdapterInfo,
    False,
    None))



class VcenterAdapterInfo(VapiStruct):
    """
    vCenter Adapter information registered in Vcf Operations instance.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'address': 'address',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 address=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Adapter ID.
        :type  name: :class:`str` or ``None``
        :param name: Adapter name.
        :type  address: :class:`str` or ``None``
        :param address: vCenter address.
        """
        self.id = id
        self.name = name
        self.address = address
        VapiStruct.__init__(self)


VcenterAdapterInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcenter_adapter_info', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'address': type.OptionalType(type.StringType()),
    },
    VcenterAdapterInfo,
    False,
    None))



class VcfAutomationNodeInfo(VapiStruct):
    """
    VCF Automation node information.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'addresses': 'addresses',
                            'certificateThumbprints': 'certificate_thumbprints',
                            }

    def __init__(self,
                 name=None,
                 addresses=None,
                 certificate_thumbprints=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Node name.
        :type  addresses: :class:`list` of :class:`NodeAddress` or ``None``
        :param addresses: Node addresses.
        :type  certificate_thumbprints: :class:`list` of :class:`str` or ``None``
        :param certificate_thumbprints: Certificate thumbprints (SHA256).
        """
        self.name = name
        self.addresses = addresses
        self.certificate_thumbprints = certificate_thumbprints
        VapiStruct.__init__(self)


VcfAutomationNodeInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_automation_node_info', {
        'name': type.OptionalType(type.StringType()),
        'addresses': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'NodeAddress'))),
        'certificateThumbprints': type.OptionalType(type.ListType(type.StringType())),
    },
    VcfAutomationNodeInfo,
    False,
    None))



class VcfOperationsDiscoveryResult(VapiStruct):
    """
    Topology discovery result from querying VCF Operations instance.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'vcfOperationsVersion': 'vcf_operations_version',
                            'vcfOperationsBuildNumber': 'vcf_operations_build_number',
                            'vcfOperationsNodes': 'vcf_operations_nodes',
                            'vcfOperationsManagementNode': 'vcf_operations_management_node',
                            'vcfAutomationNodes': 'vcf_automation_nodes',
                            'vcenterAdapters': 'vcenter_adapters',
                            'nsxAdapters': 'nsx_adapters',
                            }

    def __init__(self,
                 vcf_operations_version=None,
                 vcf_operations_build_number=None,
                 vcf_operations_nodes=None,
                 vcf_operations_management_node=None,
                 vcf_automation_nodes=None,
                 vcenter_adapters=None,
                 nsx_adapters=None,
                ):
        """
        :type  vcf_operations_version: :class:`str` or ``None``
        :param vcf_operations_version: VCF Operations instance version.
        :type  vcf_operations_build_number: :class:`str` or ``None``
        :param vcf_operations_build_number: VCF Operations instance build number.
        :type  vcf_operations_nodes: :class:`list` of :class:`VcfOperationsNodeInfo` or ``None``
        :param vcf_operations_nodes: VCF Operations nodes info.
        :type  vcf_operations_management_node: :class:`VcfOperationsManagementNodeInfo` or ``None``
        :param vcf_operations_management_node:         :type  vcf_automation_nodes: :class:`list` of :class:`VcfAutomationNodeInfo` or ``None``
        :param vcf_automation_nodes: VCF Automation nodes info.
        :type  vcenter_adapters: :class:`list` of :class:`VcenterAdapterInfo` or ``None``
        :param vcenter_adapters: Registered vCenter adapters.
        :type  nsx_adapters: :class:`list` of :class:`NsxAdapterInfo` or ``None``
        :param nsx_adapters: Registered NSX adapters.
        """
        self.vcf_operations_version = vcf_operations_version
        self.vcf_operations_build_number = vcf_operations_build_number
        self.vcf_operations_nodes = vcf_operations_nodes
        self.vcf_operations_management_node = vcf_operations_management_node
        self.vcf_automation_nodes = vcf_automation_nodes
        self.vcenter_adapters = vcenter_adapters
        self.nsx_adapters = nsx_adapters
        VapiStruct.__init__(self)


VcfOperationsDiscoveryResult._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_discovery_result', {
        'vcfOperationsVersion': type.OptionalType(type.StringType()),
        'vcfOperationsBuildNumber': type.OptionalType(type.StringType()),
        'vcfOperationsNodes': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcfOperationsNodeInfo'))),
        'vcfOperationsManagementNode': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsManagementNodeInfo')),
        'vcfAutomationNodes': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcfAutomationNodeInfo'))),
        'vcenterAdapters': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcenterAdapterInfo'))),
        'nsxAdapters': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'NsxAdapterInfo'))),
    },
    VcfOperationsDiscoveryResult,
    False,
    None))



class VcfOperationsManagementNodeInfo(VapiStruct):
    """
    VCF Operations Management node information.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'addresses': 'addresses',
                            'certificateThumbprints': 'certificate_thumbprints',
                            }

    def __init__(self,
                 name=None,
                 addresses=None,
                 certificate_thumbprints=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Node name.
        :type  addresses: :class:`list` of :class:`NodeAddress` or ``None``
        :param addresses: Node addresses.
        :type  certificate_thumbprints: :class:`list` of :class:`str` or ``None``
        :param certificate_thumbprints: Certificate thumbprints (SHA256).
        """
        self.name = name
        self.addresses = addresses
        self.certificate_thumbprints = certificate_thumbprints
        VapiStruct.__init__(self)


VcfOperationsManagementNodeInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_management_node_info', {
        'name': type.OptionalType(type.StringType()),
        'addresses': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'NodeAddress'))),
        'certificateThumbprints': type.OptionalType(type.ListType(type.StringType())),
    },
    VcfOperationsManagementNodeInfo,
    False,
    None))



class VcfOperationsNodeInfo(VapiStruct):
    """
    VCF Operations node information.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'address': 'address',
                            'name': 'name',
                            'type': 'type',
                            }

    def __init__(self,
                 address=None,
                 name=None,
                 type=None,
                ):
        """
        :type  address: :class:`str` or ``None``
        :param address: Node address.
        :type  name: :class:`str` or ``None``
        :param name: Node name.
        :type  type: :class:`str` or ``None``
        :param type: Node type. One among: master, replica, data, witness, cloudproxy
        """
        self.address = address
        self.name = name
        self.type = type
        VapiStruct.__init__(self)


VcfOperationsNodeInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_node_info', {
        'address': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
    },
    VcfOperationsNodeInfo,
    False,
    None))



class VcenterDiscoverySpec(VapiStruct):
    """
    vCenter specification holding endpoint information which to query for
    topology/discovery data.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'address': 'address',
                            'username': 'username',
                            'password': 'password',
                            'sslThumbprint': 'ssl_thumbprint',
                            }

    def __init__(self,
                 address=None,
                 username=None,
                 password=None,
                 ssl_thumbprint=None,
                ):
        """
        :type  address: :class:`str` or ``None``
        :param address: vCenter address.
        :type  username: :class:`str` or ``None``
        :param username: SSO username.
        :type  password: :class:`str` or ``None``
        :param password: SSO password.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: vCenter SSL thumbprint (SHA256)
        """
        self.address = address
        self.username = username
        self.password = password
        self.ssl_thumbprint = ssl_thumbprint
        VapiStruct.__init__(self)


VcenterDiscoverySpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcenter_discovery_spec', {
        'address': type.OptionalType(type.StringType()),
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.StringType()),
        'sslThumbprint': type.OptionalType(type.StringType()),
    },
    VcenterDiscoverySpec,
    False,
    None))



class VcenterDiscoveryResult(VapiStruct):
    """
    Topology discovery result from querying vCenter instance.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'vcenterVersion': 'vcenter_version',
                            'vcenterBuildNumber': 'vcenter_build_number',
                            'nsxInfo': 'nsx_info',
                            }

    def __init__(self,
                 vcenter_version=None,
                 vcenter_build_number=None,
                 nsx_info=None,
                ):
        """
        :type  vcenter_version: :class:`str` or ``None``
        :param vcenter_version: vCenter version.
        :type  vcenter_build_number: :class:`str` or ``None``
        :param vcenter_build_number: vCenter build number.
        :type  nsx_info: :class:`VcenterNsxInfo` or ``None``
        :param nsx_info:         """
        self.vcenter_version = vcenter_version
        self.vcenter_build_number = vcenter_build_number
        self.nsx_info = nsx_info
        VapiStruct.__init__(self)


VcenterDiscoveryResult._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcenter_discovery_result', {
        'vcenterVersion': type.OptionalType(type.StringType()),
        'vcenterBuildNumber': type.OptionalType(type.StringType()),
        'nsxInfo': type.OptionalType(type.ReferenceType(__name__, 'VcenterNsxInfo')),
    },
    VcenterDiscoveryResult,
    False,
    None))



class VcenterNsxInfo(VapiStruct):
    """
    NSX instance associated with vCenter instance.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'address': 'address',
                            }

    def __init__(self,
                 address=None,
                ):
        """
        :type  address: :class:`str` or ``None``
        :param address: NSX address.
        """
        self.address = address
        VapiStruct.__init__(self)


VcenterNsxInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcenter_nsx_info', {
        'address': type.OptionalType(type.StringType()),
    },
    VcenterNsxInfo,
    False,
    None))



class Validation(VapiStruct):
    """
    Represents a validation with a list of one or more validation checks that
    are performed as part of the validation

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'description': 'description',
                            'executionStatus': 'execution_status',
                            'resultStatus': 'result_status',
                            'validationChecks': 'validation_checks',
                            'additionalProperties': 'additional_properties',
                            }

    def __init__(self,
                 id=None,
                 description=None,
                 execution_status=None,
                 result_status=None,
                 validation_checks=None,
                 additional_properties=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: ID of the validation 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Description of the validation 
            
            * Property is read-only.
            
            
        :type  execution_status: :class:`str` or ``None``
        :param execution_status: Execution status of the validation. One among: IN_PROGRESS, FAILED,
            COMPLETED, UNKNOWN, SKIPPED, CANCELLED, CANCELLATION_IN_PROGRESS 
            
            * Property is read-only.
            
            
        :type  result_status: :class:`str` or ``None``
        :param result_status: Result status of the validation after it has completed its
            execution. One among: SUCCEEDED, FAILED, WARNING, UNKNOWN,
            CANCELLATION_IN_PROGRESS 
            
            * Property is read-only.
            
            
        :type  validation_checks: :class:`list` of :class:`ValidationCheck` or ``None``
        :param validation_checks: List of one or more validation checks that are performed as part of
            the validation 
            
            * Property is read-only.
            
            
        :type  additional_properties: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
        :param additional_properties:         """
        self.id = id
        self.description = description
        self.execution_status = execution_status
        self.result_status = result_status
        self.validation_checks = validation_checks
        self.additional_properties = additional_properties
        VapiStruct.__init__(self)


Validation._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.validation', {
        'id': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'executionStatus': type.OptionalType(type.StringType()),
        'resultStatus': type.OptionalType(type.StringType()),
        'validationChecks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ValidationCheck'))),
        'additionalProperties': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
    },
    Validation,
    False,
    None))



class ValidationCheck(VapiStruct):
    """
    Represents a validation check

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'description': 'description',
                            'severity': 'severity',
                            'resultStatus': 'result_status',
                            'acknowledge': 'acknowledge',
                            'errorResponse': 'error_response',
                            }

    def __init__(self,
                 description=None,
                 severity=None,
                 result_status=None,
                 acknowledge=None,
                 error_response=None,
                ):
        """
        :type  description: :class:`str` or ``None``
        :param description: Description of the validation check 
            
            * Property is read-only.
            
            
        :type  severity: :class:`str` or ``None``
        :param severity: Severity of the validation check 
            
            * Property is read-only.
            
            
        :type  result_status: :class:`str` or ``None``
        :param result_status: Result status of the validation check after it has completed its
            execution
        :type  acknowledge: :class:`bool` or ``None``
        :param acknowledge: Flag indicating whether the validation check requires
            acknowledgment 
            
            * Property is read-only.
            
            
        :type  error_response: :class:`Error` or ``None``
        :param error_response:         """
        self.description = description
        self.severity = severity
        self.result_status = result_status
        self.acknowledge = acknowledge
        self.error_response = error_response
        VapiStruct.__init__(self)


ValidationCheck._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.validation_check', {
        'description': type.OptionalType(type.StringType()),
        'severity': type.OptionalType(type.StringType()),
        'resultStatus': type.OptionalType(type.StringType()),
        'acknowledge': type.OptionalType(type.BooleanType()),
        'errorResponse': type.OptionalType(type.ReferenceType(__name__, 'Error')),
    },
    ValidationCheck,
    False,
    None))



class SddcNetworkConfigProfileSpec(VapiStruct):
    """
    This specification contains the parameters needed to get pre-configured
    network profiles which to facilitate the configuration of the networking
    stack during Management Domain creation

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    STORAGE_TYPE_VSAN = "VSAN"
    """
    Storage type of the Management Domain

    """
    STORAGE_TYPE_VSAN_ESA = "VSAN_ESA"
    """
    Storage type of the Management Domain

    """
    STORAGE_TYPE_NFS = "NFS"
    """
    Storage type of the Management Domain

    """
    STORAGE_TYPE_FC = "FC"
    """
    Storage type of the Management Domain

    """



    _canonical_to_pep_names = {
                            'storageType': 'storage_type',
                            'hostSpecs': 'host_specs',
                            'subdomain': 'subdomain',
                            'nsxConfigType': 'nsx_config_type',
                            }

    def __init__(self,
                 storage_type=None,
                 host_specs=None,
                 subdomain=None,
                 nsx_config_type=None,
                ):
        """
        :type  storage_type: :class:`str` or ``None``
        :param storage_type: Storage type of the Management Domain
        :type  host_specs: :class:`list` of :class:`SddcHostSpec` or ``None``
        :param host_specs: List of hosts which will be used for the Management Domain
        :type  subdomain: :class:`str` or ``None``
        :param subdomain: Tenant Sub domain. Includes the full domain suffix
        :type  nsx_config_type: :class:`str` or ``None``
        :param nsx_config_type: NSX Config Type
        """
        self.storage_type = storage_type
        self.host_specs = host_specs
        self.subdomain = subdomain
        self.nsx_config_type = nsx_config_type
        VapiStruct.__init__(self)


SddcNetworkConfigProfileSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_network_config_profile_spec', {
        'storageType': type.OptionalType(type.StringType()),
        'hostSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcHostSpec'))),
        'subdomain': type.OptionalType(type.StringType()),
        'nsxConfigType': type.OptionalType(type.StringType()),
    },
    SddcNetworkConfigProfileSpec,
    False,
    None))



class SddcNetworkConfigProfile(VapiStruct):
    """
    Network configuration profile which can be used to configure the networking
    stack of the Management Domain.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'description': 'description',
                            'dvsSpecs': 'dvs_specs',
                            'dvsNameToPortgroupSpecs': 'dvs_name_to_portgroup_specs',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 description=None,
                 dvs_specs=None,
                 dvs_name_to_portgroup_specs=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Id of the profile. One among: "DEFAULT", "STORAGE_SEPARATION",
            "NSX_SEPARATION", "STORAGE_NSX_SEPARATION" 
            
            * Property is read-only.
            
            
        :type  name: :class:`str` or ``None``
        :param name: Name of the profile 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Description of the profile 
            
            * Property is read-only.
            
            
        :type  dvs_specs: :class:`list` of :class:`DvsSpec` or ``None``
        :param dvs_specs: vSphere Distributed Switches topology 
            
            * Property is read-only.
            
            
        :type  dvs_name_to_portgroup_specs: (:class:`dict` of :class:`str` and :class:`list` of :class:`SddcNetworkSpec`) or ``None``
        :param dvs_name_to_portgroup_specs: Map of vSphere Distributed Switch name to portgroup/network specs 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.name = name
        self.description = description
        self.dvs_specs = dvs_specs
        self.dvs_name_to_portgroup_specs = dvs_name_to_portgroup_specs
        VapiStruct.__init__(self)


SddcNetworkConfigProfile._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_network_config_profile', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'dvsSpecs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'DvsSpec'))),
        'dvsNameToPortgroupSpecs': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.ReferenceType(__name__, 'SddcNetworkSpec')))),
    },
    SddcNetworkConfigProfile,
    False,
    None))



class SddcNetworkConfigProfileResponse(VapiStruct):
    """
    Response holding pre-configured network profiles and list of common
    physical NICs.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'commonPhysicalNics': 'common_physical_nics',
                            'profiles': 'profiles',
                            }

    def __init__(self,
                 common_physical_nics=None,
                 profiles=None,
                ):
        """
        :type  common_physical_nics: :class:`list` of :class:`SddcPhysicalNic` or ``None``
        :param common_physical_nics: List of physical NICs common to all hosts. 
            
            * Property is read-only.
            
            
        :type  profiles: :class:`list` of :class:`SddcNetworkConfigProfile` or ``None``
        :param profiles: List of pre-configured network profiles 
            
            * Property is read-only.
            
            
        """
        self.common_physical_nics = common_physical_nics
        self.profiles = profiles
        VapiStruct.__init__(self)


SddcNetworkConfigProfileResponse._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_network_config_profile_response', {
        'commonPhysicalNics': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcPhysicalNic'))),
        'profiles': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcNetworkConfigProfile'))),
    },
    SddcNetworkConfigProfileResponse,
    False,
    None))



class SddcPhysicalNic(VapiStruct):
    """
    Physical NIC information which can be shared between multiple hosts

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'deviceName': 'device_name',
                            'speedMb': 'speed_mb',
                            'isSmartNic': 'is_smart_nic',
                            'smartNic': 'smart_nic',
                            }

    def __init__(self,
                 device_name=None,
                 speed_mb=None,
                 is_smart_nic=None,
                 smart_nic=None,
                ):
        """
        :type  device_name: :class:`str` or ``None``
        :param device_name: Device name of the physical NIC 
            
            * Property is read-only.
            
            
        :type  speed_mb: :class:`long` or ``None``
        :param speed_mb: Speed of the physical NIC 
            
            * Property is read-only.
            
            
        :type  is_smart_nic: :class:`bool` or ``None``
        :param is_smart_nic: 
            
            * Property is write-only.
            
            
        :type  smart_nic: :class:`bool` or ``None``
        :param smart_nic:         """
        self.device_name = device_name
        self.speed_mb = speed_mb
        self.is_smart_nic = is_smart_nic
        self.smart_nic = smart_nic
        VapiStruct.__init__(self)


SddcPhysicalNic._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_physical_nic', {
        'deviceName': type.OptionalType(type.StringType()),
        'speedMb': type.OptionalType(type.IntegerType()),
        'isSmartNic': type.OptionalType(type.BooleanType()),
        'smartNic': type.OptionalType(type.BooleanType()),
    },
    SddcPhysicalNic,
    False,
    None))



class SddcInstallerRequest(VapiStruct):
    """
    Spec contains parameters for Host

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'endpoints': 'endpoints',
                            'subdomain': 'subdomain',
                            }

    def __init__(self,
                 endpoints=None,
                 subdomain=None,
                ):
        """
        :type  endpoints: :class:`list` of :class:`SddcHostSpec` or ``None``
        :param endpoints: List of ESXi/vCenter in which the appliance will check for itself
        :type  subdomain: :class:`str` or ``None``
        :param subdomain: Tenant Sub domain. Includes the full domain suffix
        """
        self.endpoints = endpoints
        self.subdomain = subdomain
        VapiStruct.__init__(self)


SddcInstallerRequest._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sddc_installer_request', {
        'endpoints': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcHostSpec'))),
        'subdomain': type.OptionalType(type.StringType()),
    },
    SddcInstallerRequest,
    False,
    None))



class InstallerSpec(VapiStruct):
    """
    VCF Installer Installer Specification

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    TYPE_INTERNAL = "Internal"
    """
    Installer type

    """
    TYPE_EXTERNAL = "External"
    """
    Installer type

    """
    TYPE_INTERNAL_EXTERNAL = "Internal, External"
    """
    Installer type

    """



    _canonical_to_pep_names = {
                            'applianceFqdn': 'appliance_fqdn',
                            'type': 'type',
                            }

    def __init__(self,
                 appliance_fqdn=None,
                 type=None,
                ):
        """
        :type  appliance_fqdn: :class:`str` or ``None``
        :param appliance_fqdn: Appliance FQDN
        :type  type: :class:`str` or ``None``
        :param type: Installer type
        """
        self.appliance_fqdn = appliance_fqdn
        self.type = type
        VapiStruct.__init__(self)


InstallerSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.installer_spec', {
        'applianceFqdn': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
    },
    InstallerSpec,
    False,
    None))



class TrustedCertificateSpec(VapiStruct):
    """
    This specification contains certificate & certificate usage

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'certificate': 'certificate',
                            'certificateUsageType': 'certificate_usage_type',
                            }

    def __init__(self,
                 certificate=None,
                 certificate_usage_type=None,
                ):
        """
        :type  certificate: :class:`str` or ``None``
        :param certificate: Certificate in PEM format
        :type  certificate_usage_type: :class:`str` or ``None``
        :param certificate_usage_type: Certificate usage
        """
        self.certificate = certificate
        self.certificate_usage_type = certificate_usage_type
        VapiStruct.__init__(self)


TrustedCertificateSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.trusted_certificate_spec', {
        'certificate': type.OptionalType(type.StringType()),
        'certificateUsageType': type.OptionalType(type.StringType()),
    },
    TrustedCertificateSpec,
    False,
    None))



class PageMetadata(VapiStruct):
    """
    Represents pageable elements pagination metadata

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'pageNumber': 'page_number',
                            'pageSize': 'page_size',
                            'totalElements': 'total_elements',
                            'totalPages': 'total_pages',
                            }

    def __init__(self,
                 page_number=None,
                 page_size=None,
                 total_elements=None,
                 total_pages=None,
                ):
        """
        :type  page_number: :class:`long` or ``None``
        :param page_number: Returns the current page number 
            
            * Property is read-only.
            
            
        :type  page_size: :class:`long` or ``None``
        :param page_size: Returns the number of elements in the current page 
            
            * Property is read-only.
            
            
        :type  total_elements: :class:`long` or ``None``
        :param total_elements: Returns the total number of elements 
            
            * Property is read-only.
            
            
        :type  total_pages: :class:`long` or ``None``
        :param total_pages: Returns the total number of pages 
            
            * Property is read-only.
            
            
        """
        self.page_number = page_number
        self.page_size = page_size
        self.total_elements = total_elements
        self.total_pages = total_pages
        VapiStruct.__init__(self)


PageMetadata._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_metadata', {
        'pageNumber': type.OptionalType(type.IntegerType()),
        'pageSize': type.OptionalType(type.IntegerType()),
        'totalElements': type.OptionalType(type.IntegerType()),
        'totalPages': type.OptionalType(type.IntegerType()),
    },
    PageMetadata,
    False,
    None))



class PageOfTrustedCertificate(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`TrustedCertificate` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfTrustedCertificate._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_trusted_certificate', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'TrustedCertificate'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfTrustedCertificate,
    False,
    None))



class TrustedCertificate(VapiStruct):
    """
    The Trusted Certificate details.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'alias': 'alias',
                            'certificate': 'certificate',
                            }

    def __init__(self,
                 alias=None,
                 certificate=None,
                ):
        """
        :type  alias: :class:`str` or ``None``
        :param alias: Certificate alias
        :type  certificate: :class:`str` or ``None``
        :param certificate: Certificate in PEM format
        """
        self.alias = alias
        self.certificate = certificate
        VapiStruct.__init__(self)


TrustedCertificate._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.trusted_certificate', {
        'alias': type.OptionalType(type.StringType()),
        'certificate': type.OptionalType(type.StringType()),
    },
    TrustedCertificate,
    False,
    None))



class BundleUploadSpec(VapiStruct):
    """
    Bundle Upload Specification

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'bundleFilePath': 'bundle_file_path',
                            'manifestFilePath': 'manifest_file_path',
                            'signatureFilePath': 'signature_file_path',
                            'compatibilitySetsFilePath': 'compatibility_sets_file_path',
                            'partnerExtensionSpec': 'partner_extension_spec',
                            }

    def __init__(self,
                 bundle_file_path=None,
                 manifest_file_path=None,
                 signature_file_path=None,
                 compatibility_sets_file_path=None,
                 partner_extension_spec=None,
                ):
        """
        :type  bundle_file_path: :class:`str` or ``None``
        :param bundle_file_path: Bundle Upload File Path
        :type  manifest_file_path: :class:`str` or ``None``
        :param manifest_file_path: Bundle Upload Manifest File Path
        :type  signature_file_path: :class:`str` or ``None``
        :param signature_file_path: Bundle Upload Signature File Path
        :type  compatibility_sets_file_path: :class:`str` or ``None``
        :param compatibility_sets_file_path: [Deprecated] Path to the software compatibility sets file
        :type  partner_extension_spec: :class:`PartnerExtensionSpec` or ``None``
        :param partner_extension_spec:         """
        self.bundle_file_path = bundle_file_path
        self.manifest_file_path = manifest_file_path
        self.signature_file_path = signature_file_path
        self.compatibility_sets_file_path = compatibility_sets_file_path
        self.partner_extension_spec = partner_extension_spec
        VapiStruct.__init__(self)


BundleUploadSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle_upload_spec', {
        'bundleFilePath': type.OptionalType(type.StringType()),
        'manifestFilePath': type.OptionalType(type.StringType()),
        'signatureFilePath': type.OptionalType(type.StringType()),
        'compatibilitySetsFilePath': type.OptionalType(type.StringType()),
        'partnerExtensionSpec': type.OptionalType(type.ReferenceType(__name__, 'PartnerExtensionSpec')),
    },
    BundleUploadSpec,
    False,
    None))



class PartnerExtensionSpec(VapiStruct):
    """
    Specification for partner extensions. This specification is used in the
    Bundle Upload API

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'partnerBundleVersion': 'partner_bundle_version',
                            'partnerBundleMetadataFilePath': 'partner_bundle_metadata_file_path',
                            }

    def __init__(self,
                 partner_bundle_version=None,
                 partner_bundle_metadata_file_path=None,
                ):
        """
        :type  partner_bundle_version: :class:`str` or ``None``
        :param partner_bundle_version: Version of partner bundle to be uploaded. Should match one of the
            bundle versions available in the partner bundle metadata file
        :type  partner_bundle_metadata_file_path: :class:`str` or ``None``
        :param partner_bundle_metadata_file_path: Path to the bundle metadata file. The metadata file can have
            details of multiple bundles
        """
        self.partner_bundle_version = partner_bundle_version
        self.partner_bundle_metadata_file_path = partner_bundle_metadata_file_path
        VapiStruct.__init__(self)


PartnerExtensionSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.partner_extension_spec', {
        'partnerBundleVersion': type.OptionalType(type.StringType()),
        'partnerBundleMetadataFilePath': type.OptionalType(type.StringType()),
    },
    PartnerExtensionSpec,
    False,
    None))



class DocumentationLink(VapiStruct):
    """
    Represents a documentation link's url string and label

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'url': 'url',
                            'label': 'label',
                            }

    def __init__(self,
                 url=None,
                 label=None,
                ):
        """
        :type  url: :class:`str` or ``None``
        :param url: URL string of the documentation link 
            
            * Property is read-only.
            
            
        :type  label: :class:`str` or ``None``
        :param label: Label of the documentation link 
            
            * Property is read-only.
            
            
        """
        self.url = url
        self.label = label
        VapiStruct.__init__(self)


DocumentationLink._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.documentation_link', {
        'url': type.OptionalType(type.StringType()),
        'label': type.OptionalType(type.StringType()),
    },
    DocumentationLink,
    False,
    None))



class Resource(VapiStruct):
    """
    Represents the resource in the system

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'resourceId': 'resource_id',
                            'fqdn': 'fqdn',
                            'type': 'type',
                            'name': 'name',
                            'sans': 'sans',
                            }

    def __init__(self,
                 resource_id=None,
                 fqdn=None,
                 type=None,
                 name=None,
                 sans=None,
                ):
        """
        :type  resource_id: :class:`str` or ``None``
        :param resource_id: Resource ID
        :type  fqdn: :class:`str` or ``None``
        :param fqdn: Resource FQDN
        :type  type: :class:`str` or ``None``
        :param type: Resource type
        :type  name: :class:`str` or ``None``
        :param name: Name of the resource
        :type  sans: :class:`list` of :class:`str` or ``None``
        :param sans: Subject alternative name(s)
        """
        self.resource_id = resource_id
        self.fqdn = fqdn
        self.type = type
        self.name = name
        self.sans = sans
        VapiStruct.__init__(self)


Resource._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.resource', {
        'resourceId': type.OptionalType(type.StringType()),
        'fqdn': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'sans': type.OptionalType(type.ListType(type.StringType())),
    },
    Resource,
    False,
    None))



class Stage(VapiStruct):
    """
    Represents a Stage

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'type': 'type',
                            'description': 'description',
                            'status': 'status',
                            'creationTimestamp': 'creation_timestamp',
                            'completionTimestamp': 'completion_timestamp',
                            'errors': 'errors',
                            }

    def __init__(self,
                 name=None,
                 type=None,
                 description=None,
                 status=None,
                 creation_timestamp=None,
                 completion_timestamp=None,
                 errors=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Stage name 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Stage type 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Stage description 
            
            * Property is read-only.
            
            
        :type  status: :class:`str` or ``None``
        :param status: Stage status 
            
            * Property is read-only.
            
            
        :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp:         :type  completion_timestamp: :class:`str` or ``None``
        :param completion_timestamp: Stage completion timestamp 
            
            * Property is read-only.
            
            
        :type  errors: :class:`list` of :class:`Error` or ``None``
        :param errors: List of errors in case of a failure 
            
            * Property is read-only.
            
            
        """
        self.name = name
        self.type = type
        self.description = description
        self.status = status
        self.creation_timestamp = creation_timestamp
        self.completion_timestamp = completion_timestamp
        self.errors = errors
        VapiStruct.__init__(self)


Stage._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.stage', {
        'name': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'completionTimestamp': type.OptionalType(type.StringType()),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Error'))),
    },
    Stage,
    False,
    None))



class SubTask(VapiStruct):
    """
    Represents a sub-task

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'type': 'type',
                            'description': 'description',
                            'status': 'status',
                            'creationTimestamp': 'creation_timestamp',
                            'completionTimestamp': 'completion_timestamp',
                            'stages': 'stages',
                            'errors': 'errors',
                            'resources': 'resources',
                            'subTasks': 'sub_tasks',
                            'documentationLink': 'documentation_link',
                            }

    def __init__(self,
                 name=None,
                 type=None,
                 description=None,
                 status=None,
                 creation_timestamp=None,
                 completion_timestamp=None,
                 stages=None,
                 errors=None,
                 resources=None,
                 sub_tasks=None,
                 documentation_link=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Sub-task name 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Sub-task type 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Sub-task description 
            
            * Property is read-only.
            
            
        :type  status: :class:`str` or ``None``
        :param status: Sub-task status 
            
            * Property is read-only.
            
            
        :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp: Sub-task creation timestamp 
            
            * Property is read-only.
            
            
        :type  completion_timestamp: :class:`str` or ``None``
        :param completion_timestamp: Sub-task completion timestamp 
            
            * Property is read-only.
            
            
        :type  stages: :class:`list` of :class:`Stage` or ``None``
        :param stages: List of stages of the sub-task 
            
            * Property is read-only.
            
            
        :type  errors: :class:`list` of :class:`Error` or ``None``
        :param errors: List of errors in case of a failure 
            
            * Property is read-only.
            
            
        :type  resources: :class:`list` of :class:`Resource` or ``None``
        :param resources: List of resources associated with sub-task 
            
            * Property is read-only.
            
            
        :type  sub_tasks: :class:`list` of :class:`SubTask` or ``None``
        :param sub_tasks: List of child subtasks associated with this subtask 
            
            * Property is read-only.
            
            
        :type  documentation_link: :class:`DocumentationLink` or ``None``
        :param documentation_link:         """
        self.name = name
        self.type = type
        self.description = description
        self.status = status
        self.creation_timestamp = creation_timestamp
        self.completion_timestamp = completion_timestamp
        self.stages = stages
        self.errors = errors
        self.resources = resources
        self.sub_tasks = sub_tasks
        self.documentation_link = documentation_link
        VapiStruct.__init__(self)


SubTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sub_task', {
        'name': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'completionTimestamp': type.OptionalType(type.StringType()),
        'stages': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Stage'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Error'))),
        'resources': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Resource'))),
        'subTasks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SubTask'))),
        'documentationLink': type.OptionalType(type.ReferenceType(__name__, 'DocumentationLink')),
    },
    SubTask,
    False,
    None))



class Task(VapiStruct):
    """
    Represents a task

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'localizableDescriptionPack': 'localizable_description_pack',
                            'type': 'type',
                            'status': 'status',
                            'creationTimestamp': 'creation_timestamp',
                            'completionTimestamp': 'completion_timestamp',
                            'subTasks': 'sub_tasks',
                            'errors': 'errors',
                            'resources': 'resources',
                            'resolutionStatus': 'resolution_status',
                            'isCancellable': 'is_cancellable',
                            'isRetryable': 'is_retryable',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 localizable_description_pack=None,
                 type=None,
                 status=None,
                 creation_timestamp=None,
                 completion_timestamp=None,
                 sub_tasks=None,
                 errors=None,
                 resources=None,
                 resolution_status=None,
                 is_cancellable=None,
                 is_retryable=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Task ID 
            
            * Property is read-only.
            
            
        :type  name: :class:`str` or ``None``
        :param name: Task name 
            
            * Property is read-only.
            
            
        :type  localizable_description_pack: :class:`MessagePack` or ``None``
        :param localizable_description_pack:         :type  type: :class:`str` or ``None``
        :param type: Operation that is represented by the Task in machine readable
            format. The value is controlled by the owners/producers of the
            Task. The convention is <resource> _ <operation> <ul> <li>Property
            is read-only.</li> </ul> </operation> </resource>
        :type  status: :class:`str` or ``None``
        :param status: Task status 
            
            * Property is read-only.
            
            
        :type  creation_timestamp: :class:`str` or ``None``
        :param creation_timestamp: Task creation timestamp 
            
            * Property is read-only.
            
            
        :type  completion_timestamp: :class:`str` or ``None``
        :param completion_timestamp: Task completion timestamp 
            
            * Property is read-only.
            
            
        :type  sub_tasks: :class:`list` of :class:`SubTask` or ``None``
        :param sub_tasks: List of sub-tasks of the task 
            
            * Property is read-only.
            
            
        :type  errors: :class:`list` of :class:`Error` or ``None``
        :param errors: List of errors in case of a failure 
            
            * Property is read-only.
            
            
        :type  resources: :class:`list` of :class:`Resource` or ``None``
        :param resources: List of resources associated with task 
            
            * Property is read-only.
            
            
        :type  resolution_status: :class:`str` or ``None``
        :param resolution_status: Resolution state 
            
            * Property is read-only.
            
            
        :type  is_cancellable: :class:`bool` or ``None``
        :param is_cancellable: Represents task can be cancellable or not. 
            
            * Property is read-only.
            
            
        :type  is_retryable: :class:`bool` or ``None``
        :param is_retryable: Indicates whether a task is eligible for retry or not. 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.name = name
        self.localizable_description_pack = localizable_description_pack
        self.type = type
        self.status = status
        self.creation_timestamp = creation_timestamp
        self.completion_timestamp = completion_timestamp
        self.sub_tasks = sub_tasks
        self.errors = errors
        self.resources = resources
        self.resolution_status = resolution_status
        self.is_cancellable = is_cancellable
        self.is_retryable = is_retryable
        VapiStruct.__init__(self)


Task._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.task', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'localizableDescriptionPack': type.OptionalType(type.ReferenceType(__name__, 'MessagePack')),
        'type': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
        'creationTimestamp': type.OptionalType(type.StringType()),
        'completionTimestamp': type.OptionalType(type.StringType()),
        'subTasks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SubTask'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Error'))),
        'resources': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Resource'))),
        'resolutionStatus': type.OptionalType(type.StringType()),
        'isCancellable': type.OptionalType(type.BooleanType()),
        'isRetryable': type.OptionalType(type.BooleanType()),
    },
    Task,
    False,
    None))



class SystemUpdateSpec(VapiStruct):
    """
    Contains the parameters required to perform update operation on system

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'maxAllowedDomainsInSubscription': 'max_allowed_domains_in_subscription',
                            }

    def __init__(self,
                 max_allowed_domains_in_subscription=None,
                ):
        """
        :type  max_allowed_domains_in_subscription: :class:`long` or ``None``
        :param max_allowed_domains_in_subscription: new limit of amount of domains in subscription mode
        """
        self.max_allowed_domains_in_subscription = max_allowed_domains_in_subscription
        VapiStruct.__init__(self)


SystemUpdateSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.system_update_spec', {
        'maxAllowedDomainsInSubscription': type.OptionalType(type.IntegerType()),
    },
    SystemUpdateSpec,
    False,
    None))



class DepotSyncInfo(VapiStruct):
    """
    Depot Sync Information

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'syncStatus': 'sync_status',
                            'errorMessage': 'error_message',
                            'lastSyncCompletionTimestamp': 'last_sync_completion_timestamp',
                            }

    def __init__(self,
                 sync_status=None,
                 error_message=None,
                 last_sync_completion_timestamp=None,
                ):
        """
        :type  sync_status: :class:`str` or ``None``
        :param sync_status: Depot sync status 
            
            * Property is read-only.
            
            
        :type  error_message: :class:`str` or ``None``
        :param error_message: Depot sync error message 
            
            * Property is read-only.
            
            
        :type  last_sync_completion_timestamp: :class:`str` or ``None``
        :param last_sync_completion_timestamp: The completion timestamp of the last sync operation 
            
            * Property is read-only.
            
            
        """
        self.sync_status = sync_status
        self.error_message = error_message
        self.last_sync_completion_timestamp = last_sync_completion_timestamp
        VapiStruct.__init__(self)


DepotSyncInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.depot_sync_info', {
        'syncStatus': type.OptionalType(type.StringType()),
        'errorMessage': type.OptionalType(type.StringType()),
        'lastSyncCompletionTimestamp': type.OptionalType(type.StringType()),
    },
    DepotSyncInfo,
    False,
    None))



class ProxyConfiguration(VapiStruct):
    """
    Proxy Configuration

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """
    TRANSFER_PROTOCOL_HTTP = "HTTP"
    """
    Proxy transfer protocol, default value is HTTP

    """
    TRANSFER_PROTOCOL_HTTPS = "HTTPS"
    """
    Proxy transfer protocol, default value is HTTP

    """



    _canonical_to_pep_names = {
                            'isConfigured': 'is_configured',
                            'isEnabled': 'is_enabled',
                            'host': 'host',
                            'port': 'port',
                            'transferProtocol': 'transfer_protocol',
                            'username': 'username',
                            'password': 'password',
                            'isAuthenticated': 'is_authenticated',
                            }

    def __init__(self,
                 is_configured=None,
                 is_enabled=None,
                 host=None,
                 port=None,
                 transfer_protocol=None,
                 username=None,
                 password=None,
                 is_authenticated=None,
                ):
        """
        :type  is_configured: :class:`bool` or ``None``
        :param is_configured: Defines if the proxy is configured. 
            
            * Property is read-only.
            
            
        :type  is_enabled: :class:`bool` or ``None``
        :param is_enabled: Defines if the proxy configuration is enabled. To disable the
            proxy, this should be set to false.
        :type  host: :class:`str` or ``None``
        :param host: IP address/FQDN of proxy server. This must be set if proxy is
            enabled.
        :type  port: :class:`long` or ``None``
        :param port: Port of proxy server. This must be set if proxy is enabled.
        :type  transfer_protocol: :class:`str` or ``None``
        :param transfer_protocol: Proxy transfer protocol, default value is HTTP
        :type  username: :class:`str` or ``None``
        :param username: User name to connect
        :type  password: :class:`str` or ``None``
        :param password: User password to connect, will return null on reading
        :type  is_authenticated: :class:`bool` or ``None``
        :param is_authenticated: If proxy authentication is required, isAuthenticated must be
            enabled and username and password should be set.
        """
        self.is_configured = is_configured
        self.is_enabled = is_enabled
        self.host = host
        self.port = port
        self.transfer_protocol = transfer_protocol
        self.username = username
        self.password = password
        self.is_authenticated = is_authenticated
        VapiStruct.__init__(self)


ProxyConfiguration._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.proxy_configuration', {
        'isConfigured': type.OptionalType(type.BooleanType()),
        'isEnabled': type.OptionalType(type.BooleanType()),
        'host': type.OptionalType(type.StringType()),
        'port': type.OptionalType(type.IntegerType()),
        'transferProtocol': type.OptionalType(type.StringType()),
        'username': type.OptionalType(type.StringType()),
        'password': type.OptionalType(type.StringType()),
        'isAuthenticated': type.OptionalType(type.BooleanType()),
    },
    ProxyConfiguration,
    False,
    None))



class BundleDownloadSpec(VapiStruct):
    """
    Bundle Download Specification. This specification gets used in the Bundle
    Download API

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'scheduledTimestamp': 'scheduled_timestamp',
                            'downloadNow': 'download_now',
                            'cancelNow': 'cancel_now',
                            }

    def __init__(self,
                 scheduled_timestamp=None,
                 download_now=None,
                 cancel_now=None,
                ):
        """
        :type  scheduled_timestamp: :class:`str` or ``None``
        :param scheduled_timestamp: Bundle Download Scheduled Time
        :type  download_now: :class:`bool` or ``None``
        :param download_now: Flag for enabling Download Now. If true, scheduledTimestamp is
            ignored
        :type  cancel_now: :class:`bool` or ``None``
        :param cancel_now: Flag for cancelling the download. If true,
            scheduledTimestamp/downloadNow is ignored
        """
        self.scheduled_timestamp = scheduled_timestamp
        self.download_now = download_now
        self.cancel_now = cancel_now
        VapiStruct.__init__(self)


BundleDownloadSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle_download_spec', {
        'scheduledTimestamp': type.OptionalType(type.StringType()),
        'downloadNow': type.OptionalType(type.BooleanType()),
        'cancelNow': type.OptionalType(type.BooleanType()),
    },
    BundleDownloadSpec,
    False,
    None))



class BundleUpdateSpec(VapiStruct):
    """
    Bundle Update Specification

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'bundleDownloadSpec': 'bundle_download_spec',
                            }

    def __init__(self,
                 bundle_download_spec=None,
                ):
        """
        :type  bundle_download_spec: :class:`BundleDownloadSpec` or ``None``
        :param bundle_download_spec:         """
        self.bundle_download_spec = bundle_download_spec
        VapiStruct.__init__(self)


BundleUpdateSpec._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle_update_spec', {
        'bundleDownloadSpec': type.OptionalType(type.ReferenceType(__name__, 'BundleDownloadSpec')),
    },
    BundleUpdateSpec,
    False,
    None))



class PageOfVcfService(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`VcfService` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfVcfService._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_vcf_service', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcfService'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfVcfService,
    False,
    None))



class VcfService(VapiStruct):
    """
    VCF service representation

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'name': 'name',
                            'version': 'version',
                            'status': 'status',
                            }

    def __init__(self,
                 id=None,
                 name=None,
                 version=None,
                 status=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: ID of the service
        :type  name: :class:`str` or ``None``
        :param name: Name of the service
        :type  version: :class:`str` or ``None``
        :param version: Version of the service
        :type  status: :class:`str` or ``None``
        :param status: Status of the service
        """
        self.id = id
        self.name = name
        self.version = version
        self.status = status
        VapiStruct.__init__(self)


VcfService._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_service', {
        'id': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'status': type.OptionalType(type.StringType()),
    },
    VcfService,
    False,
    None))



class PageOfTask(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`Task` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_task', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Task'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfTask,
    False,
    None))



class System(VapiStruct):
    """
    Represents a system

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'maxAllowedDomainsInSubscription': 'max_allowed_domains_in_subscription',
                            }

    def __init__(self,
                 id=None,
                 max_allowed_domains_in_subscription=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: The identifier of the system 
            
            * Property is read-only.
            
            
        :type  max_allowed_domains_in_subscription: :class:`long` or ``None``
        :param max_allowed_domains_in_subscription: The maximum number of domains allowed in subscription mode 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.max_allowed_domains_in_subscription = max_allowed_domains_in_subscription
        VapiStruct.__init__(self)


System._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.system', {
        'id': type.OptionalType(type.StringType()),
        'maxAllowedDomainsInSubscription': type.OptionalType(type.IntegerType()),
    },
    System,
    False,
    None))



class VcfAutomation(VapiStruct):
    """
    VCF Automation

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'fqdn': 'fqdn',
                            'deploymentStatus': 'deployment_status',
                            'deploymentType': 'deployment_type',
                            }

    def __init__(self,
                 fqdn=None,
                 deployment_status=None,
                 deployment_type=None,
                ):
        """
        :type  fqdn: :class:`str` or ``None``
        :param fqdn: FQDN 
            
            * Property is read-only.
            
            
        :type  deployment_status: :class:`str` or ``None``
        :param deployment_status: VCF Automation deployment status. One among: NOT_FOUND,
            NOT_STARTED, IN_PROGRESS, FAILED, SUCCEEDED 
            
            * Property is read-only.
            
            
        :type  deployment_type: :class:`str` or ``None``
        :param deployment_type: VCF Automation deployment type. One among: NEW, EXISTING 
            
            * Property is read-only.
            
            
        """
        self.fqdn = fqdn
        self.deployment_status = deployment_status
        self.deployment_type = deployment_type
        VapiStruct.__init__(self)


VcfAutomation._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_automation', {
        'fqdn': type.OptionalType(type.StringType()),
        'deploymentStatus': type.OptionalType(type.StringType()),
        'deploymentType': type.OptionalType(type.StringType()),
    },
    VcfAutomation,
    False,
    None))



class VcfManagementComponents(VapiStruct):
    """
    VCF Management Components

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'vcfOperationsFleetManagement': 'vcf_operations_fleet_management',
                            'vcfOperations': 'vcf_operations',
                            'vcfOperationsCollector': 'vcf_operations_collector',
                            'vcfAutomation': 'vcf_automation',
                            }

    def __init__(self,
                 vcf_operations_fleet_management=None,
                 vcf_operations=None,
                 vcf_operations_collector=None,
                 vcf_automation=None,
                ):
        """
        :type  vcf_operations_fleet_management: :class:`VcfOperationsFleetManagement` or ``None``
        :param vcf_operations_fleet_management:         :type  vcf_operations: :class:`VcfOperations` or ``None``
        :param vcf_operations:         :type  vcf_operations_collector: :class:`VcfOperationsCollector` or ``None``
        :param vcf_operations_collector:         :type  vcf_automation: :class:`VcfAutomation` or ``None``
        :param vcf_automation:         """
        self.vcf_operations_fleet_management = vcf_operations_fleet_management
        self.vcf_operations = vcf_operations
        self.vcf_operations_collector = vcf_operations_collector
        self.vcf_automation = vcf_automation
        VapiStruct.__init__(self)


VcfManagementComponents._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_management_components', {
        'vcfOperationsFleetManagement': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsFleetManagement')),
        'vcfOperations': type.OptionalType(type.ReferenceType(__name__, 'VcfOperations')),
        'vcfOperationsCollector': type.OptionalType(type.ReferenceType(__name__, 'VcfOperationsCollector')),
        'vcfAutomation': type.OptionalType(type.ReferenceType(__name__, 'VcfAutomation')),
    },
    VcfManagementComponents,
    False,
    None))



class VcfOperations(VapiStruct):
    """
    VCF Operations

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'nodes': 'nodes',
                            'loadBalancerFqdn': 'load_balancer_fqdn',
                            'deploymentStatus': 'deployment_status',
                            'deploymentType': 'deployment_type',
                            }

    def __init__(self,
                 nodes=None,
                 load_balancer_fqdn=None,
                 deployment_status=None,
                 deployment_type=None,
                ):
        """
        :type  nodes: :class:`list` of :class:`VcfOperationsNodeDetails` or ``None``
        :param nodes: List of nodes 
            
            * Property is read-only.
            
            
        :type  load_balancer_fqdn: :class:`str` or ``None``
        :param load_balancer_fqdn: Load Balancer FQDN 
            
            * Property is read-only.
            
            
        :type  deployment_status: :class:`str` or ``None``
        :param deployment_status: VCF Operations deployment status. One among: NOT_FOUND,
            NOT_STARTED, IN_PROGRESS, FAILED, SUCCEEDED 
            
            * Property is read-only.
            
            
        :type  deployment_type: :class:`str` or ``None``
        :param deployment_type: VCF Operations deployment type. One among: NEW, EXISTING 
            
            * Property is read-only.
            
            
        """
        self.nodes = nodes
        self.load_balancer_fqdn = load_balancer_fqdn
        self.deployment_status = deployment_status
        self.deployment_type = deployment_type
        VapiStruct.__init__(self)


VcfOperations._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations', {
        'nodes': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VcfOperationsNodeDetails'))),
        'loadBalancerFqdn': type.OptionalType(type.StringType()),
        'deploymentStatus': type.OptionalType(type.StringType()),
        'deploymentType': type.OptionalType(type.StringType()),
    },
    VcfOperations,
    False,
    None))



class VcfOperationsCollector(VapiStruct):
    """
    VCF Operations collector

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'fqdn': 'fqdn',
                            'deploymentStatus': 'deployment_status',
                            'deploymentType': 'deployment_type',
                            }

    def __init__(self,
                 fqdn=None,
                 deployment_status=None,
                 deployment_type=None,
                ):
        """
        :type  fqdn: :class:`str` or ``None``
        :param fqdn: FQDN 
            
            * Property is read-only.
            
            
        :type  deployment_status: :class:`str` or ``None``
        :param deployment_status: VCF Operations collector deployment status. One among: NOT_FOUND,
            NOT_STARTED, IN_PROGRESS, FAILED, SUCCEEDED 
            
            * Property is read-only.
            
            
        :type  deployment_type: :class:`str` or ``None``
        :param deployment_type: VCF Operations collector deployment type. Only valid value is: NEW 
            
            * Property is read-only.
            
            
        """
        self.fqdn = fqdn
        self.deployment_status = deployment_status
        self.deployment_type = deployment_type
        VapiStruct.__init__(self)


VcfOperationsCollector._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_collector', {
        'fqdn': type.OptionalType(type.StringType()),
        'deploymentStatus': type.OptionalType(type.StringType()),
        'deploymentType': type.OptionalType(type.StringType()),
    },
    VcfOperationsCollector,
    False,
    None))



class VcfOperationsFleetManagement(VapiStruct):
    """
    VCF Operations fleet management

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'fqdn': 'fqdn',
                            'deploymentStatus': 'deployment_status',
                            'deploymentType': 'deployment_type',
                            }

    def __init__(self,
                 fqdn=None,
                 deployment_status=None,
                 deployment_type=None,
                ):
        """
        :type  fqdn: :class:`str` or ``None``
        :param fqdn: FQDN 
            
            * Property is read-only.
            
            
        :type  deployment_status: :class:`str` or ``None``
        :param deployment_status: VCF Operations fleet management deployment status. One among:
            NOT_FOUND, NOT_STARTED, IN_PROGRESS, FAILED, SUCCEEDED 
            
            * Property is read-only.
            
            
        :type  deployment_type: :class:`str` or ``None``
        :param deployment_type: VCF Operations fleet management deployment type. One among: NEW,
            EXISTING 
            
            * Property is read-only.
            
            
        """
        self.fqdn = fqdn
        self.deployment_status = deployment_status
        self.deployment_type = deployment_type
        VapiStruct.__init__(self)


VcfOperationsFleetManagement._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_fleet_management', {
        'fqdn': type.OptionalType(type.StringType()),
        'deploymentStatus': type.OptionalType(type.StringType()),
        'deploymentType': type.OptionalType(type.StringType()),
    },
    VcfOperationsFleetManagement,
    False,
    None))



class VcfOperationsNodeDetails(VapiStruct):
    """
    VCF Operations node details

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'fqdn': 'fqdn',
                            'type': 'type',
                            }

    def __init__(self,
                 fqdn=None,
                 type=None,
                ):
        """
        :type  fqdn: :class:`str` or ``None``
        :param fqdn: FQDN 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Node type. One among: master, replica, data 
            
            * Property is read-only.
            
            
        """
        self.fqdn = fqdn
        self.type = type
        VapiStruct.__init__(self)


VcfOperationsNodeDetails._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.vcf_operations_node_details', {
        'fqdn': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
    },
    VcfOperationsNodeDetails,
    False,
    None))



class Ceip(VapiStruct):
    """
    Defines VCF CEIP status and instance id

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'status': 'status',
                            'instanceId': 'instance_id',
                            }

    def __init__(self,
                 status=None,
                 instance_id=None,
                ):
        """
        :type  status: :class:`str` or ``None``
        :param status: CEIP status
        :type  instance_id: :class:`str` or ``None``
        :param instance_id: Instance Id of VCF 
            
            * Property is read-only.
            
            
        """
        self.status = status
        self.instance_id = instance_id
        VapiStruct.__init__(self)


Ceip._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.ceip', {
        'status': type.OptionalType(type.StringType()),
        'instanceId': type.OptionalType(type.StringType()),
    },
    Ceip,
    False,
    None))



class ApplianceInfo(VapiStruct):
    """
    Appliance Information

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'role': 'role',
                            'version': 'version',
                            }

    def __init__(self,
                 role=None,
                 version=None,
                ):
        """
        :type  role: :class:`str` or ``None``
        :param role: Appliance Role
        :type  version: :class:`str` or ``None``
        :param version: Appliance version
        """
        self.role = role
        self.version = version
        VapiStruct.__init__(self)


ApplianceInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.appliance_info', {
        'role': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
    },
    ApplianceInfo,
    False,
    None))



class PageOfSddcTask(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`SddcTask` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfSddcTask._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_sddc_task', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SddcTask'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfSddcTask,
    False,
    None))



class PageOfValidation(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`Validation` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfValidation._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_validation', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Validation'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfValidation,
    False,
    None))



class PageOfRelease(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`Release` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfRelease._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_release', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Release'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfRelease,
    False,
    None))



class PatchBundle(VapiStruct):
    """
    Model for patch bundle in a release

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'bundleId': 'bundle_id',
                            'bundleType': 'bundle_type',
                            'bundleElements': 'bundle_elements',
                            'cumulativeFromVcfVersion': 'cumulative_from_vcf_version',
                            }

    def __init__(self,
                 bundle_id=None,
                 bundle_type=None,
                 bundle_elements=None,
                 cumulative_from_vcf_version=None,
                ):
        """
        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: Bundle ID of the patch bundle 
            
            * Property is read-only.
            
            
        :type  bundle_type: :class:`str` or ``None``
        :param bundle_type: Bundle type of the patch bundle 
            
            * Property is read-only.
            
            
        :type  bundle_elements: :class:`list` of :class:`str` or ``None``
        :param bundle_elements: Bundle elements of the patch bundle 
            
            * Property is read-only.
            
            
        :type  cumulative_from_vcf_version: :class:`str` or ``None``
        :param cumulative_from_vcf_version: Minimum VCF version that this patch bundle can be directly applied
            on 
            
            * Property is read-only.
            
            
        """
        self.bundle_id = bundle_id
        self.bundle_type = bundle_type
        self.bundle_elements = bundle_elements
        self.cumulative_from_vcf_version = cumulative_from_vcf_version
        VapiStruct.__init__(self)


PatchBundle._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.patch_bundle', {
        'bundleId': type.OptionalType(type.StringType()),
        'bundleType': type.OptionalType(type.StringType()),
        'bundleElements': type.OptionalType(type.ListType(type.StringType())),
        'cumulativeFromVcfVersion': type.OptionalType(type.StringType()),
    },
    PatchBundle,
    False,
    None))



class ProductVersion(VapiStruct):
    """
    Details of the product/component for the release.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'version': 'version',
                            'changeId': 'change_id',
                            'publicName': 'public_name',
                            'releaseURL': 'release_url',
                            'additionalMetadata': 'additional_metadata',
                            'automatedInstall': 'automated_install',
                            'lifecycleManagedBy': 'lifecycle_managed_by',
                            }

    def __init__(self,
                 name=None,
                 version=None,
                 change_id=None,
                 public_name=None,
                 release_url=None,
                 additional_metadata=None,
                 automated_install=None,
                 lifecycle_managed_by=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Name of the product. e.g ESX 
            
            * Property is read-only.
            
            
        :type  version: :class:`str` or ``None``
        :param version: Version for the product, e.g 6.7.0-11675023 
            
            * Property is read-only.
            
            
        :type  change_id: :class:`str` or ``None``
        :param change_id: Build or CLN for the product, e.g 11675023 
            
            * Property is read-only.
            
            
        :type  public_name: :class:`str` or ``None``
        :param public_name: Public name of the product, e.g VMware ESXi 
            
            * Property is read-only.
            
            
        :type  release_url: :class:`str` or ``None``
        :param release_url: URL for the release. 
            
            * Property is read-only.
            
            
        :type  additional_metadata: :class:`str` or ``None``
        :param additional_metadata: any additional metadata 
            
            * Property is read-only.
            
            
        :type  automated_install: :class:`bool` or ``None``
        :param automated_install: Automated install or not, e.g. true 
            
            * Property is read-only.
            
            
        :type  lifecycle_managed_by: :class:`str` or ``None``
        :param lifecycle_managed_by: Lifecycle is managed by whom, e.g. SDDC_MANAGER_VCF 
            
            * Property is read-only.
            
            
        """
        self.name = name
        self.version = version
        self.change_id = change_id
        self.public_name = public_name
        self.release_url = release_url
        self.additional_metadata = additional_metadata
        self.automated_install = automated_install
        self.lifecycle_managed_by = lifecycle_managed_by
        VapiStruct.__init__(self)


ProductVersion._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.product_version', {
        'name': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'changeId': type.OptionalType(type.StringType()),
        'publicName': type.OptionalType(type.StringType()),
        'releaseURL': type.OptionalType(type.StringType()),
        'additionalMetadata': type.OptionalType(type.StringType()),
        'automatedInstall': type.OptionalType(type.BooleanType()),
        'lifecycleManagedBy': type.OptionalType(type.StringType()),
    },
    ProductVersion,
    False,
    None))



class Release(VapiStruct):
    """
    Model for releases with their description and product version

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'product': 'product',
                            'version': 'version',
                            'minCompatibleVcfVersion': 'min_compatible_vcf_version',
                            'description': 'description',
                            'releaseDate': 'release_date',
                            'bom': 'bom',
                            'isApplicable': 'is_applicable',
                            'notApplicableReason': 'not_applicable_reason',
                            'sku': 'sku',
                            'updates': 'updates',
                            'patchBundles': 'patch_bundles',
                            'eol': 'eol',
                            'upgradeOrder': 'upgrade_order',
                            'minInstallerVersion': 'min_installer_version',
                            }

    def __init__(self,
                 product=None,
                 version=None,
                 min_compatible_vcf_version=None,
                 description=None,
                 release_date=None,
                 bom=None,
                 is_applicable=None,
                 not_applicable_reason=None,
                 sku=None,
                 updates=None,
                 patch_bundles=None,
                 eol=None,
                 upgrade_order=None,
                 min_installer_version=None,
                ):
        """
        :type  product: :class:`str` or ``None``
        :param product: Name of the product e.g. "VCF" 
            
            * Property is read-only.
            
            
        :type  version: :class:`str` or ``None``
        :param version: Version of the release 
            
            * Property is read-only.
            
            
        :type  min_compatible_vcf_version: :class:`str` or ``None``
        :param min_compatible_vcf_version: Minimum compatible VCF version, used to represent compatibility of
            SDDC Manager and VMware BOM components 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Release description with all major features. 
            
            * Property is read-only.
            
            
        :type  release_date: :class:`str` or ``None``
        :param release_date: Release date e.g. 2020-06-08T02:20:15.844Z in
            yyyy-MM-dd'T'HH:mm:ss[.SSS]XXX ISO 8601 format 
            
            * Property is read-only.
            
            
        :type  bom: :class:`list` of :class:`ProductVersion` or ``None``
        :param bom: Release bill of materials 
            
            * Property is read-only.
            
            
        :type  is_applicable: :class:`bool` or ``None``
        :param is_applicable: [Deprecated] Whether bundle is applicable or not. 
            
            * Property is read-only.
            
            
        :type  not_applicable_reason: :class:`str` or ``None``
        :param not_applicable_reason: [Deprecated] Incompatibility reason for not applicable. 
            
            * Property is read-only.
            
            
        :type  sku: :class:`list` of :class:`SkuBomDetails` or ``None``
        :param sku: Release sku specific patch and bill of materials 
            
            * Property is read-only.
            
            
        :type  updates: :class:`list` of :class:`ReleaseUpdate` or ``None``
        :param updates: Collection of release updates 
            
            * Property is read-only.
            
            
        :type  patch_bundles: :class:`list` of :class:`PatchBundle` or ``None``
        :param patch_bundles: List of patch bundles in this release 
            
            * Property is read-only.
            
            
        :type  eol: :class:`str` or ``None``
        :param eol: Release eol information e.g. 2020-06-08T02:20:15.844Z in
            yyyy-MM-dd'T'HH:mm:ss[.SSS]XXX ISO 8601 format 
            
            * Property is read-only.
            
            
        :type  upgrade_order: :class:`str` or ``None``
        :param upgrade_order: Custom upgrade order. Comma separated list of components in upgrade
            order. Supported components types: NSX_T_MANAGER, VCENTER,
            ESX_HOST. 
            
            * Property is read-only.
            
            
        :type  min_installer_version: :class:`str` or ``None``
        :param min_installer_version: Minimum installer version, e.g. 9.0.0.0 
            
            * Property is read-only.
            
            
        """
        self.product = product
        self.version = version
        self.min_compatible_vcf_version = min_compatible_vcf_version
        self.description = description
        self.release_date = release_date
        self.bom = bom
        self.is_applicable = is_applicable
        self.not_applicable_reason = not_applicable_reason
        self.sku = sku
        self.updates = updates
        self.patch_bundles = patch_bundles
        self.eol = eol
        self.upgrade_order = upgrade_order
        self.min_installer_version = min_installer_version
        VapiStruct.__init__(self)


Release._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.release', {
        'product': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'minCompatibleVcfVersion': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'releaseDate': type.OptionalType(type.StringType()),
        'bom': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ProductVersion'))),
        'isApplicable': type.OptionalType(type.BooleanType()),
        'notApplicableReason': type.OptionalType(type.StringType()),
        'sku': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SkuBomDetails'))),
        'updates': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReleaseUpdate'))),
        'patchBundles': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'PatchBundle'))),
        'eol': type.OptionalType(type.StringType()),
        'upgradeOrder': type.OptionalType(type.StringType()),
        'minInstallerVersion': type.OptionalType(type.StringType()),
    },
    Release,
    False,
    None))



class ReleaseUpdate(VapiStruct):
    """
    Update to a given release

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'productName': 'product_name',
                            'baseProductVersion': 'base_product_version',
                            'description': 'description',
                            'releaseUpdateURL': 'release_update_url',
                            'releaseDate': 'release_date',
                            }

    def __init__(self,
                 id=None,
                 product_name=None,
                 base_product_version=None,
                 description=None,
                 release_update_url=None,
                 release_date=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Release version 
            
            * Property is read-only.
            
            
        :type  product_name: :class:`str` or ``None``
        :param product_name: Product name for which the release update is provided 
            
            * Property is read-only.
            
            
        :type  base_product_version: :class:`str` or ``None``
        :param base_product_version: Base product version for the release 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Description of the release update 
            
            * Property is read-only.
            
            
        :type  release_update_url: :class:`str` or ``None``
        :param release_update_url: URL to the release update 
            
            * Property is read-only.
            
            
        :type  release_date: :class:`str` or ``None``
        :param release_date: Release date e.g. 2020-06-08T02:20:15.844Z in
            yyyy-MM-dd'T'HH:mm:ss[.SSS]XXX ISO 8601 format 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.product_name = product_name
        self.base_product_version = base_product_version
        self.description = description
        self.release_update_url = release_update_url
        self.release_date = release_date
        VapiStruct.__init__(self)


ReleaseUpdate._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.release_update', {
        'id': type.OptionalType(type.StringType()),
        'productName': type.OptionalType(type.StringType()),
        'baseProductVersion': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'releaseUpdateURL': type.OptionalType(type.URIType()),
        'releaseDate': type.OptionalType(type.StringType()),
    },
    ReleaseUpdate,
    False,
    None))



class SkuBomDetails(VapiStruct):
    """
    Model for sku with their name, description, patchBundles and bom

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'description': 'description',
                            'skuSpecificPatchBundles': 'sku_specific_patch_bundles',
                            'bom': 'bom',
                            }

    def __init__(self,
                 name=None,
                 description=None,
                 sku_specific_patch_bundles=None,
                 bom=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: SKU name 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Description to be shown in release page 
            
            * Property is read-only.
            
            
        :type  sku_specific_patch_bundles: :class:`list` of :class:`SkuSpecificPatchBundles` or ``None``
        :param sku_specific_patch_bundles: List of patch bundles in this release 
            
            * Property is read-only.
            
            
        :type  bom: :class:`list` of :class:`ProductVersion` or ``None``
        :param bom: Sku specific bill of materials 
            
            * Property is read-only.
            
            
        """
        self.name = name
        self.description = description
        self.sku_specific_patch_bundles = sku_specific_patch_bundles
        self.bom = bom
        VapiStruct.__init__(self)


SkuBomDetails._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sku_bom_details', {
        'name': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'skuSpecificPatchBundles': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SkuSpecificPatchBundles'))),
        'bom': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ProductVersion'))),
    },
    SkuBomDetails,
    False,
    None))



class SkuSpecificPatchBundles(VapiStruct):
    """
    Model for Sku specific patch bundle in a release

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'bundleType': 'bundle_type',
                            'bundleVersion': 'bundle_version',
                            'version': 'version',
                            }

    def __init__(self,
                 bundle_type=None,
                 bundle_version=None,
                 version=None,
                ):
        """
        :type  bundle_type: :class:`str` or ``None``
        :param bundle_type: Bundle type of the patch bundle 
            
            * Property is read-only.
            
            
        :type  bundle_version: :class:`str` or ``None``
        :param bundle_version: Bundle Version of the product 
            
            * Property is read-only.
            
            
        :type  version: :class:`str` or ``None``
        :param version: Product version 
            
            * Property is read-only.
            
            
        """
        self.bundle_type = bundle_type
        self.bundle_version = bundle_version
        self.version = version
        VapiStruct.__init__(self)


SkuSpecificPatchBundles._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.sku_specific_patch_bundles', {
        'bundleType': type.OptionalType(type.StringType()),
        'bundleVersion': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
    },
    SkuSpecificPatchBundles,
    False,
    None))



class CustomPatch(VapiStruct):
    """
    Patch or Install info from Product Version Catalog.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'productVersion': 'product_version',
                            'date': 'date',
                            'artifacts': 'artifacts',
                            }

    def __init__(self,
                 product_version=None,
                 date=None,
                 artifacts=None,
                ):
        """
        :type  product_version: :class:`str` or ``None``
        :param product_version: Product version of the install/patch bundle 
            
            * Property is read-only.
            
            
        :type  date: :class:`str` or ``None``
        :param date: Time of publish of the product e.g. 2020-06-08T02:20:15.844Z 
            
            * Property is read-only.
            
            
        :type  artifacts: :class:`CustomPatchArtifact` or ``None``
        :param artifacts:         """
        self.product_version = product_version
        self.date = date
        self.artifacts = artifacts
        VapiStruct.__init__(self)


CustomPatch._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.custom_patch', {
        'productVersion': type.OptionalType(type.StringType()),
        'date': type.OptionalType(type.StringType()),
        'artifacts': type.OptionalType(type.ReferenceType(__name__, 'CustomPatchArtifact')),
    },
    CustomPatch,
    False,
    None))



class CustomPatchArtifact(VapiStruct):
    """
    Patch rest model that is located in the Product Version Catalog.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'bundles': 'bundles',
                            }

    def __init__(self,
                 bundles=None,
                ):
        """
        :type  bundles: :class:`list` of :class:`CustomPatchBundleInfo` or ``None``
        :param bundles: List of bundle artifacts for corresponding product patch/install
            version 
            
            * Property is read-only.
            
            
        """
        self.bundles = bundles
        VapiStruct.__init__(self)


CustomPatchArtifact._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.custom_patch_artifact', {
        'bundles': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'CustomPatchBundleInfo'))),
    },
    CustomPatchArtifact,
    False,
    None))



class CustomPatchBundleInfo(VapiStruct):
    """
    Patch/Install bundle info from ProductVersionCatalog.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'type': 'type',
                            'name': 'name',
                            'size': 'size',
                            }

    def __init__(self,
                 id=None,
                 type=None,
                 name=None,
                 size=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Bundle id 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Type of bundle. ex) PATCH, INSTALL 
            
            * Property is read-only.
            
            
        :type  name: :class:`str` or ``None``
        :param name: Patch/Install bundle name 
            
            * Property is read-only.
            
            
        :type  size: :class:`long` or ``None``
        :param size: Binary size 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.type = type
        self.name = name
        self.size = size
        VapiStruct.__init__(self)


CustomPatchBundleInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.custom_patch_bundle_info', {
        'id': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'name': type.OptionalType(type.StringType()),
        'size': type.OptionalType(type.IntegerType()),
    },
    CustomPatchBundleInfo,
    False,
    None))



class PageOfReleaseComponentDetail(VapiStruct):
    """
    Paginated response containing the list of release component detail.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`ReleaseComponentDetail` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfReleaseComponentDetail._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_release_component_detail', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReleaseComponentDetail'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfReleaseComponentDetail,
    False,
    None))



class ProductReleaseComponent(VapiStruct):
    """
    Product Release Component

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'name': 'name',
                            'sku': 'sku',
                            'publicName': 'public_name',
                            'automatedInstall': 'automated_install',
                            'versions': 'versions',
                            }

    def __init__(self,
                 name=None,
                 sku=None,
                 public_name=None,
                 automated_install=None,
                 versions=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Product name 
            
            * Property is read-only.
            
            
        :type  sku: :class:`str` or ``None``
        :param sku: SKU of the install/patch bundle 
            
            * Property is read-only.
            
            
        :type  public_name: :class:`str` or ``None``
        :param public_name: Product public name 
            
            * Property is read-only.
            
            
        :type  automated_install: :class:`bool` or ``None``
        :param automated_install: automated Install 
            
            * Property is read-only.
            
            
        :type  versions: :class:`list` of :class:`CustomPatch` or ``None``
        :param versions: Product version details 
            
            * Property is read-only.
            
            
        """
        self.name = name
        self.sku = sku
        self.public_name = public_name
        self.automated_install = automated_install
        self.versions = versions
        VapiStruct.__init__(self)


ProductReleaseComponent._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.product_release_component', {
        'name': type.OptionalType(type.StringType()),
        'sku': type.OptionalType(type.StringType()),
        'publicName': type.OptionalType(type.StringType()),
        'automatedInstall': type.OptionalType(type.BooleanType()),
        'versions': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'CustomPatch'))),
    },
    ProductReleaseComponent,
    False,
    None))



class ReleaseComponentDetail(VapiStruct):
    """
    Model for Release Component Detail

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'releaseVersion': 'release_version',
                            'components': 'components',
                            }

    def __init__(self,
                 release_version=None,
                 components=None,
                ):
        """
        :type  release_version: :class:`str` or ``None``
        :param release_version: VCF/VVF release version 
            
            * Property is read-only.
            
            
        :type  components: :class:`list` of :class:`ProductReleaseComponent` or ``None``
        :param components: VCF/VVF release elements 
            
            * Property is read-only.
            
            
        """
        self.release_version = release_version
        self.components = components
        VapiStruct.__init__(self)


ReleaseComponentDetail._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.release_component_detail', {
        'releaseVersion': type.OptionalType(type.StringType()),
        'components': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ProductReleaseComponent'))),
    },
    ReleaseComponentDetail,
    False,
    None))



class AlternativeApplicableSddcManagerVersion(VapiStruct):
    """
    Version of Target SDDC Manager

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'version': 'version',
                            }

    def __init__(self,
                 version=None,
                ):
        """
        :type  version: :class:`str` or ``None``
        :param version: Version of target SDDC manger 
            
            * Property is read-only.
            
            
        """
        self.version = version
        VapiStruct.__init__(self)


AlternativeApplicableSddcManagerVersion._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.alternative_applicable_sddc_manager_version', {
        'version': type.OptionalType(type.StringType()),
    },
    AlternativeApplicableSddcManagerVersion,
    False,
    None))



class DomainFutureRelease(VapiStruct):
    """
    Model for releases with details if applicable to current domain version or
    not.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'reasonNotApplicable': 'reason_not_applicable',
                            'reasonsNotApplicable': 'reasons_not_applicable',
                            'warnings': 'warnings',
                            'alternativeApplicableSddcManagerVersions': 'alternative_applicable_sddc_manager_versions',
                            'applicabilityStatus': 'applicability_status',
                            'product': 'product',
                            'version': 'version',
                            'minCompatibleVcfVersion': 'min_compatible_vcf_version',
                            'description': 'description',
                            'releaseDate': 'release_date',
                            'bom': 'bom',
                            'isApplicable': 'is_applicable',
                            'notApplicableReason': 'not_applicable_reason',
                            'sku': 'sku',
                            'updates': 'updates',
                            'patchBundles': 'patch_bundles',
                            'eol': 'eol',
                            'upgradeOrder': 'upgrade_order',
                            'minInstallerVersion': 'min_installer_version',
                            }

    def __init__(self,
                 reason_not_applicable=None,
                 reasons_not_applicable=None,
                 warnings=None,
                 alternative_applicable_sddc_manager_versions=None,
                 applicability_status=None,
                 product=None,
                 version=None,
                 min_compatible_vcf_version=None,
                 description=None,
                 release_date=None,
                 bom=None,
                 is_applicable=None,
                 not_applicable_reason=None,
                 sku=None,
                 updates=None,
                 patch_bundles=None,
                 eol=None,
                 upgrade_order=None,
                 min_installer_version=None,
                ):
        """
        :type  reason_not_applicable: :class:`MessagePack` or ``None``
        :param reason_not_applicable:         :type  reasons_not_applicable: :class:`list` of :class:`MessagePack` or ``None``
        :param reasons_not_applicable: List of Incompatibility details for not applicable 
            
            * Property is read-only.
            
            
        :type  warnings: :class:`list` of :class:`MessagePack` or ``None``
        :param warnings: List of warning messages for product compatibility 
            
            * Property is read-only.
            
            
        :type  alternative_applicable_sddc_manager_versions: :class:`list` of :class:`AlternativeApplicableSddcManagerVersion` or ``None``
        :param alternative_applicable_sddc_manager_versions: List of AlternativeApplicableSddcManagerVersions 
            
            * Property is read-only.
            
            
        :type  applicability_status: :class:`str` or ``None``
        :param applicability_status: Whether bundle is applicable or not. 
            
            * Property is read-only.
            
            
        :type  product: :class:`str` or ``None``
        :param product: Name of the product e.g. "VCF" 
            
            * Property is read-only.
            
            
        :type  version: :class:`str` or ``None``
        :param version: Version of the release 
            
            * Property is read-only.
            
            
        :type  min_compatible_vcf_version: :class:`str` or ``None``
        :param min_compatible_vcf_version: Minimum compatible VCF version, used to represent compatibility of
            SDDC Manager and VMware BOM components 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Release description with all major features. 
            
            * Property is read-only.
            
            
        :type  release_date: :class:`str` or ``None``
        :param release_date: Release date e.g. 2020-06-08T02:20:15.844Z in
            yyyy-MM-dd'T'HH:mm:ss[.SSS]XXX ISO 8601 format 
            
            * Property is read-only.
            
            
        :type  bom: :class:`list` of :class:`ProductVersion` or ``None``
        :param bom: Release bill of materials 
            
            * Property is read-only.
            
            
        :type  is_applicable: :class:`bool` or ``None``
        :param is_applicable: [Deprecated] Whether bundle is applicable or not. 
            
            * Property is read-only.
            
            
        :type  not_applicable_reason: :class:`str` or ``None``
        :param not_applicable_reason: [Deprecated] Incompatibility reason for not applicable. 
            
            * Property is read-only.
            
            
        :type  sku: :class:`list` of :class:`SkuBomDetails` or ``None``
        :param sku: Release sku specific patch and bill of materials 
            
            * Property is read-only.
            
            
        :type  updates: :class:`list` of :class:`ReleaseUpdate` or ``None``
        :param updates: Collection of release updates 
            
            * Property is read-only.
            
            
        :type  patch_bundles: :class:`list` of :class:`PatchBundle` or ``None``
        :param patch_bundles: List of patch bundles in this release 
            
            * Property is read-only.
            
            
        :type  eol: :class:`str` or ``None``
        :param eol: Release eol information e.g. 2020-06-08T02:20:15.844Z in
            yyyy-MM-dd'T'HH:mm:ss[.SSS]XXX ISO 8601 format 
            
            * Property is read-only.
            
            
        :type  upgrade_order: :class:`str` or ``None``
        :param upgrade_order: Custom upgrade order. Comma separated list of components in upgrade
            order. Supported components types: NSX_T_MANAGER, VCENTER,
            ESX_HOST. 
            
            * Property is read-only.
            
            
        :type  min_installer_version: :class:`str` or ``None``
        :param min_installer_version: Minimum installer version, e.g. 9.0.0.0 
            
            * Property is read-only.
            
            
        """
        self.reason_not_applicable = reason_not_applicable
        self.reasons_not_applicable = reasons_not_applicable
        self.warnings = warnings
        self.alternative_applicable_sddc_manager_versions = alternative_applicable_sddc_manager_versions
        self.applicability_status = applicability_status
        self.product = product
        self.version = version
        self.min_compatible_vcf_version = min_compatible_vcf_version
        self.description = description
        self.release_date = release_date
        self.bom = bom
        self.is_applicable = is_applicable
        self.not_applicable_reason = not_applicable_reason
        self.sku = sku
        self.updates = updates
        self.patch_bundles = patch_bundles
        self.eol = eol
        self.upgrade_order = upgrade_order
        self.min_installer_version = min_installer_version
        VapiStruct.__init__(self)


DomainFutureRelease._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.domain_future_release', {
        'reasonNotApplicable': type.OptionalType(type.ReferenceType(__name__, 'MessagePack')),
        'reasonsNotApplicable': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'MessagePack'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'MessagePack'))),
        'alternativeApplicableSddcManagerVersions': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'AlternativeApplicableSddcManagerVersion'))),
        'applicabilityStatus': type.OptionalType(type.StringType()),
        'product': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'minCompatibleVcfVersion': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'releaseDate': type.OptionalType(type.StringType()),
        'bom': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ProductVersion'))),
        'isApplicable': type.OptionalType(type.BooleanType()),
        'notApplicableReason': type.OptionalType(type.StringType()),
        'sku': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SkuBomDetails'))),
        'updates': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReleaseUpdate'))),
        'patchBundles': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'PatchBundle'))),
        'eol': type.OptionalType(type.StringType()),
        'upgradeOrder': type.OptionalType(type.StringType()),
        'minInstallerVersion': type.OptionalType(type.StringType()),
    },
    DomainFutureRelease,
    False,
    None))



class PageOfDomainFutureRelease(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`DomainFutureRelease` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfDomainFutureRelease._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_domain_future_release', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'DomainFutureRelease'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfDomainFutureRelease,
    False,
    None))



class FlexibleProductPatch(VapiStruct):
    """
    Model for product async/hot patches with their supported product versions

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'productType': 'product_type',
                            'versions': 'versions',
                            }

    def __init__(self,
                 product_type=None,
                 versions=None,
                ):
        """
        :type  product_type: :class:`str` or ``None``
        :param product_type: product type of patch 
            
            * Property is read-only.
            
            
        :type  versions: :class:`list` of :class:`str` or ``None``
        :param versions: supported versions of patch 
            
            * Property is read-only.
            
            
        """
        self.product_type = product_type
        self.versions = versions
        VapiStruct.__init__(self)


FlexibleProductPatch._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.flexible_product_patch', {
        'productType': type.OptionalType(type.StringType()),
        'versions': type.OptionalType(type.ListType(type.StringType())),
    },
    FlexibleProductPatch,
    False,
    None))



class FlexibleProductPatches(VapiStruct):
    """
    Model for supported product async/hot patches associated with a VCF release

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'version': 'version',
                            'patches': 'patches',
                            }

    def __init__(self,
                 version=None,
                 patches=None,
                ):
        """
        :type  version: :class:`str` or ``None``
        :param version: Domain VCF release version 
            
            * Property is read-only.
            
            
        :type  patches: :class:`list` of :class:`FlexibleProductPatch` or ``None``
        :param patches: List of available patches on the VCF release 
            
            * Property is read-only.
            
            
        """
        self.version = version
        self.patches = patches
        VapiStruct.__init__(self)


FlexibleProductPatches._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.flexible_product_patches', {
        'version': type.OptionalType(type.StringType()),
        'patches': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FlexibleProductPatch'))),
    },
    FlexibleProductPatches,
    False,
    None))



class CustomPatches(VapiStruct):
    """
    Model for supported product install/patches associated with a VCF/VVF
    release

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'releaseVersion': 'release_version',
                            'patches': 'patches',
                            }

    def __init__(self,
                 release_version=None,
                 patches=None,
                ):
        """
        :type  release_version: :class:`str` or ``None``
        :param release_version: VCF/VVF release version 
            
            * Property is read-only.
            
            
        :type  patches: (:class:`dict` of :class:`str` and :class:`list` of :class:`CustomPatch`) or ``None``
        :param patches: Patches used for the product version catalog 
            
            * Property is read-only.
            
            
        """
        self.release_version = release_version
        self.patches = patches
        VapiStruct.__init__(self)


CustomPatches._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.custom_patches', {
        'releaseVersion': type.OptionalType(type.StringType()),
        'patches': type.OptionalType(type.MapType(type.StringType(), type.ListType(type.ReferenceType(__name__, 'CustomPatch')))),
    },
    CustomPatches,
    False,
    None))



class Bundle(VapiStruct):
    """
    Bundle contains bits to install/update the appropriate Cloud Foundation
    software components in your management domain or workload domain.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'id': 'id',
                            'type': 'type',
                            'description': 'description',
                            'version': 'version',
                            'severity': 'severity',
                            'vendor': 'vendor',
                            'releasedDate': 'released_date',
                            'isCumulative': 'is_cumulative',
                            'isCompliant': 'is_compliant',
                            'sizeMB': 'size_mb',
                            'downloadStatus': 'download_status',
                            'components': 'components',
                            'applicabilityStatus': 'applicability_status',
                            'applicabilityOrder': 'applicability_order',
                            'isPartiallyUpgraded': 'is_partially_upgraded',
                            }

    def __init__(self,
                 id=None,
                 type=None,
                 description=None,
                 version=None,
                 severity=None,
                 vendor=None,
                 released_date=None,
                 is_cumulative=None,
                 is_compliant=None,
                 size_mb=None,
                 download_status=None,
                 components=None,
                 applicability_status=None,
                 applicability_order=None,
                 is_partially_upgraded=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: Bundle ID 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Bundle Type 
            
            * Property is read-only.
            
            
        :type  description: :class:`str` or ``None``
        :param description: Bundle Description 
            
            * Property is read-only.
            
            
        :type  version: :class:`str` or ``None``
        :param version: Bundle Version 
            
            * Property is read-only.
            
            
        :type  severity: :class:`str` or ``None``
        :param severity: Bundle Severity 
            
            * Property is read-only.
            
            
        :type  vendor: :class:`str` or ``None``
        :param vendor: Bundle Vendor 
            
            * Property is read-only.
            
            
        :type  released_date: :class:`str` or ``None``
        :param released_date: Bundle Release Date 
            
            * Property is read-only.
            
            
        :type  is_cumulative: :class:`bool` or ``None``
        :param is_cumulative: Is Bundle Cumulative 
            
            * Property is read-only.
            
            
        :type  is_compliant: :class:`bool` or ``None``
        :param is_compliant: Is compliant with the current VCF version 
            
            * Property is read-only.
            
            
        :type  size_mb: :class:`float` or ``None``
        :param size_mb: Bundle Size in MB 
            
            * Property is read-only.
            
            
        :type  download_status: :class:`str` or ``None``
        :param download_status: Bundle Download Status 
            
            * Property is read-only.
            
            
        :type  components: :class:`list` of :class:`BundleComponent` or ``None``
        :param components: Bundle Components 
            
            * Property is read-only.
            
            
        :type  applicability_status: :class:`str` or ``None``
        :param applicability_status: Bundle Applicability Status 
            
            * Property is read-only.
            
            
        :type  applicability_order: :class:`long` or ``None``
        :param applicability_order: Bundle Applicability Order 
            
            * Property is read-only.
            
            
        :type  is_partially_upgraded: :class:`bool` or ``None``
        :param is_partially_upgraded: Is Bundle partially upgraded 
            
            * Property is read-only.
            
            
        """
        self.id = id
        self.type = type
        self.description = description
        self.version = version
        self.severity = severity
        self.vendor = vendor
        self.released_date = released_date
        self.is_cumulative = is_cumulative
        self.is_compliant = is_compliant
        self.size_mb = size_mb
        self.download_status = download_status
        self.components = components
        self.applicability_status = applicability_status
        self.applicability_order = applicability_order
        self.is_partially_upgraded = is_partially_upgraded
        VapiStruct.__init__(self)


Bundle._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle', {
        'id': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
        'description': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'severity': type.OptionalType(type.StringType()),
        'vendor': type.OptionalType(type.StringType()),
        'releasedDate': type.OptionalType(type.StringType()),
        'isCumulative': type.OptionalType(type.BooleanType()),
        'isCompliant': type.OptionalType(type.BooleanType()),
        'sizeMB': type.OptionalType(type.DoubleType()),
        'downloadStatus': type.OptionalType(type.StringType()),
        'components': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'BundleComponent'))),
        'applicabilityStatus': type.OptionalType(type.StringType()),
        'applicabilityOrder': type.OptionalType(type.IntegerType()),
        'isPartiallyUpgraded': type.OptionalType(type.BooleanType()),
    },
    Bundle,
    False,
    None))



class BundleComponent(VapiStruct):
    """
    Bundle Software Component

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'description': 'description',
                            'vendor': 'vendor',
                            'releasedDate': 'released_date',
                            'toVersion': 'to_version',
                            'fromVersion': 'from_version',
                            'imageType': 'image_type',
                            'id': 'id',
                            'type': 'type',
                            }

    def __init__(self,
                 description=None,
                 vendor=None,
                 released_date=None,
                 to_version=None,
                 from_version=None,
                 image_type=None,
                 id=None,
                 type=None,
                ):
        """
        :type  description: :class:`str` or ``None``
        :param description: Bundle Component Description 
            
            * Property is read-only.
            
            
        :type  vendor: :class:`str` or ``None``
        :param vendor: Bundle Component Vendor 
            
            * Property is read-only.
            
            
        :type  released_date: :class:`str` or ``None``
        :param released_date: Bundle Component Release Date 
            
            * Property is read-only.
            
            
        :type  to_version: :class:`str` or ``None``
        :param to_version: Bundle Component's to/target version after Upgrade 
            
            * Property is read-only.
            
            
        :type  from_version: :class:`str` or ``None``
        :param from_version: Bundle Component's from/source version before Upgrade 
            
            * Property is read-only.
            
            
        :type  image_type: :class:`str` or ``None``
        :param image_type: Bundle Component Image Type 
            
            * Property is read-only.
            
            
        :type  id: :class:`str` or ``None``
        :param id: ID of Resource/Software Component 
            
            * Property is read-only.
            
            
        :type  type: :class:`str` or ``None``
        :param type: Type of Resource/Software Component 
            
            * Property is read-only.
            
            
        """
        self.description = description
        self.vendor = vendor
        self.released_date = released_date
        self.to_version = to_version
        self.from_version = from_version
        self.image_type = image_type
        self.id = id
        self.type = type
        VapiStruct.__init__(self)


BundleComponent._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle_component', {
        'description': type.OptionalType(type.StringType()),
        'vendor': type.OptionalType(type.StringType()),
        'releasedDate': type.OptionalType(type.StringType()),
        'toVersion': type.OptionalType(type.StringType()),
        'fromVersion': type.OptionalType(type.StringType()),
        'imageType': type.OptionalType(type.StringType()),
        'id': type.OptionalType(type.StringType()),
        'type': type.OptionalType(type.StringType()),
    },
    BundleComponent,
    False,
    None))



class PageOfBundle(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`Bundle` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfBundle._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_bundle', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Bundle'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfBundle,
    False,
    None))



class BundleDownloadStatusInfo(VapiStruct):
    """
    Model for download status for the bundle of a release component.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'componentType': 'component_type',
                            'version': 'version',
                            'bundleId': 'bundle_id',
                            'downloadId': 'download_id',
                            'downloadStatus': 'download_status',
                            'downloadedSize': 'downloaded_size',
                            'downloadStartTime': 'download_start_time',
                            'downloadEndTime': 'download_end_time',
                            'downloadScheduledTime': 'download_scheduled_time',
                            'isDownloadCancellable': 'is_download_cancellable',
                            'message': 'message',
                            'isDownloadable': 'is_downloadable',
                            }

    def __init__(self,
                 component_type=None,
                 version=None,
                 bundle_id=None,
                 download_id=None,
                 download_status=None,
                 downloaded_size=None,
                 download_start_time=None,
                 download_end_time=None,
                 download_scheduled_time=None,
                 is_download_cancellable=None,
                 message=None,
                 is_downloadable=None,
                ):
        """
        :type  component_type: :class:`str` or ``None``
        :param component_type: The type of the component that the bundle represents.
        :type  version: :class:`str` or ``None``
        :param version: The version (patch version) of the component.
        :type  bundle_id: :class:`str` or ``None``
        :param bundle_id: The bundle ID associated with a component version.
        :type  download_id: :class:`str` or ``None``
        :param download_id: The task ID of the download.
        :type  download_status: :class:`str` or ``None``
        :param download_status: The current status of the download.
        :type  downloaded_size: :class:`long` or ``None``
        :param downloaded_size: The size of the file part that was downloaded so far.
        :type  download_start_time: :class:`long` or ``None``
        :param download_start_time: The time when the download started.
        :type  download_end_time: :class:`long` or ``None``
        :param download_end_time: The time when the download finished or interrupted.
        :type  download_scheduled_time: :class:`long` or ``None``
        :param download_scheduled_time: The time when the download was scheduled to start.
        :type  is_download_cancellable: :class:`bool` or ``None``
        :param is_download_cancellable: True if download can be cancelled.
        :type  message: :class:`str` or ``None``
        :param message: In case of failed download, the error message.
        :type  is_downloadable: :class:`bool` or ``None``
        :param is_downloadable: Indicates whether the bundle for this component version is
            downloadable currently or not.
        """
        self.component_type = component_type
        self.version = version
        self.bundle_id = bundle_id
        self.download_id = download_id
        self.download_status = download_status
        self.downloaded_size = downloaded_size
        self.download_start_time = download_start_time
        self.download_end_time = download_end_time
        self.download_scheduled_time = download_scheduled_time
        self.is_download_cancellable = is_download_cancellable
        self.message = message
        self.is_downloadable = is_downloadable
        VapiStruct.__init__(self)


BundleDownloadStatusInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.bundle_download_status_info', {
        'componentType': type.OptionalType(type.StringType()),
        'version': type.OptionalType(type.StringType()),
        'bundleId': type.OptionalType(type.StringType()),
        'downloadId': type.OptionalType(type.StringType()),
        'downloadStatus': type.OptionalType(type.StringType()),
        'downloadedSize': type.OptionalType(type.IntegerType()),
        'downloadStartTime': type.OptionalType(type.IntegerType()),
        'downloadEndTime': type.OptionalType(type.IntegerType()),
        'downloadScheduledTime': type.OptionalType(type.IntegerType()),
        'isDownloadCancellable': type.OptionalType(type.BooleanType()),
        'message': type.OptionalType(type.StringType()),
        'isDownloadable': type.OptionalType(type.BooleanType()),
    },
    BundleDownloadStatusInfo,
    False,
    None))



class PageOfBundleDownloadStatusInfo(VapiStruct):
    """


    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'elements': 'elements',
                            'pageMetadata': 'page_metadata',
                            }

    def __init__(self,
                 elements=None,
                 page_metadata=None,
                ):
        """
        :type  elements: :class:`list` of :class:`BundleDownloadStatusInfo` or ``None``
        :param elements: The list of elements included in this page 
            
            * Property is read-only.
            
            
        :type  page_metadata: :class:`PageMetadata` or ``None``
        :param page_metadata:         """
        self.elements = elements
        self.page_metadata = page_metadata
        VapiStruct.__init__(self)


PageOfBundleDownloadStatusInfo._set_binding_type(type.StructType(
    'vmware.vcf_installer.model.page_of_bundle_download_status_info', {
        'elements': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'BundleDownloadStatusInfo'))),
        'pageMetadata': type.OptionalType(type.ReferenceType(__name__, 'PageMetadata')),
    },
    PageOfBundleDownloadStatusInfo,
    False,
    None))



class Error(VapiError):
    """
    Error response containing a minor error code, a localized error message, a
    localized remediation message and optionally a reference token to correlate
    the error with the logs

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _qualname = 'Error'
    _canonical_to_pep_names = {
                'errorCode' : 'error_code',
                'errorType' : 'error_type',
                'arguments' : 'arguments',
                'context' : 'context',
                'message' : 'message',
                'remediationMessage' : 'remediation_message',
                'causes' : 'causes',
                'nestedErrors' : 'nested_errors',
                'referenceToken' : 'reference_token',
                'label' : 'label',
                'remediationUrl' : 'remediation_url',
    }

    def __init__(self,
                 error_code=None,
                 error_type=None,
                 arguments=None,
                 context=None,
                 message=None,
                 remediation_message=None,
                 causes=None,
                 nested_errors=None,
                 reference_token=None,
                 label=None,
                 remediation_url=None,
                ):
        """
        :type  error_code: :class:`str` or ``None``
        :param error_code: The minor error code 
            
            * Property is read-only.
            
            
        :type  error_type: :class:`str` or ``None``
        :param error_type: The error type 
            
            * Property is read-only.
            
            
        :type  arguments: :class:`list` of :class:`str` or ``None``
        :param arguments: The arguments used to localize the message, Can be used by scripts
            to automate the error processing. 
            
            * Property is read-only.
            
            
        :type  context: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
        :param context: The error context (e.g. the component where it occurred). 
            
            * Property is read-only.
            
            
        :type  message: :class:`str` or ``None``
        :param message: The localized error message 
            
            * Property is read-only.
            
            
        :type  remediation_message: :class:`str` or ``None``
        :param remediation_message: The localized remediation error message
        :type  causes: :class:`list` of :class:`ErrorCause` or ``None``
        :param causes: The underlying cause exceptions.
        :type  nested_errors: :class:`list` of :class:`Error` or ``None``
        :param nested_errors: The nested errors when the error is a composite one
        :type  reference_token: :class:`str` or ``None``
        :param reference_token: A reference token correlating the error with the relevant detailed
            error logs. Should be sent to the service provider when reporting
            issues. 
            
            * Property is read-only.
            
            
        :type  label: :class:`str` or ``None``
        :param label: The localized label message 
            
            * Property is read-only.
            
            
        :type  remediation_url: :class:`str` or ``None``
        :param remediation_url: The URL string for remediation documentation link 
            
            * Property is read-only.
            
            
        """

        self.error_code = error_code
        self.error_type = error_type
        self.arguments = arguments
        self.context = context
        self.message = message
        self.remediation_message = remediation_message
        self.causes = causes
        self.nested_errors = nested_errors
        self.reference_token = reference_token
        self.label = label
        self.remediation_url = remediation_url
        VapiError.__init__(self)

Error._set_binding_type(type.ErrorType(
    'vmware.vcf_installer.model.error', {
        'errorCode': type.OptionalType(type.StringType()),
        'errorType': type.OptionalType(type.StringType()),
        'arguments': type.OptionalType(type.ListType(type.StringType())),
        'context': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
        'message': type.OptionalType(type.StringType()),
        'remediationMessage': type.OptionalType(type.StringType()),
        'causes': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ErrorCause'))),
        'nestedErrors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Error'))),
        'referenceToken': type.OptionalType(type.StringType()),
        'label': type.OptionalType(type.StringType()),
        'remediationUrl': type.OptionalType(type.StringType()),
    },
    Error))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

