# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.edges.foundation.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.namespace_management.networks.edges.foundation_client``
module provides classes and classes to manage vSphere Foundation Load
Balancers.

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

class AvailabilityMode(Enum):
    """
    ``AvailabilityMode`` describes the availability options for the load
    balancer.
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
    ACTIVE_PASSIVE = None
    """
    Deploys two nodes with one node responsible for serving traffic and the
    second node acting in standby. In the event that nodes cannot communicate
    with each other or are otherwise deemed unhealthy, a fail-over will occur
    and the passive node will begin serving traffic. 
    
    In the event of a fail-over, your workloads may be unavailable for a few
    seconds and connections to and from the load balancer may be reset. 
    
    Both nodes will be deployed to a single vSphere Zone in your Supervisor.

    """
    SINGLE_NODE = None
    """
    Deploys a single node into a Supervisor vSphere Zone. A single node
    configuration trades availability to reduce resource consumption. In the
    event of a node failure, workloads will not be available until the node is
    able to be re-provisioned and configured. Re-provisioning happens
    automatically, but it is best-effort and requires a healthy cluster. 
    
    It is recommended you deploy with :attr:`AvailabilityMode.ACTIVE_PASSIVE`
    configuration if your Supervisor has enough resources.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`AvailabilityMode` instance.
        """
        Enum.__init__(string)

AvailabilityMode._set_values({
    'ACTIVE_PASSIVE': AvailabilityMode('ACTIVE_PASSIVE'),
    'SINGLE_NODE': AvailabilityMode('SINGLE_NODE'),
})
AvailabilityMode._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.availability_mode',
    AvailabilityMode))



class Persona(Enum):
    """
    A ``Persona`` determines the type of traffic that passes through a network
    interface.
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
    MANAGEMENT = None
    """
    A Management Persona allows management traffic to pass through this
    interface. Management traffic may include (but is not limited to) node
    health checks, rsyslog, and control plane capabilities. 
    
    Management traffic can be safely isolated from workload and external
    traffic by placing the Management Persona NIC onto a different network from
    other NICs.

    """
    WORKLOAD = None
    """
    A Workload Persona allows traffic to reach workload networks through the
    provisioning of LoadBalancer Services in Kubernetes. Thus, interface
    associated with this persona must be able to reach node IP addresses on
    Supervisor workload networks. 
    
    An interface with the Workload Persona cannot be connected to a DHCP
    network.

    """
    FRONTEND = None
    """
    A Frontend Persona is used to host load balancer IP addresses. It allows
    external traffic to reach the load balancer addresses which can then be
    forwarded to interfaces with a Workload Persona. 
    
    IP addresses supplied in
    :attr:`com.vmware.vcenter.namespace_management.networks.edges_client.Edge.load_balancer_address_ranges`,
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks_client.Edges.FoundationLoadBalancerCreateSpec.vip_ranges`,
    or
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks_client.Edges.FoundationLoadBalancerUpdateSpec.vip_ranges`
    will be utilized by the network interface configured with this Persona. 
    
    Virtual IP traffic can be safely isolated from workload and management
    traffic by placing the Frontend Persona NIC onto a different network from
    other NICs. 
    
    An interface with the Frontend Persona cannot be connected to a DHCP
    network. 
    
    **Frontend Persona interface cannot be changed.**

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`Persona` instance.
        """
        Enum.__init__(string)

Persona._set_values({
    'MANAGEMENT': Persona('MANAGEMENT'),
    'WORKLOAD': Persona('WORKLOAD'),
    'FRONTEND': Persona('FRONTEND'),
})
Persona._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.persona',
    Persona))



