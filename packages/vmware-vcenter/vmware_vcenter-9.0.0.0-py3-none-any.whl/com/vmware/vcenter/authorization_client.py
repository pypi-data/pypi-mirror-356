# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.authorization.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.authorization_client`` module provides classes for
managing authorization.

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


class Permissions(VapiInterface):
    """
    The ``Permissions`` class provides methods to create, update, delete and
    retrieve authorization permissions in the vCenter Server. 
    
    The authorization permissions are the actual access-control rules. There
    are currently two kinds of permissions - global and inventory permissions.
    But in the future we could support more. 
    
    An inventory permission is defined on an resource which is part of
    vCenter's inventory and specifies the user or group to which the rule
    applies. The role specifies the privileges to apply, and the propagate flag
    specifies whether or not the rule applies to the sub-resources of the
    inventory. 
    
    A resource may have multiple permissions, but can have only one permission
    per user or group. If, when logging in, a user has both a user permission
    and a group permission (as a group member) for the same resource, then the
    user-specific permission takes precedent. If there is no user-specific
    permission, but two or more group permissions are present, and the user is
    a member of the groups, then the privileges are the union of the specified
    roles. 
    
    There global permissions are assigned without specifying a resource. These
    permissions, if set as propagated, could propagated down to all resources,
    including inventory.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.authorization.Permission"
    """
    Resource type for authorization permission in vCenter Server.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.authorization.permissions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PermissionsStub)
        self._VAPI_OPERATION_IDS = {}

    class Principal(VapiStruct):
        """
        The ``Permissions.Principal`` class contains the name, the domain and
        whether it is a user or group.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     name=None,
                     domain=None,
                    ):
            """
            :type  type: :class:`Permissions.Principal.Type`
            :param type: The type of the principal.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  name: :class:`str`
            :param name: The name of the principal.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  domain: :class:`str` or ``None``
            :param domain: The domain name which this principal belongs to.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, 'localos' domain is assumed.
            """
            self.type = type
            self.name = name
            self.domain = domain
            VapiStruct.__init__(self)


        class Type(Enum):
            """
            The ``Permissions.Principal.Type`` class lists all possible types of
            principals.
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
            USER = None
            """
            The principal is a user.

            """
            GROUP = None
            """
            The principal is a group.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'USER': Type('USER'),
            'GROUP': Type('GROUP'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.authorization.permissions.principal.type',
            Type))

    Principal._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.principal', {
            'type': type.ReferenceType(__name__, 'Permissions.Principal.Type'),
            'name': type.StringType(),
            'domain': type.OptionalType(type.StringType()),
        },
        Principal,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Permissions.CreateSpec`` class contains detailed information about
        the creation of a permission.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     object=None,
                     principal=None,
                     role=None,
                     propagating=None,
                    ):
            """
            :type  object: :class:`com.vmware.vapi.std_client.DynamicID`
            :param object: The object that this permission is assigned on.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  principal: :class:`Permissions.Principal`
            :param principal: The principal that this permission is assigned for.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  role: :class:`str`
            :param role: The role which this permission grants.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``.
            :type  propagating: :class:`bool`
            :param propagating: Indicator whether the permission apply only on the object which it
                is assigned on or it propagates through the hierarchy of
                sub-entities.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.object = object
            self.principal = principal
            self.role = role
            self.propagating = propagating
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.create_spec', {
            'object': type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'),
            'principal': type.ReferenceType(__name__, 'Permissions.Principal'),
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
            'propagating': type.BooleanType(),
        },
        CreateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Permissions.Info`` class contains detailed information about a
        specific authorization permission.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     object=None,
                     principal=None,
                     role=None,
                     propagating=None,
                    ):
            """
            :type  object: :class:`com.vmware.vapi.std_client.DynamicID`
            :param object: The object that this permission is assigned on.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  principal: :class:`Permissions.Principal`
            :param principal: The principal that this permission is assigned for.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  role: :class:`str`
            :param role: The role which this permission grants.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``.
            :type  propagating: :class:`bool`
            :param propagating: Indicator whether the permission apply only on the object which it
                is assigned on or it propagates through the hierarchy of
                sub-entities.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.object = object
            self.principal = principal
            self.role = role
            self.propagating = propagating
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.info', {
            'object': type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'),
            'principal': type.ReferenceType(__name__, 'Permissions.Principal'),
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
            'propagating': type.BooleanType(),
        },
        Info,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Permissions.UpdateSpec`` class contains detailed information about
        the update of a specific authorization permission.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     role=None,
                     is_propagating=None,
                    ):
            """
            :type  role: :class:`str` or ``None``
            :param role: The role which this permission grants.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``.
                If None the role won't be updated.
            :type  is_propagating: :class:`bool` or ``None``
            :param is_propagating: Indicator whether the permission apply only on the object which it
                is assigned on or it propagates through the hierarchy of
                sub-entities.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None propagation flag won't be updated.
            """
            self.role = role
            self.is_propagating = is_propagating
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.update_spec', {
            'role': type.OptionalType(type.IdType()),
            'is_propagating': type.OptionalType(type.BooleanType()),
        },
        UpdateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Permissions.FilterSpec`` class contains attributes based on which
        authorization permissions can be filtered. Any permission matching all of
        the conditions is returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     objects=None,
                     principals=None,
                     roles=None,
                     is_propagating=None,
                    ):
            """
            :type  objects: :class:`list` of :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param objects: Objects which permissions are assigned on.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all permissions match.
            :type  principals: :class:`list` of :class:`Permissions.Principal` or ``None``
            :param principals: Principals who permissions are assigned for.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all permissions match.
            :type  roles: :class:`set` of :class:`str` or ``None``
            :param roles: The roles granted by the permissions.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Role``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Role``.
                If None all permissions match.
            :type  is_propagating: :class:`bool` or ``None``
            :param is_propagating: Whether the permission is propagating.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all permissions match.
            """
            self.objects = objects
            self.principals = principals
            self.roles = roles
            self.is_propagating = is_propagating
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.filter_spec', {
            'objects': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'))),
            'principals': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Permissions.Principal'))),
            'roles': type.OptionalType(type.SetType(type.IdType())),
            'is_propagating': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Permissions.ListItem`` class contains information about an
        authorization permission in the vCenter Server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     permission=None,
                     info=None,
                    ):
            """
            :type  permission: :class:`str`
            :param permission: The ID of the permission.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Permission``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Permission``.
            :type  info: :class:`Permissions.Info`
            :param info: Information about the permission.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.permission = permission
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.list_item', {
            'permission': type.IdType(resource_types='com.vmware.vcenter.authorization.Permission'),
            'info': type.ReferenceType(__name__, 'Permissions.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Permissions.ListResult`` class contains information about the
        authorization permissions defined in the vCenter Server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                     marker=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Permissions.ListItem`
            :param items: The permissions that match the
                specified:class:`Permissions.FilterSpec` and
                :class:`Permissions.IterationSpec` in lexicographical order.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  marker: :class:`str` or ``None``
            :param marker: An opaque marker indicating the last returned permission. If there
                are more permissions collected than were returned, the next ones
                can be retrieved directly by passing this value to another call to
                #list. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None then all of the currently available permissions have been
                returned.
            """
            self.items = items
            self.marker = marker
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Permissions.ListItem')),
            'marker': type.OptionalType(type.StringType()),
        },
        ListResult,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Permissions.IterationSpec`` class contains attributes used to break
        results into pages when listing permissions, see :func:`Permissions.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     page_size=None,
                     marker=None,
                    ):
            """
            :type  page_size: :class:`long` or ``None``
            :param page_size: Maximum number of records to return in one call. Clients can limit
                the response size to a number of records they feel comfortable
                handling with this setting. A service policy can overwrite it to
                something that is less than the value specified by the client. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to 200 permissions.
            :type  marker: :class:`str` or ``None``
            :param marker: The marker is a simple cursor (pointer) pointing to the position of
                the last record that has been previously returned. By using the
                marker, the client is guaranteed to iterate through all records
                without repetition. 
                
                Presenting a marker means that only the records after the position
                to which the marker points will be returned to the client. 
                
                This value is obtained from #list method. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, first page of records will be returned.
            """
            self.page_size = page_size
            self.marker = marker
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.permissions.iteration_spec', {
            'page_size': type.OptionalType(type.IntegerType()),
            'marker': type.OptionalType(type.StringType()),
        },
        IterationSpec,
        False,
        None))



    def create(self,
               spec,
               ):
        """
        Creates a new authorization permission in vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Permissions.CreateSpec`
        :param spec: The CreateSpec for the new permission.
        :rtype: :class:`str`
        :return: ID of the newly created permission.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Permission``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if there is already such permission created. No duplicates are
            allowed.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the CreateSpec contains invalid data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges on the current
            object to create the new permission.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def get(self,
            permission,
            ):
        """
        Returns the detailed information about a specific authorization
        permission in the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  permission: :class:`str`
        :param permission: the unique identifier of the permission.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Permission``.
        :rtype: :class:`Permissions.Info`
        :return: Detailed information about the specified permission.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no permission found with the specified ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege granted on the
            current object.
        """
        return self._invoke('get',
                            {
                            'permission': permission,
                            })

    def delete(self,
               permission,
               ):
        """
        Deletes an authorization permission from the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  permission: :class:`str`
        :param permission: the unique identifier of the permission in the vCenter Server.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Permission``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the permission is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the system will be left without Administrator permission on the
            root resource.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges on the current
            object to delete the new permission.
        """
        return self._invoke('delete',
                            {
                            'permission': permission,
                            })

    def list(self,
             filter=None,
             iterate=None,
             ):
        """
        Queries the authorization permissions in the vCenter Server matching
        given criteria.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Permissions.FilterSpec` or ``None``
        :param filter: Return only permissions matching the specified filters.
            If None return all permissions.
        :type  iterate: :class:`Permissions.IterationSpec` or ``None``
        :param iterate: allows to iterate over the set of permissions.
            if None, only the first permissions that fit in a size defined by
            the service will be returned.
        :rtype: :class:`Permissions.ListResult`
        :return: Detailed information about the permissions.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if both filter and marker are passed
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            })

    def update(self,
               permission,
               spec,
               ):
        """
        Updates an existing authorization permission in the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  permission: :class:`str`
        :param permission: the unique identifier of the permission which is about to be
            updated in the vCenter Server.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Permission``.
        :type  spec: :class:`Permissions.UpdateSpec`
        :param spec: The update spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the UpdateSpec contains invalid data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the the permission is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the system will be left without Administrator permission on the
            root resource.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have sufficient privileges on the current
            object to update the new permission.
        """
        return self._invoke('update',
                            {
                            'permission': permission,
                            'spec': spec,
                            })
class PrivilegeChecks(VapiInterface):
    """
    The ``PrivilegeChecks`` class provides methods for retrieving permission
    privilege checks recorded by VPXD. 
    
    The privilege checks are recorded as VPXD makes them. The latest recorded
    privilege check can be retrieved by a call to
    com.vmware.vcenter.authorization.privilege_checks.Latest.get This allows
    for querying of all privilege checks before or after that moment. For
    example, if an administrator wants to record the privilege checks made by a
    given UI workflow, they can do the following. 1. Retrieve the latest
    privilege check and store it. 2. Go through the UI workflow. 3. Retrieve
    the latest privilege check and store it. 4. Invoke
    com.vmware.vcenter.authorization.PrivilegeChecks.list with the values from
    steps 1) and 3) along with any additional filters.
    This class was added in **vSphere API 8.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.authorization.privilege_checks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrivilegeChecksStub)
        self._VAPI_OPERATION_IDS = {}

    class Principal(VapiStruct):
        """
        The ``PrivilegeChecks.Principal`` class contains an identity management
        principal ID.
        This class was added in **vSphere API 8.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     domain=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The principal's username.
                This attribute was added in **vSphere API 8.0.0.0**.
            :type  domain: :class:`str`
            :param domain: The principal's domain.
                This attribute was added in **vSphere API 8.0.0.0**.
            """
            self.name = name
            self.domain = domain
            VapiStruct.__init__(self)


    Principal._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privilege_checks.principal', {
            'name': type.StringType(),
            'domain': type.StringType(),
        },
        Principal,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``PrivilegeChecks.Info`` class contains detailed information about a
        privilege check.
        This class was added in **vSphere API 8.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     object=None,
                     principal=None,
                     privilege=None,
                    ):
            """
            :type  object: :class:`com.vmware.vapi.std_client.DynamicID`
            :param object: Object for which the privilege was checked.
                This attribute was added in **vSphere API 8.0.0.0**.
            :type  principal: :class:`PrivilegeChecks.Principal` or ``None``
            :param principal: Principal for which the privilege was checked. Note that the
                username and domain specified are case-insensitive.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None the privilege was checked for an unauthenticated session.
            :type  privilege: :class:`str`
            :param privilege: Privilege that was checked.
                This attribute was added in **vSphere API 8.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.authz.Privilege``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.cis.authz.Privilege``.
            """
            self.object = object
            self.principal = principal
            self.privilege = privilege
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privilege_checks.info', {
            'object': type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'),
            'principal': type.OptionalType(type.ReferenceType(__name__, 'PrivilegeChecks.Principal')),
            'privilege': type.IdType(resource_types='com.vmware.cis.authz.Privilege'),
        },
        Info,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``PrivilegeChecks.IterationSpec`` class contains attributes used to
        break results into pages when listing privilege checks, see
        :func:`PrivilegeChecks.list`).
        This class was added in **vSphere API 8.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     size=None,
                     marker=None,
                     end_marker=None,
                     timeout_ms=None,
                    ):
            """
            :type  size: :class:`long` or ``None``
            :param size: Specifies the maximum number of results to return.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None defaults to default page size, which is controlled by
                config.vpxd.privilegeChecks.pageSize advanced option.
            :type  marker: :class:`str` or ``None``
            :param marker: An opaque token which determines where the returned page should
                begin.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None or empty, privilege checks will be returned from the first
                record.
            :type  end_marker: :class:`str` or ``None``
            :param end_marker: An opaque token which determines where the returned page should
                end.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None or empty, privilege checks will be returned up to size, if
                set, or up to the default page size.
            :type  timeout_ms: :class:`long` or ``None``
            :param timeout_ms: Indicates how long the request should wait in ms for a matching
                check if :attr:`PrivilegeChecks.IterationSpec.marker` is set, and
                there no matching checks to be added to the result.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None or empty, the request will not wait for additional
                privilege checks and will return immediately.
            """
            self.size = size
            self.marker = marker
            self.end_marker = end_marker
            self.timeout_ms = timeout_ms
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privilege_checks.iteration_spec', {
            'size': type.OptionalType(type.IntegerType()),
            'marker': type.OptionalType(type.StringType()),
            'end_marker': type.OptionalType(type.StringType()),
            'timeout_ms': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``PrivilegeChecks.FilterSpec`` class contains attributes based on which
        privilege checks can be filtered. Any privilege check matching at least one
        of the conditions is returned.
        This class was added in **vSphere API 8.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     objects=None,
                     sessions=None,
                     principals=None,
                     privileges=None,
                     op_ids=None,
                    ):
            """
            :type  objects: :class:`list` of :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param objects: IDs of the objects on which the privilege check was performed.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None all objects match.
            :type  sessions: :class:`set` of :class:`str` or ``None``
            :param sessions: Sessions for which the check was performed.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None all sessions match.
            :type  principals: :class:`list` of (:class:`PrivilegeChecks.Principal` or ``None``) or ``None``
            :param principals: Principles for which the privilege check was performed. The None
                ``PrivilegeChecks.Principal`` value matches privilege checks for
                anonymous sessions.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None all principles match.
            :type  privileges: :class:`set` of :class:`str` or ``None``
            :param privileges: Privileges that were checked.
                This attribute was added in **vSphere API 8.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.cis.authz.Privilege``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.cis.authz.Privilege``.
                If None all privileges match.
            :type  op_ids: :class:`set` of :class:`str` or ``None``
            :param op_ids: OpIDs of the requests for which the check was performed.
                This attribute was added in **vSphere API 8.0.0.0**.
                If None all opIDs match.
            """
            self.objects = objects
            self.sessions = sessions
            self.principals = principals
            self.privileges = privileges
            self.op_ids = op_ids
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privilege_checks.filter_spec', {
            'objects': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'))),
            'sessions': type.OptionalType(type.SetType(type.StringType())),
            'principals': type.OptionalType(type.ListType(type.OptionalType(type.ReferenceType(__name__, 'PrivilegeChecks.Principal')))),
            'privileges': type.OptionalType(type.SetType(type.IdType())),
            'op_ids': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``PrivilegeChecks.ListResult`` class contains information about the
        performed privilege checks, if there are any further privilege checks
        available for reading, and if there are privilege checks potentially
        missing.
        This class was added in **vSphere API 8.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                     marker=None,
                     truncated=None,
                    ):
            """
            :type  items: :class:`list` of :class:`PrivilegeChecks.Info`
            :param items: Privilege checks that match the
                specified:class:`PrivilegeChecks.FilterSpec` and
                :class:`PrivilegeChecks.IterationSpec` in chronological order as
                they were performed. Each check is recorded only the first time it
                is made. If more than one privilege check matches a given
                :class:`PrivilegeChecks.FilterSpec` (for example, two different
                opIDs checked System.Read for the same object and the same
                principal, a FilterSpec which specifies only the principal will
                only contain the first check).
                This attribute was added in **vSphere API 8.0.0.0**.
            :type  marker: :class:`str`
            :param marker: An opaque marker indicating the last returned privilege check. If
                there are more privilege checks collected than were returned, the
                next ones can be retrieved directly by passing this value to
                another call to
                com.vmware.vcenter.authorization.PrivilegeChecks.list. 
                This attribute was added in **vSphere API 8.0.0.0**.
            :type  truncated: :class:`bool`
            :param truncated: In case :attr:`PrivilegeChecks.IterationSpec.marker` was specified
                and valid, but the privilege check indicated by it is no longer
                stored, ListResult.truncated is set to True to indicate that some
                privilege checks are potentially missing. 
                
                The number of privilege checks stored is determined by the value of
                config.vpxd.privilegeChecks.bufferSize advanced option.
                This attribute was added in **vSphere API 8.0.0.0**.
            """
            self.items = items
            self.marker = marker
            self.truncated = truncated
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privilege_checks.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'PrivilegeChecks.Info')),
            'marker': type.StringType(),
            'truncated': type.BooleanType(),
        },
        ListResult,
        False,
        None))



    def list(self,
             iteration=None,
             filter=None,
             ):
        """
        Queries the privilege checks matching given criteria.
        This method was added in **vSphere API 8.0.0.0**.

        :type  iteration: :class:`PrivilegeChecks.IterationSpec` or ``None``
        :param iteration: Contains optional settings for pagination of the result.
            if unset, the oldest privilege checks recorded are returned, paged
            by the default page size. 
            
            The default page size can be changed from
            config.vpxd.privilegeChecks.pageSize advanced option.
        :type  filter: :class:`PrivilegeChecks.FilterSpec` or ``None``
        :param filter: Contains optional settings by which the privilege checks should be
            filtered.
            if unset, recorded privilege checks matching the iteration spec are
            returned.
        :rtype: :class:`PrivilegeChecks.ListResult`
        :return: Detailed information about the privileges collected so far.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if filter or iteration spec contain invalid values.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the iteration spec contains a marker that could not be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Sessions.CollectPrivilegeChecks``.
        """
        return self._invoke('list',
                            {
                            'iteration': iteration,
                            'filter': filter,
                            })
class Privileges(VapiInterface):
    """
    The ``Privileges`` class provides methods to query and retrieve
    authorization privileges in the vCenter Server. 
    
    Privileges are the most fine grained rights required by operations in order
    to be performed. They are statically defined in the vCenter Server.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.authorization.Privilege"
    """
    Resource type for authorization privileges in vCenter Server.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.authorization.privileges'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrivilegesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Privileges.Info`` class contains detailed information about a
        specific privilege.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                     on_parent=None,
                     version=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the privilege. It matches completely with the ID of the
                privilege.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: A brief summary what this privilege is dedicated for.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  on_parent: :class:`bool`
            :param on_parent: Indicates whether the privilege needs to apply on parent object as
                well.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  version: :class:`long`
            :param version: The latest version of the privilege. Default version when the
                privilege is created is 0. If privilege is modified this counter is
                increased.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.description = description
            self.on_parent = on_parent
            self.version = version
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privileges.info', {
            'name': type.StringType(),
            'description': type.StringType(),
            'on_parent': type.BooleanType(),
            'version': type.IntegerType(),
        },
        Info,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Privileges.IterationSpec`` class contains attributes used to break
        results into pages when listing privileges, see :func:`Privileges.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     page_size=None,
                     marker=None,
                    ):
            """
            :type  page_size: :class:`long` or ``None``
            :param page_size: Maximum number of records to return in one call. Clients can limit
                the response size to a number of records they feel comfortable
                handling with this setting. A service policy can overwrite it to
                something that is less than the value specified by the client. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to 200 privileges.
            :type  marker: :class:`str` or ``None``
            :param marker: The marker is a simple cursor (pointer) pointing to the position of
                the last record that has been previously returned. By using the
                marker, the client is guaranteed to iterate through all records
                without repetition. 
                
                Presenting a marker means that only the records after the position
                to which the marker points will be returned to the client. 
                
                This value is obtained from #list method. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, first page of records will be returned.
            """
            self.page_size = page_size
            self.marker = marker
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privileges.iteration_spec', {
            'page_size': type.OptionalType(type.IntegerType()),
            'marker': type.OptionalType(type.StringType()),
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Privileges.FilterSpec`` class contains attributes based on which
        privileges can be filtered. Any privilege matching all of the conditions is
        returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     names=None,
                     is_on_parent=None,
                     versions=None,
                    ):
            """
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names of the privileges. The name of a privilege matches completely
                with its ID.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all privileges match.
            :type  is_on_parent: :class:`bool` or ``None``
            :param is_on_parent: Whether the privileges should apply to parent object as well.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all privileges match.
            :type  versions: :class:`set` of :class:`long` or ``None``
            :param versions: The versions of the privileges.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all privileges match.
            """
            self.names = names
            self.is_on_parent = is_on_parent
            self.versions = versions
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privileges.filter_spec', {
            'names': type.OptionalType(type.SetType(type.StringType())),
            'is_on_parent': type.OptionalType(type.BooleanType()),
            'versions': type.OptionalType(type.SetType(type.IntegerType())),
        },
        FilterSpec,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Privileges.ListItem`` class contains information about an
        authorization privilege in the vCenter Server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     privilege=None,
                     info=None,
                    ):
            """
            :type  privilege: :class:`str`
            :param privilege: The ID of the privilege.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``. When methods return
                a value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``.
            :type  info: :class:`Privileges.Info`
            :param info: Information about the privilege.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.privilege = privilege
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privileges.list_item', {
            'privilege': type.IdType(resource_types='com.vmware.vcenter.authorization.Privilege'),
            'info': type.ReferenceType(__name__, 'Privileges.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Privileges.ListResult`` class contains information about the
        performed privilege checks, if there are any further privilege checks
        available for reading, and if there are privilege checks potentially
        missing.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                     marker=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Privileges.ListItem`
            :param items: The privileges that match the
                specified:class:`Privileges.FilterSpec` and
                :class:`Privileges.IterationSpec` in lexicographical order.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  marker: :class:`str` or ``None``
            :param marker: An opaque marker indicating the last returned privilege. If there
                are more privileges collected than were returned, the next ones can
                be retrieved directly by passing this value to another call to
                {#list}. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None then all of the currently available privileges have been
                returned.
            """
            self.items = items
            self.marker = marker
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.privileges.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Privileges.ListItem')),
            'marker': type.OptionalType(type.StringType()),
        },
        ListResult,
        False,
        None))



    def list(self,
             filter=None,
             iterate=None,
             ):
        """
        Queries the authorization privileges in the vCenter Server matching
        given criteria.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Privileges.FilterSpec` or ``None``
        :param filter: Return only privileges matching the specified filters.
            If None return all privileges.
        :type  iterate: :class:`Privileges.IterationSpec` or ``None``
        :param iterate: allows to iterate over the set of privileges.
            if None, only the first privileges that fit in a size defined by
            the service will be returned.
        :rtype: :class:`Privileges.ListResult`
        :return: Detailed information about the privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if filterSpec or iterationSpec contain invalid data
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            })

    def get(self,
            privilege,
            ):
        """
        Returns the detailed information about a specific authorization
        privilege in the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  privilege: :class:`str`
        :param privilege: the unique identifier of the privilege.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Privilege``.
        :rtype: :class:`Privileges.Info`
        :return: Detailed information about the specified privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no privilege found with the specified ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'privilege': privilege,
                            })
