# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespaces.networks.nsx.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespaces.networks.nsx_client`` module provides
classes and classes for managing NSX resources.

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

class VpcSubnetAccessMode(Enum):
    """
    The ``VpcSubnetAccessMode`` enumerates the default access modes of NSX VPC
    subnets hosting resources created in namespaces.
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
    PUBLIC = None
    """
    :attr:`VpcSubnetAccessMode.PUBLIC` indicates new subnets are allocated from
    :attr:`VpcConnectivityProfileInfo.external_ip_blocks` and are routable from
    external networks.

    """
    PRIVATE_TGW = None
    """
    :attr:`VpcSubnetAccessMode.PRIVATE_TGW` indicates new subnets are allocated
    from :attr:`VpcConnectivityProfileInfo.privatetgw_ip_blocks` and are
    routable within other VPCs from the same project.

    """
    PRIVATE = None
    """
    :attr:`VpcSubnetAccessMode.PRIVATE` indicates new subnets are allocated
    from private CIDRs and are routable only within the same VPC.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`VpcSubnetAccessMode` instance.
        """
        Enum.__init__(string)

VpcSubnetAccessMode._set_values({
    'PUBLIC': VpcSubnetAccessMode('PUBLIC'),
    'PRIVATE_TGW': VpcSubnetAccessMode('PRIVATE_TGW'),
    'PRIVATE': VpcSubnetAccessMode('PRIVATE'),
})
VpcSubnetAccessMode._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespaces.networks.nsx.vpc_subnet_access_mode',
    VpcSubnetAccessMode))




class VpcConnectivityProfileInfo(VapiStruct):
    """
    The ``VpcConnectivityProfileInfo`` provides information of NSX VPC
    Connectivity Profile.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """



    _canonical_to_pep_names = {
                            'external_IP_blocks': 'external_ip_blocks',
                            'privateTGW_IP_blocks': 'privatetgw_ip_blocks',
                            }

    def __init__(self,
                 profile=None,
                 name=None,
                 nsx_path=None,
                 description=None,
                 default_profile=None,
                 external_ip_blocks=None,
                 privatetgw_ip_blocks=None,
                ):
        """
        :type  profile: :class:`str`
        :param profile: Identifier of the VPC Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.VpcConnectivityProfile``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.VpcConnectivityProfile``.
        :type  name: :class:`str`
        :param name: Name of the VPC Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  nsx_path: :class:`str`
        :param nsx_path: NSX path of the VPC Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  description: :class:`str` or ``None``
        :param description: Description of the VPC Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no description is added to the VPC Connectivity Profile.
        :type  default_profile: :class:`bool`
        :param default_profile: ``true`` if this profile is the default connectivity profile in NSX
            project, ``false`` otherwise.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  external_ip_blocks: :class:`list` of :class:`IPBlockInfo` or ``None``
        :param external_ip_blocks: List of NSX External IP Blocks currently configured with the VPC
            Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no external IP blocks are defined in the VPC Connectivity
            Profile.
        :type  privatetgw_ip_blocks: :class:`list` of :class:`IPBlockInfo` or ``None``
        :param privatetgw_ip_blocks: List of NSX Private TGW IP Blocks currently configured with the VPC
            Connectivity Profile.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no private TGW IP blocks are defined in the VPC
            Connectivity Profile.
        """
        self.profile = profile
        self.name = name
        self.nsx_path = nsx_path
        self.description = description
        self.default_profile = default_profile
        self.external_ip_blocks = external_ip_blocks
        self.privatetgw_ip_blocks = privatetgw_ip_blocks
        VapiStruct.__init__(self)


VpcConnectivityProfileInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespaces.networks.nsx.vpc_connectivity_profile_info', {
        'profile': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.VpcConnectivityProfile'),
        'name': type.StringType(),
        'nsx_path': type.StringType(),
        'description': type.OptionalType(type.StringType()),
        'default_profile': type.BooleanType(),
        'external_IP_blocks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'IPBlockInfo'))),
        'privateTGW_IP_blocks': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'IPBlockInfo'))),
    },
    VpcConnectivityProfileInfo,
    False,
    None))



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
        :type  cidr: :class:`Ipv4Cidr`
        :param cidr: IP block CIDR.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  available_ip_ranges: :class:`list` of :class:`IPRange`
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
    'com.vmware.vcenter.namespaces.networks.nsx.IP_block_info', {
        'path': type.StringType(),
        'name': type.StringType(),
        'cidr': type.ReferenceType(__name__, 'Ipv4Cidr'),
        'available_IP_ranges': type.ListType(type.ReferenceType(__name__, 'IPRange')),
        'used_IP_count': type.IntegerType(),
        'available_IP_count': type.IntegerType(),
    },
    IPBlockInfo,
    False,
    None))



class Ipv4Cidr(VapiStruct):
    """
    The specification for representing CIDR notation of IP range.
    This class was added in **vSphere API 7.0.2.00100**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 address=None,
                 prefix=None,
                ):
        """
        :type  address: :class:`str`
        :param address: The IPv4 address.
            This attribute was added in **vSphere API 7.0.2.00100**.
        :type  prefix: :class:`long`
        :param prefix: The CIDR prefix.
            This attribute was added in **vSphere API 7.0.2.00100**.
        """
        self.address = address
        self.prefix = prefix
        VapiStruct.__init__(self)


