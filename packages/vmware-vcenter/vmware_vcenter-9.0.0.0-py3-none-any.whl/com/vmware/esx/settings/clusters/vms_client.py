# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.clusters.vms.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.clusters.vms_client`` module provides classes to
manage the System VM Solutions on an ESXi cluster through a desired state
specification.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from com.vmware.cis_client import Tasks
from vmware.vapi.stdlib.client.task import Task
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

class LifecycleState(Enum):
    """
    The ``LifecycleState`` class contains the different VM lifecycle states a
    solution can hook into. See :class:`LifecycleHooks` and
    :class:`SolutionSpec`.
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
    POST_PROVISIONING = None
    """
    Post VM provisioning, reached once immediately after a VM is created.

    """
    POST_POWER_ON = None
    """
    Post VM power-on, reached immediately after every VM power-on.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`LifecycleState` instance.
        """
        Enum.__init__(string)

LifecycleState._set_values({
    'POST_PROVISIONING': LifecycleState('POST_PROVISIONING'),
    'POST_POWER_ON': LifecycleState('POST_POWER_ON'),
})
LifecycleState._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.lifecycle_state',
    LifecycleState))



class DiskType(Enum):
    """
    The ``DiskType`` class contains the supported disk provisioning types for
    VMs.
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
    DEFAULT = None
    """
    Denotes no specific type for disk provisioning. Disks are provisioned as
    defaulted by vCenter.

    """
    THIN = None
    """
    Disks are provisioned with only used space allocated.

    """
    THICK = None
    """
    Disks are provisioned with full size and the space is zeroed on demand.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`DiskType` instance.
        """
        Enum.__init__(string)

DiskType._set_values({
    'DEFAULT': DiskType('DEFAULT'),
    'THIN': DiskType('THIN'),
    'THICK': DiskType('THICK'),
})
DiskType._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.disk_type',
    DiskType))



class StoragePolicy(Enum):
    """
    The ``StoragePolicy`` class defines the different storage policies that can
    be used for VMs.
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
    DEFAULT = None
    """
    The default storage policy defined by the Storage Policy Based Management.

    """
    PROFILE = None
    """
    Profile storage policy.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`StoragePolicy` instance.
        """
        Enum.__init__(string)

StoragePolicy._set_values({
    'DEFAULT': StoragePolicy('DEFAULT'),
    'PROFILE': StoragePolicy('PROFILE'),
})
StoragePolicy._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.storage_policy',
    StoragePolicy))



class VmCloneConfig(Enum):
    """
    The ``VmCloneConfig`` class defines the different configurations for VM
    cloning.
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
    ALL_CLONES = None
    """
    The system creates a snapshot of the first deployed VM and after that uses
    one of the available VM clone methods to deploy others.

    """
    FULL_CLONES_ONLY = None
    """
    The system creates a snapshot of the first deployed VM and after that uses
    full VM clone method to deploy others.

    """
    NO_CLONES = None
    """
    The system does not use VM clone methods to deploy VMs.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`VmCloneConfig` instance.
        """
        Enum.__init__(string)

VmCloneConfig._set_values({
    'ALL_CLONES': VmCloneConfig('ALL_CLONES'),
    'FULL_CLONES_ONLY': VmCloneConfig('FULL_CLONES_ONLY'),
    'NO_CLONES': VmCloneConfig('NO_CLONES'),
})
VmCloneConfig._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.vm_clone_config',
    VmCloneConfig))



class DeploymentType(Enum):
    """
    The ``DeploymentType`` class defines the different solution deployment
    types.
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
    EVERY_HOST_PINNED = None
    """
    The solution requires exactly one VM deployed to any host in the cluster.
    Every solution VM is pinned (has affinity) to the host and cannot be
    migrated or restarted on another host inside the cluster.

    """
    CLUSTER_VM_SET = None
    """
    The solution requires a set of VMs to be deployed inside the cluster.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`DeploymentType` instance.
        """
        Enum.__init__(string)

DeploymentType._set_values({
    'EVERY_HOST_PINNED': DeploymentType('EVERY_HOST_PINNED'),
    'CLUSTER_VM_SET': DeploymentType('CLUSTER_VM_SET'),
})
DeploymentType._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.deployment_type',
    DeploymentType))



class VmPlacementPolicy(Enum):
    """
    The ``VmPlacementPolicy`` class defines the DRS placement policies applied
    on the VMs.
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
    VM_VM_ANTI_AFFINITY = None
    """
    VMs are anti-affined to each other.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`VmPlacementPolicy` instance.
        """
        Enum.__init__(string)

VmPlacementPolicy._set_values({
    'VM_VM_ANTI_AFFINITY': VmPlacementPolicy('VM_VM_ANTI_AFFINITY'),
})
VmPlacementPolicy._set_binding_type(type.EnumType(
    'com.vmware.esx.settings.clusters.vms.vm_placement_policy',
    VmPlacementPolicy))




class LifecycleHookConfig(VapiStruct):
    """
    The ``LifecycleHookConfig`` class contains attributes that describe a VM
    lifecycle hook configuration. See :class:`LifecycleHooks`.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 timeout=None,
                ):
        """
        :type  timeout: :class:`long` or ``None``
        :param timeout: The maximum time in seconds for vLCM to wait for a hook to be
            processed by the solution. An issue is raised if the time elapsed
            and the hook is still not processed. See
            :class:`Solutions.IssueInfo`. The issue is attached to the
            :class:`Solutions.DeploymentInfo` structure that holds the VM for
            which the hook was activated.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None, defaults to 10 hours.
        """
        self.timeout = timeout
        VapiStruct.__init__(self)


LifecycleHookConfig._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.lifecycle_hook_config', {
        'timeout': type.OptionalType(type.IntegerType()),
    },
    LifecycleHookConfig,
    False,
    None))



class LifecycleHookInfo(VapiStruct):
    """
    The ``LifecycleHookInfo`` class contains attributes that describe a VM
    lifecycle hook that is activated for a given VM.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm=None,
                 lifecycle_state=None,
                 configuration=None,
                 hook_activated=None,
                ):
        """
        :type  vm: :class:`str`
        :param vm: Identifier of the VM for which the hook is activated.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``VirtualMachine``. When methods return a value of this class as a
            return value, the attribute will be an identifier for the resource
            type: ``VirtualMachine``.
        :type  lifecycle_state: :class:`LifecycleState`
        :param lifecycle_state: VM lifecycle state of the VM specified by ``vm``
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  configuration: :class:`LifecycleHookConfig`
        :param configuration: Configuration of the hook.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  hook_activated: :class:`datetime.datetime`
        :param hook_activated: The vLCM system time when the hook is activated.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.vm = vm
        self.lifecycle_state = lifecycle_state
        self.configuration = configuration
        self.hook_activated = hook_activated
        VapiStruct.__init__(self)


LifecycleHookInfo._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.lifecycle_hook_info', {
        'vm': type.IdType(resource_types='VirtualMachine'),
        'lifecycle_state': type.ReferenceType(__name__, 'LifecycleState'),
        'configuration': type.ReferenceType(__name__, 'LifecycleHookConfig'),
        'hook_activated': type.DateTimeType(),
    },
    LifecycleHookInfo,
    False,
    None))



class OvfResource(VapiStruct):
    """
    The ``OvfResource`` class contains attributes that describe the location of
    an OVF package and a configuration for its download.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'location_type',
            {
                'REMOTE_FILE' : [('url', True), ('ssl_certificate_validation', True)],
                'LOCAL_FILE' : [('url', True)],
            }
        ),
        UnionValidator(
            'ssl_certificate_validation',
            {
                'ENABLED' : [('certificate', False)],
                'DISABLED' : [],
            }
        ),
    ]



    def __init__(self,
                 location_type=None,
                 url=None,
                 ssl_certificate_validation=None,
                 certificate=None,
                ):
        """
        :type  location_type: :class:`OvfResource.LocationType`
        :param location_type: Location type of OVF package.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  url: :class:`str`
        :param url: URL to the file server or the local VC file system where the OVF
            package can be downloaded. The supported URI schemes are http,
            https, and file.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``locationType`` is one of
            :attr:`OvfResource.LocationType.REMOTE_FILE` or
            :attr:`OvfResource.LocationType.LOCAL_FILE`.
        :type  ssl_certificate_validation: :class:`OvfResource.SslCertificateValidation`
        :param ssl_certificate_validation: Configuration for SSL Certificate validation of the URL specified
            by the ``url``.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``locationType`` is
            :attr:`OvfResource.LocationType.REMOTE_FILE`.
        :type  certificate: :class:`str` or ``None``
        :param certificate: The ssl certificate that is to be trusted by vLCM when downloading
            the OVF package from a file server.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the system validates the file server certificate against
            the system trusted CAs.
        """
        self.location_type = location_type
        self.url = url
        self.ssl_certificate_validation = ssl_certificate_validation
        self.certificate = certificate
        VapiStruct.__init__(self)


    class LocationType(Enum):
        """
        The ``OvfResource.LocationType`` class defines the supported locations of
        OVF packages.
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
        REMOTE_FILE = None
        """
        The OVF package is hosted on a file server.

        """
        LOCAL_FILE = None
        """
        The OVF package is located on the local VC file system.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`LocationType` instance.
            """
            Enum.__init__(string)

    LocationType._set_values({
        'REMOTE_FILE': LocationType('REMOTE_FILE'),
        'LOCAL_FILE': LocationType('LOCAL_FILE'),
    })
    LocationType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.vms.ovf_resource.location_type',
        LocationType))

    class SslCertificateValidation(Enum):
        """
        The ``OvfResource.SslCertificateValidation`` class defines the supported
        configurations for SSL Certificate validation.
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
        ENABLED = None
        """
        The certificate must be fully validated by the system.

        """
        DISABLED = None
        """
        The certificate validation is disabled. The system trusts any certificate.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SslCertificateValidation` instance.
            """
            Enum.__init__(string)

    SslCertificateValidation._set_values({
        'ENABLED': SslCertificateValidation('ENABLED'),
        'DISABLED': SslCertificateValidation('DISABLED'),
    })
    SslCertificateValidation._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.vms.ovf_resource.ssl_certificate_validation',
        SslCertificateValidation))

OvfResource._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.ovf_resource', {
        'location_type': type.ReferenceType(__name__, 'OvfResource.LocationType'),
        'url': type.OptionalType(type.URIType()),
        'ssl_certificate_validation': type.OptionalType(type.ReferenceType(__name__, 'OvfResource.SslCertificateValidation')),
        'certificate': type.OptionalType(type.StringType()),
    },
    OvfResource,
    False,
    None))



