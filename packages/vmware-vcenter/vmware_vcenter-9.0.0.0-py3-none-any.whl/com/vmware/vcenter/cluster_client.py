# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.cluster.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.cluster_client`` module provides classes for managing
clusters.

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


class EvcMode(VapiInterface):
    """
    The ``EvcMode`` class provides methods to manage ``EvcMode`` settings for a
    cluster.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.cluster.evc_mode'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EvcModeStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'set_task': 'set$task'})
        self._VAPI_OPERATION_IDS.update({'check_set_task': 'check_set$task'})
        self._VAPI_OPERATION_IDS.update({'check_add_host_evc_task': 'check_add_host_evc$task'})

    class SetSpec(VapiStruct):
        """
        Information about configuring or checking ``EvcMode`` for a cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     evc_mode=None,
                    ):
            """
            :type  evc_mode: :class:`com.vmware.vcenter.evc_mode_client.EvcMode` or ``None``
            :param evc_mode: The EvcMode to configure the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                evcMode If the field is None, EvcMode is reset for the cluster.
            """
            self.evc_mode = evc_mode
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.evc_mode.set_spec', {
            'evc_mode': type.OptionalType(type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode')),
        },
        SetSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``EvcMode.Info`` class contains information about the EvcMode
        configured for the cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     evc_mode=None,
                    ):
            """
            :type  evc_mode: :class:`com.vmware.vcenter.evc_mode_client.EvcMode` or ``None``
            :param evc_mode: The EvcMode configured on the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, then the cluster's EvcMode is unset.
            """
            self.evc_mode = evc_mode
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.evc_mode.info', {
            'evc_mode': type.OptionalType(type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode')),
        },
        Info,
        False,
        None))


    class CheckResult(VapiStruct):
        """
        Information returned from operations that check EvcMode based
        compatibility.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     error=None,
                     host_system=None,
                    ):
            """
            :type  error: :class:`com.vmware.vapi.std.errors_client.Error`
            :param error: The error associated with the check.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  host_system: :class:`str` or ``None``
            :param host_system: The host associated with the error.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If None, then the error is not associated with any host.
            """
            self.error = error
            self.host_system = host_system
            VapiStruct.__init__(self)


    CheckResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.evc_mode.check_result', {
            'error': type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'host_system': type.OptionalType(type.IdType()),
        },
        CheckResult,
        False,
        None))




    def set_task(self,
            cluster,
            set_spec,
            ):
        """
        Set or clear EvcMode for a cluster.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: The identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  set_spec: :class:`EvcMode.SetSpec`
        :param set_spec: Information about how to configure cluster's EvcMode.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the input parameters are not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the specified cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``Host.Inventory.EditCluster``.
        """
        task_id = self._invoke('set$task',
                                {
                                'cluster': cluster,
                                'set_spec': set_spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance

    def get(self,
            cluster,
            ):
        """
        Gets the EvcMode associated with a cluster.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: The identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`EvcMode.Info`
        :return: The EvcMode set on the cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the specified cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })


    def check_set_task(self,
                  cluster,
                  set_spec,
                  ):
        """
        Check if an EvcMode can be configured for a cluster.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: The identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  set_spec: :class:`EvcMode.SetSpec`
        :param set_spec: Information about the EvcMode to configure on the cluster.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the setSpec is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the specified cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        task_id = self._invoke('check_set$task',
                                {
                                'cluster': cluster,
                                'set_spec': set_spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.OptionalType(type.ListType(type.ReferenceType(__name__, 'EvcMode.CheckResult'))))
        return task_instance


    def check_add_host_evc_task(self,
                           cluster,
                           create_spec,
                           ):
        """
        Check if a host can be added to a cluster based on the cluster's
        EvcMode.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: The identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  create_spec: :class:`com.vmware.vcenter_client.Host.CreateSpec`
        :param create_spec: Information about how to connect to the host.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the specified cluster is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the host connection is not successful.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.View``.
        """
        task_id = self._invoke('check_add_host_evc$task',
                                {
                                'cluster': cluster,
                                'create_spec': create_spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.OptionalType(type.ListType(type.ReferenceType(__name__, 'EvcMode.CheckResult'))))
        return task_instance
class _EvcModeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'set_spec': type.ReferenceType(__name__, 'EvcMode.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/cluster/{cluster}/evc-mode',
            request_body_parameter='set_spec',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
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
            url_template='/vcenter/cluster/{cluster}/evc-mode',
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

        # properties for check_set operation
        check_set_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'set_spec': type.ReferenceType(__name__, 'EvcMode.SetSpec'),
        })
        check_set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        check_set_input_value_validator_list = [
        ]
        check_set_output_validator_list = [
        ]
        check_set_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/cluster/{cluster}/evc-mode?action=check-set',
            request_body_parameter='set_spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-set',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for check_add_host_evc operation
        check_add_host_evc_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'create_spec': type.ReferenceType('com.vmware.vcenter_client', 'Host.CreateSpec'),
        })
        check_add_host_evc_error_dict = {
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
        check_add_host_evc_input_value_validator_list = [
        ]
        check_add_host_evc_output_validator_list = [
        ]
        check_add_host_evc_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/cluster/{cluster}/evc-mode?action=check-add-host-evc',
            request_body_parameter='create_spec',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-add-host-evc',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'set$task': {
                'input_type': set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'EvcMode.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check_set$task': {
                'input_type': check_set_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': check_set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': check_set_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'check_add_host_evc$task': {
                'input_type': check_add_host_evc_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': check_add_host_evc_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': check_add_host_evc_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'get': get_rest_metadata,
            'check_set': check_set_rest_metadata,
            'check_add_host_evc': check_add_host_evc_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.cluster.evc_mode',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'EvcMode': EvcMode,
    }

