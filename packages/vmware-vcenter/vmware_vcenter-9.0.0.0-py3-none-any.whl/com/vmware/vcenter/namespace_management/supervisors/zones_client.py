# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.supervisors.zones.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.supervisors.zones_client`` module
provides classes related to vSphere Zones for a Supervisor.

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


class Bindings(VapiInterface):
    """
    The ``Bindings`` class manages the bindings of vSphere Zones with
    Supervisors for placing workloads and control plane components.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.supervisors.zones.bindings'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _BindingsStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``Bindings.Type`` class represents the type of the vSphere Zone.
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
        The vSphere Zone is a zone which contains control plane components and
        workloads.

        """
        WORKLOAD = None
        """
        The vSphere Zone is a zone which only contains workloads.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'MANAGEMENT': Type('MANAGEMENT'),
        'WORKLOAD': Type('WORKLOAD'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.type',
        Type))


    class ConfigStatus(Enum):
        """
        The ``Bindings.ConfigStatus`` class describes the status of configuration
        for the vSphere Zone binding. When status is different than READY, desired
        configuration for vSphere Zone has not been realized.
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
        CONFIGURING = None
        """
        New configuration has been detected and is being applied to the vSphere
        Zone.

        """
        REMOVING = None
        """
        The vSphere Zone is being removed.

        """
        READY = None
        """
        The vSphere Zone configuration has been applied successfully.

        """
        ERROR = None
        """
        Failed to apply the configuration to the vSphere Zone, user intervention
        may be needed. See vSphere Zone :attr:`Bindings.Info.messages` for more
        details.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConfigStatus` instance.
            """
            Enum.__init__(string)

    ConfigStatus._set_values({
        'CONFIGURING': ConfigStatus('CONFIGURING'),
        'REMOVING': ConfigStatus('REMOVING'),
        'READY': ConfigStatus('READY'),
        'ERROR': ConfigStatus('ERROR'),
    })
    ConfigStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.config_status',
        ConfigStatus))


    class Info(VapiStruct):
        """
        The ``Bindings.Info`` class contains the information for a vSphere Zone
        related to a Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     zone=None,
                     type=None,
                     namespaces=None,
                     marked_for_removal=None,
                     status=None,
                     messages=None,
                     resource_allocation=None,
                    ):
            """
            :type  zone: :class:`str`
            :param zone: Identifier of the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``.
            :type  type: :class:`Bindings.Type`
            :param type: Type of the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  namespaces: :class:`list` of :class:`str`
            :param namespaces: List of vSphere Namespaces names associated with the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  marked_for_removal: :class:`bool`
            :param marked_for_removal: Indicates if vSphere Zone has been marked for removal.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Bindings.ConfigStatus`
            :param status: Indicates vSphere Zone's configuration status.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  messages: :class:`list` of :class:`com.vmware.vcenter.namespace_management.supervisors_client.Conditions.Message` or ``None``
            :param messages: List of messages populated when the vSphere Zone configuration was
                not successfully applied.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  resource_allocation: :class:`Bindings.ResourceAllocationInfo` or ``None``
            :param resource_allocation: Desired resource allocations for the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.zone = zone
            self.type = type
            self.namespaces = namespaces
            self.marked_for_removal = marked_for_removal
            self.status = status
            self.messages = messages
            self.resource_allocation = resource_allocation
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.info', {
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
            'type': type.ReferenceType(__name__, 'Bindings.Type'),
            'namespaces': type.ListType(type.StringType()),
            'marked_for_removal': type.BooleanType(),
            'status': type.OptionalType(type.ReferenceType(__name__, 'Bindings.ConfigStatus')),
            'messages': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors_client', 'Conditions.Message'))),
            'resource_allocation': type.OptionalType(type.ReferenceType(__name__, 'Bindings.ResourceAllocationInfo')),
        },
        Info,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Bindings.ListResult`` class contains the list of vSphere Zones
        associated with the Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     zones=None,
                    ):
            """
            :type  zones: :class:`list` of :class:`Bindings.Info`
            :param zones: List of vSphere Zones associated with the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.zones = zones
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.list_result', {
            'zones': type.ListType(type.ReferenceType(__name__, 'Bindings.Info')),
        },
        ListResult,
        False,
        None))


    class VirtualMachineClassAllocationSpec(VapiStruct):
        """
        The ``Bindings.VirtualMachineClassAllocationSpec`` class describes the
        definition of an allocation for Virtual Machines of a given class.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reserved_vm_class=None,
                     count=None,
                    ):
            """
            :type  reserved_vm_class: :class:`str`
            :param reserved_vm_class: Identifier of the Virtual Machine class used for allocation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  count: :class:`long`
            :param count: Number of instances of given Virtual Machine class.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.reserved_vm_class = reserved_vm_class
            self.count = count
            VapiStruct.__init__(self)


    VirtualMachineClassAllocationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.virtual_machine_class_allocation_spec', {
            'reserved_vm_class': type.StringType(),
            'count': type.IntegerType(),
        },
        VirtualMachineClassAllocationSpec,
        False,
        None))


    class VirtualMachineClassAllocationInfo(VapiStruct):
        """
        The ``Bindings.VirtualMachineClassAllocationInfo`` class contains
        information describing desired allocation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reserved_vm_class=None,
                     count=None,
                    ):
            """
            :type  reserved_vm_class: :class:`str`
            :param reserved_vm_class: Identifier of the Virtual Machine class used for allocation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  count: :class:`long`
            :param count: Number of instances of given Virtual Machine class.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.reserved_vm_class = reserved_vm_class
            self.count = count
            VapiStruct.__init__(self)


    VirtualMachineClassAllocationInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.virtual_machine_class_allocation_info', {
            'reserved_vm_class': type.StringType(),
            'count': type.IntegerType(),
        },
        VirtualMachineClassAllocationInfo,
        False,
        None))


    class ResourceAllocationSpec(VapiStruct):
        """
        The ``Bindings.ResourceAllocationSpec`` class contains configuration of
        resources on a vSphere Zone associated with the Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm_reservations=None,
                    ):
            """
            :type  vm_reservations: :class:`list` of :class:`Bindings.VirtualMachineClassAllocationSpec` or ``None``
            :param vm_reservations: Identifier and quantities of Virtual Machine Classes for which
                instances should be reserved.
                This attribute was added in **vSphere API 9.0.0.0**.
                If unset vSphere Zone will have no Virtual Machine Class Instances
                reserved.
            """
            self.vm_reservations = vm_reservations
            VapiStruct.__init__(self)


    ResourceAllocationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.resource_allocation_spec', {
            'vm_reservations': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Bindings.VirtualMachineClassAllocationSpec'))),
        },
        ResourceAllocationSpec,
        False,
        None))


    class ResourceAllocationInfo(VapiStruct):
        """
        The ``Bindings.ResourceAllocationInfo`` class contains information about
        resource allocation on a vSphere Zone associated with the Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm_reservations=None,
                    ):
            """
            :type  vm_reservations: :class:`list` of :class:`Bindings.VirtualMachineClassAllocationInfo` or ``None``
            :param vm_reservations: Identifier and quantities of Virtual Machines for which
                reservations are desired.
                This attribute was added in **vSphere API 9.0.0.0**.
                If unset vSphere Zone will have no Virtual Machine Class Instances
                reserved.
            """
            self.vm_reservations = vm_reservations
            VapiStruct.__init__(self)


    ResourceAllocationInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.resource_allocation_info', {
            'vm_reservations': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Bindings.VirtualMachineClassAllocationInfo'))),
        },
        ResourceAllocationInfo,
        False,
        None))


    class ZoneSpec(VapiStruct):
        """
        The ``Bindings.ZoneSpec`` class contains the input parameters for creating
        the bindings between the vSphere Zone and a Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     zone=None,
                     type=None,
                     resource_allocation=None,
                    ):
            """
            :type  zone: :class:`str`
            :param zone: Identifiers of the vSphere Zone to bind with the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.consumption_domains.Zone``.
            :type  type: :class:`Bindings.Type` or ``None``
            :param type: Type of the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the type of the vSphere Zone is default to
                :attr:`Bindings.Type.WORKLOAD`.
            :type  resource_allocation: :class:`Bindings.ResourceAllocationSpec` or ``None``
            :param resource_allocation: Resource allocation to be configured on the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no resources will be allocated to the Supervisor in this
                vSphere Zone.
            """
            self.zone = zone
            self.type = type
            self.resource_allocation = resource_allocation
            VapiStruct.__init__(self)


    ZoneSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.zone_spec', {
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
            'type': type.OptionalType(type.ReferenceType(__name__, 'Bindings.Type')),
            'resource_allocation': type.OptionalType(type.ReferenceType(__name__, 'Bindings.ResourceAllocationSpec')),
        },
        ZoneSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Bindings.UpdateSpec`` class contains parameters for updating the
        configuration of the specified vSphere Zone bound to the given Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     resource_allocation=None,
                    ):
            """
            :type  resource_allocation: :class:`Bindings.ResourceAllocationSpec` or ``None``
            :param resource_allocation: Resource allocation to be configured on the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, resource allocation will not be changed.
            """
            self.resource_allocation = resource_allocation
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.update_spec', {
            'resource_allocation': type.OptionalType(type.ReferenceType(__name__, 'Bindings.ResourceAllocationSpec')),
        },
        UpdateSpec,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``Bindings.SetSpec`` class contains parameters for updating the
        configuration of the specified vSphere Zone bound to the given Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     resource_allocation=None,
                    ):
            """
            :type  resource_allocation: :class:`Bindings.ResourceAllocationSpec` or ``None``
            :param resource_allocation: Resource allocation to be configured on the vSphere Zone.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no resources will be allocated to the Supervisor in this
                vSphere Zone.
            """
            self.resource_allocation = resource_allocation
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.set_spec', {
            'resource_allocation': type.OptionalType(type.ReferenceType(__name__, 'Bindings.ResourceAllocationSpec')),
        },
        SetSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Bindings.CreateSpec`` class contains the input parameters for
        creating the bindings between the vSphere Zones and a Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     specs=None,
                    ):
            """
            :type  specs: :class:`list` of :class:`Bindings.ZoneSpec`
            :param specs: List of vSphere Zones to bind to the Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.specs = specs
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.zones.bindings.create_spec', {
            'specs': type.ListType(type.ReferenceType(__name__, 'Bindings.ZoneSpec')),
        },
        CreateSpec,
        False,
        None))



    def create(self,
               supervisor,
               spec,
               ):
        """
        Associates a list of vSphere Zones to the given Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  spec: :class:`Bindings.CreateSpec`
        :param spec: A list of vSphere Zones to bind to the Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the zones feature is not enabled.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if any of the zones was already associated with a different
            Supervisor since a vSphere Zone can only be associated with one
            Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Zone ID provided in specs or ``supervisor`` is not found in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the Namespaces.Manage privilege.
        """
        return self._invoke('create',
                            {
                            'supervisor': supervisor,
                            'spec': spec,
                            })

    def list(self,
             supervisor,
             ):
        """
        Lists the vSphere Zones bound to the given Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :rtype: :class:`Bindings.ListResult`
        :return: The list of vSphere Zones bound to the Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ID ``supervisor`` is not found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the System.Read privilege.
        """
        return self._invoke('list',
                            {
                            'supervisor': supervisor,
                            })

    def delete(self,
               supervisor,
               zone,
               ):
        """
        Removes the binding of the vSphere Zone from a Supervisor. 
        
        By default, zones will be marked for deletion. When zones are marked,
        new workloads will not be permitted to be scheduled on the zone, and
        existing workloads will not be permitted to restart. The users will
        need to remove their workloads from the zone in all namespaces. Once
        drained of all workloads, the zone deletion from the Supervisor will
        complete automatically. This gives the user the opportunity to
        gracefully stop their workloads and reschedule them on available zones
        in their namespace.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  zone: :class:`str`
        :param zone: The ID of the vSphere Zone to remove from the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the zone is a management zone or the last zone in a supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ID ``zone`` or ``supervisor`` is not found in the system or
            ``zone`` is not associated with the ``supervisor``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the zones feature is not enabled.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the vSphere Zone being deleted is of type
            :attr:`Bindings.Type.MANAGEMENT` or if the Supervisor is in
            REMOVING state.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the Namespaces.Manage privilege.
        """
        return self._invoke('delete',
                            {
                            'supervisor': supervisor,
                            'zone': zone,
                            })

    def update(self,
               supervisor,
               zone,
               spec,
               ):
        """
        Patches the configuration of Supervisor to vSphere Zone binding.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  zone: :class:`str`
        :param zone: The ID of the vSphere Zone.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``.
        :type  spec: :class:`Bindings.UpdateSpec`
        :param spec: The UpdateSpec specifying new configuration for vSphere Zone.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ID ``zone`` or ``supervisor`` is not found in the system or
            ``zone`` is not associated with the ``supervisor``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the zones feature is not enabled.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the vSphere Zone is being deleted.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the Namespaces.Manage privilege.
        """
        return self._invoke('update',
                            {
                            'supervisor': supervisor,
                            'zone': zone,
                            'spec': spec,
                            })

    def set(self,
            supervisor,
            zone,
            spec,
            ):
        """
        Reconfigures the Supervisor to vSphere Zone binding.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  zone: :class:`str`
        :param zone: The ID of the vSphere Zone.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.consumption_domains.Zone``.
        :type  spec: :class:`Bindings.SetSpec`
        :param spec: The SetSpec specifying new configuration for vSphere Zone.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the zones feature is not enabled.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the ID ``zone`` or ``supervisor`` is not found in the system or
            ``zone`` is not associated with the ``supervisor``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the vSphere Zone is being deleted.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the Namespaces.Manage privilege.
        """
        return self._invoke('set',
                            {
                            'supervisor': supervisor,
                            'zone': zone,
                            'spec': spec,
                            })
class _BindingsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'spec': type.ReferenceType(__name__, 'Bindings.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/zones/bindings',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/zones/bindings',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/zones/{zone}/bindings',
            path_variables={
                'supervisor': 'supervisor',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
            'spec': type.ReferenceType(__name__, 'Bindings.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/zones/{zone}/bindings',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'zone': type.IdType(resource_types='com.vmware.vcenter.consumption_domains.Zone'),
            'spec': type.ReferenceType(__name__, 'Bindings.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/zones/{zone}/bindings',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
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
            'create': {
                'input_type': create_input_type,
                'output_type': type.VoidType(),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Bindings.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'list': list_rest_metadata,
            'delete': delete_rest_metadata,
            'update': update_rest_metadata,
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.supervisors.zones.bindings',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Bindings': Bindings,
    }