class SizeHint(Enum):
    """
    The ``SizeHint`` determines the Foundation load balancer form factor.
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
    SMALL = None
    """
    :attr:`SizeHint.SMALL` requires 2 CPUs, 4 GB memory and 8 GB storage
    resources.

    """
    MEDIUM = None
    """
    :attr:`SizeHint.MEDIUM` requires 4 CPUs, 8 GB memory and 8 GB storage
    resources.

    """
    LARGE = None
    """
    :attr:`SizeHint.LARGE` requires 8 CPUs, 12 GB memory and 8 GB storage
    resources.

    """
    X_LARGE = None
    """
    :attr:`SizeHint.X_LARGE` requires 16 CPUs, 16 GB memory and 8 GB storage
    resources.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`SizeHint` instance.
        """
        Enum.__init__(string)

SizeHint._set_values({
    'SMALL': SizeHint('SMALL'),
    'MEDIUM': SizeHint('MEDIUM'),
    'LARGE': SizeHint('LARGE'),
    'X_LARGE': SizeHint('X_LARGE'),
})
SizeHint._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.size_hint',
    SizeHint))




class DeploymentTarget(VapiStruct):
    """
    A ``DeploymentTarget`` describes how to deploy the vSphere Foundation Load
    Balancer.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 zones=None,
                 storage_policy=None,
                 deployment_size=None,
                 availability=None,
                ):
        """
        :type  zones: :class:`list` of :class:`str` or ``None``
        :param zones: The list of zones to deploy onto. 
            
            Currently only a single Supervisor Management Zone is supported. 
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``. When methods
            return a value of this class as a return value, the attribute will
            contain identifiers for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``.
            If no zones are provided, one will be chosen for you.
        :type  storage_policy: :class:`str` or ``None``
        :param storage_policy: Storage Policy containing datastores hosting the load balancer
            nodes.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``SpsStorageProfile``. When methods return a value of this class as
            a return value, the attribute will be an identifier for the
            resource type: ``SpsStorageProfile``.
            Defaults to the Supervisor's control plane Storage Policy.
        :type  deployment_size: :class:`SizeHint` or ``None``
        :param deployment_size: Determines the CPU/memory resource size of the load balancer
            deployment.
            This attribute was added in **vSphere API 9.0.0.0**.
            Defaults to :attr:`SizeHint.SMALL`.
        :type  availability: :class:`AvailabilityMode` or ``None``
        :param availability: Configures the availability level for the load balancer.
            This attribute was added in **vSphere API 9.0.0.0**.
            Defaults to :attr:`AvailabilityMode.ACTIVE_PASSIVE`.
        """
        self.zones = zones
        self.storage_policy = storage_policy
        self.deployment_size = deployment_size
        self.availability = availability
        VapiStruct.__init__(self)


DeploymentTarget._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.deployment_target', {
        'zones': type.OptionalType(type.ListType(type.IdType())),
        'storage_policy': type.OptionalType(type.IdType()),
        'deployment_size': type.OptionalType(type.ReferenceType(__name__, 'SizeHint')),
        'availability': type.OptionalType(type.ReferenceType(__name__, 'AvailabilityMode')),
    },
    DeploymentTarget,
    False,
    None))



