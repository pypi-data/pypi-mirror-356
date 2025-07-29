# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.software.supervisors.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.software.supervisors_client``
module provides classes for managing Supervisor upgrades.

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


class Prechecks(VapiInterface):
    """
    The ``Prechecks`` class provides methods to perform Supervisor upgrade
    pre-checks.
    This class was added in **vSphere API 8.0.3.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.software.supervisors.prechecks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _PrechecksStub)
        self._VAPI_OPERATION_IDS = {}

    class PrecheckSpec(VapiStruct):
        """
        The ``Prechecks.PrecheckSpec`` class contains the specification required to
        run Supervisor upgrade pre-checks.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     target_version=None,
                    ):
            """
            :type  target_version: :class:`str`
            :param target_version: The target version indicates the Supervisor upgrade version against
                which the Supervisor upgrade pre-checks should run, the value for
                this field should be provided from the list of
                :attr:`com.vmware.vcenter.namespace_management.software_client.Clusters.Info.available_versions`.
                This attribute was added in **vSphere API 8.0.3.0**.
            """
            self.target_version = target_version
            VapiStruct.__init__(self)


    PrecheckSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.prechecks.precheck_spec', {
            'target_version': type.StringType(),
        },
        PrecheckSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Prechecks.Info`` class contains detailed information about the
        Supervisor upgrade pre-check results for multiple Supervisor upgrade
        version(s).
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     precheck_results=None,
                    ):
            """
            :type  precheck_results: :class:`list` of :class:`Prechecks.PrecheckResult` or ``None``
            :param precheck_results: Information about Supervisor upgrade pre-check results.
                This attribute was added in **vSphere API 8.0.3.0**.
                If None, the Supervisor upgrade pre-checks did not run or upgrade
                is not available.
            """
            self.precheck_results = precheck_results
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.prechecks.info', {
            'precheck_results': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Prechecks.PrecheckResult'))),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Prechecks.FilterSpec`` class contains request filter(s) for fetching
        the Supervisor upgrade pre-checks.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     target_version=None,
                    ):
            """
            :type  target_version: :class:`str` or ``None``
            :param target_version: Supervisor upgrade version for which pre-check results should be
                queried.
                This attribute was added in **vSphere API 8.0.3.0**.
                If :class:`set`, return the pre-check results only for the
                specified target version. If None, return the pre-check results for
                all the Supervisor upgrade versions against which pre-checks have
                already been executed.
            """
            self.target_version = target_version
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.prechecks.filter_spec', {
            'target_version': type.OptionalType(type.StringType()),
        },
        FilterSpec,
        False,
        None))


    class PrecheckResult(VapiStruct):
        """
        The ``Prechecks.PrecheckResult`` class contains the detailed information
        about Supervisor upgrade pre-checks against individual upgrade version.
        This class was added in **vSphere API 8.0.3.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     target_version=None,
                     status=None,
                     conditions=None,
                    ):
            """
            :type  target_version: :class:`str`
            :param target_version: Represents Supervisor upgrade version for which
                :attr:`Prechecks.PrecheckResult.conditions` belong to.
                This attribute was added in **vSphere API 8.0.3.0**.
            :type  status: :class:`com.vmware.vcenter.namespace_management.supervisors_client.Conditions.ConditionGroup.Status`
            :param status: Represents the consolidated status of Supervisor upgrade
                pre-checks.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  conditions: :class:`list` of :class:`com.vmware.vcenter.namespace_management_client.Clusters.Condition`
            :param conditions: Supervisor upgrade pre-check results for
                :attr:`Prechecks.PrecheckResult.target_version`
                This attribute was added in **vSphere API 8.0.3.0**.
            """
            self.target_version = target_version
            self.status = status
            self.conditions = conditions
            VapiStruct.__init__(self)


    PrecheckResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.prechecks.precheck_result', {
            'target_version': type.StringType(),
            'status': type.OptionalType(type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors_client', 'Conditions.ConditionGroup.Status')),
            'conditions': type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management_client', 'Clusters.Condition')),
        },
        PrecheckResult,
        False,
        None))



    def run(self,
            supervisor,
            spec,
            ):
        """
        Run Supervisor upgrade pre-checks. This operation will initiate
        Supervisor upgrade pre-checks for a specific target version.
        This method was added in **vSphere API 8.0.3.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the supervisor on which upgraded pre-checks are run.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  spec: :class:`Prechecks.PrecheckSpec`
        :param spec: Specification for running Supervisor upgrade pre-checks.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if upgrade is not available for the Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if Supervisor upgrade is in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Supervisor could not be located.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Upgrade privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the  contains invalid details.
        """
        return self._invoke('run',
                            {
                            'supervisor': supervisor,
                            'spec': spec,
                            })

    def get(self,
            supervisor,
            filter=None,
            ):
        """
        Returns information about Supervisor upgrade pre-checks.
        This method was added in **vSphere API 8.0.3.0**.

        :type  supervisor: :class:`str`
        :param supervisor: Identifier for the Supervisor.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  filter: :class:`Prechecks.FilterSpec` or ``None``
        :param filter: Includes specification to fetch pre-check results for specific
            Supervisor upgrade version.
            If :class:`set` returns the pre-check results only for the
            specified target version. If None returns the pre-check results for
            all the versions against which pre-checks ran.
        :rtype: :class:`Prechecks.Info`
        :return: Supervisor upgrade pre-check results.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if Supervisor could not be located or pre-check results not found
            for :attr:`Prechecks.FilterSpec.target_version` or pre-check
            results not found for any available upgrade version(s).
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'supervisor': supervisor,
                            'filter': filter,
                            })
