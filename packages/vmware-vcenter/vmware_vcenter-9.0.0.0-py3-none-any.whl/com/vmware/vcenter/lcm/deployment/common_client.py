# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.deployment.common.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.lcm.deployment.common_client`` module provides common
classes for install/upgrade of a vCenter Server.

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

class ApplianceSize(Enum):
    """
    The ``ApplianceSize`` class defines the size of the appliance (CPU and
    memory) to be deployed.
    This enumeration was added in **vSphere API 9.0.0.0**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    TINY = None
    """
    Appliance size of 'tiny'.

    """
    SMALL = None
    """
    Appliance size of 'small'.

    """
    MEDIUM = None
    """
    Appliance size of 'medium'.

    """
    LARGE = None
    """
    Appliance size of 'large',

    """
    XLARGE = None
    """
    Appliance size of 'extra large'.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ApplianceSize` instance.
        """
        Enum.__init__(string)

ApplianceSize._set_values({
    'TINY': ApplianceSize('TINY'),
    'SMALL': ApplianceSize('SMALL'),
    'MEDIUM': ApplianceSize('MEDIUM'),
    'LARGE': ApplianceSize('LARGE'),
    'XLARGE': ApplianceSize('XLARGE'),
})
ApplianceSize._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.appliance_size',
    ApplianceSize))



class StorageSize(Enum):
    """
    The ``StorageSize`` class defines the storage size of the appliance to be
    deployed.
    This enumeration was added in **vSphere API 9.0.0.0**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    REGULAR = None
    """
    Regular storage

    """
    LARGE = None
    """
    Large storage

    """
    XLARGE = None
    """
    Extra large storage

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`StorageSize` instance.
        """
        Enum.__init__(string)

StorageSize._set_values({
    'REGULAR': StorageSize('REGULAR'),
    'LARGE': StorageSize('LARGE'),
    'XLARGE': StorageSize('XLARGE'),
})
StorageSize._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.storage_size',
    StorageSize))



class AllocateResource(Enum):
    """
    The ``AllocateResource`` class defines when to allocate resource to the
    target VM. See :class:`ResourceAllocationInfo`
    This enumeration was added in **vSphere API 9.0.0.0**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    ON_DEPLOYMENT = None
    """
    On deployment of a new VM allocate the resource.

    """
    ON_SUCCESSFUL_UPGRADE = None
    """
    On successful upgrade of the VC allocate the resource to the VM deployed as
    part of the upgrade.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`AllocateResource` instance.
        """
        Enum.__init__(string)

AllocateResource._set_values({
    'ON_DEPLOYMENT': AllocateResource('ON_DEPLOYMENT'),
    'ON_SUCCESSFUL_UPGRADE': AllocateResource('ON_SUCCESSFUL_UPGRADE'),
})
AllocateResource._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.allocate_resource',
    AllocateResource))



class HashAlgorithm(Enum):
    """
    The ``HashAlgorithm`` class defines the valid hash algorithms.
    This enumeration was added in **vSphere API 9.0.0.0**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    SHA256 = None
    """
    Hash algorithm: SHA-256

    """
    SHA512 = None
    """
    Hash algorithm: SHA-512

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`HashAlgorithm` instance.
        """
        Enum.__init__(string)

HashAlgorithm._set_values({
    'SHA256': HashAlgorithm('SHA256'),
    'SHA512': HashAlgorithm('SHA512'),
})
HashAlgorithm._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.hash_algorithm',
    HashAlgorithm))



class Status(Enum):
    """
    The ``Status`` class defines the status values that can be reported by the
    upgrade process.
    This enumeration was added in **vSphere API 9.0.0.0**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    PENDING = None
    """
    The operation is in pending state.

    """
    RUNNING = None
    """
    The operation is in progress.

    """
    BLOCKED = None
    """
    The operation is blocked.

    """
    SUCCEEDED = None
    """
    The operation completed successfully.

    """
    FAILED = None
    """
    The operation failed.

    """
    CANCELED = None
    """
    The operation was canceled.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`Status` instance.
        """
        Enum.__init__(string)

Status._set_values({
    'PENDING': Status('PENDING'),
    'RUNNING': Status('RUNNING'),
    'BLOCKED': Status('BLOCKED'),
    'SUCCEEDED': Status('SUCCEEDED'),
    'FAILED': Status('FAILED'),
    'CANCELED': Status('CANCELED'),
})
Status._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.status',
    Status))




class Network(VapiStruct):
    """
    The ``Network`` class defines the network configuration.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'mode',
            {
                'STATIC' : [('ip', True), ('dns_servers', True), ('prefix', True), ('gateway', True), ('hostname', False)],
                'DHCP' : [],
            }
        ),
    ]



    def __init__(self,
                 ip_family=None,
                 mode=None,
                 ip=None,
                 dns_servers=None,
                 prefix=None,
                 gateway=None,
                 hostname=None,
                ):
        """
        :type  ip_family: :class:`Network.IpType` or ``None``
        :param ip_family: Network IP address family.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None defaults to IPv4
        :type  mode: :class:`Network.NetworkMode`
        :param mode: Network mode.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  ip: :class:`str`
        :param ip: Network IP address. Required for static mode only.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``mode`` is :attr:`Network.NetworkMode.STATIC`.
        :type  dns_servers: :class:`list` of :class:`str`
        :param dns_servers: A comma-separated list of IP addresses of DNS servers.Required for
            static mode only. A JSON array such as ["1.2.3.4", "127.0.0.1"].
            The DNS servers must be reachable from the source appliance and
            only the first two will be used.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``mode`` is :attr:`Network.NetworkMode.STATIC`.
        :type  prefix: :class:`long`
        :param prefix: Network prefix length. Required for static mode only. This is the
            number of bits set in the subnet mask; for instance, if the subnet
            mask is 255.255.255.0, there are 24 bits in the binary version of
            the subnet mask, so the prefix length is 24. If used, the values
            must be in the inclusive range of 0 to 32 for IPv4 and 0 to 128 for
            IPv6.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``mode`` is :attr:`Network.NetworkMode.STATIC`.
        :type  gateway: :class:`str`
        :param gateway: Gateway of the network. Required for static mode only.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``mode`` is :attr:`Network.NetworkMode.STATIC`.
        :type  hostname: :class:`str` or ``None``
        :param hostname: Primary network identity. Can be either an IP address or a fully
            qualified domain name(FQDN).
            This attribute was added in **vSphere API 9.0.0.0**.
            hostname may not be applicable
        """
        self.ip_family = ip_family
        self.mode = mode
        self.ip = ip
        self.dns_servers = dns_servers
        self.prefix = prefix
        self.gateway = gateway
        self.hostname = hostname
        VapiStruct.__init__(self)


    class IpType(Enum):
        """
        Network IP address family.
        This enumeration was added in **vSphere API 9.0.0.0**.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        IPV4 = None
        """
        IPv4 Type of IP address.

        """
        IPV6 = None
        """
        IPv6 Type of IP address.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IpType` instance.
            """
            Enum.__init__(string)

    IpType._set_values({
        'IPV4': IpType('IPV4'),
        'IPV6': IpType('IPV6'),
    })
    IpType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.common.network.ip_type',
        IpType))

    class NetworkMode(Enum):
        """
        Network mode.
        This enumeration was added in **vSphere API 9.0.0.0**.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DHCP = None
        """
        DHCP mode.

        """
        STATIC = None
        """
        Static IP mode.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`NetworkMode` instance.
            """
            Enum.__init__(string)

    NetworkMode._set_values({
        'DHCP': NetworkMode('DHCP'),
        'STATIC': NetworkMode('STATIC'),
    })
    NetworkMode._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.common.network.network_mode',
        NetworkMode))

