# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance_client``
module provides classes for NumberOfHostsPlusOneForMaintenance capability
offered by vCenter.

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


class CreateSpec(VapiStruct):
    """
    The ``CreateSpec`` class contains information to create a
    NumberOfHostsPlusOneForMaintenance policy, used to define a VM placement
    constraint, see :func:`com.vmware.vcenter.compute_client.Policies.create`. 
    
    The powered-on virtual machines in a vCenter cluster that share the tag
    indicated by :attr:`CreateSpec.vm_tag` will be on at most
    :attr:`CreateSpec.number_of_hosts` number of hosts. When one of these hosts
    is entering maintenance-mode, then until that host has entered
    maintenance-mode, these virtual machines will be on at most
    :attr:`CreateSpec.number_of_hosts` plus one number of hosts.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_tag=None,
                 number_of_hosts=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance',
                 name=None,
                 description=None,
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: Identifier of a tag that can be associated with a virtual machine. 
            
            Powered-on virtual machines in a vCenter cluster that share the tag
            indicated by :attr:`CreateSpec.vm_tag` will be on at most
            :attr:`CreateSpec.number_of_hosts` number of hosts. When one of
            these hosts is entering maintenance-mode, then until that host has
            entered maintenance-mode, these virtual machines will be on at most
            :attr:`CreateSpec.number_of_hosts` plus one number of hosts.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``. When methods return
            a value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``.
        :type  number_of_hosts: :class:`long`
        :param number_of_hosts: Placement of virtual machines will consider at most
            :attr:`CreateSpec.number_of_hosts` number of hosts. 
            
            Powered-on virtual machines in a vCenter cluster that share the tag
            indicated by :attr:`CreateSpec.vm_tag` will be on at most
            :attr:`CreateSpec.number_of_hosts` number of hosts. When one of
            these hosts is entering maintenance-mode, then until that host has
            entered maintenance-mode, these virtual machines will be on at most
            :attr:`CreateSpec.number_of_hosts` plus one number of hosts.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  capability: :class:`str`
        :param capability: Identifier of the capability this policy is based on.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``.
        :type  name: :class:`str`
        :param name: Name of the policy. The name needs to be unique within this vCenter
            server.
        :type  description: :class:`str`
        :param description: Description of the policy.
        """
        self.vm_tag = vm_tag
        self.number_of_hosts = number_of_hosts
        self._capability = capability
        self.name = name
        self.description = description
        VapiStruct.__init__(self)

    @property
    def capability(self):
        """
        Return the discriminator value
        """
        return self._capability

CreateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance.create_spec', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'number_of_hosts': type.IntegerType(),
        'capability': type.IdType(resource_types='com.vmware.vcenter.compute.policies.Capability'),
        'name': type.StringType(),
        'description': type.StringType(),
    },
    CreateSpec,
    False,
    None))



class Info(VapiStruct):
    """
    The ``Info`` class contains information about a
    NumberOfHostsPlusOneForMaintenance policy, see
    :func:`com.vmware.vcenter.compute_client.Policies.get`. 
    
    The powered-on virtual machines in a vCenter cluster that share the tag
    indicated by :attr:`Info.vm_tag` will be on at most
    :attr:`Info.number_of_hosts` number of hosts. When one of these hosts is
    entering maintenance-mode, then until that host has entered
    maintenance-mode, these virtual machines will be on at most
    :attr:`Info.number_of_hosts` plus one number of hosts.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_tag=None,
                 number_of_hosts=None,
                 name=None,
                 description=None,
                 capability='com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance',
                ):
        """
        :type  vm_tag: :class:`str`
        :param vm_tag: Identifier of a tag that can be associated with a virtual machine. 
            
            Powered-on virtual machines in a vCenter cluster that share the tag
            indicated by :attr:`Info.vm_tag` will be on at most
            :attr:`Info.number_of_hosts` number of hosts. When one of these
            hosts is entering maintenance-mode, then until that host has
            entered maintenance-mode, these virtual machines will be on at most
            :attr:`Info.number_of_hosts` plus one number of hosts.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``. When methods return
            a value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.cis.tagging.Tag:VirtualMachine``.
        :type  number_of_hosts: :class:`long`
        :param number_of_hosts: Placement of virtual machines will consider at most
            :attr:`Info.number_of_hosts` number of hosts. 
            
            Powered-on virtual machines in a vCenter cluster that share the tag
            indicated by :attr:`Info.vm_tag` will be on at most
            :attr:`Info.number_of_hosts` number of hosts. When one of these
            hosts is entering maintenance-mode, then until that host has
            entered maintenance-mode, these virtual machines will be on at most
            :attr:`Info.number_of_hosts` plus one number of hosts.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  name: :class:`str`
        :param name: Name of the policy.
        :type  description: :class:`str`
        :param description: Description of the policy.
        :type  capability: :class:`str`
        :param capability: Identifier of the capability this policy is based on.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.vcenter.compute.policies.Capability``.
        """
        self.vm_tag = vm_tag
        self.number_of_hosts = number_of_hosts
        self.name = name
        self.description = description
        self._capability = capability
        VapiStruct.__init__(self)

    @property
    def capability(self):
        """
        Return the discriminator value
        """
        return self._capability

Info._set_binding_type(type.StructType(
    'com.vmware.vcenter.compute.policies.capabilities.vm.placement.span.limit.number_of_hosts_plus_one_for_maintenance.info', {
        'vm_tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag:VirtualMachine'),
        'number_of_hosts': type.IntegerType(),
        'name': type.StringType(),
        'description': type.StringType(),
        'capability': type.IdType(resource_types='com.vmware.vcenter.compute.policies.Capability'),
    },
    Info,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

