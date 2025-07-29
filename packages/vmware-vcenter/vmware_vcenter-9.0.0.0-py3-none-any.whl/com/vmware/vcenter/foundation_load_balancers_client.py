# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.foundation_load_balancers.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.foundation_load_balancers_client`` module provides
classes to manage and use Foundation Load Balancers.

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


class Nodes(VapiInterface):
    """
    The ``Nodes`` class provides methods to manager load balancer node(s).
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.FoundationLoadBalancerNode"
    """
    Resource type for load balancer node(s).

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.foundation_load_balancers.nodes'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NodesStub)
        self._VAPI_OPERATION_IDS = {}

    class ListResult(VapiStruct):
        """
        The ``Nodes.ListResult`` class provides a list of identifiers describing
        load balancer node(s).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     load_balancer_nodes=None,
                    ):
            """
            :type  load_balancer_nodes: :class:`set` of :class:`str`
            :param load_balancer_nodes: Identifiers of load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancerNode``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancerNode``.
            """
            self.load_balancer_nodes = load_balancer_nodes
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.nodes.list_result', {
            'load_balancer_nodes': type.SetType(type.IdType()),
        },
        ListResult,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Nodes.Info`` class provides load balancer node description
        information.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     node_info=None,
                    ):
            """
            :type  node_info: :class:`com.vmware.vcenter_client.FoundationLoadBalancers.NodeInfo`
            :param node_info: The nodeInfo
                :class:`com.vmware.vcenter_client.FoundationLoadBalancers.NodeInfo`
                defines load balancer node permanent description information and
                runtime operation information.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.node_info = node_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.nodes.info', {
            'node_info': type.ReferenceType('com.vmware.vcenter_client', 'FoundationLoadBalancers.NodeInfo'),
        },
        Info,
        False,
        None))



    def enter_maintenance_mode(self,
                               foundation_load_balancer,
                               node_id,
                               ):
        """
        Enters load balancer node in maintenance mode.
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :type  node_id: :class:`str`
        :param node_id: identifier of load balancer node to put in maintenance mode.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancerNode``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer or load balancer node is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have "FoundationLoadBalancers.Manage"
            privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``FoundationLoadBalancers.Manage``.
        """
        return self._invoke('enter_maintenance_mode',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            'node_id': node_id,
                            })

    def exit_maintenance_mode(self,
                              foundation_load_balancer,
                              node_id,
                              ):
        """
        Exits load balancer node from maintenance mode.
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :type  node_id: :class:`str`
        :param node_id: identifier of load balancer node to exit from maintenance mode.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancerNode``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer or load balancer node is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have "FoundationLoadBalancers.Manage"
            privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``FoundationLoadBalancers.Manage``.
        """
        return self._invoke('exit_maintenance_mode',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            'node_id': node_id,
                            })

    def redeploy(self,
                 foundation_load_balancer,
                 node_id,
                 ):
        """
        Redeploys load balancer node.
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :type  node_id: :class:`str`
        :param node_id: identifier of load balancer node to redeploy.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancerNode``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer or load balancer node is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the operation is not allowed in the current state.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have "FoundationLoadBalancers.Manage"
            privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``FoundationLoadBalancers.Manage``.
        """
        return self._invoke('redeploy',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            'node_id': node_id,
                            })

    def get(self,
            foundation_load_balancer,
            node_id,
            ):
        """
        Retrieves information about load balancer node.
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :type  node_id: :class:`str`
        :param node_id: identifier of load balancer node to get information.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancerNode``.
        :rtype: :class:`Nodes.Info`
        :return: :class:`Nodes.Info` information about the load balancer node.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer or load balancer node is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the "System.Read" privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            'node_id': node_id,
                            })

    def list(self,
             foundation_load_balancer,
             ):
        """
        Returns load balancer instance contained node(s).
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :rtype: :class:`Nodes.ListResult`
        :return: :class:`Nodes.ListResult` the identifiers of load balancer member
            node(s).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the "System.Read" privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.Read``.
        """
        return self._invoke('list',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            })
class _NodesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for enter_maintenance_mode operation
        enter_maintenance_mode_input_type = type.StructType('operation-input', {
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'node_id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancerNode'),
        })
        enter_maintenance_mode_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        enter_maintenance_mode_input_value_validator_list = [
        ]
        enter_maintenance_mode_output_validator_list = [
        ]
        enter_maintenance_mode_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}/nodes/{nodeId}?action=enter-maintenance-mode',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
                'node_id': 'nodeId',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'enter-maintenance-mode',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for exit_maintenance_mode operation
        exit_maintenance_mode_input_type = type.StructType('operation-input', {
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'node_id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancerNode'),
        })
        exit_maintenance_mode_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        exit_maintenance_mode_input_value_validator_list = [
        ]
        exit_maintenance_mode_output_validator_list = [
        ]
        exit_maintenance_mode_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}/nodes/{nodeId}?action=exit-maintenance-mode',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
                'node_id': 'nodeId',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'exit-maintenance-mode',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for redeploy operation
        redeploy_input_type = type.StructType('operation-input', {
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'node_id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancerNode'),
        })
        redeploy_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        redeploy_input_value_validator_list = [
        ]
        redeploy_output_validator_list = [
        ]
        redeploy_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}/nodes/{nodeId}?action=redeploy',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
                'node_id': 'nodeId',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'redeploy',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'node_id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancerNode'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}/nodes/{nodeId}',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
                'node_id': 'nodeId',
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
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}/nodes',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
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
            'enter_maintenance_mode': {
                'input_type': enter_maintenance_mode_input_type,
                'output_type': type.VoidType(),
                'errors': enter_maintenance_mode_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': enter_maintenance_mode_input_value_validator_list,
                'output_validator_list': enter_maintenance_mode_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'exit_maintenance_mode': {
                'input_type': exit_maintenance_mode_input_type,
                'output_type': type.VoidType(),
                'errors': exit_maintenance_mode_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': exit_maintenance_mode_input_value_validator_list,
                'output_validator_list': exit_maintenance_mode_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'redeploy': {
                'input_type': redeploy_input_type,
                'output_type': type.VoidType(),
                'errors': redeploy_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': redeploy_input_value_validator_list,
                'output_validator_list': redeploy_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Nodes.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Nodes.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'enter_maintenance_mode': enter_maintenance_mode_rest_metadata,
            'exit_maintenance_mode': exit_maintenance_mode_rest_metadata,
            'redeploy': redeploy_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.foundation_load_balancers.nodes',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Nodes': Nodes,
    }

