# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.lifecycle.content.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.lifecycle.content_client`` module
provides classes to configure vSphere Namespaces with content libraries that
contain Supervisor images used during Supervisor Asynchronous upgrades and
enablement workflows.

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


class Libraries(VapiInterface):
    """
    The ``Libraries`` class provides methods to configure vSphere Namespaces
    with Content Library containing Supervisor images used during the
    enablement or upgrade workflows.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.lifecycle.content.libraries'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LibrariesStub)
        self._VAPI_OPERATION_IDS = {}

    class Status(Enum):
        """
        The ``Libraries.Status`` class describes the configuration status of the
        vSphere Namespaces with a Content Library.
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
        Indicates vSphere Namespaces is being configured with Content Library.

        """
        READY = None
        """
        Indicates vSphere Namespaces is ready to consume the Content Library.
        Expected status transition: 1. CONFIGURING --> READY

        """
        REMOVING = None
        """
        Indicates the Content Library is being removed and vSphere Namespaces is
        de-configured with Content Library. Expected status transition: 2.
        CONFIGURING --> REMOVING 3. READY --> REMOVING

        """
        ERROR = None
        """
        Indicates configuring the vSphere Namespaces with Content Library has an
        error or Content Library is not available anymore. The expected
        transitions: 1. CONFIGURING --> ERROR 2. CONFIGURING --> READY -->
        CONFIGURING --> ERROR 2. CONFIGURING --> READY --> ERROR 3. CONFIGURING -->
        READY --> REMOVING --> ERROR 4. CONFIGURING --> REMOVING --> ERROR

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'CONFIGURING': Status('CONFIGURING'),
        'READY': Status('READY'),
        'REMOVING': Status('REMOVING'),
        'ERROR': Status('ERROR'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.status',
        Status))


    class ContentLibrarySpec(VapiStruct):
        """
        The ``Libraries.ContentLibrarySpec`` class contains the specification
        required to configure the vSphere Namespaces with Content Library of
        Supervisor images.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the Content Library. The Content Library must exist
                in the vSphere inventory.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.content.Library``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.content.Library``.
            """
            self.id = id
            VapiStruct.__init__(self)


    ContentLibrarySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.content_library_spec', {
            'id': type.IdType(resource_types='com.vmware.content.Library'),
        },
        ContentLibrarySpec,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``Libraries.SetSpec`` class contains the specification required to
        configure vSphere Namespaces with an existing Content Library of Supervisor
        images.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     library=None,
                    ):
            """
            :type  library: :class:`str`
            :param library: The vSphere Namespaces will be configured with the
                :attr:`Libraries.SetSpec.library`.
                :attr:`Libraries.SetSpec.library` must refer to a Content Library
                in the vSphere inventory.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.content.Library``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.content.Library``.
            """
            self.library = library
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.set_spec', {
            'library': type.IdType(resource_types='com.vmware.content.Library'),
        },
        SetSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Libraries.Info`` class provides detailed information about a Content
        Library and configuration status with vSphere Namespaces.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     library=None,
                     status=None,
                     messages=None,
                    ):
            """
            :type  library: :class:`Libraries.ContentLibrarySpec`
            :param library: Details of the Content Library.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Libraries.Status`
            :param status: Configuration status of vSphere Namespaces with this Content
                Library.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  messages: :class:`list` of :class:`Libraries.Message`
            :param messages: Messages related to configuration between vSphere Namespaces and
                Content Library.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.library = library
            self.status = status
            self.messages = messages
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.info', {
            'library': type.ReferenceType(__name__, 'Libraries.ContentLibrarySpec'),
            'status': type.ReferenceType(__name__, 'Libraries.Status'),
            'messages': type.ListType(type.ReferenceType(__name__, 'Libraries.Message')),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Libraries.Summary`` class provides basic information about the
        Content Library configured with vSphere Namespaces.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     library=None,
                     status=None,
                    ):
            """
            :type  library: :class:`Libraries.ContentLibrarySpec`
            :param library: Details of the Content Library.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Libraries.Status`
            :param status: Indicates the configuration status of vSphere Namespaces with this
                Content Library.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.library = library
            self.status = status
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.summary', {
            'library': type.ReferenceType(__name__, 'Libraries.ContentLibrarySpec'),
            'status': type.ReferenceType(__name__, 'Libraries.Status'),
        },
        Summary,
        False,
        None))


    class Message(VapiStruct):
        """
        The ``Libraries.Message`` class contains the information about the Content
        Library configuration with vSphere Namespaces.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     severity=None,
                     message=None,
                    ):
            """
            :type  severity: :class:`Libraries.Message.Severity`
            :param severity: Type of the message.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  message: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param message: Details about the message.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.severity = severity
            self.message = message
            VapiStruct.__init__(self)


        class Severity(Enum):
            """
            The ``Libraries.Message.Severity`` class represents the severity of the
            message.
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
            INFO = None
            """
            Informational message. This may be accompanied by vCenter event.

            """
            WARNING = None
            """
            Warning message. This may be accompanied by vCenter event.

            """
            ERROR = None
            """
            Error message. This is accompanied by vCenter event and/or alarm.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Severity` instance.
                """
                Enum.__init__(string)

        Severity._set_values({
            'INFO': Severity('INFO'),
            'WARNING': Severity('WARNING'),
            'ERROR': Severity('ERROR'),
        })
        Severity._set_binding_type(type.EnumType(
            'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.message.severity',
            Severity))

    Message._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.message', {
            'severity': type.ReferenceType(__name__, 'Libraries.Message.Severity'),
            'message': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        },
        Message,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Libraries.ListResult`` class represents the result of
        :func:`Libraries.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     libraries=None,
                    ):
            """
            :type  libraries: :class:`list` of :class:`Libraries.Summary`
            :param libraries: List of content libraries.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.libraries = libraries
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.lifecycle.content.libraries.list_result', {
            'libraries': type.ListType(type.ReferenceType(__name__, 'Libraries.Summary')),
        },
        ListResult,
        False,
        None))



    def set(self,
            spec,
            ):
        """
        Assigns user-created Content Library to vSphere Namespaces which will
        consume Supervisor images from this Content Library during enablement
        and upgrade flows. The Content Library must be subscribed to vSphere
        Supervisor images repository or must have Supervisor images added
        manually.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Libraries.SetSpec`
        :param spec: Specification to configure vSphere Namespaces with user-created
            Content Library.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if Supervisor enablement or upgrade is in progress or vSphere
            Namespaces is configured with the same Content Library.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Content Library identifier specified in
            :attr:`Libraries.ContentLibrarySpec.id` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Manage privilege.
        """
        return self._invoke('set',
                            {
                            'spec': spec,
                            })

    def unassign(self,
                 library,
                 ):
        """
        Remove Content Library configuration with vSphere Namespaces.
        This method was added in **vSphere API 9.0.0.0**.

        :type  library: :class:`str`
        :param library: Identifier for the Content Library.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.Library``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            when Supervisor enablement or upgrade is in progress or another
            unassign operation is in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if vSphere Namespaces is not configured with ``library``
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Manage privilege.
        """
        return self._invoke('unassign',
                            {
                            'library': library,
                            })

    def get(self,
            library,
            ):
        """
        Get detailed information about the Content Library configured with
        vSphere Namespaces.
        This method was added in **vSphere API 9.0.0.0**.

        :type  library: :class:`str`
        :param library: Identifier for the Content Library.
            The parameter must be an identifier for the resource type:
            ``com.vmware.content.Library``.
        :rtype: :class:`Libraries.Info`
        :return: Detailed information about requested Content Library.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Content Library identifier specified in ``library`` is not found
            or vSphere Namespaces is not configured with it
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'library': library,
                            })

    def list(self):
        """
        List all content libraries configured with vSphere Namespaces.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Libraries.ListResult`
        :return: Basic information of all content libraries configured with vSphere
            Namespaces
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list', None)
class _LibrariesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Libraries.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/lifecycle/content/libraries',
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

        # properties for unassign operation
        unassign_input_type = type.StructType('operation-input', {
            'library': type.IdType(resource_types='com.vmware.content.Library'),
        })
        unassign_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        unassign_input_value_validator_list = [
        ]
        unassign_output_validator_list = [
        ]
        unassign_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/lifecycle/content/libraries/{library}?action=unassign',
            path_variables={
                'library': 'library',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'unassign',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'library': type.IdType(resource_types='com.vmware.content.Library'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/vcenter/namespace-management/lifecycle/content/libraries/{library}',
            path_variables={
                'library': 'library',
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
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/vcenter/namespace-management/lifecycle/content/libraries',
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
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'unassign': {
                'input_type': unassign_input_type,
                'output_type': type.VoidType(),
                'errors': unassign_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': unassign_input_value_validator_list,
                'output_validator_list': unassign_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Libraries.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Libraries.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'unassign': unassign_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.lifecycle.content.libraries',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Libraries': Libraries,
    }

