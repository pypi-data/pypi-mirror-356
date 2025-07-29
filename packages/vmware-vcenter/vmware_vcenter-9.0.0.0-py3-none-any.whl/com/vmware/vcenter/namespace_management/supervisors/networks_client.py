# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.supervisors.networks.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.supervisors.networks_client``
module provides classes for Supervisor network configuration.

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


class NetworkSegment(VapiStruct):
    """
    ``NetworkSegment`` class represents a layer 2 broadcast domain.
    This class was added in **vSphere API 8.0.3.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 networks=None,
                ):
        """
        :type  networks: :class:`list` of :class:`str`
        :param networks: List of Standard Port Groups or Distributed Virtual Port Groups or
            Opaque Network identifiers that are part of the same layer 2
            broadcast domain.
            This attribute was added in **vSphere API 8.0.3.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``Network``. When methods return a value of this class as a return
            value, the attribute will contain identifiers for the resource
            type: ``Network``.
        """
        self.networks = networks
        VapiStruct.__init__(self)


NetworkSegment._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.networks.network_segment', {
        'networks': type.ListType(type.IdType()),
    },
    NetworkSegment,
    False,
    None))



class Edges(VapiInterface):
    """
    The ``Edges`` class enables users to create, update, or delete edge
    appliances including load balancers.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.supervisors.networks.edges'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EdgesStub)
        self._VAPI_OPERATION_IDS = {}

    class FoundationLoadBalancerUpdateAvailabilityMode(Enum):
        """
        The ``Edges.FoundationLoadBalancerUpdateAvailabilityMode`` defines
        parameters for update.
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

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`FoundationLoadBalancerUpdateAvailabilityMode` instance.
            """
            Enum.__init__(string)

    FoundationLoadBalancerUpdateAvailabilityMode._set_values({
        'ACTIVE_PASSIVE': FoundationLoadBalancerUpdateAvailabilityMode('ACTIVE_PASSIVE'),
    })
    FoundationLoadBalancerUpdateAvailabilityMode._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_update_availability_mode',
        FoundationLoadBalancerUpdateAvailabilityMode))


    class Info(VapiStruct):
        """
        ``Edges.Info`` describes the current state of an edge.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'provider',
                {
                    'AVI' : [('avi', True)],
                    'HAPROXY' : [('haproxy', True)],
                    'VSPHERE_FOUNDATION' : [('foundation', False)],
                    'NSX_LB' : [('nsx', False)],
                    'NSX_REGISTERED_AVI' : [],
                }
            ),
        ]



        def __init__(self,
                     edge=None,
                     name=None,
                     provider=None,
                     avi=None,
                     haproxy=None,
                     foundation=None,
                     nsx=None,
                    ):
            """
            :type  edge: :class:`str`
            :param edge: The identifier of this edge.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.network.edge.Edge``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.network.edge.Edge``.
            :type  name: :class:`str`
            :param name: The human-readable descriptor of this edge.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  provider: :class:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider`
            :param provider: The edge provider.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  avi: :class:`Edges.AviInfo`
            :param avi: The ``Edges.AviInfo`` is a conditional configuration made available
                upon selecting the Avi load balancer provider. It is used to
                retrieve the load balancer runtime configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`.
            :type  haproxy: :class:`Edges.HAProxyInfo`
            :param haproxy: The ``Edges.HAProxyInfo`` is a conditional configuration made
                available upon selecting the HAProxy load balancer provider. It is
                used to retrieve the load balancer runtime configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.HAPROXY`.

                .. deprecated:: vSphere API 9.0.0.0
                    This attribute is deprecated as of **vSphere API 9.0.0.0**.
                    Instead, use :attr:`Edges.Info.foundation` with provider type
                    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.VSPHERE_FOUNDATION`
                    or :attr:`Edges.Info.avi` with provider type
                    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`.
            :type  foundation: :class:`Edges.FoundationLoadBalancerInfo`
            :param foundation: The ``Edges.FoundationLoadBalancerInfo`` is a conditional
                configuration made available upon selecting the Foundation Load
                Balancer provider. It is used to retrieve the load balancer runtime
                configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.VSPHERE_FOUNDATION`.
            :type  nsx: :class:`Edges.NSXLoadBalancerInfo`
            :param nsx: The ``Edges.NSXLoadBalancerInfo`` represents information about the
                NSX Load Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_LB`.
            """
            self.edge = edge
            self.name = name
            self.provider = provider
            self.avi = avi
            self.haproxy = haproxy
            self.foundation = foundation
            self.nsx = nsx
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.info', {
            'edge': type.IdType(resource_types='com.vmware.vcenter.namespace_management.network.edge.Edge'),
            'name': type.StringType(),
            'provider': type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors.networks.edges_client', 'EdgeProvider'),
            'avi': type.OptionalType(type.ReferenceType(__name__, 'Edges.AviInfo')),
            'haproxy': type.OptionalType(type.ReferenceType(__name__, 'Edges.HAProxyInfo')),
            'foundation': type.OptionalType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerInfo')),
            'nsx': type.OptionalType(type.ReferenceType(__name__, 'Edges.NSXLoadBalancerInfo')),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        ``Edges.CreateSpec`` defines parameters for creating an edge.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'provider',
                {
                    'AVI' : [('avi', True)],
                    'VSPHERE_FOUNDATION' : [('foundation', False)],
                    'HAPROXY' : [],
                    'NSX_LB' : [],
                    'NSX_REGISTERED_AVI' : [],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     provider=None,
                     avi=None,
                     foundation=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of this edge. The name must be an RFC 1123 compatible DNS
                name.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  provider: :class:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider`
            :param provider: The edge provider.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  avi: :class:`Edges.AviCreateSpec`
            :param avi: The ``Edges.AviCreateSpec`` is a conditional configuration that
                must be provided when FLB provider is selected. It is used to
                create a new load balancer configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`.
            :type  foundation: :class:`Edges.FoundationLoadBalancerCreateSpec`
            :param foundation: The ``Edges.FoundationLoadBalancerCreateSpec`` is a conditional
                configuration that must be provided when FLB provider is selected.
                It is used to create a new load balancer configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.VSPHERE_FOUNDATION`.
            """
            self.name = name
            self.provider = provider
            self.avi = avi
            self.foundation = foundation
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.create_spec', {
            'name': type.StringType(),
            'provider': type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors.networks.edges_client', 'EdgeProvider'),
            'avi': type.OptionalType(type.ReferenceType(__name__, 'Edges.AviCreateSpec')),
            'foundation': type.OptionalType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerCreateSpec')),
        },
        CreateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        ``Edges.UpdateSpec`` defines parameters for updating an edge.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'provider',
                {
                    'AVI' : [('avi', True)],
                    'HAPROXY' : [('haproxy', True)],
                    'VSPHERE_FOUNDATION' : [('foundation', False)],
                    'NSX_LB' : [('nsx', False)],
                    'NSX_REGISTERED_AVI' : [],
                }
            ),
        ]



        def __init__(self,
                     provider=None,
                     avi=None,
                     haproxy=None,
                     foundation=None,
                     nsx=None,
                    ):
            """
            :type  provider: :class:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider`
            :param provider: The edge provider.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  avi: :class:`Edges.AviUpdateSpec`
            :param avi: The ``Edges.AviUpdateSpec`` is a conditional configuration made
                available upon selecting the Avi load balancer provider. It is used
                to configure the load balancer at run time.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`.
            :type  haproxy: :class:`Edges.HAProxyUpdateSpec`
            :param haproxy: The ``Edges.HAProxyUpdateSpec`` is a conditional configuration made
                available upon selecting the HAProxy load balancer provider. It is
                used to configure the load balancer at run time.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.HAPROXY`.

                .. deprecated:: vSphere API 9.0.0.0
                    This attribute is deprecated as of **vSphere API 9.0.0.0**.
                    Instead, use :attr:`Edges.UpdateSpec.foundation` with provider
                    type
                    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.VSPHERE_FOUNDATION`
                    or :attr:`Edges.UpdateSpec.avi` with provider type
                    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.AVI`.
            :type  foundation: :class:`Edges.FoundationLoadBalancerUpdateSpec`
            :param foundation: The ``Edges.FoundationLoadBalancerUpdateSpec`` is a conditional
                configuration made available upon selecting the Foundation Load
                Balancer provider. It is used to configure the load balancer at run
                time.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.VSPHERE_FOUNDATION`.
            :type  nsx: :class:`Edges.NSXLoadBalancerUpdateSpec`
            :param nsx: The ``Edges.NSXLoadBalancerUpdateSpec`` is a conditional
                configuration made available upon selecting the NSX Load Balancer.
                It is used to configure properties of the load balancer at run
                time.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``provider`` is
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider.NSX_LB`.
            """
            self.provider = provider
            self.avi = avi
            self.haproxy = haproxy
            self.foundation = foundation
            self.nsx = nsx
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.update_spec', {
            'provider': type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors.networks.edges_client', 'EdgeProvider'),
            'avi': type.OptionalType(type.ReferenceType(__name__, 'Edges.AviUpdateSpec')),
            'haproxy': type.OptionalType(type.ReferenceType(__name__, 'Edges.HAProxyUpdateSpec')),
            'foundation': type.OptionalType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerUpdateSpec')),
            'nsx': type.OptionalType(type.ReferenceType(__name__, 'Edges.NSXLoadBalancerUpdateSpec')),
        },
        UpdateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        ``Edges.FilterSpec`` defines parameters to constrain a results set.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     providers=None,
                     edges=None,
                     names=None,
                    ):
            """
            :type  providers: :class:`list` of :class:`com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.EdgeProvider` or ``None``
            :param providers: Filter by one or more edge providers.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None this filter is not applied.
            :type  edges: :class:`list` of :class:`str` or ``None``
            :param edges: Filter by one or more unique edge identifiers.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.namespace_management.network.edge.Edge``. When
                methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.vcenter.namespace_management.network.edge.Edge``.
                if None this filter is not applied.
            :type  names: :class:`list` of :class:`str` or ``None``
            :param names: Filter by one or more unique edge names.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None this filter is not applied.
            """
            self.providers = providers
            self.edges = edges
            self.names = names
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.filter_spec', {
            'providers': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors.networks.edges_client', 'EdgeProvider'))),
            'edges': type.OptionalType(type.ListType(type.IdType())),
            'names': type.OptionalType(type.ListType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Edges.ListResult`` contains a set of results constrained by filtered
        parameters.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     edges=None,
                    ):
            """
            :type  edges: :class:`list` of :class:`Edges.Info`
            :param edges: All edges matching the provided filters or all edges in the system
                if no filters were set.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.edges = edges
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.list_result', {
            'edges': type.ListType(type.ReferenceType(__name__, 'Edges.Info')),
        },
        ListResult,
        False,
        None))


    class Condition(VapiStruct):
        """
        The ``Edges.Condition`` class defines an observation of the configuration
        state of a Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     status=None,
                     last_transition_time=None,
                     reason=None,
                     message=None,
                    ):
            """
            :type  type: :class:`Edges.Condition.Type`
            :param type: The type of an Edge's runtime state.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Edges.Condition.Status`
            :param status: The status of the condition.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_transition_time: :class:`datetime.datetime` or ``None``
            :param last_transition_time: Last time the condition transitioned from one state to another. A
                transition happens when the value of status field changes.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, there are no ongoing operations related to bringing the
                condition to the desired state.
            :type  reason: :class:`str`
            :param reason: A brief CamelCase message indicating details about the reason for
                the last transition.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param message: A human-readable message that provides additional details about the
                last transition.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None no additional information is available.
            """
            self.type = type
            self.status = status
            self.last_transition_time = last_transition_time
            self.reason = reason
            self.message = message
            VapiStruct.__init__(self)


        class Status(Enum):
            """
            Status of the condition, which can be one of TRUE, FALSE or UNKNOWN.
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
            TRUE = None
            """
            Indicates that the condition has reached the desired state.

            """
            FALSE = None
            """
            Indicates that the condition has not reached the desired state.

            """
            UNKNOWN = None
            """
            Indicates that the status of the condition can not be determined.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Status` instance.
                """
                Enum.__init__(string)

        Status._set_values({
            'TRUE': Status('TRUE'),
            'FALSE': Status('FALSE'),
            'UNKNOWN': Status('UNKNOWN'),
        })
        Status._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.supervisors.networks.edges.condition.status',
            Status))

        class Type(Enum):
            """
            Type of the condition.
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
            HEALTHY = None
            """
            Condition type that represents the consolidated health status of load
            balancer workload(s). HEALTHY condition type with status TRUE implies that
            the load balancer is up and can serve requests as expected. HEALTHY
            condition type with status FALSE implies either the load balancer has
            degraded functionality or it is unavailable to serve requests.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'HEALTHY': Type('HEALTHY'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.supervisors.networks.edges.condition.type',
            Type))

    Condition._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.condition', {
            'type': type.ReferenceType(__name__, 'Edges.Condition.Type'),
            'status': type.ReferenceType(__name__, 'Edges.Condition.Status'),
            'last_transition_time': type.OptionalType(type.DateTimeType()),
            'reason': type.StringType(),
            'message': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Condition,
        False,
        None))


    class IPRange(VapiStruct):
        """
        ``Edges.IPRange`` is an IP range that can be used for node or Virtual
        Server IP addresses depending on the context.
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
            :param address: The starting address of the range.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  count: :class:`long`
            :param count: The number of IP addresses in the range.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.address = address
            self.count = count
            VapiStruct.__init__(self)


    IPRange._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.IP_range', {
            'address': type.StringType(),
            'count': type.IntegerType(),
        },
        IPRange,
        False,
        None))


    class Server(VapiStruct):
        """
        A ``Edges.Server`` represents an endpoint used to configure load balancers.
        This class was added in **vSphere API 9.0.0.0**.

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
            :param host: Load balancer hostname or IPv4 address.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  port: :class:`long`
            :param port: Load balancer port.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.host = host
            self.port = port
            VapiStruct.__init__(self)


    Server._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.server', {
            'host': type.StringType(),
            'port': type.IntegerType(),
        },
        Server,
        False,
        None))


    class NSXLoadBalancerInfo(VapiStruct):
        """
        ``Edges.NSXLoadBalancerInfo`` contains detailed information about an NSX
        Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     default_ingress_tls_certificate=None,
                    ):
            """
            :type  default_ingress_tls_certificate: :class:`str`
            :param default_ingress_tls_certificate: :attr:`Edges.NSXLoadBalancerInfo.default_ingress_tls_certificate`
                defines a default certificate that is served on Ingress services
                when another certificate is not configured.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.default_ingress_tls_certificate = default_ingress_tls_certificate
            VapiStruct.__init__(self)


    NSXLoadBalancerInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.NSX_load_balancer_info', {
            'default_ingress_tls_certificate': type.StringType(),
        },
        NSXLoadBalancerInfo,
        False,
        None))


    class AviInfo(VapiStruct):
        """
        ``Edges.AviInfo`` contains detailed information about an Avi Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     server=None,
                     username=None,
                     certificate_authority_chain=None,
                     cloud_name=None,
                    ):
            """
            :type  server: :class:`Edges.Server`
            :param server: Server is the address for the Avi Controller used to configure
                Virtual Servers.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  username: :class:`str`
            :param username: An administrator user name for accessing the Avi Controller.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  certificate_authority_chain: :class:`str`
            :param certificate_authority_chain: PEM-encoded CA certificate chain which is used to verify x509
                certificates received from the server.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cloud_name: :class:`str` or ``None``
            :param cloud_name: The cloud name for the Avi Controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set` if custom cloud name is configured for this Avi
                Controller. If None, it defaults to "Default-Cloud".
            """
            self.server = server
            self.username = username
            self.certificate_authority_chain = certificate_authority_chain
            self.cloud_name = cloud_name
            VapiStruct.__init__(self)


    AviInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.avi_info', {
            'server': type.ReferenceType(__name__, 'Edges.Server'),
            'username': type.StringType(),
            'certificate_authority_chain': type.StringType(),
            'cloud_name': type.OptionalType(type.StringType()),
        },
        AviInfo,
        False,
        None))


    class AviCreateSpec(VapiStruct):
        """
        The ``Edges.AviCreateSpec`` defines parameters for creating an Avi Load
        Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     username=None,
                     password=None,
                     certificate_authority_chain=None,
                     server=None,
                     cloud_name=None,
                    ):
            """
            :type  username: :class:`str`
            :param username: :attr:`Edges.AviCreateSpec.username` is used for accessing the Avi
                Controller.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  password: :class:`str`
            :param password: :attr:`Edges.AviCreateSpec.password` secures the
                :attr:`Edges.AviCreateSpec.username`.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  certificate_authority_chain: :class:`str`
            :param certificate_authority_chain: :attr:`Edges.AviCreateSpec.certificate_authority_chain` contains
                PEM-encoded CA chain which is used to verify x509 certificates
                received from the server.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  server: :class:`Edges.Server`
            :param server: Server is the address for the Avi Controller, used to configure
                Virtual Servers.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cloud_name: :class:`str` or ``None``
            :param cloud_name: The cloud name for the Avi Controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set` if custom cloud name is configured for this Avi
                Controller. If None, it defaults to "Default-Cloud".
            """
            self.username = username
            self.password = password
            self.certificate_authority_chain = certificate_authority_chain
            self.server = server
            self.cloud_name = cloud_name
            VapiStruct.__init__(self)


    AviCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.avi_create_spec', {
            'username': type.StringType(),
            'password': type.SecretType(),
            'certificate_authority_chain': type.StringType(),
            'server': type.ReferenceType(__name__, 'Edges.Server'),
            'cloud_name': type.OptionalType(type.StringType()),
        },
        AviCreateSpec,
        False,
        None))


    class AviUpdateSpec(VapiStruct):
        """
        The ``Edges.AviUpdateSpec`` defines parameters for updating an Avi Load
        Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     username=None,
                     password=None,
                     certificate_authority_chain=None,
                    ):
            """
            :type  username: :class:`str` or ``None``
            :param username: An administrator user name for accessing the Avi Controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing username will not be modified.
            :type  password: :class:`str` or ``None``
            :param password: The password for the administrator user.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing password will not be modified.
            :type  certificate_authority_chain: :class:`str` or ``None``
            :param certificate_authority_chain: CertificateAuthorityChain contains PEM-encoded CA chain which is
                used to verify x509 certificates received from the server.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing PEM-encoded CA chain will not be modified.
            """
            self.username = username
            self.password = password
            self.certificate_authority_chain = certificate_authority_chain
            VapiStruct.__init__(self)


    AviUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.avi_update_spec', {
            'username': type.OptionalType(type.StringType()),
            'password': type.OptionalType(type.SecretType()),
            'certificate_authority_chain': type.OptionalType(type.StringType()),
        },
        AviUpdateSpec,
        False,
        None))


    class NSXLoadBalancerUpdateSpec(VapiStruct):
        """
        The ``Edges.NSXLoadBalancerUpdateSpec`` defines parameters for updating an
        NSX Load Balancer configuration.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     default_ingress_tls_certificate=None,
                     default_ingress_tls_private_key=None,
                    ):
            """
            :type  default_ingress_tls_certificate: :class:`str` or ``None``
            :param default_ingress_tls_certificate: PEM-encoded x509 certificate used by NSX as a default fallback
                certificate for Kubernetes Ingress services.   Certificate(s) used
                can be created by one of the two supported methods: 
                
                #. 1. By signing the Certificate Signing Request obtained from the
                   Namespace Certificate Management API. OR
                #. 2. By creating a certificate using public key cryptography. In
                   such case the certificate
                   :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_certificate`
                   should be specified along with the private key
                   :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_private_key`
                   used to generate the certificate.
                
                
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the Kubernetes Ingress services certificate will not be
                modified.
            :type  default_ingress_tls_private_key: :class:`str` or ``None``
            :param default_ingress_tls_private_key: Private Key matching
                :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_certificate`
                
                When using certificates generated externally by the user and not
                using Certificate Signing Request obtained from Namespace
                Certificate Management API, users should be able to specify the
                private key which was used to generate the certificate
                :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_certificate`.
                
                Users with externally generated key pairs can import their own
                public key certificates and key pairs.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None and
                :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_certificate`
                is specified then the Supervisor will attempt to find a matching
                key that was generated with Certificate Signing Request. Otherwise,
                :attr:`Edges.NSXLoadBalancerUpdateSpec.default_ingress_tls_private_key`
                will not be modified.
            """
            self.default_ingress_tls_certificate = default_ingress_tls_certificate
            self.default_ingress_tls_private_key = default_ingress_tls_private_key
            VapiStruct.__init__(self)


    NSXLoadBalancerUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.NSX_load_balancer_update_spec', {
            'default_ingress_tls_certificate': type.OptionalType(type.StringType()),
            'default_ingress_tls_private_key': type.OptionalType(type.SecretType()),
        },
        NSXLoadBalancerUpdateSpec,
        False,
        None))


    class HAProxyInfo(VapiStruct):
        """
        ``Edges.Info`` contains detailed information about an HAProxy Load
        Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. deprecated:: vSphere API 9.0.0.0
            This class is deprecated as of **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     address_ranges=None,
                     servers=None,
                     username=None,
                     certificate_authority_chain=None,
                    ):
            """
            :type  address_ranges: :class:`list` of :class:`Edges.IPRange`
            :param address_ranges: IP address range from which virtual servers are assigned their IPs.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  servers: :class:`list` of :class:`Edges.Server`
            :param servers: A list of the addresses for the DataPlane API servers used to
                configure HAProxy.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  username: :class:`str`
            :param username: An administrator user name for accessing the HAProxy Data Plane API
                server.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  certificate_authority_chain: :class:`str`
            :param certificate_authority_chain: PEM-encoded CA certificate chain which is used to verify x509
                certificates received from the server.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            warn('com.vmware.vcenter.namespace_management.supervisors.networks.Edges.HAProxyInfo is deprecated as of release vSphere API 9.0.0.0.', DeprecationWarning)
            self.address_ranges = address_ranges
            self.servers = servers
            self.username = username
            self.certificate_authority_chain = certificate_authority_chain
            VapiStruct.__init__(self)


    HAProxyInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.HA_proxy_info', {
            'address_ranges': type.ListType(type.ReferenceType(__name__, 'Edges.IPRange')),
            'servers': type.ListType(type.ReferenceType(__name__, 'Edges.Server')),
            'username': type.StringType(),
            'certificate_authority_chain': type.StringType(),
        },
        HAProxyInfo,
        False,
        None))


    class HAProxyUpdateSpec(VapiStruct):
        """
        The ``Edges.HAProxyUpdateSpec`` defines parameters for updating an HAProxy
        Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. deprecated:: vSphere API 9.0.0.0
            This class is deprecated as of **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     address_ranges=None,
                     username=None,
                     password=None,
                     certificate_authority_chain=None,
                    ):
            """
            :type  address_ranges: :class:`list` of :class:`Edges.IPRange` or ``None``
            :param address_ranges: List of address ranges that will be used to derive frontend IP
                addresses for L4 virtual servers. At least one range must be
                provided. An update operation only allows for addition of new IP
                ranges to the existing list of IP ranges.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing list of address ranges will not be modified.
            :type  username: :class:`str` or ``None``
            :param username: An administrator user name for accessing the HAProxy Data Plane API
                server.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing username will not be modified.
            :type  password: :class:`str` or ``None``
            :param password: The password for the administrator user.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing password will not be modified.
            :type  certificate_authority_chain: :class:`str` or ``None``
            :param certificate_authority_chain: CertificateAuthorityChain contains PEM-encoded CA chain which is
                used to verify x509 certificates received from the server.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the existing PEM-encoded CA chain will not be modified.
            """
            warn('com.vmware.vcenter.namespace_management.supervisors.networks.Edges.HAProxyUpdateSpec is deprecated as of release vSphere API 9.0.0.0.', DeprecationWarning)
            self.address_ranges = address_ranges
            self.username = username
            self.password = password
            self.certificate_authority_chain = certificate_authority_chain
            VapiStruct.__init__(self)


    HAProxyUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.HA_proxy_update_spec', {
            'address_ranges': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Edges.IPRange'))),
            'username': type.OptionalType(type.StringType()),
            'password': type.OptionalType(type.SecretType()),
            'certificate_authority_chain': type.OptionalType(type.StringType()),
        },
        HAProxyUpdateSpec,
        False,
        None))


    class FoundationLoadBalancerNetworkInterface(VapiStruct):
        """
        A ``Edges.FoundationLoadBalancerNetworkInterface`` defines how a Foundation
        Load Balancer will be connected to a Supervisor workload network.
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
            :type  personas: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.Persona`
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
            :type  network: :class:`str`
            :param network: Identifier of a Supervisor workload network. This network cannot be
                a DHCP network when
                :attr:`Edges.FoundationLoadBalancerNetworkInterface.personas`
                contains a Workload Persona or Frontend Persona.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.Network``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.Network``.
            """
            self.personas = personas
            self.network = network
            VapiStruct.__init__(self)


    FoundationLoadBalancerNetworkInterface._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_network_interface', {
            'personas': type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'Persona')),
            'network': type.IdType(resource_types='com.vmware.vcenter.namespace_management.Network'),
        },
        FoundationLoadBalancerNetworkInterface,
        False,
        None))


    class FoundationLoadBalancerRuntime(VapiStruct):
        """
        ``Edges.FoundationLoadBalancerRuntime`` contains the runtime state of the
        Foundation Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     conditions=None,
                     version=None,
                     vips_allocated=None,
                     vips_available=None,
                    ):
            """
            :type  conditions: :class:`list` of :class:`Edges.Condition`
            :param conditions: Contains a record of recent state transitions. 
                
                If the condition with the HEALTHY type has a status set to TRUE,
                then the system is operating normally. If the condition with the
                HEALTHY type has a status set to FALSE, then remediation may be
                required. If the condition with the HEALTHY type has a status set
                to UNKNOWN, then the system health could not be determined and
                remediation may be required.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  version: :class:`str`
            :param version: The current version of the load balancer. 
                
                The version selected is determined by your vCenter version and
                Supervisor version. 
                
                **The load balancer is upgraded when your Supervisor is updated.
                Upgrades will cause your workloads to incur downtime. Thus, you
                should plan for workload downtime when upgrading your Supervisor.**
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vips_allocated: :class:`long`
            :param vips_allocated: Total number of Virtual IP addresses currently allocated to
                services.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vips_available: :class:`long`
            :param vips_available: Total number of available Virtual IP addresses eligible to be used
                for load balancer services.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.conditions = conditions
            self.version = version
            self.vips_allocated = vips_allocated
            self.vips_available = vips_available
            VapiStruct.__init__(self)


    FoundationLoadBalancerRuntime._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_runtime', {
            'conditions': type.ListType(type.ReferenceType(__name__, 'Edges.Condition')),
            'version': type.StringType(),
            'vips_allocated': type.IntegerType(),
            'vips_available': type.IntegerType(),
        },
        FoundationLoadBalancerRuntime,
        False,
        None))


    class FoundationLoadBalancerInfo(VapiStruct):
        """
        ``Edges.FoundationLoadBalancerInfo`` describes the current desired state
        configured along with the runtime state reflected from the Supervisor's
        Kubernetes API server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     runtime=None,
                     interfaces=None,
                     vip_ranges=None,
                     vip_subnets=None,
                     size=None,
                     availability=None,
                     zones=None,
                     storage_policy=None,
                     dns_servers=None,
                     dns_search_domains=None,
                     ntp_servers=None,
                     syslog_endpoint=None,
                     syslog_certificate_authority_pem=None,
                    ):
            """
            :type  runtime: :class:`Edges.FoundationLoadBalancerRuntime`
            :param runtime: The ``Edges.FoundationLoadBalancerRuntime`` class contains the
                observed state of the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  interfaces: :class:`list` of :class:`Edges.FoundationLoadBalancerNetworkInterface`
            :param interfaces: Defines the current networks this load balancer is attached to.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vip_ranges: :class:`list` of :class:`Edges.IPRange`
            :param vip_ranges: Virtual IP addresses assigned to Kubernetes load balancer services,
                which allow ingress into the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vip_subnets: :class:`list` of :class:`str`
            :param vip_subnets: Subnets to service Virtual IP addresses. These subnets in addition
                to the subnet of the network attached to the interface with the
                Frontend Persona, allow traffic from
                :attr:`Edges.FoundationLoadBalancerInfo.vip_ranges` to route back
                to their destination.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  size: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.SizeHint`
            :param size: The current resource size of the load balancer deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  availability: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.AvailabilityMode`
            :param availability: The current availability mode configured for the Foundation Load
                Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  zones: :class:`list` of :class:`str`
            :param zones: The zones this Foundation Load Balancer is deployed onto.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``.
            :type  storage_policy: :class:`str`
            :param storage_policy: Storage Policy containing datastores hosting the Foundation Load
                Balancer nodes.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SpsStorageProfile``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SpsStorageProfile``.
            :type  dns_servers: :class:`list` of :class:`str`
            :param dns_servers: The current DNS servers configured for the Foundation Load Balancer
                control plane.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  dns_search_domains: :class:`list` of :class:`str`
            :param dns_search_domains: The current DNS search domains configured for the Foundation Load
                Balancer control plane.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  ntp_servers: :class:`list` of :class:`str`
            :param ntp_servers: The current NTP servers configured for the Foundation Load Balancer
                control plane.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  syslog_endpoint: :class:`str` or ``None``
            :param syslog_endpoint: The remote endpoint configured to receive logs from the Foundation
                Load Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None and the Management Persona interface is connected to the
                Supervisor's management network, then the syslog setting is
                inherited from vCenter Server. Otherwise, no syslog endpoint is
                configured.
            :type  syslog_certificate_authority_pem: :class:`str` or ``None``
            :param syslog_certificate_authority_pem: The trust bundle in PEM format verifying syslog TLS endpoints.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None and the Management Persona interface is connected to the
                Supervisor's management network, then the trust bundle is inherited
                from vCenter Server. Otherwise, no syslog certificate authority
                bundle is configured.
            """
            self.runtime = runtime
            self.interfaces = interfaces
            self.vip_ranges = vip_ranges
            self.vip_subnets = vip_subnets
            self.size = size
            self.availability = availability
            self.zones = zones
            self.storage_policy = storage_policy
            self.dns_servers = dns_servers
            self.dns_search_domains = dns_search_domains
            self.ntp_servers = ntp_servers
            self.syslog_endpoint = syslog_endpoint
            self.syslog_certificate_authority_pem = syslog_certificate_authority_pem
            VapiStruct.__init__(self)


    FoundationLoadBalancerInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_info', {
            'runtime': type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerRuntime'),
            'interfaces': type.ListType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerNetworkInterface')),
            'vip_ranges': type.ListType(type.ReferenceType(__name__, 'Edges.IPRange')),
            'vip_subnets': type.ListType(type.StringType()),
            'size': type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'SizeHint'),
            'availability': type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'AvailabilityMode'),
            'zones': type.ListType(type.IdType()),
            'storage_policy': type.IdType(resource_types='SpsStorageProfile'),
            'dns_servers': type.ListType(type.StringType()),
            'dns_search_domains': type.ListType(type.StringType()),
            'ntp_servers': type.ListType(type.StringType()),
            'syslog_endpoint': type.OptionalType(type.StringType()),
            'syslog_certificate_authority_pem': type.OptionalType(type.StringType()),
        },
        FoundationLoadBalancerInfo,
        False,
        None))


    class FoundationLoadBalancerCreateSpec(VapiStruct):
        """
        ``Edges.FoundationLoadBalancerCreateSpec`` defines parameters for creating
        a Foundation Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vip_ranges=None,
                     vip_subnets=None,
                     interfaces=None,
                     deployment_target=None,
                     network_services=None,
                    ):
            """
            :type  vip_ranges: :class:`list` of :class:`Edges.IPRange`
            :param vip_ranges: Virtual IP addresses assigned to Kubernetes load balancer services,
                which allow ingress into the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vip_subnets: :class:`list` of :class:`str` or ``None``
            :param vip_subnets: Subnets to service Virtual IP addresses. 
                
                If any of the IP Addresses provided as part of
                :attr:`Edges.FoundationLoadBalancerCreateSpec.vip_ranges` falls
                outside the frontend network subnet, then you must supply
                corresponding subnet(s) for those IP addresses. 
                
                The load balancer nodes are configured with additional routing
                rules for the provided
                :attr:`Edges.FoundationLoadBalancerCreateSpec.vip_subnets` that
                ensure return traffic for client requests coming from a source IP
                addresses that fall under
                :attr:`Edges.FoundationLoadBalancerCreateSpec.vip_subnets` ranges
                get forwarded to frontend network gateway via frontend network
                interface instead of the workload network gateway. 
                
                Subnet values should be in their canonical subnet CIDR form (e.g.
                192.168.0.0/24).
                This attribute was added in **vSphere API 9.0.0.0**.
                if unset no additional routing rules are setup on load balancer
                nodes.
            :type  interfaces: :class:`list` of :class:`Edges.FoundationLoadBalancerNetworkInterface` or ``None``
            :param interfaces: Customize the network interfaces of the load balancer granting them
                roles based on your network topology requirements. 
                
                All three personas must be used. Up to three network interfaces may
                be configured. 
                
                For Persona properties see
                :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.Persona`
                This attribute was added in **vSphere API 9.0.0.0**.
                If no interfaces are configured, then the load balancer will be
                attached to the Supervisor's management and workload networks when
                applicable. 
                
                If a Supervisor is provisioned with two networks, the following
                interface profile is created: 
                
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
                interface profile is created. 
                
                +-----------------+--------------------------------------------------------+-----------------------------+
                | Interface Index | Persona(s)                                     
                | Network                     |
                +-----------------+--------------------------------------------------------+-----------------------------+
                | 1               | Management Persona, Workload Persona, Frontend
                Persona | Supervisor Workload Network |
                +-----------------+--------------------------------------------------------+-----------------------------+
                In this context a single network interface is used for management,
                workload, and load balancer traffic.
            :type  deployment_target: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.DeploymentTarget` or ``None``
            :param deployment_target: Customize the placement of the Load Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the load balancer will be placed using its default
                configuration. See fields in
                :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.DeploymentTarget`
                for a description of each default configuration.
            :type  network_services: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.NetworkServices` or ``None``
            :param network_services: Configure network services for this load balancer. Network services
                increase the reliability of your load balancer. 
                
                Network services must be accessible from a network interface with a
                Management Persona assigned.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, and the interface configured with a Management Persona is
                connected to a DHCP network, it will attempt to obtain its settings
                from a DHCP server. If the interface configured with a Management
                Persona is connected to a static IP network, the values will be
                synced with the Supervisor's management services
                :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.Network.services`.
                
                **Availability of your load balancer may be reduced if network
                services are not configured. Therefore, it is highly recommended
                you ensure that network services are configured for your load
                balancer.**
            """
            self.vip_ranges = vip_ranges
            self.vip_subnets = vip_subnets
            self.interfaces = interfaces
            self.deployment_target = deployment_target
            self.network_services = network_services
            VapiStruct.__init__(self)


    FoundationLoadBalancerCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_create_spec', {
            'vip_ranges': type.ListType(type.ReferenceType(__name__, 'Edges.IPRange')),
            'vip_subnets': type.OptionalType(type.ListType(type.StringType())),
            'interfaces': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerNetworkInterface'))),
            'deployment_target': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'DeploymentTarget')),
            'network_services': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'NetworkServices')),
        },
        FoundationLoadBalancerCreateSpec,
        False,
        None))


    class FoundationDeploymentTargetUpdateSpec(VapiStruct):
        """
        The ``Edges.FoundationDeploymentTargetUpdateSpec`` specifies parameters for
        updating the placement of a deployed Foundation Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     size=None,
                     availability=None,
                     storage_policy=None,
                    ):
            """
            :type  size: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.SizeHint` or ``None``
            :param size: Scale up the size of the load balancer nodes. The size specified
                must be larger than the current size.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  availability: :class:`Edges.FoundationLoadBalancerUpdateAvailabilityMode` or ``None``
            :param availability: The availability controls the number of load balancer replicas. 
                
                You may only increase the availability of a deployed Foundation
                Load Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  storage_policy: :class:`str` or ``None``
            :param storage_policy: Update the Storage Policy hosting the load balancer nodes. 
                
                Updates to storage policy are not applied to running nodes. Nodes
                will consume the new storage policy when they are redeployed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SpsStorageProfile``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SpsStorageProfile``.
                If None current settings are unchanged.
            """
            self.size = size
            self.availability = availability
            self.storage_policy = storage_policy
            VapiStruct.__init__(self)


    FoundationDeploymentTargetUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_deployment_target_update_spec', {
            'size': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'SizeHint')),
            'availability': type.OptionalType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerUpdateAvailabilityMode')),
            'storage_policy': type.OptionalType(type.IdType()),
        },
        FoundationDeploymentTargetUpdateSpec,
        False,
        None))


    class FoundationLoadBalancerUpdateSpec(VapiStruct):
        """
        ``Edges.FoundationLoadBalancerUpdateSpec`` defines parameters for updating
        a Foundation Load Balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vip_ranges=None,
                     vip_subnets=None,
                     interfaces=None,
                     network_services=None,
                     deployment_target=None,
                    ):
            """
            :type  vip_ranges: :class:`list` of :class:`Edges.IPRange` or ``None``
            :param vip_ranges: Add Virtual IP addresses assigned to Kubernetes load balancer
                services, which allow ingress into the Supervisor. 
                
                The provided ranges are appended to existing ranges and thus may
                not overlap with existing ranges. 
                
                Existing Virtual IP addresses cannot be changed, and thus should
                not be specified.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  vip_subnets: :class:`list` of :class:`str` or ``None``
            :param vip_subnets: Add subnets to service Virtual IP addresses. 
                
                If any of the IP Addresses provided as part of
                :attr:`Edges.FoundationLoadBalancerUpdateSpec.vip_ranges` falls
                outside the frontend network subnet, then you must supply
                corresponding subnet(s) for those IP addresses. 
                
                The load balancer nodes are configured with additional routing
                rules for the provided
                :attr:`Edges.FoundationLoadBalancerUpdateSpec.vip_subnets` that
                ensure return traffic for client requests coming from a source IP
                addresses that fall under
                :attr:`Edges.FoundationLoadBalancerUpdateSpec.vip_subnets` ranges
                get forwarded to frontend network gateway via frontend network
                interface instead of the workload network gateway. 
                
                The supplied list of subnets will replace existing subnets. 
                
                Subnet values should be in their canonical subnet CIDR form (e.g.
                192.168.0.0/24).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  interfaces: :class:`list` of :class:`Edges.FoundationLoadBalancerNetworkInterface` or ``None``
            :param interfaces: Interfaces to be updated. 
                
                The following restrictions apply in addition to those specified as
                part of {link #create}. 
                
                * Interfaces can only be added and not removed.
                * The interface hosting the Frontend Persona cannot be changed.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  network_services: :class:`com.vmware.vcenter.namespace_management.networks.edges.foundation_client.NetworkServices` or ``None``
            :param network_services: ``com.vmware.vcenter.namespace_management.networks.edges.foundation_client.NetworkServices``
                contains external services on a network that the load balancer is
                eligible to interact with.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            :type  deployment_target: :class:`Edges.FoundationDeploymentTargetUpdateSpec` or ``None``
            :param deployment_target: ``Edges.FoundationDeploymentTargetUpdateSpec`` contains structures
                to update the placement of a Foundation Load Balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None current settings are unchanged.
            """
            self.vip_ranges = vip_ranges
            self.vip_subnets = vip_subnets
            self.interfaces = interfaces
            self.network_services = network_services
            self.deployment_target = deployment_target
            VapiStruct.__init__(self)


    FoundationLoadBalancerUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.networks.edges.foundation_load_balancer_update_spec', {
            'vip_ranges': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Edges.IPRange'))),
            'vip_subnets': type.OptionalType(type.ListType(type.StringType())),
            'interfaces': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Edges.FoundationLoadBalancerNetworkInterface'))),
            'network_services': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.edges.foundation_client', 'NetworkServices')),
            'deployment_target': type.OptionalType(type.ReferenceType(__name__, 'Edges.FoundationDeploymentTargetUpdateSpec')),
        },
        FoundationLoadBalancerUpdateSpec,
        False,
        None))



    def list(self,
             supervisor,
             filter=None,
             ):
        """
        List detailed configuration about all edges in the system, filtered
        upon request.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: The unique identifier for the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  filter: :class:`Edges.FilterSpec` or ``None``
        :param filter: parameters on which to filter response contents.
            If None, all known edges will be returned.
        :rtype: :class:`Edges.ListResult`
        :return: A list of detailed information about each requested edge.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the Supervisor ID cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege on the Supervisor
            for each edge.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider does not allow or implement deletion.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if one or more provided parameters do not match any edge providers,
            edges, or Supervisors in the system.
        """
        return self._invoke('list',
                            {
                            'supervisor': supervisor,
                            'filter': filter,
                            })

    def create(self,
               supervisor,
               spec,
               ):
        """
        Create an edge with the specified configuration.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: The unique identifier for the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  spec: :class:`Edges.CreateSpec`
        :param spec: Information about the edge to be created.
        :rtype: :class:`str`
        :return: the edge ID used for querying the status of the request.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.network.edge.Edge``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the associated Supervisor is being disabled or if the edge is
            already marked for delete.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the Supervisor ID cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``spec`` contains any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Manage privilege on the
            associated Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider does not allow or implement create.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if an edge with the same name already exists.
        """
        return self._invoke('create',
                            {
                            'supervisor': supervisor,
                            'spec': spec,
                            })

    def update(self,
               supervisor,
               edge,
               spec,
               ):
        """
        Update the edge configuration. Only the provided parameters will be
        updated. None parameters will remain in their current state.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: The unique identifier for the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  edge: :class:`str`
        :param edge: The unique identifier for the edge.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.network.edge.Edge``.
        :type  spec: :class:`Edges.UpdateSpec`
        :param spec: Information about the edge to be updated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Manage privilege on the
            associated Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the provider does not allow or implement update.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the associated Supervisor is being disabled or if the edge is
            already marked for delete.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the Supervisor or edge ID cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``spec`` contains any errors.
        """
        return self._invoke('update',
                            {
                            'supervisor': supervisor,
                            'edge': edge,
                            'spec': spec,
                            })
class _EdgesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Edges.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/networks/edges',
            path_variables={
                'supervisor': 'supervisor',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'spec': type.ReferenceType(__name__, 'Edges.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/networks/edges',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'edge': type.IdType(resource_types='com.vmware.vcenter.namespace_management.network.edge.Edge'),
            'spec': type.ReferenceType(__name__, 'Edges.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/networks/edges/{edge}',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
                'edge': 'edge',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Edges.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.namespace_management.network.edge.Edge'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.supervisors.networks.edges',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Edges': Edges,
        'edges': 'com.vmware.vcenter.namespace_management.supervisors.networks.edges_client.StubFactory',
        'management': 'com.vmware.vcenter.namespace_management.supervisors.networks.management_client.StubFactory',
        'workload': 'com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.StubFactory',
    }