Network._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.network', {
        'ip_family': type.OptionalType(type.ReferenceType(__name__, 'Network.IpType')),
        'mode': type.ReferenceType(__name__, 'Network.NetworkMode'),
        'ip': type.OptionalType(type.StringType()),
        'dns_servers': type.OptionalType(type.ListType(type.StringType())),
        'prefix': type.OptionalType(type.IntegerType()),
        'gateway': type.OptionalType(type.StringType()),
        'hostname': type.OptionalType(type.StringType()),
    },
    Network,
    False,
    None))



class ResourceAllocationInfo(VapiStruct):
    """
    The ``ResourceAllocationInfo`` class contains resource allocation
    information for a VM.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 reservation=None,
                 allocate=None,
                ):
        """
        :type  reservation: :class:`long`
        :param reservation: Amount of resource that is guaranteed available to the virtual
            machine. Reserved resources are not wasted if they are not used. If
            the utilization is less than the reservation, the resources can be
            utilized by other running virtual machines. Units are MB for
            memory, and MHz for CPU.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  allocate: :class:`AllocateResource` or ``None``
        :param allocate: This attribute was added in **vSphere API 9.0.0.0**.
            If None will allocate resource at VM deployment.
        """
        self.reservation = reservation
        self.allocate = allocate
        VapiStruct.__init__(self)


ResourceAllocationInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.resource_allocation_info', {
        'reservation': type.IntegerType(),
        'allocate': type.OptionalType(type.ReferenceType(__name__, 'AllocateResource')),
    },
    ResourceAllocationInfo,
    False,
    None))



class OvaInfo(VapiStruct):
    """
    The ``OvaInfo`` class defines the OVA file location info to be used by the
    lifecycle service.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 location=None,
                 ssl_verify=None,
                 ova_checksum=None,
                 ova_checksum_algorithm=None,
                 certificate=None,
                ):
        """
        :type  location: :class:`str`
        :param location: The location of the OVA file for installation. It can be web URL or
            absolute filepath i.e https://server.com/appliance.ova or
            file://storage/appliance.ova
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: A flag to indicate whether SSL verification is required for the ova
            location.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None defaults to True
        :type  ova_checksum: :class:`str` or ``None``
        :param ova_checksum: Checksum to validate the OVA file.
            This attribute was added in **vSphere API 9.0.0.0**.
            If :class:`set` will be used for checksum validation of the ova
            file on the vCenter.
        :type  ova_checksum_algorithm: :class:`HashAlgorithm` or ``None``
        :param ova_checksum_algorithm: The hash algorithm (SHA256, SHA512) used to calculate the checksum.
            This attribute was added in **vSphere API 9.0.0.0**.
            If not specified the default checksum algorithm is
            :attr:`HashAlgorithm.SHA256`.
        :type  certificate: :class:`str` or ``None``
        :param certificate: Certificate to verify the SSL OVA location. The value should be the
            x509 leaf certificate encoded in PEM format. 
            
            * If ``sslVerify`` is true and this field is omitted. a CA based
              validation will be used.
            * If ``sslVerify`` is true and this field is provided will be used
              for SSL validation.
            This attribute was added in **vSphere API 9.0.0.0**.
            If :class:`set` will be used for SSL validation.
        """
        self.location = location
        self.ssl_verify = ssl_verify
        self.ova_checksum = ova_checksum
        self.ova_checksum_algorithm = ova_checksum_algorithm
        self.certificate = certificate
        VapiStruct.__init__(self)


OvaInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.ova_info', {
        'location': type.URIType(),
        'ssl_verify': type.OptionalType(type.BooleanType()),
        'ova_checksum': type.OptionalType(type.StringType()),
        'ova_checksum_algorithm': type.OptionalType(type.ReferenceType(__name__, 'HashAlgorithm')),
        'certificate': type.OptionalType(type.StringType()),
    },
    OvaInfo,
    False,
    None))



class ApplianceDeployment(VapiStruct):
    """
    The ``ApplianceDeployment`` class describes the new appliance deployment
    configuration.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 size=None,
                 thin_disk_mode=None,
                 disk_size=None,
                 root_password=None,
                 network_settings=None,
                 ova_info=None,
                 ceip_enabled=None,
                 cpu_allocation=None,
                 memory_allocation=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: The VM name of the appliance to deploy.
            This attribute was added in **vSphere API 9.0.0.0**.
            If ``name`` is not specified, default VM name will be used with
            following format: vcenter-upgrade-[upgrade-uuid].
        :type  size: :class:`ApplianceSize` or ``None``
        :param size: A size descriptor based on the number of virtual machines which
            will be managed by the new vCenter appliance.
            This attribute was added in **vSphere API 9.0.0.0**.
            If ``size`` is not provided, will use the size of the source VCSA
        :type  thin_disk_mode: :class:`bool` or ``None``
        :param thin_disk_mode: Whether to deploy the appliance with thin mode virtual disks.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, the source vCenter disk deployment will be tried. If there
            is no information provided for the source container a default value
            of thin deployment will be set.
        :type  disk_size: :class:`StorageSize` or ``None``
        :param disk_size: The disk size of the new vCenter appliance.
            This attribute was added in **vSphere API 9.0.0.0**.
            If ``diskSize`` is not provided, will use the diskSize of the
            source VCSA.
        :type  root_password: :class:`str`
        :param root_password: A root password to be used for that appliance. During migration
            upgrade it is only temporary passwords. It must conform to the
            following requirements: 
            
            * At least 8 characters.
            * No more than 20 characters.
            * At least 1 uppercase character.
            * At least 1 lowercase character.
            * At least 1 number.
            * At least 1 special character (e.g., '!', '(', '\\\\@', etc.).
            * Only visible A-Z, a-z, 0-9 and punctuation (spaces are not
              allowed)
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  network_settings: :class:`Network` or ``None``
        :param network_settings: The network settings of the appliance to be deployed.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the appliance will be deployed with an automatically
            selected link-local address.
        :type  ova_info: :class:`OvaInfo` or ``None``
        :param ova_info: Custom location of the OVA for deployment.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None use the OVA file for the desired version in the configured
            repository.
        :type  ceip_enabled: :class:`bool` or ``None``
        :param ceip_enabled: This key describes the enabling option for the VMware's Customer
            Experience Improvement Program (CEIP).
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, defaults to True
        :type  cpu_allocation: :class:`ResourceAllocationInfo` or ``None``
        :param cpu_allocation: Resource allocation information of CPU.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None will deploy the appliance with no cpu reservation.
        :type  memory_allocation: :class:`ResourceAllocationInfo` or ``None``
        :param memory_allocation: Resource allocation information of Memory
            This attribute was added in **vSphere API 9.0.0.0**.
            If None will deploy the appliance with no memory reservation.
        """
        self.name = name
        self.size = size
        self.thin_disk_mode = thin_disk_mode
        self.disk_size = disk_size
        self.root_password = root_password
        self.network_settings = network_settings
        self.ova_info = ova_info
        self.ceip_enabled = ceip_enabled
        self.cpu_allocation = cpu_allocation
        self.memory_allocation = memory_allocation
        VapiStruct.__init__(self)


