# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespaces.mobility.virtualmachines.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespaces.mobility.virtualmachines_client`` module
provides classes for Supervisors' mobility operations for virtual machines. You
may use these classes to import VMs into Supervisor namespaces and take
advantages of Supervisor features that provide a consistent and streamlined
Kubernetes experience.

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


class Imports(VapiInterface):
    """
    The ``Imports`` class provides methods to manage importing VM into a
    Supervisor.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ImportsStub)
        self._VAPI_OPERATION_IDS = {}

    class ConditionStatus(Enum):
        """
        The ``Imports.ConditionStatus`` class describes the status of a condition.
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
        The condition is true.

        """
        FALSE = None
        """
        The condition is false.

        """
        UNKNOWN = None
        """
        The condition is unknown.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConditionStatus` instance.
            """
            Enum.__init__(string)

    ConditionStatus._set_values({
        'TRUE': ConditionStatus('TRUE'),
        'FALSE': ConditionStatus('FALSE'),
        'UNKNOWN': ConditionStatus('UNKNOWN'),
    })
    ConditionStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.condition_status',
        ConditionStatus))


    class CreateSpec(VapiStruct):
        """
        The ``Imports.CreateSpec`` class contains the specifications required to
        create an Import.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm=None,
                     storage_policy=None,
                     subnet_mappings=None,
                     network_customization=None,
                    ):
            """
            :type  vm: :class:`str`
            :param vm: The VM to be imported.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  storage_policy: :class:`str` or ``None``
            :param storage_policy: Storage policy to be used for the importing VM. A storage policy
                different from the VM's current storage policy might result in the
                associated storage resources being relocated to a datastore that
                conforms with the selected storage policy.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SpsStorageProfile``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SpsStorageProfile``.
                If None, and the target namespace has only a single storage policy,
                that storage policy will be used.
            :type  subnet_mappings: (:class:`dict` of :class:`str` and :class:`Imports.SubnetInfo`) or ``None``
            :param subnet_mappings: Map of network device keys to Subnet information specifying the
                Subnets to which the VM's network devices should be connected. 
                
                The key of the map is the device key of the network device on the
                VM, and the value is the Subnet information. Each device key must
                be unique within the map; overlapping or duplicate device keys are
                not allowed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``.
                If None, or any ethernet card is not specified, the default network
                configuration for the VM's target namespace will be used.
            :type  network_customization: :class:`Imports.NetworkCustomization` or ``None``
            :param network_customization: Network customization settings for Windows VM.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, Windows VM will not be able to receive new network
                identity assigned from the Supervisor workload network. This may
                result in a loss of network connectivity for VM that requires
                automated network identity configuration post import, such as
                systems not using DHCP. This field is not used for non-Windows VM.
            """
            self.vm = vm
            self.storage_policy = storage_policy
            self.subnet_mappings = subnet_mappings
            self.network_customization = network_customization
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.create_spec', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'storage_policy': type.OptionalType(type.IdType()),
            'subnet_mappings': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'Imports.SubnetInfo'))),
            'network_customization': type.OptionalType(type.ReferenceType(__name__, 'Imports.NetworkCustomization')),
        },
        CreateSpec,
        False,
        None))


    class SubnetInfo(VapiStruct):
        """
        The ``Imports.SubnetInfo`` class contains information identifying a Subnet.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     type=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the Subnet to which the network device should be
                connected. 
                
                This name corresponds to the
                :attr:`com.vmware.vcenter.namespaces.networks.nsx_client.Subnets.Info.name`
                field retrieved from the Subnets API.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  type: :class:`Imports.SubnetInfo.Entity` or ``None``
            :param type: The type of the Subnet, indicating whether it is a SUBNET or
                SUBNETSET. 
                
                This corresponds to the
                :attr:`com.vmware.vcenter.namespaces.networks.nsx_client.Subnets.Info.type`
                field retrieved from the Subnets API.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the :attr:`Imports.SubnetInfo.name` will be used to find
                the appropriate SUBNET or SUBNETSET. This is required if the same
                name is found for both SUBNET and SUBNETSET.
            """
            self.name = name
            self.type = type
            VapiStruct.__init__(self)


        class Entity(Enum):
            """
            The ``Imports.SubnetInfo.Entity`` enumerates the type of the entity listed
            supported by :class:`Imports`.
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
            A :attr:`Imports.SubnetInfo.Entity.SUBNET` in a VPC represents an
            independent layer 2 broadcast domain with its associated CIDR and
            properties like Access mode (network advertisement), DHCP configuration
            etc.

            """
            SUBNETSET = None
            """
            A :attr:`Imports.SubnetInfo.Entity.SUBNETSET` is a scalable grouping of VPC
            subnets sharing the same properties, which will allow auto-scale of
            networking availability to connect workloads.

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
            'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.subnet_info.entity',
            Entity))

    SubnetInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.subnet_info', {
            'name': type.StringType(),
            'type': type.OptionalType(type.ReferenceType(__name__, 'Imports.SubnetInfo.Entity')),
        },
        SubnetInfo,
        False,
        None))


    class CustomizationSysprepUserData(VapiStruct):
        """
        The ``Imports.CustomizationSysprepUserData`` class contains the personal
        data pertaining to the owner of the virtual machine. The
        CustomizationSysprepUserData data object type maps to the UserData key in
        the sysprep.inf answer file. These values are transferred directly into the
        sysprep.inf file that VirtualCenter stores on the target virtual disk.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     computer_name=None,
                     full_name=None,
                     org_name=None,
                     product_id=None,
                    ):
            """
            :type  computer_name: :class:`str`
            :param computer_name: The ``computerName`` attribute is the computer name of the Windows
                guest. Computer name may contain letters (A-Z), numbers(0-9), and
                hyphens (-) but no spaces or periods (.). The name may not consist
                entirely of digits. Computer name is limited to 15 characters in
                length due to a Windows restriction.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  full_name: :class:`str`
            :param full_name: User's full name.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  org_name: :class:`str`
            :param org_name: User's organization.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  product_id: :class:`str`
            :param product_id: The ``productId`` attribute is a valid serial number. Microsoft
                Sysprep requires that a valid serial number be included in the
                answer file when mini-setup runs. This serial number is ignored if
                the original guest operating system was installed using a
                volume-licensed CD.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.computer_name = computer_name
            self.full_name = full_name
            self.org_name = org_name
            self.product_id = product_id
            VapiStruct.__init__(self)


    CustomizationSysprepUserData._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.customization_sysprep_user_data', {
            'computer_name': type.StringType(),
            'full_name': type.StringType(),
            'org_name': type.StringType(),
            'product_id': type.SecretType(),
        },
        CustomizationSysprepUserData,
        False,
        None))


    class NetworkCustomization(VapiStruct):
        """
        The ``Imports.NetworkCustomization`` class contains network customization
        settings.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     customization_sysprep_user_data=None,
                    ):
            """
            :type  customization_sysprep_user_data: :class:`Imports.CustomizationSysprepUserData`
            :param customization_sysprep_user_data: CustomizationSysprepUserData is the user data for sysprep
                customization. Must be provided for Windows VM that requires
                automated network identity configuration post import through Guest
                OS Customization.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.customization_sysprep_user_data = customization_sysprep_user_data
            VapiStruct.__init__(self)


    NetworkCustomization._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.network_customization', {
            'customization_sysprep_user_data': type.ReferenceType(__name__, 'Imports.CustomizationSysprepUserData'),
        },
        NetworkCustomization,
        False,
        None))


    class State(VapiStruct):
        """
        The ``Imports.State`` class represents the observed state of the Import.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     conditions=None,
                     start_time=None,
                     completion_time=None,
                     virtual_machine_name=None,
                    ):
            """
            :type  conditions: :class:`list` of :class:`Imports.Condition` or ``None``
            :param conditions: List of conditions describing the current state of the Import.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if the Kubernetes resource associated
                with this operation is not yet created or ready to report
                conditions.
            :type  start_time: :class:`datetime.datetime` or ``None``
            :param start_time: The time when the operation starts in the Supervisor. It is
                represented in RFC3339 form and is UTC.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if the operation has not started yet.
            :type  completion_time: :class:`datetime.datetime` or ``None``
            :param completion_time: The time when the operation finishes in the Supervisor. It is
                represented in RFC3339 form and is UTC.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if the operation has not completed yet.
            :type  virtual_machine_name: :class:`str` or ``None``
            :param virtual_machine_name: The name of the virtual machine in the target namespace of the
                Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None until the VM is imported. The value
                corresponds to the name in vm-operator virtualmachine and does not
                match the display name in vCenter Server.
            """
            self.conditions = conditions
            self.start_time = start_time
            self.completion_time = completion_time
            self.virtual_machine_name = virtual_machine_name
            VapiStruct.__init__(self)


    State._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.state', {
            'conditions': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Imports.Condition'))),
            'start_time': type.OptionalType(type.DateTimeType()),
            'completion_time': type.OptionalType(type.DateTimeType()),
            'virtual_machine_name': type.OptionalType(type.StringType()),
        },
        State,
        False,
        None))


    class Condition(VapiStruct):
        """
        The ``Imports.Condition`` class represents a condition of the Import.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     reason=None,
                     status=None,
                     message=None,
                     last_transition_time=None,
                    ):
            """
            :type  type: :class:`str`
            :param type: The type of condition. 
                
                Possible values may include, but not limited to: 
                
                * SpecValid
                * NetworkBackingReady
                * VirtualMachineReadyForImport
                * VirtualMachineCreated
                * VirtualMachineReady
                * Completed
                * RollbackVirtualMachineLocationCompleted
                * RollbackVirtualMachinePropertyCompleted
                * RollbackCustomResourceCompleted
                * RollbackCompleted
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  reason: :class:`str`
            :param reason: The reason for the condition's last transition.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Imports.ConditionStatus`
            :param status: The status of the condition.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
            :param message: A human-readable message indicating details about the last
                transition.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if the message details are not required
                for taking actions. Some conditions are user actionable in order
                for the import operation to reach the desired state.
            :type  last_transition_time: :class:`datetime.datetime` or ``None``
            :param last_transition_time: Last time the condition transitioned from one status to another.
                This should be when the underlying condition changed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if there are no status transitions for
                the condition.
            """
            self.type = type
            self.reason = reason
            self.status = status
            self.message = message
            self.last_transition_time = last_transition_time
            VapiStruct.__init__(self)


    Condition._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.condition', {
            'type': type.StringType(),
            'reason': type.StringType(),
            'status': type.ReferenceType(__name__, 'Imports.ConditionStatus'),
            'message': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
            'last_transition_time': type.OptionalType(type.DateTimeType()),
        },
        Condition,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Imports.Info`` class represents an Import, containing both the spec
        and status.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'FAILED' : [('error', False), ('start_time', True), ('end_time', True)],
                    'RUNNING' : [('start_time', True)],
                    'BLOCKED' : [('start_time', True)],
                    'SUCCEEDED' : [('start_time', True), ('end_time', True)],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     spec=None,
                     state=None,
                     description=None,
                     service=None,
                     operation=None,
                     parent=None,
                     target=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                     user=None,
                    ):
            """
            :type  spec: :class:`Imports.CreateSpec`
            :param spec: Specification of the desired behavior of the operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  state: :class:`Imports.State`
            :param state: Observed state of the operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
            :type  service: :class:`str`
            :param service: Identifier of the service containing the operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.service``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.service``.
            :type  operation: :class:`str`
            :param operation: Identifier of the operation associated with the task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.operation``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.operation``.
            :type  parent: :class:`str` or ``None``
            :param parent: Parent of the current task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.task``. When methods return a value of this class
                as a return value, the attribute will be an identifier for the
                resource type: ``com.vmware.cis.task``.
                This attribute will be None if the task has no parent.
            :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param target: Identifier of the target created by the operation or an existing
                one the operation performed on.
                This attribute will be None if the operation has no target or
                multiple targets.
            :type  status: :class:`com.vmware.cis.task_client.Status`
            :param status: Status of the operation associated with the task.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED".
                If None the description of why the operation failed will be
                included in the result of the operation (see
                :attr:`com.vmware.cis.task_client.Info.result`).
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  user: :class:`str` or ``None``
            :param user: Name of the user who performed the operation.
                This attribute will be None if the operation is performed by the
                system.
            """
            self.spec = spec
            self.state = state
            self.description = description
            self.service = service
            self.operation = operation
            self.parent = parent
            self.target = target
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            self.user = user
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespaces.mobility.virtualmachines.imports.info', {
            'spec': type.ReferenceType(__name__, 'Imports.CreateSpec'),
            'state': type.ReferenceType(__name__, 'Imports.State'),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'service': type.IdType(resource_types='com.vmware.vapi.service'),
            'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
            'parent': type.OptionalType(type.IdType()),
            'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
            'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'user': type.OptionalType(type.StringType()),
        },
        Info,
        False,
        None))



    def create(self,
               namespace,
               spec,
               ):
        """
        Creates a new Import based on the specifications. 
        
        This API supports importing a single VM specified in the  into the
        target namespace. This will result in the VM becoming a VM Service
        managed VM. If the VM has First Class Disks attached, those First Class
        Disks will be registered to the Supervisor as PersistentVolumeClaim
        resources attached to the VM. 
        
        This API triggers a cancellable task and returns its identifier. Use
        this identifier to query basic task information by calling the
        Tasks.get method, or to query import operation-specific information
        through the :func:`Imports.get` task. The task is retained as per the
        default retention rules configured in vCenter. 
        
        This is a non-idempotent API that creates custom resources on the
        Supervisor as a side effect. If the API returns an error, manually
        address them before attempting import again. 
        
        After the import to the Supervisor, power cycles are required to
        perform guest customization to update the network configuration to
        restore network connectivity.
        This method was added in **vSphere API 9.0.0.0**.

        :type  namespace: :class:`str`
        :param namespace: Identifier for the namespace.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespaces.Instance``.
        :type  spec: :class:`Imports.CreateSpec`
        :param spec: Specification for the Import.
        :rtype: :class:`str`
        :return: The task identifier for the import operation.
            The return value will be an identifier for the resource type:
            ``com.vmware.cis.task``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the arguments are invalid. For example: 
            
            * If :attr:`Imports.CustomizationSysprepUserData.computer_name`
              does not conform to requirements.
            * If :attr:`Imports.CreateSpec.storage_policy` needs to be
              specified.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the specified resources (such as importing VM, target
            namespace, target storage, or target network) cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with the Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if the target namespace does not have sufficient resources for the
            importing VM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Edit privilege on the target
            Namespace and VirtualMachine.Namespaces.Transfer privilege on the
            VM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the Supervisor does not support importing VM.
        """
        return self._invoke('create',
                            {
                            'namespace': namespace,
                            'spec': spec,
                            })

    def get(self,
            namespace,
            task,
            ):
        """
        Retrieves information about a specific import operation, including its
        associated task info.
        This method was added in **vSphere API 9.0.0.0**.

        :type  namespace: :class:`str`
        :param namespace: Identifier for the namespace.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespaces.Instance``.
        :type  task: :class:`str`
        :param task: Task identifier for the Import.
            The parameter must be an identifier for the resource type:
            ``com.vmware.cis.task``.
        :rtype: :class:`Imports.Info`
        :return: Information about the specified operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the operation does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with the Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        """
        return self._invoke('get',
                            {
                            'namespace': namespace,
                            'task': task,
                            })
class _ImportsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'namespace': type.IdType(resource_types='com.vmware.vcenter.namespaces.Instance'),
            'spec': type.ReferenceType(__name__, 'Imports.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespaces/{namespace}/mobility/virtualmachines/imports',
            request_body_parameter='spec',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'namespace': type.IdType(resource_types='com.vmware.vcenter.namespaces.Instance'),
            'task': type.IdType(resource_types='com.vmware.cis.task'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/namespaces/{namespace}/mobility/virtualmachines/imports/{task}',
            path_variables={
                'namespace': 'namespace',
                'task': 'task',
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
                'output_type': type.IdType(resource_types='com.vmware.cis.task'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Imports.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespaces.mobility.virtualmachines.imports',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Imports': Imports,
    }

