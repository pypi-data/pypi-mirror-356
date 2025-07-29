# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.repository.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.repository_client`` module provides classes to
manage desired state software in the repository.

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


class Software(VapiInterface):
    """
    The ``Software`` class provides methods to manage desired state software
    specifications in the repository.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.repository.software_spec"
    """
    Resource type for software specification

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.repository.software'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SoftwareStub)
        self._VAPI_OPERATION_IDS = {}

    class ExportType(Enum):
        """
        The ``Software.ExportType`` class defines the formats in which software
        specification document or image can be exported.
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
        SOFTWARE_SPEC = None
        """
        Export software specification document.

        """
        ISO_IMAGE = None
        """
        Export ISO image.

        """
        OFFLINE_BUNDLE = None
        """
        Export offline bundle.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ExportType` instance.
            """
            Enum.__init__(string)

    ExportType._set_values({
        'SOFTWARE_SPEC': ExportType('SOFTWARE_SPEC'),
        'ISO_IMAGE': ExportType('ISO_IMAGE'),
        'OFFLINE_BUNDLE': ExportType('OFFLINE_BUNDLE'),
    })
    ExportType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.repository.software.export_type',
        ExportType))


    class SoftwareType(Enum):
        """
        The ``Software.SoftwareType`` class describes whether a software
        specification is Single or Composite.
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
        SINGLE = None
        """
        A software specification of this type contains only one image (default
        image).

        """
        COMPOSITE = None
        """
        A software specification of this type contains one default image and one or
        more alternative images.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SoftwareType` instance.
            """
            Enum.__init__(string)

    SoftwareType._set_values({
        'SINGLE': SoftwareType('SINGLE'),
        'COMPOSITE': SoftwareType('COMPOSITE'),
    })
    SoftwareType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.repository.software.software_type',
        SoftwareType))


    class ExportSpec(VapiStruct):
        """
        The ``Software.ExportSpec`` class contains information describing how a
        software specification or image should be exported.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     export_software_spec=None,
                     export_iso_image=None,
                     export_offline_bundle=None,
                     export_only_default_image=None,
                    ):
            """
            :type  export_software_spec: :class:`bool`
            :param export_software_spec: Whether to export software specification document.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  export_iso_image: :class:`bool`
            :param export_iso_image: Whether to export ISO image.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  export_offline_bundle: :class:`bool`
            :param export_offline_bundle: Whether to export offline bundle.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  export_only_default_image: :class:`bool`
            :param export_only_default_image: Whether to export only default image.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.export_software_spec = export_software_spec
            self.export_iso_image = export_iso_image
            self.export_offline_bundle = export_offline_bundle
            self.export_only_default_image = export_only_default_image
            VapiStruct.__init__(self)


    ExportSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.export_spec', {
            'export_software_spec': type.BooleanType(),
            'export_iso_image': type.BooleanType(),
            'export_offline_bundle': type.BooleanType(),
            'export_only_default_image': type.BooleanType(),
        },
        ExportSpec,
        False,
        None))


    class ClusterInfo(VapiStruct):
        """
        The ``Software.ClusterInfo`` class contains the information about a cluster
        that is assigned a software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     name=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  name: :class:`str`
            :param name: Name of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.name = name
            VapiStruct.__init__(self)


    ClusterInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.cluster_info', {
            'id': type.IdType(resource_types='ClusterComputeResource'),
            'name': type.StringType(),
        },
        ClusterInfo,
        False,
        None))


    class HostInfo(VapiStruct):
        """
        The ``Software.HostInfo`` class contains the information about a standalone
        host that is assigned a software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     name=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the host.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
            :type  name: :class:`str`
            :param name: Name of the host.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.name = name
            VapiStruct.__init__(self)


    HostInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.host_info', {
            'id': type.IdType(resource_types='HostSystem'),
            'name': type.StringType(),
        },
        HostInfo,
        False,
        None))


    class AssignedEntities(VapiStruct):
        """
        The ``Software.AssignedEntities`` class contains the list of entities
        assigned to a software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     clusters=None,
                     hosts=None,
                    ):
            """
            :type  clusters: :class:`list` of :class:`Software.ClusterInfo`
            :param clusters: List of clusters. For a software specification that is not
                associated with any cluster, this list will be empty.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  hosts: :class:`list` of :class:`Software.HostInfo`
            :param hosts: List of hosts. For a software specification that is not associated
                with any host, this list will be empty.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.clusters = clusters
            self.hosts = hosts
            VapiStruct.__init__(self)


    AssignedEntities._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.assigned_entities', {
            'clusters': type.ListType(type.ReferenceType(__name__, 'Software.ClusterInfo')),
            'hosts': type.ListType(type.ReferenceType(__name__, 'Software.HostInfo')),
        },
        AssignedEntities,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Software.Info`` class contains information about a software
        specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                     type=None,
                     software_info=None,
                     software_spec=None,
                     assigned_entities=None,
                     editable=None,
                     creation_time=None,
                     modified_time=None,
                     orchestrator_info=None,
                    ):
            """
            :type  display_name: :class:`str`
            :param display_name: Display name of the software specification. The returned name is
                UTF-8 encoded.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  type: :class:`Software.SoftwareType`
            :param type: The software specification type (Single or Composite).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  software_info: :class:`com.vmware.esx.settings_client.SoftwareInfo`
            :param software_info: Software information associated with the software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  software_spec: :class:`com.vmware.esx.settings_client.SoftwareSpec`
            :param software_spec: Software specification details.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  assigned_entities: :class:`Software.AssignedEntities`
            :param assigned_entities: Entities that have this software specification assigned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  editable: :class:`bool`
            :param editable: If set to true, this software specification can be edited.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Timestamp describing when this software specification was created.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  modified_time: :class:`datetime.datetime`
            :param modified_time: Timestamp describing when this software specification was last
                modified. This timestamp is updated when the #update API is called
                or when a draft of this software specification is committed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  orchestrator_info: :class:`com.vmware.esx.settings_client.OrchestratorInfo`
            :param orchestrator_info: Orchestrator information of the software specification in the
                repository.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.display_name = display_name
            self.type = type
            self.software_info = software_info
            self.software_spec = software_spec
            self.assigned_entities = assigned_entities
            self.editable = editable
            self.creation_time = creation_time
            self.modified_time = modified_time
            self.orchestrator_info = orchestrator_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.info', {
            'display_name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Software.SoftwareType'),
            'software_info': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareInfo'),
            'software_spec': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareSpec'),
            'assigned_entities': type.ReferenceType(__name__, 'Software.AssignedEntities'),
            'editable': type.BooleanType(),
            'creation_time': type.DateTimeType(),
            'modified_time': type.DateTimeType(),
            'orchestrator_info': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'OrchestratorInfo')),
        },
        Info,
        False,
        None))


    class Record(VapiStruct):
        """
        The ``Software.Record`` class contains attributes to describe details
        regarding a software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     display_name=None,
                     type=None,
                     software_info=None,
                     software_spec=None,
                     assigned_entities=None,
                     editable=None,
                     creation_time=None,
                     modified_time=None,
                     orchestrator_info=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Unique identifier of the software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``.
            :type  display_name: :class:`str`
            :param display_name: Display name of the software specification. The returned name is
                UTF-8 encoded.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  type: :class:`Software.SoftwareType`
            :param type: The software specification type (Single or Composite).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  software_info: :class:`com.vmware.esx.settings_client.SoftwareInfo`
            :param software_info: Software information associated with the software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  software_spec: :class:`com.vmware.esx.settings_client.SoftwareSpec`
            :param software_spec: Software specification details.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  assigned_entities: :class:`Software.AssignedEntities`
            :param assigned_entities: Entities that have this software specification assigned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  editable: :class:`bool`
            :param editable: If set to true, this software specification can be edited.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Timestamp describing when this software specification was created.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  modified_time: :class:`datetime.datetime`
            :param modified_time: Timestamp describing when this software specification was last
                modified. This timestamp is updated when the #update API is called
                or when a draft of this software specification is committed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  orchestrator_info: :class:`com.vmware.esx.settings_client.OrchestratorInfo`
            :param orchestrator_info: Orchestrator information of the software specification in the
                repository.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.id = id
            self.display_name = display_name
            self.type = type
            self.software_info = software_info
            self.software_spec = software_spec
            self.assigned_entities = assigned_entities
            self.editable = editable
            self.creation_time = creation_time
            self.modified_time = modified_time
            self.orchestrator_info = orchestrator_info
            VapiStruct.__init__(self)


    Record._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.record', {
            'id': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'display_name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Software.SoftwareType'),
            'software_info': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareInfo'),
            'software_spec': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareSpec'),
            'assigned_entities': type.ReferenceType(__name__, 'Software.AssignedEntities'),
            'editable': type.BooleanType(),
            'creation_time': type.DateTimeType(),
            'modified_time': type.DateTimeType(),
            'orchestrator_info': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'OrchestratorInfo')),
        },
        Record,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Software.ListResult`` class contains the response when listing
        software specifications in the repository. (see :func:`Software.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     records=None,
                    ):
            """
            :type  records: :class:`list` of :class:`Software.Record`
            :param records: List of software specifications.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.records = records
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.list_result', {
            'records': type.ListType(type.ReferenceType(__name__, 'Software.Record')),
        },
        ListResult,
        False,
        None))


    class MatchResult(VapiStruct):
        """
        The ``Software.MatchResult`` contains the result for one matching software
        specification.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     match_types=None,
                     record=None,
                    ):
            """
            :type  match_types: :class:`set` of :class:`Software.MatchResult.MatchType`
            :param match_types: The types of matches.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  record: :class:`Software.Record`
            :param record: The summary of the software specification that matched the user
                input.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.match_types = match_types
            self.record = record
            VapiStruct.__init__(self)


        class MatchType(Enum):
            """
            The ``Software.MatchResult.MatchType`` class defines the types of matches
            that are possible for a software specification.
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
            NAME_MATCH = None
            """
            The status indicates a software specification matching the name in the user
            input was found.

            """
            SOFTWARE_SPEC_MATCH = None
            """
            The status indicates a software specification matching the spec in the user
            input was found.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`MatchType` instance.
                """
                Enum.__init__(string)

        MatchType._set_values({
            'NAME_MATCH': MatchType('NAME_MATCH'),
            'SOFTWARE_SPEC_MATCH': MatchType('SOFTWARE_SPEC_MATCH'),
        })
        MatchType._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.repository.software.match_result.match_type',
            MatchType))

    MatchResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.match_result', {
            'match_types': type.SetType(type.ReferenceType(__name__, 'Software.MatchResult.MatchType')),
            'record': type.ReferenceType(__name__, 'Software.Record'),
        },
        MatchResult,
        False,
        None))


    class CheckResult(VapiStruct):
        """
        The ``Software.CheckResult`` class contains attributes that describe the
        result of a check for a software specification in the repository. see
        :func:`Software.check_repository`
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     matches=None,
                    ):
            """
            :type  matches: :class:`list` of :class:`Software.MatchResult`
            :param matches: The type of match and the summary of one or more software
                specification in the repository if the check found a match. If the
                list is empty, a match was not found for the inputs specified by
                the user.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.matches = matches
            VapiStruct.__init__(self)


    CheckResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.check_result', {
            'matches': type.ListType(type.ReferenceType(__name__, 'Software.MatchResult')),
        },
        CheckResult,
        False,
        None))


    class CheckSpec(VapiStruct):
        """
        The ``Software.CheckSpec`` class contains attributes used to check if a
        matching software specification is found in the repository. For a software
        specification in the repository to be considered a match, it has to match
        one of the fields.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                     software_spec=None,
                    ):
            """
            :type  display_name: :class:`str` or ``None``
            :param display_name: The displayName to check in the repository.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, display names are not checked.
            :type  software_spec: :class:`com.vmware.esx.settings_client.SoftwareSpec` or ``None``
            :param software_spec: The software spec to check in the repository.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, software specs are not checked.
            """
            self.display_name = display_name
            self.software_spec = software_spec
            VapiStruct.__init__(self)


    CheckSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.check_spec', {
            'display_name': type.OptionalType(type.StringType()),
            'software_spec': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareSpec')),
        },
        CheckSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Software.UpdateSpec`` class defines the information used to update a
        software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     display_name=None,
                     orchestrator=None,
                    ):
            """
            :type  display_name: :class:`str` or ``None``
            :param display_name: Display name of the software specification. Supported encoding is
                UTF-8.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the display name is not updated.
            :type  orchestrator: :class:`com.vmware.esx.settings_client.OrchestratorSpec` or ``None``
            :param orchestrator: Orchestrator specification of the software specification in The
                repository.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no orchestrator details is provided with the commit.
            """
            self.display_name = display_name
            self.orchestrator = orchestrator
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.update_spec', {
            'display_name': type.OptionalType(type.StringType()),
            'orchestrator': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'OrchestratorSpec')),
        },
        UpdateSpec,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Software.IterationSpec`` class contains attributes used to break
        results into pages when listing software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                    ):
            """
            """
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.iteration_spec', {
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Software.FilterSpec`` class contains attributes used to filter the
        results when listing software specifications in repository. (see
        :func:`Software.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owners=None,
                     display_names=None,
                    ):
            """
            :type  owners: :class:`set` of :class:`str` or ``None``
            :param owners: Filter software specification in repository based on the image
                owners.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the filter will match all the owners.
            :type  display_names: :class:`set` of :class:`str` or ``None``
            :param display_names: Filter software specification in repository based on the display
                names.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the filter will match all the display names.
            """
            self.owners = owners
            self.display_names = display_names
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.filter_spec', {
            'owners': type.OptionalType(type.SetType(type.StringType())),
            'display_names': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class SortCriteria(VapiStruct):
        """
        The ``Software.SortCriteria`` class contains attributes that determine how
        a list of result items should be sorted by the values of one or more
        properties.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                    ):
            """
            """
            VapiStruct.__init__(self)


    SortCriteria._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.sort_criteria', {
        },
        SortCriteria,
        False,
        None))


    class CopySpec(VapiStruct):
        """
        The ``Software.CopySpec`` class contains attributes that are used to create
        a draft based on an existing software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     delete_existing_draft=None,
                    ):
            """
            :type  delete_existing_draft: :class:`bool` or ``None``
            :param delete_existing_draft: Deletes any existing draft by the user before creating a new draft,
                if deleteExistingDraft is set to TRUE.
                This attribute was added in **vSphere API 9.0.0.0**.
                If deleteExistingDraft is either unset of set to FALSE and there is
                already draft created by the user, an \\\\`AlreadyExists\\\\`
                exception is thrown.
            """
            self.delete_existing_draft = delete_existing_draft
            VapiStruct.__init__(self)


    CopySpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.copy_spec', {
            'delete_existing_draft': type.OptionalType(type.BooleanType()),
        },
        CopySpec,
        False,
        None))


    class EditSpec(VapiStruct):
        """
        The ``Software.EditSpec`` class contains attributes that are used to edit
        the software specification in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     delete_existing_draft=None,
                    ):
            """
            :type  delete_existing_draft: :class:`bool` or ``None``
            :param delete_existing_draft: Deletes any existing draft by the user before creating a new draft,
                if deleteExistingDraft is set to TRUE.
                This attribute was added in **vSphere API 9.0.0.0**.
                If deleteExistingDraft is either unset of set to FALSE and there is
                already draft created by the user, an \\\\`AlreadyExists\\\\`
                exception is thrown.
            """
            self.delete_existing_draft = delete_existing_draft
            VapiStruct.__init__(self)


    EditSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.edit_spec', {
            'delete_existing_draft': type.OptionalType(type.BooleanType()),
        },
        EditSpec,
        False,
        None))



    def delete(self,
               software_spec,
               ):
        """
        Delete the software specification in the repository.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: The identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            If the software specification associated with ``software_spec`` is
            assigned to one or more entities.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('delete',
                            {
                            'software_spec': software_spec,
                            })

    def get(self,
            software_spec,
            ):
        """
        Returns the details of a software specification in the repository.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: The identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :rtype: :class:`Software.Info`
        :return: Information about the software specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('get',
                            {
                            'software_spec': software_spec,
                            })

    def list(self,
             filter=None,
             iterate=None,
             sort=None,
             ):
        """
        Returns the list of software specification in the repository.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Software.FilterSpec` or ``None``
        :param filter: The filter applied to the list of software specification.
            If None, the behavior is equivalent to a
            :class:`Software.FilterSpec` with all attributes None, which means
            all records match the filter.
        :type  iterate: :class:`Software.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the behavior is to retrieve all the records.
        :type  sort: :class:`Software.SortCriteria` or ``None``
        :param sort: The sort criteria applied to the list response.
            If None, the results are not sorted.
        :rtype: :class:`Software.ListResult`
        :return: List of software specification in the repository matching the
            filter.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            'sort': sort,
                            })

    def update(self,
               software_spec,
               spec,
               ):
        """
        Updates the software specification in the repository.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: Identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  spec: :class:`Software.UpdateSpec`
        :param spec: The update specification. Fields set in the update spec are updated
            with the new value passed in the request. The fields that are not
            set (or empty) are ignored.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('update',
                            {
                            'software_spec': software_spec,
                            'spec': spec,
                            })

    def export(self,
               software_spec,
               spec,
               ):
        """
        Exports the software specification document and/or the image.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: Identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  spec: :class:`Software.ExportSpec`
        :param spec: The export specification to specify data types to be exported.
        :rtype: :class:`dict` of :class:`Software.ExportType` and :class:`str`
        :return: A map from export type to URL of the exported data for that type.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('export',
                            {
                            'software_spec': software_spec,
                            'spec': spec,
                            })

    def copy(self,
             software_spec,
             spec,
             ):
        """
        Create a draft based on an existing software specification in the
        repository. A new global draft is created if one doesn't exist already.
        The draft is populated with the details of the existing software
        specification. The draft will have the name and spec of the existing
        software specification. The user should modify these before validating
        and saving the draft. Validating or saving the draft will fail if the
        name and spec are not modified. Upon a successful commit of this draft
        a new software specification in the repository will be created and this
        draft will be deleted.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: Identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  spec: :class:`Software.CopySpec`
        :param spec: The spec to be used to create a draft based on existing software
            specfication in the repository.
        :rtype: :class:`str`
        :return: Identifier of the working copy of the software.
            The return value will be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If there is already a draft created by this user.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('copy',
                            {
                            'software_spec': software_spec,
                            'spec': spec,
                            })

    def edit(self,
             software_spec,
             spec,
             ):
        """
        Edit the software specification in the repository. This operation will
        create a draft of the given software spec if it doesn't exist already.
        Upon a successful commit of this draft the existing software
        specification in the repository will be updated and this draft will be
        deleted.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: Identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  spec: :class:`Software.EditSpec`
        :param spec: The spec to be used to edit the software specification in the
            repository.
        :rtype: :class:`str`
        :return: Identifier of the working copy of the software.
            The return value will be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If there is already a draft created by this user.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is an unknown internal error. The accompanying error
            message will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no software specification associated with
            ``software_spec`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            If the software associated with ``software_spec`` has inventory
            entities assigned to it.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('edit',
                            {
                            'software_spec': software_spec,
                            'spec': spec,
                            })

    def check_repository(self,
                         spec,
                         ):
        """
        Check if the provided software specification or name already exists in
        the repository. If any of the attributes provided in ``spec`` by the
        user matches exactly with a software specification in the repository,
        the software specification is said to already exist. If the software
        specification exists in the repository, this operation will return a
        summary of the software specification.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Software.CheckSpec`
        :param spec: The specification that describes what data needs to be checked in
            the repository.
        :rtype: :class:`Software.CheckResult`
        :return: Complete summary of all the matching software specifications in the
            repository along with the type of match.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If ``spec`` is empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller does not have the necessary privileges.
        """
        return self._invoke('check_repository',
                            {
                            'spec': spec,
                            })
class _SoftwareStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
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
            url_template='/esx/settings/repository/software/{softwareSpec}',
            path_variables={
                'software_spec': 'softwareSpec',
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
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
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

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/repository/software/{softwareSpec}',
            path_variables={
                'software_spec': 'softwareSpec',
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
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Software.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Software.IterationSpec')),
            'sort': type.OptionalType(type.ReferenceType(__name__, 'Software.SortCriteria')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
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
            url_template='/esx/settings/repository/software',
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
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'spec': type.ReferenceType(__name__, 'Software.UpdateSpec'),
        })
        update_error_dict = {
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
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/esx/settings/repository/software/{softwareSpec}',
            request_body_parameter='spec',
            path_variables={
                'software_spec': 'softwareSpec',
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

        # properties for export operation
        export_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'spec': type.ReferenceType(__name__, 'Software.ExportSpec'),
        })
        export_error_dict = {
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
        export_input_value_validator_list = [
        ]
        export_output_validator_list = [
        ]
        export_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/{softwareSpec}?action=export',
            request_body_parameter='spec',
            path_variables={
                'software_spec': 'softwareSpec',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'export',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for copy operation
        copy_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'spec': type.ReferenceType(__name__, 'Software.CopySpec'),
        })
        copy_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
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
        copy_input_value_validator_list = [
        ]
        copy_output_validator_list = [
        ]
        copy_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/{softwareSpec}?action=copy',
            request_body_parameter='spec',
            path_variables={
                'software_spec': 'softwareSpec',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'copy',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for edit operation
        edit_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'spec': type.ReferenceType(__name__, 'Software.EditSpec'),
        })
        edit_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        edit_input_value_validator_list = [
        ]
        edit_output_validator_list = [
        ]
        edit_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/{softwareSpec}?action=edit',
            request_body_parameter='spec',
            path_variables={
                'software_spec': 'softwareSpec',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'edit',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for check_repository operation
        check_repository_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Software.CheckSpec'),
        })
        check_repository_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        check_repository_input_value_validator_list = [
        ]
        check_repository_output_validator_list = [
        ]
        check_repository_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software?action=check-repository',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check-repository',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Software.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Software.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'export': {
                'input_type': export_input_type,
                'output_type': type.MapType(type.ReferenceType(__name__, 'Software.ExportType'), type.URIType()),
                'errors': export_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': export_input_value_validator_list,
                'output_validator_list': export_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'copy': {
                'input_type': copy_input_type,
                'output_type': type.IdType(resource_types='com.vmware.esx.settings.draft'),
                'errors': copy_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': copy_input_value_validator_list,
                'output_validator_list': copy_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'edit': {
                'input_type': edit_input_type,
                'output_type': type.IdType(resource_types='com.vmware.esx.settings.draft'),
                'errors': edit_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': edit_input_value_validator_list,
                'output_validator_list': edit_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check_repository': {
                'input_type': check_repository_input_type,
                'output_type': type.ReferenceType(__name__, 'Software.CheckResult'),
                'errors': check_repository_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': check_repository_input_value_validator_list,
                'output_validator_list': check_repository_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'update': update_rest_metadata,
            'export': export_rest_metadata,
            'copy': copy_rest_metadata,
            'edit': edit_rest_metadata,
            'check_repository': check_repository_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.repository.software',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Software': Software,
        'software': 'com.vmware.esx.settings.repository.software_client.StubFactory',
    }

