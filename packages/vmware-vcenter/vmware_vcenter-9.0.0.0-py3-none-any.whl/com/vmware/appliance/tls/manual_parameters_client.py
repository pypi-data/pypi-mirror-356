# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.tls.manual_parameters.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.tls.manual_parameters_client`` module provides
classes for managing the manual/custom TLS parameters as an alternative for
using VMware-provided standard TLS Profiles.

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


class Global(VapiInterface):
    """
    ``Global`` class provides methods APIs to configure manual/custom TLS
    parameters.
    This class was added in **vSphere API 8.0.3.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.tls.manual_parameters.global'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _GlobalStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})

    class ProtocolVersionInfo(VapiStruct):
        """
        The ``Global.ProtocolVersionInfo`` class contains the information about the
        TLS protocol version and its ciphers.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     ciphers=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Defines the TLS protocol version.
                This attribute was added in **vSphere API 8.0.3.0**.
            :type  ciphers: :class:`list` of :class:`str`
            :param ciphers: Defines the TLS protocol ciphers in IANA form.
                This attribute was added in **vSphere API 8.0.3.0**.
            """
            self.version = version
            self.ciphers = ciphers
            VapiStruct.__init__(self)


    ProtocolVersionInfo._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.global.protocol_version_info', {
            'version': type.StringType(),
            'ciphers': type.ListType(type.StringType()),
        },
        ProtocolVersionInfo,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``Global.SetSpec`` class contains the information about the TLS
        Profile.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     protocol_versions=None,
                     curves=None,
                     fips_enforced=None,
                    ):
            """
            :type  protocol_versions: :class:`list` of :class:`Global.ProtocolVersionInfo`
            :param protocol_versions: Defines the list of TLS protocol version and their ciphers
                This attribute was added in **vSphere API 8.0.3.0**.
            :type  curves: :class:`list` of :class:`str`
            :param curves: Defines the TLS Profile curves in IANA form.
                This attribute was added in **vSphere API 8.0.3.0**.
            :type  fips_enforced: :class:`bool`
            :param fips_enforced: Indicates if FIPS 140-3 compliance is enforced for the TLS Profile.
                This attribute was added in **vSphere API 8.0.3.0**.

                .. deprecated:: vSphere API 9.0.0.0
                    This attribute is deprecated as of **vSphere API 9.0.0.0**. in
                    9.0.0.0 and above all profiles are FIPS compliant, always
                    \\\\@term true.
            """
            self.protocol_versions = protocol_versions
            self.curves = curves
            self.fips_enforced = fips_enforced
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.global.set_spec', {
            'protocol_versions': type.ListType(type.ReferenceType(__name__, 'Global.ProtocolVersionInfo')),
            'curves': type.ListType(type.StringType()),
            'fips_enforced': type.BooleanType(),
        },
        SetSpec,
        False,
        None))


    class SetSpecEx(VapiStruct):
        """
        The ``Global.SetSpecEx`` class contains the parameters for the custom TLS
        Profile which shall be applied to the appliance.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     protocol_versions=None,
                     curves=None,
                    ):
            """
            :type  protocol_versions: :class:`list` of :class:`Global.ProtocolVersionInfo`
            :param protocol_versions: Defines the list of TLS protocol version and their ciphers
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  curves: :class:`list` of :class:`str`
            :param curves: Defines the TLS Profile curves in IANA form.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.protocol_versions = protocol_versions
            self.curves = curves
            VapiStruct.__init__(self)


    SetSpecEx._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.global.set_spec_ex', {
            'protocol_versions': type.ListType(type.ReferenceType(__name__, 'Global.ProtocolVersionInfo')),
            'curves': type.ListType(type.StringType()),
        },
        SetSpecEx,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Global.Info`` class contains the information about a profile and its
        TLS configuration.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     manual_active=None,
                     spec=None,
                    ):
            """
            :type  manual_active: :class:`bool`
            :param manual_active: Indicates if the current manual TLS parameters are activated for
                the appliance or standard TLS Profile is used instead of them
                This attribute was added in **vSphere API 8.0.3.0**.
            :type  spec: :class:`Global.SetSpec`
            :param spec: Contains information about the configuration.
                This attribute was added in **vSphere API 8.0.3.0**.
            """
            self.manual_active = manual_active
            self.spec = spec
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.global.info', {
            'manual_active': type.BooleanType(),
            'spec': type.ReferenceType(__name__, 'Global.SetSpec'),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Gets the current custom/manual global TLS parameters configured in the
        appliance.
        This method was added in **vSphere API 8.0.3.0**.


        :rtype: :class:`Global.Info`
        :return: The current protocol version, ciphers, and other TLS parameters.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have operator
            privileges.
        """
        return self._invoke('get', None)


    def set_task(self,
            spec,
            ):
        """
        Sets manual/custom TLS parameters globally in the appliance. The result
        of this operation can be queried by calling the cis/tasks/{task-id}
        with the task-id in the response of this call. In case of a VCHA
        enabled cluster, setting a profile expects the VCHA cluster to be
        healthy and in maintenance or disabled mode before proceeding with the
        operation.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Global.SetSpecEx`
        :param spec: Defines the new TLS parameters to be set.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have
            superAdministrator privileges to perform this operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the passed ciphers, curves and protocol version is either empty
            or not valid.
        """
        task_id = self._invoke('set$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Services(VapiInterface):
    """
    ``Services`` class provides methods APIs to configure manual/custom TLS
    parameters for a specific service.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.tls.manual_parameters.services'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ServicesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class ProtocolVersionInfo(VapiStruct):
        """
        The ``Services.ProtocolVersionInfo`` class contains the information about
        the TLS protocol version and its ciphers.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     ciphers=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Defines the TLS protocol version.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  ciphers: :class:`list` of :class:`str`
            :param ciphers: Defines the TLS protocol ciphers in IANA form.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.version = version
            self.ciphers = ciphers
            VapiStruct.__init__(self)


    ProtocolVersionInfo._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.services.protocol_version_info', {
            'version': type.StringType(),
            'ciphers': type.ListType(type.StringType()),
        },
        ProtocolVersionInfo,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``Services.SetSpec`` class contains the information about the TLS
        parameters.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     protocol_versions=None,
                     curves=None,
                    ):
            """
            :type  protocol_versions: :class:`list` of :class:`Services.ProtocolVersionInfo`
            :param protocol_versions: Defines the list of TLS protocol version and their ciphers
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  curves: :class:`list` of :class:`str`
            :param curves: Defines the TLS Profile curves in IANA form.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.protocol_versions = protocol_versions
            self.curves = curves
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.services.set_spec', {
            'protocol_versions': type.ListType(type.ReferenceType(__name__, 'Services.ProtocolVersionInfo')),
            'curves': type.ListType(type.StringType()),
        },
        SetSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Services.Info`` class contains the information about TLS
        configuration of a specific service.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     protocol_versions=None,
                     curves=None,
                     fips_enforced=None,
                    ):
            """
            :type  protocol_versions: :class:`list` of :class:`Services.ProtocolVersionInfo`
            :param protocol_versions: Defines the list of TLS protocol version and their ciphers
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  curves: :class:`list` of :class:`str`
            :param curves: Defines the TLS Profile curves in IANA form.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  fips_enforced: :class:`bool`
            :param fips_enforced: Indicates if FIPS 140-3 compliance is enforced for the TLS Profile.
                This attribute was added in **vSphere API 9.0.0.0**.

                .. deprecated:: vSphere API 9.0.0.0
                    This attribute is deprecated as of **vSphere API 9.0.0.0**. in
                    9.0.0.0 and above all profiles are FIPS compliant, always
                    \\\\@term true.
            """
            self.protocol_versions = protocol_versions
            self.curves = curves
            self.fips_enforced = fips_enforced
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.services.info', {
            'protocol_versions': type.ListType(type.ReferenceType(__name__, 'Services.ProtocolVersionInfo')),
            'curves': type.ListType(type.StringType()),
            'fips_enforced': type.BooleanType(),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Services.ListItem`` class contains the information about the service.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     service=None,
                     info=None,
                    ):
            """
            :type  service: :class:`str`
            :param service: Defines the TLS integrated service.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.tls.manual_parameters.services``. When
                methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.appliance.tls.manual_parameters.services``.
            :type  info: :class:`Services.Info` or ``None``
            :param info: Contains information about the TLS configurations of a specific
                service.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, there is no specific configuration for that service.
            """
            self.service = service
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.services.list_item', {
            'service': type.IdType(resource_types='com.vmware.appliance.tls.manual_parameters.services'),
            'info': type.OptionalType(type.ReferenceType(__name__, 'Services.Info')),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Services.ListResult`` class contains the information about the list
        of services integrated with TLS.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     services=None,
                    ):
            """
            :type  services: :class:`list` of :class:`Services.ListItem`
            :param services: Defines the list of services integrated with TLS and its
                configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.services = services
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.appliance.tls.manual_parameters.services.list_result', {
            'services': type.ListType(type.ReferenceType(__name__, 'Services.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self):
        """
        Gets the list of all the available services integrated with TLS
        Profiles and its configurations.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Services.ListResult`
        :return: The list of all services integrated with TLS Profiles and its
            configurations.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have operator
            privileges.
        """
        return self._invoke('list', None)

    def get(self,
            service,
            ):
        """
        Gets the current TLS parameters configured for a specific service.
        This method was added in **vSphere API 9.0.0.0**.

        :type  service: :class:`str`
        :param service: for which the current TLS parameters has to be fetched.
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.tls.manual_parameters.services``.
        :rtype: :class:`Services.Info`
        :return: the current TLS parameters configured for the passed service.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the service is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have operator
            privileges.
        """
        return self._invoke('get',
                            {
                            'service': service,
                            })


    def set_task(self,
            service,
            spec,
            ):
        """
        Sets manual/custom TLS parameters for a specific service. In case of a
        VCHA enabled cluster, setting a profile expects the VCHA cluster to be
        healthy and in maintenance or disabled mode before proceeding with the
        operation.
        This method was added in **vSphere API 9.0.0.0**.

        :type  service: :class:`str`
        :param service: for which the configured TLS parameters has to be set.
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.tls.manual_parameters.services``.
        :type  spec: :class:`Services.SetSpec`
        :param spec: Defines the new TLS parameters to be set for the passed service.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the service is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have
            superAdministrator privileges to perform this operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the passed ciphers, curves and protocol version is either empty
            or not valid.
        """
        task_id = self._invoke('set$task',
                                {
                                'service': service,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               service,
               ):
        """
        Deletes manual/custom TLS parameters for a specific service. In case of
        a VCHA enabled cluster, deleting a profile expects the VCHA cluster to
        be healthy and in maintenance or disabled mode before proceeding with
        the operation.
        This method was added in **vSphere API 9.0.0.0**.

        :type  service: :class:`str`
        :param service: for which the configured TLS parameters has to be deleted.
            The parameter must be an identifier for the resource type:
            ``com.vmware.appliance.tls.manual_parameters.services``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the service is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is some unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized. User needs to have
            superAdministrator privileges to perform this operation.
        """
        task_id = self._invoke('delete$task',
                                {
                                'service': service,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class _GlobalStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
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
            url_template='/appliance/tls/manual-parameters/global',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Global.SetSpecEx'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/tls/manual-parameters/global',
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
                'output_type': type.ReferenceType(__name__, 'Global.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'set': set_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.tls.manual_parameters.global',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ServicesStub(ApiInterfaceStub):
    def __init__(self, config):
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
            url_template='/appliance/tls/manual-parameters/services',
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
            'service': type.IdType(resource_types='com.vmware.appliance.tls.manual_parameters.services'),
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
            url_template='/appliance/tls/manual-parameters/services/{service}',
            path_variables={
                'service': 'service',
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
            'service': type.IdType(resource_types='com.vmware.appliance.tls.manual_parameters.services'),
            'spec': type.ReferenceType(__name__, 'Services.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/appliance/tls/manual-parameters/services/{service}',
            path_variables={
                'service': 'service',
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
            'service': type.IdType(resource_types='com.vmware.appliance.tls.manual_parameters.services'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/appliance/tls/manual-parameters/services/{service}',
            path_variables={
                'service': 'service',
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
                'output_type': type.ReferenceType(__name__, 'Services.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Services.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.tls.manual_parameters.services',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Global': Global,
        'Services': Services,
    }