class Roles(VapiInterface):
    """
    The ``Roles`` class provides methods to create, update, delete and retrieve
    authorization roles in the vCenter Server. 
    
    The authorization role is a collection of :class:`Privileges` which are
    grouped in a such way that they are related to a specific functionality. 
    
    Each user defined authorization role contains at minimum three specific
    :class:`Privileges` "System.Anonymous", "System.View", "System.Read".
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.authorization.Role"
    """
    Resource type for authorization roles in vCenter Server.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.authorization.roles'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RolesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Roles.Info`` class contains detailed information about a specific
        role.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                     privileges=None,
                     system=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the role.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: A brief summary what this role is dedicated for.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  privileges: :class:`set` of :class:`str`
            :param privileges: The set of :class:`Privileges` which are part of this role.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``. When methods return
                a value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``.
            :type  system: :class:`bool`
            :param system: Indicator if role is created as system built-in role.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.description = description
            self.privileges = privileges
            self.system = system
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.info', {
            'name': type.StringType(),
            'description': type.StringType(),
            'privileges': type.SetType(type.IdType()),
            'system': type.BooleanType(),
        },
        Info,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Roles.CreateSpec`` class contains detailed information about the
        creation of a specific role.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                     privileges=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the role.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: A brief summary what this role is dedicated for.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  privileges: :class:`set` of :class:`str`
            :param privileges: The set of :class:`Privileges` which are part of this role.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``. When methods return
                a value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``.
            """
            self.name = name
            self.description = description
            self.privileges = privileges
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.create_spec', {
            'name': type.StringType(),
            'description': type.StringType(),
            'privileges': type.SetType(type.IdType()),
        },
        CreateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Roles.UpdateSpec`` class contains detailed information about the
        update of a specific role.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                     privileges=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: The name of the role.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the value is unchanged.
            :type  description: :class:`str` or ``None``
            :param description: A brief summary what this role is dedicated for.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the value is unchanged.
            :type  privileges: :class:`set` of :class:`str` or ``None``
            :param privileges: The set of :class:`Privileges` which are part of this role.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``. When methods return
                a value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``.
                If None, the value is unchanged.
            """
            self.name = name
            self.description = description
            self.privileges = privileges
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.update_spec', {
            'name': type.OptionalType(type.StringType()),
            'description': type.OptionalType(type.StringType()),
            'privileges': type.OptionalType(type.SetType(type.IdType())),
        },
        UpdateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Roles.FilterSpec`` class contains attributes based on which
        authorization roles can be filtered. Any role matching all of the
        conditions is returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     names=None,
                     privileges=None,
                     is_system=None,
                    ):
            """
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names of the roles.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all roles match.
            :type  privileges: :class:`set` of :class:`str` or ``None``
            :param privileges: The :class:`Privileges` part of the role.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``. When methods return
                a value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.authorization.Privilege``.
                If None all roles match.
            :type  is_system: :class:`bool` or ``None``
            :param is_system: Whether the role is a system built-in role.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None all roles match.
            """
            self.names = names
            self.privileges = privileges
            self.is_system = is_system
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.filter_spec', {
            'names': type.OptionalType(type.SetType(type.StringType())),
            'privileges': type.OptionalType(type.SetType(type.IdType())),
            'is_system': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Roles.ListItem`` class contains information about an authorization
        role in the vCenter Server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     role=None,
                     info=None,
                    ):
            """
            :type  role: :class:`str`
            :param role: The ID of the role.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.authorization.Role``.
            :type  info: :class:`Roles.Info`
            :param info: Information about the role.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.role = role
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.list_item', {
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
            'info': type.ReferenceType(__name__, 'Roles.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Roles.ListResult`` class contains information about the authorization
        roles defined in the vCenter Server.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                     marker=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Roles.ListItem`
            :param items: The roles that match the specified:class:`Roles.FilterSpec` and
                :class:`Roles.IterationSpec` in lexicographical order.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  marker: :class:`str` or ``None``
            :param marker: An opaque marker indicating the last returned role. If there are
                more roles collected than were returned, the next ones can be
                retrieved directly by passing this value to another call to #list. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None then all of the currently available roles have been
                returned.
            """
            self.items = items
            self.marker = marker
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Roles.ListItem')),
            'marker': type.OptionalType(type.StringType()),
        },
        ListResult,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Roles.IterationSpec`` class contains attributes used to break results
        into pages when listing roles, see :func:`Roles.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     page_size=None,
                     marker=None,
                    ):
            """
            :type  page_size: :class:`long` or ``None``
            :param page_size: Maximum number of records to return in one call. Clients can limit
                the response size to a number of records they feel comfortable
                handling with this setting. A service policy can overwrite it to
                something that is less than the value specified by the client. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to 200 roles.
            :type  marker: :class:`str` or ``None``
            :param marker: The marker is a simple cursor (pointer) pointing to the position of
                the last record that has been previously returned. By using the
                marker, the client is guaranteed to iterate through all records
                without repetition. 
                
                Presenting a marker means that only the records after the position
                to which the marker points will be returned to the client. 
                
                This value is obtained from #list method. 
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, first page of records will be returned.
            """
            self.page_size = page_size
            self.marker = marker
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.authorization.roles.iteration_spec', {
            'page_size': type.OptionalType(type.IntegerType()),
            'marker': type.OptionalType(type.StringType()),
        },
        IterationSpec,
        False,
        None))



    def create(self,
               spec,
               ):
        """
        Creates a new authorization role in vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Roles.CreateSpec`
        :param spec: The CreateSpec for the new role.
        :rtype: :class:`str`
        :return: ID of the newly created role.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Role``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if there is already a role with the same name.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the CreateSpec contains invalid data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Authorization.ModifyRoles``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def get(self,
            role,
            ):
        """
        Returns the detailed information about a specific authorization role in
        the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  role: :class:`str`
        :param role: the unique identifier of the role.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Role``.
        :rtype: :class:`Roles.Info`
        :return: Detailed information about the specified role.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no role found with the specified ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'role': role,
                            })

    def delete(self,
               role,
               ):
        """
        Deletes an authorization role from the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  role: :class:`str`
        :param role: the unique identifier of the role in the vCenter Server.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Role``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if the role used by :class:`Permissions`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the updated role is a system build-in role.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the role is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Authorization.ModifyRoles``.
        """
        return self._invoke('delete',
                            {
                            'role': role,
                            })

    def list(self,
             filter=None,
             iterate=None,
             ):
        """
        Queries the authorization roles in the vCenter Server matching given
        criteria.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Roles.FilterSpec` or ``None``
        :param filter: Return only roles matching the specified filters.
            If None return all roles.
        :type  iterate: :class:`Roles.IterationSpec` or ``None``
        :param iterate: allows to iterate over the set of roles.
            if None, only the first roles that fit in a size defined by the
            service will be returned.
        :rtype: :class:`Roles.ListResult`
        :return: Detailed information about the roles.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if an error occurred while getting the data.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if filterSpec or iterationSpec contain invalid data
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            })

    def update(self,
               role,
               spec,
               ):
        """
        Updates an existing authorization role in the vCenter Server.
        This method was added in **vSphere API 9.0.0.0**.

        :type  role: :class:`str`
        :param role: the unique identifier of the role which is about to be updated in
            the vCenter Server.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.authorization.Role``.
        :type  spec: :class:`Roles.UpdateSpec`
        :param spec: The update spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the UpdateSpec contains invalid data.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the updated role name matches with an already existing role name
            but with other ID.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the updated role is a system build-in role.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the the role is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If any other error occurs.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``Authorization.ModifyRoles``.
        """
        return self._invoke('update',
                            {
                            'role': role,
                            'spec': spec,
                            })
class _PermissionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Permissions.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/authorization/permissions',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'permission': type.IdType(resource_types='com.vmware.vcenter.authorization.Permission'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/authorization/permissions/{permission}',
            path_variables={
                'permission': 'permission',
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
            'permission': type.IdType(resource_types='com.vmware.vcenter.authorization.Permission'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
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
            url_template='/vcenter/authorization/permissions/{permission}',
            path_variables={
                'permission': 'permission',
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
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Permissions.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Permissions.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/authorization/permissions?action=list',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'list',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'permission': type.IdType(resource_types='com.vmware.vcenter.authorization.Permission'),
            'spec': type.ReferenceType(__name__, 'Permissions.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/authorization/permissions/{permission}',
            request_body_parameter='spec',
            path_variables={
                'permission': 'permission',
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
                'output_type': type.IdType(resource_types='com.vmware.vcenter.authorization.Permission'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Permissions.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Permissions.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.authorization.permissions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PrivilegeChecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'iteration': type.OptionalType(type.ReferenceType(__name__, 'PrivilegeChecks.IterationSpec')),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'PrivilegeChecks.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/authorization/privilege-checks?action=list',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'list',
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
                'output_type': type.ReferenceType(__name__, 'PrivilegeChecks.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.authorization.privilege_checks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _PrivilegesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Privileges.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Privileges.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/authorization/privileges',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'privilege': type.IdType(resource_types='com.vmware.vcenter.authorization.Privilege'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/authorization/privileges/{privilege}',
            path_variables={
                'privilege': 'privilege',
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
                'output_type': type.ReferenceType(__name__, 'Privileges.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Privileges.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.authorization.privileges',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _RolesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Roles.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/authorization/roles',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/authorization/roles/{role}',
            path_variables={
                'role': 'role',
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
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/authorization/roles/{role}',
            path_variables={
                'role': 'role',
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
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Roles.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Roles.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/authorization/roles',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'role': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
            'spec': type.ReferenceType(__name__, 'Roles.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/vcenter/authorization/roles/{role}',
            request_body_parameter='spec',
            path_variables={
                'role': 'role',
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
                'output_type': type.IdType(resource_types='com.vmware.vcenter.authorization.Role'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Roles.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Roles.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'get': get_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.authorization.roles',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Permissions': Permissions,
        'PrivilegeChecks': PrivilegeChecks,
        'Privileges': Privileges,
        'Roles': Roles,
        'privilege_checks': 'com.vmware.vcenter.authorization.privilege_checks_client.StubFactory',
        'vt_containers': 'com.vmware.vcenter.authorization.vt_containers_client.StubFactory',
    }

