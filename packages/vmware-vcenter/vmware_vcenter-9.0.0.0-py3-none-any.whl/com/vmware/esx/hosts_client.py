# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.hosts.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.hosts_client`` module provides classes to manage ESX host.

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


class CertificateInfo(VapiStruct):
    """
    The ``CertificateInfo`` Class contains information about the SSL
    certificate for a server.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 ssl_thumbprint=None,
                 ssl_certificate=None,
                ):
        """
        :type  ssl_thumbprint: :class:`str`
        :param ssl_thumbprint: The SHA thumbprint of the SSL certificate for a server.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  ssl_certificate: :class:`str` or ``None``
        :param ssl_certificate: PEM-encoded SSL certificate of the ESX host.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional because it was added in a newer version
            than its parent node.
        """
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_certificate = ssl_certificate
        VapiStruct.__init__(self)


CertificateInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.certificate_info', {
        'ssl_thumbprint': type.StringType(),
        'ssl_certificate': type.OptionalType(type.StringType()),
    },
    CertificateInfo,
    False,
    None))



class Notification(VapiStruct):
    """
    The ``Notification`` class contains attributes to describe any
    info/warning/error messages that Tasks can raise.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 id=None,
                 time=None,
                 message=None,
                 resolution=None,
                ):
        """
        :type  id: :class:`str`
        :param id: The notification id.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  time: :class:`datetime.datetime`
        :param time: The time the notification was raised/found.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param message: The notification message.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  resolution: :class:`com.vmware.vapi.std_client.LocalizableMessage` or ``None``
        :param resolution: The resolution message, if any.
            This attribute was added in **vSphere API 7.0.2.0**.
            Only :class:`set` if there is a resolution available for this
            notification.
        """
        self.id = id
        self.time = time
        self.message = message
        self.resolution = resolution
        VapiStruct.__init__(self)


Notification._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.notification', {
        'id': type.StringType(),
        'time': type.DateTimeType(),
        'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'resolution': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
    },
    Notification,
    False,
    None))



class Notifications(VapiStruct):
    """
    The ``Notifications`` class contains info/warning/error messages that can
    be reported be the task.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 info=None,
                 warnings=None,
                 errors=None,
                ):
        """
        :type  info: :class:`list` of :class:`Notification` or ``None``
        :param info: Info notification messages reported.
            This attribute was added in **vSphere API 7.0.2.0**.
            Only :class:`set` if an info was reported by the task.
        :type  warnings: :class:`list` of :class:`Notification` or ``None``
        :param warnings: Warning notification messages reported.
            This attribute was added in **vSphere API 7.0.2.0**.
            Only :class:`set` if an warning was reported by the task.
        :type  errors: :class:`list` of :class:`Notification` or ``None``
        :param errors: Error notification messages reported.
            This attribute was added in **vSphere API 7.0.2.0**.
            Only :class:`set` if an error was reported by the task.
        """
        self.info = info
        self.warnings = warnings
        self.errors = errors
        VapiStruct.__init__(self)


Notifications._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.notifications', {
        'info': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Notification'))),
    },
    Notifications,
    False,
    None))



class ComponentInfo(VapiStruct):
    """
    The ``ComponentInfo`` class contains attributes that describe a specific
    component version in the software solution.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                 display_name=None,
                 display_version=None,
                 vendor=None,
                ):
        """
        :type  version: :class:`str`
        :param version: Version of the component. It will be empty when the component is
            removed.
        :type  display_name: :class:`str`
        :param display_name: Display name of the component.
        :type  display_version: :class:`str`
        :param display_version: Human readable version of the component.
        :type  vendor: :class:`str`
        :param vendor: Vendor of the component.
        """
        self.version = version
        self.display_name = display_name
        self.display_version = display_version
        self.vendor = vendor
        VapiStruct.__init__(self)


ComponentInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.component_info', {
        'version': type.StringType(),
        'display_name': type.StringType(),
        'display_version': type.StringType(),
        'vendor': type.StringType(),
    },
    ComponentInfo,
    False,
    None))



class SolutionInfo(VapiStruct):
    """
    The ``SolutionInfo`` class contains attributes that describe solution
    registered in the software solution.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                 display_name=None,
                 components=None,
                ):
        """
        :type  version: :class:`str`
        :param version: Version of the solution.
        :type  display_name: :class:`str`
        :param display_name: Display name of the solution.
        :type  components: :class:`dict` of :class:`str` and :class:`ComponentInfo`
        :param components: Components registered by the solution.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
        """
        self.version = version
        self.display_name = display_name
        self.components = components
        VapiStruct.__init__(self)


SolutionInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.solution_info', {
        'version': type.StringType(),
        'display_name': type.StringType(),
        'components': type.MapType(type.IdType(), type.ReferenceType(__name__, 'ComponentInfo')),
    },
    SolutionInfo,
    False,
    None))



class BaseImageInfo(VapiStruct):
    """
    The ``BaseImageInfo`` class contains attributes that describe a specific
    ESX base-image in the software solution.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                 display_name=None,
                 display_version=None,
                 release_date=None,
                ):
        """
        :type  version: :class:`str`
        :param version: Version of the base-image.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.esx.hosts.base_image``. When methods return a value of
            this class as a return value, the attribute will be an identifier
            for the resource type: ``com.vmware.esx.hosts.base_image``.
        :type  display_name: :class:`str`
        :param display_name: Display name of the base-image.
        :type  display_version: :class:`str`
        :param display_version: Human readable version of the base-image.
        :type  release_date: :class:`datetime.datetime`
        :param release_date: Release date of the base-image.
        """
        self.version = version
        self.display_name = display_name
        self.display_version = display_version
        self.release_date = release_date
        VapiStruct.__init__(self)


BaseImageInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.base_image_info', {
        'version': type.IdType(resource_types='com.vmware.esx.hosts.base_image'),
        'display_name': type.StringType(),
        'display_version': type.StringType(),
        'release_date': type.DateTimeType(),
    },
    BaseImageInfo,
    False,
    None))



class AddOnInfo(VapiStruct):
    """
    The ``AddOnInfo`` class contains attributes that describe a specific OEM
    customization add-on in the software solution.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 version=None,
                 display_name=None,
                 vendor=None,
                 display_version=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the add-on
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.esx.hosts.add_on``. When methods return a value of
            this class as a return value, the attribute will be an identifier
            for the resource type: ``com.vmware.esx.hosts.add_on``.
        :type  version: :class:`str`
        :param version: Version of the add-on
        :type  display_name: :class:`str`
        :param display_name: Display name of the OEM add-on.
        :type  vendor: :class:`str`
        :param vendor: Vendor of the OEM add-on.
        :type  display_version: :class:`str`
        :param display_version: Human readable version of the OEM add-on.
        """
        self.name = name
        self.version = version
        self.display_name = display_name
        self.vendor = vendor
        self.display_version = display_version
        VapiStruct.__init__(self)


AddOnInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.add_on_info', {
        'name': type.IdType(resource_types='com.vmware.esx.hosts.add_on'),
        'version': type.StringType(),
        'display_name': type.StringType(),
        'vendor': type.StringType(),
        'display_version': type.StringType(),
    },
    AddOnInfo,
    False,
    None))



class HardwareSupportPackageInfo(VapiStruct):
    """
    The ``HardwareSupportPackageInfo`` class contains information to describe
    the Hardware Support Package (HSP) configured for a single device or
    distinct group of devices (typically the OEM's, including BIOS and device
    firmware).
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 pkg=None,
                 version=None,
                ):
        """
        :type  pkg: :class:`str`
        :param pkg: Identifier of Hardware Support Package (HSP) selected
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.esx.hosts.hardware_support.package``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.esx.hosts.hardware_support.package``.
        :type  version: :class:`str`
        :param version: Version of the Hardware Support Package (HSP) selected (e.g.
            "20180128.1" or "v42")
            This attribute was added in **vSphere API 7.0.2.0**.
        """
        self.pkg = pkg
        self.version = version
        VapiStruct.__init__(self)


HardwareSupportPackageInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.hardware_support_package_info', {
        'pkg': type.IdType(resource_types='com.vmware.esx.hosts.hardware_support.package'),
        'version': type.StringType(),
    },
    HardwareSupportPackageInfo,
    False,
    None))



class HardwareSupportInfo(VapiStruct):
    """
    The ``HardwareSupportInfo`` class contains information to describe the
    Hardware Support Package (HSP) in the software solution.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 packages=None,
                ):
        """
        :type  packages: :class:`dict` of :class:`str` and :class:`HardwareSupportPackageInfo`
        :param packages: Map of Hardware Support Packages (HSPs). The key is the Hardware
            Support Manager (HSM) identifier and the value is the specification
            detailing the HSP configured for that HSM.
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.hardware_support.manager``. When
            methods return a value of this class as a return value, the key in
            the attribute :class:`dict` will be an identifier for the resource
            type: ``com.vmware.esx.hosts.hardware_support.manager``.
        """
        self.packages = packages
        VapiStruct.__init__(self)


HardwareSupportInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.hardware_support_info', {
        'packages': type.MapType(type.IdType(), type.ReferenceType(__name__, 'HardwareSupportPackageInfo')),
    },
    HardwareSupportInfo,
    False,
    None))