ApplianceDeployment._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.appliance_deployment', {
        'name': type.OptionalType(type.StringType()),
        'size': type.OptionalType(type.ReferenceType(__name__, 'ApplianceSize')),
        'thin_disk_mode': type.OptionalType(type.BooleanType()),
        'disk_size': type.OptionalType(type.ReferenceType(__name__, 'StorageSize')),
        'root_password': type.SecretType(),
        'network_settings': type.OptionalType(type.ReferenceType(__name__, 'Network')),
        'ova_info': type.OptionalType(type.ReferenceType(__name__, 'OvaInfo')),
        'ceip_enabled': type.OptionalType(type.BooleanType()),
        'cpu_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourceAllocationInfo')),
        'memory_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourceAllocationInfo')),
    },
    ApplianceDeployment,
    False,
    None))



class Connection(VapiStruct):
    """
    The ``Connection`` class contains information used to connect to a vCenter
    or ESXi.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 hostname=None,
                 username=None,
                 password=None,
                 https_port=None,
                 ssl_verify=None,
                 certificate=None,
                ):
        """
        :type  hostname: :class:`str`
        :param hostname: The IP address or DNS resolvable name of the ESX/VC host. If a DNS
            resolvable name is provided, it must be resolvable from the source
            appliance.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  username: :class:`str`
        :param username: A username with administrative privileges on the ESX/VC host.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  password: :class:`str`
        :param password: The password of the :attr:`Connection.username` on the ESX/VC host.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  https_port: :class:`long` or ``None``
        :param https_port: The port number for the ESX/VC.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, defaults to 443
        :type  ssl_verify: :class:`bool` or ``None``
        :param ssl_verify: A flag to indicate whether the ssl verification is required.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, defaults to True
        :type  certificate: :class:`str` or ``None``
        :param certificate: Certificate to verify the target host location. The value should be
            the x509 leaf certificate encoded in PEM format. Only if
            ``sslVerify`` is true and this field is provided will be used for
            SSL validation.
            This attribute was added in **vSphere API 9.0.0.0**.
            If :class:`set` will be used for SSL validation.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.https_port = https_port
        self.ssl_verify = ssl_verify
        self.certificate = certificate
        VapiStruct.__init__(self)


Connection._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.connection', {
        'hostname': type.StringType(),
        'username': type.StringType(),
        'password': type.SecretType(),
        'https_port': type.OptionalType(type.IntegerType()),
        'ssl_verify': type.OptionalType(type.BooleanType()),
        'certificate': type.OptionalType(type.StringType()),
    },
    Connection,
    False,
    None))