Ipv4Cidr._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespaces.networks.nsx.ipv4_cidr', {
        'address': type.StringType(),
        'prefix': type.IntegerType(),
    },
    Ipv4Cidr,
    False,
    None))



class IPRange(VapiStruct):
    """
    The ``IPRange`` class is used to express a range of IP addresses. The IP
    address supported by this structure will depend on the IP version that is
    being used by Supervisor. 
    
    Currently, the Supervisor only supports IPv4.

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
        :param address: :attr:`IPRange.address` is the starting IP address of the
            ``IPRange``.
        :type  count: :class:`long`
        :param count: 
            
            :attr:`IPRange.count` is number of IP addresses in the range. 
            
            For example: 
            
            A /24 subnet will have a count of 256. 
            
            A /24 subnet with a gateway address and a broadcast address will
            have a count of 254.
        """
        self.address = address
        self.count = count
        VapiStruct.__init__(self)


IPRange._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespaces.networks.nsx.IP_range', {
        'address': type.StringType(),
        'count': type.IntegerType(),
    },
    IPRange,
    False,
    None))



class ProjectInfo(VapiStruct):
    """
    The ``ProjectInfo`` class contains information about a NSX Project.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 project=None,
                 name=None,
                 nsx_path=None,
                ):
        """
        :type  project: :class:`str`
        :param project: Identifier of NSX Project.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``NSXProject``. When methods return a value of this class as a
            return value, the attribute will be an identifier for the resource
            type: ``NSXProject``.
        :type  name: :class:`str`
        :param name: NSX Project name.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  nsx_path: :class:`str`
        :param nsx_path: NSX path of the Project.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.project = project
        self.name = name
        self.nsx_path = nsx_path
        VapiStruct.__init__(self)


ProjectInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespaces.networks.nsx.project_info', {
        'project': type.IdType(resource_types='NSXProject'),
        'name': type.StringType(),
        'nsx_path': type.StringType(),
    },
    ProjectInfo,
    False,
    None))