class Versions(VapiInterface):
    """
    The ``Versions`` class provides methods to retrieve available Supervisor
    versions along with detailed information about each version. The list of
    Supervisor versions is computed from both the Supervisor images already
    bundled with the vCenter Server release and the Supervisor images available
    in the Content Library configured with vSphere Namespaces.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.software.supervisors.versions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VersionsStub)
        self._VAPI_OPERATION_IDS = {}

    class Compatibility(Enum):
        """
        The ``Versions.Compatibility`` class represents the compatibility of a
        Supervisor image with the current infrastructure.
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
        COMPATIBLE = None
        """
        The Supervisor image is compatible with the current infrastructure (vCenter
        Server, ESX and NSX versions).

        """
        COMPATIBLE_AND_DEGRADED = None
        """
        The Supervisor image is compatible with the current infrastructure and will
        continue to work after the Supervisor upgrade. However, few new features
        released as part of Supervisor release may not be available until the
        vCenter is upgraded.

        """
        INCOMPATIBLE = None
        """
        The Supervisor image is incompatible with the current infrastructure.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Compatibility` instance.
            """
            Enum.__init__(string)

    Compatibility._set_values({
        'COMPATIBLE': Compatibility('COMPATIBLE'),
        'COMPATIBLE_AND_DEGRADED': Compatibility('COMPATIBLE_AND_DEGRADED'),
        'INCOMPATIBLE': Compatibility('INCOMPATIBLE'),
    })
    Compatibility._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.compatibility',
        Compatibility))


    class Status(Enum):
        """
        The ``Versions.Status`` class represents the supportability status of the
        Supervisor capability with the current infrastructure.
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
        SUPPORTED = None
        """
        The Supervisor capability is supported with the current infrastructure
        (vCenter Server and NSX versions).

        """
        SUPPORTED_AND_DEGRADED = None
        """
        The Supervisor capability is supported in the given Supervisor version but
        it is unavailable with the current infrastructure (vCenter Server and NSX
        versions). However, to make this capability available, the infrastructure
        upgrade is required.

        """
        UNSUPPORTED = None
        """
        The Supervisor capability is not supported with the current infrastructure
        (vCenter Server and NSX versions).

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'SUPPORTED': Status('SUPPORTED'),
        'SUPPORTED_AND_DEGRADED': Status('SUPPORTED_AND_DEGRADED'),
        'UNSUPPORTED': Status('UNSUPPORTED'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.status',
        Status))


    class Capability(VapiStruct):
        """
        The ``Versions.Capability`` class contains the details about the new
        vSphere Namespaces feature and its compatibility with the current
        infrastructure. TODO:VKAL-21206 - Add other fields after analysis, like -
        1. Description of feature. 2. Minimum VC release which supports this
        feature. 3. Dependencies, etc.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     status=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the vSphere Namespaces feature.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Versions.Status`
            :param status: Supportability status of this capability with the current
                infrastructure (vCenter and NSX versions).
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.status = status
            VapiStruct.__init__(self)


    Capability._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.capability', {
            'name': type.StringType(),
            'status': type.ReferenceType(__name__, 'Versions.Status'),
        },
        Capability,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Versions.Info`` class contains the detailed information about a
        Supervisor version.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                     name=None,
                     description=None,
                     release_date=None,
                     release_notes=None,
                     image_source_specs=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Identifier for the Supervisor version.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SupervisorVersion``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SupervisorVersion``.
            :type  name: :class:`str`
            :param name: Name of the Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: Description of the Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Date of Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  release_notes: :class:`str`
            :param release_notes: Details of Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  image_source_specs: :class:`list` of :class:`com.vmware.vcenter.namespace_management.supervisors_client.ImageSourceSpec`
            :param image_source_specs: Details about the source of Supervisor image.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.version = version
            self.name = name
            self.description = description
            self.release_date = release_date
            self.release_notes = release_notes
            self.image_source_specs = image_source_specs
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.info', {
            'version': type.IdType(resource_types='SupervisorVersion'),
            'name': type.StringType(),
            'description': type.StringType(),
            'release_date': type.DateTimeType(),
            'release_notes': type.StringType(),
            'image_source_specs': type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors_client', 'ImageSourceSpec')),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Versions.Summary`` class contains basic information about a
        Supervisor version.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     version=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Identifier for the Supervisor versions.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SupervisorVersion``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SupervisorVersion``.
            """
            self.version = version
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.summary', {
            'version': type.IdType(resource_types='SupervisorVersion'),
        },
        Summary,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Versions.ListResult`` class represents the result of the
        :func:`Versions.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     supervisor_versions=None,
                    ):
            """
            :type  supervisor_versions: :class:`list` of :class:`Versions.Summary`
            :param supervisor_versions: List of all Supervisor versions.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.supervisor_versions = supervisor_versions
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.list_result', {
            'supervisor_versions': type.ListType(type.ReferenceType(__name__, 'Versions.Summary')),
        },
        ListResult,
        False,
        None))


    class CheckCompatibilitySpec(VapiStruct):
        """
        The ``Versions.CheckCompatibilitySpec`` class includes attributes used to
        assess the compatibility of Supervisor version with a particular Cluster,
        Supervisor or list of Zones.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     supervisor=None,
                     zones=None,
                    ):
            """
            :type  cluster: :class:`str` or ``None``
            :param cluster: The cluster ID for which the compatibility of Supervisor version is
                being checked.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If None, the field :attr:`Versions.CheckCompatibilitySpec.zones` or
                :attr:`Versions.CheckCompatibilitySpec.supervisor` should be
                specified.
            :type  supervisor: :class:`str` or ``None``
            :param supervisor: The Supervisor ID for which the compatibility of Supervisor version
                is being checked.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
                If None, the field :attr:`Versions.CheckCompatibilitySpec.cluster`
                or :attr:`Versions.CheckCompatibilitySpec.zones` should be
                specified.
            :type  zones: :class:`list` of :class:`str` or ``None``
            :param zones: List of Zones for which the compatibility of Supervisor version is
                being checked.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the field :attr:`Versions.CheckCompatibilitySpec.cluster`
                or :attr:`Versions.CheckCompatibilitySpec.supervisor` should be
                specified.
            """
            self.cluster = cluster
            self.supervisor = supervisor
            self.zones = zones
            VapiStruct.__init__(self)


    CheckCompatibilitySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.check_compatibility_spec', {
            'cluster': type.OptionalType(type.IdType()),
            'supervisor': type.OptionalType(type.IdType()),
            'zones': type.OptionalType(type.ListType(type.StringType())),
        },
        CheckCompatibilitySpec,
        False,
        None))


    class CompatibilityInfo(VapiStruct):
        """
        The ``Versions.CompatibilityInfo`` class the outcome of the
        :func:`Versions.check_compatibility` method and provides detailed
        information about the compatibility and capabilities of the Supervisor
        version.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'compatibility',
                {
                    'INCOMPATIBLE' : [('incompatibility_reasons', True)],
                    'COMPATIBLE' : [('capabilities', True)],
                    'COMPATIBLE_AND_DEGRADED' : [('capabilities', True)],
                }
            ),
        ]



        def __init__(self,
                     version=None,
                     name=None,
                     description=None,
                     release_date=None,
                     release_notes=None,
                     image_source_specs=None,
                     compatibility=None,
                     incompatibility_reasons=None,
                     capabilities=None,
                    ):
            """
            :type  version: :class:`str`
            :param version: Identifier for the Supervisor version.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``SupervisorVersion``. When methods return a value of this class as
                a return value, the attribute will be an identifier for the
                resource type: ``SupervisorVersion``.
            :type  name: :class:`str`
            :param name: Name of the Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: Description of the Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  release_date: :class:`datetime.datetime`
            :param release_date: Date of Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  release_notes: :class:`str`
            :param release_notes: Details of Supervisor release.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  image_source_specs: :class:`list` of :class:`com.vmware.vcenter.namespace_management.supervisors_client.ImageSourceSpec`
            :param image_source_specs: Details about the source of Supervisor image.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compatibility: :class:`Versions.Compatibility`
            :param compatibility: Indicates the compatibility of Supervisor
                :attr:`Versions.CompatibilityInfo.version` with the current
                infrastructure(vCenter, ESX and NSX).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  incompatibility_reasons: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param incompatibility_reasons: If the compatibility status of Supervisor
                :attr:`Versions.CompatibilityInfo.version` is
                :attr:`Versions.Compatibility.INCOMPATIBLE`, the field
                :attr:`Versions.CompatibilityInfo.incompatibility_reasons`
                represents the list of reasons for incompatibility.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the Supervisor image is compatible with current
                infrastructure.
            :type  capabilities: :class:`list` of :class:`Versions.Capability`
            :param capabilities: Represents the list of capabilities offered with the Supervisor
                :attr:`Versions.CompatibilityInfo.version`.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the Supervisor image is incompatible with current
                infrastructure. Hence, we don't compute capabilities.
            """
            self.version = version
            self.name = name
            self.description = description
            self.release_date = release_date
            self.release_notes = release_notes
            self.image_source_specs = image_source_specs
            self.compatibility = compatibility
            self.incompatibility_reasons = incompatibility_reasons
            self.capabilities = capabilities
            VapiStruct.__init__(self)


    CompatibilityInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.software.supervisors.versions.compatibility_info', {
            'version': type.IdType(resource_types='SupervisorVersion'),
            'name': type.StringType(),
            'description': type.StringType(),
            'release_date': type.DateTimeType(),
            'release_notes': type.StringType(),
            'image_source_specs': type.ListType(type.ReferenceType('com.vmware.vcenter.namespace_management.supervisors_client', 'ImageSourceSpec')),
            'compatibility': type.ReferenceType(__name__, 'Versions.Compatibility'),
            'incompatibility_reasons': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'))),
            'capabilities': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Versions.Capability'))),
        },
        CompatibilityInfo,
        False,
        None))



    def list(self):
        """
        Retrieves the list of all Supervisor versions.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Versions.ListResult`
        :return: List of all Supervisor versions.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('list', None)

    def get(self,
            version,
            ):
        """
        Retrieves detailed information about the requested Supervisor version.
        This method was added in **vSphere API 9.0.0.0**.

        :type  version: :class:`str`
        :param version: Identifier of the Supervisor version.
            The parameter must be an identifier for the resource type:
            ``SupervisorVersion``.
        :rtype: :class:`Versions.Info`
        :return: Information about the requested Supervisor version.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``version`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have System.Read privilege.
        """
        return self._invoke('get',
                            {
                            'version': version,
                            })

    def check_compatibility(self,
                            version,
                            spec=None,
                            ):
        """
        Evaluates the compatibility of the specified Supervisor version with
        the current infrastructure (vCenter, ESX, and NSX). If the Supervisor
        version is compatible, it checks the feature compatibility.
        This method was added in **vSphere API 9.0.0.0**.

        :type  version: :class:`str`
        :param version: Identifier of the Supervisor version.
            The parameter must be an identifier for the resource type:
            ``SupervisorVersion``.
        :type  spec: :class:`Versions.CheckCompatibilitySpec` or ``None``
        :param spec: Specification to compute the compatibility for the provided
            Supervisor version.
            If None, the compatibility check of ESX hosts will be omitted.
        :rtype: :class:`Versions.CompatibilityInfo`
        :return: Compatibility status of Supervisor version with provided ClusterID,
            SupervisorID or Zones along with the list of capabilities and their
            statuses.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``version`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have Namespaces.Manage privilege.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if ``spec`` is populated with multiple fields(Cluster ID,
            Supervisor ID & Zones).
        """
        return self._invoke('check_compatibility',
                            {
                            'version': version,
                            'spec': spec,
                            })