class EsxPlacementConfig(VapiStruct):
    """
    The ``EsxPlacementConfig`` class contains configuration of ESX placement of
    the target appliance.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 datastore_name=None,
                 network_name=None,
                 resource_pool_path=None,
                ):
        """
        :type  datastore_name: :class:`str`
        :param datastore_name: The datastore on which to store the files of the appliance. This
            value has to be either a specific datastore name, or a specific
            datastore in a datastore cluster. The datastore must be accessible
            from the ESX host.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  network_name: :class:`str` or ``None``
        :param network_name: The network of the ESX host to which the new appliance should
            connect. Omit this parameter if the ESX host has one network.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None and there is only one network configured, it will be used.
        :type  resource_pool_path: :class:`str` or ``None``
        :param resource_pool_path: The path to the resource pool on the ESX host in which the
            appliance will be deployed.
            This attribute was added in **vSphere API 9.0.0.0**.
            Not applicable when not in resource pool
        """
        self.datastore_name = datastore_name
        self.network_name = network_name
        self.resource_pool_path = resource_pool_path
        VapiStruct.__init__(self)


EsxPlacementConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.esx_placement_config', {
        'datastore_name': type.StringType(),
        'network_name': type.OptionalType(type.StringType()),
        'resource_pool_path': type.OptionalType(type.StringType()),
    },
    EsxPlacementConfig,
    False,
    None))



class StoragePolicySpec(VapiStruct):
    """
    The ``StoragePolicySpec`` class contains information about the storage
    policy to be associated with a virtual machine object.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 policy=None,
                ):
        """
        :type  policy: :class:`str`
        :param policy: Identifier of the storage policy which should be associated with
            the virtual machine.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.StoragePolicy``. When methods return a value
            of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.vcenter.StoragePolicy``.
        """
        self.policy = policy
        VapiStruct.__init__(self)


StoragePolicySpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.storage_policy_spec', {
        'policy': type.IdType(resource_types='com.vmware.vcenter.StoragePolicy'),
    },
    StoragePolicySpec,
    False,
    None))