class Network(VapiStruct):
    """
    A ``Network`` describes how packets from the load balancer reach their
    destinations.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'network_type',
            {
                'DVPG' : [('dvpg_network', True)],
                'SUPERVISOR_MANAGEMENT' : [],
                'PRIMARY_WORKLOAD' : [],
            }
        ),
    ]



    def __init__(self,
                 network_type=None,
                 dvpg_network=None,
                ):
        """
        :type  network_type: :class:`Network.NetworkType`
        :param network_type: The type of network this interface is attached to.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  dvpg_network: :class:`DistributedPortGroupNetwork`
        :param dvpg_network: A network defines how packets reach their destination.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``networkType`` is :attr:`Network.NetworkType.DVPG`.
        """
        self.network_type = network_type
        self.dvpg_network = dvpg_network
        VapiStruct.__init__(self)


    class NetworkType(Enum):
        """
        A ``Network.NetworkType`` determines which type of network this NIC is
        attached to.
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
        SUPERVISOR_MANAGEMENT = None
        """
        This network refers to the management network provided as Supervisor
        enablement
        :attr:`com.vmware.vcenter.namespace_management.supervisors_client.ControlPlane.network`.

        """
        PRIMARY_WORKLOAD = None
        """
        This network refers to the Supervisor default workload network provided at
        enablement
        :attr:`com.vmware.vcenter.namespace_management.supervisors_client.Workloads.network`.

        """
        DVPG = None
        """
        Refers to a custom ``DistributedPortGroupNetwork``.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`NetworkType` instance.
            """
            Enum.__init__(string)

    NetworkType._set_values({
        'SUPERVISOR_MANAGEMENT': NetworkType('SUPERVISOR_MANAGEMENT'),
        'PRIMARY_WORKLOAD': NetworkType('PRIMARY_WORKLOAD'),
        'DVPG': NetworkType('DVPG'),
    })
    NetworkType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.networks.edges.foundation.network.network_type',
        NetworkType))

Network._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.network', {
        'network_type': type.ReferenceType(__name__, 'Network.NetworkType'),
        'dvpg_network': type.OptionalType(type.ReferenceType(__name__, 'DistributedPortGroupNetwork')),
    },
    Network,
    False,
    None))



class DistributedPortGroupNetwork(VapiStruct):
    """
    ``DistributedPortGroupNetwork`` is a network backed by a single vSphere
    distributed port group.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'ipam',
            {
                'STATIC' : [('ip_config', True)],
                'DHCP' : [],
            }
        ),
    ]



    def __init__(self,
                 name=None,
                 network=None,
                 ipam=None,
                 ip_config=None,
                ):
        """
        :type  name: :class:`str`
        :param name: The user-facing name of the network. A Supervisor workload network
            will be created with this name. This name must be compliant with
            DNS naming specifications as stated in RFC 1123.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  network: :class:`str`
        :param network: Distributed Virtual Port Group identifier.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``vSphereDistributedPortGroup``. When methods return a value of
            this class as a return value, the attribute will be an identifier
            for the resource type: ``vSphereDistributedPortGroup``.
        :type  ipam: :class:`DistributedPortGroupNetwork.IPAMType`
        :param ipam: IP Address management scheme for this network.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  ip_config: :class:`IPConfig`
        :param ip_config: Configuration used to configure static IP addresses.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``ipam`` is :attr:`DistributedPortGroupNetwork.IPAMType.STATIC`.
        """
        self.name = name
        self.network = network
        self.ipam = ipam
        self.ip_config = ip_config
        VapiStruct.__init__(self)


    class IPAMType(Enum):
        """
        IP Address management scheme for this network.
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
        STATIC = None
        """
        IP addresses are statically allocated.

        """
        DHCP = None
        """
        IP addresses are acquired through a DHCP server via the DHCP protocol.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`IPAMType` instance.
            """
            Enum.__init__(string)

    IPAMType._set_values({
        'STATIC': IPAMType('STATIC'),
        'DHCP': IPAMType('DHCP'),
    })
    IPAMType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.networks.edges.foundation.distributed_port_group_network.IPAM_type',
        IPAMType))

DistributedPortGroupNetwork._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.distributed_port_group_network', {
        'name': type.StringType(),
        'network': type.IdType(resource_types='vSphereDistributedPortGroup'),
        'ipam': type.ReferenceType(__name__, 'DistributedPortGroupNetwork.IPAMType'),
        'ip_config': type.OptionalType(type.ReferenceType(__name__, 'IPConfig')),
    },
    DistributedPortGroupNetwork,
    False,
    None))



