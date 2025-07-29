# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.repository.software.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.repository.software_client`` module provides
classes to manage desired state software in the repository.

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


class Drafts(VapiInterface):
    """
    The ``Drafts`` class provides methods to manage working copy of software
    specification in the repository.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.esx.settings.draft"
    """
    Resource type for draft resource

    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.repository.software.drafts'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DraftsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'commit_task': 'commit$task'})
        self._VAPI_OPERATION_IDS.update({'validate_task': 'validate$task'})

    class StatusType(Enum):
        """
        The ``Drafts.StatusType`` class defines possible values of status of a
        software draft. A draft is invalid if a newer version of the original
        software specification has been committed since this draft was created.
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
        VALID = None
        """
        Software draft is valid.

        """
        INVALID = None
        """
        Software draft is invalid.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`StatusType` instance.
            """
            Enum.__init__(string)

    StatusType._set_values({
        'VALID': StatusType('VALID'),
        'INVALID': StatusType('INVALID'),
    })
    StatusType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.repository.software.drafts.status_type',
        StatusType))


    class SourceType(Enum):
        """
        The ``Drafts.SourceType`` class defines possible values of sources to
        import software specification.
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
        PULL = None
        """
        Content is pulled from the URL location. The URL scheme of the value in
        #pullLocation can be http, https or file.

        """
        PUSH = None
        """
        Content was previously uploaded using the file upload endpoint present on
        vCenter appliance. This endpoint is present at
        https://VCENTERFQDN:9087/vum-fileupload URL.

        """
        JSON_STRING = None
        """
        The string representing the content of the software specification.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SourceType` instance.
            """
            Enum.__init__(string)

    SourceType._set_values({
        'PULL': SourceType('PULL'),
        'PUSH': SourceType('PUSH'),
        'JSON_STRING': SourceType('JSON_STRING'),
    })
    SourceType._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.repository.software.drafts.source_type',
        SourceType))


    class ValidateResult(VapiStruct):
        """
        The ``Drafts.ValidateResult`` class contains attributes to describe result
        of validation of desired software specification.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                    ):
            """
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications associated with the validation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.notifications = notifications
            VapiStruct.__init__(self)


    ValidateResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.validate_result', {
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ValidateResult,
        False,
        None))


    class Metadata(VapiStruct):
        """
        The ``Drafts.Metadata`` class defines the metadata information about
        software draft.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owner=None,
                     status=None,
                     creation_time=None,
                    ):
            """
            :type  owner: :class:`str`
            :param owner: Owner of the software draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Drafts.StatusType`
            :param status: Status of the software draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Creation time of the software draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.owner = owner
            self.status = status
            self.creation_time = creation_time
            VapiStruct.__init__(self)


    Metadata._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.metadata', {
            'owner': type.StringType(),
            'status': type.ReferenceType(__name__, 'Drafts.StatusType'),
            'creation_time': type.DateTimeType(),
        },
        Metadata,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Drafts.Info`` class defines the information about software draft.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     metadata=None,
                     display_name=None,
                     software_spec=None,
                     software_info=None,
                    ):
            """
            :type  metadata: :class:`Drafts.Metadata`
            :param metadata: Metadata about the software draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  display_name: :class:`str`
            :param display_name: Display name of the software draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  software_spec: :class:`str`
            :param software_spec: Identifier of the software in the repository for which this draft
                is created.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``.
            :type  software_info: :class:`com.vmware.esx.settings_client.SoftwareInfo`
            :param software_info: Software specification associated with the draft.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.metadata = metadata
            self.display_name = display_name
            self.software_spec = software_spec
            self.software_info = software_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.info', {
            'metadata': type.ReferenceType(__name__, 'Drafts.Metadata'),
            'display_name': type.StringType(),
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'software_info': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareInfo'),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Drafts.FilterSpec`` class contains attributes used to filter the
        results when listing software drafts. See :func:`Drafts.list`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     software_spec_ids=None,
                     owners=None,
                    ):
            """
            :type  software_spec_ids: :class:`set` of :class:`str` or ``None``
            :param software_spec_ids: Software specification identifier for which the draft is created.
                If the software specification identifier is set to -1, global
                software drafts are returned.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``. When methods
                return a value of this class as a return value, the attribute will
                contain identifiers for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``.
                If None or empty, drafts from all software specification
                identifiers are returned.
            :type  owners: :class:`set` of :class:`str` or ``None``
            :param owners: Owners of the drafts.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or empty, drafts from all owners will be returned.
            """
            self.software_spec_ids = software_spec_ids
            self.owners = owners
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.filter_spec', {
            'software_spec_ids': type.OptionalType(type.SetType(type.IdType())),
            'owners': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class CommitSpec(VapiStruct):
        """
        The ``Drafts.CommitSpec`` class contains attributes that are used to create
        a new commit in the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     message=None,
                     orchestrator=None,
                    ):
            """
            :type  message: :class:`str` or ``None``
            :param message: Message to include with the commit. The message is saved as part of
                the software specification's history.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, message is set to empty string.
            :type  orchestrator: :class:`com.vmware.esx.settings_client.OrchestratorSpec` or ``None``
            :param orchestrator: Orchestrator specification of the commit.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no orchestrator details is provided with the commit. 
                
                Note: 
                
                1. It is used by vLCM orchestrators like SDDC Manager to manage the
                desired state. For a non-orchestrator user i.e. a VC user, it must
                be unset. 
                
                2. Setting it prevents other users from modifying the committed
                desired state.
            """
            self.message = message
            self.orchestrator = orchestrator
            VapiStruct.__init__(self)


    CommitSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.commit_spec', {
            'message': type.OptionalType(type.StringType()),
            'orchestrator': type.OptionalType(type.ReferenceType('com.vmware.esx.settings_client', 'OrchestratorSpec')),
        },
        CommitSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``Drafts.CreateSpec`` class contains attributes that are used to create
        a draft of a new software spec in the repository.
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


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.create_spec', {
            'delete_existing_draft': type.OptionalType(type.BooleanType()),
        },
        CreateSpec,
        False,
        None))


    class ImportSpec(VapiStruct):
        """
        The ``Drafts.ImportSpec`` class defines the information used to import the
        desired software specification into the repository.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'source_type',
                {
                    'PULL' : [('location', True)],
                    'PUSH' : [('file_id', True)],
                    'JSON_STRING' : [('software_spec', True)],
                }
            ),
        ]



        def __init__(self,
                     display_name=None,
                     source_type=None,
                     location=None,
                     file_id=None,
                     software_spec=None,
                     delete_existing_draft=None,
                    ):
            """
            :type  display_name: :class:`str`
            :param display_name: Display name for the draft created.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  source_type: :class:`Drafts.SourceType`
            :param source_type: Type of the source to import the desired software specification
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  location: :class:`str`
            :param location: Location of the software specification file to be imported.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``sourceType`` is :attr:`Drafts.SourceType.PULL`.
            :type  file_id: :class:`str`
            :param file_id: File identifier returned by the file upload endpoint after file is
                uploaded.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``sourceType`` is :attr:`Drafts.SourceType.PUSH`.
            :type  software_spec: :class:`str`
            :param software_spec: The JSON string representing the desired software specification.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``sourceType`` is :attr:`Drafts.SourceType.JSON_STRING`.
            :type  delete_existing_draft: :class:`bool` or ``None``
            :param delete_existing_draft: Deletes any existing draft by the user before creating a new draft,
                if deleteExistingDraft is set to TRUE.
                This attribute was added in **vSphere API 9.0.0.0**.
                If deleteExistingDraft is either unset of set to FALSE and there is
                already draft created by the user, an \\\\`AlreadyExists\\\\`
                exception is thrown.
            """
            self.display_name = display_name
            self.source_type = source_type
            self.location = location
            self.file_id = file_id
            self.software_spec = software_spec
            self.delete_existing_draft = delete_existing_draft
            VapiStruct.__init__(self)


    ImportSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.drafts.import_spec', {
            'display_name': type.StringType(),
            'source_type': type.ReferenceType(__name__, 'Drafts.SourceType'),
            'location': type.OptionalType(type.URIType()),
            'file_id': type.OptionalType(type.StringType()),
            'software_spec': type.OptionalType(type.StringType()),
            'delete_existing_draft': type.OptionalType(type.BooleanType()),
        },
        ImportSpec,
        False,
        None))




    def commit_task(self,
               draft,
               spec,
               ):
        """
        Commits the specified draft as the software specification in the
        repository. The result of this operation can be queried by calling the
        cis/tasks/{task-id} where the task-id is the response of this
        operation.
        This method was added in **vSphere API 9.0.0.0**.

        :type  draft: :class:`str`
        :param draft: Identifier of the working copy of the document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :type  spec: :class:`Drafts.CommitSpec`
        :param spec: The spec to be used to create the commit.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no draft associated with ``draft`` in the repository.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the software document fails. The value of the data
            attribute of :class:`com.vmware.vapi.std.errors_client.Error` will
            be a class that contains all the attributes defined in
            :class:`Drafts.ValidateResult`.
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
        task_id = self._invoke('commit$task',
                                {
                                'draft': draft,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.esx.settings.commit'))
        return task_instance

    def create(self,
               spec,
               ):
        """
        Creates a draft of a new software spec in the repository. It will be
        deleted, when the draft is committed successfully. This method will
        create an empty draft.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Drafts.CreateSpec`
        :param spec: The spec to be used to create the draft.
        :rtype: :class:`str`
        :return: Identifier of the working copy of the document.
            The return value will be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If there is already a draft created by this user.
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
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def delete(self,
               draft,
               ):
        """
        Deletes the software draft.
        This method was added in **vSphere API 9.0.0.0**.

        :type  draft: :class:`str`
        :param draft: Identifier of the working copy of the document.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no draft associated with ``draft`` in the repository.
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
                            'draft': draft,
                            })

    def get(self,
            draft,
            ):
        """
        Returns the information about given software draft.
        This method was added in **vSphere API 9.0.0.0**.

        :type  draft: :class:`str`
        :param draft: Identifier of the software draft.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:`Drafts.Info`
        :return: Information about the Software Draft.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no draft associated with ``draft`` in the repository.
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
                            'draft': draft,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about the software drafts for the specified cluster
        that match the :class:`Drafts.FilterSpec`.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Drafts.FilterSpec` or ``None``
        :param filter: Filter to be applied while returning drafts.
            If None, all drafts will be returned.
        :rtype: :class:`dict` of :class:`str` and :class:`Drafts.Info`
        :return: Map of software drafts in the repository keyed by their identifiers
            that match the :class:`Drafts.FilterSpec`.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.draft``.
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
                            })


    def validate_task(self,
                 draft,
                 ):
        """
        Validate the software draft. The result of this operation can be
        queried by calling the cis/tasks/{task-id} where the task-id is the
        response of this operation.
        This method was added in **vSphere API 9.0.0.0**.

        :type  draft: :class:`str`
        :param draft: Identifier of the software draft.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no draft associated with ``draft`` in the repository.
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
        task_id = self._invoke('validate$task',
                                {
                                'draft': draft,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Drafts.ValidateResult'))
        return task_instance

    def import_software_spec(self,
                             spec,
                             ):
        """
        Imports the desired software specification as a new draft.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Drafts.ImportSpec`
        :param spec: Specification to import desired software specification.
        :rtype: :class:`str`
        :return: Identifier of the software draft.
            The return value will be an identifier for the resource type:
            ``com.vmware.esx.settings.draft``.
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
              ``VcIntegrity.lifecycleSoftwareSpecification.Write``.
        """
        return self._invoke('import_software_spec',
                            {
                            'spec': spec,
                            })
class EffectiveComponents(VapiInterface):
    """
    The ``EffectiveComponents`` class provides methods to get effective list of
    components.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.repository.software.effective_components'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EffectiveComponentsStub)
        self._VAPI_OPERATION_IDS = {}

    class FilterSpec(VapiStruct):
        """
        The ``EffectiveComponents.FilterSpec`` class contains the filtering
        specification for :func:`EffectiveComponents.list` operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     with_removed_components=None,
                    ):
            """
            :type  with_removed_components: :class:`bool` or ``None``
            :param with_removed_components: Whether include removed components in the result.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None removed components are not included.
            """
            self.with_removed_components = with_removed_components
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.repository.software.effective_components.filter_spec', {
            'with_removed_components': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))



    def list(self,
             software_spec,
             spec=None,
             ):
        """
        Returns the components that comprise the desired software state.
        This method was added in **vSphere API 9.0.0.0**.

        :type  software_spec: :class:`str`
        :param software_spec: The identifier of the software specification in the repository.
            The parameter must be an identifier for the resource type:
            ``com.vmware.esx.settings.repository.software_spec``.
        :type  spec: :class:`EffectiveComponents.FilterSpec` or ``None``
        :param spec: Filter spec to indicate whether removed components are included.
            If None, removed components are not included.
        :rtype: :class:`dict` of :class:`str` and :class:`com.vmware.esx.settings_client.EffectiveComponentInfo`
        :return: Map of effective components keyed by their identifier.
            The key in the return value :class:`dict` will be an identifier for
            the resource type: ``com.vmware.esx.settings.component``.
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
            If the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires
              ``VcIntegrity.lifecycleSoftwareSpecification.Read``.
        """
        return self._invoke('list',
                            {
                            'software_spec': software_spec,
                            'spec': spec,
                            })
class _DraftsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for commit operation
        commit_input_type = type.StructType('operation-input', {
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
            'spec': type.ReferenceType(__name__, 'Drafts.CommitSpec'),
        })
        commit_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        commit_input_value_validator_list = [
        ]
        commit_output_validator_list = [
        ]
        commit_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/drafts/{draft}?action=commit',
            request_body_parameter='spec',
            path_variables={
                'draft': 'draft',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'commit',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Drafts.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
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
            url_template='/esx/settings/repository/software/drafts',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        delete_error_dict = {
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
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/esx/settings/repository/software/drafts/{draft}',
            path_variables={
                'draft': 'draft',
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
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
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
            url_template='/esx/settings/repository/software/drafts/{draft}',
            path_variables={
                'draft': 'draft',
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
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Drafts.FilterSpec')),
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
            url_template='/esx/settings/repository/software/drafts',
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

        # properties for validate operation
        validate_input_type = type.StructType('operation-input', {
            'draft': type.IdType(resource_types='com.vmware.esx.settings.draft'),
        })
        validate_error_dict = {
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
        validate_input_value_validator_list = [
        ]
        validate_output_validator_list = [
        ]
        validate_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/drafts/{draft}?action=validate',
            path_variables={
                'draft': 'draft',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'validate',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for import_software_spec operation
        import_software_spec_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Drafts.ImportSpec'),
        })
        import_software_spec_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        import_software_spec_input_value_validator_list = [
        ]
        import_software_spec_output_validator_list = [
        ]
        import_software_spec_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/esx/settings/repository/software/drafts?action=import-software-spec',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'import-software-spec',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'commit$task': {
                'input_type': commit_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': commit_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': commit_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.esx.settings.draft'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Drafts.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType(__name__, 'Drafts.Info')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'validate$task': {
                'input_type': validate_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': validate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': validate_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'import_software_spec': {
                'input_type': import_software_spec_input_type,
                'output_type': type.IdType(resource_types='com.vmware.esx.settings.draft'),
                'errors': import_software_spec_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': import_software_spec_input_value_validator_list,
                'output_validator_list': import_software_spec_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'commit': commit_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'validate': validate_rest_metadata,
            'import_software_spec': import_software_spec_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.repository.software.drafts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EffectiveComponentsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'software_spec': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'EffectiveComponents.FilterSpec')),
        })
        list_error_dict = {
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
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/repository/software/{softwareSpec}/effective-components',
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

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.MapType(type.IdType(), type.ReferenceType('com.vmware.esx.settings_client', 'EffectiveComponentInfo')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.repository.software.effective_components',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Drafts': Drafts,
        'EffectiveComponents': EffectiveComponents,
        'alternative_images': 'com.vmware.esx.settings.repository.software.alternative_images_client.StubFactory',
        'drafts': 'com.vmware.esx.settings.repository.software.drafts_client.StubFactory',
    }