class VcPlacementConfig(VapiStruct):
    """
    The ``VcPlacementConfig`` class contains configuration of VC placement of
    the target appliance.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_folder_path=None,
                 resource_pool_path=None,
                 cluster_path=None,
                 host_path=None,
                 datastore_name=None,
                 datastore_cluster_name=None,
                 network_name=None,
                ):
        """
        :type  vm_folder_path: :class:`str` or ``None``
        :param vm_folder_path: Absolute path of the VM folder. VM folder must be visible by the
            Data Center of the compute
            resourceFormat:/{dc}/{vm_folder1}/{vm_folder2}e.g.:'/DCenter/VM
            Folder 0/VM Folder1'.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the default VM folder of the Datacenter will be used.
        :type  resource_pool_path: :class:`str` or ``None``
        :param resource_pool_path: Absolute path to resource pool. Format: /{datacenter
            folder}/{datacenter name}/host/{host
            name}/{cluster_name}/Resources/{resource pool}. e.g: Your
            Datacenter Folder/Your Datacenter/host/Your Cluster/Resources/Your
            Resource Pool
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutually exclusive between ``resourcePoolPath``, ``clusterPath``,
            and ``hostPath``
        :type  cluster_path: :class:`str` or ``None``
        :param cluster_path: Absolute path to the cluster. Format: /{datacenter
            folder}/{datacenter name}/host/{cluster_name}. e.g: /Your
            Datacenter Folder/Your Datacenter/host/Your Cluster
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutually exclusive between ``resourcePoolPath``, ``clusterPath``,
            and ``hostPath``
        :type  host_path: :class:`str` or ``None``
        :param host_path: Absolute path of the ESX host (FQDN/IP) in the vCenter inventory
            tree.
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutually exclusive between ``resourcePoolPath``, ``clusterPath``,
            and ``hostPath``
        :type  datastore_name: :class:`str` or ``None``
        :param datastore_name: The datastore on which to store the files of the appliance. This
            value has to be either a specific datastore name, or a specific
            datastore in a datastore cluster. The datastore must have the space
            defined as appliance storage size.
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutually exclusive between ``datastoreName`` and
            ``datastoreClusterName``
        :type  datastore_cluster_name: :class:`str` or ``None``
        :param datastore_cluster_name: The datastore cluster on which to store the files of the appliance.
            The datastore cluster must have the space defined as appliance
            storage size.
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutually exclusive between ``datastoreName`` and
            ``datastoreClusterName``
        :type  network_name: :class:`str` or ``None``
        :param network_name: Name of the network. e.g. VM Network
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the target appliance will be deployed on the same network
            as current vCenter. If current vCenter is not self managed and
            source container is not specified, upgrade initialization will
            fail.
        """
        self.vm_folder_path = vm_folder_path
        self.resource_pool_path = resource_pool_path
        self.cluster_path = cluster_path
        self.host_path = host_path
        self.datastore_name = datastore_name
        self.datastore_cluster_name = datastore_cluster_name
        self.network_name = network_name
        VapiStruct.__init__(self)


VcPlacementConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.vc_placement_config', {
        'vm_folder_path': type.OptionalType(type.StringType()),
        'resource_pool_path': type.OptionalType(type.StringType()),
        'cluster_path': type.OptionalType(type.StringType()),
        'host_path': type.OptionalType(type.StringType()),
        'datastore_name': type.OptionalType(type.StringType()),
        'datastore_cluster_name': type.OptionalType(type.StringType()),
        'network_name': type.OptionalType(type.StringType()),
    },
    VcPlacementConfig,
    False,
    None))



class Esx(VapiStruct):
    """
    The ``Esx`` class contains ESX configuration that should be used for
    deployment.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 connection=None,
                 placement_config=None,
                ):
        """
        :type  connection: :class:`Connection`
        :param connection: The configuration to connect to an ESX/VC.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  placement_config: :class:`EsxPlacementConfig`
        :param placement_config: The location of the new version of the vCSA on the desired ESX.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.connection = connection
        self.placement_config = placement_config
        VapiStruct.__init__(self)


Esx._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.esx', {
        'connection': type.ReferenceType(__name__, 'Connection'),
        'placement_config': type.ReferenceType(__name__, 'EsxPlacementConfig'),
    },
    Esx,
    False,
    None))



class VCenter(VapiStruct):
    """
    The ``VCenter`` class contains VC configuration that should be used for
    deployment.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 connection=None,
                 placement_config=None,
                ):
        """
        :type  connection: :class:`Connection` or ``None``
        :param connection: The configuration to connect to a VCenter.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the target appliance will be deployed on the location
            specified in :attr:`VCenter.placement_config` on the current
            vCenter.
        :type  placement_config: :class:`VcPlacementConfig`
        :param placement_config: The location of the new version of the vCSA on the desired vCenter.
            
            All names are case-sensitive. you can install the appliance to one
            of the following destinations: 1. A resource pool in a cluster, use
            'cluster_path'. 2. A specific ESX host in a cluster, use
            'host_path'. 3. A resource pool in a specific ESX host being
            managed by the current vCenter, use 'resource_pool_path'. 4. To
            install a new appliance to a specific ESX host in a cluster,
            provide the 'host_path' key, and the 'datastore_name', e.g.
            'host_path': '/MyDataCenter/host/MyCluster/10.20.30.40',
            'datastore_name': 'Your Datastore'. 5. To install a new appliance
            to a specific resource pool, provide the 'resource_pool_path', and
            the 'datastore_name', e.g. 'resource_pool_path': '/Your Datacenter
            Folder/Your Datacenter/host/Your Cluster/Resources/Your Resource
            Pool', 'datastore_name': 'Your Datastore'. 6. To place a new
            appliance to a virtual machine Folder, provide the
            'vm_folder_path', e.g. vm_folder_path': 'VM Folder 0/VM Folder1'.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.connection = connection
        self.placement_config = placement_config
        VapiStruct.__init__(self)


VCenter._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.V_center', {
        'connection': type.OptionalType(type.ReferenceType(__name__, 'Connection')),
        'placement_config': type.ReferenceType(__name__, 'VcPlacementConfig'),
    },
    VCenter,
    False,
    None))



class Location(VapiStruct):
    """
    The ``Location`` class contains configuration of appliance location.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 esx=None,
                 vcenter=None,
                ):
        """
        :type  esx: :class:`Esx` or ``None``
        :param esx: This section describes the ESX host on which to deploy the
            appliance. Required if you are deploying the appliance directly on
            an ESX host.
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutual exclusive between ``esx`` and ``vcenter``
        :type  vcenter: :class:`VCenter` or ``None``
        :param vcenter: This subsection describes the vCenter on which to deploy the
            appliance.
            This attribute was added in **vSphere API 9.0.0.0**.
            Mutual exclusive between ``esx`` and ``vcenter``
        """
        self.esx = esx
        self.vcenter = vcenter
        VapiStruct.__init__(self)


