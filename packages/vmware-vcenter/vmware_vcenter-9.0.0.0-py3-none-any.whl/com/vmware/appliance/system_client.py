# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.appliance.system.
#---------------------------------------------------------------------------

"""
The ``com.vmware.appliance.system_client`` module provides classes to query the
appliance system information. The module is available starting in vSphere 6.5.

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


class CryptoHash(VapiInterface):
    """
    The ``CryptoHash`` class provides methods to switch systems global crypto
    one-way hash algorithms.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.crypto_hash'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CryptoHashStub)
        self._VAPI_OPERATION_IDS = {}

    class HashModeStatus(Enum):
        """
        ``CryptoHash.HashModeStatus`` class Defines status indicating any pending
        activities for using current hash mode
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
        UP_TO_DATE = None
        """


        """
        RESTART_PENDING = None
        """


        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`HashModeStatus` instance.
            """
            Enum.__init__(string)

    HashModeStatus._set_values({
        'UP_TO_DATE': HashModeStatus('UP_TO_DATE'),
        'RESTART_PENDING': HashModeStatus('RESTART_PENDING'),
    })
    HashModeStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.system.crypto_hash.hash_mode_status',
        HashModeStatus))


    class AlgorithmStatus(Enum):
        """
        ``CryptoHash.AlgorithmStatus`` class Defines status indicating whether all
        algorithms are strong.
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
        STRONG = None
        """


        """
        NOT_STRONG = None
        """


        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`AlgorithmStatus` instance.
            """
            Enum.__init__(string)

    AlgorithmStatus._set_values({
        'STRONG': AlgorithmStatus('STRONG'),
        'NOT_STRONG': AlgorithmStatus('NOT_STRONG'),
    })
    AlgorithmStatus._set_binding_type(type.EnumType(
        'com.vmware.appliance.system.crypto_hash.algorithm_status',
        AlgorithmStatus))


    class Info(VapiStruct):
        """
        ``CryptoHash.Info`` class Structure representing the current crypto hash
        state
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hash_mode=None,
                     algorithm_status=None,
                     hash_algorithms=None,
                     status=None,
                     common_hash=None,
                    ):
            """
            :type  hash_mode: :class:`str`
            :param hash_mode: Hash type representing state of global hash switch Possible values:
                STRONG, COMPATIBLE
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.system.crypto_hash``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.appliance.system.crypto_hash``.
            :type  algorithm_status: :class:`CryptoHash.AlgorithmStatus`
            :param algorithm_status: Status indicating whether all algorithms are strong
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  hash_algorithms: :class:`list` of :class:`str`
            :param hash_algorithms: List of algorithms supported by hashMode
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`CryptoHash.HashModeStatus`
            :param status: Status of current hash mode
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  common_hash: :class:`str`
            :param common_hash: This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.hash_mode = hash_mode
            self.algorithm_status = algorithm_status
            self.hash_algorithms = hash_algorithms
            self.status = status
            self.common_hash = common_hash
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.appliance.system.crypto_hash.info', {
            'hash_mode': type.IdType(resource_types='com.vmware.appliance.system.crypto_hash'),
            'algorithm_status': type.ReferenceType(__name__, 'CryptoHash.AlgorithmStatus'),
            'hash_algorithms': type.ListType(type.StringType()),
            'status': type.ReferenceType(__name__, 'CryptoHash.HashModeStatus'),
            'common_hash': type.StringType(),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Get current system crypto one-way hash settings.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`CryptoHash.Info`
        :return: Current one-way hash settings.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            session is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is not authorized.
        """
        return self._invoke('get', None)
class Storage(VapiInterface):
    """
    ``Storage`` class provides methods Appliance storage configuration
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.storage'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _StorageStub)
        self._VAPI_OPERATION_IDS = {}

    class StorageMapping(VapiStruct):
        """
        The ``Storage.StorageMapping`` class describes the mapping between VCSA
        partitions and the Hard disk numbers visible in the vSphere Web Client.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     disk=None,
                     partition=None,
                     description=None,
                    ):
            """
            :type  disk: :class:`str`
            :param disk: The disk number in the vSphere Web Client.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.appliance.system.storage``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.appliance.system.storage``.
            :type  partition: :class:`str`
            :param partition: Storage partition name.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of partition
                This attribute was added in **vSphere API 6.7**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.disk = disk
            self.partition = partition
            self.description = description
            VapiStruct.__init__(self)


    StorageMapping._set_binding_type(type.StructType(
        'com.vmware.appliance.system.storage.storage_mapping', {
            'disk': type.IdType(resource_types='com.vmware.appliance.system.storage'),
            'partition': type.StringType(),
            'description': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
        },
        StorageMapping,
        False,
        None))


    class StorageChange(VapiStruct):
        """
        The ``Storage.StorageChange`` class describes the changes in capasity of a
        storage partition.
        This class was added in **vSphere API 6.7**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     old_size=None,
                     new_size=None,
                    ):
            """
            :type  old_size: :class:`long`
            :param old_size: Original size of the partition in MB.
                This attribute was added in **vSphere API 6.7**.
            :type  new_size: :class:`long`
            :param new_size: Nedw size of the partition in MB.
                This attribute was added in **vSphere API 6.7**.
            """
            self.old_size = old_size
            self.new_size = new_size
            VapiStruct.__init__(self)


    StorageChange._set_binding_type(type.StructType(
        'com.vmware.appliance.system.storage.storage_change', {
            'old_size': type.IntegerType(),
            'new_size': type.IntegerType(),
        },
        StorageChange,
        False,
        None))



    def list(self):
        """
        Get disk to partition mapping.


        :rtype: :class:`list` of :class:`Storage.StorageMapping`
        :return: list of mapping items
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('list', None)

    def resize(self):
        """
        Resize all partitions to 100 percent of disk size.


        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('resize', None)

    def resize_ex(self):
        """
        Resize all partitions to 100 percent of disk size.
        This method was added in **vSphere API 6.7**.


        :rtype: :class:`dict` of :class:`str` and :class:`Storage.StorageChange`
        :return: List of the partitions with the size before and after resizing
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('resize_ex', None)
class Uptime(VapiInterface):
    """
    ``Uptime`` class provides methods Get the system uptime.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.uptime'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _UptimeStub)
        self._VAPI_OPERATION_IDS = {}


    def get(self):
        """
        Get the system uptime.


        :rtype: :class:`float`
        :return: system uptime
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class Time(VapiInterface):
    """
    ``Time`` class provides methods Gets system time.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.time'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TimeStub)
        self._VAPI_OPERATION_IDS = {}

    class SystemTimeStruct(VapiStruct):
        """
        ``Time.SystemTimeStruct`` class Structure representing the system time.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     seconds_since_epoch=None,
                     date=None,
                     time=None,
                     timezone=None,
                    ):
            """
            :type  seconds_since_epoch: :class:`float`
            :param seconds_since_epoch: seconds since the epoch
            :type  date: :class:`str`
            :param date: date format: Thu 07-31-2014
            :type  time: :class:`str`
            :param time: time format: 18:18:32
            :type  timezone: :class:`str`
            :param timezone: timezone
            """
            self.seconds_since_epoch = seconds_since_epoch
            self.date = date
            self.time = time
            self.timezone = timezone
            VapiStruct.__init__(self)


    SystemTimeStruct._set_binding_type(type.StructType(
        'com.vmware.appliance.system.time.system_time_struct', {
            'seconds_since_epoch': type.DoubleType(),
            'date': type.StringType(),
            'time': type.StringType(),
            'timezone': type.StringType(),
        },
        SystemTimeStruct,
        False,
        None))



    def get(self):
        """
        Get system time.


        :rtype: :class:`Time.SystemTimeStruct`
        :return: System time
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class Version(VapiInterface):
    """
    ``Version`` class provides methods Get the appliance version.
    """

    _VAPI_SERVICE_ID = 'com.vmware.appliance.system.version'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VersionStub)
        self._VAPI_OPERATION_IDS = {}

    class VersionStruct(VapiStruct):
        """
        ``Version.VersionStruct`` class Structure representing appliance version
        information.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     product=None,
                     build=None,
                     type=None,
                     summary=None,
                     releasedate=None,
                     install_time=None,
                     name=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Appliance version.
            :type  product: :class:`str`
            :param product: Appliance name.
            :type  build: :class:`str`
            :param build: Appliance build number.
            :type  type: :class:`str`
            :param type: Type of product. Same product can have different deployment
                options, which is represented by type.
            :type  summary: :class:`str`
            :param summary: Summary of patch (empty string, if the appliance has not been
                patched)
            :type  releasedate: :class:`str`
            :param releasedate: Release date of patch (empty string, if the appliance has not been
                patched)
            :type  install_time: :class:`str`
            :param install_time: Display the date and time when this system was first installed.
                Value will not change on subsequent updates.
            :type  name: :class:`str` or ``None``
            :param name: Appliance release name.
            """
            self.version = version
            self.product = product
            self.build = build
            self.type = type
            self.summary = summary
            self.releasedate = releasedate
            self.install_time = install_time
            self.name = name
            VapiStruct.__init__(self)


    VersionStruct._set_binding_type(type.StructType(
        'com.vmware.appliance.system.version.version_struct', {
            'version': type.StringType(),
            'product': type.StringType(),
            'build': type.StringType(),
            'type': type.StringType(),
            'summary': type.StringType(),
            'releasedate': type.StringType(),
            'install_time': type.StringType(),
            'name': type.OptionalType(type.StringType()),
        },
        VersionStruct,
        False,
        None))



    def get(self):
        """
        Get the version.


        :rtype: :class:`Version.VersionStruct`
        :return: version information about the appliance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            Generic error
        """
        return self._invoke('get', None)
class _CryptoHashStub(ApiInterfaceStub):
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
            url_template='/appliance/system/crypto-hash',
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
                'output_type': type.ReferenceType(__name__, 'CryptoHash.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.crypto_hash',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _StorageStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {})
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/system/storage',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for resize operation
        resize_input_type = type.StructType('operation-input', {})
        resize_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        resize_input_value_validator_list = [
        ]
        resize_output_validator_list = [
        ]
        resize_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/system/storage/resize',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for resize_ex operation
        resize_ex_input_type = type.StructType('operation-input', {})
        resize_ex_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        resize_ex_input_value_validator_list = [
        ]
        resize_ex_output_validator_list = [
        ]
        resize_ex_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/appliance/system/storage?action=resize-ex',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Storage.StorageMapping')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'resize': {
                'input_type': resize_input_type,
                'output_type': type.VoidType(),
                'errors': resize_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': resize_input_value_validator_list,
                'output_validator_list': resize_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'resize_ex': {
                'input_type': resize_ex_input_type,
                'output_type': type.MapType(type.StringType(), type.ReferenceType(__name__, 'Storage.StorageChange')),
                'errors': resize_ex_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': resize_ex_input_value_validator_list,
                'output_validator_list': resize_ex_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'resize': resize_rest_metadata,
            'resize_ex': resize_ex_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.storage',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _UptimeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/system/uptime',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.DoubleType(),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.uptime',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TimeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/system/time',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Time.SystemTimeStruct'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.time',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VersionStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/appliance/system/version',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Version.VersionStruct'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.appliance.system.version',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'CryptoHash': CryptoHash,
        'Storage': Storage,
        'Uptime': Uptime,
        'Time': Time,
        'Version': Version,
        'crypto_hash': 'com.vmware.appliance.system.crypto_hash_client.StubFactory',
        'security': 'com.vmware.appliance.system.security_client.StubFactory',
        'time': 'com.vmware.appliance.system.time_client.StubFactory',
    }