class FoundationIPRange(VapiStruct):
    """
    ``FoundationIPRange`` defines a contiguous set of IP addresses in the
    context of a Foundation Load Balancer.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 address=None,
                 count=None,
                ):
        """
        :type  address: :class:`str`
        :param address: :attr:`FoundationIPRange.address` is the starting IP address.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  count: :class:`long`
        :param count: :attr:`FoundationIPRange.count` is number of IP addresses in the
            range. 
            
            For example: 
            
            * A /24 subnet will have a count of 256.
            * A /24 subnet with a gateway address and a broadcast address will
              have a count of 254.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.address = address
        self.count = count
        VapiStruct.__init__(self)


FoundationIPRange._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.foundation_IP_range', {
        'address': type.StringType(),
        'count': type.IntegerType(),
    },
    FoundationIPRange,
    False,
    None))



class IPConfig(VapiStruct):
    """
    ``IPConfig`` encapsulates configuration required to enable the load
    balancer on static IP networks.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ip_ranges=None,
                 gateway=None,
                ):
        """
        :type  ip_ranges: :class:`list` of :class:`FoundationIPRange`
        :param ip_ranges: IP ranges will be used to provision IP addresses for nodes on a
            network. You must supply at least one IP address per network
            override per node. The IP addresses must exist within the same
            subnet as the provided gateway. 
            
            If you want to scale up the number of load balancer nodes, you must
            have enough free IP addresses present in the pool on each
            respective network. To deploy a load balancer, one IP address is
            required for each node on each network. For example, if deploying
            in HA configuration, you must supply two IP addresses for each
            network for a total of four IP addresses.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  gateway: :class:`str`
        :param gateway: A gateway is the default gateway on a network specified in CIDR
            notation. E.g. 192.168.0.1/24. IP addresses specified in
            :attr:`IPConfig.ip_ranges` must be contained within the same subnet
            as this gateway.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.ip_ranges = ip_ranges
        self.gateway = gateway
        VapiStruct.__init__(self)


IPConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.IP_config', {
        'ip_ranges': type.ListType(type.ReferenceType(__name__, 'FoundationIPRange')),
        'gateway': type.StringType(),
    },
    IPConfig,
    False,
    None))



class NetworkInterface(VapiStruct):
    """
    A ``NetworkInterface`` defines how a load balancer will be connected to a
    network.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 personas=None,
                 network=None,
                ):
        """
        :type  personas: :class:`list` of :class:`Persona`
        :param personas: The list of interface personas. 
            
            An interface must have at least one persona and may have additional
            *distinct* personas. 
            
            For example, an interface with Management Persona, Workload
            Persona, and Frontend Personas will configure the load balancer to
            put load balancer IPs on the same interface that will be used to
            reach workloads and other load balancer nodes. An interface
            configured with only a Frontend Persona will allow ingress and
            return traffic to exit that interface while relying on different
            interfaces for management traffic and workload traffic.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  network: :class:`Network`
        :param network: A network defines how packets reach their destination from this
            interface.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.personas = personas
        self.network = network
        VapiStruct.__init__(self)


NetworkInterface._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.network_interface', {
        'personas': type.ListType(type.ReferenceType(__name__, 'Persona')),
        'network': type.ReferenceType(__name__, 'Network'),
    },
    NetworkInterface,
    False,
    None))