class HostSolutionSpec(VapiStruct):
    """
    The ``HostSolutionSpec`` class contains attributes that describe solution
    configuration only applicable for solutions with deployment type
    :attr:`DeploymentType.EVERY_HOST_PINNED`
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 prefer_host_configuration=None,
                 vm_networks=None,
                 vm_datastores=None,
                ):
        """
        :type  prefer_host_configuration: :class:`bool` or ``None``
        :param prefer_host_configuration: Describes whether the VM datastore and network configured through
            vim.host.EsxAgentHostManager take precedence over the networks and
            datastores specified by the vmNetworks and vmDatastores attributes
            when configuring the VMs. 
            
            NOTE: This option is reserved only for NSX and future plans are to
            be deprecated.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, defaults to ``false``.
        :type  vm_networks: :class:`list` of :class:`str` or ``None``
        :param vm_networks: Networks to be configured on the VMs. The first available network
            on the host is used. 
            
            If the ``preferHostConfiguration`` is set to ``true``, the default
            network configured through vim.host.EsxAgentHostManager will take
            precedence over the specified by the ``vmNetworks``. 
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``Network``. When methods return a value of this class as a return
            value, the attribute will contain identifiers for the resource
            type: ``Network``.
            If None the network configured through vim.host.EsxAgentHostManager
            is used.
        :type  vm_datastores: :class:`list` of :class:`str` or ``None``
        :param vm_datastores: Datastores to be configured as a storage of the VMs. The first
            available datastore on the host is used. 
            
            If the ``preferHostConfiguration`` is set to ``true``, the default
            datastore configured through vim.host.EsxAgentHostManager will take
            precedence over the ones specified by ``vmDatastores``. 
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``Datastore``. When methods return a value of this class as a
            return value, the attribute will contain identifiers for the
            resource type: ``Datastore``.
            If None the datastore configured through
            vim.host.EsxAgentHostManager is used.
        """
        self.prefer_host_configuration = prefer_host_configuration
        self.vm_networks = vm_networks
        self.vm_datastores = vm_datastores
        VapiStruct.__init__(self)


HostSolutionSpec._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.host_solution_spec', {
        'prefer_host_configuration': type.OptionalType(type.BooleanType()),
        'vm_networks': type.OptionalType(type.ListType(type.IdType())),
        'vm_datastores': type.OptionalType(type.ListType(type.IdType())),
    },
    HostSolutionSpec,
    False,
    None))



class ClusterSolutionSpec(VapiStruct):
    """
    The ``ClusterSolutionSpec`` class contains attributes that describe
    solution configuration only applicable for solutions with deployment type
    :attr:`DeploymentType.CLUSTER_VM_SET`.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_count=None,
                 vm_placement_policies=None,
                 vm_networks=None,
                 vm_datastores=None,
                 devices=None,
                ):
        """
        :type  vm_count: :class:`long`
        :param vm_count: The number of instances of the specified VM to be deployed across
            the cluster.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  vm_placement_policies: :class:`set` of :class:`VmPlacementPolicy` or ``None``
        :param vm_placement_policies: VM placement policies to be configured on the VMs.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None no VM placement policies are configured.
        :type  vm_networks: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
        :param vm_networks: Networks to be configured on the VMs. The map keys represent the
            logical network names defined in the OVF descriptor while the map
            values represent the VM network identifiers.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the value
            in the attribute :class:`dict` must be an identifier for the
            resource type: ``Network``. When methods return a value of this
            class as a return value, the value in the attribute :class:`dict`
            will be an identifier for the resource type: ``Network``.
            If None no VM networks are configured.
        :type  vm_datastores: :class:`list` of :class:`str` or ``None``
        :param vm_datastores: Datastores to be configured as a storage of the VMs. The first
            datastore from the list available in the cluster is used.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``Datastore``. When methods return a value of this class as a
            return value, the attribute will contain identifiers for the
            resource type: ``Datastore``.
            If None the system automatically selects the datastore. The
            selection takes into account the other properties of the desired
            state specification (the provided VM storage policies and VM
            devices) and the runtime state of the datastores in the cluster. It
            is required DRS to be enabled on the cluster.
        :type  devices: :class:`vmware.vapi.struct.VapiStruct` or ``None``
        :param devices: Devices of the VMs not defined in the OVF descriptor. 
            
            If {#member vmDatastores} is not set, the devices of the VMs not
            defined in the OVF descriptor should be provided to {#member
            devices} and not as part of a VM lifecycle hook (VM
            reconfiguration). Otherwise, the compatibility of the devices with
            the selected host and datastore where the VM is deployed needs to
            be ensured by the client. 
            
            1. For VM initial placement the devices are added to the VM
            configuration. 2. For the reconfiguration it is checked what
            devices need to be added, removed, and edited on the existing VMs.
            NOTE: No VM relocation is executed before the VM reconfiguration. 
            
            The supported property of vim.vm.ConfigSpec is
            vim.vm.ConfigSpec.deviceChange. The supported
            vim.vm.device.VirtualDeviceSpec.operation is Operation#add. For
            vim.vm.device.VirtualEthernetCard the unique identifier is
            vim.vm.device.VirtualDevice#unitNumber. {#member vmNetworks} and
            {#member devices} are mutually exclusive. 
            This attribute was added in **vSphere API 9.0.0.0**.
            If None no additional devices will be added to the VMs.
        """
        self.vm_count = vm_count
        self.vm_placement_policies = vm_placement_policies
        self.vm_networks = vm_networks
        self.vm_datastores = vm_datastores
        self.devices = devices
        VapiStruct.__init__(self)


ClusterSolutionSpec._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.cluster_solution_spec', {
        'vm_count': type.IntegerType(),
        'vm_placement_policies': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'VmPlacementPolicy'))),
        'vm_networks': type.OptionalType(type.MapType(type.StringType(), type.IdType())),
        'vm_datastores': type.OptionalType(type.ListType(type.IdType())),
        'devices': type.OptionalType(type.DynamicStructType('vmware.vapi.dynamic_struct', {}, VapiStruct)),
    },
    ClusterSolutionSpec,
    False,
    None))



