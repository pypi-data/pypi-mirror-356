# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles_client``
module provides classes and classes for managing VPC Connectivity Profile
resources.

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
    Supervisor enablement compatibility information of VPC Connectivity
    Profiles.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles.compatibility'
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
        The ``Compatibility.Summary`` class contains information about a VPC
        Connectivity Profile, including whether it is compatible with the
        Supervisor enablement feature and incompatibility reasons.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     profile=None,
                     name=None,
                     nsx_path=None,
                     compatible=None,
                     incompatibility_reasons=None,
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
            :param name: User-friendly identifier of the VPC Connectivity Profile.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nsx_path: :class:`str`
            :param nsx_path: NSX path of the VPC Connectivity Profile.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compatible: :class:`bool`
            :param compatible: Compatibility of this VPC Connectivity Profile with Supervisor
                enablement.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  incompatibility_reasons: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param incompatibility_reasons: List of reasons for incompatibility. If
                :attr:`Compatibility.Summary.compatible` is true, this list will be
                empty.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.profile = profile
            self.name = name
            self.nsx_path = nsx_path
            self.compatible = compatible
            self.incompatibility_reasons = incompatibility_reasons
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles.compatibility.summary', {
            'profile': type.IdType(resource_types='VpcConnectivityProfile'),
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
              profile,
              ):
        """
        Check the given VPC Connectivity Profile compatibility with a
        Supervisor enablement. A valid VPC Connectivity Profile requires that a
        Gateway Connection exists in the Transit Gateway External Attachment,
        External IP Blocks exist, and Auto SNAT is enabled.
        This method was added in **vSphere API 9.0.0.0**.

        :type  project: :class:`str`
        :param project: Identifier of the Project.
            The parameter must be an identifier for the resource type:
            ``NSXProject``.
        :type  profile: :class:`str`
        :param profile: Identifier of the VPC Connectivity Profile.
            The parameter must be an identifier for the resource type:
            ``VpcConnectivityProfile``.
        :rtype: :class:`Compatibility.Summary`
        :return: VPC Connectivity Profile compatibility summaries.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``project`` or ``profile`` cannot be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have ``System.Read`` privilege.
        """
        return self._invoke('check',
                            {
                            'project': project,
                            'profile': profile,
                            })
class _CompatibilityStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'project': type.IdType(resource_types='NSXProject'),
            'profile': type.IdType(resource_types='VpcConnectivityProfile'),
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
            url_template='/vcenter/namespace-management/networks/nsx/projects/{project}/vpc-connectivity-profiles/{profile}?action=check-compatibility',
            path_variables={
                'project': 'project',
                'profile': 'profile',
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
            self, iface_name='com.vmware.vcenter.namespace_management.networks.nsx.projects.vpcconnectivityprofiles.compatibility',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Compatibility': Compatibility,
    }