class NetworkServices(VapiStruct):
    """
    ``NetworkServices`` contains external services on a network that the load
    balancer is eligible to interact with.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 dns=None,
                 ntp=None,
                 syslog=None,
                ):
        """
        :type  dns: :class:`DNS` or ``None``
        :param dns: Domain Name Service configuration.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, and the interface configured with a Management Persona is
            connected to a DHCP network, it will attempt to obtain its settings
            from a DHCP server. If the interface configured with a Management
            Persona is connected to a static IP network, the values will be
            synced with the Supervisor's management services
            :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
        :type  ntp: :class:`NTP` or ``None``
        :param ntp: Network Time Protocol configuration.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, and the interface configured with a Management Persona is
            connected to a DHCP network, it will attempt to obtain its settings
            from a DHCP server. If the interface configured with a Management
            Persona is connected to a static IP network, the values will be
            synced with the Supervisor's management services
            :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
        :type  syslog: :class:`Syslog` or ``None``
        :param syslog: Configure remote log forwarding for all load balancer nodes.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None logs will be persisted locally and can be retrieved through
            the Supervisor support bundle collection APIs.
        """
        self.dns = dns
        self.ntp = ntp
        self.syslog = syslog
        VapiStruct.__init__(self)


NetworkServices._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.network_services', {
        'dns': type.OptionalType(type.ReferenceType(__name__, 'DNS')),
        'ntp': type.OptionalType(type.ReferenceType(__name__, 'NTP')),
        'syslog': type.OptionalType(type.ReferenceType(__name__, 'Syslog')),
    },
    NetworkServices,
    False,
    None))



class DNS(VapiStruct):
    """
    ``DNS`` describes DNS servers and search domains for a given network.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 servers=None,
                 search_domains=None,
                ):
        """
        :type  servers: :class:`list` of :class:`str`
        :param servers: :attr:`DNS.servers` is a list of IP addresses that clients may use
            for DNS resolution on a given network in priority order. 
            
            If None, and the interface configured with a Management Persona is
            connected to a DHCP network, it will attempt to obtain its settings
            from a DHCP server. If the interface configured with a Management
            Persona is connected to a static IP network, the values will be
            synced with the Supervisor's management services
            :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  search_domains: :class:`list` of :class:`str`
        :param search_domains: :attr:`DNS.search_domains` is a list of DNS search domains to be
            used on this network. 
            
            This field is useful for corporate networks or local domains that
            are not publicly resolvable. 
            
            If None, and the interface configured with a Management Persona is
            connected to a DHCP network, it will attempt to obtain its settings
            from a DHCP server. If the interface configured with a Management
            Persona is connected to a static IP network, the values will be
            synced with the Supervisor's management services
            :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.servers = servers
        self.search_domains = search_domains
        VapiStruct.__init__(self)


DNS._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.DNS', {
        'servers': type.ListType(type.StringType()),
        'search_domains': type.ListType(type.StringType()),
    },
    DNS,
    False,
    None))



class NTP(VapiStruct):
    """
    ``NTP`` describes network time protocol configuration for a network.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 servers=None,
                ):
        """
        :type  servers: :class:`list` of :class:`str`
        :param servers: :attr:`NTP.servers` contains a list of servers in priority order
            that clients can use for network time protocol. 
            
            If None, and the interface configured with a Management Persona is
            connected to a DHCP network, it will attempt to obtain its settings
            from a DHCP server. If the interface configured with a Management
            Persona is connected to a static IP network, the values will be
            synced with the Supervisor's management services
            :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.servers = servers
        VapiStruct.__init__(self)


NTP._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.NTP', {
        'servers': type.ListType(type.StringType()),
    },
    NTP,
    False,
    None))



class Syslog(VapiStruct):
    """
    A ``Syslog`` configuration defines how logs are exported using the syslog
    protocol.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 endpoint=None,
                 certificate_authority_pem=None,
                ):
        """
        :type  endpoint: :class:`str` or ``None``
        :param endpoint: FQDN or IP address of the remote syslog server taking the form
            ``protocol://hostname|ipv4|ipv6[:port]``. The syslog protocol
            defaults to tcp.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None logs will be persisted locally.
        :type  certificate_authority_pem: :class:`str` or ``None``
        :param certificate_authority_pem: The Certificate Authority certificate can be provided in PEM format
            to validate the :attr:`Syslog.endpoint` when using a TLS protocol.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None no validation will be performed.
        """
        self.endpoint = endpoint
        self.certificate_authority_pem = certificate_authority_pem
        VapiStruct.__init__(self)


Syslog._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.foundation.syslog', {
        'endpoint': type.OptionalType(type.StringType()),
        'certificate_authority_pem': type.OptionalType(type.StringType()),
    },
    Syslog,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

