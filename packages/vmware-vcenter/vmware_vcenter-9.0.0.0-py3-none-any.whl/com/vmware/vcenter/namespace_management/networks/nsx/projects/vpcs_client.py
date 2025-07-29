# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs_client``
module provides classes and classes for managing VPC resources.

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
    Namespaces compatibility information of VPCs.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.compatibility'
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
        including whether it is compatible with the vCenter Namespaces feature and
        incompatibility reasons.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vpc=None,
                     name=None,
                     nsx_path=None,
                     compatible=None,
                     incompatibility_reasons=None,
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
            :param name: User-friendly identifier of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the VPC.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compatible: :class:`bool`
            :param compatible: Compatibility of this VPC with the given Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  incompatibility_reasons: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param incompatibility_reasons: List of reasons for incompatibility. If
                :attr:`Compatibility.Summary.compatible` is true, this list will be
                empty.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vpc = vpc
            self.name = name
            self.nsx_path = nsx_path
            self.compatible = compatible
            self.incompatibility_reasons = incompatibility_reasons
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.compatibility.summary', {
            'vpc': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.Vpc'),
            'name': type.StringType(),
            'nsx_path': type.StringType(),
            'compatible': type.BooleanType(),
            'incompatibility_reasons': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        Summary,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Compatibility.FilterSpec`` class contains attributes used to filter
        the results when checking VPCs compatibility (see
        :func:`Compatibility.check`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     supervisor=None,
                    ):
            """
            :type  supervisor: :class:`str`
            :param supervisor: Identifier for the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
            """
            self.supervisor = supervisor
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.compatibility.filter_spec', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
        },
        FilterSpec,
        False,
        None))



    def check(self,
              project,
              vpc,
              filter,
              ):
        """
        Check the given VPC's compatibility for Namespace creation. Compatible
        VPCs: 1. Belong to a compatible NSX Project (see
        :func:`com.vmware.vcenter.namespace_management.networks.nsx.projects_client.Compatibility.check`)
        and has a compatible VPC Connectivity Profile (see
        :func:`com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles_client.Compatibility.check`).
        2. Contain no IP configurations (External IP Blocks, PrivateTGW IP
        Blocks, or Private CIDRs) that overlap with Service CIDRs. 3. Are not
        auto-created by Supervisor or VCF Automation. 4. Have a Load Balancer
        configured: if NSX LB used, check a LB instance is created under the
        VPC, if AVI is used, check LoadBalancer Endpoint is enabled in the VPC.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  vpc: :class:`str`
        :param vpc: Identifier of the VPC.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.networks.nsx.Vpc``.
        :type  filter: :class:`Compatibility.FilterSpec`
        :param filter: Specification of matching VPC for which information should be
            returned.
        :rtype: :class:`Compatibility.Summary`
        :return: VPC compatibility summaries.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``filter`` contain any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` or ``vpc`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('check',
                            {
                            'project': project,
                            'vpc': vpc,
                            'filter': filter,
                            })
class _CompatibilityStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'vpc': type.IdType(resource_types='com.vmware.vcenter.namespace_management.networks.nsx.Vpc'),
            'filter': type.ReferenceType(__name__, 'Compatibility.FilterSpec'),
        })
        check_error_dict = {
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
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpcs/{vpc}?action=check-compatibility',
            path_variables={
                'project': 'project',
                'vpc': 'vpc',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': check_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'check': check_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcs.compatibility',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Compatibility': Compatibility,
    }

