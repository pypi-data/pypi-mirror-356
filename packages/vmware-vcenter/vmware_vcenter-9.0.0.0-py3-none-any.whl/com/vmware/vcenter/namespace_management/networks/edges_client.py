# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.edges.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.networks.edges_client`` module
provides classes and classes to manage Edge resources.

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

class LoadBalancerSize(Enum):
    """
    The ``LoadBalancerSize`` class enumerates load balancer sizes supported by
    NSX.
    This enumeration was added in **vSphere API 8.0.0.1**.

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
    :attr:`LoadBalancerSize.SMALL` is a load balancer that hosts up to 20
    virtual servers.

    """
    MEDIUM = None
    """
    :attr:`LoadBalancerSize.MEDIUM` is a load balancer that hosts up to 100
    virtual servers.

    """
    LARGE = None
    """
    :attr:`LoadBalancerSize.LARGE` is a load balancer that hosts up to 1000
    virtual servers.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`LoadBalancerSize` instance.
        """
        Enum.__init__(string)

LoadBalancerSize._set_values({
    'SMALL': LoadBalancerSize('SMALL'),
    'MEDIUM': LoadBalancerSize('MEDIUM'),
    'LARGE': LoadBalancerSize('LARGE'),
})
LoadBalancerSize._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.load_balancer_size',
    LoadBalancerSize))



class NSXRoutingMode(Enum):
    """
    ``NSXRoutingMode`` enum defines an enumeration of available routing modes.
    This enumeration was added in **vSphere API 8.0.0.1**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    ROUTED = None
    """
    :attr:`NSXRoutingMode.ROUTED` configures NSX to route directly to Pods
    cluster IP addresses.

    """
    NAT = None
    """
    :attr:`NSXRoutingMode.NAT` uses network address translation and the
    :attr:`NSXConfig.egress_ip_ranges` to route traffic out of the cluster.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`NSXRoutingMode` instance.
        """
        Enum.__init__(string)

NSXRoutingMode._set_values({
    'ROUTED': NSXRoutingMode('ROUTED'),
    'NAT': NSXRoutingMode('NAT'),
})
NSXRoutingMode._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.NSX_routing_mode',
    NSXRoutingMode))



class EdgeProvider(Enum):
    """
    ``EdgeProvider`` describes the supported available edge services.
    This enumeration was added in **vSphere API 8.0.0.1**.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    HAPROXY = None
    """
    :attr:`EdgeProvider.HAPROXY` is an HAProxy load balancer fronted by the
    Data Plane API. This provider is only compatible with Supervisors
    configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.VSPHERE`.

    .. deprecated:: vSphere API 9.0.0.0
        This class attribute is deprecated as of **vSphere API 9.0.0.0**. Use
        :attr:`EdgeProvider.VSPHERE_FOUNDATION` or
        :attr:`EdgeProvider.NSX_ADVANCED` instead.

    """
    NSX = None
    """
    :attr:`EdgeProvider.NSX` specifies NSX-managed edge services. This provider
    is only compatible with Supervisors configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSXT`.
    
    With this provider, an edge configuration managed by NSX will be
    automatically detected by the Supervisor. Upon edge detection, either edge
    provider
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_LB`,
    or if entitled to NSX Advanced Load Balancer (Avi Load Balancer), then
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_REGISTERED_AVI`,
    will be configured.

    """
    NSX_ADVANCED = None
    """
    :attr:`EdgeProvider.NSX_ADVANCED` specifies the NSX Advanced Load Balancer
    and Ingress. This provider is only compatible with Supervisors configured
    with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.VSPHERE`.
    :attr:`EdgeProvider.NSX_ADVANCED` maps to edge provider
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`
    after Supervisor enablement.

    """
    NSX_VPC = None
    """
    :attr:`EdgeProvider.NSX_VPC` specifies NSX-managed edge services with
    support for Virtual Private Clouds (VPCs). This provider is only compatible
    with Supervisors configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSX_VPC`.
    
    With this provider, an edge configuration managed by NSX will be
    automatically detected by the Supervisor. Upon edge detection, either edge
    provider
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_LB`,
    or if entitled to NSX Advanced Load Balancer (Avi Load Balancer), then
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_REGISTERED_AVI`,
    will be configured.
    This class attribute was added in **vSphere API 9.0.0.0**.

    """
    VSPHERE_FOUNDATION = None
    """
    :attr:`EdgeProvider.VSPHERE_FOUNDATION` specifies the vSphere Foundation
    Load Balancer. This provider is only compatible with Supervisors configured
    with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.VSPHERE`.
    This class attribute was added in **vSphere API 9.0.0.0**.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`EdgeProvider` instance.
        """
        Enum.__init__(string)