Location._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.location', {
        'esx': type.OptionalType(type.ReferenceType(__name__, 'Esx')),
        'vcenter': type.OptionalType(type.ReferenceType(__name__, 'VCenter')),
    },
    Location,
    False,
    None))



class ApplianceDeploymentConfig(VapiStruct):
    """
    The ``ApplianceDeploymentConfig`` class contains the new appliance
    deployment configuration.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 source_container=None,
                 appliance=None,
                 location=None,
                ):
        """
        :type  source_container: :class:`Connection` or ``None``
        :param source_container: A connection to container, which hosts the source appliance. This
            connection information is required for automatically extracting and
            preserving VM configuration during deployment, e.g. Virtual
            Ethernet Cards. If either the current vCenter is self managed or
            the VM configuration is not necessary to be preserved during
            deployment this field might be omitted.
            This attribute was added in **vSphere API 9.0.0.0**.
            Not required if the current VCenter is self managed. Otherwise if
            not set VM configuration won't be preserved.
        :type  appliance: :class:`ApplianceDeployment`
        :param appliance: Description of the new appliance configuration.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  location: :class:`Location` or ``None``
        :param location: ESX or VC on which to deploy the appliance.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the target appliance will be deployed on the same location
            as current vCenter. If current vCenter is not self managed and
            source container is not specified, upgrade initialization will
            fail.
        """
        self.source_container = source_container
        self.appliance = appliance
        self.location = location
        VapiStruct.__init__(self)


ApplianceDeploymentConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.appliance_deployment_config', {
        'source_container': type.OptionalType(type.ReferenceType(__name__, 'Connection')),
        'appliance': type.ReferenceType(__name__, 'ApplianceDeployment'),
        'location': type.OptionalType(type.ReferenceType(__name__, 'Location')),
    },
    ApplianceDeploymentConfig,
    False,
    None))



class CommonInfo(VapiStruct):
    """
    The ``CommonInfo`` class contains information common to all tasks.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'status',
            {
                'FAILED' : [('error', False), ('start_time', True), ('end_time', True)],
                'CANCELED' : [('error', False), ('start_time', True), ('end_time', True)],
                'RUNNING' : [('start_time', True)],
                'BLOCKED' : [('start_time', True)],
                'SUCCEEDED' : [('start_time', True), ('end_time', True)],
                'PENDING' : [],
            }
        ),
    ]



    def __init__(self,
                 description=None,
                 status=None,
                 cancelable=None,
                 error=None,
                 start_time=None,
                 end_time=None,
                ):
        """
        :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param description: Description of the operation associated with the task.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  status: :class:`Status`
        :param status: Status of the operation associated with the task.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  cancelable: :class:`bool`
        :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
            value may change as the operation progresses.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  error: :class:`Exception` or ``None``
        :param error: Description of the error if the operation status is "FAILED" or the
            upgrade has been canceled.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None there is no error raised by the upgrade
        :type  start_time: :class:`datetime.datetime`
        :param start_time: Time when the operation is started.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of :attr:`Status.RUNNING`,
            :attr:`Status.BLOCKED`, :attr:`Status.SUCCEEDED`,
            :attr:`Status.FAILED`, or :attr:`Status.CANCELED`.
        :type  end_time: :class:`datetime.datetime`
        :param end_time: Time when the operation is completed.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of :attr:`Status.SUCCEEDED`,
            :attr:`Status.FAILED`, or :attr:`Status.CANCELED`.
        """
        self.description = description
        self.status = status
        self.cancelable = cancelable
        self.error = error
        self.start_time = start_time
        self.end_time = end_time
        VapiStruct.__init__(self)


CommonInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.common_info', {
        'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'status': type.ReferenceType(__name__, 'Status'),
        'cancelable': type.BooleanType(),
        'error': type.OptionalType(type.AnyErrorType()),
        'start_time': type.OptionalType(type.DateTimeType()),
        'end_time': type.OptionalType(type.DateTimeType()),
    },
    CommonInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