class HostHardwareInfo(VapiStruct):
    """
    The ``HostHardwareInfo`` class contains attributes to describe the host's
    hardware specifications like vendor, model, family and oem string.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vendor=None,
                 models=None,
                 families=None,
                 oem_strings=None,
                ):
        """
        :type  vendor: :class:`str`
        :param vendor: Host's vendor name. Maps to "Manufacturer" in SMBIOS: System
            Information (Type 1) and offset 04h
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  models: :class:`set` of :class:`str` or ``None``
        :param models: Host's model name.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, model name will not be used for image selection Maps to
            "Product Name" in SMBIOS: System Information (Type 1) and offset
            05h
        :type  families: :class:`set` of :class:`str` or ``None``
        :param families: Host's family name.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, family name will not be used for image selection Maps to
            "Family" in SMBIOS: System Information (Type 1) and offset 1Ah
        :type  oem_strings: :class:`set` of :class:`str` or ``None``
        :param oem_strings: Host's OEM string.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, oem string will not be used for image selection Maps to
            SMBIOS: OEM Strings (Type 11)
        """
        self.vendor = vendor
        self.models = models
        self.families = families
        self.oem_strings = oem_strings
        VapiStruct.__init__(self)


HostHardwareInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.host_hardware_info', {
        'vendor': type.StringType(),
        'models': type.OptionalType(type.SetType(type.StringType())),
        'families': type.OptionalType(type.SetType(type.StringType())),
        'oem_strings': type.OptionalType(type.SetType(type.StringType())),
    },
    HostHardwareInfo,
    False,
    None))



class ImageSelectionInfo(VapiStruct):
    """
    The ``ImageSelectionInfo`` class contains attributes to describe the
    selection criteria used to select an image for 1 or more hosts
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'selection_type',
            {
                'HOST_UUID' : [('host_uuids', True)],
                'HOST_HARDWARE_SPEC' : [('host_hardware_spec', True)],
            }
        ),
    ]



    def __init__(self,
                 selection_type=None,
                 host_uuids=None,
                 host_hardware_spec=None,
                ):
        """
        :type  selection_type: :class:`ImageSelectionInfo.SelectionType`
        :param selection_type: Specifies what type of selection (HOST_UUID, HOST_HARDWARE_SPEC) is
            to be used for selecting an image for a host. HOST_UUID is intended
            to be used when an image needs to be selected for a host based on
            the host's uuid. Maps to "UUID" in SMBIOS: System Information (Type
            1) and offset 08h HOST_HARDWARE_SPEC is intended to be used when an
            image needs to be selected for 1 or more hosts based on the host's
            hardware specifications like vendor, model, family and oem string.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  host_uuids: :class:`set` of :class:`str`
        :param host_uuids: Specifies the host's uuid for which an image needs to be selected.
            Maps to "UUID" in SMBIOS: System Information (Type 1) and offset
            08h
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``selectionType`` is
            :attr:`ImageSelectionInfo.SelectionType.HOST_UUID`.
        :type  host_hardware_spec: :class:`HostHardwareInfo`
        :param host_hardware_spec: Specifies the host's hardware specification like vendor, model,
            family and oem string for which an image needs to be selected. 
            
            Selection logic will be AND operation across the attributes and OR
            operation within an attribute 
            
            Ex: For vendor = "OEM 1" model = ["Model Gen9", "Model Gen10"]
            family = ["Family 1", "Family 2"] oemString = ["OEM String 1", "OEM
            String 2"] 
            
            Logic will be "OEM 1" AND ("Model Gen9" OR "Model Gen10") AND
            ("Family 1" OR "Family 2") AND ("OEM String 1" OR "OEM String 2")
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``selectionType`` is
            :attr:`ImageSelectionInfo.SelectionType.HOST_HARDWARE_SPEC`.
        """
        self.selection_type = selection_type
        self.host_uuids = host_uuids
        self.host_hardware_spec = host_hardware_spec
        VapiStruct.__init__(self)


    class SelectionType(Enum):
        """
        The ``ImageSelectionInfo.SelectionType`` class contains attributes that
        describe the selection type to be used for selecting an image for a host.
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
        HOST_UUID = None
        """
        Select image using host's uuid.

        """
        HOST_HARDWARE_SPEC = None
        """
        Select image using host's hardware specification. ``HostHardwareInfo``
        class

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SelectionType` instance.
            """
            Enum.__init__(string)

    SelectionType._set_values({
        'HOST_UUID': SelectionType('HOST_UUID'),
        'HOST_HARDWARE_SPEC': SelectionType('HOST_HARDWARE_SPEC'),
    })
    SelectionType._set_binding_type(type.EnumType(
        'com.vmware.esx.hosts.image_selection_info.selection_type',
        SelectionType))

ImageSelectionInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.image_selection_info', {
        'selection_type': type.ReferenceType(__name__, 'ImageSelectionInfo.SelectionType'),
        'host_uuids': type.OptionalType(type.SetType(type.StringType())),
        'host_hardware_spec': type.OptionalType(type.ReferenceType(__name__, 'HostHardwareInfo')),
    },
    ImageSelectionInfo,
    False,
    None))



class AlternativeImageInfo(VapiStruct):
    """
    The ``AlternativeImageInfo`` class contains attributes that describes an
    alternative image for the desired software specification.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 base_image=None,
                 add_on=None,
                 components=None,
                 solutions=None,
                 hardware_support=None,
                 removed_components=None,
                 display_name=None,
                 selection_criteria=None,
                ):
        """
        :type  base_image: :class:`BaseImageInfo`
        :param base_image: Base image of the ESX.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  add_on: :class:`AddOnInfo` or ``None``
        :param add_on: OEM customization on top of given base-image. The components in
            this customization override the components in the base base-image.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no OEM customization exists.
        :type  components: :class:`dict` of :class:`str` and (:class:`ComponentInfo` or ``None``)
        :param components: Map of components in an ESX image. The key is the component name
            and value is the information about specific version of the
            component.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
        :type  solutions: :class:`dict` of :class:`str` and :class:`SolutionInfo`
        :param solutions: Map of software solutions in an ESX image. The key is the solution
            name and value is the specification detailing components registered
            by that solution.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.solution``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.solution``.
        :type  hardware_support: :class:`HardwareSupportInfo` or ``None``
        :param hardware_support: Information about the Hardware Support Packages (HSP) configured.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no Hardware Support Package (HSP) info exists.
        :type  removed_components: (:class:`dict` of :class:`str` and :class:`ComponentInfo`) or ``None``
        :param removed_components: Information about the components to be removed in the software
            specification.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
            If None, no removed component info exists.
        :type  display_name: :class:`str`
        :param display_name: Display name of the Alternative Image. Supported encoding is UTF-8.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  selection_criteria: :class:`ImageSelectionInfo`
        :param selection_criteria: Selection criteria used to select the alternative image for 1 or
            more hosts
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.base_image = base_image
        self.add_on = add_on
        self.components = components
        self.solutions = solutions
        self.hardware_support = hardware_support
        self.removed_components = removed_components
        self.display_name = display_name
        self.selection_criteria = selection_criteria
        VapiStruct.__init__(self)


AlternativeImageInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.alternative_image_info', {
        'base_image': type.ReferenceType(__name__, 'BaseImageInfo'),
        'add_on': type.OptionalType(type.ReferenceType(__name__, 'AddOnInfo')),
        'components': type.MapType(type.IdType(), type.OptionalType(type.ReferenceType(__name__, 'ComponentInfo'))),
        'solutions': type.MapType(type.IdType(), type.ReferenceType(__name__, 'SolutionInfo')),
        'hardware_support': type.OptionalType(type.ReferenceType(__name__, 'HardwareSupportInfo')),
        'removed_components': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'ComponentInfo'))),
        'display_name': type.StringType(),
        'selection_criteria': type.ReferenceType(__name__, 'ImageSelectionInfo'),
    },
    AlternativeImageInfo,
    False,
    None))



class SoftwareInfo(VapiStruct):
    """
    The ``SoftwareInfo`` class contains attributes that describes the software
    solution for an ESX host.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 base_image=None,
                 add_on=None,
                 components=None,
                 solutions=None,
                 hardware_support=None,
                 removed_components=None,
                 alternative_images=None,
                ):
        """
        :type  base_image: :class:`BaseImageInfo`
        :param base_image: Base image of the ESX.
        :type  add_on: :class:`AddOnInfo` or ``None``
        :param add_on: OEM customization on top of given base-image. The components in
            this customization override the components in the base base-image.
            If None, no OEM customization exists.
        :type  components: :class:`dict` of :class:`str` and (:class:`ComponentInfo` or ``None``)
        :param components: Map of components in an ESX image. The key is the component name
            and value is the information about specific version of the
            component.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
        :type  solutions: :class:`dict` of :class:`str` and :class:`SolutionInfo`
        :param solutions: Map of software solutions in an ESX image. The key is the solution
            name and value is the specification detailing components registered
            by that solution.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.solution``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.solution``.
        :type  hardware_support: :class:`HardwareSupportInfo` or ``None``
        :param hardware_support: Information about the Hardware Support Packages (HSP) configured.
            This attribute was added in **vSphere API 7.0.2.0**.
            If None, no Hardware Support Package (HSP) info exists.
        :type  removed_components: :class:`dict` of :class:`str` and :class:`ComponentInfo`
        :param removed_components: Information about the components to be removed in the software
            specification.
            This attribute was added in **vSphere API 8.0.3.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
            This attribute is optional because it was added in a newer version
            than its parent node.
        :type  alternative_images: (:class:`dict` of :class:`str` and :class:`AlternativeImageInfo`) or ``None``
        :param alternative_images: Alternative Images apart from the Default Image
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.settings.image``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
            If None, no alternative image will be part of the software
            specification. Image ID supports only the following ASCII
            characters [a-z][A-Z][0-9][-] Case will be ignored when comparing
            identifiers "IMAGE-1" is equal to "image-1"
        """
        self.base_image = base_image
        self.add_on = add_on
        self.components = components
        self.solutions = solutions
        self.hardware_support = hardware_support
        self.removed_components = removed_components
        self.alternative_images = alternative_images
        VapiStruct.__init__(self)


SoftwareInfo._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.software_info', {
        'base_image': type.ReferenceType(__name__, 'BaseImageInfo'),
        'add_on': type.OptionalType(type.ReferenceType(__name__, 'AddOnInfo')),
        'components': type.MapType(type.IdType(), type.OptionalType(type.ReferenceType(__name__, 'ComponentInfo'))),
        'solutions': type.MapType(type.IdType(), type.ReferenceType(__name__, 'SolutionInfo')),
        'hardware_support': type.OptionalType(type.ReferenceType(__name__, 'HardwareSupportInfo')),
        'removed_components': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'ComponentInfo'))),
        'alternative_images': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'AlternativeImageInfo'))),
    },
    SoftwareInfo,
    False,
    None))



class SolutionComponentSpec(VapiStruct):
    """
    The ``SolutionComponentSpec`` class contains attributes that describe a
    component registered by a software solution.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 component=None,
                ):
        """
        :type  component: :class:`str`
        :param component: Identifier of the component.
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``. When methods return a value of
            this class as a return value, the attribute will be an identifier
            for the resource type: ``com.vmware.esx.hosts.component``.
        """
        self.component = component
        VapiStruct.__init__(self)


SolutionComponentSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.solution_component_spec', {
        'component': type.IdType(resource_types='com.vmware.esx.hosts.component'),
    },
    SolutionComponentSpec,
    False,
    None))



class SolutionSpec(VapiStruct):
    """
    The ``SolutionSpec`` class contains attributes that describe solution
    registered in the software specification.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                 components=None,
                ):
        """
        :type  version: :class:`str`
        :param version: Version of the solution.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  components: :class:`list` of :class:`SolutionComponentSpec`
        :param components: Components registered by the solution.
            This attribute was added in **vSphere API 7.0.2.0**.
        """
        self.version = version
        self.components = components
        VapiStruct.__init__(self)


SolutionSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.solution_spec', {
        'version': type.StringType(),
        'components': type.ListType(type.ReferenceType(__name__, 'SolutionComponentSpec')),
    },
    SolutionSpec,
    False,
    None))



class BaseImageSpec(VapiStruct):
    """
    The ``BaseImageSpec`` class contains attributes that describe a specific
    ESX base-image in the software specification.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 version=None,
                ):
        """
        :type  version: :class:`str`
        :param version: Version of the base-image
            This attribute was added in **vSphere API 7.0.2.0**.
        """
        self.version = version
        VapiStruct.__init__(self)


BaseImageSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.base_image_spec', {
        'version': type.StringType(),
    },
    BaseImageSpec,
    False,
    None))



class AddOnSpec(VapiStruct):
    """
    The ``AddOnSpec`` class contains attributes that describe a specific OEM
    customization add-on in the software specification.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 version=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the add-on
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  version: :class:`str`
        :param version: Version of the add-on
            This attribute was added in **vSphere API 7.0.2.0**.
        """
        self.name = name
        self.version = version
        VapiStruct.__init__(self)


AddOnSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.add_on_spec', {
        'name': type.StringType(),
        'version': type.StringType(),
    },
    AddOnSpec,
    False,
    None))



class HardwareSupportPackageSpec(VapiStruct):
    """
    The ``HardwareSupportPackageSpec`` class contains attributes to describe
    the Hardware Support Package (HSP) configured for a single device or
    distinct group of devices (typically the OEM's, including BIOS, device
    firmware and OEM-supplied driver or agent components).
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 pkg=None,
                 version=None,
                ):
        """
        :type  pkg: :class:`str` or ``None``
        :param pkg: Hardware Support Package (HSP) selected
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.esx.hosts.hardware_support.package``. When methods
            return a value of this class as a return value, the attribute will
            be an identifier for the resource type:
            ``com.vmware.esx.hosts.hardware_support.package``.
        :type  version: :class:`str` or ``None``
        :param version: Version of the Hardware Support Package (HSP) selected (e.g.
            "20180128.1" or "v42")
            This attribute was added in **vSphere API 7.0.2.0**.
            If None, the system will use an empty string as the version.
        """
        self.pkg = pkg
        self.version = version
        VapiStruct.__init__(self)


HardwareSupportPackageSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.hardware_support_package_spec', {
        'pkg': type.OptionalType(type.IdType()),
        'version': type.OptionalType(type.StringType()),
    },
    HardwareSupportPackageSpec,
    False,
    None))



class HardwareSupportSpec(VapiStruct):
    """
    The ``HardwareSupportSpec`` class contains attributes to describe the
    Hardware Support Packages (HSP) included in the software specification.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 packages=None,
                ):
        """
        :type  packages: :class:`dict` of :class:`str` and :class:`HardwareSupportPackageSpec`
        :param packages: Map of Hardware Support Packages (HSPs). The key is the Hardware
            Support Manager (HSM) name and the value is the specification
            detailing the HSP configured for that HSM.
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.hardware_support.manager``. When
            methods return a value of this class as a return value, the key in
            the attribute :class:`dict` will be an identifier for the resource
            type: ``com.vmware.esx.hosts.hardware_support.manager``.
        """
        self.packages = packages
        VapiStruct.__init__(self)


HardwareSupportSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.hardware_support_spec', {
        'packages': type.MapType(type.IdType(), type.ReferenceType(__name__, 'HardwareSupportPackageSpec')),
    },
    HardwareSupportSpec,
    False,
    None))



class HostHardwareSpec(VapiStruct):
    """
    The ``HostHardwareSpec`` class contains attributes to describe the host's
    hardware specifications like vendor, model, family and oem string.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vendor=None,
                 models=None,
                 families=None,
                 oem_strings=None,
                ):
        """
        :type  vendor: :class:`str`
        :param vendor: Host's vendor name. Maps to "Manufacturer" in SMBIOS: System
            Information (Type 1) and offset 04h
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  models: :class:`set` of :class:`str` or ``None``
        :param models: Host's model name.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, model name will not be used for image selection Maps to
            "Product Name" in SMBIOS: System Information (Type 1) and offset
            05h
        :type  families: :class:`set` of :class:`str` or ``None``
        :param families: Host's family name.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, family name will not be used for image selection Maps to
            "Family" in SMBIOS: System Information (Type 1) and offset 1Ah
        :type  oem_strings: :class:`set` of :class:`str` or ``None``
        :param oem_strings: Host's OEM string.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, oem string will not be used for image selection Maps to
            SMBIOS: OEM Strings (Type 11)
        """
        self.vendor = vendor
        self.models = models
        self.families = families
        self.oem_strings = oem_strings
        VapiStruct.__init__(self)


HostHardwareSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.host_hardware_spec', {
        'vendor': type.StringType(),
        'models': type.OptionalType(type.SetType(type.StringType())),
        'families': type.OptionalType(type.SetType(type.StringType())),
        'oem_strings': type.OptionalType(type.SetType(type.StringType())),
    },
    HostHardwareSpec,
    False,
    None))



class ImageSelectionSpec(VapiStruct):
    """
    The ``ImageSelectionSpec`` class contains attributes to describe the
    selection criteria used to select an image for 1 or more hosts
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'selection_type',
            {
                'HOST_UUID' : [('host_uuids', True)],
                'HOST_HARDWARE_SPEC' : [('host_hardware_spec', True)],
            }
        ),
    ]



    def __init__(self,
                 selection_type=None,
                 host_uuids=None,
                 host_hardware_spec=None,
                ):
        """
        :type  selection_type: :class:`ImageSelectionSpec.SelectionType`
        :param selection_type: Specifies what type of selection (HOST_UUID, HOST_HARDWARE_SPEC) is
            to be used for selecting an image for a host. HOST_UUID is intended
            to be used when an image needs to be selected for a host based on
            the host's uuid. Maps to "UUID" in SMBIOS: System Information (Type
            1) and offset 08h HOST_HARDWARE_SPEC is intended to be used when an
            image needs to be selected for 1 or more hosts based on the host's
            hardware specifications like vendor, model, family and oem string.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  host_uuids: :class:`set` of :class:`str`
        :param host_uuids: Specifies the host's uuid for which an image needs to be selected.
            Maps to "UUID" in SMBIOS: System Information (Type 1) and offset
            08h
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``selectionType`` is
            :attr:`ImageSelectionSpec.SelectionType.HOST_UUID`.
        :type  host_hardware_spec: :class:`HostHardwareSpec`
        :param host_hardware_spec: Specifies the host's hardware specification like vendor, model,
            family and oem string for which an image needs to be selected. 
            
            Selection logic will be AND operation across the attributes and OR
            operation within an attribute 
            
            Ex: For vendor = "OEM 1" model = ["Model Gen9", "Model Gen10"]
            family = ["Family 1", "Family 2"] oemString = ["OEM String 1", "OEM
            String 2"] 
            
            Logic will be "OEM 1" AND ("Model Gen9" OR "Model Gen10") AND
            ("Family 1" OR "Family 2") AND ("OEM String 1" OR "OEM String 2")
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``selectionType`` is
            :attr:`ImageSelectionSpec.SelectionType.HOST_HARDWARE_SPEC`.
        """
        self.selection_type = selection_type
        self.host_uuids = host_uuids
        self.host_hardware_spec = host_hardware_spec
        VapiStruct.__init__(self)


    class SelectionType(Enum):
        """
        The ``ImageSelectionSpec.SelectionType`` class contains attributes that
        describe the selection type to be used for selecting an image for a host.
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
        HOST_UUID = None
        """
        Select image using host's uuid.

        """
        HOST_HARDWARE_SPEC = None
        """
        Select image using host's hardware specification. ``HostHardwareSpec``
        class

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SelectionType` instance.
            """
            Enum.__init__(string)

    SelectionType._set_values({
        'HOST_UUID': SelectionType('HOST_UUID'),
        'HOST_HARDWARE_SPEC': SelectionType('HOST_HARDWARE_SPEC'),
    })
    SelectionType._set_binding_type(type.EnumType(
        'com.vmware.esx.hosts.image_selection_spec.selection_type',
        SelectionType))

ImageSelectionSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.image_selection_spec', {
        'selection_type': type.ReferenceType(__name__, 'ImageSelectionSpec.SelectionType'),
        'host_uuids': type.OptionalType(type.SetType(type.StringType())),
        'host_hardware_spec': type.OptionalType(type.ReferenceType(__name__, 'HostHardwareSpec')),
    },
    ImageSelectionSpec,
    False,
    None))



class AlternativeImageSpec(VapiStruct):
    """
    The ``AlternativeImageSpec`` class contains attributes that describes an
    alternative image for the desired software specification.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 base_image=None,
                 add_on=None,
                 components=None,
                 solutions=None,
                 hardware_support=None,
                 removed_components=None,
                 display_name=None,
                 selection_criteria=None,
                ):
        """
        :type  base_image: :class:`BaseImageSpec`
        :param base_image: Base image of the ESX.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  add_on: :class:`AddOnSpec` or ``None``
        :param add_on: OEM customization on top of given base-image. The components in
            this customization override the components in the base base-image.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no OEM customization will be applied.
        :type  components: (:class:`dict` of :class:`str` and (:class:`str` or ``None``)) or ``None``
        :param components: Additional components which are part of the software specification.
            If value is not given for a particular component then version for
            that component will be picked from the constraints. These override
            the components present in :attr:`AlternativeImageSpec.add_on` and
            :attr:`AlternativeImageSpec.base_image`.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
            If None, no additional components are present in the software
            specification.
        :type  solutions: (:class:`dict` of :class:`str` and :class:`SolutionSpec`) or ``None``
        :param solutions: Mapping from solution identifier to the solution specification. The
            key is the solution name and the value is the specification
            detailing components registered by that solution.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.solution``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.solution``.
            If None, no solutions are present in the software specification.
        :type  hardware_support: :class:`HardwareSupportSpec` or ``None``
        :param hardware_support: Information about the Hardware Support Package (HSP) configured in
            the software specification.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None or empty, no firmware info will be part of the software
            specification.
        :type  removed_components: :class:`set` of :class:`str` or ``None``
        :param removed_components: Components to be removed from the software specification.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.esx.hosts.component``. When methods return a value of
            this class as a return value, the attribute will contain
            identifiers for the resource type:
            ``com.vmware.esx.hosts.component``.
            If None no component will be removed.
        :type  display_name: :class:`str`
        :param display_name: Display name of the Alternative Image. Supported encoding is UTF-8.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  selection_criteria: :class:`ImageSelectionSpec`
        :param selection_criteria: Selection criteria used to select the alternative image for 1 or
            more hosts
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.base_image = base_image
        self.add_on = add_on
        self.components = components
        self.solutions = solutions
        self.hardware_support = hardware_support
        self.removed_components = removed_components
        self.display_name = display_name
        self.selection_criteria = selection_criteria
        VapiStruct.__init__(self)


AlternativeImageSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.alternative_image_spec', {
        'base_image': type.ReferenceType(__name__, 'BaseImageSpec'),
        'add_on': type.OptionalType(type.ReferenceType(__name__, 'AddOnSpec')),
        'components': type.OptionalType(type.MapType(type.IdType(), type.OptionalType(type.StringType()))),
        'solutions': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'SolutionSpec'))),
        'hardware_support': type.OptionalType(type.ReferenceType(__name__, 'HardwareSupportSpec')),
        'removed_components': type.OptionalType(type.SetType(type.IdType())),
        'display_name': type.StringType(),
        'selection_criteria': type.ReferenceType(__name__, 'ImageSelectionSpec'),
    },
    AlternativeImageSpec,
    False,
    None))



class SoftwareSpec(VapiStruct):
    """
    The ``SoftwareSpec`` class contains attributes that describe software
    specification for an ESX host.
    This class was added in **vSphere API 7.0.2.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 base_image=None,
                 add_on=None,
                 components=None,
                 solutions=None,
                 hardware_support=None,
                 removed_components=None,
                 alternative_images=None,
                ):
        """
        :type  base_image: :class:`BaseImageSpec`
        :param base_image: Base image of the ESX.
            This attribute was added in **vSphere API 7.0.2.0**.
        :type  add_on: :class:`AddOnSpec` or ``None``
        :param add_on: OEM customization on top of given base-image. The components in
            this customization override the components in the base base-image.
            This attribute was added in **vSphere API 7.0.2.0**.
            If None, no OEM customization will be applied.
        :type  components: (:class:`dict` of :class:`str` and (:class:`str` or ``None``)) or ``None``
        :param components: Additional components which are part of the software specification.
            If value is not given for a particular component then version for
            that component will be picked from the constraints. These override
            the components present in :attr:`SoftwareSpec.add_on` and
            :attr:`SoftwareSpec.base_image`.
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.component``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.component``.
            If None, no additional components are present in the software
            specification.
        :type  solutions: (:class:`dict` of :class:`str` and :class:`SolutionSpec`) or ``None``
        :param solutions: Mapping from solution identifier to the solution specification. The
            key is the solution name and the value is the specification
            detailing components registered by that solution.
            This attribute was added in **vSphere API 7.0.2.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.hosts.solution``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.hosts.solution``.
            If None, no solutions are present in the software specification.
        :type  hardware_support: :class:`HardwareSupportSpec` or ``None``
        :param hardware_support: Information about the Hardware Support Package (HSP) configured in
            the software specification.
            This attribute was added in **vSphere API 7.0.2.0**.
            If None or empty, no firmware info will be part of the software
            specification.
        :type  removed_components: :class:`set` of :class:`str` or ``None``
        :param removed_components: Components to be removed from the software specification.
            This attribute was added in **vSphere API 8.0.3.0**.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.esx.hosts.component``. When methods return a value of
            this class as a return value, the attribute will contain
            identifiers for the resource type:
            ``com.vmware.esx.hosts.component``.
            If None no component will be removed.
        :type  alternative_images: (:class:`dict` of :class:`str` and :class:`AlternativeImageSpec`) or ``None``
        :param alternative_images: Alternative Images apart from the Default Image
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the key in
            the attribute :class:`dict` must be an identifier for the resource
            type: ``com.vmware.esx.settings.image``. When methods return a
            value of this class as a return value, the key in the attribute
            :class:`dict` will be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
            If None, no alternative image will be part of the software
            specification. Image ID supports only the following ASCII
            characters [a-z][A-Z][0-9][-] Case will be ignored when comparing
            identifiers "IMAGE-1" is equal to "image-1"
        """
        self.base_image = base_image
        self.add_on = add_on
        self.components = components
        self.solutions = solutions
        self.hardware_support = hardware_support
        self.removed_components = removed_components
        self.alternative_images = alternative_images
        VapiStruct.__init__(self)