EdgeProvider._set_values({
    'HAPROXY': EdgeProvider('HAPROXY'),
    'NSX': EdgeProvider('NSX'),
    'NSX_ADVANCED': EdgeProvider('NSX_ADVANCED'),
    'NSX_VPC': EdgeProvider('NSX_VPC'),
    'VSPHERE_FOUNDATION': EdgeProvider('VSPHERE_FOUNDATION'),
})
EdgeProvider._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.networks.edges.edge_provider',
    EdgeProvider))




class Edge(VapiStruct):
    """
    ``Edge`` class contains configuration for network traffic entering and
    exiting a Supervisor.
    This class was added in **vSphere API 8.0.0.1**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'provider',
            {
                'HAPROXY' : [('haproxy', True)],
                'NSX' : [('nsx', True)],
                'NSX_ADVANCED' : [('nsx_advanced', True)],
                'VSPHERE_FOUNDATION' : [('foundation', False)],
                'NSX_VPC' : [],
            }
        ),
    ]



    def __init__(self,
                 id=None,
                 load_balancer_address_ranges=None,
                 haproxy=None,
                 nsx=None,
                 nsx_advanced=None,
                 foundation=None,
                 provider=None,
                ):
        """
        :type  id: :class:`str` or ``None``
        :param id: :attr:`Edge.id` is a unique identifier that can be referenced for
            updates.
            This attribute was added in **vSphere API 8.0.0.1**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.network.edge.Edge``. When
            methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.network.edge.Edge``.
            If unset, an ID will be automatically generated.
        :type  load_balancer_address_ranges: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks_client.IPRange` or ``None``
        :param load_balancer_address_ranges: 
            
            :attr:`Edge.load_balancer_address_ranges` defines the list of
            addresses that a load balancer can consume to publish Kubernetes
            services. This range must contain at least one IP address unless
            the NSX Advanced provider is selected. It is recommended to supply
            a large enough range to support load balancers requested for pods
            in the control plane and Kubernetes Clusters.
            This attribute was added in **vSphere API 8.0.0.1**.
            This field must be set if :attr:`Edge.provider` is not an NSX
            Advanced Load Balancer.
        :type  haproxy: :class:`HAProxyConfig`
        :param haproxy: :attr:`Edge.haproxy` defines configuration for the HAProxy Load
            Balancer.
            This attribute was added in **vSphere API 8.0.0.1**.
            This attribute is optional and it is only relevant when the value
            of ``provider`` is :attr:`EdgeProvider.HAPROXY`.

            .. deprecated:: vSphere API 9.0.0.0
                This attribute is deprecated as of **vSphere API 9.0.0.0**.
                Instead, use :attr:`Edge.foundation` with provider type
                :attr:`EdgeProvider.VSPHERE_FOUNDATION` or
                :attr:`Edge.nsx_advanced` with provider type
                :attr:`EdgeProvider.NSX_ADVANCED`.
        :type  nsx: :class:`NSXConfig`
        :param nsx: :attr:`Edge.nsx` defines configuration for the NSX Load Balancer.
            This attribute was added in **vSphere API 8.0.0.1**.
            This attribute is optional and it is only relevant when the value
            of ``provider`` is :attr:`EdgeProvider.NSX`.
        :type  nsx_advanced: :class:`NSXAdvancedLBConfig`
        :param nsx_advanced: :attr:`Edge.nsx_advanced` defines configuration for the NSX
            Advanced Load Balancer and Ingress Software.
            This attribute was added in **vSphere API 8.0.0.1**.
            This attribute is optional and it is only relevant when the value
            of ``provider`` is :attr:`EdgeProvider.NSX_ADVANCED`.
        :type  foundation: :class:`VsphereFoundationConfig`
        :param foundation: :attr:`Edge.foundation` defines configuration for the vSphere
            Foundation Load Balancer
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``provider`` is :attr:`EdgeProvider.VSPHERE_FOUNDATION`.
        :type  provider: :class:`EdgeProvider` or ``None``
        :param provider: :attr:`Edge.provider` specifies the vendor providing edge services.
            This attribute was added in **vSphere API 8.0.0.1**.
            If None, there will be no edge services provider in this
            Supervisor.
        """
        self.id = id
        self.load_balancer_address_ranges = load_balancer_address_ranges
        self.haproxy = haproxy
        self.nsx = nsx
        self.nsx_advanced = nsx_advanced
        self.foundation = foundation
        self.provider = provider
        VapiStruct.__init__(self)


Edge._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.edge', {
        'id': type.OptionalType(type.IdType()),
        'load_balancer_address_ranges': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks_client', 'IPRange'))),
        'haproxy': type.OptionalType(type.ReferenceType(__name__, 'HAProxyConfig')),
        'nsx': type.OptionalType(type.ReferenceType(__name__, 'NSXConfig')),
        'nsx_advanced': type.OptionalType(type.ReferenceType(__name__, 'NSXAdvancedLBConfig')),
        'foundation': type.OptionalType(type.ReferenceType(__name__, 'VsphereFoundationConfig')),
        'provider': type.OptionalType(type.ReferenceType(__name__, 'EdgeProvider')),
    },
    Edge,
    False,
    None))



class NSXAdvancedLBConfig(VapiStruct):
    """
    ``NSXAdvancedLBConfig`` class is used to describe the NSX Advanced Load
    Balancer configuration.
    This class was added in **vSphere API 8.0.0.1**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 server=None,
                 username=None,
                 password=None,
                 certificate_authority_chain=None,
                 cloud_name=None,
                ):
        """
        :type  server: :class:`Server`
        :param server: :attr:`NSXAdvancedLBConfig.server` is the address for the Avi
            Controller, used to configure Virtual Servers.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  username: :class:`str`
        :param username: :attr:`NSXAdvancedLBConfig.username` is used by the Avi Kubernetes
            Operator to program the Avi Controller.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  password: :class:`str`
        :param password: :attr:`NSXAdvancedLBConfig.password` is the password for the
            username.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  certificate_authority_chain: :class:`str`
        :param certificate_authority_chain: :attr:`NSXAdvancedLBConfig.certificate_authority_chain` contains
            PEM-encoded CA chain which is used to verify x509 certificates
            received from the server.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  cloud_name: :class:`str` or ``None``
        :param cloud_name: The cloud name for the Avi Controller.
            This attribute was added in **vSphere API 8.0.2.00300**.
            Only :class:`set` if custom cloud name is configured for this Avi
            Controller. If None, it defaults to "Default-Cloud".
        """
        self.server = server
        self.username = username
        self.password = password
        self.certificate_authority_chain = certificate_authority_chain
        self.cloud_name = cloud_name
        VapiStruct.__init__(self)


NSXAdvancedLBConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.NSX_advanced_LB_config', {
        'server': type.ReferenceType(__name__, 'Server'),
        'username': type.StringType(),
        'password': type.SecretType(),
        'certificate_authority_chain': type.StringType(),
        'cloud_name': type.OptionalType(type.StringType()),
    },
    NSXAdvancedLBConfig,
    False,
    None))



class HAProxyConfig(VapiStruct):
    """
    ``HAProxyConfig`` class describes configuration for the HAProxy Load
    Balancer.
    This class was added in **vSphere API 8.0.0.1**.

    .. deprecated:: vSphere API 9.0.0.0
        This class is deprecated as of **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 servers=None,
                 username=None,
                 password=None,
                 certificate_authority_chain=None,
                ):
        """
        :type  servers: :class:`list` of :class:`Server`
        :param servers: :attr:`HAProxyConfig.servers` is a list of the addresses for the
            data plane API servers used to configure Virtual Servers.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  username: :class:`str`
        :param username: :attr:`HAProxyConfig.username` is used by the HAProxy Kubernetes
            Operator to program the HAProxy Controller.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  password: :class:`str`
        :param password: :attr:`HAProxyConfig.password` secures the
            :attr:`HAProxyConfig.username`.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  certificate_authority_chain: :class:`str`
        :param certificate_authority_chain: :attr:`HAProxyConfig.certificate_authority_chain` contains
            PEM-encoded CA chain which is used to verify x509 certificates
            received from the server.
            This attribute was added in **vSphere API 8.0.0.1**.
        """
        warn('com.vmware.vcenter.namespace_management.networks.edges.HAProxyConfig is deprecated as of release vSphere API 9.0.0.0.', DeprecationWarning)
        self.servers = servers
        self.username = username
        self.password = password
        self.certificate_authority_chain = certificate_authority_chain
        VapiStruct.__init__(self)


HAProxyConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.HA_proxy_config', {
        'servers': type.ListType(type.ReferenceType(__name__, 'Server')),
        'username': type.StringType(),
        'password': type.SecretType(),
        'certificate_authority_chain': type.StringType(),
    },
    HAProxyConfig,
    False,
    None))



class NSXConfig(VapiStruct):
    """
    ``NSXConfig`` class describes the configuration for NSX Edge services.
    This class was added in **vSphere API 8.0.0.1**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'routing_mode',
            {
                'NAT' : [('egress_IP_ranges', True)],
                'ROUTED' : [],
            }
        ),
    ]


    _canonical_to_pep_names = {
                            'edge_cluster_ID': 'edge_cluster_id',
                            'default_ingress_TLS_certificate': 'default_ingress_tls_certificate',
                            'egress_IP_ranges': 'egress_ip_ranges',
                            }

    def __init__(self,
                 edge_cluster_id=None,
                 default_ingress_tls_certificate=None,
                 routing_mode=None,
                 egress_ip_ranges=None,
                 t0_gateway=None,
                 load_balancer_size=None,
                ):
        """
        :type  edge_cluster_id: :class:`str` or ``None``
        :param edge_cluster_id: :attr:`NSXConfig.edge_cluster_id` defines the NSX Edge Cluster to
            be used for Kubernetes Services of type LoadBalancer, Kubernetes
            Ingresses, and NSX SNAT.
            This attribute was added in **vSphere API 8.0.0.1**.
            Defaults to a the edge cluster created earliest.
        :type  default_ingress_tls_certificate: :class:`str` or ``None``
        :param default_ingress_tls_certificate: :attr:`NSXConfig.default_ingress_tls_certificate` defines a default
            certificate that is served on Ingress services, when another
            certificate is not presented. This configuration applies to all
            namespaces by default.
            This attribute was added in **vSphere API 8.0.0.1**.
            If unset, there will be no certificate served on Ingress.
        :type  routing_mode: :class:`NSXRoutingMode` or ``None``
        :param routing_mode: :attr:`NSXConfig.routing_mode` enables the network topology in
            either NAT mode or Routed Mode. Enabling routed mode will result in
            all the workloads i.e vSphere PODs, VMs and Kubernetes Clusters
            Node IPs to be directly accessible from networks beyond the Tier-0
            router. Once a namespace mode is applied, it cannot be changed.
            This attribute was added in **vSphere API 8.0.0.1**.
            The default setting is NAT mode.
        :type  egress_ip_ranges: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks_client.IPRange`
        :param egress_ip_ranges: :attr:`NSXConfig.egress_ip_ranges` lists the IP Ranges from which
            NSX assigns IP addresses used for performing SNAT from container
            IPs to external IPs. These ranges must not overlap with other IP
            ranges on this network.
            This attribute was added in **vSphere API 8.0.0.1**.
            If this range is empty, network traffic will not be able to exit
            the cluster.
        :type  t0_gateway: :class:`str` or ``None``
        :param t0_gateway: :attr:`NSXConfig.t0_gateway` specifies the default Tier-0 gateway
            ID for the namespaces configuration.
            This attribute was added in **vSphere API 8.0.0.1**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``NSXTier0Gateway``. When methods return a value of this class as a
            return value, the attribute will be an identifier for the resource
            type: ``NSXTier0Gateway``.
            If unset, the default Tier-0 gateway from the edge cluster is used.
        :type  load_balancer_size: :class:`LoadBalancerSize` or ``None``
        :param load_balancer_size: :attr:`NSXConfig.load_balancer_size` describes the load balancer
            sizing options available. Larger sizes support more active virtual
            servers, but consume more resources.
            This attribute was added in **vSphere API 8.0.0.1**.
            If unset, the size defaults to small.
        """
        self.edge_cluster_id = edge_cluster_id
        self.default_ingress_tls_certificate = default_ingress_tls_certificate
        self.routing_mode = routing_mode
        self.egress_ip_ranges = egress_ip_ranges
        self.t0_gateway = t0_gateway
        self.load_balancer_size = load_balancer_size
        VapiStruct.__init__(self)


NSXConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.NSX_config', {
        'edge_cluster_ID': type.OptionalType(type.StringType()),
        'default_ingress_TLS_certificate': type.OptionalType(type.StringType()),
        'routing_mode': type.OptionalType(type.ReferenceType(__name__, 'NSXRoutingMode')),
        'egress_IP_ranges': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks_client', 'IPRange'))),
        't0_gateway': type.OptionalType(type.IdType()),
        'load_balancer_size': type.OptionalType(type.ReferenceType(__name__, 'LoadBalancerSize')),
    },
    NSXConfig,
    False,
    None))



class VsphereFoundationConfig(VapiStruct):
    """
    ``VsphereFoundationConfig`` class contains configuration for enabling a
    vSphere Foundation Load Balancer to load balance Supervisor workload
    traffic.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 deployment_target=None,
                 interfaces=None,
                 network_services=None,
                ):
        """
        :type  deployment_target: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.DeploymentTarget` or ``None``
        :param deployment_target: Customize the placement of the Load Balancer.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, the load balancer will be placed using its default
            configuration. See fields in
            :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.DeploymentTarget`
            for a description of each default configuration.
        :type  interfaces: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.NetworkInterface` or ``None``
        :param interfaces: Customize the network interfaces of the Load Balancer. For details,
            see
            :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.Persona`
            
            Supported network interface/persona combinations currently include:
            
            * One interface with combined Frontend and Management Personas
            * One interface with Management Persona, one interface with
              Frontend Persona
            * One interface with Management Persona, one interface with
              Frontend Persona, one interface with Backend Persona
            This attribute was added in **vSphere API 9.0.0.0**.
            If no interfaces are configured, then the load balancer will be
            attached to the Supervisor's management and workload networks when
            applicable. 
            
            If a Supervisor is provisioned with two networks, the following
            interface configuration is created: 
            
            +-----------------+------------------------------------+-------------------------------+
            | Interface Index | Persona(s)                         | Network   
            |
            +-----------------+------------------------------------+-------------------------------+
            | 1               | Management Persona                 | Supervisor
            Management Network |
            +-----------------+------------------------------------+-------------------------------+
            | 2               | Workload Persona, Frontend Persona | Supervisor
            Workload Network   |
            +-----------------+------------------------------------+-------------------------------+
            In this context management traffic is isolated from workload and
            load balancer traffic. 
            
            If a Supervisor is provisioned with one network, the following
            interface configuration is created. 
            
            +-----------------+--------------------------------------------------------+-----------------------------+
            | Interface Index | Persona(s)                                     
            | Network                     |
            +-----------------+--------------------------------------------------------+-----------------------------+
            | 1               | Management Persona, Workload Persona, Frontend
            Persona | Supervisor Workload Network |
            +-----------------+--------------------------------------------------------+-----------------------------+
            In this context a single interface is used for management,
            workload, and load balancer traffic. 
        :type  network_services: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.NetworkServices` or ``None``
        :param network_services: Configure network services for this load balancer. Network services
            increase the reliability of your load balancer. 
            
            Network services must be accessible from a network interface with a
            Management Persona.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, and :attr:`VsphereFoundationConfig.interfaces` is unset,
            the load balancer will inherit settings from the Supervisor. If the
            an interface configured with a Management Persona is connected to a
            DHCP network, it will attempt to obtain its settings from a DHCP
            server. Otherwise, no services will be configured. 
            
            **Availability of your load balancer may be reduced if network
            services are not configured. Therefore, it is highly recommended
            you ensure that network services are configured for your load
            balancer.**
        """
        self.deployment_target = deployment_target
        self.interfaces = interfaces
        self.network_services = network_services
        VapiStruct.__init__(self)


VsphereFoundationConfig._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.vsphere_foundation_config', {
        'deployment_target': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'DeploymentTarget')),
        'interfaces': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'NetworkInterface'))),
        'network_services': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'NetworkServices')),
    },
    VsphereFoundationConfig,
    False,
    None))



class Server(VapiStruct):
    """
    A ``Server`` class represents an endpoint used to configure load balancers.
    This class was added in **vSphere API 8.0.0.1**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 host=None,
                 port=None,
                ):
        """
        :type  host: :class:`str`
        :param host: :attr:`Server.host` specifies a the management hostname or IPv4
            address for a load balancer.
            This attribute was added in **vSphere API 8.0.0.1**.
        :type  port: :class:`long`
        :param port: :attr:`Server.port` specifies a management port used to access a
            load balancer.
            This attribute was added in **vSphere API 8.0.0.1**.
        """
        self.host = host
        self.port = port
        VapiStruct.__init__(self)


Server._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.edges.server', {
        'host': type.StringType(),
        'port': type.IntegerType(),
    },
    Server,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
        'foundation': 'com.vmware.vcenter.namespace_management.networks.edges.foundation_client.StubFactory',
    }

