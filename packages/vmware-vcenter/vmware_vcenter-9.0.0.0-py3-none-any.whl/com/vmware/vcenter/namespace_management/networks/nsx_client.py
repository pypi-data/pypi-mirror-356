# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.nsx.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.networks.nsx_client`` module
provides classes and classes for managing NSX resources.

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


class IPBlockInfo(VapiStruct):
    """
    The ``IPBlockInfo`` class contains information about IP blocks.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'available_IP_ranges': 'available_ip_ranges',
                            'used_IP_count': 'used_ip_count',
                            'available_IP_count': 'available_ip_count',
                            }

    def __init__(self,
                 path=None,
                 name=None,
                 cidr=None,
                 available_ip_ranges=None,
                 used_ip_count=None,
                 available_ip_count=None,
                ):
        """
        :type  path: :class:`str`
        :param path: NSX policy path of the IP block.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  name: :class:`str`
        :param name: IP block name.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  cidr: :class:`com.vmware.vcenter.namespace_management.networks_client.Ipv4Cidr`
        :param cidr: IP block CIDR.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  available_ip_ranges: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks_client.IPRange`
        :param available_ip_ranges: Available IP Ranges of the IP block.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  used_ip_count: :class:`long`
        :param used_ip_count: The count of used IP addresses in the IPBlock.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  available_ip_count: :class:`long`
        :param available_ip_count: The count of available IP addresses in the IPBlock.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.path = path
        self.name = name
        self.cidr = cidr
        self.available_ip_ranges = available_ip_ranges
        self.used_ip_count = used_ip_count
        self.available_ip_count = available_ip_count
        VapiStruct.__init__(self)


IPBlockInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.networks.nsx.IP_block_info', {
        'path': type.StringType(),
        'name': type.StringType(),
        'cidr': type.ReferenceType('com.vmware.vcenter.namespace_management.networks_client', 'Ipv4Cidr'),
        'available_IP_ranges': type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks_client', 'IPRange')),
        'used_IP_count': type.IntegerType(),
        'available_IP_count': type.IntegerType(),
    },
    IPBlockInfo,
    False,
    None))



class DistributedSwitches(VapiInterface):
    """
    The ``DistributedSwitches`` class provides methods to get the basic
    information of Distributed Switches.
    This class was added in **vSphere API 8.0.0.1**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.distributed_switches'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DistributedSwitchesStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``DistributedSwitches.Summary`` class contains the basic information
        about a Distributed Switch.
        This class was added in **vSphere API 8.0.0.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     distributed_switch=None,
                     name=None,
                    ):
            """
            :type  distributed_switch: :class:`str`
            :param distributed_switch: Identifier of the switch. The value of this field refers to the
                UUID of a vim.DistributedVirtualSwitch.
                This attribute was added in **vSphere API 8.0.0.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``vSphereDistributedSwitch``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``vSphereDistributedSwitch``.
            :type  name: :class:`str`
            :param name: Human-readable identifier of the switch.
                This attribute was added in **vSphere API 8.0.0.1**.
            """
            self.distributed_switch = distributed_switch
            self.name = name
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.distributed_switches.summary', {
            'distributed_switch': type.IdType(resource_types='vSphereDistributedSwitch'),
            'name': type.StringType(),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``DistributedSwitches.FilterSpec`` class contains attributes used to
        filter the results when listing Distributed Switches (see
        :func:`DistributedSwitches.list`).
        This class was added in **vSphere API 8.0.0.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     compatible=None,
                     zones=None,
                    ):
            """
            :type  compatible: :class:`bool` or ``None``
            :param compatible: Compatibility criteria. If true, only Distributed Switches
                compatible with the vSphere Namespaces will be returned. If false,
                only Distributed Switches incompatible with the vSphere Namespaces
                will be returned.
                This attribute was added in **vSphere API 8.0.0.1**.
                If None, both compatible and incompatible Distributed Switches will
                be returned.
            :type  zones: :class:`list` of :class:`str`
            :param zones: Zone compatibility criteria. If zones are specified, the common
                distributed switches across the given zones will returned. A
                distributed switch is considered common if it is present in all of
                the vSphere clusters in a given zone.
                This attribute was added in **vSphere API 8.0.0.1**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``.
            """
            self.compatible = compatible
            self.zones = zones
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.distributed_switches.filter_spec', {
            'compatible': type.OptionalType(type.BooleanType()),
            'zones': type.ListType(type.IdType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns basic information of the Distributed Switches matching the
        :class:`DistributedSwitches.FilterSpec`.
        This method was added in **vSphere API 8.0.0.1**.

        :type  filter: :class:`DistributedSwitches.FilterSpec` or ``None``
        :param filter: Specification of matching Distributed Switches for which
            information should be returned.
            If None, the behavior is equivalent to a
            :class:`DistributedSwitches.FilterSpec` with all attributes None
            which means all Distributed Switches will be returned.
        :rtype: :class:`list` of :class:`DistributedSwitches.Summary`
        :return: List of Distributed Switches summaries matching the
            :class:`DistributedSwitches.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if one or more fields of the
            :class:`DistributedSwitches.FilterSpec` is incorrect.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })
class Edges(VapiInterface):
    """
    The ``Edges`` class provides methods to retrieve the basic information for
    NSX Edges.
    This class was added in **vSphere API 8.0.0.1**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.edges'
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

    class Summary(VapiStruct):
        """
        The ``Edges.Summary`` class contains the basic information about an Edge.
        This class was added in **vSphere API 8.0.0.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     edge_cluster=None,
                     name=None,
                     path=None,
                    ):
            """
            :type  edge_cluster: :class:`str`
            :param edge_cluster: Identifier of the Edge.
                This attribute was added in **vSphere API 8.0.0.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``NSXEdgeCluster``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``NSXEdgeCluster``.
            :type  name: :class:`str`
            :param name: Human-readable identifier of the Edge.
                This attribute was added in **vSphere API 8.0.0.1**.
            :type  path: :class:`str`
            :param path: NSX Policy path of the Edge.
                This attribute was added in **vSphere API 8.0.0.1**.
            """
            self.edge_cluster = edge_cluster
            self.name = name
            self.path = path
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.edges.summary', {
            'edge_cluster': type.IdType(resource_types='NSXEdgeCluster'),
            'name': type.StringType(),
            'path': type.StringType(),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Edges.FilterSpec`` class contains attributes used to filter the
        results when listing Edges (see :func:`Edges.list`).
        This class was added in **vSphere API 8.0.0.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     compatible=None,
                     distributed_switch=None,
                    ):
            """
            :type  compatible: :class:`bool` or ``None``
            :param compatible: Compatibility criteria. If true, only Edges which are compatible
                with vSphere Namespaces will be returned. If false, only Edges
                incompatible with vSphere Namespaces will be returned.
                This attribute was added in **vSphere API 8.0.0.1**.
                If None, both compatible and incompatible Edges will be returned.
            :type  distributed_switch: :class:`list` of :class:`str`
            :param distributed_switch: Distributed switch UUID criteria. If distributed switches
                identifiers are specified, they will be used to filter the Edges.
                To obtain the available distributed switch UUIDs, use:
                :func:`DistributedSwitches.list`.
                This attribute was added in **vSphere API 8.0.0.1**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``vSphereDistributedSwitch``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``vSphereDistributedSwitch``.
            """
            self.compatible = compatible
            self.distributed_switch = distributed_switch
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.edges.filter_spec', {
            'compatible': type.OptionalType(type.BooleanType()),
            'distributed_switch': type.ListType(type.IdType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns a list of Edges matching the given filter.
        This method was added in **vSphere API 8.0.0.1**.

        :type  filter: :class:`Edges.FilterSpec` or ``None``
        :param filter: Specification of matching Edges for which information should be
            returned.
            If None, the behavior is equivalent to a :class:`Edges.FilterSpec`
            with all attributes None which means all Edges will be returned.
        :rtype: :class:`list` of :class:`Edges.Summary`
        :return: List of Edge summaries matching the given filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if one or more fields of the :class:`Edges.FilterSpec` is
            incorrect.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })
class Projects(VapiInterface):
    """
    The ``Projects`` provides methods to get information of NSX Projects.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProjectsStub)
        self._VAPI_OPERATION_IDS = {}

    class VpcConnectivityProfileInfo(VapiStruct):
        """
        The ``Projects.VpcConnectivityProfileInfo`` class contains information
        about a VPC Connectivity Profile.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     profile=None,
                     name=None,
                     nsx_path=None,
                    ):
            """
            :type  profile: :class:`str`
            :param profile: Identifier of the profile.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VpcConnectivityProfile``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``VpcConnectivityProfile``.
            :type  name: :class:`str`
            :param name: Name used for this profile.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the profile.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.profile = profile
            self.name = name
            self.nsx_path = nsx_path
            VapiStruct.__init__(self)


    VpcConnectivityProfileInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profile_info', {
            'profile': type.IdType(resource_types='VpcConnectivityProfile'),
            'name': type.StringType(),
            'nsx_path': type.StringType(),
        },
        VpcConnectivityProfileInfo,
        False,
        None))


    class EdgeClusterInfo(VapiStruct):
        """
        The ``Projects.EdgeClusterInfo`` class contains info of NSX Edge cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     edge_cluster_path=None,
                     edge_cluster_name=None,
                    ):
            """
            :type  edge_cluster_path: :class:`str`
            :param edge_cluster_path: NSX Edge cluster path to be used for SNAT and other centralized
                services.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  edge_cluster_name: :class:`str`
            :param edge_cluster_name: NSX Edge cluster name used for this cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.edge_cluster_path = edge_cluster_path
            self.edge_cluster_name = edge_cluster_name
            VapiStruct.__init__(self)


    EdgeClusterInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.edge_cluster_info', {
            'edge_cluster_path': type.StringType(),
            'edge_cluster_name': type.StringType(),
        },
        EdgeClusterInfo,
        False,
        None))


    class NsxGatewayInfo(VapiStruct):
        """
        The ``Projects.NsxGatewayInfo`` class contains info of NSX Gateway.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     nsx_gateway_path=None,
                     nsx_gateway_name=None,
                    ):
            """
            :type  nsx_gateway_path: :class:`str`
            :param nsx_gateway_path: NSX Tier0 or VRF Gateway path used for this cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_gateway_name: :class:`str`
            :param nsx_gateway_name: NSX Tier0 or VRF Gateway name used for this cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.nsx_gateway_path = nsx_gateway_path
            self.nsx_gateway_name = nsx_gateway_name
            VapiStruct.__init__(self)


    NsxGatewayInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.nsx_gateway_info', {
            'nsx_gateway_path': type.StringType(),
            'nsx_gateway_name': type.StringType(),
        },
        NsxGatewayInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Projects.Info`` class contains information about an NSX Project.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'external_IPv4_blocks': 'external_ipv4_blocks',
                                }

        def __init__(self,
                     project=None,
                     name=None,
                     description=None,
                     nsx_path=None,
                     gateways=None,
                     edge_clusters=None,
                     external_ipv4_blocks=None,
                     default_project=None,
                     vpc_connectivity_profiles=None,
                    ):
            """
            :type  project: :class:`str`
            :param project: Identifier of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``NSXProject``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``NSXProject``.
            :type  name: :class:`str`
            :param name: Name of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: Description of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  gateways: :class:`list` of :class:`Projects.NsxGatewayInfo`
            :param gateways: List of NSX Tier0 or Tier0-VRF gateways currently configured with
                the project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  edge_clusters: :class:`list` of :class:`Projects.EdgeClusterInfo`
            :param edge_clusters: List of NSX Edge Clusters currently configured with the project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  external_ipv4_blocks: :class:`list` of :class:`IPBlockInfo`
            :param external_ipv4_blocks: List of NSX External IPv4 Blocks currently configured with the
                project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  default_project: :class:`bool`
            :param default_project: ``true`` if this Project is the default Project in NSX, ``false``
                otherwise.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vpc_connectivity_profiles: :class:`list` of :class:`Projects.VpcConnectivityProfileInfo`
            :param vpc_connectivity_profiles: VPC Connectivity Profile under this project.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.project = project
            self.name = name
            self.description = description
            self.nsx_path = nsx_path
            self.gateways = gateways
            self.edge_clusters = edge_clusters
            self.external_ipv4_blocks = external_ipv4_blocks
            self.default_project = default_project
            self.vpc_connectivity_profiles = vpc_connectivity_profiles
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.info', {
            'project': type.IdType(resource_types='NSXProject'),
            'name': type.StringType(),
            'description': type.StringType(),
            'nsx_path': type.StringType(),
            'gateways': type.ListType(type.ReferenceType(__name__, 'Projects.NsxGatewayInfo')),
            'edge_clusters': type.ListType(type.ReferenceType(__name__, 'Projects.EdgeClusterInfo')),
            'external_IPv4_blocks': type.ListType(type.ReferenceType(__name__, 'IPBlockInfo')),
            'default_project': type.BooleanType(),
            'vpc_connectivity_profiles': type.ListType(type.ReferenceType(__name__, 'Projects.VpcConnectivityProfileInfo')),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Projects.FilterSpec`` class contains attributes used to filter the
        results when listing Projects (see :func:`Projects.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     compatible=None,
                    ):
            """
            :type  compatible: :class:`bool` or ``None``
            :param compatible: Compatibility criteria. If true, only Projects which are compatible
                with Supervisor enablement will be returned. If false, only
                Projects incompatible with Supervisor enablement will be returned.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, both compatible and incompatible Projects will be
                returned.
            """
            self.compatible = compatible
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.filter_spec', {
            'compatible': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Projects.ListResult`` class represents the result of the
        :func:`Projects.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     projects=None,
                    ):
            """
            :type  projects: :class:`list` of :class:`Projects.Info`
            :param projects: List of all NSX projects.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.projects = projects
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.list_result', {
            'projects': type.ListType(type.ReferenceType(__name__, 'Projects.Info')),
        },
        ListResult,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information of NSX Projects.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Projects.FilterSpec` or ``None``
        :param filter: Specification of matching Projects for which information should be
            returned.
            If None, the behavior is equivalent to a
            :class:`Projects.FilterSpec` with all attributes None which means
            all Projects will be returned.
        :rtype: :class:`Projects.ListResult`
        :return: List of summaries of Projects matching the given filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            project,
            ):
        """
        Returns information of a NSX Project.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :rtype: :class:`Projects.Info`
        :return: Information about a Project.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'project': project,
                            })
class _DistributedSwitchesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'DistributedSwitches.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/networks/nsx/distributed-switches',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'DistributedSwitches.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.distributed_switches',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EdgesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Edges.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/networks/nsx/edges',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Edges.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.edges',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ProjectsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Projects.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/networks/nsx/projects',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}',
            path_variables={
                'project': 'project',
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
                'output_type': type.ReferenceType(__name__, 'Projects.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Projects.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'DistributedSwitches': DistributedSwitches,
        'Edges': Edges,
        'Projects': Projects,
        'distributed_switches': 'com.vmware.vcenter.namespace_management.networks.nsx.distributed_switches_client.StubFactory',
        'edges': 'com.vmware.vcenter.namespace_management.networks.nsx.edges_client.StubFactory',
        'projects': 'com.vmware.vcenter.namespace_management.networks.nsx.projects_client.StubFactory',
    }