SoftwareSpec._set_binding_type(type.StructType(
    'com.vmware.esx.hosts.software_spec', {
        'base_image': type.ReferenceType(__name__, 'BaseImageSpec'),
        'add_on': type.OptionalType(type.ReferenceType(__name__, 'AddOnSpec')),
        'components': type.OptionalType(type.MapType(type.IdType(), type.OptionalType(type.StringType()))),
        'solutions': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'SolutionSpec'))),
        'hardware_support': type.OptionalType(type.ReferenceType(__name__, 'HardwareSupportSpec')),
        'removed_components': type.OptionalType(type.SetType(type.IdType())),
        'alternative_images': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'AlternativeImageSpec'))),
    },
    SoftwareSpec,
    False,
    None))



class Software(VapiInterface):
    """
    The ``Software`` class provides methods to get and extract the current
    software specification applied to the host.
    This class was added in **vSphere API 7.0.2.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.hosts.software'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SoftwareStub)
        self._VAPI_OPERATION_IDS = {}

    class HostCredentials(VapiStruct):
        """
        The ``Software.HostCredentials`` class contains attributes that describe
        the host's username, password, port number, ssl thumbprint or ssl
        certificate to be used when connecting to the host using USERNAME_PASSWORD
        option in the ``AuthenticationType`` class.
        This class was added in **vSphere API 7.0.2.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host_name=None,
                     user_name=None,
                     password=None,
                     port=None,
                     ssl_thumb_print=None,
                     ssl_certificate=None,
                    ):
            """
            :type  host_name: :class:`str`
            :param host_name: The IP address or DNS resolvable name of the host.
                This attribute was added in **vSphere API 7.0.2.0**.
            :type  user_name: :class:`str`
            :param user_name: Specifies the username to be used during the :func:`Software.get`
                method
                This attribute was added in **vSphere API 7.0.2.0**.
            :type  password: :class:`str`
            :param password: Specifies the password to be used during the :func:`Software.get`
                method
                This attribute was added in **vSphere API 7.0.2.0**.
            :type  port: :class:`long` or ``None``
            :param port: Specifies the port number of the host to be used during
                :func:`Software.get` method
                This attribute was added in **vSphere API 7.0.2.0**.
                If None, port number is set to 443.
            :type  ssl_thumb_print: :class:`str` or ``None``
            :param ssl_thumb_print: Specifies the sslThumbPrint of the host to be used during
                :func:`Software.get` method SHA1 hash of the host's SSL
                certificate.
                This attribute was added in **vSphere API 7.0.2.0**.
                If specified and the server presents that thumbprint, the
                connection will be established; if None, the connection will only
                proceed if the server-presented certificate can be validated by
                specified *sslCertificate*.

                .. deprecated:: vSphere API 9.0.0.0
                    This attribute is deprecated as of **vSphere API 9.0.0.0**.
                    This field is deprecated and will be removed in future
                    versions. Please use the 'ssl_certificate' field instead.
            :type  ssl_certificate: :class:`str` or ``None``
            :param ssl_certificate: Specifies the sslCertificate of the host to be used during
                :func:`Software.get` method PEM format of the host's SSL
                certificate.
                This attribute was added in **vSphere API 9.0.0.0**.
                If specified and the server presents that certificate, the
                connection will be established; if None, the connection will only
                proceed if the server-presented thumbprint can be validated by
                specified *sslThumbprint*. Note: *sslThumbprint* and
                *sslCertificate* parameters are mutually exclusive, and should
                never be used simultaneously. If both are set, this operation will
                throw InvalidArgument exception.
            """
            self.host_name = host_name
            self.user_name = user_name
            self.password = password
            self.port = port
            self.ssl_thumb_print = ssl_thumb_print
            self.ssl_certificate = ssl_certificate
            VapiStruct.__init__(self)


    HostCredentials._set_binding_type(type.StructType(
        'com.vmware.esx.hosts.software.host_credentials', {
            'host_name': type.StringType(),
            'user_name': type.StringType(),
            'password': type.SecretType(),
            'port': type.OptionalType(type.IntegerType()),
            'ssl_thumb_print': type.OptionalType(type.StringType()),
            'ssl_certificate': type.OptionalType(type.StringType()),
        },
        HostCredentials,
        False,
        None))


    class ConnectionSpec(VapiStruct):
        """
        The ``Software.ConnectionSpec`` class contains attributes that describe the
        specification to be used for connecting to the host during the
        :func:`Software.get` method
        This class was added in **vSphere API 7.0.2.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'auth_type',
                {
                    'USERNAME_PASSWORD' : [('host_credential', True)],
                    'EXISTING' : [('host', True)],
                }
            ),
        ]



        def __init__(self,
                     auth_type=None,
                     host_credential=None,
                     host=None,
                    ):
            """
            :type  auth_type: :class:`Software.ConnectionSpec.AuthenticationType`
            :param auth_type: Specifies what type of authentication (USERNAME_PASSWORD, EXISTING)
                is to be used when connecting with the host. USERNAME_PASSWORD is
                intended to be used when connecting to a host that is not currently
                part of the vCenter inventory. EXISTING is intented for hosts that
                are in vCenter inventory, in which case, HostServiceTicket will be
                used to connect to the host.
                This attribute was added in **vSphere API 7.0.2.0**.
            :type  host_credential: :class:`Software.HostCredentials`
            :param host_credential: Specifies the host details to be used during the
                :func:`Software.get` method
                This attribute was added in **vSphere API 7.0.2.0**.
                This attribute is optional and it is only relevant when the value
                of ``authType`` is
                :attr:`Software.ConnectionSpec.AuthenticationType.USERNAME_PASSWORD`.
            :type  host: :class:`str`
            :param host: Specifies the host Managed Object ID to be used during the
                :func:`Software.get` method
                This attribute was added in **vSphere API 7.0.2.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                This attribute is optional and it is only relevant when the value
                of ``authType`` is
                :attr:`Software.ConnectionSpec.AuthenticationType.EXISTING`.
            """
            self.auth_type = auth_type
            self.host_credential = host_credential
            self.host = host
            VapiStruct.__init__(self)


        class AuthenticationType(Enum):
            """
            The ``Software.ConnectionSpec.AuthenticationType`` class defines the
            possible types of authentication supported when connecting to the host.
            This enumeration was added in **vSphere API 7.0.2.0**.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            USERNAME_PASSWORD = None
            """
            Connect to host using host's credentials ``HostCredentials`` class.

            """
            EXISTING = None
            """
            Connect to the host using service ticket. Note: This is supported only for
            hosts present in the VC inventory.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`AuthenticationType` instance.
                """
                Enum.__init__(string)

        AuthenticationType._set_values({
            'USERNAME_PASSWORD': AuthenticationType('USERNAME_PASSWORD'),
            'EXISTING': AuthenticationType('EXISTING'),
        })
        AuthenticationType._set_binding_type(type.EnumType(
            'com.vmware.esx.hosts.software.connection_spec.authentication_type',
            AuthenticationType))

    ConnectionSpec._set_binding_type(type.StructType(
        'com.vmware.esx.hosts.software.connection_spec', {
            'auth_type': type.ReferenceType(__name__, 'Software.ConnectionSpec.AuthenticationType'),
            'host_credential': type.OptionalType(type.ReferenceType(__name__, 'Software.HostCredentials')),
            'host': type.OptionalType(type.IdType()),
        },
        ConnectionSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Software.Info`` class contains attributes that describe the current
        software information on a host.
        This class was added in **vSphere API 7.0.2.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                     software_info=None,
                    ):
            """
            :type  notifications: :class:`Notifications`
            :param notifications: Notifications returned by the get operation.
                This attribute was added in **vSphere API 7.0.2.0**.
            :type  software_info: :class:`SoftwareInfo`
            :param software_info: Host software information returned by the get operation.
                This attribute was added in **vSphere API 7.0.2.0**.
            """
            self.notifications = notifications
            self.software_info = software_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.hosts.software.info', {
            'notifications': type.ReferenceType(__name__, 'Notifications'),
            'software_info': type.ReferenceType(__name__, 'SoftwareInfo'),
        },
        Info,
        False,
        None))



    def get(self,
            spec,
            ):
        """
        Returns details about the current software specification applied to the
        host.
        This method was added in **vSphere API 7.0.2.0**.

        :type  spec: :class:`Software.ConnectionSpec`
        :param spec: ConnectionSpec connection spec for the host.
        :rtype: :class:`Software.Info`
        :return: Info details about the current software specification applied to
            the host.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``ConnectionSpec.HostCredentials`` attribute of ``spec`` is
            invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no ``ConnectionSpec.HostCredentials#hostName``
            attribute associated with host id in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If the SSL certificate of the target node cannot be validated by
            comparing with the thumbprint provided in
            ConnectionSpec.HostCredentials#sslThumbPrint or the full
            certificate provided in
            ConnectionSpec.HostCredentials#sslCertificate. The value of the
            {\\\\@link UnverifiedPeer#data) {\\\\@term field} will be a
            {\\\\@term structure} that contains the {\\\\@term fields} defined
            in {\\\\@link com.vmware.esx.hosts.CertificateInfo}.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'spec': spec,
                            })
class _SoftwareStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Software.ConnectionSpec'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/software',
            request_body_parameter='spec',
            path_variables={
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
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Software.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.hosts.software',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Software': Software,
        'software': 'com.vmware.esx.hosts.software_client.StubFactory',
    }

