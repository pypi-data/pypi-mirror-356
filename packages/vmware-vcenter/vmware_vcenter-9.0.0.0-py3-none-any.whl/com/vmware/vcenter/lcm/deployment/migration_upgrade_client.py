# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.deployment.migration_upgrade.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.lcm.deployment.migration_upgrade_client`` module
provides classes for executing migration-based operations.

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


class Status(VapiInterface):
    """
    The ``Status`` class provides methods to retrieve the status information
    about the vCenter Appliance upgrade. 
    
    The vCenter upgrade API is recommended to be used via the "/lcm/api" and
    "/lcm/rest" endpoints and not via the "/api" endpoint. The "/lcm/api" and
    "/lcm/rest" endpoints work correctly on any supported source version,
    allowing monitoring and controlling the upgrade even during the upgrade's
    switchover. In contrast, the "/api" endpoint has certain limitations and
    does not work on all of the older supported source vCenter versions and
    during the upgrade's switchover.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.deployment.migration_upgrade.status'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _StatusStub)
        self._VAPI_OPERATION_IDS = {}

    class State(Enum):
        """
        The ``Status.State`` class defines the various states of the migration
        upgrade process.
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
        INITIALIZING = None
        """
        The upgrade process is initializing with the defined migration
        configuration.

        """
        INITIALIZED = None
        """
        The upgrade process is successfully initialized with the defined migration
        configuration.

        """
        STAGING = None
        """
        The upgrade process is downloading or deploying the new target appliance
        version.

        """
        STAGED = None
        """
        The upgrade process deployed the new version and is ready for the next step
        of the process.

        """
        PREPARING = None
        """
        The upgrade process is replicating the source data to the newly deployed
        target vCenter.

        """
        PREPARED = None
        """
        The upgrade process has prepared the source vCenter for switchover. Most of
        the data has been replicated and the remaining part will be replicated
        during the switchover. There will be only some small delta of the data for
        replication during switchover and thus it is expected the switchover to be
        as fast as possible.

        """
        SWITCHOVER = None
        """
        The upgrade process is switching from the source to the target vCenter.
        This includes disabling the source vCenter (stop and disable services and
        network adapters), powering it off if requested, migrating the network
        identity, and starting the services on the target vCenter.

        """
        UPGRADED = None
        """
        The upgrade process promoted the target appliance successfully and the
        vCenter is successfully running on the new version.

        """
        CANCELING = None
        """
        The upgrade process is canceling. In this state the source vCenter is being
        reverted to the state as it was before the start of the upgrade process.

        """
        CANCELED = None
        """
        The upgrade has been canceled.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`State` instance.
            """
            Enum.__init__(string)

    State._set_values({
        'INITIALIZING': State('INITIALIZING'),
        'INITIALIZED': State('INITIALIZED'),
        'STAGING': State('STAGING'),
        'STAGED': State('STAGED'),
        'PREPARING': State('PREPARING'),
        'PREPARED': State('PREPARED'),
        'SWITCHOVER': State('SWITCHOVER'),
        'UPGRADED': State('UPGRADED'),
        'CANCELING': State('CANCELING'),
        'CANCELED': State('CANCELED'),
    })
    State._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.status.state',
        State))


    class Task(VapiStruct):
        """
        The ``Status.Task`` class contains attributes to describe a particular
        deployment task.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'RUNNING' : [('progress', True), ('start_time', True)],
                    'BLOCKED' : [('progress', True), ('start_time', True)],
                    'SUCCEEDED' : [('progress', True), ('start_time', True), ('end_time', True)],
                    'FAILED' : [('progress', True), ('error', False), ('start_time', True), ('end_time', True)],
                    'CANCELED' : [('progress', True), ('error', False), ('start_time', True), ('end_time', True)],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     progress=None,
                     notifications=None,
                     description=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                    ):
            """
            :type  progress: :class:`com.vmware.cis.task_client.Progress`
            :param progress: The progress info of this deployment task.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``CommonInfo#status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.RUNNING`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.BLOCKED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            :type  notifications: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param notifications: Result of the task.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute will be None if result is not available at the
                current step of the task.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`com.vmware.vcenter.lcm.deployment.common_client.Status`
            :param status: Status of the operation associated with the task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED" or the
                upgrade has been canceled.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None there is no error raised by the upgrade
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.RUNNING`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.BLOCKED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            """
            self.progress = progress
            self.notifications = notifications
            self.description = description
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            VapiStruct.__init__(self)


    Task._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.status.task', {
            'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
            'notifications': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'status': type.ReferenceType('com.vmware.vcenter.lcm.deployment.common_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
        },
        Task,
        False,
        None))


    class UpgradeInfo(VapiStruct):
        """
        The ``Status.UpgradeInfo`` class contains attributes to describe important
        parameters and state of the upgrade process.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     upgrade_to=None,
                     start_switchover=None,
                     pause=None,
                     error=None,
                     remaining_replication_data=None,
                     identifier=None,
                    ):
            """
            :type  upgrade_to: :class:`str` or ``None``
            :param upgrade_to: Indicates to which version the upgrade is being executed or was
                executed.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade process was not initialized.
            :type  start_switchover: :class:`datetime.datetime` or ``None``
            :param start_switchover: Determines if the upgrade process will start the switchover at a
                specific time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade process will execute the switchover operation
                without a delay, once the replication is almost done and the
                upgrade can be executed with the least possible downtime.
            :type  pause: :class:`com.vmware.vcenter.lcm.deployment_client.MigrationUpgrade.PausePolicy` or ``None``
            :param pause: Determines if the upgrade process is set to pause at a specific
                point.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade is not configured to pause.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error that cause the upgrade to fail. In case of
                resume the error is removed. However, in case of cancel the error
                here is left for historical reasons only.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade did not raise any errors.
            :type  remaining_replication_data: :class:`long`
            :param remaining_replication_data: The size of the data (in MB) that is left to be replicated from the
                source vCenter to the target vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  identifier: :class:`str` or ``None``
            :param identifier: A unique identifier assign to an upgrade run. New upgrade run will
                assign new ID.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, there is no upgrade initialized on the vCenter.
            """
            self.upgrade_to = upgrade_to
            self.start_switchover = start_switchover
            self.pause = pause
            self.error = error
            self.remaining_replication_data = remaining_replication_data
            self.identifier = identifier
            VapiStruct.__init__(self)


    UpgradeInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.status.upgrade_info', {
            'upgrade_to': type.OptionalType(type.StringType()),
            'start_switchover': type.OptionalType(type.DateTimeType()),
            'pause': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm.deployment_client', 'MigrationUpgrade.PausePolicy')),
            'error': type.OptionalType(type.AnyErrorType()),
            'remaining_replication_data': type.IntegerType(),
            'identifier': type.OptionalType(type.StringType()),
        },
        UpgradeInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Status.Info`` class contains attributes to describe the state of the
        appliance.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'RUNNING' : [('progress', True), ('start_time', True)],
                    'BLOCKED' : [('progress', True), ('start_time', True)],
                    'SUCCEEDED' : [('progress', True), ('start_time', True), ('end_time', True)],
                    'FAILED' : [('progress', True), ('error', False), ('start_time', True), ('end_time', True)],
                    'CANCELED' : [('progress', True), ('error', False), ('start_time', True), ('end_time', True)],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     subtasks=None,
                     subtask_order=None,
                     current_state=None,
                     desired_state=None,
                     progress=None,
                     notifications=None,
                     upgrade_info=None,
                     last_update_time=None,
                     description=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                    ):
            """
            :type  subtasks: :class:`dict` of :class:`str` and :class:`Status.Task`
            :param subtasks: The map of the upgrade subtasks and their status information.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  subtask_order: :class:`list` of :class:`str`
            :param subtask_order: The ordered list of subtasks for this upgrade operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  current_state: :class:`Status.State` or ``None``
            :param current_state: The current state of migration upgrade process.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None there is no upgrade running in the environment.
            :type  desired_state: :class:`Status.State` or ``None``
            :param desired_state: Desired state of the migration upgrade process.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None there is no configured upgrade in the environment.
            :type  progress: :class:`com.vmware.cis.task_client.Progress`
            :param progress: The progress information of the current upgrade process.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``CommonInfo#status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.RUNNING`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.BLOCKED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            :type  notifications: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param notifications: Notifications containing upgrade infos, errors and warnings.
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set` if an infos, errors or warnings have been
                reported by the upgrade process.
            :type  upgrade_info: :class:`Status.UpgradeInfo`
            :param upgrade_info: The metadata of the upgrade process
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_update_time: :class:`datetime.datetime`
            :param last_update_time: The time when the status has been updated
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`com.vmware.vcenter.lcm.deployment.common_client.Status`
            :param status: Status of the operation associated with the task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED" or the
                upgrade has been canceled.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None there is no error raised by the upgrade
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.RUNNING`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.BLOCKED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.SUCCEEDED`,
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.FAILED`,
                or
                :attr:`com.vmware.vcenter.lcm.deployment.common_client.Status.CANCELED`.
            """
            self.subtasks = subtasks
            self.subtask_order = subtask_order
            self.current_state = current_state
            self.desired_state = desired_state
            self.progress = progress
            self.notifications = notifications
            self.upgrade_info = upgrade_info
            self.last_update_time = last_update_time
            self.description = description
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.status.info', {
            'subtasks': type.MapType(type.StringType(), type.ReferenceType(__name__, 'Status.Task')),
            'subtask_order': type.ListType(type.StringType()),
            'current_state': type.OptionalType(type.ReferenceType(__name__, 'Status.State')),
            'desired_state': type.OptionalType(type.ReferenceType(__name__, 'Status.State')),
            'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
            'notifications': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
            'upgrade_info': type.ReferenceType(__name__, 'Status.UpgradeInfo'),
            'last_update_time': type.DateTimeType(),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'status': type.ReferenceType('com.vmware.vcenter.lcm.deployment.common_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Returns the current status of the vCenter migration upgrade.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Status.Info`
        :return: Info structure containing the status information about the vCenter
            upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the status call. The
            accompanying error message will give more details about the
            failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.View``.
        """
        return self._invoke('get', None)
class _StatusStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/deployment/migration-upgrade/status',
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
                'output_type': type.ReferenceType(__name__, 'Status.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.deployment.migration_upgrade.status',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Status': Status,
    }

