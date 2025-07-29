# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.system.crypto_hash.
#---------------------------------------------------------------------------

"""


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


class Options(VapiInterface):
    """
    The ``Options`` class provides methods to retrieve available crypto hash
    modes
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.crypto_hash.options'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _OptionsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        ``Options.Info`` class Structure representing hash mode and supported hash
        algorithms
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hash_mode=None,
                     hash_algorithms=None,
                    ):
            """
            :type  hash_mode: :class:`str`
            :param hash_mode: Hash mode representing state of global hash switch
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.system.crypto_hash``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.appliance.system.crypto_hash``.
            :type  hash_algorithms: :class:`list` of :class:`str`
            :param hash_algorithms: List of hash algorithms supported for a hash mode
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.hash_mode = hash_mode
            self.hash_algorithms = hash_algorithms
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.system.crypto_hash.options.info', {
            'hash_mode': type.IdType(resource_types='com.vmware.appliance.system.crypto_hash'),
            'hash_algorithms': type.ListType(type.StringType()),
        },
        Info,
        False,
        None))


    class ListResult(VapiStruct):
        """
        List of available hash modes that can be set
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     modes=None,
                    ):
            """
            :type  modes: :class:`list` of :class:`Options.Info`
            :param modes: List of hash mode Info
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.modes = modes
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.appliance.system.crypto_hash.options.list_result', {
            'modes': type.ListType(type.ReferenceType(__name__, 'Options.Info')),
        },
        ListResult,
        False,
        None))



    def list(self):
        """
        Get list of available options for hash mode and supported algorithms
        for each hash mode
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Options.ListResult`
        :return: list of available hash settings
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized.
        """
        return self._invoke('list', None)
class _OptionsStub(ApiInterfaceStub):
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
            url_template='/appliance/system/crypto-hash/options',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Options.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.crypto_hash.options',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Options': Options,
    }