class VmNameTemplate(VapiStruct):
    """
    The ``VmNameTemplate`` class contains attributes that describe a template
    for VM names
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 prefix=None,
                 suffix=None,
                ):
        """
        :type  prefix: :class:`str`
        :param prefix: VM name prefix.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  suffix: :class:`VmNameTemplate.SuffixFormat`
        :param suffix: VM name suffix format.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.prefix = prefix
        self.suffix = suffix
        VapiStruct.__init__(self)


    class SuffixFormat(Enum):
        """
        The ``VmNameTemplate.SuffixFormat`` class defines the types of VM name
        suffixes.
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
        UUID = None
        """
        UUID suffix format.

        """
        COUNTER = None
        """
        Suffix in the format "(counter)" where "counter" is monotonically growing
        integer.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SuffixFormat` instance.
            """
            Enum.__init__(string)

    SuffixFormat._set_values({
        'UUID': SuffixFormat('UUID'),
        'COUNTER': SuffixFormat('COUNTER'),
    })
    SuffixFormat._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.vms.vm_name_template.suffix_format',
        SuffixFormat))

VmNameTemplate._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.vm_name_template', {
        'prefix': type.StringType(),
        'suffix': type.ReferenceType(__name__, 'VmNameTemplate.SuffixFormat'),
    },
    VmNameTemplate,
    False,
    None))



class VmResourceSpec(VapiStruct):
    """
    The ``VmResourceSpec`` class contains attributes that describe the VM
    resource configurations.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ovf_deployment_option=None,
                ):
        """
        :type  ovf_deployment_option: :class:`str` or ``None``
        :param ovf_deployment_option: The VM deployment option that corresponds to the Configuration
            element of the DeploymentOptionSection in the OVF descriptor (e.g.
            "small", "medium", "large").
            This attribute was added in **vSphere API 9.0.0.0**.
            if None the default deployment options as specified in the OVF
            descriptor is used.
        """
        self.ovf_deployment_option = ovf_deployment_option
        VapiStruct.__init__(self)


VmResourceSpec._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.vm_resource_spec', {
        'ovf_deployment_option': type.OptionalType(type.StringType()),
    },
    VmResourceSpec,
    False,
    None))



class SolutionSpec(VapiStruct):
    """
    The ``SolutionSpec`` class contains attributes that describe the desired
    specification of a System VM solution that is to be installed or updated in
    a given cluster.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'deployment_type',
            {
                'EVERY_HOST_PINNED' : [('host_solution_spec', True)],
                'CLUSTER_VM_SET' : [('cluster_solution_spec', True)],
            }
        ),
        UnionValidator(
            'vm_storage_policy',
            {
                'PROFILE' : [('vm_storage_profiles', True)],
                'DEFAULT' : [],
            }
        ),
    ]



    def __init__(self,
                 deployment_type=None,
                 display_name=None,
                 display_version=None,
                 vm_name_template=None,
                 host_solution_spec=None,
                 cluster_solution_spec=None,
                 hook_configurations=None,
                 ovf_resource=None,
                 ovf_descriptor_properties=None,
                 vm_clone_config=None,
                 vm_storage_policy=None,
                 vm_storage_profiles=None,
                 vm_disk_type=None,
                 vm_resource_pool=None,
                 vm_folder=None,
                 vm_resource_spec=None,
                ):
        """
        :type  deployment_type: :class:`DeploymentType`
        :param deployment_type: Deployment type of the solution.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  display_name: :class:`str`
        :param display_name: Display name of the solution.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  display_version: :class:`str`
        :param display_version: Display version of the solution.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  vm_name_template: :class:`VmNameTemplate`
        :param vm_name_template: VM name template.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  host_solution_spec: :class:`HostSolutionSpec`
        :param host_solution_spec: Configuration that is only applicable for solutions with deployment
            type :attr:`DeploymentType.EVERY_HOST_PINNED`
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``deploymentType`` is :attr:`DeploymentType.EVERY_HOST_PINNED`.
        :type  cluster_solution_spec: :class:`ClusterSolutionSpec`
        :param cluster_solution_spec: Configuration that is only applicable for solutions with deployment
            type :attr:`DeploymentType.CLUSTER_VM_SET`
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``deploymentType`` is :attr:`DeploymentType.CLUSTER_VM_SET`.
        :type  hook_configurations: (:class:`dict` of :class:`LifecycleState` and :class:`LifecycleHookConfig`) or ``None``
        :param hook_configurations: VM lifecycle hooks configurations. See :class:`LifecycleHooks`. The
            map keys represent :class:`LifecycleState`s while the map values
            represent their configurations.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None or empty, no hooks are configured.
        :type  ovf_resource: :class:`OvfResource`
        :param ovf_resource: Information about the OVF resource that to be used for the VM
            deployments.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  ovf_descriptor_properties: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
        :param ovf_descriptor_properties: OVF properties that to be assigned to the VMs' OVF properties when
            powered on. The keys of the map must not include any white-space
            characters. The map keys represent the names of properties while
            the map values represent the values of those properties.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None or empty, no properties are assigned.
        :type  vm_clone_config: :class:`VmCloneConfig` or ``None``
        :param vm_clone_config: VM cloning configuration.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None, defaults to :attr:`VmCloneConfig.ALL_CLONES`.
        :type  vm_storage_policy: :class:`StoragePolicy`
        :param vm_storage_policy: Storage policies to be configured on the VMs.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  vm_storage_profiles: :class:`list` of :class:`str`
        :param vm_storage_profiles: Storage policy profiles to be configured on the VMs. The profiles
            are passed to vim.vm.ConfigSpec#vmProfile without any
            interpretation.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.spbm.StorageProfile``. When methods return a value of
            this class as a return value, the attribute will contain
            identifiers for the resource type:
            ``com.vmware.spbm.StorageProfile``.
            This attribute is optional and it is only relevant when the value
            of ``vmStoragePolicy`` is :attr:`StoragePolicy.PROFILE`.
        :type  vm_disk_type: :class:`DiskType` or ``None``
        :param vm_disk_type: Disk provisioning type of the VMs.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None, defaults to :attr:`DiskType.DEFAULT`.
        :type  vm_resource_pool: :class:`str` or ``None``
        :param vm_resource_pool: Identifier of the resource pool where the VMs to be deployed.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``ResourcePool``. When methods return a value of this class as a
            return value, the attribute will be an identifier for the resource
            type: ``ResourcePool``.
            if None the VMs for each compute resource will be deployed under
            top level nested resource pool created for the solutions. If unable
            to create a nested resource pool, the root resource pool of the
            compute resource will be used.
        :type  vm_folder: :class:`str` or ``None``
        :param vm_folder: Identifier of the folder inventory object where the VMs to be
            deployed.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type: ``Folder``.
            When methods return a value of this class as a return value, the
            attribute will be an identifier for the resource type: ``Folder``.
            if None the VMs are deployed inside the top level folder created in
            each datacenter for solutions.
        :type  vm_resource_spec: :class:`VmResourceSpec` or ``None``
        :param vm_resource_spec: VMs resource configuration.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None the default resource configuration specified in the OVF
            descriptor is used.
        """
        self.deployment_type = deployment_type
        self.display_name = display_name
        self.display_version = display_version
        self.vm_name_template = vm_name_template
        self.host_solution_spec = host_solution_spec
        self.cluster_solution_spec = cluster_solution_spec
        self.hook_configurations = hook_configurations
        self.ovf_resource = ovf_resource
        self.ovf_descriptor_properties = ovf_descriptor_properties
        self.vm_clone_config = vm_clone_config
        self.vm_storage_policy = vm_storage_policy
        self.vm_storage_profiles = vm_storage_profiles
        self.vm_disk_type = vm_disk_type
        self.vm_resource_pool = vm_resource_pool
        self.vm_folder = vm_folder
        self.vm_resource_spec = vm_resource_spec
        VapiStruct.__init__(self)


SolutionSpec._set_binding_type(type.StructType(
    'com.vmware.esx.settings.clusters.vms.solution_spec', {
        'deployment_type': type.ReferenceType(__name__, 'DeploymentType'),
        'display_name': type.StringType(),
        'display_version': type.StringType(),
        'vm_name_template': type.ReferenceType(__name__, 'VmNameTemplate'),
        'host_solution_spec': type.OptionalType(type.ReferenceType(__name__, 'HostSolutionSpec')),
        'cluster_solution_spec': type.OptionalType(type.ReferenceType(__name__, 'ClusterSolutionSpec')),
        'hook_configurations': type.OptionalType(type.MapType(type.ReferenceType(__name__, 'LifecycleState'), type.ReferenceType(__name__, 'LifecycleHookConfig'))),
        'ovf_resource': type.ReferenceType(__name__, 'OvfResource'),
        'ovf_descriptor_properties': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
        'vm_clone_config': type.OptionalType(type.ReferenceType(__name__, 'VmCloneConfig')),
        'vm_storage_policy': type.ReferenceType(__name__, 'StoragePolicy'),
        'vm_storage_profiles': type.OptionalType(type.ListType(type.IdType())),
        'vm_disk_type': type.OptionalType(type.ReferenceType(__name__, 'DiskType')),
        'vm_resource_pool': type.OptionalType(type.IdType()),
        'vm_folder': type.OptionalType(type.IdType()),
        'vm_resource_spec': type.OptionalType(type.ReferenceType(__name__, 'VmResourceSpec')),
    },
    SolutionSpec,
    False,
    None))



class LifecycleHooks(VapiInterface):
    """
    The ``LifecycleHooks`` class provides methods to read and process VM
    lifecycle hooks in an ESXi cluster. See :class:`LifecycleHookInfo` and
    :class:`LifecycleHookConfig`. 
    
    VM lifecycle hook workflow: 
    
    #. A System VM solution configures hooks for the different lifecycle states
       of its VMs as part of a desired specification.
    #. The system starts a deployment of a VM for that solution.
    #. The VM reaches a lifecycle state for which a hook is configured in the
       desired specification of the solution.
    #. The system activates a hook that matches the lifecycle state of the VM
       and starts waiting for the solution to process this hook. Until the hook is
       not processed the system does not work actively to reach the desired state
       of the VM.
    #. The solution makes the necessary configurations related to the VM.
    #. The solution marks the hook as proccessed.
    #. The system continues working actively to reach the desired specification
       of the deployment
    
    
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.vms.lifecycle_hooks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LifecycleHooksStub)
        self._VAPI_OPERATION_IDS = {}

    class ProcessedHookSpec(VapiStruct):
        """
        The ``LifecycleHooks.ProcessedHookSpec`` class contains attributes that
        describe a specification for marking a hook as processed.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm=None,
                     lifecycle_state=None,
                     processed_successfully=None,
                    ):
            """
            :type  vm: :class:`str`
            :param vm: Identifier of the VM whose hook needs to be marked as processed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  lifecycle_state: :class:`LifecycleState`
            :param lifecycle_state: Expected VM lifecycle state of the VM specified by the ``vm`` for
                which the hook is activated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  processed_successfully: :class:`bool`
            :param processed_successfully: Result of the client hook processing. True if processed
                successfully, false otherwise.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vm = vm
            self.lifecycle_state = lifecycle_state
            self.processed_successfully = processed_successfully
            VapiStruct.__init__(self)


    ProcessedHookSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.lifecycle_hooks.processed_hook_spec', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'lifecycle_state': type.ReferenceType(__name__, 'LifecycleState'),
            'processed_successfully': type.BooleanType(),
        },
        ProcessedHookSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``LifecycleHooks.ListResult`` class contains attributes that describe
        all activated hooks that the system is waiting to be processed by a given
        solution.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hooks=None,
                    ):
            """
            :type  hooks: :class:`list` of :class:`LifecycleHookInfo`
            :param hooks: Activated Hooks that the system is waiting for solutions to
                process.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.hooks = hooks
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.lifecycle_hooks.list_result', {
            'hooks': type.ListType(type.ReferenceType(__name__, 'LifecycleHookInfo')),
        },
        ListResult,
        False,
        None))



    def mark_as_processed(self,
                          cluster,
                          spec,
                          ):
        """
        Marks an activated hook as proccessed.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`LifecycleHooks.ProcessedHookSpec`
        :param spec: Specification for hook processing.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the ``spec`` specifies an invalid argument. For example thrown
            if a VM that is specified within the ``spec`` is not present in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If 1) the lifecycleState attribute of the ``spec`` does not match
            the current lifecycle state of the VM or 2) System VMs are disabled
            on the cluster via internal ESX Agent Manager (EAM) API
            (eam.EsxtAgentManager#disable).
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Write``.
        """
        return self._invoke('mark_as_processed',
                            {
                            'cluster': cluster,
                            'spec': spec,
                            })

    def list(self,
             cluster,
             solution,
             ):
        """
        All activated hooks that the system is waiting to be processed for a
        given solution.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  solution: :class:`str`
        :param solution: Identifier of the solution.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.vms.SystemVmSolution``.
        :rtype: :class:`LifecycleHooks.ListResult`
        :return: :class:`LifecycleHooks.ListResult` that describes the hooks that
            the system is waiting to be processed by a given solution.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system or
            no solution associated with ``solution`` in the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Read``.
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'solution': solution,
                            })
class Solutions(VapiInterface):
    """
    The ``Solutions`` class provides methods to manage the desired System VM
    solution specification of an ESXi cluster.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.vms.SystemVmSolution"
    """
    Resource type for System VM solution resource.

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.vms.solutions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SolutionsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'apply_task': 'apply$task'})
        self._VAPI_OPERATION_IDS.update({'check_compliance_task': 'check_compliance$task'})

    class ComplianceStatus(Enum):
        """
        The ``Solutions.ComplianceStatus`` class describes the possible compliance
        status.
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
        COMPLIANT = None
        """
        The status is compliant with the desired solution specification.

        """
        NON_COMPLIANT = None
        """
        The status is **non**-compliant with the desired solution specification.

        """
        INCOMPATIBLE = None
        """
        Target state is incompatible with the system.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ComplianceStatus` instance.
            """
            Enum.__init__(string)

    ComplianceStatus._set_values({
        'COMPLIANT': ComplianceStatus('COMPLIANT'),
        'NON_COMPLIANT': ComplianceStatus('NON_COMPLIANT'),
        'INCOMPATIBLE': ComplianceStatus('INCOMPATIBLE'),
    })
    ComplianceStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.vms.solutions.compliance_status',
        ComplianceStatus))


    class ValidateResult(VapiStruct):
        """
        The ``Solutions.ValidateResult`` class contains attributes that describe
        the validation result during the execution of a :func:`Solutions.set` or
        :func:`Solutions.delete` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                    ):
            """
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications associated with the validation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.notifications = notifications
            VapiStruct.__init__(self)


    ValidateResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.validate_result', {
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ValidateResult,
        False,
        None))


    class HostSolutionInfo(VapiStruct):
        """
        The ``Solutions.HostSolutionInfo`` class contains attributes that describe
        solution configuration only applicable for solutions with deployment type
        :attr:`DeploymentType.EVERY_HOST_PINNED`
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     prefer_host_configuration=None,
                     vm_networks=None,
                     vm_datastores=None,
                    ):
            """
            :type  prefer_host_configuration: :class:`bool`
            :param prefer_host_configuration: Describes whether the VM datastore and network configured through
                vim.host.EsxAgentHostManager take precedence over the networks and
                datastores specified by the vmNetworks and vmDatastores attributes
                when configuring the VMs. 
                
                NOTE: This option is reserved only for NSX and future plans are to
                be deprecated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_networks: :class:`list` of :class:`str`
            :param vm_networks: Networks to be configured on the VMs. The first available network
                on the host is used. 
                
                If the ``preferHostConfiguration`` is set to ``true``, the default
                network configured through vim.host.EsxAgentHostManager will take
                precedence over the specified by the ``vmNetworks``. 
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Network``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Network``.
            :type  vm_datastores: :class:`list` of :class:`str`
            :param vm_datastores: Datastores to be configured as a storage of the VMs. The first
                available datastore on the host is used. 
                
                If the ``preferHostConfiguration`` is set to ``true``, the default
                datastore configured through vim.host.EsxAgentHostManager will take
                precedence over the specified by ``vmDatastores``. 
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datastore``.
            """
            self.prefer_host_configuration = prefer_host_configuration
            self.vm_networks = vm_networks
            self.vm_datastores = vm_datastores
            VapiStruct.__init__(self)


    HostSolutionInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_solution_info', {
            'prefer_host_configuration': type.BooleanType(),
            'vm_networks': type.ListType(type.IdType()),
            'vm_datastores': type.ListType(type.IdType()),
        },
        HostSolutionInfo,
        False,
        None))


    class ClusterSolutionInfo(VapiStruct):
        """
        The ``Solutions.ClusterSolutionInfo`` class contains attributes that
        describe solution configuration only applicable for solutions with
        deployment type :attr:`DeploymentType.CLUSTER_VM_SET`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm_count=None,
                     vm_placement_policies=None,
                     vm_networks=None,
                     vm_datastores=None,
                     devices=None,
                    ):
            """
            :type  vm_count: :class:`long`
            :param vm_count: The number of instances of the specified VM to be deployed across
                the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_placement_policies: :class:`set` of :class:`VmPlacementPolicy`
            :param vm_placement_policies: VM placement policies to be configured on the VMs.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_networks: :class:`dict` of :class:`str` and :class:`str`
            :param vm_networks: Networks to be configured on the VMs. The map keys represent the
                logical network names defined in the OVF descriptor while the map
                values represent the VM network identifiers.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the value
                in the attribute :class:`dict` must be an identifier for the
                resource type: ``Network``. When methods return a value of this
                class as a return value, the value in the attribute :class:`dict`
                will be an identifier for the resource type: ``Network``.
            :type  vm_datastores: :class:`list` of :class:`str`
            :param vm_datastores: Datastores to be configured as a storage of the VMs. The first
                datastore from the list available in the cluster is used.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datastore``.
            :type  devices: :class:`vmware.vapi.struct.VapiStruct` or ``None``
            :param devices: Devices of the VMs not defined in the OVF descriptor.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None no additional devices will be added to the VMs.
            """
            self.vm_count = vm_count
            self.vm_placement_policies = vm_placement_policies
            self.vm_networks = vm_networks
            self.vm_datastores = vm_datastores
            self.devices = devices
            VapiStruct.__init__(self)


    ClusterSolutionInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solution_info', {
            'vm_count': type.IntegerType(),
            'vm_placement_policies': type.SetType(type.ReferenceType(__name__, 'VmPlacementPolicy')),
            'vm_networks': type.MapType(type.StringType(), type.IdType()),
            'vm_datastores': type.ListType(type.IdType()),
            'devices': type.OptionalType(type.DynamicStructType('vmware.vapi.dynamic_struct', {}, VapiStruct)),
        },
        ClusterSolutionInfo,
        False,
        None))


    class SolutionInfo(VapiStruct):
        """
        The ``Solutions.SolutionInfo`` class contains attributes that describe the
        desired specification of a System VM solution.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'deployment_type',
                {
                    'EVERY_HOST_PINNED' : [('host_solution_info', True)],
                    'CLUSTER_VM_SET' : [('cluster_solution_info', True)],
                }
            ),
            UnionValidator(
                'vm_storage_policy',
                {
                    'PROFILE' : [('vm_storage_profiles', True)],
                    'DEFAULT' : [],
                }
            ),
        ]



        def __init__(self,
                     deployment_type=None,
                     display_name=None,
                     display_version=None,
                     vm_name_template=None,
                     host_solution_info=None,
                     cluster_solution_info=None,
                     hook_configurations=None,
                     ovf_resource=None,
                     ovf_descriptor_properties=None,
                     vm_clone_config=None,
                     vm_storage_policy=None,
                     vm_storage_profiles=None,
                     vm_disk_type=None,
                     vm_resource_pool=None,
                     vm_folder=None,
                     vm_resource_spec=None,
                    ):
            """
            :type  deployment_type: :class:`DeploymentType`
            :param deployment_type: Deployment type of the solution.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  display_name: :class:`str`
            :param display_name: Display name of the solution.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  display_version: :class:`str`
            :param display_version: Display version of the solution.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_name_template: :class:`VmNameTemplate`
            :param vm_name_template: VM name template.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  host_solution_info: :class:`Solutions.HostSolutionInfo`
            :param host_solution_info: Information about a configuration that is only applicable to
                solutions with deployment type
                :attr:`DeploymentType.EVERY_HOST_PINNED`
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``deploymentType`` is :attr:`DeploymentType.EVERY_HOST_PINNED`.
            :type  cluster_solution_info: :class:`Solutions.ClusterSolutionInfo`
            :param cluster_solution_info: Information about a configuration that is only applicable to
                solutions with deployment type
                :attr:`DeploymentType.CLUSTER_VM_SET`
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``deploymentType`` is :attr:`DeploymentType.CLUSTER_VM_SET`.
            :type  hook_configurations: :class:`dict` of :class:`LifecycleState` and :class:`LifecycleHookConfig`
            :param hook_configurations: VM lifecycle hooks configurations. See :class:`LifecycleHooks`. The
                map keys represent :class:`LifecycleState`s while the map values
                represent their configurations.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  ovf_resource: :class:`OvfResource`
            :param ovf_resource: Information about the OVF resource that is used for the VM
                deployments.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  ovf_descriptor_properties: :class:`dict` of :class:`str` and :class:`str`
            :param ovf_descriptor_properties: OVF properties that are assigned to the VMs' OVF properties when
                powered on. The keys of the map must not include any white-space
                characters. The map keys represent the names of properties while
                the map values represent the values of those properties.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_clone_config: :class:`VmCloneConfig`
            :param vm_clone_config: VM cloning configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_storage_policy: :class:`StoragePolicy`
            :param vm_storage_policy: Storage policies that are configured on the VMs.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_storage_profiles: :class:`list` of :class:`str`
            :param vm_storage_profiles: Storage policy profiles that are configured on the VMs. The
                profiles are passed to vim.vm.ConfigSpec#vmProfile without any
                interpretation.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.spbm.StorageProfile``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.spbm.StorageProfile``.
                This attribute is optional and it is only relevant when the value
                of ``vmStoragePolicy`` is :attr:`StoragePolicy.PROFILE`.
            :type  vm_disk_type: :class:`DiskType`
            :param vm_disk_type: Disk provisioning type of the VMs.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm_resource_pool: :class:`str` or ``None``
            :param vm_resource_pool: Identifier of the resource pool where the VMs are deployed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                if None the VMs for each compute resource will be deployed under
                top level nested resource pool created for the solutions. If unable
                to create a nested resource pool, the root resource pool of the
                compute resource will be used.
            :type  vm_folder: :class:`str` or ``None``
            :param vm_folder: Identifier of the folder inventory object where VMs are deployed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                if None the VMs are deployed inside the top level folder created in
                each datacenter for solutions.
            :type  vm_resource_spec: :class:`VmResourceSpec` or ``None``
            :param vm_resource_spec: VMs resource configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the default resource configuration specified in the OVF
                descriptor is used.
            """
            self.deployment_type = deployment_type
            self.display_name = display_name
            self.display_version = display_version
            self.vm_name_template = vm_name_template
            self.host_solution_info = host_solution_info
            self.cluster_solution_info = cluster_solution_info
            self.hook_configurations = hook_configurations
            self.ovf_resource = ovf_resource
            self.ovf_descriptor_properties = ovf_descriptor_properties
            self.vm_clone_config = vm_clone_config
            self.vm_storage_policy = vm_storage_policy
            self.vm_storage_profiles = vm_storage_profiles
            self.vm_disk_type = vm_disk_type
            self.vm_resource_pool = vm_resource_pool
            self.vm_folder = vm_folder
            self.vm_resource_spec = vm_resource_spec
            VapiStruct.__init__(self)


    SolutionInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.solution_info', {
            'deployment_type': type.ReferenceType(__name__, 'DeploymentType'),
            'display_name': type.StringType(),
            'display_version': type.StringType(),
            'vm_name_template': type.ReferenceType(__name__, 'VmNameTemplate'),
            'host_solution_info': type.OptionalType(type.ReferenceType(__name__, 'Solutions.HostSolutionInfo')),
            'cluster_solution_info': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ClusterSolutionInfo')),
            'hook_configurations': type.MapType(type.ReferenceType(__name__, 'LifecycleState'), type.ReferenceType(__name__, 'LifecycleHookConfig')),
            'ovf_resource': type.ReferenceType(__name__, 'OvfResource'),
            'ovf_descriptor_properties': type.MapType(type.StringType(), type.StringType()),
            'vm_clone_config': type.ReferenceType(__name__, 'VmCloneConfig'),
            'vm_storage_policy': type.ReferenceType(__name__, 'StoragePolicy'),
            'vm_storage_profiles': type.OptionalType(type.ListType(type.IdType())),
            'vm_disk_type': type.ReferenceType(__name__, 'DiskType'),
            'vm_resource_pool': type.OptionalType(type.IdType()),
            'vm_folder': type.OptionalType(type.IdType()),
            'vm_resource_spec': type.OptionalType(type.ReferenceType(__name__, 'VmResourceSpec')),
        },
        SolutionInfo,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Solutions.ListResult`` class contains attributes that describe the
        desired specification of the solutions in a given cluster specified by the
        :class:`Solutions.FilterSpec` of the corresponding :func:`Solutions.list`
        method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     solutions=None,
                    ):
            """
            :type  solutions: :class:`dict` of :class:`str` and :class:`Solutions.SolutionInfo`
            :param solutions: Map of solution identifiers to their desired specification.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``.
            """
            self.solutions = solutions
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.list_result', {
            'solutions': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.SolutionInfo')),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Solutions.FilterSpec`` class contains attributes that are used to
        filter the desired specification that to be returned. See
        :func:`Solutions.list`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     solutions=None,
                    ):
            """
            :type  solutions: :class:`set` of :class:`str` or ``None``
            :param solutions: Solutions to return desired specification for.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``.
                if None or empty the desired specification of all solutions in the
                cluster to be returned.
            """
            self.solutions = solutions
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.filter_spec', {
            'solutions': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class HostSolutionsApplyFilterSpec(VapiStruct):
        """
        The ``Solutions.HostSolutionsApplyFilterSpec`` class contains attributes
        that describe a filter that to be used for applying the desired
        specification of solutions with deployment type
        :attr:`DeploymentType.EVERY_HOST_PINNED` to a given cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     solutions=None,
                     hosts=None,
                    ):
            """
            :type  solutions: :class:`set` of :class:`str` or ``None``
            :param solutions: Specific solutions within the cluster to be considered during the
                execution of the apply method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``.
                if None or empty, all solutions are applied.
            :type  hosts: :class:`set` of :class:`str` or ``None``
            :param hosts: Hosts on which solutions that are specified by this structure need
                to be applied.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                if None or empty, the solutions are applied on all of the hosts in
                the cluster.
            """
            self.solutions = solutions
            self.hosts = hosts
            VapiStruct.__init__(self)


    HostSolutionsApplyFilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_solutions_apply_filter_spec', {
            'solutions': type.OptionalType(type.SetType(type.IdType())),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
        },
        HostSolutionsApplyFilterSpec,
        False,
        None))


    class ClusterSolutionsApplyFilterSpec(VapiStruct):
        """
        The ``Solutions.ClusterSolutionsApplyFilterSpec`` class contains attributes
        that describe a filter that to be used for applying the desired
        specification of solutions with deployment type
        :attr:`DeploymentType.CLUSTER_VM_SET` to a given cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     solutions=None,
                     deployment_units=None,
                    ):
            """
            :type  solutions: :class:`set` of :class:`str` or ``None``
            :param solutions: Specific solutions within the cluster to be considered during the
                execution of the apply method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``.
                if None or empty, all solutions are applied.
            :type  deployment_units: :class:`list` of :class:`str` or ``None``
            :param deployment_units: Deployment units on which solutions that are specified by this
                structure need to be applied. 
                
                The deployment unit represents a single VM instance deployment. It
                is returned by the #checkCompliance method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``. When
                methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``.
                if None or empty, the configured solutions by ``solutions`` are
                applied on all of the deployment units in the cluster.
            """
            self.solutions = solutions
            self.deployment_units = deployment_units
            VapiStruct.__init__(self)


    ClusterSolutionsApplyFilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solutions_apply_filter_spec', {
            'solutions': type.OptionalType(type.SetType(type.IdType())),
            'deployment_units': type.OptionalType(type.ListType(type.IdType())),
        },
        ClusterSolutionsApplyFilterSpec,
        False,
        None))


    class ApplySpec(VapiStruct):
        """
        The ``Solutions.ApplySpec`` class contains attributes that describe a
        specification to be used for applying the desired solution specification to
        a given cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host_solutions=None,
                     cluster_solutions=None,
                    ):
            """
            :type  host_solutions: :class:`Solutions.HostSolutionsApplyFilterSpec` or ``None``
            :param host_solutions: Apply filter for solutions with deployment type
                :attr:`DeploymentType.EVERY_HOST_PINNED`.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None or empty and {#member clusterSolutions} is None or empty,
                all solutions are applied on the cluster.
            :type  cluster_solutions: :class:`Solutions.ClusterSolutionsApplyFilterSpec` or ``None``
            :param cluster_solutions: Apply filter for solutions with deployment type
                :attr:`DeploymentType.CLUSTER_VM_SET`.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None or empty and {#member hostSolutions} is None or empty, all
                solutions are applied on the cluster.
            """
            self.host_solutions = host_solutions
            self.cluster_solutions = cluster_solutions
            VapiStruct.__init__(self)


    ApplySpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.apply_spec', {
            'host_solutions': type.OptionalType(type.ReferenceType(__name__, 'Solutions.HostSolutionsApplyFilterSpec')),
            'cluster_solutions': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ClusterSolutionsApplyFilterSpec')),
        },
        ApplySpec,
        False,
        None))


    class ApplyStatus(VapiStruct):
        """
        The ``Solutions.ApplyStatus`` class contains attributes that describe the
        status of an :func:`Solutions.apply` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'SUCCESS' : [('end_time', True)],
                    'ERROR' : [('end_time', True)],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     start_time=None,
                     end_time=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus.Status` or ``None``
            :param status: The status of the method.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the operation is not completed.
            :type  start_time: :class:`datetime.datetime`
            :param start_time: The vLCM system time when the method started.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: The vLCM system time when the method completed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`Solutions.ApplyStatus.Status.SUCCESS` or
                :attr:`Solutions.ApplyStatus.Status.ERROR`.
            """
            self.status = status
            self.start_time = start_time
            self.end_time = end_time
            VapiStruct.__init__(self)


        class Status(Enum):
            """
            The ``Solutions.ApplyStatus.Status`` class contains the status codes of an
            :func:`Solutions.apply` method.
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
            SUCCESS = None
            """
            The apply method completed successfully.

            """
            ERROR = None
            """
            The apply method encountered an error.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Status` instance.
                """
                Enum.__init__(string)

        Status._set_values({
            'SUCCESS': Status('SUCCESS'),
            'ERROR': Status('ERROR'),
        })
        Status._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.clusters.vms.solutions.apply_status.status',
            Status))

    ApplyStatus._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.apply_status', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus.Status')),
            'start_time': type.DateTimeType(),
            'end_time': type.OptionalType(type.DateTimeType()),
        },
        ApplyStatus,
        False,
        None))


    class HostApplyStatus(VapiStruct):
        """
        The ``Solutions.HostApplyStatus`` class contains attributes that describe
        the apply status for a specific host.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     solution_statuses=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus` or ``None``
            :param status: Aggregated apply status of the solutions on the host.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the apply method is not completed for the specified host.
            :type  solution_statuses: :class:`dict` of :class:`str` and :class:`Solutions.ApplyStatus`
            :param solution_statuses: The apply status of the different solutions on the host.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``.
            """
            self.status = status
            self.solution_statuses = solution_statuses
            VapiStruct.__init__(self)


    HostApplyStatus._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_apply_status', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
            'solution_statuses': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
        },
        HostApplyStatus,
        False,
        None))


    class HostSolutionsApplyStatus(VapiStruct):
        """
        The ``Solutions.HostSolutionsApplyStatus`` class contains attributes that
        describe the apply status of solutions with deployment type
        :attr:`DeploymentType.EVERY_HOST_PINNED`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     host_statuses=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus` or ``None``
            :param status: Aggregated apply status of the solutions.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the apply method is not completed for solutions with
                deployment type :attr:`DeploymentType.EVERY_HOST_PINNED`.
            :type  host_statuses: :class:`dict` of :class:`str` and :class:`Solutions.HostApplyStatus`
            :param host_statuses: The apply status of the hosts that were part of the apply method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``HostSystem``. When methods return a value of this class as
                a return value, the key in the attribute :class:`dict` will be an
                identifier for the resource type: ``HostSystem``.
            """
            self.status = status
            self.host_statuses = host_statuses
            VapiStruct.__init__(self)


    HostSolutionsApplyStatus._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_solutions_apply_status', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
            'host_statuses': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.HostApplyStatus')),
        },
        HostSolutionsApplyStatus,
        False,
        None))


    class ClusterSolutionApplyStatus(VapiStruct):
        """
        The ``Solutions.ClusterSolutionApplyStatus`` class contains attributes that
        describe the apply status for a specific solution.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     deployment_unit_statuses=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus` or ``None``
            :param status: Aggregated apply status for the deployment units of the solution.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the apply method is not completed for the specified
                deployment unit.
            :type  deployment_unit_statuses: :class:`dict` of :class:`str` and :class:`Solutions.ApplyStatus`
            :param deployment_unit_statuses: The apply status for the different deployment units of the
                solution.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``.
            """
            self.status = status
            self.deployment_unit_statuses = deployment_unit_statuses
            VapiStruct.__init__(self)


    ClusterSolutionApplyStatus._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solution_apply_status', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
            'deployment_unit_statuses': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
        },
        ClusterSolutionApplyStatus,
        False,
        None))


    class ClusterSolutionsApplyStatus(VapiStruct):
        """
        The ``Solutions.ClusterSolutionsApplyStatus`` class contains attributes
        that describe the apply status of solutions with deployment type
        :attr:`DeploymentType.CLUSTER_VM_SET`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     solution_statuses=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus` or ``None``
            :param status: Aggregated apply status of the solutions.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the apply method is not completed for solutions with
                deployment type :attr:`DeploymentType.CLUSTER_VM_SET`.
            :type  solution_statuses: :class:`dict` of :class:`str` and :class:`Solutions.ClusterSolutionApplyStatus`
            :param solution_statuses: The apply status of the solutions that were part of the apply
                method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``.
            """
            self.status = status
            self.solution_statuses = solution_statuses
            VapiStruct.__init__(self)


    ClusterSolutionsApplyStatus._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solutions_apply_status', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
            'solution_statuses': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.ClusterSolutionApplyStatus')),
        },
        ClusterSolutionsApplyStatus,
        False,
        None))


    class ApplyResult(VapiStruct):
        """
        The ``Solutions.ApplyResult`` class contains attributes that describe the
        result of an :func:`Solutions.apply` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     host_solutions_status=None,
                     cluster_solutions_status=None,
                    ):
            """
            :type  status: :class:`Solutions.ApplyStatus` or ``None``
            :param status: Aggregated status of an apply method.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the apply method is in progress.
            :type  host_solutions_status: :class:`Solutions.HostSolutionsApplyStatus`
            :param host_solutions_status: The apply status of all solutions with deployment type
                :attr:`DeploymentType.EVERY_HOST_PINNED` that were part of the
                apply method.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cluster_solutions_status: :class:`Solutions.ClusterSolutionsApplyStatus`
            :param cluster_solutions_status: The apply status of all solutions with deployment type
                :attr:`DeploymentType.CLUSTER_VM_SET` that were part of the apply
                method.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.status = status
            self.host_solutions_status = host_solutions_status
            self.cluster_solutions_status = cluster_solutions_status
            VapiStruct.__init__(self)


    ApplyResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.apply_result', {
            'status': type.OptionalType(type.ReferenceType(__name__, 'Solutions.ApplyStatus')),
            'host_solutions_status': type.ReferenceType(__name__, 'Solutions.HostSolutionsApplyStatus'),
            'cluster_solutions_status': type.ReferenceType(__name__, 'Solutions.ClusterSolutionsApplyStatus'),
        },
        ApplyResult,
        False,
        None))


    class CheckComplianceFilterSpec(VapiStruct):
        """
        The ``Solutions.CheckComplianceFilterSpec`` class contains attributes that
        describe a filter for compliance check in a given cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     solutions=None,
                     hosts=None,
                     deployment_units=None,
                    ):
            """
            :type  solutions: :class:`set` of :class:`str` or ``None``
            :param solutions: Identifiers of the solutions that to be checked for compliance.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmSolution``.
                If None, the compliance is checked for all solutions in the
                cluster.
            :type  hosts: :class:`set` of :class:`str` or ``None``
            :param hosts: Identifiers of the hosts that to be checked for compliance of all
                solutions with deployment type
                :attr:`DeploymentType.EVERY_HOST_PINNED`.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                If None or empty and {#member deploymentUnits} is None or empty,
                the compliance is checked for all hosts in the cluster.
            :type  deployment_units: :class:`set` of :class:`str` or ``None``
            :param deployment_units: Identifiers of the deployment units that to be checked for
                compliance of all solutions with deployment type
                :attr:`DeploymentType.CLUSTER_VM_SET`. 
                
                The deployment unit represents a single VM instance deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``. When
                methods return a value of this class as a return value, the
                attribute will contain identifiers for the resource type:
                ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``.
                If None or empty and {#member hosts} is None or empty, the
                compliance is checked for all deployment units in the cluster.
            """
            self.solutions = solutions
            self.hosts = hosts
            self.deployment_units = deployment_units
            VapiStruct.__init__(self)


    CheckComplianceFilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.check_compliance_filter_spec', {
            'solutions': type.OptionalType(type.SetType(type.IdType())),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'deployment_units': type.OptionalType(type.SetType(type.IdType())),
        },
        CheckComplianceFilterSpec,
        False,
        None))


    class IssueInfo(VapiStruct):
        """
        The ``Solutions.IssueInfo`` class contains attributes that describe an
        issue that blocks the system to reach the desired specification of a given
        VM deployment.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     notifications=None,
                    ):
            """
            :type  type: :class:`Solutions.IssueInfo.IssueType`
            :param type: Type of the issue.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Provides additional information about the issue.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.type = type
            self.notifications = notifications
            VapiStruct.__init__(self)


        class IssueType(Enum):
            """
            The ``Solutions.IssueInfo.IssueType`` class defines the type of the issues.
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
            VM_POWERED_ON = None
            """
            The System VM is expected to be powered-off, but it is powered-on. To
            remediate the deployment, re-invoke :func:`Solutions.apply` to have vLCM
            power-off the System VM.

            """
            VM_POWERED_OFF = None
            """
            The System VM is expected to be powered-on, but it is powered-off. To
            remediate the deployment, re-invoke :func:`Solutions.apply` to have vLCM
            power-on the System VM.

            """
            VM_SUSPENDED = None
            """
            The System VM is expected to be powered-on, but it is suspended. To
            remediate the deployment, re-invoke :func:`Solutions.apply` to have vLCM
            power-on the System VM.

            """
            VM_INACCESSIBLE = None
            """
            The System VM is expected to be connected, but it is inaccessible. To
            remediate the deployment, remove the VM and re-invoke
            :func:`Solutions.apply` to have vLCM redeploy the System VM or do the
            necessary changes to ensure that the connection state of the VM is
            (vim.ConnectionState#connected). 
            
            NOTE: When the HA is enabled on the cluster this may be transient state and
            automatically remediated.

            """
            VM_CORRUPTED = None
            """
            The System VM is corrupted. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM delete the System VM and redeploys it.

            """
            VM_NOT_DEPLOYED = None
            """
            The System VM has not been deployed because of an unexpected error. To
            remediate the deployment, re-invoke :func:`Solutions.apply` to have vLCM
            redeploy the System VM.

            """
            VM_NOT_REMOVED = None
            """
            The System VM has not been deployed because of an unexpected error. To
            remediate the deployment, manually remove the VM or re-invoke
            :func:`Solutions.apply` to have vLCM retry the System VM removal.

            """
            VM_DATASTORE_MISSING = None
            """
            The System VM has not been deployed because the configured datastore for it
            is missing on the host. To unblock the System VM deployment, provide a
            proper datastore in the ``SolutionSpec``. To remediate the deployment,
            re-invoke :func:`Solutions.apply` to have vLCM to redeploy the System VM.

            """
            VM_NETWORK_MISSING = None
            """
            The System VM has not been deployed because the configured network for it
            is missing on the host. To unblock the System VM deployment provide a
            proper network in the ``SolutionSpec``. To remediate the deployment,
            re-invoke :func:`Solutions.apply` to have vLCM redeploy the System VM.

            """
            OVF_INVALID_FORMAT = None
            """
            The System VM has not been deployed because the provided ``OvfResource``
            part of ``SolutionSpec`` contains an invalid OVF. To unblock the System VM
            deployment provide a new ``OvfResource`` with valid OVF. To remediate the
            deployment, re-invoke :func:`Solutions.apply` to have vLCM redeploy the
            System VM.

            """
            OVF_INVALID_PROPERTY = None
            """
            The System VM is expected to be deployed or reconfigured, but an OVF
            property is either missing or has an invalid value. To unblock the System
            VM deployment or reconfiguration, provide a new ``ovfDescriptorProperties``
            in the ``SolutionSpec``. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM redeploy or reconfigure the System VM.

            """
            OVF_CANNOT_ACCESS = None
            """
            The System VM has not been deployed because vLCM is not able to access the
            OVF package. To unblock the System VM deployment, provide a proper
            accessible ``OvfResource``. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM redeploy the System VM.

            """
            OVF_CERTIFICATE_NOT_TRUSTED = None
            """
            The System VM has not been deployed because vLCM is not able to make
            successful SSL trust verification of the server certificate when
            establishing connection to the provided OVF package. To unblock the System
            VM deployment, provide a valid ``certificate`` or ensure the server
            certificate is signed by a CA trusted by the system. To remediate the
            deployment, re-invoke :func:`Solutions.apply` to have vLCM redeploy the
            System VM.

            """
            INSUFFICIENT_SPACE = None
            """
            The System VM has not been deployed because the configured System VM
            datastore does not have enough free space. To unblock the System VM
            deployment, make enough free space on the datastore or provide a new
            datastore in the ``SolutionSpec``. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM redeploy the System VM.

            """
            INSUFFICIENT_RESOURCES = None
            """
            The System VM has not been powered-on because the cluster does not have
            enough free CPU or memory resources. To unblock the System VM power-on,
            make enough CPU and memory resources available. To remediate the
            deployment, re-invoke :func:`Solutions.apply` to have vLCM power-on the
            System VM.

            """
            HOST_IN_MAINTENANCE_MODE = None
            """
            A System VM operation has not been initiated because the host is in
            maintenance mode. To unblock the System VM operation, move the host out of
            maintenance mode. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM retry the operation.

            """
            HOST_IN_PARTIAL_MAINTENANCE_MODE = None
            """
            A System VM operation has not been initiated because the host is in partial
            maintenance mode. To unblock the System VM operation, move the host out of
            partial maintenance mode. To remediate the deployment, re-invoke
            :func:`Solutions.apply` to have vLCM retry the operation.

            """
            HOST_IN_STAND_BY_MODE = None
            """
            A System VM operation has not been initiated because the host is in stand
            by mode. To unblock the System VM operation, move the host out of stand by
            mode. To remediate the deployment, re-invoke :func:`Solutions.apply` to
            have vLCM retry the operation.

            """
            HOST_NOT_REACHABLE = None
            """
            A System VM operation has not been initiated because the host is not
            reachable from vCenter Server. Any operation on the affected host is not
            possible. Typical reasons are disconnected or powered-off host. To unblock
            the System VM operation, reconnect and powered-on the host. To remediate
            the deployment, re-invoke :func:`Solutions.apply` to have vLCM retry the
            operation.

            """
            VM_INVALID_CONFIG = None
            """
            A System VM operation has not been initiated because the System VM has an
            invalid configuration. To unblock the System VM operation, inspect and
            correct the System VM configuration as necessary. To remediate the
            deployment, re-invoke :func:`Solutions.apply` to have vLCM retry the
            operation.

            """
            VMS_DISABLED = None
            """
            System VMs are disabled on the cluster via internal ESX Agent Manager (EAM)
            API (eam.EsxtAgentManager#disable). The present System VMs in the cluster
            are powered-off. No new System VMs are created. Modifications of the
            desired speification are not permitted. 
            
            This issue cannot be remediated via vLCM API. Remediation requires the
            System VMs to be enabled on the cluster via internal EAM API
            (eam.EsxAgentManager#enable). As result, the present System VMs are
            powered-on, Modifications of the desired specification are permitted. 
            
            Enabling and disabling the System VMs operations on the cluster is operated
            by vSAN Cluster Shutdown and Start-up workflows. Refer to vSAN Cluster
            Shutdown and Start-up documentation. 
            
            NOTE: In future versions of vLCM, Enabling and disabling the System VM
            operations will happen via internal vLCM APIs.

            """
            VM_LIFECYCLE_HOOK_TIMED_OUT = None
            """
            The System VM deployment is not completed because the System VM lifecycle
            hook has not been proccessed in the configured
            :attr:`LifecycleHookConfig.timeout`. To remediate the deployment, re-invoke
            :func:`Solutions.apply` and process again the VM lifecycle hook.

            """
            VM_LIFECYCLE_HOOK_FAILED = None
            """
            The System VM deployment is not completed because the System VM lifecycle
            hook has been failed by the client. To remediate the deployment, re-invoke
            :func:`Solutions.apply` and process again the VM lifecycle hook.

            """
            VM_PROTECTED = None
            """
            The System VM deployment is not completed because the System VM is
            protected from modifications (example: VM is in a process of vSphere HA
            recovery). To remediate the deployment, re-invoke :func:`Solutions.apply`
            to have vLCM retry the operation.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`IssueType` instance.
                """
                Enum.__init__(string)

        IssueType._set_values({
            'VM_POWERED_ON': IssueType('VM_POWERED_ON'),
            'VM_POWERED_OFF': IssueType('VM_POWERED_OFF'),
            'VM_SUSPENDED': IssueType('VM_SUSPENDED'),
            'VM_INACCESSIBLE': IssueType('VM_INACCESSIBLE'),
            'VM_CORRUPTED': IssueType('VM_CORRUPTED'),
            'VM_NOT_DEPLOYED': IssueType('VM_NOT_DEPLOYED'),
            'VM_NOT_REMOVED': IssueType('VM_NOT_REMOVED'),
            'VM_DATASTORE_MISSING': IssueType('VM_DATASTORE_MISSING'),
            'VM_NETWORK_MISSING': IssueType('VM_NETWORK_MISSING'),
            'OVF_INVALID_FORMAT': IssueType('OVF_INVALID_FORMAT'),
            'OVF_INVALID_PROPERTY': IssueType('OVF_INVALID_PROPERTY'),
            'OVF_CANNOT_ACCESS': IssueType('OVF_CANNOT_ACCESS'),
            'OVF_CERTIFICATE_NOT_TRUSTED': IssueType('OVF_CERTIFICATE_NOT_TRUSTED'),
            'INSUFFICIENT_SPACE': IssueType('INSUFFICIENT_SPACE'),
            'INSUFFICIENT_RESOURCES': IssueType('INSUFFICIENT_RESOURCES'),
            'HOST_IN_MAINTENANCE_MODE': IssueType('HOST_IN_MAINTENANCE_MODE'),
            'HOST_IN_PARTIAL_MAINTENANCE_MODE': IssueType('HOST_IN_PARTIAL_MAINTENANCE_MODE'),
            'HOST_IN_STAND_BY_MODE': IssueType('HOST_IN_STAND_BY_MODE'),
            'HOST_NOT_REACHABLE': IssueType('HOST_NOT_REACHABLE'),
            'VM_INVALID_CONFIG': IssueType('VM_INVALID_CONFIG'),
            'VMS_DISABLED': IssueType('VMS_DISABLED'),
            'VM_LIFECYCLE_HOOK_TIMED_OUT': IssueType('VM_LIFECYCLE_HOOK_TIMED_OUT'),
            'VM_LIFECYCLE_HOOK_FAILED': IssueType('VM_LIFECYCLE_HOOK_FAILED'),
            'VM_PROTECTED': IssueType('VM_PROTECTED'),
        })
        IssueType._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.clusters.vms.solutions.issue_info.issue_type',
            IssueType))

    IssueInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.issue_info', {
            'type': type.ReferenceType(__name__, 'Solutions.IssueInfo.IssueType'),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        IssueInfo,
        False,
        None))


    class DeploymentInfo(VapiStruct):
        """
        The ``Solutions.DeploymentInfo`` class contains attributes that describe
        the state of a single VM deployment of a solution.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'IN_PROGRESS' : [('solution_info', True)],
                    'COMPLIANT' : [('solution_info', True)],
                    'ISSUE' : [('solution_info', True)],
                    'IN_LIFECYCLE_HOOK' : [('solution_info', True)],
                    'OBSOLETE_SPEC' : [('solution_info', True)],
                    'NOT_APPLIED' : [],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     vm=None,
                     replacement_vm=None,
                     issues=None,
                     lifecycle_hook=None,
                     solution_info=None,
                    ):
            """
            :type  status: :class:`Solutions.DeploymentInfo.Status`
            :param status: Compliance status of the deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vm: :class:`str` or ``None``
            :param vm: Identifier of the currently deployed VM. More information about the
                runtime state of the VM can be observed through the VIM API.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
                This field is None if: 
                
                * The VM deployment is not started yet.
                * There are issues specified by the ``issues`` that prevents the VM
                  to be deployed.
            :type  replacement_vm: :class:`str` or ``None``
            :param replacement_vm: Identifier of the VM that is going to replace the current deployed
                VM. More information about the runtime state of the VM can be
                observed through the VIM API.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
                This field is None if there is no ongoing VM upgrade for the
                current VM deployment.
            :type  issues: :class:`list` of :class:`Solutions.IssueInfo`
            :param issues: List of :class:`Solutions.IssueInfo` which do not allow the
                deployment to reach the desired specification specified by the
                ``solutionInfo``. In order to remediate these issues an apply
                operation :func:`Solutions.apply` need to be initiated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  lifecycle_hook: :class:`LifecycleHookInfo` or ``None``
            :param lifecycle_hook: The activated VM lifecycle hook for the VM specified by the ``vm``
                that the system is waiting to be processed by the solution in order
                to continue attempting to reach the desired specification.
                This attribute was added in **vSphere API 9.0.0.0**.
                This field is None if there is no activated hook for the VM.
            :type  solution_info: :class:`Solutions.SolutionInfo`
            :param solution_info: Describes the current desired solution specification of the
                deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`Solutions.DeploymentInfo.Status.IN_PROGRESS`,
                :attr:`Solutions.DeploymentInfo.Status.COMPLIANT`,
                :attr:`Solutions.DeploymentInfo.Status.ISSUE`,
                :attr:`Solutions.DeploymentInfo.Status.IN_LIFECYCLE_HOOK`, or
                :attr:`Solutions.DeploymentInfo.Status.OBSOLETE_SPEC`.
            """
            self.status = status
            self.vm = vm
            self.replacement_vm = replacement_vm
            self.issues = issues
            self.lifecycle_hook = lifecycle_hook
            self.solution_info = solution_info
            VapiStruct.__init__(self)


        class Status(Enum):
            """
            The ``Solutions.DeploymentInfo.Status`` class defines how well a deployment
            conforms to the desired specification that is specified by the
            ``solutionInfo``.
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
            NOT_APPLIED = None
            """
            The desired specification of the solution has never been applied.

            """
            IN_PROGRESS = None
            """
            The system is actively working to reach the desired specification.

            """
            COMPLIANT = None
            """
            The deployment is in full compliance with the desired specification.

            """
            ISSUE = None
            """
            The system has hit issues that do not allow the deployment to reach the
            desired specification. See :attr:`Solutions.DeploymentInfo.issues`.

            """
            IN_LIFECYCLE_HOOK = None
            """
            The system is waiting on an activated VM lifecycle hook to be processed by
            the solution in order to continue attempting to reach the desired
            specification. See :attr:`Solutions.DeploymentInfo.lifecycle_hook`.

            """
            OBSOLETE_SPEC = None
            """
            The current desired specification of the solution is newer than the
            applied. 
            
            * ``IN_PROGRESS``
            * ``ISSUE``
            * ``IN_LIFECYCLE_HOOK``

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Status` instance.
                """
                Enum.__init__(string)

        Status._set_values({
            'NOT_APPLIED': Status('NOT_APPLIED'),
            'IN_PROGRESS': Status('IN_PROGRESS'),
            'COMPLIANT': Status('COMPLIANT'),
            'ISSUE': Status('ISSUE'),
            'IN_LIFECYCLE_HOOK': Status('IN_LIFECYCLE_HOOK'),
            'OBSOLETE_SPEC': Status('OBSOLETE_SPEC'),
        })
        Status._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.clusters.vms.solutions.deployment_info.status',
            Status))

    DeploymentInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.deployment_info', {
            'status': type.ReferenceType(__name__, 'Solutions.DeploymentInfo.Status'),
            'vm': type.OptionalType(type.IdType()),
            'replacement_vm': type.OptionalType(type.IdType()),
            'issues': type.ListType(type.ReferenceType(__name__, 'Solutions.IssueInfo')),
            'lifecycle_hook': type.OptionalType(type.ReferenceType(__name__, 'LifecycleHookInfo')),
            'solution_info': type.OptionalType(type.ReferenceType(__name__, 'Solutions.SolutionInfo')),
        },
        DeploymentInfo,
        False,
        None))


    class DeploymentCompliance(VapiStruct):
        """
        The ``Solutions.DeploymentCompliance`` class contains attributes that
        describe the compliance of a given VM deployment. See
        :class:`Solutions.DeploymentInfo`
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     notifications=None,
                     deployment=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Compliance status of the deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications describing the compliance result.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  deployment: :class:`Solutions.DeploymentInfo`
            :param deployment: The current VM deployment.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.status = status
            self.notifications = notifications
            self.deployment = deployment
            VapiStruct.__init__(self)


    DeploymentCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.deployment_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
            'deployment': type.ReferenceType(__name__, 'Solutions.DeploymentInfo'),
        },
        DeploymentCompliance,
        False,
        None))


    class HostCompliance(VapiStruct):
        """
        The ``Solutions.HostCompliance`` class contains attributes that describe
        the compliance for a specific host.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     compliances=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Aggregated compliance status for all solutions for which compliance
                check was requested.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliances: :class:`dict` of :class:`str` and :class:`Solutions.DeploymentCompliance`
            :param compliances: Compliance for the solutions for which a compliance check was
                requested.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``.
            """
            self.status = status
            self.compliances = compliances
            VapiStruct.__init__(self)


    HostCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'compliances': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.DeploymentCompliance')),
        },
        HostCompliance,
        False,
        None))


    class HostSolutionsCompliance(VapiStruct):
        """
        The ``Solutions.HostSolutionsCompliance`` class contains attributes that
        describe the compliance of solutions with deployment type
        :attr:`DeploymentType.EVERY_HOST_PINNED`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     compliances=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Aggregated compliance status for all solutions for which a
                compliance check was requested.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliances: :class:`dict` of :class:`str` and :class:`Solutions.HostCompliance`
            :param compliances: Compliance status of the hosts that were part of the check
                compliance method.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``HostSystem``. When methods return a value of this class as
                a return value, the key in the attribute :class:`dict` will be an
                identifier for the resource type: ``HostSystem``.
            """
            self.status = status
            self.compliances = compliances
            VapiStruct.__init__(self)


    HostSolutionsCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.host_solutions_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'compliances': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.HostCompliance')),
        },
        HostSolutionsCompliance,
        False,
        None))


    class ClusterSolutionCompliance(VapiStruct):
        """
        The ``Solutions.ClusterSolutionCompliance`` class contains attributes that
        describe the compliance for a specific solution.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     compliances=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Aggregated compliance status for all deployment units for which a
                compliance check was requested.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliances: :class:`dict` of :class:`str` and :class:`Solutions.DeploymentCompliance`
            :param compliances: Compliance status for the deployment units for which a compliance
                check was requested.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmDeploymentUnit``.
            """
            self.status = status
            self.compliances = compliances
            VapiStruct.__init__(self)


    ClusterSolutionCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solution_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'compliances': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.DeploymentCompliance')),
        },
        ClusterSolutionCompliance,
        False,
        None))


    class ClusterSolutionsCompliance(VapiStruct):
        """
        The ``Solutions.ClusterSolutionsCompliance`` class contains attributes that
        describe the compliance of solutions with deployment type
        :attr:`DeploymentType.CLUSTER_VM_SET`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     compliances=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Aggregated compliance status for all solutions for which a
                compliance check was requested.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliances: :class:`dict` of :class:`str` and :class:`Solutions.ClusterSolutionCompliance`
            :param compliances: Compliance for the solutions for which a compliance check was
                requested.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.esx.settings.vms.SystemVmSolution``.
            """
            self.status = status
            self.compliances = compliances
            VapiStruct.__init__(self)


    ClusterSolutionsCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_solutions_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'compliances': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Solutions.ClusterSolutionCompliance')),
        },
        ClusterSolutionsCompliance,
        False,
        None))


    class ClusterCompliance(VapiStruct):
        """
        The ``Solutions.ClusterCompliance`` class contains attributes that describe
        the result of the compliance :func:`Solutions.check_compliance` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     status=None,
                     host_solutions_status=None,
                     cluster_solutions_status=None,
                    ):
            """
            :type  status: :class:`Solutions.ComplianceStatus`
            :param status: Aggregated status of the compliance check method.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  host_solutions_status: :class:`Solutions.HostSolutionsCompliance`
            :param host_solutions_status: Compliance status of all solutions with deployment type
                :attr:`DeploymentType.EVERY_HOST_PINNED` that were part of the
                :func:`Solutions.check_compliance` method.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cluster_solutions_status: :class:`Solutions.ClusterSolutionsCompliance`
            :param cluster_solutions_status: Compliance status of all solutions with deployment type
                :attr:`DeploymentType.CLUSTER_VM_SET` that were part of the
                :func:`Solutions.check_compliance` method.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.status = status
            self.host_solutions_status = host_solutions_status
            self.cluster_solutions_status = cluster_solutions_status
            VapiStruct.__init__(self)


    ClusterCompliance._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.solutions.cluster_compliance', {
            'status': type.ReferenceType(__name__, 'Solutions.ComplianceStatus'),
            'host_solutions_status': type.ReferenceType(__name__, 'Solutions.HostSolutionsCompliance'),
            'cluster_solutions_status': type.ReferenceType(__name__, 'Solutions.ClusterSolutionsCompliance'),
        },
        ClusterCompliance,
        False,
        None))



    def get(self,
            cluster,
            solution,
            ):
        """
        Returns the desired specification of a solution in a given cluster.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  solution: :class:`str`
        :param solution: Identifier of the solution.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.vms.SystemVmSolution``.
        :rtype: :class:`Solutions.SolutionInfo`
        :return: The desired specification of the ``solution`` in the ``cluster``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system or
            no solution associated with ``solution`` in the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Read``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            'solution': solution,
                            })

    def list(self,
             cluster,
             filter_spec=None,
             ):
        """
        Returns the desired specification of given solutions in a given
        cluster.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter_spec: :class:`Solutions.FilterSpec` or ``None``
        :param filter_spec: Spec to filter the desired specification that to be returned.
            if None or empty the desired specification of all solutions in the
            cluster is returned.
        :rtype: :class:`Solutions.ListResult`
        :return: The desired specification of solutions in the ``cluster`` specified
            by the ``filter_spec``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system or
            the ``filter_spec`` specifies one or more solutions that are not
            associated with the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Read``.
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'filter_spec': filter_spec,
                            })


    def set_task(self,
            cluster,
            solution,
            spec,
            ):
        """
        Sets and overrides the current desired specification for a given
        solution and cluster. The provided desired specification is validated
        before that.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  solution: :class:`str`
        :param solution: Identifier of the solution.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.vms.SystemVmSolution``.
        :type  spec: :class:`SolutionSpec`
        :param spec: Solution specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the validation of the solution specification fails. The value of
            the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` contains more
            information. It is a class that contains all the attributes defined
            in :class:`Solutions.ValidateResult`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster``.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Write``.
        """
        task_id = self._invoke('set$task',
                                {
                                'cluster': cluster,
                                'solution': solution,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               solution,
               ):
        """
        Deletes the current desired specification of a solution for a given
        cluster. 
        
        The actual uninstallation of the solution is executed after an apply
        operation that implicitly or explicitly contains the identifier of the
        deleted solution. Examples: 
        
        * Explicit: The apply operation is triggered with
          :class:`Solutions.ApplySpec` that contains the identifier of the
          deleted solution.
        * Implicit: The apply operation is triggered with
          :class:`Solutions.ApplySpec` whose hostSolutions attribute is None or
          empty. solution.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  solution: :class:`str`
        :param solution: Identifier of the VM solution.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.vms.SystemVmSolution``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the validation of the cluster desired specification fails. The
            value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` contains more
            information. It is a class that contains all the attributes defined
            in :class:`Solutions.ValidateResult`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system or
            no solution associated with ``solution`` in the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Write``.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'solution': solution,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def apply_task(self,
              cluster,
              spec,
              ):
        """
        Applies the current desired solution specification to a given cluster
        as specified by the :class:`Solutions.ApplySpec`. 
        
        The runtime state of the applied desired solution specification can be
        observed using :func:`Solutions.check_compliance` method. 
        
        If a solution that is specified within the ``spec`` is uninstalled/not
        present (not present in the cluster's desired state and runtime state)
        it is omitted from the result. 
        
        If a deployment unit that is specified within the ``spec`` is
        uninstalled/not present (not present for any of the solutions specified
        within the ``spec``) it is omitted from the result.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`Solutions.ApplySpec`
        :param spec: Apply specification.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an internal error. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the ``spec`` specifies an invalid argument. For example thrown
            if a host that is specified within the ``spec`` is not present in
            the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If 1) there is another operation in progress for any of the
            solutions specified within the ``spec`` or 2) System VMs are
            disabled on the cluster via internal ESX Agent Manager (EAM) API
            (eam.EsxtAgentManager#disable).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with the ``cluster`` parameter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Write``.
        """
        task_id = self._invoke('apply$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Solutions.ApplyResult'))
        return task_instance


    def check_compliance_task(self,
                         cluster,
                         filter_spec,
                         ):
        """
        Checks compliance of solutions in the cluster against the current
        desired state. 
        
        If a solution that is specified within the ``filter_spec`` is
        uninstalled/not present (not present in the cluster's desired state and
        runtime state) it is omitted from the result. 
        
        If a deployment unit that is specified within the ``filter_spec`` is
        uninstalled/not present (not present for any of the solutions specified
        within the ``filter_spec``) it is omitted from the result.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter_spec: :class:`Solutions.CheckComplianceFilterSpec`
        :param filter_spec: Filter for checking the compliance status in a cluster.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If an internal error occurred. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If the ``filter_spec`` specifies an invalid argument. For example
            thrown if a host that is specified within the ``filter_spec`` is
            not present in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with the ``cluster`` parameter.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Read``.
        """
        task_id = self._invoke('check_compliance$task',
                                {
                                'cluster': cluster,
                                'filter_spec': filter_spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Solutions.ClusterCompliance'))
        return task_instance
class Transition(VapiInterface):
    """
    The ``Transition`` class provides methods to manage the transition of a
    System VM solution desired solution specification from EAM to vLCM.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.vms.transition'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TransitionStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'enable_task': 'enable$task'})

    class ValidationResult(VapiStruct):
        """
        The ``Transition.ValidationResult`` class contains attributes that describe
        the the validation result during the execution of an
        :func:`Transition.enable` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                    ):
            """
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications associated with the validation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.notifications = notifications
            VapiStruct.__init__(self)


    ValidationResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.transition.validation_result', {
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ValidationResult,
        False,
        None))


    class EnableSpec(VapiStruct):
        """
        The ``Transition.EnableSpec`` class contains attributes that describe
        specification for enablement of EAM managed solution in vLCM.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     eam_agency_id=None,
                     solution=None,
                    ):
            """
            :type  eam_agency_id: :class:`str`
            :param eam_agency_id: Identifier of the solution in EAM (EAM agency).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  solution: :class:`SolutionSpec`
            :param solution: Target desired solution specification in vLCM.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.eam_agency_id = eam_agency_id
            self.solution = solution
            VapiStruct.__init__(self)


    EnableSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.vms.transition.enable_spec', {
            'eam_agency_id': type.StringType(),
            'solution': type.ReferenceType(__name__, 'SolutionSpec'),
        },
        EnableSpec,
        False,
        None))




    def enable_task(self,
               cluster,
               solution,
               spec,
               ):
        """
        Enables an EAM managed solution in vLCM. The solution specification is
        validated before the enablement is started. 
        
        The enablement only transfers ownership of the solution from EAM to
        LCCM and sets the desired state in LCCM. The new desired state is not
        applied, the solution system VMs are untouched.  The following happens
        once the method is started: 
        
        * A removal of the corresponding agency in EAM is triggered.
        
        The following happens once the method is completed: 
        
        * The corresponding agency in EAM can no longer be controlled through
          the EAM API.
        * The management of the desired solution specification can be done only
          trough vLCM. See :class:`Solutions`
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  solution: :class:`str`
        :param solution: Identifier of the solution.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.vms.SystemVmSolution``.
        :type  spec: :class:`Transition.EnableSpec`
        :param spec: Enablement specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an internal error. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If: 
            
            * the validation of the cluster desired specification fails.
            * the solution associated with ``solution`` already exists in vLCM
              for the cluster.
            * the agency associated with the eamAgencyID attribute exists, but
              is not in the scope of the ``cluster``.
            
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` contains more
            information. It is a class that contains all the attributes defined
            in :class:`Transition.ValidationResult`.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If System VMs are disabled on the cluster via internal ESX Agent
            Manager (EAM) API (eam.EsxtAgentManager#disable).
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the cluster associated with ``cluster`` is not managed by vLCM.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with the ``cluster`` or if there
            is no EAM agency associated with the eamAgencyID attribute of the
            ``spec`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.systemVM.Write``.
        """
        task_id = self._invoke('enable$task',
                                {
                                'cluster': cluster,
                                'solution': solution,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _LifecycleHooksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for mark_as_processed operation
        mark_as_processed_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'LifecycleHooks.ProcessedHookSpec'),
        })
        mark_as_processed_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        mark_as_processed_input_value_validator_list = [
        ]
        mark_as_processed_output_validator_list = [
        ]
        mark_as_processed_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/vms/lifecycle-hooks?action=mark-as-processed',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'mark-as-processed',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'solution': type.IdType(resource_types='com.vmware.esx.settings.vms.SystemVmSolution'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/esx/settings/clusters/{cluster}/vms/lifecycle-hooks/{solution}',
            path_variables={
                'cluster': 'cluster',
                'solution': 'solution',
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
            'mark_as_processed': {
                'input_type': mark_as_processed_input_type,
                'output_type': type.VoidType(),
                'errors': mark_as_processed_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': mark_as_processed_input_value_validator_list,
                'output_validator_list': mark_as_processed_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'LifecycleHooks.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'mark_as_processed': mark_as_processed_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.vms.lifecycle_hooks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SolutionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'solution': type.IdType(resource_types='com.vmware.esx.settings.vms.SystemVmSolution'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions/{solution}',
            path_variables={
                'cluster': 'cluster',
                'solution': 'solution',
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
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter_spec': type.OptionalType(type.ReferenceType(__name__, 'Solutions.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions',
            path_variables={
                'cluster': 'cluster',
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
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'solution': type.IdType(resource_types='com.vmware.esx.settings.vms.SystemVmSolution'),
            'spec': type.ReferenceType(__name__, 'SolutionSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions/{solution}',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'solution': 'solution',
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
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'solution': type.IdType(resource_types='com.vmware.esx.settings.vms.SystemVmSolution'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions/{solution}',
            path_variables={
                'cluster': 'cluster',
                'solution': 'solution',
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

        # properties for apply operation
        apply_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'Solutions.ApplySpec'),
        })
        apply_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        apply_input_value_validator_list = [
        ]
        apply_output_validator_list = [
        ]
        apply_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions?action=apply',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'apply',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for check_compliance operation
        check_compliance_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter_spec': type.ReferenceType(__name__, 'Solutions.CheckComplianceFilterSpec'),
        })
        check_compliance_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        check_compliance_input_value_validator_list = [
        ]
        check_compliance_output_validator_list = [
        ]
        check_compliance_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/vms/solutions?action=check-compliance',
            request_body_parameter='filter_spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-compliance',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Solutions.SolutionInfo'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Solutions.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'apply$task': {
                'input_type': apply_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': apply_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': apply_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'check_compliance$task': {
                'input_type': check_compliance_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': check_compliance_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': check_compliance_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
            'apply': apply_rest_metadata,
            'check_compliance': check_compliance_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.vms.solutions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TransitionStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for enable operation
        enable_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'solution': type.IdType(resource_types='com.vmware.esx.settings.vms.SystemVmSolution'),
            'spec': type.ReferenceType(__name__, 'Transition.EnableSpec'),
        })
        enable_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        enable_input_value_validator_list = [
        ]
        enable_output_validator_list = [
        ]
        enable_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/vms/transition/{solution}?action=enable',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'solution': 'solution',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'enable',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'enable$task': {
                'input_type': enable_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': enable_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': enable_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'enable': enable_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.vms.transition',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'LifecycleHooks': LifecycleHooks,
        'Solutions': Solutions,
        'Transition': Transition,
    }

