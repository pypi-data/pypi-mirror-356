# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.network.projects.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.network.projects_client`` module provides classes to
manage vpc projects.

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


class Vpcs(VapiInterface):
    """
    The ``Vpcs`` class provides methods to manage VPC(Virtual Private Cloud) in
    vCenter.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.network.projects.vpcs'
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

    class FilterSpec(VapiStruct):
        """
        The ``Vpcs.FilterSpec`` class contains attributes used to filter the
        results when listing VPCs. If multiple attributes are specified, only VPCs
        matching all of the attributes match the filter.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ids=None,
                     names=None,
                     external_ids=None,
                    ):
            """
            :type  ids: :class:`set` of :class:`str` or ``None``
            :param ids: Identifiers that VPC must have to match the filter (see
                :attr:`Vpcs.VpcInfo.id`).
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.network.vpc``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.network.vpc``.
                If None or empty, VPC with any ID match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that VPC must have to match the filter (see
                :attr:`Vpcs.VpcInfo.name`).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or empty, VPC with any name match the filter.
            :type  external_ids: :class:`set` of :class:`str` or ``None``
            :param external_ids: External identifiers that VPC must have to match the filter (see
                :attr:`Vpcs.VpcInfo.external_id`).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or empty, VPC with any external identifier match the
                filter.
            """
            self.ids = ids
            self.names = names
            self.external_ids = external_ids
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.projects.vpcs.filter_spec', {
            'ids': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'external_ids': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class VpcInfo(VapiStruct):
        """
        The ``Vpcs.VpcInfo`` class contains details of a VPC in vCenter.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     name=None,
                     external_id=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.network.vpc``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.vcenter.network.vpc``.
            :type  name: :class:`str`
            :param name: Name of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  external_id: :class:`str`
            :param external_id: External identifier of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.name = name
            self.external_id = external_id
            VapiStruct.__init__(self)


    VpcInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.projects.vpcs.vpc_info', {
            'id': type.IdType(resource_types='com.vmware.vcenter.network.vpc'),
            'name': type.StringType(),
            'external_id': type.StringType(),
        },
        VpcInfo,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Vpcs.ListResult`` class represents the result of :func:`Vpcs.list`
        method.
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
            :param vpcs: Info(s) of VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vpcs = vpcs
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.projects.vpcs.list_result', {
            'vpcs': type.ListType(type.ReferenceType(__name__, 'Vpcs.Info')),
        },
        ListResult,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Vpcs.Info`` class contains commonly used information about a certain
        VPC.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vpc=None,
                     project=None,
                    ):
            """
            :type  vpc: :class:`Vpcs.VpcInfo`
            :param vpc: Details of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  project: :class:`com.vmware.vcenter.network_client.Projects.ProjectInfo`
            :param project: Details of the project.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vpc = vpc
            self.project = project
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.projects.vpcs.info', {
            'vpc': type.ReferenceType(__name__, 'Vpcs.VpcInfo'),
            'project': type.ReferenceType('com.vmware.vcenter.network_client', 'Projects.ProjectInfo'),
        },
        Info,
        False,
        None))



    def list(self,
             project,
             filter=None,
             ):
        """
        Returns information about VPCs in vCenter matching the
        :class:`Vpcs.FilterSpec`.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the project to which the VPC belongs.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.network.vpc``.
        :type  filter: :class:`Vpcs.FilterSpec` or ``None``
        :param filter: Specification of matching VPCs for which information should be
            returned.
            If None, the behavior is equivalent to a :class:`Vpcs.FilterSpec`
            with all attributes None which means all VPC match the filter.
        :rtype: :class:`Vpcs.ListResult`
        :return: Commonly used information about the VPC matching the
            :class:`Vpcs.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
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
        Returns information about a certain VPC in vCenter
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the project to which the VPC belongs.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.network.vpc``.
        :type  vpc: :class:`str`
        :param vpc: Identifier of the VPC.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.network.vpc``.
        :rtype: :class:`Vpcs.Info`
        :return: Commonly used information about this certain VPC matching
            ``project`` and ``vpc``.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if no matching VPC found.
        """
        return self._invoke('get',
                            {
                            'project': project,
                            'vpc': vpc,
                            })
class _VpcsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='com.vmware.vcenter.network.vpc'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Vpcs.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
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
            url_template='/vcenter/network/projects/{project}/vpcs',
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
            'project': type.IdType(resource_types='com.vmware.vcenter.network.vpc'),
            'vpc': type.IdType(resource_types='com.vmware.vcenter.network.vpc'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/network/projects/{project}/vpcs/{vpc}',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Vpcs.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).build(),
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
            self, iface_name='com.vmware.vcenter.network.projects.vpcs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Vpcs': Vpcs,
        'vpcs': 'com.vmware.vcenter.network.projects.vpcs_client.StubFactory',
    }

