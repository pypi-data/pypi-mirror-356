# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.repository.software.alternative_images.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.repository.software.alternative_images_client``
module provides classes to manage desired state software in the repository.

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


class EffectiveComponents(VapiInterface):
    """
    The ``EffectiveComponents`` class provides methods to get effective list of
    components.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.repository.software.alternative_images.effective_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EffectiveComponentsStub)
        self._VAPI_OPERATION_IDS = {}

    class FilterSpec(VapiStruct):
        """
        The ``EffectiveComponents.FilterSpec`` class contains the filtering
        specification for :func:`EffectiveComponents.list` operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     with_removed_components=None,
                    ):
            """
            :type  with_removed_components: :class:`bool` or ``None``
            :param with_removed_components: Whether include removed components in the result.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None removed components are not included.
            """
            self.with_removed_components = with_removed_components
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.alternative_images.effective_components.filter_spec', {
            'with_removed_components': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             software_spec,
             image,
             spec=None,
             ):
        """
        Returns the components that comprise the desired software state.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: The identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  image: :class:`str`
        :param image: Identifier of the alternative image.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.image``.
        :type  spec: :class:`EffectiveComponents.FilterSpec` or ``None``
        :param spec: Filter spec to indicate whether removed components are included.
            If None, removed components are not included.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.EffectiveComponentInfo`
        :return: Map of effective components keyed by their identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'software_spec': software_spec,
                            'image': image,
                            'spec': spec,
                            })
class _EffectiveComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'image': type.IdType(resource_types='com.vmware.esx.settings.image'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'EffectiveComponents.FilterSpec')),
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

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/repository/software/{softwareSpec}/alternative-images/{image}/effective-components',
            path_variables={
                'software_spec': 'softwareSpec',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'EffectiveComponentInfo')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.repository.software.alternative_images.effective_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'EffectiveComponents': EffectiveComponents,
    }

