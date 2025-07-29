# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.
#---------------------------------------------------------------------------

"""
The
``com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides_client``
module provides classes to manage overrides of HCL status classifications
(compliance and VCG product identification) for PCI devices in clusters of ESXi
hosts.

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


class VcgEntries(VapiInterface):
    """
    This class provides methods to store and return information about local
    host hardware provided by the user.
    This class was added in **vSphere API 7.0.3.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VcgEntriesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})

    class PciDeviceIdentifier(VapiStruct):
        """
        The ``VcgEntries.PciDeviceIdentifier`` class specifies a particular PCI
        device product its characteristic ID (VID/DID/SVID/SSID)
        This class was added in **vSphere API 7.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vid=None,
                     did=None,
                     svid=None,
                     ssid=None,
                    ):
            """
            :type  vid: :class:`str`
            :param vid: The PCI device's Vendor ID (VID). 
                
                The VID is a unique number assigned by the PCI SIG to every PCI
                device vendor to identify the chipset manufacturer (e.g. for a NIC
                that might be Broadcom or Atheros). The VID and the Device ID (DID)
                below typically determine the choice of device driver.
                This attribute was added in **vSphere API 7.0.3.0**.
            :type  did: :class:`str`
            :param did: The PCI device's Device ID (DID). 
                
                The DID is assigned by the vendor to identify a particular device.
                This attribute was added in **vSphere API 7.0.3.0**.
            :type  svid: :class:`str`
            :param svid: The PCI device's sub-vendor ID (SVID). 
                
                Where the VID identifies the chipset of a given card, the SVID
                identifies the card manufacturer (e.g. for a NIC, the card
                manufacturer might be Netgear or D-Link). 
                
                May be 0 to indicate the override should apply to all PCI devices
                of the specified VID/DID
                This attribute was added in **vSphere API 7.0.3.0**.
            :type  ssid: :class:`str`
            :param ssid: The PCI device's Subsystem ID (SSID). 
                
                The Subsystem ID is assigned by the subsystem vendor from the sam
                number space as the Device ID. The SVID and SSID together provide
                information the driver might use to apply a small card-specific
                changes in operation based on the card's unique characteristics. 
                
                May be 0 to indicate the override should apply to all PCI devices
                of the specified VID/DID
                This attribute was added in **vSphere API 7.0.3.0**.
            """
            self.vid = vid
            self.did = did
            self.svid = svid
            self.ssid = ssid
            VapiStruct.__init__(self)


    PciDeviceIdentifier._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries.pci_device_identifier', {
            'vid': type.StringType(),
            'did': type.StringType(),
            'svid': type.StringType(),
            'ssid': type.StringType(),
        },
        PciDeviceIdentifier,
        False,
        None))


    class Key(VapiStruct):
        """
        The ``VcgEntries.Key`` class specifies a particular combination of PCI ID,
        specific FW version if known, Driver name, Driver version, and vSphere
        release for which a given override applies.
        This class was added in **vSphere API 7.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     device=None,
                     firmware_version=None,
                     part_number=None,
                     driver_name=None,
                     driver_version=None,
                     product_id=None,
                     capacity=None,
                    ):
            """
            :type  device: :class:`VcgEntries.PciDeviceIdentifier`
            :param device: The PCI device ID
                This attribute was added in **vSphere API 7.0.3.0**.
            :type  firmware_version: :class:`str` or ``None``
            :param firmware_version: The device firmware version
                This attribute was added in **vSphere API 7.0.3.0**.
                if not specified, the override applies to devices with an unknown
                firmware version.
            :type  part_number: :class:`str` or ``None``
            :param part_number: OEM part number for device as used in BCG
                This attribute was added in **vSphere API 7.0.3.0**.
                if None the override applies to devices without a part number.
            :type  driver_name: :class:`str` or ``None``
            :param driver_name: The name of the device driver for which this override applies
                This attribute was added in **vSphere API 7.0.3.0**.
                if None the override applies to the specified device regardless of
                driver name.
            :type  driver_version: :class:`str` or ``None``
            :param driver_version: The version of the device driver for which this override applies
                (only accepted if 'driverName' is also specified)
                This attribute was added in **vSphere API 7.0.3.0**.
                if None the override applies to the specified device regardless of
                driver version.
            :type  product_id: :class:`str` or ``None``
            :param product_id: The Product ID for the device which this override applies (as
                presented by the device itself). May be left None for devices that
                don't present a model number/product ID.
                This attribute was added in **vSphere API 7.0.3.0**.
                if None the override applies to the specified device regardless of
                product ID.
            :type  capacity: :class:`long` or ``None``
            :param capacity: Storage device capacity (in bytes)
                This attribute was added in **vSphere API 7.0.3.0**.
                if None the override applies to the specified device regardless of
                capacity.
            """
            self.device = device
            self.firmware_version = firmware_version
            self.part_number = part_number
            self.driver_name = driver_name
            self.driver_version = driver_version
            self.product_id = product_id
            self.capacity = capacity
            VapiStruct.__init__(self)


    Key._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries.key', {
            'device': type.ReferenceType(__name__, 'VcgEntries.PciDeviceIdentifier'),
            'firmware_version': type.OptionalType(type.StringType()),
            'part_number': type.OptionalType(type.StringType()),
            'driver_name': type.OptionalType(type.StringType()),
            'driver_version': type.OptionalType(type.StringType()),
            'product_id': type.OptionalType(type.StringType()),
            'capacity': type.OptionalType(type.IntegerType()),
        },
        Key,
        False,
        None))


    class ProductSelectionSpec(VapiStruct):
        """
        The ``VcgEntries.ProductSelectionSpec`` class describes overrides for a
        given PCI device.
        This class was added in **vSphere API 7.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     target=None,
                     vcg_product=None,
                    ):
            """
            :type  target: :class:`VcgEntries.Key`
            :param target: The PCI device this update should apply to.
                This attribute was added in **vSphere API 7.0.3.0**.
            :type  vcg_product: :class:`str` or ``None``
            :param vcg_product: The BCG Product ID to be used.
                This attribute was added in **vSphere API 7.0.3.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.vcg_product``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.esx.settings.vcg_product``.
                if None, the override is removed and the system reverts to matching
                the device to a BCG/HCL entry by PCI ID, device FW, driver, and
                driver version.
            """
            self.target = target
            self.vcg_product = vcg_product
            VapiStruct.__init__(self)


    ProductSelectionSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries.product_selection_spec', {
            'target': type.ReferenceType(__name__, 'VcgEntries.Key'),
            'vcg_product': type.OptionalType(type.IdType()),
        },
        ProductSelectionSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``VcgEntries.UpdateSpec`` class describes the override(s) to be applied
        for a set of PCI devices
        This class was added in **vSphere API 7.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     product_selections=None,
                    ):
            """
            :type  product_selections: :class:`list` of :class:`VcgEntries.ProductSelectionSpec`
            :param product_selections: The overrides to be applied for the specified targets.
                This attribute was added in **vSphere API 7.0.3.0**.
            """
            self.product_selections = product_selections
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries.update_spec', {
            'product_selections': type.ListType(type.ReferenceType(__name__, 'VcgEntries.ProductSelectionSpec')),
        },
        UpdateSpec,
        False,
        None))




    def update_task(self,
               cluster,
               spec,
               ):
        """
        Updates a PCI Device's HCL treatment, either driving a particular BCG
        Proudct ID or overriding compliance status based on user specification
        This method was added in **vSphere API 7.0.3.0**.

        :type  cluster: :class:`str`
        :param cluster: identifier of the cluster for validity domain of this update
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`VcgEntries.UpdateSpec`
        :param spec: Specification for the override(s) to be applied.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown error. The accompanying error message will
            give more details about the failure and any possible resolution(s).
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if an invalid override is specified
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no cluster with the given id.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the vCenter this API is executed on is not part of the Customer
            Experience Improvement Program (CEIP).
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.HardwareCompatibility.Write``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.HardwareCompatibility.Write``.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _VcgEntriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType(__name__, 'VcgEntries.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
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
            url_template='/esx/settings/clusters/{cluster}/software/reports/hardware-compatibility/pci-device-overrides/vcg-entries',
            request_body_parameter='spec',
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

        operations = {
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.software.reports.hardware_compatibility.pci_device_overrides.vcg_entries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'VcgEntries': VcgEntries,
    }

