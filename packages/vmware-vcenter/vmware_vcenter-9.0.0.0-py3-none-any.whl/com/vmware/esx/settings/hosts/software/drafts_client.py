# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.hosts.software.drafts.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.hosts.software.drafts_client`` module provides
classes to manage software drafts for ESX host.

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
    The ``DisplayName`` class provides methods to manage the display name in a
    host draft.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.hosts.software.drafts.display_name'
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
        of a software specification.
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
            :param display_name: Display name of the software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.display_name = display_name
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hosts.software.drafts.display_name.info', {
            'display_name': type.StringType(),
        },
        Info,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``DisplayName.SetSpec`` class contains information about the display
        name of a software specification.
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
            :param display_name: Display name of the software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.display_name = display_name
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.hosts.software.drafts.display_name.set_spec', {
            'display_name': type.StringType(),
        },
        SetSpec,
        False,
        None))



    def get(self,
            host,
            draft,
            ):
        """
        Returns the display name of the software draft.
        This method was added in **vSphere API 9.0.0.0**.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the software draft.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`DisplayName.Info`
        :return: display name of the Software Draft.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standalone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'host': host,
                            'draft': draft,
                            })

    def set(self,
            host,
            draft,
            spec,
            ):
        """
        Sets a new display name in the software draft. It will overwrite the
        existing name if one already exists.
        This method was added in **vSphere API 9.0.0.0**.

        :type  host: :class:`str`
        :param host: Identifier of the host.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :type  draft: :class:`str`
        :param draft: Identifier of the working copy document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  spec: :class:`DisplayName.SetSpec`
        :param spec: Display name specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no host associated with ``host`` or no draft associated
            with ``draft`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the host is not a vLCM managed standalone host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
            * The resource ``HostSystem`` referenced by the parameter ``host``
              requires ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('set',
                            {
                            'host': host,
                            'draft': draft,
                            'spec': spec,
                            })
class _DisplayNameStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
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
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/display-name',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
            'host': type.IdType(resource_types='HostSystem'),
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'spec': type.ReferenceType(__name__, 'DisplayName.SetSpec'),
        })
        set_error_dict = {
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
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/esx/settings/hosts/{host}/software/drafts/{draft}/display-name',
            request_body_parameter='spec',
            path_variables={
                'host': 'host',
                'draft': 'draft',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.hosts.software.drafts.display_name',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'DisplayName': DisplayName,
        'software': 'com.vmware.esx.settings.hosts.software.drafts.software_client.StubFactory',
    }

