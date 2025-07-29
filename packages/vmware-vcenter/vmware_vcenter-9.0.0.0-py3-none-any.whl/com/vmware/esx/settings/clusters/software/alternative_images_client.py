# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.clusters.software.alternative_images.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.clusters.software.alternative_images_client``
module provides classes to manage alternative images for the cluster.

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


class DisplayName(VapiInterface):
    """
    The ``DisplayName`` class provides methods to manage the display name of
    the alternative image.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.image"
    """
    Resource type for image resource

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.software.alternative_images.display_name'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DisplayNameStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``DisplayName.Info`` class contains information about the display name
        of an alternative image.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                    ):
            """
            :type  display_name: :class:`str`
            :param display_name: Display name of the alternative image.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.display_name = display_name
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.alternative_images.display_name.info', {
            'display_name': type.StringType(),
        },
        Info,
        False,
        None))



    def get(self,
            cluster,
            image,
            ):
        """
        Returns the display name of the alternative image.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  image: :class:`str`
        :param image: Identifier of the alternative image.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
        :rtype: :class:`DisplayName.Info`
        :return: Display name of the alternative image.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or no image
            associated with ``image`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            'image': image,
                            })
class SelectionCriteria(VapiInterface):
    """
    The ``SelectionCriteria`` class provides methods to manage the selection
    criteria of the alternative image.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.image"
    """
    Resource type for image resource

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.software.alternative_images.selection_criteria'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SelectionCriteriaStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self,
            cluster,
            image,
            ):
        """
        Returns the selection criteria of the alternative image.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: The cluster identifier.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  image: :class:`str`
        :param image: Identifier of the alternative image.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
        :rtype: :class:`com.vmware.esx.settings_client.ImageSelectionInfo`
        :return: Selection criteria of the alternative image.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or no draft
            associated with ``image`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            'image': image,
                            })
class Software(VapiInterface):
    """
    The ``Software`` class provides methods to manage the desired software
    specification of the alternative image.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.image"
    """
    Resource type for image resource

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.clusters.software.alternative_images.software'
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

    class ExportType(Enum):
        """
        The ``Software.ExportType`` class defines the formats in which software
        specification document or image can be exported.
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
        SOFTWARE_SPEC = None
        """
        Export software specification document.

        """
        ISO_IMAGE = None
        """
        Export ISO image.

        """
        OFFLINE_BUNDLE = None
        """
        Export offline bundle.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ExportType` instance.
            """
            Enum.__init__(string)

    ExportType._set_values({
        'SOFTWARE_SPEC': ExportType('SOFTWARE_SPEC'),
        'ISO_IMAGE': ExportType('ISO_IMAGE'),
        'OFFLINE_BUNDLE': ExportType('OFFLINE_BUNDLE'),
    })
    ExportType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.clusters.software.alternative_images.software.export_type',
        ExportType))


    class ExportSpec(VapiStruct):
        """
        The ``Software.ExportSpec`` class contains information describing how a
        software specification or image should be exported.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     export_software_spec=None,
                     export_iso_image=None,
                     export_offline_bundle=None,
                    ):
            """
            :type  export_software_spec: :class:`bool`
            :param export_software_spec: Whether to export software specification document.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  export_iso_image: :class:`bool`
            :param export_iso_image: Whether to export ISO image.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  export_offline_bundle: :class:`bool`
            :param export_offline_bundle: Whether to export offline bundle.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.export_software_spec = export_software_spec
            self.export_iso_image = export_iso_image
            self.export_offline_bundle = export_offline_bundle
            VapiStruct.__init__(self)


    ExportSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.clusters.software.alternative_images.software.export_spec', {
            'export_software_spec': type.BooleanType(),
            'export_iso_image': type.BooleanType(),
            'export_offline_bundle': type.BooleanType(),
        },
        ExportSpec,
        False,
        None))



    def export(self,
               cluster,
               image,
               spec,
               ):
        """
        Exports the desired software specification document and/or offline
        bundle and/or iso for the given alternative image. 
        
        This API will not export the solution section of the desired software
        specification.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  image: :class:`str`
        :param image: Identifier of the alternative image.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
        :type  spec: :class:`Software.ExportSpec`
        :param spec: The export specification to specify data types to be exported.
        :rtype: :class:`dict` of :class:`Software.ExportType` and :class:`str`
        :return: A map from export type to URL of the exported data for that type.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is am unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system or
            if desired software document is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('export',
                            {
                            'cluster': cluster,
                            'image': image,
                            'spec': spec,
                            })
class _DisplayNameStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'image': type.IdType(resource_types='com.vmware.esx.settings.image'),
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

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/software/alternative-images/{image}/display-name',
            path_variables={
                'cluster': 'cluster',
                'image': 'image',
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
                'output_type': type.ReferenceType(__name__, 'DisplayName.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.software.alternative_images.display_name',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SelectionCriteriaStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'image': type.IdType(resource_types='com.vmware.esx.settings.image'),
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

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/clusters/{cluster}/software/alternative-images/{image}/selection-criteria',
            path_variables={
                'cluster': 'cluster',
                'image': 'image',
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
                'output_type': type.ReferenceType('com.vmware.esx.settings_client', 'ImageSelectionInfo'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.software.alternative_images.selection_criteria',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SoftwareStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for export operation
        export_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'image': type.IdType(resource_types='com.vmware.esx.settings.image'),
            'spec': type.ReferenceType(__name__, 'Software.ExportSpec'),
        })
        export_error_dict = {
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

        }
        export_input_value_validator_list = [
        ]
        export_output_validator_list = [
        ]
        export_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/clusters/{cluster}/software/alternative-images/{image}/software?action=export',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'image': 'image',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'export',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'export': {
                'input_type': export_input_type,
                'output_type': type.MapType(type.ReferenceType(__name__, 'Software.ExportType'), type.URIType()),
                'errors': export_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': export_input_value_validator_list,
                'output_validator_list': export_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'export': export_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.clusters.software.alternative_images.software',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'DisplayName': DisplayName,
        'SelectionCriteria': SelectionCriteria,
        'Software': Software,
        'software': 'com.vmware.esx.settings.clusters.software.alternative_images.software_client.StubFactory',
    }