class _PrechecksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for run operation
        run_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'spec': type.ReferenceType(__name__, 'Prechecks.PrecheckSpec'),
        })
        run_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        run_input_value_validator_list = [
        ]
        run_output_validator_list = [
        ]
        run_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/software/supervisors/{supervisor}/prechecks?action=run',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'run',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Prechecks.FilterSpec')),
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
            url_template='/vcenter/namespace-management/software/supervisors/{supervisor}/prechecks',
            request_body_parameter='filter',
            path_variables={
                'supervisor': 'supervisor',
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
            'run': {
                'input_type': run_input_type,
                'output_type': type.VoidType(),
                'errors': run_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': run_input_value_validator_list,
                'output_validator_list': run_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Prechecks.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'run': run_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.software.supervisors.prechecks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VersionsStub(ApiInterfaceStub):
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
            url_template='/vcenter/namespace-management/software/supervisors/versions',
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
            'version': type.IdType(resource_types='SupervisorVersion'),
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
            url_template='/vcenter/namespace-management/software/supervisors/versions/{version}',
            path_variables={
                'version': 'version',
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

        # properties for check_compatibility operation
        check_compatibility_input_type = type.StructType('operation-input', {
            'version': type.IdType(resource_types='SupervisorVersion'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'Versions.CheckCompatibilitySpec')),
        })
        check_compatibility_error_dict = {
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
        check_compatibility_input_value_validator_list = [
        ]
        check_compatibility_output_validator_list = [
        ]
        check_compatibility_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/namespace-management/software/supervisors/versions/{version}?action=check-compatibility',
            path_variables={
                'version': 'version',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-compatibility',
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
                'output_type': type.ReferenceType(__name__, 'Versions.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Versions.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check_compatibility': {
                'input_type': check_compatibility_input_type,
                'output_type': type.ReferenceType(__name__, 'Versions.CompatibilityInfo'),
                'errors': check_compatibility_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': check_compatibility_input_value_validator_list,
                'output_validator_list': check_compatibility_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'check_compatibility': check_compatibility_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.software.supervisors.versions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Prechecks': Prechecks,
        'Versions': Versions,
    }