class VpcInfo(VapiStruct):
    """
    The ``VpcInfo`` class contains information about a VPC.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vpc=None,
                 name=None,
                 nsx_path=None,
                 nsx_project_info=None,
                 vpc_connectivity_profile_info=None,
                 private_cidrs=None,
                ):
        """
        :type  vpc: :class:`str`
        :param vpc: Identifier of the VPC.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.Vpc``. When
            methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.Vpc``.
        :type  name: :class:`str`
        :param name: Name of the VPC.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  nsx_path: :class:`str`
        :param nsx_path: NSX path of the VPC.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  nsx_project_info: :class:`ProjectInfo`
        :param nsx_project_info: NSX Project used for this namespace.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  vpc_connectivity_profile_info: :class:`VpcConnectivityProfileInfo`
        :param vpc_connectivity_profile_info: VpcConnectivityProfile used for this namespace.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  private_cidrs: :class:`list` of :class:`Ipv4Cidr` or ``None``
        :param private_cidrs: CIDR blocks from which private subnets and private pod IPs are
            allocated.
            This attribute was added in **vSphere API 9.0.0.0**.
            None if no private CIDRs configured.
        """
        self.vpc = vpc
        self.name = name
        self.nsx_path = nsx_path
        self.nsx_project_info = nsx_project_info
        self.vpc_connectivity_profile_info = vpc_connectivity_profile_info
        self.private_cidrs = private_cidrs
        VapiStruct.__init__(self)


VpcInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespaces.networks.nsx.vpc_info', {
        'vpc': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.Vpc'),
        'name': type.StringType(),
        'nsx_path': type.StringType(),
        'nsx_project_info': type.ReferenceType(__name__, 'ProjectInfo'),
        'vpc_connectivity_profile_info': type.ReferenceType(__name__, 'VpcConnectivityProfileInfo'),
        'private_cidrs': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Ipv4Cidr'))),
    },
    VpcInfo,
    False,
    None))



class Subnets(VapiInterface):
    """
    The ``Subnets`` class provides methods to get NSX Subnets present in a
    particular namespace.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespaces.networks.nsx.subnets'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SubnetsStub)
        self._VAPI_OPERATION_IDS = {}

    class Entity(Enum):
        """
        The ``Subnets.Entity`` enumerates the type of the entity listed whether
        Subnet or SubnetSet.
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
        SUBNET = None
        """
        A :attr:`Subnets.Entity.SUBNET` in a VPC represents an independent layer 2
        broadcast domain with its associated CIDR and properties like Access mode
        (network advertisement), DHCP configuration etc.

        """
        SUBNETSET = None
        """
        A :attr:`Subnets.Entity.SUBNETSET` is a scalable grouping of VPC subnets
        sharing the same properties, which will allow auto-scale of networking
        availability to connect workloads.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Entity` instance.
            """
            Enum.__init__(string)

    Entity._set_values({
        'SUBNET': Entity('SUBNET'),
        'SUBNETSET': Entity('SUBNETSET'),
    })
    Entity._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespaces.networks.nsx.subnets.entity',
        Entity))


    class Info(VapiStruct):
        """
        The ``Subnets.Info`` contains selected fields from the corresponding NSX
        Subnet or SubnetSet entity.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     type=None,
                     api_version=None,
                     uid=None,
                     labels=None,
                     access_mode=None,
                     conditions=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the entity within the namespace.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  type: :class:`Subnets.Entity`
            :param type: The type of the entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  api_version: :class:`str`
            :param api_version: The NSX API version of the entity that was retrieved.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  uid: :class:`str`
            :param uid: The unique identifier of the entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  labels: :class:`dict` of :class:`str` and :class:`str`
            :param labels: The labels associated with this entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  access_mode: :class:`str`
            :param access_mode: Access mode of entity, accessible only from within VPC or from
                outside the VPC. Possible values can be: 
                
                * Private: Accessible only within the VPC
                * Public: Accessible outside the VPC
                * PrivateTGW: Accessible within a Project
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  conditions: :class:`list` of :class:`Subnets.Condition`
            :param conditions: A list of conditions indicating the condition of the Subnet or
                SubnetSet
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.type = type
            self.api_version = api_version
            self.uid = uid
            self.labels = labels
            self.access_mode = access_mode
            self.conditions = conditions
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.networks.nsx.subnets.info', {
            'name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Subnets.Entity'),
            'api_version': type.StringType(),
            'uid': type.StringType(),
            'labels': type.MapType(type.StringType(), type.StringType()),
            'access_mode': type.StringType(),
            'conditions': type.ListType(type.ReferenceType(__name__, 'Subnets.Condition')),
        },
        Info,
        False,
        None))


    class Condition(VapiStruct):
        """
        Condition defines condition of the :class:`Subnets.Entity`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     condition_status=None,
                     time_stamp=None,
                     reason=None,
                     message=None,
                    ):
            """
            :type  type: :class:`str`
            :param type: Type of the condition. Possible values can be: 
                
                * Ready
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  condition_status: :class:`str`
            :param condition_status: Status of the condition. Possible values are: 
                
                * True
                * False
                * Unknown
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  time_stamp: :class:`datetime.datetime` or ``None``
            :param time_stamp: Last time the condition transitioned from one status to another.
                This should be the time when the underlying condition changed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This field could be None when the time of change of the condition
                is not known.
            :type  reason: :class:`str`
            :param reason: This shows a brief reason of condition.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  message: :class:`str`
            :param message: This shows a human-readable message about condition.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.type = type
            self.condition_status = condition_status
            self.time_stamp = time_stamp
            self.reason = reason
            self.message = message
            VapiStruct.__init__(self)


    Condition._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.networks.nsx.subnets.condition', {
            'type': type.StringType(),
            'condition_status': type.StringType(),
            'time_stamp': type.OptionalType(type.DateTimeType()),
            'reason': type.StringType(),
            'message': type.StringType(),
        },
        Condition,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Subnets.ListResult`` class represents the result of the
        :func:`Subnets.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     subnets=None,
                    ):
            """
            :type  subnets: :class:`list` of :class:`Subnets.Info`
            :param subnets: List of all NSX Subnets and SubnetSets.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.subnets = subnets
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.networks.nsx.subnets.list_result', {
            'subnets': type.ListType(type.ReferenceType(__name__, 'Subnets.Info')),
        },
        ListResult,
        False,
        None))



    def list(self,
             namespace,
             ):
        """
        Returns NSX Subnets and SubnetSets entities related to a specific
        namespace.
        This method was added in **vSphere API 9.0.0.0**.

        :type  namespace: :class:`str`
        :param namespace: Identifier for the Namespace.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespaces.Instance``.
        :rtype: :class:`Subnets.ListResult`
        :return: List of entities, with the length of the list limited at 1000.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if namespace could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list',
                            {
                            'namespace': namespace,
                            })
class _SubnetsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'namespace': type.IdType(resource_types='com.vmware.vcenter.namespaces.Instance'),
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

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespaces/{namespace}/networks/nsx/subnets',
            path_variables={
                'namespace': 'namespace',
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
                'output_type': type.ReferenceType(__name__, 'Subnets.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespaces.networks.nsx.subnets',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Subnets': Subnets,
    }

