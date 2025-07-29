# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespaces.instances.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespaces.instances_client`` module provides class
for managing vSphere zones associated with namespaces.

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


class Zones(VapiInterface):
    """
    The ``Zones`` class provides methods to manage vSphere zones associated
    with namespaces.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespaces.instances.zones'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ZonesStub)
        self._VAPI_OPERATION_IDS = {}


    def delete(self,
               namespace,
               zone,
               ):
        """
        Removes the zone from a vSphere namespace. 
        
        By default, zones will be marked for deletion. When zones are marked,
        new workloads will not be permitted to be scheduled on the zone, and
        existing workloads will not be permitted to restart. The users will
        need to remove their workloads from the zone. Once drained of all
        workloads, the zone deletion from the namespace will complete
        automatically. This gives the user the opportunity to gracefully stop
        their workloads and reschedule them on other available zones in the
        namespace.
        This method was added in **vSphere API 9.0.0.0**.

        :type  namespace: :class:`str`
        :param namespace: Identifier for the namespace.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespaces.Instance``.
        :type  zone: :class:`str`
        :param zone: Identifier for the zone to be removed.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            for any other error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ID ``namespace`` or ``zone`` could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Configure privilege.
        """
        return self._invoke('delete',
                            {
                            'namespace': namespace,
                            'zone': zone,
                            })
class _ZonesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'namespace': type.IdType(resource_types='com.vmware.vcenter.namespaces.Instance'),
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/namespaces/instances/{namespace}/zones/{zone}',
            path_variables={
                'namespace': 'namespace',
                'zone': 'zone',
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
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespaces.instances.zones',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Zones': Zones,
    }

