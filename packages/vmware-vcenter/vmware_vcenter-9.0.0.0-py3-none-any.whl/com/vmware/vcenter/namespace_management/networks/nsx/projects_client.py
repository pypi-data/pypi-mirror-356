# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.nsx.projects.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.networks.nsx.projects_client``
module provides classes and classes for managing NSX Projects resources.

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


class Compatibility(VapiInterface):
    """
    The ``Compatibility`` class provides methods to retrieve the basic and
    Supervisor enablement compatibility information of Projects.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects.compatibility'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CompatibilityStub)
        self._VAPI_OPERATION_IDS = {}

    class Summary(VapiStruct):
        """
        The ``Compatibility.Summary`` class contains information about a Project,
        including whether it is compatible with the Supervisor enablement feature
        and incompatibility reasons.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     project=None,
                     name=None,
                     nsx_path=None,
                     compatible=None,
                     incompatibility_reasons=None,
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
            :param name: User-friendly identifier of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the Project.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compatible: :class:`bool`
            :param compatible: Compatibility of this Project with Supervisor enablement.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  incompatibility_reasons: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param incompatibility_reasons: List of reasons for incompatibility. If
                :attr:`Compatibility.Summary.compatible` is true, this list will be
                empty.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.project = project
            self.name = name
            self.nsx_path = nsx_path
            self.compatible = compatible
            self.incompatibility_reasons = incompatibility_reasons
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.compatibility.summary', {
            'project': type.IdType(resource_types='NSXProject'),
            'name': type.StringType(),
            'nsx_path': type.StringType(),
            'compatible': type.BooleanType(),
            'incompatibility_reasons': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Summary,
        False,
        None))



    def check(self,
              project,
              ):
        """
        Check if the given NSX project is compatible for Supervisor enablement.
        Validation checks: NSX project is constrained to the "default" Overlay
        Transport Zone in NSX.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :rtype: :class:`Compatibility.Summary`
        :return: Project summary with details about incompatibities if any.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('check',
                            {
                            'project': project,
                            })
class VpcConnectivityProfiles(VapiInterface):
    """
    The ``VpcConnectivityProfiles`` provides methods to get information of VPC
    Connectivity Profiles.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profiles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VpcConnectivityProfilesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``VpcConnectivityProfiles.Info`` class contains information about a VPC
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
                ``VpcConnectivityProfile``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``VpcConnectivityProfile``.
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
            :param default_profile: ``true`` if this profile is the default VPC connectivity profile in
                the NSX project that profiles belongs to, ``false`` otherwise.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  external_ip_blocks: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks.nsx_client.IPBlockInfo` or ``None``
            :param external_ip_blocks: List of NSX external IP blocks currently configured with the VPC
                Connectivity Profile.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no external IP blocks are defined in the VPC Connectivity
                Profile.
            :type  privatetgw_ip_blocks: :class:`list` of :class:`com.vmware.vcenter.namespace_management.networks.nsx_client.IPBlockInfo` or ``None``
            :param privatetgw_ip_blocks: List of NSX private TGW IP blocks currently configured with the VPC
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


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profiles.info', {
            'profile': type.IdType(resource_types='VpcConnectivityProfile'),
            'name': type.StringType(),
            'nsx_path': type.StringType(),
            'description': type.OptionalType(type.StringType()),
            'default_profile': type.BooleanType(),
            'external_IP_blocks': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.nsx_client', 'IPBlockInfo'))),
            'privateTGW_IP_blocks': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.networks.nsx_client', 'IPBlockInfo'))),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``VpcConnectivityProfiles.FilterSpec`` class contains attributes used
        to filter the results when listing VPC Connectivity Profiles.
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
            :param compatible: Compatibility criteria for matching the filter. If true, only VPC
                Connectivity Profiles which are compatible with Supervisor
                enablement match the filter. If false, only VPC Connectivity
                Profiles which are incompatible with Supervisor enablement match
                the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, both compatible and incompatible VPC Connectivity Profiles
                match the filter.
            """
            self.compatible = compatible
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profiles.filter_spec', {
            'compatible': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``VpcConnectivityProfiles.ListResult`` class represents the result of
        the :func:`VpcConnectivityProfiles.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     profiles=None,
                    ):
            """
            :type  profiles: :class:`list` of :class:`VpcConnectivityProfiles.Info`
            :param profiles: List of all VPC Connectivity Profiles.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.profiles = profiles
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profiles.list_result', {
            'profiles': type.ListType(type.ReferenceType(__name__, 'VpcConnectivityProfiles.Info')),
        },
        ListResult,
        False,
        None))



    def list(self,
             project,
             filter=None,
             ):
        """
        Returns a list of VPC Connectivity Profiles matching the given filter.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  filter: :class:`VpcConnectivityProfiles.FilterSpec` or ``None``
        :param filter: Specification of matching Profiles for which information should be
            returned.
            If None, the behavior is equivalent to a
            :class:`VpcConnectivityProfiles.FilterSpec` with all attributes
            None which means all VPC Connectivity Profiles will be returned.
        :rtype: :class:`VpcConnectivityProfiles.ListResult`
        :return: List of VPC Connectivity Profiles matching the given filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('list',
                            {
                            'project': project,
                            'filter': filter,
                            })

    def get(self,
            project,
            profile,
            ):
        """
        Returns information of a VPC Connectivity Profile.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  profile: :class:`str`
        :param profile: Identifier of the VPC Connectivity Profile.
            The parameter must be an identifier for the resource type:
            ``VpcConnectivityProfile``.
        :rtype: :class:`VpcConnectivityProfiles.Info`
        :return: Information about a VPC Connectivity Profile.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``profile`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'project': project,
                            'profile': profile,
                            })
class Vpcs(VapiInterface):
    """
    The ``Vpcs`` class provides methods to retrieve the basic information for
    VPCs.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VpcsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Vpcs.Info`` class contains the basic information about a VPC.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vpc=None,
                     name=None,
                     nsx_path=None,
                     vpc_connectivity_profile=None,
                     private_ips=None,
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
            :param name: Human-readable identifier of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vpc_connectivity_profile: :class:`str`
            :param vpc_connectivity_profile: VPC Connectivity Profile of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VpcConnectivityProfile``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``VpcConnectivityProfile``.
            :type  private_ips: :class:`list` of :class:`str`
            :param private_ips: Private IPs of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vpc = vpc
            self.name = name
            self.nsx_path = nsx_path
            self.vpc_connectivity_profile = vpc_connectivity_profile
            self.private_ips = private_ips
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.info', {
            'vpc': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.Vpc'),
            'name': type.StringType(),
            'nsx_path': type.StringType(),
            'vpc_connectivity_profile': type.IdType(resource_types='VpcConnectivityProfile'),
            'private_ips': type.ListType(type.StringType()),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Vpcs.FilterSpec`` class contains attributes used to filter the
        results when listing VPCs (see :func:`Vpcs.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     supervisor=None,
                     compatible=None,
                    ):
            """
            :type  supervisor: :class:`str` or ``None``
            :param supervisor: Identifier for the Supervisor. It must be set if
                :attr:`Vpcs.FilterSpec.compatible` is :class:`set`.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
                If None, :attr:`Vpcs.FilterSpec.compatible` also needs None.
            :type  compatible: :class:`bool` or ``None``
            :param compatible: Compatibility criteria. If true, only VPCs which are compatible
                with the given Supervisor will be returned. If false, only VPCs
                incompatible with the given Supervisor will be returned.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, both compatible and incompatible VPCs will be returned.
            """
            self.supervisor = supervisor
            self.compatible = compatible
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.filter_spec', {
            'supervisor': type.OptionalType(type.IdType()),
            'compatible': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Vpcs.ListResult`` class represents the result of the
        :func:`Vpcs.list` method. With :attr:`Vpcs.FilterSpec.compatible` set to
        true, will only return compatible VPCs that have been pre-created on NSX,
        filtering out pre-created VPCs from Supervisor or VCF Automation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vpcs=None,
                    ):
            """
            :type  vpcs: :class:`list` of :class:`Vpcs.Info`
            :param vpcs: List of all VPCs.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vpcs = vpcs
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.list_result', {
            'vpcs': type.ListType(type.ReferenceType(__name__, 'Vpcs.Info')),
        },
        ListResult,
        False,
        None))



    def list(self,
             project,
             filter,
             ):
        """
        Returns a list of VPCs matching the given filter.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  filter: :class:`Vpcs.FilterSpec`
        :param filter: Specification of matching VPCs for which information should be
            returned.
        :rtype: :class:`Vpcs.ListResult`
        :return: List of VPC summaries matching the given filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if one or more fields of the :class:`Vpcs.FilterSpec` is incorrect.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` cannot be found in NSX.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('list',
                            {
                            'project': project,
                            'filter': filter,
                            })

    def get(self,
            project,
            vpc,
            ):
        """
        Returns information of a VPC.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  vpc: :class:`str`
        :param vpc: Identifier of the VPC.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.Vpc``.
        :rtype: :class:`Vpcs.Info`
        :return: Information about a VPC.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` or ``vpc`` cannot be found in NSX.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'project': project,
                            'vpc': vpc,
                            })
class _CompatibilityStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}?action=check-compatibility',
            path_variables={
                'project': 'project',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-compatibility',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'check': {
                'input_type': check_input_type,
                'output_type': type.ReferenceType(__name__, 'Compatibility.Summary'),
                'errors': check_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'check': check_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects.compatibility',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VpcConnectivityProfilesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'VpcConnectivityProfiles.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpc-connectivity-profiles',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'profile': type.IdType(resource_types='VpcConnectivityProfile'),
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
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpc-connectivity-profiles/{profile}',
            path_variables={
                'project': 'project',
                'profile': 'profile',
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
                'output_type': type.ReferenceType(__name__, 'VpcConnectivityProfiles.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'VpcConnectivityProfiles.Info'),
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
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects.vpc_connectivity_profiles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VpcsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'filter': type.ReferenceType(__name__, 'Vpcs.FilterSpec'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpcs',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'vpc': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.Vpc'),
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
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpcs/{vpc}',
            path_variables={
                'project': 'project',
                'vpc': 'vpc',
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
                'output_type': type.ReferenceType(__name__, 'Vpcs.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Vpcs.Info'),
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
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Compatibility': Compatibility,
        'VpcConnectivityProfiles': VpcConnectivityProfiles,
        'Vpcs': Vpcs,
        'vpcconnectivityprofiles': 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles_client.StubFactory',
        'vpcs': 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs_client.StubFactory',
    }

