# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter_client`` module provides classes for managing VMware
vSphere environments. The module is available starting in vSphere 6.5.

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


class UsernamePassword(VapiStruct):
    """
    The ``UsernamePassword`` specifies the credentials when username-password
    based authentication is to be used for a service end-point.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 user_name=None,
                 password=None,
                ):
        """
        :type  user_name: :class:`str`
        :param user_name: The username for username-password based authentication.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  password: :class:`str`
        :param password: The password for username-password based authentication.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.user_name = user_name
        self.password = password
        VapiStruct.__init__(self)


UsernamePassword._set_binding_type(type.StructType(
    'com.vmware.vcenter.username_password', {
        'user_name': type.StringType(),
        'password': type.SecretType(),
    },
    UsernamePassword,
    False,
    None))



class Credential(VapiStruct):
    """
    The ``Credential`` provides credential for authentication such as
    username/password or SAML token.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'type',
            {
                'USERNAME_PASSWORD' : [('username_password', True)],
                'SAML_TOKEN' : [('saml_token', True)],
            }
        ),
    ]



    def __init__(self,
                 type=None,
                 username_password=None,
                 saml_token=None,
                ):
        """
        :type  type: :class:`Credential.Type`
        :param type: The type of credential to use for connecting to a VC.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  username_password: :class:`UsernamePassword`
        :param username_password: Username-password details.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``type`` is :attr:`Credential.Type.USERNAME_PASSWORD`.
        :type  saml_token: :class:`str`
        :param saml_token: SAML token details, when using SAML based authentication.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``type`` is :attr:`Credential.Type.SAML_TOKEN`.
        """
        self.type = type
        self.username_password = username_password
        self.saml_token = saml_token
        VapiStruct.__init__(self)


    class Type(Enum):
        """
        The credential type to use for authentication.
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
        USERNAME_PASSWORD = None
        """
        Username-password based authentication is being used.

        """
        SAML_TOKEN = None
        """
        SAML based authentication is being used.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'USERNAME_PASSWORD': Type('USERNAME_PASSWORD'),
        'SAML_TOKEN': Type('SAML_TOKEN'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.credential.type',
        Type))

Credential._set_binding_type(type.StructType(
    'com.vmware.vcenter.credential', {
        'type': type.ReferenceType(__name__, 'Credential.Type'),
        'username_password': type.OptionalType(type.ReferenceType(__name__, 'UsernamePassword')),
        'saml_token': type.OptionalType(type.SecretType()),
    },
    Credential,
    False,
    None))



class ServiceLocator(VapiStruct):
    """
    This data object type specifies the information of a service endpoint as
    well as the parameters needed to locate and login to to the service
    endpoint.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 instance_uuid=None,
                 url=None,
                 credential=None,
                 ssl_thumbprint=None,
                 ssl_certificate=None,
                ):
        """
        :type  instance_uuid: :class:`str`
        :param instance_uuid: Unique ID of the instance to which the service belongs. For
            instances that support the vSphere API, this is the same as the
            value found in vim.AboutInfo#instanceUuid.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  url: :class:`str`
        :param url: URL used to access the service endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  credential: :class:`Credential`
        :param credential: Credential to establish the connection and login to the service.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  ssl_thumbprint: :class:`str` or ``None``
        :param ssl_thumbprint: The sslThumbprint of the service endpoint. Superseded by
            :attr:`ServiceLocator.ssl_certificate`. Note: If both
            ``sslThumbprint`` and ``sslCertificate`` are set, ``sslThumbprint``
            must correspond to the ``sslCertificate``.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None, then ``sslCertificate`` will be checked. If both these
            fields are None, then thumbprint from first connection will be
            trusted.
        :type  ssl_certificate: :class:`str` or ``None``
        :param ssl_certificate: The SSL certificate of the service endpoint in PEM format. A
            replacement for :attr:`ServiceLocator.ssl_thumbprint`. Note: If
            both ``sslThumbprint`` and ``sslCertificate`` are set,
            ``sslThumbprint`` must correspond to the ``sslCertificate``.
            This attribute was added in **vSphere API 9.0.0.0**.
            if None, then remote service endpoint certificate will not be
            verified upon connection.
        """
        self.instance_uuid = instance_uuid
        self.url = url
        self.credential = credential
        self.ssl_thumbprint = ssl_thumbprint
        self.ssl_certificate = ssl_certificate
        VapiStruct.__init__(self)


ServiceLocator._set_binding_type(type.StructType(
    'com.vmware.vcenter.service_locator', {
        'instance_uuid': type.StringType(),
        'url': type.StringType(),
        'credential': type.ReferenceType(__name__, 'Credential'),
        'ssl_thumbprint': type.OptionalType(type.StringType()),
        'ssl_certificate': type.OptionalType(type.StringType()),
    },
    ServiceLocator,
    False,
    None))



class Cluster(VapiInterface):
    """
    The ``Cluster`` class provides methods to manage clusters in the vCenter
    Server.
    """
    RESOURCE_TYPE = "ClusterComputeResource"
    """
    The resource type for the vCenter Cluster

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.cluster'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClusterStub)
        self._VAPI_OPERATION_IDS = {}

    class FilterSpec(VapiStruct):
        """
        The ``Cluster.FilterSpec`` class contains attributes used to filter the
        results when listing clusters (see :func:`Cluster.list`). If multiple
        attributes are specified, only clusters matching all of the attributes
        match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     clusters=None,
                     names=None,
                     folders=None,
                     datacenters=None,
                    ):
            """
            :type  clusters: :class:`set` of :class:`str` or ``None``
            :param clusters: Identifiers of clusters that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, clusters with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that clusters must have to match the filter (see
                :attr:`Cluster.Info.name`).
                If None or empty, clusters with any name match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the cluster for the cluster to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, clusters in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the cluster for the cluster to match
                the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, clusters in any datacenter match the filter.
            """
            self.clusters = clusters
            self.names = names
            self.folders = folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.filter_spec', {
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Cluster.Summary`` class contains commonly used information about a
        cluster in vCenter Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     name=None,
                     ha_enabled=None,
                     drs_enabled=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifier of the cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  name: :class:`str`
            :param name: Name of the cluster.
            :type  ha_enabled: :class:`bool`
            :param ha_enabled: Flag indicating whether the vSphere HA feature is enabled for the
                cluster.
            :type  drs_enabled: :class:`bool`
            :param drs_enabled: Flag indicating whether the vSphere DRS service is enabled for the
                cluster.
            """
            self.cluster = cluster
            self.name = name
            self.ha_enabled = ha_enabled
            self.drs_enabled = drs_enabled
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.summary', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'name': type.StringType(),
            'ha_enabled': type.BooleanType(),
            'drs_enabled': type.BooleanType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Cluster.Info`` class contains information about a cluster in vCenter
        Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     resource_pool=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the cluster
            :type  resource_pool: :class:`str`
            :param resource_pool: Identifier of the root resource pool of the cluster
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
            """
            self.name = name
            self.resource_pool = resource_pool
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.cluster.info', {
            'name': type.StringType(),
            'resource_pool': type.IdType(resource_types='ResourcePool'),
        },
        Info,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) clusters in vCenter matching the :class:`Cluster.FilterSpec`.

        :type  filter: :class:`Cluster.FilterSpec` or ``None``
        :param filter: Specification of matching clusters for which information should be
            returned.
            If None, the behavior is equivalent to a
            :class:`Cluster.FilterSpec` with all attributes None which means
            all clusters match the filter.
        :rtype: :class:`list` of :class:`Cluster.Summary`
        :return: Commonly used information about the clusters matching the
            :class:`Cluster.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 1000 clusters match the :class:`Cluster.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            cluster,
            ):
        """
        Retrieves information about the cluster corresponding to ``cluster``.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`Cluster.Info`
        :return: Information about the cluster associated with ``cluster``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session id is missing from the request or the corresponding
            session object cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ClusterComputeResource`` referenced by the
              parameter ``cluster`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            })
class Datacenter(VapiInterface):
    """
    The ``Datacenter`` class provides methods to manage datacenters in the
    vCenter Server.
    """
    RESOURCE_TYPE = "Datacenter"
    """
    The resource type for the vCenter Datacenter

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.datacenter'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DatacenterStub)
        self._VAPI_OPERATION_IDS = {}

    class CreateSpec(VapiStruct):
        """
        The ``Datacenter.CreateSpec`` class defines the information used to create
        a datacenter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     folder=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the datacenter to be created.
            :type  folder: :class:`str` or ``None``
            :param folder: Datacenter folder in which the new datacenter should be created.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose a suitable
                folder for the datacenter; if a folder cannot be chosen, the
                datacenter creation operation will fail.
            """
            self.name = name
            self.folder = folder
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.datacenter.create_spec', {
            'name': type.StringType(),
            'folder': type.OptionalType(type.IdType()),
        },
        CreateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Datacenter.FilterSpec`` class contains attributes used to filter the
        results when listing datacenters (see :func:`Datacenter.list`). If multiple
        attributes are specified, only datacenters matching all of the attributes
        match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datacenters=None,
                     names=None,
                     folders=None,
                    ):
            """
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Identifiers of datacenters that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, datacenters with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that datacenters must have to match the filter (see
                :attr:`Datacenter.Info.name`).
                If None or empty, datacenters with any name match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the datacenters for the datacenter to
                match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, datacenters in any folder match the filter.
            """
            self.datacenters = datacenters
            self.names = names
            self.folders = folders
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.datacenter.filter_spec', {
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Datacenter.Summary`` class contains commonly used information about a
        datacenter in vCenter Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datacenter=None,
                     name=None,
                    ):
            """
            :type  datacenter: :class:`str`
            :param datacenter: Identifier of the datacenter.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datacenter``.
            :type  name: :class:`str`
            :param name: Name of the datacenter.
            """
            self.datacenter = datacenter
            self.name = name
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.datacenter.summary', {
            'datacenter': type.IdType(resource_types='Datacenter'),
            'name': type.StringType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Datacenter.Info`` class contains information about a datacenter in
        vCenter Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     datastore_folder=None,
                     host_folder=None,
                     network_folder=None,
                     vm_folder=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the datacenter.
            :type  datastore_folder: :class:`str`
            :param datastore_folder: The root datastore folder associated with the datacenter.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
            :type  host_folder: :class:`str`
            :param host_folder: The root host and cluster folder associated with the datacenter.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
            :type  network_folder: :class:`str`
            :param network_folder: The root network folder associated with the datacenter.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
            :type  vm_folder: :class:`str`
            :param vm_folder: The root virtual machine folder associated with the datacenter.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
            """
            self.name = name
            self.datastore_folder = datastore_folder
            self.host_folder = host_folder
            self.network_folder = network_folder
            self.vm_folder = vm_folder
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.datacenter.info', {
            'name': type.StringType(),
            'datastore_folder': type.IdType(resource_types='Folder'),
            'host_folder': type.IdType(resource_types='Folder'),
            'network_folder': type.IdType(resource_types='Folder'),
            'vm_folder': type.IdType(resource_types='Folder'),
        },
        Info,
        False,
        None))



    def create(self,
               spec,
               ):
        """
        Create a new datacenter in the vCenter inventory

        :type  spec: :class:`Datacenter.CreateSpec`
        :param spec: Specification for the new datacenter to be created.
        :rtype: :class:`str`
        :return: The identifier of the newly created datacenter
            The return value will be an identifier for the resource type:
            ``Datacenter``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a datacenter with the same name is already present.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the datacenter name is empty or invalid as per the underlying
            implementation.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the folder is not specified and the system cannot choose a
            suitable one.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the datacenter folder cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def delete(self,
               datacenter,
               force=None,
               ):
        """
        Delete an empty datacenter from the vCenter Server

        :type  datacenter: :class:`str`
        :param datacenter: Identifier of the datacenter to be deleted.
            The parameter must be an identifier for the resource type:
            ``Datacenter``.
        :type  force: :class:`bool` or ``None``
        :param force: If true, delete the datacenter even if it is not empty.
            If None a :class:`com.vmware.vapi.std.errors_client.ResourceInUse`
            exception will be reported if the datacenter is not empty. This is
            the equivalent of passing the value false.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no datacenter associated with ``datacenter`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if the datacenter associated with ``datacenter`` is not empty.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('delete',
                            {
                            'datacenter': datacenter,
                            'force': force,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) datacenters in vCenter matching the
        :class:`Datacenter.FilterSpec`.

        :type  filter: :class:`Datacenter.FilterSpec` or ``None``
        :param filter: Specification of matching datacenters for which information should
            be returned.
            If None, the behavior is equivalent to a
            :class:`Datacenter.FilterSpec` with all attributes None which means
            all datacenters match the filter.
        :rtype: :class:`list` of :class:`Datacenter.Summary`
        :return: Commonly used information about the datacenters matching the
            :class:`Datacenter.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 1000 datacenters match the
            :class:`Datacenter.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            datacenter,
            ):
        """
        Retrieves information about the datacenter corresponding to
        ``datacenter``.

        :type  datacenter: :class:`str`
        :param datacenter: Identifier of the datacenter.
            The parameter must be an identifier for the resource type:
            ``Datacenter``.
        :rtype: :class:`Datacenter.Info`
        :return: Information about the datacenter associated with ``datacenter``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no datacenter associated with ``datacenter`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('get',
                            {
                            'datacenter': datacenter,
                            })
class Datastore(VapiInterface):
    """
    The Datastore class provides methods for manipulating a datastore.
    """
    RESOURCE_TYPE = "Datastore"
    """
    The resource type for the vCenter datastore

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.datastore'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DatastoreStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``Datastore.Type`` class defines the supported types of vCenter
        datastores.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        VMFS = None
        """
        VMware File System (ESX Server only).

        """
        NFS = None
        """
        Network file system v3 (linux & esx servers only).

        """
        NFS41 = None
        """
        Network file system v4.1 (linux & esx servers only).

        """
        CIFS = None
        """
        Common Internet File System.

        """
        VSAN = None
        """
        Virtual SAN (ESX Server only).

        """
        VFFS = None
        """
        Flash Read Cache (ESX Server only).

        """
        VVOL = None
        """
        vSphere Virtual Volume (ESX Server only).

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'VMFS': Type('VMFS'),
        'NFS': Type('NFS'),
        'NFS41': Type('NFS41'),
        'CIFS': Type('CIFS'),
        'VSAN': Type('VSAN'),
        'VFFS': Type('VFFS'),
        'VVOL': Type('VVOL'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.datastore.type',
        Type))


    class Info(VapiStruct):
        """
        The ``Datastore.Info`` class contains information about a datastore.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     type=None,
                     accessible=None,
                     free_space=None,
                     multiple_host_access=None,
                     thin_provisioning_supported=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the datastore.
            :type  type: :class:`Datastore.Type`
            :param type: Type (VMFS, NFS, NFS41, CIFS, VSAN, VFFS, VVOL) of the datastore.
            :type  accessible: :class:`bool`
            :param accessible: Whether or not this datastore is accessible.
            :type  free_space: :class:`long` or ``None``
            :param free_space: Available space of this datastore, in bytes. 
                
                The server periodically updates this value.
                This attribute will be None if the available space of this
                datastore is not known.
            :type  multiple_host_access: :class:`bool`
            :param multiple_host_access: Whether or not more than one host in the datacenter has been
                configured with access to the datastore.
            :type  thin_provisioning_supported: :class:`bool`
            :param thin_provisioning_supported: Whether or not the datastore supports thin provisioning on a per
                file basis. When thin provisioning is used, backing storage is
                lazily allocated.
            """
            self.name = name
            self.type = type
            self.accessible = accessible
            self.free_space = free_space
            self.multiple_host_access = multiple_host_access
            self.thin_provisioning_supported = thin_provisioning_supported
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.datastore.info', {
            'name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Datastore.Type'),
            'accessible': type.BooleanType(),
            'free_space': type.OptionalType(type.IntegerType()),
            'multiple_host_access': type.BooleanType(),
            'thin_provisioning_supported': type.BooleanType(),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Datastore.FilterSpec`` class contains attributes used to filter the
        results when listing datastores (see :func:`Datastore.list`). If multiple
        attributes are specified, only datastores matching all of the attributes
        match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastores=None,
                     names=None,
                     types=None,
                     folders=None,
                     datacenters=None,
                    ):
            """
            :type  datastores: :class:`set` of :class:`str` or ``None``
            :param datastores: Identifiers of datastores that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datastore``.
                If None or empty, datastores with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that datastores must have to match the filter (see
                :attr:`Datastore.Info.name`).
                If None or empty, datastores with any name match the filter.
            :type  types: :class:`set` of :class:`Datastore.Type` or ``None``
            :param types: Types that datastores must have to match the filter (see
                :attr:`Datastore.Summary.type`).
                If None or empty, datastores with any type match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the datastore for the datastore to match
                the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, datastores in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the datastore for the datastore to
                match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, datastores in any datacenter match the filter.
            """
            self.datastores = datastores
            self.names = names
            self.types = types
            self.folders = folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.datastore.filter_spec', {
            'datastores': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'types': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Datastore.Type'))),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Datastore.Summary`` class contains commonly used information about a
        datastore.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                     name=None,
                     type=None,
                     free_space=None,
                     capacity=None,
                    ):
            """
            :type  datastore: :class:`str`
            :param datastore: Identifier of the datastore.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
            :type  name: :class:`str`
            :param name: Name of the datastore.
            :type  type: :class:`Datastore.Type`
            :param type: Type (VMFS, NFS, NFS41, CIFS, VSAN, VFFS, VVOL) of the datatore.
            :type  free_space: :class:`long` or ``None``
            :param free_space: Available space of this datastore, in bytes. 
                
                The server periodically updates this value.
                This attribute will be None if the available space of this
                datastore is not known.
            :type  capacity: :class:`long` or ``None``
            :param capacity: Capacity of this datastore, in bytes. 
                
                The server periodically updates this value.
                This attribute will be None if the capacity of this datastore is
                not known.
            """
            self.datastore = datastore
            self.name = name
            self.type = type
            self.free_space = free_space
            self.capacity = capacity
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.datastore.summary', {
            'datastore': type.IdType(resource_types='Datastore'),
            'name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Datastore.Type'),
            'free_space': type.OptionalType(type.IntegerType()),
            'capacity': type.OptionalType(type.IntegerType()),
        },
        Summary,
        False,
        None))



    def get(self,
            datastore,
            ):
        """
        Retrieves information about the datastore indicated by ``datastore``.

        :type  datastore: :class:`str`
        :param datastore: Identifier of the datastore for which information should be
            retrieved.
            The parameter must be an identifier for the resource type:
            ``Datastore``.
        :rtype: :class:`Datastore.Info`
        :return: Information about the datastore associated with ``datastore``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the datastore indicated by ``datastore`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('get',
                            {
                            'datastore': datastore,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 2500 visible (subject to permission
        checks) datastores in vCenter matching the
        :class:`Datastore.FilterSpec`.

        :type  filter: :class:`Datastore.FilterSpec` or ``None``
        :param filter: Specification of matching datastores for which information should
            be returned.
            If None, the behavior is equivalent to a
            :class:`Datastore.FilterSpec` with all attributes None which means
            all datastores match the filter.
        :rtype: :class:`list` of :class:`Datastore.Summary`
        :return: Commonly used information about the datastores matching the
            :class:`Datastore.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Datastore.FilterSpec.types` attribute contains a
            value that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Datastore.FilterSpec.types` attribute contains a
            value that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 2500 datastores match the
            :class:`Datastore.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })
class EvcModes(VapiInterface):
    """
    The ``EvcModes`` interface provides methods to work with custom EVC
    (Enhanced vMotion Compatibility) modes.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.evc_modes'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _EvcModesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})

    class Source(VapiStruct):
        """
        ``EvcModes.Source`` are the objects used as input in the creation of custom
        ``com.vmware.vcenter.evc_mode_client.EvcMode`` objects.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     service_locator=None,
                     clusters=None,
                     hosts=None,
                    ):
            """
            :type  service_locator: :class:`ServiceLocator` or ``None``
            :param service_locator: The vCenter Server location from which the objects are referenced.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the current vCenter server will be used.
            :type  clusters: :class:`list` of :class:`str` or ``None``
            :param clusters: The clusters to be used as reference objects.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None, then no clusters are used for computing the custom EVC
                mode. At least ne of ``clusters`` or ``hosts`` must be specified.
            :type  hosts: :class:`list` of :class:`str` or ``None``
            :param hosts: The hosts to be used as reference objects.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                If None, then no hosts are used for computing the the custom EVC
                mode. At least one of ``clusters`` or ``hosts`` must be specified.
            """
            self.service_locator = service_locator
            self.clusters = clusters
            self.hosts = hosts
            VapiStruct.__init__(self)


    Source._set_binding_type(type.StructType(
        'com.vmware.vcenter.evc_modes.source', {
            'service_locator': type.OptionalType(type.ReferenceType(__name__, 'ServiceLocator')),
            'clusters': type.OptionalType(type.ListType(type.IdType())),
            'hosts': type.OptionalType(type.ListType(type.IdType())),
        },
        Source,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``EvcModes.CreateSpec`` contains information for creating a custom
        ``com.vmware.vcenter.evc_mode_client.EvcMode``.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     sources=None,
                    ):
            """
            :type  sources: :class:`list` of :class:`EvcModes.Source`
            :param sources: List of all sources to be used for creating a custom EVC mode.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.sources = sources
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.evc_modes.create_spec', {
            'sources': type.ListType(type.ReferenceType(__name__, 'EvcModes.Source')),
        },
        CreateSpec,
        False,
        None))


    class PartitionResult(VapiStruct):
        """
        This class provides information about the CPU
        ``com.vmware.vcenter.evc_mode_client.EvcMode`` and graphics
        ``com.vmware.vcenter.evc_mode_client.EvcMode`` associated with a custom
        ``com.vmware.vcenter.evc_mode_client.EvcMode``.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cpu_evc_mode=None,
                     graphics_evc_mode=None,
                    ):
            """
            :type  cpu_evc_mode: :class:`com.vmware.vcenter.evc_mode_client.EvcMode` or ``None``
            :param cpu_evc_mode: CPU specific EVC mode created from an EVC mode partitioning
                operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, then no CPU EVC mode details were found in
                ``com.vmware.vcenter.evc_mode_client.EvcMode`` object being
                partitioned.
            :type  graphics_evc_mode: :class:`com.vmware.vcenter.evc_mode_client.EvcMode` or ``None``
            :param graphics_evc_mode: Graphics specific EVC mode created from an EVC mode partitioning
                operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, then no Graphics EVC mode details were found in
                ``com.vmware.vcenter.evc_mode_client.EvcMode`` object being
                partitioned.
            """
            self.cpu_evc_mode = cpu_evc_mode
            self.graphics_evc_mode = graphics_evc_mode
            VapiStruct.__init__(self)


    PartitionResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.evc_modes.partition_result', {
            'cpu_evc_mode': type.OptionalType(type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode')),
            'graphics_evc_mode': type.OptionalType(type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode')),
        },
        PartitionResult,
        False,
        None))




    def create_task(self,
               create_spec,
               ):
        """
        Creates a custom ``com.vmware.vcenter.evc_mode_client.EvcMode`` object
        that is returned to the client. The client can then set this EVC mode
        on VMs/Clusters.
        This method was added in **vSphere API 9.0.0.0**.

        :type  create_spec: :class:`EvcModes.CreateSpec`
        :param create_spec: Spec with information about how to create the EvcMode.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is a generic error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the createSpec is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if any vCenter Server is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user does not have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            if the SSL certificate or thumbprint of the remote connection can't
            be validated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.View``.
        """
        task_id = self._invoke('create$task',
                                {
                                'create_spec': create_spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode'))
        return task_instance

    def partition(self,
                  evc_mode,
                  ):
        """
        Partition the EvcMode object into its constituent CPU and graphics
        EvcMode objects.
        This method was added in **vSphere API 9.0.0.0**.

        :type  evc_mode: :class:`com.vmware.vcenter.evc_mode_client.EvcMode`
        :param evc_mode: The EvcMode object to partition.
        :rtype: :class:`EvcModes.PartitionResult`
        :return: Partitioned CPU and graphics mode information for the given
            EvcMode.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is any error in partitioning the EvcMode.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``System.View``.
        """
        return self._invoke('partition',
                            {
                            'evc_mode': evc_mode,
                            })
class Folder(VapiInterface):
    """
    The Folder class provides methods for manipulating a vCenter Server folder.
    """
    RESOURCE_TYPE = "Folder"
    """
    The resource type for the vCenter folder

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.folder'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FolderStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``Folder.Type`` class defines the type of a vCenter Server folder. The
        type of a folder determines what what kinds of children can be contained in
        the folder.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        DATACENTER = None
        """
        A folder that can contain datacenters.

        """
        DATASTORE = None
        """
        A folder that can contain datastores.

        """
        HOST = None
        """
        A folder that can contain compute resources (hosts and clusters).

        """
        NETWORK = None
        """
        A folder that can contain networkds.

        """
        VIRTUAL_MACHINE = None
        """
        A folder that can contain virtual machines.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'DATACENTER': Type('DATACENTER'),
        'DATASTORE': Type('DATASTORE'),
        'HOST': Type('HOST'),
        'NETWORK': Type('NETWORK'),
        'VIRTUAL_MACHINE': Type('VIRTUAL_MACHINE'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.folder.type',
        Type))


    class FilterSpec(VapiStruct):
        """
        The ``Folder.FilterSpec`` class contains attributes used to filter the
        results when listing folders (see :func:`Folder.list`). If multiple
        attributes are specified, only folders matching all of the attributes match
        the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folders=None,
                     names=None,
                     type=None,
                     parent_folders=None,
                     datacenters=None,
                    ):
            """
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Identifiers of folders that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, folders with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that folders must have to match the filter (see
                :attr:`Folder.Summary.name`).
                If None or empty, folders with any name match the filter.
            :type  type: :class:`Folder.Type` or ``None``
            :param type: Type that folders must have to match the filter (see
                :attr:`Folder.Summary.type`).
                If None, folders with any type match the filter.
            :type  parent_folders: :class:`set` of :class:`str` or ``None``
            :param parent_folders: Folders that must contain the folder for the folder to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, folder in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the folder for the folder to match
                the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, folder in any datacenter match the filter.
            """
            self.folders = folders
            self.names = names
            self.type = type
            self.parent_folders = parent_folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.folder.filter_spec', {
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'type': type.OptionalType(type.ReferenceType(__name__, 'Folder.Type')),
            'parent_folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Folder.Summary`` class contains commonly used information about a
        folder.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     name=None,
                     type=None,
                    ):
            """
            :type  folder: :class:`str`
            :param folder: Identifier of the folder.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
            :type  name: :class:`str`
            :param name: Name of the vCenter Server folder.
            :type  type: :class:`Folder.Type`
            :param type: Type (DATACENTER, DATASTORE, HOST, NETWORK, VIRTUAL_MACHINE) of the
                vCenter Server folder.
            """
            self.folder = folder
            self.name = name
            self.type = type
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.folder.summary', {
            'folder': type.IdType(resource_types='Folder'),
            'name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Folder.Type'),
        },
        Summary,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) folders in vCenter matching the :class:`Folder.FilterSpec`.

        :type  filter: :class:`Folder.FilterSpec` or ``None``
        :param filter: Specification of matching folders for which information should be
            returned.
            If None, the behavior is equivalent to a :class:`Folder.FilterSpec`
            with all attributes None which means all folders match the filter.
        :rtype: :class:`list` of :class:`Folder.Summary`
        :return: Commonly used information about the folders matching the
            :class:`Folder.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Folder.FilterSpec.type` attribute contains a value
            that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 1000 folders match the :class:`Folder.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })
class FoundationLoadBalancers(VapiInterface):
    """
    The ``FoundationLoadBalancers`` class provides methods to manage load
    balancers(load balancer means foundation load balancer, the same term "load
    balancer" below has the same meaning) from vCenter Server.
    This class was added in **vSphere API 9.0.0.0**.
    """
    RESOURCE_TYPE = "com.vmware.vcenter.FoundationLoadBalancer"
    """
    Resource type for load balancers.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.foundation_load_balancers'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _FoundationLoadBalancersStub)
        self._VAPI_OPERATION_IDS = {}

    class NodeSize(Enum):
        """
        The ``FoundationLoadBalancers.NodeSize`` class defines the
        cpu/memory/storage resource size to deploy the load balancer node(s).
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
        SMALL = None
        """
        :attr:`FoundationLoadBalancers.NodeSize.SMALL` allocates 2 CPUs, 4 GB
        memory, and 8 GB storage for deployment.

        """
        MEDIUM = None
        """
        :attr:`FoundationLoadBalancers.NodeSize.MEDIUM` allocates 4 CPUs, 8 GB
        memory, and 8 GB storage for deployment.

        """
        LARGE = None
        """
        :attr:`FoundationLoadBalancers.NodeSize.LARGE` allocates 8 CPUs, 12 GB
        memory, and 8 GB storage for deployment.

        """
        X_LARGE = None
        """
        :attr:`FoundationLoadBalancers.NodeSize.X_LARGE` allocates 16 CPUs, 16 GB
        memory, and 8 GB storage for deployment.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`NodeSize` instance.
            """
            Enum.__init__(string)

    NodeSize._set_values({
        'SMALL': NodeSize('SMALL'),
        'MEDIUM': NodeSize('MEDIUM'),
        'LARGE': NodeSize('LARGE'),
        'X_LARGE': NodeSize('X_LARGE'),
    })
    NodeSize._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.node_size',
        NodeSize))


    class MaintenanceMode(Enum):
        """
        ``FoundationLoadBalancers.MaintenanceMode`` class defines maintenance
        status.
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
        ENABLE = None
        """
        Maintenance mode enabled.

        """
        DISABLE = None
        """
        Maintenance mode disabled.

        """
        UNKNOWN = None
        """
        The status means can't get maintenance status successfully.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`MaintenanceMode` instance.
            """
            Enum.__init__(string)

    MaintenanceMode._set_values({
        'ENABLE': MaintenanceMode('ENABLE'),
        'DISABLE': MaintenanceMode('DISABLE'),
        'UNKNOWN': MaintenanceMode('UNKNOWN'),
    })
    MaintenanceMode._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.maintenance_mode',
        MaintenanceMode))


    class HaStatus(Enum):
        """
        The ``FoundationLoadBalancers.HaStatus`` class defines high availability
        status of load balancer node(s).
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
        INVALID = None
        """
        The status means can't get high availability status.

        """
        ACTIVE = None
        """
        High availability status is
        :attr:`FoundationLoadBalancers.HaStatus.ACTIVE`.

        """
        STANDBY = None
        """
        High availability status is
        :attr:`FoundationLoadBalancers.HaStatus.STANDBY`.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`HaStatus` instance.
            """
            Enum.__init__(string)

    HaStatus._set_values({
        'INVALID': HaStatus('INVALID'),
        'ACTIVE': HaStatus('ACTIVE'),
        'STANDBY': HaStatus('STANDBY'),
    })
    HaStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.ha_status',
        HaStatus))


    class UtilizationStatus(Enum):
        """
        The ``FoundationLoadBalancers.UtilizationStatus`` class defines the
        utilization status of a specific indicator.
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
        INVALID = None
        """
        The status means can't get the utilization status.

        """
        GREEN = None
        """
        The utilization status is
        :attr:`FoundationLoadBalancers.UtilizationStatus.GREEN`.

        """
        YELLOW = None
        """
        The utilization status is
        :attr:`FoundationLoadBalancers.UtilizationStatus.YELLOW`.

        """
        RED = None
        """
        The utilization status is
        :attr:`FoundationLoadBalancers.UtilizationStatus.RED`.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`UtilizationStatus` instance.
            """
            Enum.__init__(string)

    UtilizationStatus._set_values({
        'INVALID': UtilizationStatus('INVALID'),
        'GREEN': UtilizationStatus('GREEN'),
        'YELLOW': UtilizationStatus('YELLOW'),
        'RED': UtilizationStatus('RED'),
    })
    UtilizationStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.utilization_status',
        UtilizationStatus))


    class DeploymentStatus(Enum):
        """
        The ``FoundationLoadBalancers.DeploymentStatus`` class describes the
        deployment status of the backend load balancer node(s).
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
        INVALID = None
        """
        The status means can't get deployment status of backend load balancer
        node(s).

        """
        IN_PROGRESS = None
        """
        The deployment process is ongoing.

        """
        SUCCESS = None
        """
        The deployment process is successful.

        """
        ERROR = None
        """
        The deployment process has encountered errors.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`DeploymentStatus` instance.
            """
            Enum.__init__(string)

    DeploymentStatus._set_values({
        'INVALID': DeploymentStatus('INVALID'),
        'IN_PROGRESS': DeploymentStatus('IN_PROGRESS'),
        'SUCCESS': DeploymentStatus('SUCCESS'),
        'ERROR': DeploymentStatus('ERROR'),
    })
    DeploymentStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.deployment_status',
        DeploymentStatus))


    class HealthStatus(Enum):
        """
        The ``FoundationLoadBalancers.HealthStatus`` class defines the load
        balancer workload runtime health status.
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
        INVALID = None
        """
        The status means can't get workload health status.

        """
        GREEN = None
        """
        The load balancer workload health status is healthy.

        """
        YELLOW = None
        """
        The load balancer workload is almost healthy, there are some errors
        occurring in non-critical components.

        """
        RED = None
        """
        The load balancer workload is not healthy, there are some critical errors.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`HealthStatus` instance.
            """
            Enum.__init__(string)

    HealthStatus._set_values({
        'INVALID': HealthStatus('INVALID'),
        'GREEN': HealthStatus('GREEN'),
        'YELLOW': HealthStatus('YELLOW'),
        'RED': HealthStatus('RED'),
    })
    HealthStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.health_status',
        HealthStatus))


    class OperationStatus(Enum):
        """
        The ``FoundationLoadBalancers.OperationStatus`` class defines the
        consolidated operation status in making changes to associated load
        balancer.
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
        SUCCESS = None
        """
        The create/update/redeploy/resize/upgrade operation is successful.

        """
        SETTING = None
        """
        The load balancer is executing operation of creating, updating or
        increasing the number of load balancer, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.SETTING` status.

        """
        SETTING_ERROR = None
        """
        There are some errors occurring in the process of creating or updating load
        balancer, it changes into
        :attr:`FoundationLoadBalancers.OperationStatus.SETTING_ERROR` status.

        """
        REDEPLOYING = None
        """
        The load balancer is executing operation of redeploying, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.REDEPLOYING` status. In such
        status, all other operations which will change the load balancer node
        status are blocked.

        """
        REDEPLOYING_ERROR = None
        """
        There are some errors occurring in redeploying the load balancer node, it
        keeps in :attr:`FoundationLoadBalancers.OperationStatus.REDEPLOYING_ERROR`
        status.

        """
        RESIZING = None
        """
        The load balancer is executing operation of resizing, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.RESIZING` status. In such
        status, all other operations which will change the load balancer status are
        blocked.

        """
        RESIZING_ERROR = None
        """
        There are some errors occurring in resizing load balancer, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.RESIZING_ERROR` status.

        """
        UPGRADING = None
        """
        The load balancer is executing operation of upgrading, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.UPGRADING` status. In such
        status, all other operations which will change the status are blocked.

        """
        UPGRADING_ERROR = None
        """
        There are some errors occurring in upgrading the load balancer, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.UPGRADING_ERROR` status.

        """
        DELETING = None
        """
        The load balancer is executing operation of deleting, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.DELETING` status. In such
        status, all other operations which will change the load balancer status are
        blocked.

        """
        DELETING_ERROR = None
        """
        There are some errors occurring in deleting the load balancer, it keeps in
        :attr:`FoundationLoadBalancers.OperationStatus.DELETING_ERROR` status. In
        such status, all other operations which will change the load balancer
        status are blocked.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`OperationStatus` instance.
            """
            Enum.__init__(string)

    OperationStatus._set_values({
        'SUCCESS': OperationStatus('SUCCESS'),
        'SETTING': OperationStatus('SETTING'),
        'SETTING_ERROR': OperationStatus('SETTING_ERROR'),
        'REDEPLOYING': OperationStatus('REDEPLOYING'),
        'REDEPLOYING_ERROR': OperationStatus('REDEPLOYING_ERROR'),
        'RESIZING': OperationStatus('RESIZING'),
        'RESIZING_ERROR': OperationStatus('RESIZING_ERROR'),
        'UPGRADING': OperationStatus('UPGRADING'),
        'UPGRADING_ERROR': OperationStatus('UPGRADING_ERROR'),
        'DELETING': OperationStatus('DELETING'),
        'DELETING_ERROR': OperationStatus('DELETING_ERROR'),
    })
    OperationStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.foundation_load_balancers.operation_status',
        OperationStatus))


    class SizingSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.SizingSpec`` class defines the capacity of load
        balancer node(s).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reserve_cpu=None,
                     reserve_mem=None,
                     size=None,
                    ):
            """
            :type  reserve_cpu: :class:`bool` or ``None``
            :param reserve_cpu: CPU resource reservation: If set to false, no CPU resource is
                reserved. If set to true, the CPU matching the specified
                :class:`FoundationLoadBalancers.NodeSize` is fully reserved. If the
                load balancer node size :class:`FoundationLoadBalancers.NodeSize`
                is changed, the new size will also be fully reserved. The CPU
                reservation is calculated as 1GHZ \* number of CPUs.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, there is no CPU reserved.
            :type  reserve_mem: :class:`bool` or ``None``
            :param reserve_mem: Memory resource reservation: If set to false, no memory resource is
                reserved. If set to true, the memory matching the specified
                :class:`FoundationLoadBalancers.NodeSize` is fully reserved. If the
                load balancer node size :class:`FoundationLoadBalancers.NodeSize`
                is changed, the new size will also be fully reserved.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, there is no memory reserved.
            :type  size: :class:`FoundationLoadBalancers.NodeSize` or ``None``
            :param size: Deployment size of load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, its default value is MEDIUM.
            """
            self.reserve_cpu = reserve_cpu
            self.reserve_mem = reserve_mem
            self.size = size
            VapiStruct.__init__(self)


    SizingSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.sizing_spec', {
            'reserve_cpu': type.OptionalType(type.BooleanType()),
            'reserve_mem': type.OptionalType(type.BooleanType()),
            'size': type.OptionalType(type.ReferenceType(__name__, 'FoundationLoadBalancers.NodeSize')),
        },
        SizingSpec,
        False,
        None))


    class PlacementSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.PlacementSpec`` class defines the location
        information of the load balancer node(s).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     res_pool=None,
                     storage_policy=None,
                     folder=None,
                    ):
            """
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster where the load balancer node(s) should be placed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                This field is currently required, alternative configuration may be
                supported in the future, if this attribute is None, it may indicate
                support for cross-cluster functionality.
            :type  res_pool: :class:`str` or ``None``
            :param res_pool: Resource pool where the load balancer node(s) should be placed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                In the future, if this attribute is None, the system will attempt
                to choose a suitable resource pool for the load balancer node(s),
                if a resource pool can't be chosen, the load balancer node(s)
                creation operation will fail.
            :type  storage_policy: :class:`str` or ``None``
            :param storage_policy: Identifier of the storage policy which should be associated with
                the load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.StoragePolicy``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.StoragePolicy``.
                This field is required for now, In the future, if this attribute is
                None, it means customer specify datastore directly.
            :type  folder: :class:`str` or ``None``
            :param folder: The folder where load balancer node(s) should be placed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If this attribute is None, the load balancer node(s) will stay in
                the current folder.
            """
            self.cluster = cluster
            self.res_pool = res_pool
            self.storage_policy = storage_policy
            self.folder = folder
            VapiStruct.__init__(self)


    PlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.placement_spec', {
            'cluster': type.OptionalType(type.IdType()),
            'res_pool': type.OptionalType(type.IdType()),
            'storage_policy': type.OptionalType(type.IdType()),
            'folder': type.OptionalType(type.IdType()),
        },
        PlacementSpec,
        False,
        None))


    class LoadBalancerController(VapiStruct):
        """
        The ``FoundationLoadBalancers.LoadBalancerController`` class defines the
        load balancer controller server network connection information.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     address=None,
                     port=None,
                    ):
            """
            :type  address: :class:`str`
            :param address: The load balancer server IP address, e.g., 10.0.0.1.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  port: :class:`long`
            :param port: The load balancer controller server port.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.address = address
            self.port = port
            VapiStruct.__init__(self)


    LoadBalancerController._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.load_balancer_controller', {
            'address': type.StringType(),
            'port': type.IntegerType(),
        },
        LoadBalancerController,
        False,
        None))


    class DNS(VapiStruct):
        """
        The ``FoundationLoadBalancers.DNS`` class describes DNS servers and search
        domains for a given network.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     servers=None,
                     search_domains=None,
                    ):
            """
            :type  servers: :class:`list` of :class:`str` or ``None``
            :param servers: The DNS server IP addresses of the load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the servers keep unchanged.
            :type  search_domains: :class:`list` of :class:`str` or ``None``
            :param search_domains: DNS search domains.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the search domains keep unchanged.
            """
            self.servers = servers
            self.search_domains = search_domains
            VapiStruct.__init__(self)


    DNS._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.DNS', {
            'servers': type.OptionalType(type.ListType(type.StringType())),
            'search_domains': type.OptionalType(type.ListType(type.StringType())),
        },
        DNS,
        False,
        None))


    class NetworkConfigSpec(VapiStruct):
        """
        The ``FoundationLoadBalancers.NetworkConfigSpec`` class defines load
        balancer node(s) network configuration.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ntp_servers=None,
                     dns=None,
                     extra_vip_subnets=None,
                    ):
            """
            :type  ntp_servers: :class:`list` of :class:`str` or ``None``
            :param ntp_servers: The NTP server IP addresses of the load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the ntpServers keep unchanged on load balancer node(s).
            :type  dns: :class:`FoundationLoadBalancers.DNS` or ``None``
            :param dns: The DNS servers and search domains for a given network.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the servers and search domains keep unchanged on load
                balancer node(s).
            :type  extra_vip_subnets: :class:`list` of :class:`str` or ``None``
            :param extra_vip_subnets: The extra VIP subnets of the load balancer node(s) in CIDR format.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the extraVipSubnets keep unchanged on load balancer
                node(s).
            """
            self.ntp_servers = ntp_servers
            self.dns = dns
            self.extra_vip_subnets = extra_vip_subnets
            VapiStruct.__init__(self)


    NetworkConfigSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.network_config_spec', {
            'ntp_servers': type.OptionalType(type.ListType(type.StringType())),
            'dns': type.OptionalType(type.ReferenceType(__name__, 'FoundationLoadBalancers.DNS')),
            'extra_vip_subnets': type.OptionalType(type.ListType(type.StringType())),
        },
        NetworkConfigSpec,
        False,
        None))


    class LogConfigSpec(VapiStruct):
        """
        The ``FoundationLoadBalancers.LogConfigSpec`` class defines the load
        balancer log configuration.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     log_verbosity=None,
                     syslog_server=None,
                    ):
            """
            :type  log_verbosity: :class:`FoundationLoadBalancers.LogConfigSpec.LogLevel` or ``None``
            :param log_verbosity: Node log level for logging specified events.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default value is INFO.
            :type  syslog_server: :class:`str` or ``None``
            :param syslog_server: Syslog server forwarding configuration, its format follows
                protocol://hostname|ipv4[:port]. The protocol can be tcp, udp or
                tls. 'tcp' means transmission of log to server via TCP channel,
                'udp' means transmission log to server via UDP channel, 'tls' means
                transmission via a TLS-encrypted channel.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default value is empty, it won't forward log to syslog
                server.
            """
            self.log_verbosity = log_verbosity
            self.syslog_server = syslog_server
            VapiStruct.__init__(self)


        class LogLevel(Enum):
            """
            The ``FoundationLoadBalancers.LogConfigSpec.LogLevel`` class defines log
            level.
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
            DEBUG = None
            """
            Debug level.

            """
            INFO = None
            """
            Info level.

            """
            NOTICE = None
            """
            Notice level.

            """
            WARNING = None
            """
            Warning level.

            """
            ERROR = None
            """
            Error level.

            """
            CRITICAL = None
            """
            Critical level.

            """
            FATAL = None
            """
            Fatal level.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`LogLevel` instance.
                """
                Enum.__init__(string)

        LogLevel._set_values({
            'DEBUG': LogLevel('DEBUG'),
            'INFO': LogLevel('INFO'),
            'NOTICE': LogLevel('NOTICE'),
            'WARNING': LogLevel('WARNING'),
            'ERROR': LogLevel('ERROR'),
            'CRITICAL': LogLevel('CRITICAL'),
            'FATAL': LogLevel('FATAL'),
        })
        LogLevel._set_binding_type(type.EnumType(
            'com.vmware.vcenter.foundation_load_balancers.log_config_spec.log_level',
            LogLevel))

    LogConfigSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.log_config_spec', {
            'log_verbosity': type.OptionalType(type.ReferenceType(__name__, 'FoundationLoadBalancers.LogConfigSpec.LogLevel')),
            'syslog_server': type.OptionalType(type.StringType()),
        },
        LogConfigSpec,
        False,
        None))


    class IpAddressSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.IpAddressSpec`` class defines IP address
        configuration.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     type=None,
                     ip_address=None,
                     prefix=None,
                     personas=None,
                     gateway=None,
                    ):
            """
            :type  type: :class:`FoundationLoadBalancers.IpAddressSpec.Type`
            :param type: IP address assignment method.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  ip_address: :class:`str` or ``None``
            :param ip_address: IP address assigned to the node.
                This attribute was added in **vSphere API 9.0.0.0**.
                The field is required when assigning a STATIC type of IP address
                and skipped when assigning a DHCP type of IP address. The field is
                automatically populated with currently requested DHCP IP address.
            :type  prefix: :class:`long` or ``None``
            :param prefix: IP address prefix length.
                This attribute was added in **vSphere API 9.0.0.0**.
                The field is required when assigning a STATIC IP address and
                skipped when assigning a DHCP IP address.
            :type  personas: :class:`list` of :class:`FoundationLoadBalancers.IpAddressSpec.Persona` or ``None``
            :param personas: The network interface role, it can contain multiple roles used for
                different scenarios.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, keep current configuration unset or unchanged.
            :type  gateway: :class:`str` or ``None``
            :param gateway: The default gateway address of the load balancer node, address in
                CIDR format, e.g., 10.0.0.1/24.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default gateway keeps unset or unchanged.
            """
            self.type = type
            self.ip_address = ip_address
            self.prefix = prefix
            self.personas = personas
            self.gateway = gateway
            VapiStruct.__init__(self)


        class Type(Enum):
            """
            ``FoundationLoadBalancers.IpAddressSpec.Type`` class defines ways to setup
            IP address.
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
            DHCP = None
            """
            IP address is automatically assigned by a DHCP server.

            """
            STATIC = None
            """
            IP address is manually assigned.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Type` instance.
                """
                Enum.__init__(string)

        Type._set_values({
            'DHCP': Type('DHCP'),
            'STATIC': Type('STATIC'),
        })
        Type._set_binding_type(type.EnumType(
            'com.vmware.vcenter.foundation_load_balancers.ip_address_spec.type',
            Type))

        class Persona(Enum):
            """
            ``FoundationLoadBalancers.IpAddressSpec.Persona`` class defines how the
            network interface is used.
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
            MANAGEMENT = None
            """
            This type is intended for network interface with manager role.

            """
            FRONTEND = None
            """
            This type is intended for network interface used for frontend.

            """
            BACKEND = None
            """
            This type is intended for network interface used for backend.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Persona` instance.
                """
                Enum.__init__(string)

        Persona._set_values({
            'MANAGEMENT': Persona('MANAGEMENT'),
            'FRONTEND': Persona('FRONTEND'),
            'BACKEND': Persona('BACKEND'),
        })
        Persona._set_binding_type(type.EnumType(
            'com.vmware.vcenter.foundation_load_balancers.ip_address_spec.persona',
            Persona))

    IpAddressSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.ip_address_spec', {
            'type': type.ReferenceType(__name__, 'FoundationLoadBalancers.IpAddressSpec.Type'),
            'ip_address': type.OptionalType(type.StringType()),
            'prefix': type.OptionalType(type.IntegerType()),
            'personas': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.IpAddressSpec.Persona'))),
            'gateway': type.OptionalType(type.StringType()),
        },
        IpAddressSpec,
        False,
        None))


    class NetworkInterfaceSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.NetworkInterfaceSpec`` class defines the
        information that is used for creating network interface.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     ip_settings=None,
                     network=None,
                     device_id=None,
                    ):
            """
            :type  ip_settings: :class:`list` of :class:`FoundationLoadBalancers.IpAddressSpec` or ``None``
            :param ip_settings: IP configuration of the network interface.
                This attribute was added in **vSphere API 9.0.0.0**.
                The field is required for deployment but optional for updating, If
                None, the IP configuration on the network interface will keep
                unchanged.
            :type  network: :class:`str` or ``None``
            :param network: The network to which the interface is attached.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Network``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Network``.
                The field is required for deployment but optional for updating, If
                None, current network configuration will keep unchanged.
            :type  device_id: :class:`str` or ``None``
            :param device_id: The network interface device identifier.
                This attribute was added in **vSphere API 9.0.0.0**.
                The field is not required when updating an existing network
                interface or creating a new one. It would be filled when getting
                the information of the load balancer node, if None indicates the
                network interface is not ready.
            """
            self.ip_settings = ip_settings
            self.network = network
            self.device_id = device_id
            VapiStruct.__init__(self)


    NetworkInterfaceSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.network_interface_spec', {
            'ip_settings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.IpAddressSpec'))),
            'network': type.OptionalType(type.IdType()),
            'device_id': type.OptionalType(type.StringType()),
        },
        NetworkInterfaceSpec,
        False,
        None))


    class NodeInfo(VapiStruct):
        """
        The ``FoundationLoadBalancers.NodeInfo`` class defines load balancer
        permanent description information and runtime operation information.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     version=None,
                     nics=None,
                     node_runtime_info=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: The load balancer node id generated by service or passed by the
                caller.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancerNode``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancerNode``.
            :type  version: :class:`FoundationLoadBalancers.Version`
            :param version: The version of load balancer image running on current node.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  nics: :class:`list` of :class:`FoundationLoadBalancers.NetworkInterfaceSpec`
            :param nics: Network interface configuration of load balancer node.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  node_runtime_info: :class:`FoundationLoadBalancers.NodeRuntimeInfo`
            :param node_runtime_info: The runtime information of the node.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.version = version
            self.nics = nics
            self.node_runtime_info = node_runtime_info
            VapiStruct.__init__(self)


    NodeInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.node_info', {
            'id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancerNode'),
            'version': type.ReferenceType(__name__, 'FoundationLoadBalancers.Version'),
            'nics': type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.NetworkInterfaceSpec')),
            'node_runtime_info': type.ReferenceType(__name__, 'FoundationLoadBalancers.NodeRuntimeInfo'),
        },
        NodeInfo,
        False,
        None))


    class Version(VapiStruct):
        """
        ``FoundationLoadBalancers.Version`` class defines version number.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     major=None,
                     minor=None,
                     patch=None,
                     revision=None,
                    ):
            """
            :type  major: :class:`long`
            :param major: Major version number.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  minor: :class:`long`
            :param minor: Minor version number.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  patch: :class:`long`
            :param patch: Patch number.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  revision: :class:`long`
            :param revision: Revision number.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.major = major
            self.minor = minor
            self.patch = patch
            self.revision = revision
            VapiStruct.__init__(self)


    Version._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.version', {
            'major': type.IntegerType(),
            'minor': type.IntegerType(),
            'patch': type.IntegerType(),
            'revision': type.IntegerType(),
        },
        Version,
        False,
        None))


    class UtilizationInfo(VapiStruct):
        """
        The ``FoundationLoadBalancers.UtilizationInfo`` class defines the combined
        utilization status, it contains cpu, memory currently.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cpu=None,
                     memory=None,
                    ):
            """
            :type  cpu: :class:`FoundationLoadBalancers.UtilizationStatus`
            :param cpu: CPU utilization. If the utilization is below 75%, the status is
                GREEN. If utilization is between 75% and 90% for more than 5
                minutes, the status changes to YELLOW. If utilization exceeds 90%
                for more than 5 minutes, the status changes to RED.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  memory: :class:`FoundationLoadBalancers.UtilizationStatus`
            :param memory: Memory utilization. If the utilization is below 85%, the status is
                GREEN. If utilization is between 85% and 95% for more than 10
                minutes, the status changes to YELLOW. If utilization exceeds 95%
                for more than 10 minutes, the status changes to RED.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cpu = cpu
            self.memory = memory
            VapiStruct.__init__(self)


    UtilizationInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.utilization_info', {
            'cpu': type.ReferenceType(__name__, 'FoundationLoadBalancers.UtilizationStatus'),
            'memory': type.ReferenceType(__name__, 'FoundationLoadBalancers.UtilizationStatus'),
        },
        UtilizationInfo,
        False,
        None))


    class NodeRuntimeInfo(VapiStruct):
        """
        The ``FoundationLoadBalancers.NodeRuntimeInfo`` class defines load balancer
        node runtime information.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm=None,
                     maintenance_mode=None,
                     management_ip=None,
                     deployment_status=None,
                     deployment_notifications=None,
                     ha_status=None,
                     health_status=None,
                     health_notifications=None,
                     workload_alarms=None,
                     utilization=None,
                    ):
            """
            :type  vm: :class:`str` or ``None``
            :param vm: The identifier of virtual machine that runs the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
                If None, the virtual machine deployment is not complete.
            :type  maintenance_mode: :class:`FoundationLoadBalancers.MaintenanceMode`
            :param maintenance_mode: The load balancer node maintenance status, the value can be
                ENABLED, DISABLED or UNKNOWN, If ENABLED, the node does not process
                network traffic.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  management_ip: :class:`str` or ``None``
            :param management_ip: The management IP address of the load balancer node.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means the management IP address is not configured or not
                ready.
            :type  deployment_status: :class:`FoundationLoadBalancers.DeploymentStatus`
            :param deployment_status: The deployment status of load balancer node.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  deployment_notifications: :class:`list` of :class:`FoundationLoadBalancers.Notification` or ``None``
            :param deployment_notifications: The notification messages used to describe the detailed process of
                deploying a load balancer node. The load balancer service will try
                to resolve possible deployment issues, for some resource issues the
                service can't deal with, it will notify the caller(s) to handle.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means there is no deployment related messages need to
                notify to the caller(s).
            :type  ha_status: :class:`FoundationLoadBalancers.HaStatus`
            :param ha_status: The high availability status.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  health_status: :class:`FoundationLoadBalancers.HealthStatus`
            :param health_status: The load balancer workload health status.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  health_notifications: :class:`list` of :class:`FoundationLoadBalancers.Notification` or ``None``
            :param health_notifications: Detailed notifications of health status.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means there is no health related messages need to notify to
                the caller(s).
            :type  workload_alarms: :class:`list` of :class:`FoundationLoadBalancers.Notification` or ``None``
            :param workload_alarms: The load balancer workload alarms.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means no alarms were sent from workload.
            :type  utilization: :class:`FoundationLoadBalancers.UtilizationInfo`
            :param utilization: The combined status of load balancer node.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vm = vm
            self.maintenance_mode = maintenance_mode
            self.management_ip = management_ip
            self.deployment_status = deployment_status
            self.deployment_notifications = deployment_notifications
            self.ha_status = ha_status
            self.health_status = health_status
            self.health_notifications = health_notifications
            self.workload_alarms = workload_alarms
            self.utilization = utilization
            VapiStruct.__init__(self)


    NodeRuntimeInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.node_runtime_info', {
            'vm': type.OptionalType(type.IdType()),
            'maintenance_mode': type.ReferenceType(__name__, 'FoundationLoadBalancers.MaintenanceMode'),
            'management_ip': type.OptionalType(type.StringType()),
            'deployment_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.DeploymentStatus'),
            'deployment_notifications': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Notification'))),
            'ha_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.HaStatus'),
            'health_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.HealthStatus'),
            'health_notifications': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Notification'))),
            'workload_alarms': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Notification'))),
            'utilization': type.ReferenceType(__name__, 'FoundationLoadBalancers.UtilizationInfo'),
        },
        NodeRuntimeInfo,
        False,
        None))


    class Notification(VapiStruct):
        """
        The ``FoundationLoadBalancers.Notification`` class contains attributes to
        describe any info/warning/error messages that the service can raise in
        deploying/configuring/running the load balancers.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     severity=None,
                     title=None,
                     message=None,
                     time=None,
                    ):
            """
            :type  severity: :class:`FoundationLoadBalancers.Notification.Severity`
            :param severity: The notification message severity level, this field indicates the
                severity of current message, user can select their preferred
                severity level for notifications based on this field.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  title: :class:`str`
            :param title: Fixed string to indicate the notification's type.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  message: :class:`str`
            :param message: The content of the notification message.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  time: :class:`datetime.datetime` or ``None``
            :param time: The generation time of the notification message.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None the notification message doesn't contain a generation time.
            """
            self.severity = severity
            self.title = title
            self.message = message
            self.time = time
            VapiStruct.__init__(self)


        class Severity(Enum):
            """
            The ``FoundationLoadBalancers.Notification.Severity`` class defines the
            severity level of notification message.
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
            INFO = None
            """
            Info level.

            """
            WARNING = None
            """
            Warning level.

            """
            ERROR = None
            """
            Error level.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Severity` instance.
                """
                Enum.__init__(string)

        Severity._set_values({
            'INFO': Severity('INFO'),
            'WARNING': Severity('WARNING'),
            'ERROR': Severity('ERROR'),
        })
        Severity._set_binding_type(type.EnumType(
            'com.vmware.vcenter.foundation_load_balancers.notification.severity',
            Severity))

    Notification._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.notification', {
            'severity': type.ReferenceType(__name__, 'FoundationLoadBalancers.Notification.Severity'),
            'title': type.StringType(),
            'message': type.StringType(),
            'time': type.OptionalType(type.DateTimeType()),
        },
        Notification,
        False,
        None))


    class RuntimeInfo(VapiStruct):
        """
        The ``FoundationLoadBalancers.RuntimeInfo`` class defines load balancer
        different status information while the load balancer is running.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     operation_status=None,
                     operation_notifications=None,
                     deployment_status=None,
                     health_status=None,
                     utilization=None,
                    ):
            """
            :type  operation_status: :class:`FoundationLoadBalancers.OperationStatus`
            :param operation_status: The consolidated operation status of load balancer, it describes
                which stage the operation is in when making changes to current
                associated load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  operation_notifications: :class:`list` of :class:`FoundationLoadBalancers.Notification` or ``None``
            :param operation_notifications: The notification messages used to describe the detailed process of
                making changes to current associated load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means there isn't any exception to notify the caller(s).
            :type  deployment_status: :class:`FoundationLoadBalancers.DeploymentStatus`
            :param deployment_status: The consolidated deployment status of all backend load balancer
                node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  health_status: :class:`FoundationLoadBalancers.HealthStatus`
            :param health_status: The consolidated health status of load balancer workload(s), more
                information of the health status refers to specific load balancer
                node.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  utilization: :class:`FoundationLoadBalancers.UtilizationInfo`
            :param utilization: The consolidated utilization status of load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.operation_status = operation_status
            self.operation_notifications = operation_notifications
            self.deployment_status = deployment_status
            self.health_status = health_status
            self.utilization = utilization
            VapiStruct.__init__(self)


    RuntimeInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.runtime_info', {
            'operation_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.OperationStatus'),
            'operation_notifications': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Notification'))),
            'deployment_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.DeploymentStatus'),
            'health_status': type.ReferenceType(__name__, 'FoundationLoadBalancers.HealthStatus'),
            'utilization': type.ReferenceType(__name__, 'FoundationLoadBalancers.UtilizationInfo'),
        },
        RuntimeInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``FoundationLoadBalancers.Info`` class defines information about load
        balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     name=None,
                     owner=None,
                     owner_id=None,
                     replica=None,
                     size=None,
                     available_versions=None,
                     version=None,
                     placement_spec=None,
                     network_config_spec=None,
                     log_config_spec=None,
                     load_balancer_controllers=None,
                     node_info_map=None,
                     trusted_ca=None,
                     runtime=None,
                     system_trusted_cas=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: The identifier of the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancer``. When methods return
                a value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancer``.
            :type  name: :class:`str`
            :param name: The name of the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  owner: :class:`str`
            :param owner: The owner of the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  owner_id: :class:`str` or ``None``
            :param owner_id: The owner identifier of the load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, it means the owner identifier is not configured when
                creating the load balancer.
            :type  replica: :class:`long`
            :param replica: The replica number of the load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  size: :class:`FoundationLoadBalancers.SizingSpec`
            :param size: The load balancer node(s) capacity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  available_versions: :class:`list` of :class:`FoundationLoadBalancers.Version` or ``None``
            :param available_versions: The available versions could be used for upgrading.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means there are no versions for upgrading.
            :type  version: :class:`FoundationLoadBalancers.Version`
            :param version: The version of load balancer image.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  placement_spec: :class:`FoundationLoadBalancers.PlacementSpec`
            :param placement_spec: The placement configuration of load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  network_config_spec: :class:`FoundationLoadBalancers.NetworkConfigSpec`
            :param network_config_spec: The network configuration of load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  log_config_spec: :class:`FoundationLoadBalancers.LogConfigSpec` or ``None``
            :param log_config_spec: The log configuration of load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means doesn't configure log setting when creating load
                balancer.
            :type  load_balancer_controllers: :class:`list` of :class:`FoundationLoadBalancers.LoadBalancerController` or ``None``
            :param load_balancer_controllers: The location of load balancer controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means doesn't configure load balancer controller when
                creating load balancer.
            :type  node_info_map: :class:`dict` of :class:`str` and :class:`FoundationLoadBalancers.NodeInfo`
            :param node_info_map: The load balancer node(s) information, the key(ID) was dynamically
                generated when creating the load balancer node and it will stick
                with the load balancer node during the whole lifecycle, even if you
                make changes to the load balancer node, such as reconfiguration and
                redeployment.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.FoundationLoadBalancerNode``. When
                methods return a value of this class as a return value, the key in
                the attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.FoundationLoadBalancerNode``.
            :type  trusted_ca: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain` or ``None``
            :param trusted_ca: The TLS certificate chain of the load balancer used by load
                balancer node(s) to verify the load balancer controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, load balancer node(s) use system-wide certificates
                finishing the verification process for load balancer controller.
            :type  runtime: :class:`FoundationLoadBalancers.RuntimeInfo`
            :param runtime: The runtime information associated with load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  system_trusted_cas: :class:`list` of :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain` or ``None``
            :param system_trusted_cas: List of trusted CA certificate chains used by load balancer node(s)
                for verifying the TLS certificates. These certificate chains are
                imported into the system-wide database to secure TLS connections of
                load balancer node(s).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the system certificate store of the load balancer node(s)
                will remain empty.
            """
            self.id = id
            self.name = name
            self.owner = owner
            self.owner_id = owner_id
            self.replica = replica
            self.size = size
            self.available_versions = available_versions
            self.version = version
            self.placement_spec = placement_spec
            self.network_config_spec = network_config_spec
            self.log_config_spec = log_config_spec
            self.load_balancer_controllers = load_balancer_controllers
            self.node_info_map = node_info_map
            self.trusted_ca = trusted_ca
            self.runtime = runtime
            self.system_trusted_cas = system_trusted_cas
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.info', {
            'id': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'name': type.StringType(),
            'owner': type.StringType(),
            'owner_id': type.OptionalType(type.StringType()),
            'replica': type.IntegerType(),
            'size': type.ReferenceType(__name__, 'FoundationLoadBalancers.SizingSpec'),
            'available_versions': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Version'))),
            'version': type.ReferenceType(__name__, 'FoundationLoadBalancers.Version'),
            'placement_spec': type.ReferenceType(__name__, 'FoundationLoadBalancers.PlacementSpec'),
            'network_config_spec': type.ReferenceType(__name__, 'FoundationLoadBalancers.NetworkConfigSpec'),
            'log_config_spec': type.OptionalType(type.ReferenceType(__name__, 'FoundationLoadBalancers.LogConfigSpec')),
            'load_balancer_controllers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.LoadBalancerController'))),
            'node_info_map': type.MapType(type.IdType(), type.ReferenceType(__name__, 'FoundationLoadBalancers.NodeInfo')),
            'trusted_ca': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
            'runtime': type.ReferenceType(__name__, 'FoundationLoadBalancers.RuntimeInfo'),
            'system_trusted_cas': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain'))),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``FoundationLoadBalancers.FilterSpec`` class contains parameters used
        for filter the results when listing load balancers.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     owner=None,
                     owner_id=None,
                     name=None,
                     full_info=None,
                    ):
            """
            :type  owner: :class:`str` or ``None``
            :param owner: The creator name of load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, it won't match creator information when listing load
                balancers.
            :type  owner_id: :class:`str` or ``None``
            :param owner_id: The load balancer creator identifier.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, it won't match creator information when listing load
                balancers.
            :type  name: :class:`str` or ``None``
            :param name: The load balancer name.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, it won't match load balancer name when listing load
                balancers.
            :type  full_info: :class:`bool` or ``None``
            :param full_info: The field indicates whether to get load balancer detailed info
                list, if the value is true, get load balancer detailed info list
                and ID list, if the value is false, get load balancer ID list only.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means get load balancer ID list only.
            """
            self.owner = owner
            self.owner_id = owner_id
            self.name = name
            self.full_info = full_info
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.filter_spec', {
            'owner': type.OptionalType(type.StringType()),
            'owner_id': type.OptionalType(type.StringType()),
            'name': type.OptionalType(type.StringType()),
            'full_info': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``FoundationLoadBalancers.ListResult`` class contains commonly used
        information about a load balancer.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     load_balancers=None,
                     infos=None,
                    ):
            """
            :type  load_balancers: :class:`set` of :class:`str`
            :param load_balancers: Identifier(s) of load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancer``. When methods return
                a value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.FoundationLoadBalancer``.
            :type  infos: :class:`list` of :class:`FoundationLoadBalancers.Info` or ``None``
            :param infos: Detailed info list of load balancer.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None means client doesn't intend to get a detailed info list.
            """
            self.load_balancers = load_balancers
            self.infos = infos
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.list_result', {
            'load_balancers': type.SetType(type.IdType()),
            'infos': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'FoundationLoadBalancers.Info'))),
        },
        ListResult,
        False,
        None))


    class ControllerSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.ControllerSpec`` class defines information for
        load balancer node(s) connecting to controller.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     jwt=None,
                     trusted_ca=None,
                    ):
            """
            :type  jwt: :class:`str` or ``None``
            :param jwt: Token used by load balancer node(s) to authenticate with the
                controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, load balancer node(s) won't have a token in JWT format
                when accessing load balancer controller.
            :type  trusted_ca: :class:`com.vmware.vcenter.trusted_infrastructure_client.X509CertChain` or ``None``
            :param trusted_ca: The TLS certificate chain of the load balancer used by load
                balancer node(s) to verify the load balancer controller.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, load balancer node(s) will stop certificate verification
                workflow for load balancer controller.
            """
            self.jwt = jwt
            self.trusted_ca = trusted_ca
            VapiStruct.__init__(self)


    ControllerSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.controller_spec', {
            'jwt': type.OptionalType(type.SecretType()),
            'trusted_ca': type.OptionalType(type.ReferenceType('com.vmware.vcenter.trusted_infrastructure_client', 'X509CertChain')),
        },
        ControllerSpec,
        False,
        None))


    class LoginConfigSpec(VapiStruct):
        """
        ``FoundationLoadBalancers.LoginConfigSpec`` class defines login
        configuration.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     password=None,
                     authorized_keys=None,
                    ):
            """
            :type  password: :class:`str` or ``None``
            :param password: Password used for "vmware-system-user" user.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the value keeps unset or unchanged.
            :type  authorized_keys: :class:`list` of :class:`str` or ``None``
            :param authorized_keys: The authorized keys of the load balancer node(s) for key-based ssh
                login.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the value keeps unset or unchanged.
            """
            self.password = password
            self.authorized_keys = authorized_keys
            VapiStruct.__init__(self)


    LoginConfigSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.login_config_spec', {
            'password': type.OptionalType(type.SecretType()),
            'authorized_keys': type.OptionalType(type.ListType(type.StringType())),
        },
        LoginConfigSpec,
        False,
        None))


    class PasswordSpec(VapiStruct):
        """
        The ``FoundationLoadBalancers.PasswordSpec`` class defines the new password
        for load balancer node(s).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     password=None,
                    ):
            """
            :type  password: :class:`str`
            :param password: The field indicates the new password user wants to set to the load
                balancer node.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.password = password
            VapiStruct.__init__(self)


    PasswordSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.foundation_load_balancers.password_spec', {
            'password': type.SecretType(),
        },
        PasswordSpec,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about load balancers matching the
        :class:`FoundationLoadBalancers.FilterSpec`.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`FoundationLoadBalancers.FilterSpec` or ``None``
        :param filter: specification of matching load balancers for which information
            should be returned.
            if None, all load balancers match the filter.
        :rtype: :class:`FoundationLoadBalancers.ListResult`
        :return: the identifier of load balancers matching the
            :class:`FoundationLoadBalancers.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``filter`` is invalid.
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
                            'filter': filter,
                            })

    def get(self,
            foundation_load_balancer,
            ):
        """
        Retrieves information about the load balancer corresponding to the
        specified ``foundation_load_balancer``.
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :rtype: :class:`FoundationLoadBalancers.Info`
        :return: information about the load balancer.
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
        return self._invoke('get',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            })

    def reset_password(self,
                       foundation_load_balancer,
                       password,
                       ):
        """
        Resets password of user "vmware-system-user" (used for debugging
        purposes only) in the load balancer virtual machine(s).
        This method was added in **vSphere API 9.0.0.0**.

        :type  foundation_load_balancer: :class:`str`
        :param foundation_load_balancer: identifier of the load balancer.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.FoundationLoadBalancer``.
        :type  password: :class:`FoundationLoadBalancers.PasswordSpec`
        :param password: :class:`FoundationLoadBalancers.PasswordSpec` new password to set.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the load balancer is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``password`` is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the reset password is not allowed in the current state.
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
        return self._invoke('reset_password',
                            {
                            'foundation_load_balancer': foundation_load_balancer,
                            'password': password,
                            })
class Host(VapiInterface):
    """
    The ``Host`` class provides methods to manage hosts in the vCenter Server.
    """
    RESOURCE_TYPE = "HostSystem"
    """
    The resource type for the vCenter Host.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.host'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HostStub)
        self._VAPI_OPERATION_IDS = {}

    class ConnectionState(Enum):
        """
        The ``Host.ConnectionState`` class defines the connection status of a host.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        CONNECTED = None
        """
        Host is connected to the vCenter Server

        """
        DISCONNECTED = None
        """
        Host is disconnected from the vCenter Server

        """
        NOT_RESPONDING = None
        """
        VirtualCenter is not receiving heartbeats from the server. The state
        automatically changes to connected once heartbeats are received again.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConnectionState` instance.
            """
            Enum.__init__(string)

    ConnectionState._set_values({
        'CONNECTED': ConnectionState('CONNECTED'),
        'DISCONNECTED': ConnectionState('DISCONNECTED'),
        'NOT_RESPONDING': ConnectionState('NOT_RESPONDING'),
    })
    ConnectionState._set_binding_type(type.EnumType(
        'com.vmware.vcenter.host.connection_state',
        ConnectionState))


    class PowerState(Enum):
        """
        The ``Host.PowerState`` class defines the power states of a host.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        POWERED_ON = None
        """
        The host is powered on. A host that is entering standby mode is also in
        this state.

        """
        POWERED_OFF = None
        """
        The host was specifically powered off by the user through vCenter server.
        This state is not a cetain state, because after vCenter server issues the
        command to power off the host, the host might crash, or kill all the
        processes but fail to power off.

        """
        STANDBY = None
        """
        The host was specifically put in standby mode, either explicitly by the
        user, or automatically by DPM. This state is not a cetain state, because
        after VirtualCenter issues the command to put the host in standby state,
        the host might crash, or kill all the processes but fail to enter standby
        mode. A host that is exiting standby mode is also in this state.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`PowerState` instance.
            """
            Enum.__init__(string)

    PowerState._set_values({
        'POWERED_ON': PowerState('POWERED_ON'),
        'POWERED_OFF': PowerState('POWERED_OFF'),
        'STANDBY': PowerState('STANDBY'),
    })
    PowerState._set_binding_type(type.EnumType(
        'com.vmware.vcenter.host.power_state',
        PowerState))


    class CreateSpec(VapiStruct):
        """
        The ``Host.CreateSpec`` class defines the information used to create a
        host.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'thumbprint_verification',
                {
                    'THUMBPRINT' : [('thumbprint', True)],
                    'CERTIFICATE' : [('ssl_certificate', False)],
                    'NONE' : [],
                }
            ),
        ]



        def __init__(self,
                     hostname=None,
                     port=None,
                     user_name=None,
                     password=None,
                     folder=None,
                     thumbprint_verification=None,
                     thumbprint=None,
                     ssl_certificate=None,
                     force_add=None,
                    ):
            """
            :type  hostname: :class:`str`
            :param hostname: The IP address or DNS resolvable name of the host.
            :type  port: :class:`long` or ``None``
            :param port: The port of the host.
                If None, port 443 will be used.
            :type  user_name: :class:`str`
            :param user_name: The administrator account on the host.
            :type  password: :class:`str`
            :param password: The password for the administrator account on the host.
            :type  folder: :class:`str` or ``None``
            :param folder: Host and cluster folder in which the new standalone host should be
                created.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose a suitable
                folder for the host; if a folder cannot be chosen, the host
                creation operation will fail.
            :type  thumbprint_verification: :class:`Host.CreateSpec.ThumbprintVerification`
            :param thumbprint_verification: Type of host's SSL certificate verification to be done.
            :type  thumbprint: :class:`str`
            :param thumbprint: The thumbprint of the SSL certificate, which the host is expected
                to have. The thumbprint is always computed using the SHA1 hash and
                is the string representation of that hash in the format:
                xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx where,
                'x' represents a hexadecimal digit.
                This attribute is optional and it is only relevant when the value
                of ``thumbprintVerification`` is
                :attr:`Host.CreateSpec.ThumbprintVerification.THUMBPRINT`.
            :type  ssl_certificate: :class:`str`
            :param ssl_certificate: The SSL certificate in PEM format, which the host is expected to
                have.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``thumbprintVerification`` is
                :attr:`Host.CreateSpec.ThumbprintVerification.CERTIFICATE`.
            :type  force_add: :class:`bool` or ``None``
            :param force_add: Whether host should be added to the vCenter Server even if it is
                being managed by another vCenter Server. The original vCenterServer
                loses connection to the host.
                If None, forceAdd is default to false.
            """
            self.hostname = hostname
            self.port = port
            self.user_name = user_name
            self.password = password
            self.folder = folder
            self.thumbprint_verification = thumbprint_verification
            self.thumbprint = thumbprint
            self.ssl_certificate = ssl_certificate
            self.force_add = force_add
            VapiStruct.__init__(self)


        class ThumbprintVerification(Enum):
            """
            The ``Host.CreateSpec.ThumbprintVerification`` class defines the thumbprint
            verification schemes for a host's SSL certificate.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            NONE = None
            """
            Accept the host's thumbprint without verifying it.

            """
            THUMBPRINT = None
            """
            Host's SSL certificate verified by checking its thumbprint against the
            specified thumbprint.

            """
            CERTIFICATE = None
            """
            Host's SSL certificate verified by checking it against the provided PEM SSL
            certificate.
            This class attribute was added in **vSphere API 9.0.0.0**.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`ThumbprintVerification` instance.
                """
                Enum.__init__(string)

        ThumbprintVerification._set_values({
            'NONE': ThumbprintVerification('NONE'),
            'THUMBPRINT': ThumbprintVerification('THUMBPRINT'),
            'CERTIFICATE': ThumbprintVerification('CERTIFICATE'),
        })
        ThumbprintVerification._set_binding_type(type.EnumType(
            'com.vmware.vcenter.host.create_spec.thumbprint_verification',
            ThumbprintVerification))

    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.host.create_spec', {
            'hostname': type.StringType(),
            'port': type.OptionalType(type.IntegerType()),
            'user_name': type.StringType(),
            'password': type.SecretType(),
            'folder': type.OptionalType(type.IdType()),
            'thumbprint_verification': type.ReferenceType(__name__, 'Host.CreateSpec.ThumbprintVerification'),
            'thumbprint': type.OptionalType(type.StringType()),
            'ssl_certificate': type.OptionalType(type.StringType()),
            'force_add': type.OptionalType(type.BooleanType()),
        },
        CreateSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Host.FilterSpec`` class contains attributes used to filter the
        results when listing hosts (see :func:`Host.list`). If multiple attributes
        are specified, only hosts matching all of the attributes match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     hosts=None,
                     names=None,
                     folders=None,
                     datacenters=None,
                     standalone=None,
                     clusters=None,
                     connection_states=None,
                     host_uuids=None,
                    ):
            """
            :type  hosts: :class:`set` of :class:`str` or ``None``
            :param hosts: Identifiers of hosts that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                If None or empty, hosts with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that hosts must have to match the filter (see
                :attr:`Host.Summary.name`).
                If None or empty, hosts with any name match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the hosts for the hosts to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, hosts in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the hosts for the hosts to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, hosts in any datacenter match the filter.
            :type  standalone: :class:`bool` or ``None``
            :param standalone: If true, only hosts that are not part of a cluster can match the
                filter, and if false, only hosts that are are part of a cluster can
                match the filter.
                If None Hosts can match filter independent of whether they are part
                of a cluster or not. If this field is true and
                :attr:`Host.FilterSpec.clusters` os not empty, no hosts will match
                the filter.
            :type  clusters: :class:`set` of :class:`str` or ``None``
            :param clusters: Clusters that must contain the hosts for the hosts to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, hosts in any cluster and hosts that are not in a
                cluster match the filter. If this attribute is not empty and
                :attr:`Host.FilterSpec.standalone` is true, no hosts will match the
                filter.
            :type  connection_states: :class:`set` of :class:`Host.ConnectionState` or ``None``
            :param connection_states: Connection states that a host must be in to match the filter (see
                :attr:`Host.Summary.connection_state`.
                If None or empty, hosts in any connection state match the filter.
            :type  host_uuids: :class:`set` of :class:`str` or ``None``
            :param host_uuids: UUID of hosts that can match the filter. Maps to "UUID" in SMBIOS:
                System Information (Type 1) and offset 08h
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or empty, hosts with any identifier match the filter.
            """
            self.hosts = hosts
            self.names = names
            self.folders = folders
            self.datacenters = datacenters
            self.standalone = standalone
            self.clusters = clusters
            self.connection_states = connection_states
            self.host_uuids = host_uuids
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.host.filter_spec', {
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
            'standalone': type.OptionalType(type.BooleanType()),
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'connection_states': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Host.ConnectionState'))),
            'host_uuids': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Host.Summary`` class contains commonly used information about a host
        in vCenter Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'connection_state',
                {
                    'CONNECTED' : [('power_state', True)],
                    'DISCONNECTED' : [],
                    'NOT_RESPONDING' : [],
                }
            ),
        ]



        def __init__(self,
                     host=None,
                     name=None,
                     connection_state=None,
                     power_state=None,
                     host_uuid=None,
                    ):
            """
            :type  host: :class:`str`
            :param host: Identifier of the host.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
            :type  name: :class:`str`
            :param name: Name of the host.
            :type  connection_state: :class:`Host.ConnectionState`
            :param connection_state: Connection status of the host
            :type  power_state: :class:`Host.PowerState`
            :param power_state: Power state of the host
                This attribute is optional and it is only relevant when the value
                of ``connectionState`` is :attr:`Host.ConnectionState.CONNECTED`.
            :type  host_uuid: :class:`str`
            :param host_uuid: UUID of the host. Maps to "UUID" in SMBIOS: System Information
                (Type 1) and offset 08h
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.host = host
            self.name = name
            self.connection_state = connection_state
            self.power_state = power_state
            self.host_uuid = host_uuid
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.host.summary', {
            'host': type.IdType(resource_types='HostSystem'),
            'name': type.StringType(),
            'connection_state': type.ReferenceType(__name__, 'Host.ConnectionState'),
            'power_state': type.OptionalType(type.ReferenceType(__name__, 'Host.PowerState')),
            'host_uuid': type.OptionalType(type.StringType()),
        },
        Summary,
        False,
        None))



    def create(self,
               spec,
               ):
        """
        Add a new standalone host in the vCenter inventory. The newly connected
        host will be in connected state. The vCenter Server will verify the SSL
        certificate before adding the host to its inventory. In the case where
        the SSL certificate cannot be verified because the Certificate
        Authority is not recognized or the certificate is self signed, the
        vCenter Server will fall back to thumbprint verification mode as
        defined by :class:`Host.CreateSpec.ThumbprintVerification`.

        :type  spec: :class:`Host.CreateSpec`
        :param spec: Specification for the new host to be created.
        :rtype: :class:`str`
        :return: The newly created identifier of the host in vCenter.
            The return value will be an identifier for the resource type:
            ``HostSystem``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if the host with the same name is already present.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if installation of VirtualCenter agent on a host fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the host name is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the host folder is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the SSL thumbprint specified is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the PEM SSL certificate in CreateSpec.sslCertificate is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if both CreateSpec.thumbprint and CreateSpec.sslCertificate are
            :class:`set`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the CreateSpec.sslCertificate argument is not set, and the
            CreateSpec.thumbprint argument is set, but the SHA-1 hashing
            algorithm is currently disabled for computing certificate
            thumbprints.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidElementType` 
            if the host folder id does not support vSphere compute resource as
            its children type.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no folder associated with the ``folder`` attribute in
            the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if the host is already being managed by another vCenter Server
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if there are not enough licenses to add the host.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user name or password for the administration account on the
            host are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the software version on the host is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def delete(self,
               host,
               ):
        """
        Remove a standalone host from the vCenter Server.

        :type  host: :class:`str`
        :param host: Identifier of the host to be deleted.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no host associated with ``host`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if the host associated with ``host`` is in a vCenter cluster
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('delete',
                            {
                            'host': host,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 2500 visible (subject to permission
        checks) hosts in vCenter matching the :class:`Host.FilterSpec`.

        :type  filter: :class:`Host.FilterSpec` or ``None``
        :param filter: Specification of matching hosts for which information should be
            returned.
            If None, the behavior is equivalent to a :class:`Host.FilterSpec`
            with all attributes None which means all hosts match the filter.
        :rtype: :class:`list` of :class:`Host.Summary`
        :return: Commonly used information about the hosts matching the
            :class:`Host.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Host.FilterSpec.connection_states` attribute contains
            a value that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 2500 hosts match the :class:`Host.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def connect(self,
                host,
                ):
        """
        Connect to the host corresponding to ``host`` previously added to the
        vCenter server.

        :type  host: :class:`str`
        :param host: Identifier of the host to be reconnected.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if the host associated with ``host`` is already connected.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no host associated with ``host`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('connect',
                            {
                            'host': host,
                            })

    def disconnect(self,
                   host,
                   ):
        """
        Disconnect the host corresponding to ``host`` from the vCenter server

        :type  host: :class:`str`
        :param host: Identifier of the host to be disconnected.
            The parameter must be an identifier for the resource type:
            ``HostSystem``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            if the host associated with ``host`` is already disconnected.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no host associated with ``host`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('disconnect',
                            {
                            'host': host,
                            })
class Network(VapiInterface):
    """
    The Network class provides methods for manipulating a vCenter Server
    network.
    """
    RESOURCE_TYPE = "Network"
    """
    The resource type for the vCenter network

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.network'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _NetworkStub)
        self._VAPI_OPERATION_IDS = {}

    class Type(Enum):
        """
        The ``Network.Type`` class defines the type of a vCenter Server network.
        The type of a network can be used to determine what features it supports
        and which APIs can be used to find more information about the network or
        change its configuration.

        .. note::
            This class represents an enumerated type in the interface language
            definition. The class contains class attributes which represent the
            values in the current version of the enumerated type. Newer versions of
            the enumerated type may contain new values. To use new values of the
            enumerated type in communication with a server that supports the newer
            version of the API, you instantiate this class. See :ref:`enumerated
            type description page <enumeration_description>`.
        """
        STANDARD_PORTGROUP = None
        """
        vSphere standard portgroup (created and managed on ESX)

        """
        DISTRIBUTED_PORTGROUP = None
        """
        Distributed virtual portgroup (created and managed through vCenter)

        """
        OPAQUE_NETWORK = None
        """
        A network whose configuration is managed outside of vSphere. The identifer
        and name of the network is made available through vSphere so that host and
        virtual machine virtual ethernet devices can connect to them.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Type` instance.
            """
            Enum.__init__(string)

    Type._set_values({
        'STANDARD_PORTGROUP': Type('STANDARD_PORTGROUP'),
        'DISTRIBUTED_PORTGROUP': Type('DISTRIBUTED_PORTGROUP'),
        'OPAQUE_NETWORK': Type('OPAQUE_NETWORK'),
    })
    Type._set_binding_type(type.EnumType(
        'com.vmware.vcenter.network.type',
        Type))


    class FilterSpec(VapiStruct):
        """
        The ``Network.FilterSpec`` class contains attributes used to filter the
        results when listing networks (see :func:`Network.list`). If multiple
        attributes are specified, only networks matching all of the attributes
        match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     networks=None,
                     names=None,
                     types=None,
                     folders=None,
                     datacenters=None,
                    ):
            """
            :type  networks: :class:`set` of :class:`str` or ``None``
            :param networks: Identifiers of networks that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Network``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Network``.
                If None or empty, networks with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that networks must have to match the filter (see
                :attr:`Network.Summary.name`).
                If None or empty, networks with any name match the filter.
            :type  types: :class:`set` of :class:`Network.Type` or ``None``
            :param types: Types that networks must have to match the filter (see
                :attr:`Network.Summary.type`).
                If None, networks with any type match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the network for the network to match the
                filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, networks in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the network for the network to match
                the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, networks in any datacenter match the filter.
            """
            self.networks = networks
            self.names = names
            self.types = types
            self.folders = folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.filter_spec', {
            'networks': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'types': type.OptionalType(type.SetType(type.ReferenceType(__name__, 'Network.Type'))),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Network.Summary`` class contains commonly used information about a
        network.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     network=None,
                     name=None,
                     type=None,
                    ):
            """
            :type  network: :class:`str`
            :param network: Identifier of the network.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Network``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Network``.
            :type  name: :class:`str`
            :param name: Name of the network.
            :type  type: :class:`Network.Type`
            :param type: Type (STANDARD_PORTGROUP, DISTRIBUTED_PORTGROUP, OPAQUE_NETWORK) of
                the vCenter Server network.
            """
            self.network = network
            self.name = name
            self.type = type
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.network.summary', {
            'network': type.IdType(resource_types='Network'),
            'name': type.StringType(),
            'type': type.ReferenceType(__name__, 'Network.Type'),
        },
        Summary,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) networks in vCenter matching the :class:`Network.FilterSpec`.

        :type  filter: :class:`Network.FilterSpec` or ``None``
        :param filter: Specification of matching networks for which information should be
            returned.
            If None, the behavior is equivalent to a
            :class:`Network.FilterSpec` with all attributes None which means
            all networks match the filter.
        :rtype: :class:`list` of :class:`Network.Summary`
        :return: Commonly used information about the networks matching the
            :class:`Network.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`Network.FilterSpec.types` attribute contains a value
            that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 1000 networks match the :class:`Network.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })
class ResourcePool(VapiInterface):
    """
    The ResourcePool class provides methods for manipulating a vCenter Server
    resource pool. 
    
    This class does not include virtual appliances in the inventory of resource
    pools even though part of the behavior of a virtual appliance is to act
    like a resource pool.
    """
    RESOURCE_TYPE = "ResourcePool"
    """
    The resource type for the vCenter resource pool

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.resource_pool'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ResourcePoolStub)
        self._VAPI_OPERATION_IDS = {}

    class SharesInfo(VapiStruct):
        """
        The ``ResourcePool.SharesInfo`` class provides specification of shares. 
        
        Shares are used to determine relative allocation between resource
        consumers. In general, a consumer with more shares gets proportionally more
        of the resource, subject to certain other constraints.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'level',
                {
                    'CUSTOM' : [('shares', True)],
                    'LOW' : [],
                    'NORMAL' : [],
                    'HIGH' : [],
                }
            ),
        ]



        def __init__(self,
                     level=None,
                     shares=None,
                    ):
            """
            :type  level: :class:`ResourcePool.SharesInfo.Level`
            :param level: The allocation level. It maps to a pre-determined set of numeric
                values for shares. If the shares value does not map to a predefined
                size, then the level is set as CUSTOM.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  shares: :class:`long`
            :param shares: When :attr:`ResourcePool.SharesInfo.level` is set to CUSTOM, it is
                the number of shares allocated. Otherwise, this value is ignored. 
                
                There is no unit for this value. It is a relative measure based on
                the settings for other resource pools.
                This attribute was added in **vSphere API 7.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``level`` is :attr:`ResourcePool.SharesInfo.Level.CUSTOM`.
            """
            self.level = level
            self.shares = shares
            VapiStruct.__init__(self)


        class Level(Enum):
            """
            The ``ResourcePool.SharesInfo.Level`` class defines the possible values for
            the allocation level.
            This enumeration was added in **vSphere API 7.0.0.0**.

            .. note::
                This class represents an enumerated type in the interface language
                definition. The class contains class attributes which represent the
                values in the current version of the enumerated type. Newer versions of
                the enumerated type may contain new values. To use new values of the
                enumerated type in communication with a server that supports the newer
                version of the API, you instantiate this class. See :ref:`enumerated
                type description page <enumeration_description>`.
            """
            LOW = None
            """
            For CPU: Shares = 500 \* number of virtual CPUs.
            For Memory: Shares = 5 \* virtual machine memory size in MB.

            """
            NORMAL = None
            """
            For CPU: Shares = 1000 \* number of virtual CPUs.
            For Memory: Shares = 10 \* virtual machine memory size in MB.

            """
            HIGH = None
            """
            For CPU: Shares = 2000 \* number of virtual CPUs.
            For Memory: Shares = 20 \* virtual machine memory size in MB.

            """
            CUSTOM = None
            """
            If :class:`set`, in case there is resource contention the server uses the
            shares value to determine the resource allocation.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Level` instance.
                """
                Enum.__init__(string)

        Level._set_values({
            'LOW': Level('LOW'),
            'NORMAL': Level('NORMAL'),
            'HIGH': Level('HIGH'),
            'CUSTOM': Level('CUSTOM'),
        })
        Level._set_binding_type(type.EnumType(
            'com.vmware.vcenter.resource_pool.shares_info.level',
            Level))

    SharesInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.shares_info', {
            'level': type.ReferenceType(__name__, 'ResourcePool.SharesInfo.Level'),
            'shares': type.OptionalType(type.IntegerType()),
        },
        SharesInfo,
        False,
        None))


    class ResourceAllocationInfo(VapiStruct):
        """
        The ``ResourcePool.ResourceAllocationInfo`` class contains resource
        allocation information of a resource pool.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reservation=None,
                     expandable_reservation=None,
                     limit=None,
                     shares=None,
                    ):
            """
            :type  reservation: :class:`long`
            :param reservation: Amount of resource that is guaranteed available to a resource pool.
                Reserved resources are not wasted if they are not used. If the
                utilization is less than the reservation, the resources can be
                utilized by other running virtual machines. Units are MB fo memory,
                and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  expandable_reservation: :class:`bool`
            :param expandable_reservation: In a resource pool with an expandable reservation, the reservation
                can grow beyond the specified value, if the parent resource pool
                has unreserved resources. A non-expandable reservation is called a
                fixed reservation.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  limit: :class:`long`
            :param limit: The utilization of a resource pool will not exceed this limit, even
                if there are available resources. This is typically used to ensure
                a consistent performance of resource pools independent of available
                resources. If set to -1, then there is no fixed limit on resource
                usage (only bounded by available resources and shares). Units are
                MB for memory, and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  shares: :class:`ResourcePool.SharesInfo`
            :param shares: Shares are used in case of resource contention.
                This attribute was added in **vSphere API 7.0.0.0**.
            """
            self.reservation = reservation
            self.expandable_reservation = expandable_reservation
            self.limit = limit
            self.shares = shares
            VapiStruct.__init__(self)


    ResourceAllocationInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.resource_allocation_info', {
            'reservation': type.IntegerType(),
            'expandable_reservation': type.BooleanType(),
            'limit': type.IntegerType(),
            'shares': type.ReferenceType(__name__, 'ResourcePool.SharesInfo'),
        },
        ResourceAllocationInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``ResourcePool.Info`` class contains information about a resource pool.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     resource_pools=None,
                     cpu_allocation=None,
                     memory_allocation=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the vCenter Server resource pool.
            :type  resource_pools: :class:`set` of :class:`str`
            :param resource_pools: Identifiers of the child resource pools contained in this resource
                pool.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``ResourcePool``.
            :type  cpu_allocation: :class:`ResourcePool.ResourceAllocationInfo`
            :param cpu_allocation: Resource allocation information for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  memory_allocation: :class:`ResourcePool.ResourceAllocationInfo`
            :param memory_allocation: Resource allocation information for memory.
                This attribute was added in **vSphere API 7.0.0.0**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.name = name
            self.resource_pools = resource_pools
            self.cpu_allocation = cpu_allocation
            self.memory_allocation = memory_allocation
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.info', {
            'name': type.StringType(),
            'resource_pools': type.SetType(type.IdType()),
            'cpu_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationInfo')),
            'memory_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationInfo')),
        },
        Info,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``ResourcePool.FilterSpec`` class contains attributes used to filter
        the results when listing resource pools (see :func:`ResourcePool.list`). If
        multiple attributes are specified, only resource pools matching all of the
        attributes match the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     resource_pools=None,
                     names=None,
                     parent_resource_pools=None,
                     datacenters=None,
                     hosts=None,
                     clusters=None,
                    ):
            """
            :type  resource_pools: :class:`set` of :class:`str` or ``None``
            :param resource_pools: Identifiers of resource pools that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``ResourcePool``.
                If None or empty, resource pools with any identifier match the
                filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that resource pools must have to match the filter (see
                :attr:`ResourcePool.Info.name`).
                If None or empty, resource pools with any name match the filter.
            :type  parent_resource_pools: :class:`set` of :class:`str` or ``None``
            :param parent_resource_pools: Resource pools that must contain the resource pool for the resource
                pool to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``ResourcePool``.
                If None or empty, resource pools in any resource pool match the
                filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the resource pool for the resource
                pool to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, resource pools in any datacenter match the
                filter.
            :type  hosts: :class:`set` of :class:`str` or ``None``
            :param hosts: Hosts that must contain the resource pool for the resource pool to
                match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                If None or empty, resource pools in any host match the filter.
            :type  clusters: :class:`set` of :class:`str` or ``None``
            :param clusters: Clusters that must contain the resource pool for the resource pool
                to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, resource pools in any cluster match the filter.
            """
            self.resource_pools = resource_pools
            self.names = names
            self.parent_resource_pools = parent_resource_pools
            self.datacenters = datacenters
            self.hosts = hosts
            self.clusters = clusters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.filter_spec', {
            'resource_pools': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'parent_resource_pools': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'clusters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``ResourcePool.Summary`` class contains commonly used information about
        a resource pool in vCenter Server.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     resource_pool=None,
                     name=None,
                    ):
            """
            :type  resource_pool: :class:`str`
            :param resource_pool: Identifier of the resource pool.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
            :type  name: :class:`str`
            :param name: Name of the resource pool.
            """
            self.resource_pool = resource_pool
            self.name = name
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.summary', {
            'resource_pool': type.IdType(resource_types='ResourcePool'),
            'name': type.StringType(),
        },
        Summary,
        False,
        None))


    class ResourceAllocationCreateSpec(VapiStruct):
        """
        The ``ResourcePool.ResourceAllocationCreateSpec`` class contains resource
        allocation information used to create a resource pool, see
        :func:`ResourcePool.create`.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reservation=None,
                     expandable_reservation=None,
                     limit=None,
                     shares=None,
                    ):
            """
            :type  reservation: :class:`long` or ``None``
            :param reservation: Amount of resource that is guaranteed available to a resource pool.
                Reserved resources are not wasted if they are not used. If the
                utilization is less than the reservation, the resources can be
                utilized by other running virtual machines. Units are MB fo memory,
                and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty,
                :attr:`ResourcePool.ResourceAllocationCreateSpec.reservation` will
                be set to 0.
            :type  expandable_reservation: :class:`bool` or ``None``
            :param expandable_reservation: In a resource pool with an expandable reservation, the reservation
                can grow beyond the specified value, if the parent resource pool
                has unreserved resources. A non-expandable reservation is called a
                fixed reservation.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty,
                :attr:`ResourcePool.ResourceAllocationCreateSpec.expandable_reservation`
                will be set to true.
            :type  limit: :class:`long` or ``None``
            :param limit: The utilization of a resource pool will not exceed this limit, even
                if there are available resources. This is typically used to ensure
                a consistent performance of resource pools independent of available
                resources. If set to -1, then there is no fixed limit on resource
                usage (only bounded by available resources and shares). Units are
                MB for memory, and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty,
                :attr:`ResourcePool.ResourceAllocationCreateSpec.limit` will be set
                to -1.
            :type  shares: :class:`ResourcePool.SharesInfo` or ``None``
            :param shares: Shares are used in case of resource contention.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty,
                :attr:`ResourcePool.ResourceAllocationCreateSpec.shares` will be
                set to ':attr:`ResourcePool.SharesInfo.Level.NORMAL`'.
            """
            self.reservation = reservation
            self.expandable_reservation = expandable_reservation
            self.limit = limit
            self.shares = shares
            VapiStruct.__init__(self)


    ResourceAllocationCreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.resource_allocation_create_spec', {
            'reservation': type.OptionalType(type.IntegerType()),
            'expandable_reservation': type.OptionalType(type.BooleanType()),
            'limit': type.OptionalType(type.IntegerType()),
            'shares': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.SharesInfo')),
        },
        ResourceAllocationCreateSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The  class contains information used to create a resource pool, see
        :func:`ResourcePool.create`.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     parent=None,
                     cpu_allocation=None,
                     memory_allocation=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the resource pool.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  parent: :class:`str`
            :param parent: Parent of the created resource pool.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
            :type  cpu_allocation: :class:`ResourcePool.ResourceAllocationCreateSpec` or ``None``
            :param cpu_allocation: Resource allocation for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                if None or empty, use the default CPU allocation specification.
            :type  memory_allocation: :class:`ResourcePool.ResourceAllocationCreateSpec` or ``None``
            :param memory_allocation: Resource allocation for memory.
                This attribute was added in **vSphere API 7.0.0.0**.
                if None or empty, use the default memory allocation specification.
            """
            self.name = name
            self.parent = parent
            self.cpu_allocation = cpu_allocation
            self.memory_allocation = memory_allocation
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.create_spec', {
            'name': type.StringType(),
            'parent': type.IdType(resource_types='ResourcePool'),
            'cpu_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationCreateSpec')),
            'memory_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationCreateSpec')),
        },
        CreateSpec,
        False,
        None))


    class ResourceAllocationUpdateSpec(VapiStruct):
        """
        The ``ResourceAllocationUpdateSpec`` class descrives the updates to be made
        to the resource allocation settings of a resource pool.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     reservation=None,
                     expandable_reservation=None,
                     limit=None,
                     shares=None,
                    ):
            """
            :type  reservation: :class:`long` or ``None``
            :param reservation: Amount of resource that is guaranteed available to a resource pool.
                Reserved resources are not wasted if they are not used. If the
                utilization is less than the reservation, the resources can be
                utilized by other running virtual machines. Units are MB fo memory,
                and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty, ``reservation`` will be set to 0.
            :type  expandable_reservation: :class:`bool` or ``None``
            :param expandable_reservation: In a resource pool with an expandable reservation, the reservation
                can grow beyond the specified value, if the parent resource pool
                has unreserved resources. A non-expandable reservation is called a
                fixed reservation.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty, ``expandableReservation`` will be set to true.
            :type  limit: :class:`long` or ``None``
            :param limit: The utilization of a resource pool will not exceed this limit, even
                if there are available resources. This is typically used to ensure
                a consistent performance of resource pools independent of available
                resources. If set to -1, then there is no fixed limit on resource
                usage (only bounded by available resources and shares). Units are
                MB for memory, and MHz for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty, ``limit`` will be set to -1.
            :type  shares: :class:`ResourcePool.SharesInfo` or ``None``
            :param shares: Shares are used in case of resource contention.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None or empty, ``shares`` will be set to
                ':attr:`ResourcePool.SharesInfo.Level.NORMAL`'.
            """
            self.reservation = reservation
            self.expandable_reservation = expandable_reservation
            self.limit = limit
            self.shares = shares
            VapiStruct.__init__(self)


    ResourceAllocationUpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.resource_allocation_update_spec', {
            'reservation': type.OptionalType(type.IntegerType()),
            'expandable_reservation': type.OptionalType(type.BooleanType()),
            'limit': type.OptionalType(type.IntegerType()),
            'shares': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.SharesInfo')),
        },
        ResourceAllocationUpdateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The  class contains specification for updating the configuration of a
        resource pool.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     cpu_allocation=None,
                     memory_allocation=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: Name of the resource pool.
                This attribute was added in **vSphere API 7.0.0.0**.
                if None or empty, the name of the resource pool will not be
                changed.
            :type  cpu_allocation: :class:`ResourcePool.ResourceAllocationUpdateSpec` or ``None``
            :param cpu_allocation: Resource allocation for CPU.
                This attribute was added in **vSphere API 7.0.0.0**.
                if None or empty, the CPU allocation of the resource pool will not
                be changed.
            :type  memory_allocation: :class:`ResourcePool.ResourceAllocationUpdateSpec` or ``None``
            :param memory_allocation: Resource allocation for memory.
                This attribute was added in **vSphere API 7.0.0.0**.
                if None or empty, the memory allocation of the resource pool will
                not be changed.
            """
            self.name = name
            self.cpu_allocation = cpu_allocation
            self.memory_allocation = memory_allocation
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.resource_pool.update_spec', {
            'name': type.OptionalType(type.StringType()),
            'cpu_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationUpdateSpec')),
            'memory_allocation': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.ResourceAllocationUpdateSpec')),
        },
        UpdateSpec,
        False,
        None))



    def get(self,
            resource_pool,
            ):
        """
        Retrieves information about the resource pool indicated by
        ``resource_pool``.

        :type  resource_pool: :class:`str`
        :param resource_pool: Identifier of the resource pool for which information should be
            retrieved.
            The parameter must be an identifier for the resource type:
            ``ResourcePool``.
        :rtype: :class:`ResourcePool.Info`
        :return: Information about the resource pool.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the resource pool indicated by ``resource_pool`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ResourcePool`` referenced by the parameter
              ``resource_pool`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'resource_pool': resource_pool,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) resource pools in vCenter matching the
        :class:`ResourcePool.FilterSpec`.

        :type  filter: :class:`ResourcePool.FilterSpec` or ``None``
        :param filter: Specification of matching resource pools for which information
            should be returned.
            If None, the behavior is equivalent to a
            :class:`ResourcePool.FilterSpec` with all attributes None which
            means all resource pools match the filter.
        :rtype: :class:`list` of :class:`ResourcePool.Summary`
        :return: Commonly used information about the resource pools matching the
            :class:`ResourcePool.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            If more than 1000 resource pools match the
            :class:`ResourcePool.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def create(self,
               spec,
               ):
        """
        Creates a resource pool.
        This method was added in **vSphere API 7.0.0.0**.

        :type  spec: :class:`ResourcePool.CreateSpec`
        :param spec: Specification of the new resource pool to be created, see
            :class:`ResourcePool.CreateSpec`.
        :rtype: :class:`str`
        :return: The identifier of the newly created resource pool.
            The return value will be an identifier for the resource type:
            ``ResourcePool``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If a parameter passed in the spec is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the resource specified in parent could not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            If the specified resource in parent is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to create the resource pool could
            not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`ResourcePool.CreateSpec.parent` requires
              ``Resource.CreatePool``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def delete(self,
               resource_pool,
               ):
        """
        Deletes a resource pool.
        This method was added in **vSphere API 7.0.0.0**.

        :type  resource_pool: :class:`str`
        :param resource_pool: Identifier of the resource pool to be deleted.
            The parameter must be an identifier for the resource type:
            ``ResourcePool``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the resource pool is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the resource pool is a root resource pool.
        """
        return self._invoke('delete',
                            {
                            'resource_pool': resource_pool,
                            })

    def update(self,
               resource_pool,
               spec,
               ):
        """
        Updates the configuration of a resource pool.
        This method was added in **vSphere API 7.0.0.0**.

        :type  resource_pool: :class:`str`
        :param resource_pool: Identifier of the resource pool.
            The parameter must be an identifier for the resource type:
            ``ResourcePool``.
        :type  spec: :class:`ResourcePool.UpdateSpec`
        :param spec: Specification for updating the configuration of the resource pool.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If any of the specified parameters is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the resource pool is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            If any of the resources needed to reconfigure the resource pool
            could not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ResourcePool`` referenced by the parameter
              ``resource_pool`` requires ``Resource.EditPool``.
        """
        return self._invoke('update',
                            {
                            'resource_pool': resource_pool,
                            'spec': spec,
                            })
class System(VapiInterface):
    """
    The ``System`` class contains methods for negotiating API communication
    parameters including release ID. 
    
    Software developers obtain a list of supported API release IDs from vCenter
    documentation or as part of the client library (SDK) they work with at the
    time they develop and test a solution. The software solution initiates a
    handshake by sending a prioritized list of release IDs supported by the
    solution. The server selects the first release ID it supports from the
    list. 
    
    Negotiating API release ID is necessary to use APIs utilizing inheritance
    based polymorphism. These include all VI/JSON APIs and a set of vSphere
    Automation APIs. vSphere Automation APIs that require API release ID state
    this in their documentation. Consult the Programming Guide and API
    reference documentation of specific methods for more information.
    This class was added in **vSphere API 8.0.2.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.system'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SystemStub)
        self._VAPI_OPERATION_IDS = {}

    class HelloResult(VapiStruct):
        """
        The ``System.HelloResult`` class contains common API communication
        parameters.
        This class was added in **vSphere API 8.0.2.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     api_release=None,
                    ):
            """
            :type  api_release: :class:`str`
            :param api_release: The ID of a mutually-supported API release. This ID should be used
                in subsequent API calls to the current vCenter system. 
                
                If there is no mutually-supported API release, the value will be an
                empty string, e.g. ``""``. Typically, this is a case where one of
                the parties is much older than the other party.
                This attribute was added in **vSphere API 8.0.2.0**.
            """
            self.api_release = api_release
            VapiStruct.__init__(self)


    HelloResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.system.hello_result', {
            'api_release': type.StringType(),
        },
        HelloResult,
        False,
        None))


    class HelloSpec(VapiStruct):
        """
        The ``System.HelloSpec`` class describes the API client preferences.
        This class was added in **vSphere API 8.0.2.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     api_releases=None,
                    ):
            """
            :type  api_releases: :class:`list` of :class:`str`
            :param api_releases: List of API release IDs that the client can work with in order of
                preference. The server will select the first mutually supported
                release ID.
                This attribute was added in **vSphere API 8.0.2.0**.
            """
            self.api_releases = api_releases
            VapiStruct.__init__(self)


    HelloSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.system.hello_spec', {
            'api_releases': type.ListType(type.StringType()),
        },
        HelloSpec,
        False,
        None))



    def hello(self,
              spec,
              ):
        """
        Negotiates common parameters for API communication. 
        
        This method selects mutually supported choices from the
        :attr:`System.HelloSpec.api_releases` list.
        This method was added in **vSphere API 8.0.2.0**.

        :type  spec: :class:`System.HelloSpec`
        :param spec: Client capabilities including list of supported API release IDs.
        :rtype: :class:`System.HelloResult`
        :return: Common parameters for API communication.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the list of client provided release IDs
            (:attr:`System.HelloSpec.api_releases`) is empty or the list is
            longer then 128 releases or given release ID is longer then 64
            characters.
        """
        return self._invoke('hello',
                            {
                            'spec': spec,
                            })
class VM(VapiInterface):
    """
    The ``VM`` class provides methods for managing the lifecycle of a virtual
    machine.
    """
    RESOURCE_TYPE = "VirtualMachine"
    """
    Resource type for virtual machines.

    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.VM'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VMStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'clone_task': 'clone$task'})
        self._VAPI_OPERATION_IDS.update({'relocate_task': 'relocate$task'})

    class InventoryPlacementSpec(VapiStruct):
        """
        The ``VM.InventoryPlacementSpec`` class contains information used to place
        a virtual machine in the vCenter inventory.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the virtual machine should be
                placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose a suitable
                folder for the virtual machine; if a folder cannot be chosen, the
                virtual machine creation operation will fail.
            """
            self.folder = folder
            VapiStruct.__init__(self)


    InventoryPlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.inventory_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
        },
        InventoryPlacementSpec,
        False,
        None))


    class ComputePlacementSpec(VapiStruct):
        """
        The ``VM.ComputePlacementSpec`` class contains information used to place a
        virtual machine on compute resources.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                    ):
            """
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the virtual machine should be placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                This attribute is currently required if both ``host`` and
                ``cluster`` are None. In the future, if this attribute is None, the
                system will attempt to choose a suitable resource pool for the
                virtual machine; if a resource pool cannot be chosen, the virtual
                machine creation operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` and ``cluster`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                This attribute may be None if ``resourcePool`` or ``cluster`` is
                specified. If None, the system will attempt to choose a suitable
                host for the virtual machine; if a host cannot be chosen, the
                virtual machine creation operation will fail.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster into which the virtual machine should be placed. 
                
                If ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. 
                
                If ``cluster`` and ``host`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            """
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            VapiStruct.__init__(self)


    ComputePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.compute_placement_spec', {
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
        },
        ComputePlacementSpec,
        False,
        None))


    class StoragePlacementSpec(VapiStruct):
        """
        The ``VM.StoragePlacementSpec`` class contains information used to store a
        virtual machine's files.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                    ):
            """
            :type  datastore: :class:`str` or ``None``
            :param datastore: Datastore on which the virtual machine's configuration state should
                be stored. This datastore will also be used for any virtual disks
                that are created as part of the virtual machine creation operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose suitable
                storage for the virtual machine; if storage cannot be chosen, the
                virtual machine creation operation will fail.
            """
            self.datastore = datastore
            VapiStruct.__init__(self)


    StoragePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.storage_placement_spec', {
            'datastore': type.OptionalType(type.IdType()),
        },
        StoragePlacementSpec,
        False,
        None))


    class PlacementSpec(VapiStruct):
        """
        The ``VM.PlacementSpec`` class contains information used to place a virtual
        machine onto resources within the vCenter inventory.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                     datastore=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the virtual machine should be
                placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose a suitable
                folder for the virtual machine; if a folder cannot be chosen, the
                virtual machine creation operation will fail.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the virtual machine should be placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                This attribute is currently required if both ``host`` and
                ``cluster`` are None. In the future, if this attribute is None, the
                system will attempt to choose a suitable resource pool for the
                virtual machine; if a resource pool cannot be chosen, the virtual
                machine creation operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` and ``cluster`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                This attribute may be None if ``resourcePool`` or ``cluster`` is
                specified. If None, the system will attempt to choose a suitable
                host for the virtual machine; if a host cannot be chosen, the
                virtual machine creation operation will fail.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster into which the virtual machine should be placed. 
                
                If ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. 
                
                If ``cluster`` and ``host`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            :type  datastore: :class:`str` or ``None``
            :param datastore: Datastore on which the virtual machine's configuration state should
                be stored. This datastore will also be used for any virtual disks
                that are created as part of the virtual machine creation operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose suitable
                storage for the virtual machine; if storage cannot be chosen, the
                virtual machine creation operation will fail.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            self.datastore = datastore
            VapiStruct.__init__(self)


    PlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
            'datastore': type.OptionalType(type.IdType()),
        },
        PlacementSpec,
        False,
        None))


    class StoragePolicySpec(VapiStruct):
        """
        The ``VM.StoragePolicySpec`` class contains information about the storage
        policy to be associated with a virtual machine object.
        This class was added in **vSphere API 6.7**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     policy=None,
                    ):
            """
            :type  policy: :class:`str`
            :param policy: Identifier of the storage policy which should be associated with
                the virtual machine.
                This attribute was added in **vSphere API 6.7**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.StoragePolicy``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.vcenter.StoragePolicy``.
            """
            self.policy = policy
            VapiStruct.__init__(self)


    StoragePolicySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.storage_policy_spec', {
            'policy': type.IdType(resource_types='com.vmware.vcenter.StoragePolicy'),
        },
        StoragePolicySpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        Document-based creation spec.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'guest_OS': 'guest_os',
                                }

        def __init__(self,
                     guest_os=None,
                     name=None,
                     placement=None,
                     hardware_version=None,
                     boot=None,
                     boot_devices=None,
                     cpu=None,
                     memory=None,
                     disks=None,
                     nics=None,
                     cdroms=None,
                     floppies=None,
                     parallel_ports=None,
                     serial_ports=None,
                     sata_adapters=None,
                     scsi_adapters=None,
                     nvme_adapters=None,
                     storage_policy=None,
                    ):
            """
            :type  guest_os: :class:`com.vmware.vcenter.vm_client.GuestOS`
            :param guest_os: Guest OS.
            :type  name: :class:`str` or ``None``
            :param name: Virtual machine name.
                If None, a default name will be generated by the server.
            :type  placement: :class:`VM.PlacementSpec` or ``None``
            :param placement: Virtual machine placement information.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose suitable
                resources on which to place the virtual machine.
            :type  hardware_version: :class:`com.vmware.vcenter.vm_client.Hardware.Version` or ``None``
            :param hardware_version: Virtual hardware version.
                If None, defaults to the most recent version supported by the
                server.
            :type  boot: :class:`com.vmware.vcenter.vm.hardware_client.Boot.CreateSpec` or ``None``
            :param boot: Boot configuration.
                If None, guest-specific default values will be used.
            :type  boot_devices: :class:`list` of :class:`com.vmware.vcenter.vm.hardware.boot_client.Device.EntryCreateSpec` or ``None``
            :param boot_devices: Boot device configuration.
                If None, a server-specific boot sequence will be used.
            :type  cpu: :class:`com.vmware.vcenter.vm.hardware_client.Cpu.UpdateSpec` or ``None``
            :param cpu: CPU configuration.
                If None, guest-specific default values will be used.
            :type  memory: :class:`com.vmware.vcenter.vm.hardware_client.Memory.UpdateSpec` or ``None``
            :param memory: Memory configuration.
                If None, guest-specific default values will be used.
            :type  disks: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Disk.CreateSpec` or ``None``
            :param disks: List of disks.
                If None, a single blank virtual disk of a guest-specific size will
                be created on the same storage as the virtual machine
                configuration, and will use a guest-specific host bus adapter type.
                If the guest-specific size is 0, no virtual disk will be created.
            :type  nics: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Ethernet.CreateSpec` or ``None``
            :param nics: List of Ethernet adapters.
                If None, no Ethernet adapters will be created.
            :type  cdroms: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Cdrom.CreateSpec` or ``None``
            :param cdroms: List of CD-ROMs.
                If None, no CD-ROM devices will be created.
            :type  floppies: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Floppy.CreateSpec` or ``None``
            :param floppies: List of floppy drives.
                If None, no floppy drives will be created.
            :type  parallel_ports: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Parallel.CreateSpec` or ``None``
            :param parallel_ports: List of parallel ports.
                If None, no parallel ports will be created.
            :type  serial_ports: :class:`list` of :class:`com.vmware.vcenter.vm.hardware_client.Serial.CreateSpec` or ``None``
            :param serial_ports: List of serial ports.
                If None, no serial ports will be created.
            :type  sata_adapters: :class:`list` of :class:`com.vmware.vcenter.vm.hardware.adapter_client.Sata.CreateSpec` or ``None``
            :param sata_adapters: List of SATA adapters.
                If None, any adapters necessary to connect the virtual machine's
                storage devices will be created; this includes any devices that
                explicitly specify a SATA host bus adapter, as well as any devices
                that do not specify a host bus adapter if the guest's preferred
                adapter type is SATA.
            :type  scsi_adapters: :class:`list` of :class:`com.vmware.vcenter.vm.hardware.adapter_client.Scsi.CreateSpec` or ``None``
            :param scsi_adapters: List of SCSI adapters.
                If None, any adapters necessary to connect the virtual machine's
                storage devices will be created; this includes any devices that
                explicitly specify a SCSI host bus adapter, as well as any devices
                that do not specify a host bus adapter if the guest's preferred
                adapter type is SCSI. The type of the SCSI adapter will be a
                guest-specific default type.
            :type  nvme_adapters: :class:`list` of :class:`com.vmware.vcenter.vm.hardware.adapter_client.Nvme.CreateSpec` or ``None``
            :param nvme_adapters: List of NVMe adapters.
                This attribute was added in **vSphere API 7.0.0.1**.
                If None, any adapters necessary to connect the virtual machine's
                storage devices will be created; this includes any devices that
                explicitly specify a NVMe host bus adapter, as well as any devices
                that do not specify a host bus adapter if the guest's preferred
                adapter type is NVMe.
            :type  storage_policy: :class:`VM.StoragePolicySpec` or ``None``
            :param storage_policy: The ``VM.StoragePolicySpec`` class contains information about the
                storage policy that is to be associated with the virtual machine
                home (which contains the configuration and log files).
                This attribute was added in **vSphere API 6.7**.
                If None the datastore default storage policy (if applicable) is
                applied. Currently a default storage policy is only supported by
                object datastores : VVol and vSAN. For non-object datastores, if
                None then no storage policy would be associated with the virtual
                machine home.
            """
            self.guest_os = guest_os
            self.name = name
            self.placement = placement
            self.hardware_version = hardware_version
            self.boot = boot
            self.boot_devices = boot_devices
            self.cpu = cpu
            self.memory = memory
            self.disks = disks
            self.nics = nics
            self.cdroms = cdroms
            self.floppies = floppies
            self.parallel_ports = parallel_ports
            self.serial_ports = serial_ports
            self.sata_adapters = sata_adapters
            self.scsi_adapters = scsi_adapters
            self.nvme_adapters = nvme_adapters
            self.storage_policy = storage_policy
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.create_spec', {
            'guest_OS': type.ReferenceType('com.vmware.vcenter.vm_client', 'GuestOS'),
            'name': type.OptionalType(type.StringType()),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VM.PlacementSpec')),
            'hardware_version': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm_client', 'Hardware.Version')),
            'boot': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Boot.CreateSpec')),
            'boot_devices': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware.boot_client', 'Device.EntryCreateSpec'))),
            'cpu': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Cpu.UpdateSpec')),
            'memory': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Memory.UpdateSpec')),
            'disks': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Disk.CreateSpec'))),
            'nics': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Ethernet.CreateSpec'))),
            'cdroms': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Cdrom.CreateSpec'))),
            'floppies': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Floppy.CreateSpec'))),
            'parallel_ports': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Parallel.CreateSpec'))),
            'serial_ports': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Serial.CreateSpec'))),
            'sata_adapters': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Sata.CreateSpec'))),
            'scsi_adapters': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Scsi.CreateSpec'))),
            'nvme_adapters': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Nvme.CreateSpec'))),
            'storage_policy': type.OptionalType(type.ReferenceType(__name__, 'VM.StoragePolicySpec')),
        },
        CreateSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        Document-based info.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'guest_OS': 'guest_os',
                                }

        def __init__(self,
                     guest_os=None,
                     name=None,
                     identity=None,
                     power_state=None,
                     instant_clone_frozen=None,
                     hardware=None,
                     boot=None,
                     boot_devices=None,
                     cpu=None,
                     memory=None,
                     disks=None,
                     nics=None,
                     cdroms=None,
                     floppies=None,
                     parallel_ports=None,
                     serial_ports=None,
                     sata_adapters=None,
                     scsi_adapters=None,
                     nvme_adapters=None,
                    ):
            """
            :type  guest_os: :class:`com.vmware.vcenter.vm_client.GuestOS`
            :param guest_os: Guest OS.
            :type  name: :class:`str`
            :param name: Virtual machine name.
            :type  identity: :class:`com.vmware.vcenter.vm_client.Identity.Info`
            :param identity: Identity of the virtual machine.
                This attribute was added in **vSphere API 6.7.1**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  power_state: :class:`com.vmware.vcenter.vm_client.Power.State`
            :param power_state: Power state of the virtual machine.
            :type  instant_clone_frozen: :class:`bool`
            :param instant_clone_frozen: Indicates whether the virtual machine is frozen for instant clone,
                or not.
                This attribute was added in **vSphere API 6.7.1**.
                This attribute is optional because it was added in a newer version
                than its parent node.
            :type  hardware: :class:`com.vmware.vcenter.vm_client.Hardware.Info`
            :param hardware: Virtual hardware version information.
            :type  boot: :class:`com.vmware.vcenter.vm.hardware_client.Boot.Info`
            :param boot: Boot configuration.
            :type  boot_devices: :class:`list` of :class:`com.vmware.vcenter.vm.hardware.boot_client.Device.Entry`
            :param boot_devices: Boot device configuration. If the :class:`list` has no entries, a
                server-specific default boot sequence is used.
            :type  cpu: :class:`com.vmware.vcenter.vm.hardware_client.Cpu.Info`
            :param cpu: CPU configuration.
            :type  memory: :class:`com.vmware.vcenter.vm.hardware_client.Memory.Info`
            :param memory: Memory configuration.
            :type  disks: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Disk.Info`
            :param disks: List of disks.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Disk``. When methods return
                a value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``.
            :type  nics: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Ethernet.Info`
            :param nics: List of Ethernet adapters.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``.
            :type  cdroms: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Cdrom.Info`
            :param cdroms: List of CD-ROMs.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Cdrom``. When methods return
                a value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Cdrom``.
            :type  floppies: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Floppy.Info`
            :param floppies: List of floppy drives.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Floppy``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Floppy``.
            :type  parallel_ports: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Parallel.Info`
            :param parallel_ports: List of parallel ports.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ParallelPort``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ParallelPort``.
            :type  serial_ports: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Serial.Info`
            :param serial_ports: List of serial ports.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SerialPort``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SerialPort``.
            :type  sata_adapters: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware.adapter_client.Sata.Info`
            :param sata_adapters: List of SATA adapters.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SataAdapter``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SataAdapter``.
            :type  scsi_adapters: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware.adapter_client.Scsi.Info`
            :param scsi_adapters: List of SCSI adapters.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ScsiAdapter``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ScsiAdapter``.
            :type  nvme_adapters: :class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware.adapter_client.Nvme.Info`
            :param nvme_adapters: List of NVMe adapters.
                This attribute was added in **vSphere API 7.0.0.1**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.NvmeAdapter``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.NvmeAdapter``.
                This attribute is optional because it was added in a newer version
                than its parent node.
            """
            self.guest_os = guest_os
            self.name = name
            self.identity = identity
            self.power_state = power_state
            self.instant_clone_frozen = instant_clone_frozen
            self.hardware = hardware
            self.boot = boot
            self.boot_devices = boot_devices
            self.cpu = cpu
            self.memory = memory
            self.disks = disks
            self.nics = nics
            self.cdroms = cdroms
            self.floppies = floppies
            self.parallel_ports = parallel_ports
            self.serial_ports = serial_ports
            self.sata_adapters = sata_adapters
            self.scsi_adapters = scsi_adapters
            self.nvme_adapters = nvme_adapters
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.info', {
            'guest_OS': type.ReferenceType('com.vmware.vcenter.vm_client', 'GuestOS'),
            'name': type.StringType(),
            'identity': type.OptionalType(type.ReferenceType('com.vmware.vcenter.vm_client', 'Identity.Info')),
            'power_state': type.ReferenceType('com.vmware.vcenter.vm_client', 'Power.State'),
            'instant_clone_frozen': type.OptionalType(type.BooleanType()),
            'hardware': type.ReferenceType('com.vmware.vcenter.vm_client', 'Hardware.Info'),
            'boot': type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Boot.Info'),
            'boot_devices': type.ListType(type.ReferenceType('com.vmware.vcenter.vm.hardware.boot_client', 'Device.Entry')),
            'cpu': type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Cpu.Info'),
            'memory': type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Memory.Info'),
            'disks': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Disk.Info')),
            'nics': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Ethernet.Info')),
            'cdroms': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Cdrom.Info')),
            'floppies': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Floppy.Info')),
            'parallel_ports': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Parallel.Info')),
            'serial_ports': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Serial.Info')),
            'sata_adapters': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Sata.Info')),
            'scsi_adapters': type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Scsi.Info')),
            'nvme_adapters': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware.adapter_client', 'Nvme.Info'))),
        },
        Info,
        False,
        None))


    class GuestCustomizationSpec(VapiStruct):
        """
        The ``VM.GuestCustomizationSpec`` class contains information required to
        customize a virtual machine when deploying it.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: Name of the customization specification.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None, no guest customization is performed.
            """
            self.name = name
            VapiStruct.__init__(self)


    GuestCustomizationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.guest_customization_spec', {
            'name': type.OptionalType(type.StringType()),
        },
        GuestCustomizationSpec,
        False,
        None))


    class DiskCloneSpec(VapiStruct):
        """
        Document-based disk clone spec.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                    ):
            """
            :type  datastore: :class:`str` or ``None``
            :param datastore: Destination datastore to clone disk.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                This attribute is currently required. In the future, if this
                attribute is None disk will be copied to the datastore specified in
                the :attr:`VM.ClonePlacementSpec.datastore` attribute of
                :attr:`VM.CloneSpec.placement`.
            """
            self.datastore = datastore
            VapiStruct.__init__(self)


    DiskCloneSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.disk_clone_spec', {
            'datastore': type.OptionalType(type.IdType()),
        },
        DiskCloneSpec,
        False,
        None))


    class ClonePlacementSpec(VapiStruct):
        """
        The ``VM.ClonePlacementSpec`` class contains information used to place a
        clone of a virtual machine onto resources within the vCenter inventory.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                     datastore=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the cloned virtual machine should
                be placed.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If attribute is None, the system will use the virtual machine
                folder of the source virtual machine. If this results in a conflict
                due to other placement parameters, the virtual machine clone
                operation will fail.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the cloned virtual machine should be
                placed.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If attribute is None, the system will use the resource pool of the
                source virtual machine. If this results in a conflict due to other
                placement parameters, the virtual machine clone operation will
                fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the cloned virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` and ``cluster`` are both specified, ``host`` must be a
                member of ``cluster``.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If this attribute is unset, if ``resourcePool`` is unset, the
                cloned virtual machine will use the host of the source virtual
                machine. if ``resourcePool`` is set, and the target is a standalone
                host, the host is used. if ``resourcePool`` is set, and the target
                is a DRS cluster, a host will be picked by DRS. if ``resourcePool``
                is set, and the target is a cluster without DRS, InvalidArgument
                will be thrown.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster into which the cloned virtual machine should be placed. 
                
                If ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. 
                
                If ``cluster`` and ``host`` are both specified, ``host`` must be a
                member of ``cluster``.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            :type  datastore: :class:`str` or ``None``
            :param datastore: Datastore on which the cloned virtual machine's configuration state
                should be stored. This datastore will also be used for any virtual
                disks that are created as part of the virtual machine clone
                operation unless individually overridden.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                If attribute is None, the system will use the datastore of the
                source virtual machine.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            self.datastore = datastore
            VapiStruct.__init__(self)


    ClonePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.clone_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
            'datastore': type.OptionalType(type.IdType()),
        },
        ClonePlacementSpec,
        False,
        None))


    class CloneSpec(VapiStruct):
        """
        Document-based clone spec.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     source=None,
                     name=None,
                     placement=None,
                     disks_to_remove=None,
                     disks_to_update=None,
                     power_on=None,
                     guest_customization_spec=None,
                    ):
            """
            :type  source: :class:`str`
            :param source: Virtual machine to clone from.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  name: :class:`str`
            :param name: Virtual machine name.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  placement: :class:`VM.ClonePlacementSpec` or ``None``
            :param placement: Virtual machine placement information.
                This attribute was added in **vSphere API 7.0.0.0**.
                If this attribute is None, the system will use the values from the
                source virtual machine. If specified, each field will be used for
                placement. If the fields result in disjoint placement the operation
                will fail. If the fields along with the placement values of the
                source virtual machine result in disjoint placement the operation
                will fail.
            :type  disks_to_remove: :class:`set` of :class:`str` or ``None``
            :param disks_to_remove: Set of Disks to Remove.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``.
                If None, all disks will be copied. If the same identifier is in
                :attr:`VM.CloneSpec.disks_to_update` InvalidArgument fault will be
                returned.
            :type  disks_to_update: (:class:`dict` of :class:`str` and :class:`VM.DiskCloneSpec`) or ``None``
            :param disks_to_update: Map of Disks to Update.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Disk``. When methods return
                a value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``.
                If None, all disks will copied to the datastore specified in the
                :attr:`VM.ClonePlacementSpec.datastore` attribute of
                :attr:`VM.CloneSpec.placement`. If the same identifier is in
                :attr:`VM.CloneSpec.disks_to_remove` InvalidArgument fault will be
                thrown.
            :type  power_on: :class:`bool` or ``None``
            :param power_on: Attempt to perform a :attr:`VM.CloneSpec.power_on` after clone.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None, the virtual machine will not be powered on.
            :type  guest_customization_spec: :class:`VM.GuestCustomizationSpec` or ``None``
            :param guest_customization_spec: Guest customization spec to apply to the virtual machine after the
                virtual machine is deployed.
                This attribute was added in **vSphere API 7.0.0.0**.
                If None, the guest operating system is not customized after clone.
            """
            self.source = source
            self.name = name
            self.placement = placement
            self.disks_to_remove = disks_to_remove
            self.disks_to_update = disks_to_update
            self.power_on = power_on
            self.guest_customization_spec = guest_customization_spec
            VapiStruct.__init__(self)


    CloneSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.clone_spec', {
            'source': type.IdType(resource_types='VirtualMachine'),
            'name': type.StringType(),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VM.ClonePlacementSpec')),
            'disks_to_remove': type.OptionalType(type.SetType(type.IdType())),
            'disks_to_update': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'VM.DiskCloneSpec'))),
            'power_on': type.OptionalType(type.BooleanType()),
            'guest_customization_spec': type.OptionalType(type.ReferenceType(__name__, 'VM.GuestCustomizationSpec')),
        },
        CloneSpec,
        False,
        None))


    class DiskRelocateSpec(VapiStruct):
        """
        Document-based disk relocate spec.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                    ):
            """
            :type  datastore: :class:`str` or ``None``
            :param datastore: Destination datastore to relocate disk.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                This attribute is currently required. In the future, if this
                attribute is unset, disk will use the datastore specified in
                :attr:`VM.RelocatePlacementSpec.datastore` attribute of
                :attr:`VM.RelocateSpec.placement`.
            """
            self.datastore = datastore
            VapiStruct.__init__(self)


    DiskRelocateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.disk_relocate_spec', {
            'datastore': type.OptionalType(type.IdType()),
        },
        DiskRelocateSpec,
        False,
        None))


    class RelocatePlacementSpec(VapiStruct):
        """
        The ``VM.RelocatePlacementSpec`` class contains information used to change
        the placement of an existing virtual machine within the vCenter inventory.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                     datastore=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the virtual machine should be
                placed.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If this attribute is None, the virtual machine will stay in the
                current folder.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the virtual machine should be placed.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If this attribute is None, the virtual machine will stay in the
                current resource pool.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` and ``cluster`` are both specified, ``host`` must be a
                member of ``cluster``.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If this attribute is unset, if ``resourcePool`` is unset, the
                virtual machine will remain on the current host. if
                ``resourcePool`` is set, and the target is a standalone host, the
                host is used. if ``resourcePool`` is set, and the target is a DRS
                cluster, a host will be picked by DRS. if ``resourcePool`` is set,
                and the target is a cluster without DRS, InvalidArgument will be
                thrown.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster into which the virtual machine should be placed. 
                
                If ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. 
                
                If ``cluster`` and ``host`` are both specified, ``host`` must be a
                member of ``cluster``.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            :type  datastore: :class:`str` or ``None``
            :param datastore: Datastore on which the virtual machine's configuration state should
                be stored. This datastore will also be used for any virtual disks
                that are associated with the virtual machine, unless individually
                overridden.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                If this attribute is None, the virtual machine will remain on the
                current datastore.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            self.datastore = datastore
            VapiStruct.__init__(self)


    RelocatePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.relocate_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
            'datastore': type.OptionalType(type.IdType()),
        },
        RelocatePlacementSpec,
        False,
        None))


    class RelocateSpec(VapiStruct):
        """
        Document-based relocate spec.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     placement=None,
                     disks=None,
                    ):
            """
            :type  placement: :class:`VM.RelocatePlacementSpec` or ``None``
            :param placement: Virtual machine placement information.
                This attribute was added in **vSphere API 7.0.0.0**.
                If this attribute is None, the system will use the values from the
                source virtual machine. If specified, each field will be used for
                placement. If the fields result in disjoint placement the operation
                will fail. If the fields along with the other existing placement of
                the virtual machine result in disjoint placement the operation will
                fail.
            :type  disks: (:class:`dict` of :class:`str` and :class:`VM.DiskRelocateSpec`) or ``None``
            :param disks: Individual disk relocation map.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Disk``. When methods return
                a value of this class as a return value, the key in the attribute
                :class:`dict` will be an identifier for the resource type:
                ``com.vmware.vcenter.vm.hardware.Disk``.
                If None, all disks will migrate to the datastore specified in the
                :attr:`VM.RelocatePlacementSpec.datastore` attribute of
                :attr:`VM.RelocateSpec.placement`.
            """
            self.placement = placement
            self.disks = disks
            VapiStruct.__init__(self)


    RelocateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.relocate_spec', {
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VM.RelocatePlacementSpec')),
            'disks': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType(__name__, 'VM.DiskRelocateSpec'))),
        },
        RelocateSpec,
        False,
        None))


    class InstantClonePlacementSpec(VapiStruct):
        """
        The ``VM.InstantClonePlacementSpec`` class contains information used to
        place an InstantClone of a virtual machine onto resources within the
        vCenter inventory.
        This class was added in **vSphere API 6.7.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     datastore=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the InstantCloned virtual machine
                should be placed.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If attribute is None, the system will use the virtual machine
                folder of the source virtual machine.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the InstantCloned virtual machine should
                be placed.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If attribute is None, the system will use the resource pool of the
                source virtual machine.
            :type  datastore: :class:`str` or ``None``
            :param datastore: Datastore on which the InstantCloned virtual machine's
                configuration state should be stored. This datastore will also be
                used for any virtual disks that are created as part of the virtual
                machine InstantClone operation.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                If attribute is None, the system will use the datastore of the
                source virtual machine.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.datastore = datastore
            VapiStruct.__init__(self)


    InstantClonePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.instant_clone_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'datastore': type.OptionalType(type.IdType()),
        },
        InstantClonePlacementSpec,
        False,
        None))


    class InstantCloneSpec(VapiStruct):
        """
        Document-based InstantClone spec.
        This class was added in **vSphere API 6.7.1**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     source=None,
                     name=None,
                     placement=None,
                     nics_to_update=None,
                     disconnect_all_nics=None,
                     parallel_ports_to_update=None,
                     serial_ports_to_update=None,
                     bios_uuid=None,
                    ):
            """
            :type  source: :class:`str`
            :param source: Virtual machine to InstantClone from.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  name: :class:`str`
            :param name: Name of the new virtual machine.
                This attribute was added in **vSphere API 6.7.1**.
            :type  placement: :class:`VM.InstantClonePlacementSpec` or ``None``
            :param placement: Virtual machine placement information.
                This attribute was added in **vSphere API 6.7.1**.
                If this attribute is None, the system will use the values from the
                source virtual machine. If specified, each field will be used for
                placement. If the fields result in disjoint placement the operation
                will fail. If the fields along with the placement values of the
                source virtual machine result in disjoint placement the operation
                will fail.
            :type  nics_to_update: (:class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Ethernet.UpdateSpec`) or ``None``
            :param nics_to_update: Map of NICs to update.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.Ethernet``.
                If None, no NICs will be updated.
            :type  disconnect_all_nics: :class:`bool` or ``None``
            :param disconnect_all_nics: Indicates whether all NICs on the destination virtual machine
                should be disconnected from the newtwork
                This attribute was added in **vSphere API 6.7.1**.
                If None, connection status of all NICs on the destination virtual
                machine will be the same as on the source virtual machine.
            :type  parallel_ports_to_update: (:class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Parallel.UpdateSpec`) or ``None``
            :param parallel_ports_to_update: Map of parallel ports to Update.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ParallelPort``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.ParallelPort``.
                If None, no parallel ports will be updated.
            :type  serial_ports_to_update: (:class:`dict` of :class:`str` and :class:`com.vmware.vcenter.vm.hardware_client.Serial.UpdateSpec`) or ``None``
            :param serial_ports_to_update: Map of serial ports to Update.
                This attribute was added in **vSphere API 6.7.1**.
                When clients pass a value of this class as a parameter, the key in
                the attribute :class:`dict` must be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SerialPort``. When methods
                return a value of this class as a return value, the key in the
                attribute :class:`dict` will be an identifier for the resource
                type: ``com.vmware.vcenter.vm.hardware.SerialPort``.
                If None, no serial ports will be updated.
            :type  bios_uuid: :class:`str` or ``None``
            :param bios_uuid: 128-bit SMBIOS UUID of a virtual machine represented as a
                hexadecimal string in "12345678-abcd-1234-cdef-123456789abc"
                format.
                This attribute was added in **vSphere API 6.7.1**.
                If None, will be generated.
            """
            self.source = source
            self.name = name
            self.placement = placement
            self.nics_to_update = nics_to_update
            self.disconnect_all_nics = disconnect_all_nics
            self.parallel_ports_to_update = parallel_ports_to_update
            self.serial_ports_to_update = serial_ports_to_update
            self.bios_uuid = bios_uuid
            VapiStruct.__init__(self)


    InstantCloneSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.instant_clone_spec', {
            'source': type.IdType(resource_types='VirtualMachine'),
            'name': type.StringType(),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VM.InstantClonePlacementSpec')),
            'nics_to_update': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Ethernet.UpdateSpec'))),
            'disconnect_all_nics': type.OptionalType(type.BooleanType()),
            'parallel_ports_to_update': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Parallel.UpdateSpec'))),
            'serial_ports_to_update': type.OptionalType(type.MapType(type.IdType(), type.ReferenceType('com.vmware.vcenter.vm.hardware_client', 'Serial.UpdateSpec'))),
            'bios_uuid': type.OptionalType(type.StringType()),
        },
        InstantCloneSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``VM.FilterSpec`` class contains attributes used to filter the results
        when listing virtual machines (see :func:`VM.list`). If multiple attributes
        are specified, only virtual machines matching all of the attributes match
        the filter.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vms=None,
                     names=None,
                     folders=None,
                     datacenters=None,
                     hosts=None,
                     clusters=None,
                     resource_pools=None,
                     power_states=None,
                    ):
            """
            :type  vms: :class:`set` of :class:`str` or ``None``
            :param vms: Identifiers of virtual machines that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``VirtualMachine``.
                If None or empty, virtual machines with any identifier match the
                filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names that virtual machines must have to match the filter (see
                :attr:`VM.Info.name`).
                If None or empty, virtual machines with any name match the filter.
            :type  folders: :class:`set` of :class:`str` or ``None``
            :param folders: Folders that must contain the virtual machine for the virtual
                machine to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                If None or empty, virtual machines in any folder match the filter.
            :type  datacenters: :class:`set` of :class:`str` or ``None``
            :param datacenters: Datacenters that must contain the virtual machine for the virtual
                machine to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                If None or empty, virtual machines in any datacenter match the
                filter.
            :type  hosts: :class:`set` of :class:`str` or ``None``
            :param hosts: Hosts that must contain the virtual machine for the virtual machine
                to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                If None or empty, virtual machines on any host match the filter.
            :type  clusters: :class:`set` of :class:`str` or ``None``
            :param clusters: Clusters that must contain the virtual machine for the virtual
                machine to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, virtual machines in any cluster match the filter.
            :type  resource_pools: :class:`set` of :class:`str` or ``None``
            :param resource_pools: Resource pools that must contain the virtual machine for the
                virtual machine to match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``ResourcePool``.
                If None or empty, virtual machines in any resource pool match the
                filter.
            :type  power_states: :class:`set` of :class:`com.vmware.vcenter.vm_client.Power.State` or ``None``
            :param power_states: Power states that a virtual machine must be in to match the filter
                (see :attr:`com.vmware.vcenter.vm_client.Power.Info.state`.
                If None or empty, virtual machines in any power state match the
                filter.
            """
            self.vms = vms
            self.names = names
            self.folders = folders
            self.datacenters = datacenters
            self.hosts = hosts
            self.clusters = clusters
            self.resource_pools = resource_pools
            self.power_states = power_states
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.filter_spec', {
            'vms': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'resource_pools': type.OptionalType(type.SetType(type.IdType())),
            'power_states': type.OptionalType(type.SetType(type.ReferenceType('com.vmware.vcenter.vm_client', 'Power.State'))),
        },
        FilterSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``VM.Summary`` class contains commonly used information about a virtual
        machine.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """



        _canonical_to_pep_names = {
                                'memory_size_MiB': 'memory_size_mib',
                                }

        def __init__(self,
                     vm=None,
                     name=None,
                     power_state=None,
                     cpu_count=None,
                     memory_size_mib=None,
                    ):
            """
            :type  vm: :class:`str`
            :param vm: Identifier of the virtual machine.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  name: :class:`str`
            :param name: Name of the Virtual machine.
            :type  power_state: :class:`com.vmware.vcenter.vm_client.Power.State`
            :param power_state: Power state of the virtual machine.
            :type  cpu_count: :class:`long` or ``None``
            :param cpu_count: Number of CPU cores.
                This attribute will be None if the virtual machine configuration is
                not available. For example, the configuration information would be
                unavailable if the server is unable to access the virtual machine
                files on disk, and is often also unavailable during the intial
                phases of virtual machine creation.
            :type  memory_size_mib: :class:`long` or ``None``
            :param memory_size_mib: Memory size in mebibytes.
                This attribute will be None if the virtual machine configuration is
                not available. For example, the configuration information would be
                unavailable if the server is unable to access the virtual machine
                files on disk, and is often also unavailable during the intial
                phases of virtual machine creation.
            """
            self.vm = vm
            self.name = name
            self.power_state = power_state
            self.cpu_count = cpu_count
            self.memory_size_mib = memory_size_mib
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.summary', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'name': type.StringType(),
            'power_state': type.ReferenceType('com.vmware.vcenter.vm_client', 'Power.State'),
            'cpu_count': type.OptionalType(type.IntegerType()),
            'memory_size_MiB': type.OptionalType(type.IntegerType()),
        },
        Summary,
        False,
        None))


    class RegisterPlacementSpec(VapiStruct):
        """
        The ``VM.RegisterPlacementSpec`` class contains information used to place a
        virtual machine, created from existing virtual machine files on storage,
        onto resources within the vCenter inventory.
        This class was added in **vSphere API 6.8.7**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                     cluster=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the virtual machine should be
                placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose a suitable
                folder for the virtual machine; if a folder cannot be chosen, the
                virtual machine creation operation will fail.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the virtual machine should be placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                This attribute is currently required if both ``host`` and
                ``cluster`` are None. In the future, if this attribute is None, the
                system will attempt to choose a suitable resource pool for the
                virtual machine; if a resource pool cannot be chosen, the virtual
                machine creation operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` and ``cluster`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                This attribute may be None if ``resourcePool`` or ``cluster`` is
                specified. If None, the system will attempt to choose a suitable
                host for the virtual machine; if a host cannot be chosen, the
                virtual machine creation operation will fail.
            :type  cluster: :class:`str` or ``None``
            :param cluster: Cluster into which the virtual machine should be placed. 
                
                If ``cluster`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``cluster``. 
                
                If ``cluster`` and ``host`` are both specified, ``host`` must be a
                member of ``cluster``.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
                If ``resourcePool`` or ``host`` is specified, it is recommended
                that this attribute be None.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            self.cluster = cluster
            VapiStruct.__init__(self)


    RegisterPlacementSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.register_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
            'cluster': type.OptionalType(type.IdType()),
        },
        RegisterPlacementSpec,
        False,
        None))


    class RegisterSpec(VapiStruct):
        """
        The ``VM.RegisterSpec`` class contains information used to create a virtual
        machine from existing virtual machine files on storage. 
        
        The location of the virtual machine files on storage must be specified by
        providing either :attr:`VM.RegisterSpec.datastore` and
        :attr:`VM.RegisterSpec.path` or by providing
        :attr:`VM.RegisterSpec.datastore_path`. If
        :attr:`VM.RegisterSpec.datastore` and :attr:`VM.RegisterSpec.path` are
        :class:`set`, :attr:`VM.RegisterSpec.datastore_path` must be None, and if
        :attr:`VM.RegisterSpec.datastore_path` is :class:`set`,
        :attr:`VM.RegisterSpec.datastore` and :attr:`VM.RegisterSpec.path` must be
        None.
        This class was added in **vSphere API 6.8.7**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                     path=None,
                     datastore_path=None,
                     name=None,
                     placement=None,
                    ):
            """
            :type  datastore: :class:`str` or ``None``
            :param datastore: Identifier of the datastore on which the virtual machine's
                configuration state is stored.
                This attribute was added in **vSphere API 6.8.7**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
                If None, :attr:`VM.RegisterSpec.path` must also be None and
                :attr:`VM.RegisterSpec.datastore_path` must be :class:`set`.
            :type  path: :class:`str` or ``None``
            :param path: Path to the virtual machine's configuration file on the datastore
                corresponding to {\\\\@link #datastore).
                This attribute was added in **vSphere API 6.8.7**.
                If None, :attr:`VM.RegisterSpec.datastore` must also be None and
                :attr:`VM.RegisterSpec.datastore_path` must be :class:`set`.
            :type  datastore_path: :class:`str` or ``None``
            :param datastore_path: Datastore path for the virtual machine's configuration file in the
                format "[datastore name] path". For example "[storage1]
                Test-VM/Test-VM.vmx".
                This attribute was added in **vSphere API 6.8.7**.
                If None, both :attr:`VM.RegisterSpec.datastore` and
                :attr:`VM.RegisterSpec.path` must be :class:`set`.
            :type  name: :class:`str` or ``None``
            :param name: Virtual machine name.
                This attribute was added in **vSphere API 6.8.7**.
                If None, the display name from the virtual machine's configuration
                file will be used.
            :type  placement: :class:`VM.RegisterPlacementSpec` or ``None``
            :param placement: Virtual machine placement information.
                This attribute was added in **vSphere API 6.8.7**.
                This attribute is currently required. In the future, if this
                attribute is None, the system will attempt to choose suitable
                resources on which to place the virtual machine.
            """
            self.datastore = datastore
            self.path = path
            self.datastore_path = datastore_path
            self.name = name
            self.placement = placement
            VapiStruct.__init__(self)


    RegisterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.VM.register_spec', {
            'datastore': type.OptionalType(type.IdType()),
            'path': type.OptionalType(type.StringType()),
            'datastore_path': type.OptionalType(type.StringType()),
            'name': type.OptionalType(type.StringType()),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VM.RegisterPlacementSpec')),
        },
        RegisterSpec,
        False,
        None))



    def create(self,
               spec,
               ):
        """
        Creates a virtual machine.

        :type  spec: :class:`VM.CreateSpec`
        :param spec: Virtual machine specification.
        :rtype: :class:`str`
        :return: ID of newly-created virtual machine.
            The return value will be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec could not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInUse` 
            if any of the specified storage addresses (eg. IDE, SATA, SCSI,
            NVMe) result in a storage address conflict.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to create the virtual machine could
            not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if ``guestOS`` is not supported for the requested virtual hardware
            version and spec includes None attributes that default to
            guest-specific values.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``Folder`` referenced by the attribute
              :attr:`VM.InventoryPlacementSpec.folder` requires
              ``VirtualMachine.Inventory.Create``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.ComputePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.StoragePlacementSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Network`` referenced by the attribute
              :attr:`com.vmware.vcenter.vm.hardware_client.Ethernet.BackingSpec.network`
              requires ``Network.Assign``.
        """
        return self._invoke('create',
                            {
                            'spec': spec,
                            })

    def clone(self,
              spec,
              ):
        """
        Creates a virtual machine from an existing virtual machine. 
        This method was added in **vSphere API 7.0.0.0**.

        :type  spec: :class:`VM.CloneSpec`
        :param spec: Virtual machine clone specification.
        :rtype: :class:`str`
        :return: ID of newly-created virtual machine.
            The return value will be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec could not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to clone the virtual machine could
            not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.DiskCloneSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.folder` requires
              ``VirtualMachine.Inventory.CreateFromExisting``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
            * The resource ``VirtualMachine`` referenced by the attribute
              :attr:`VM.CloneSpec.source` requires
              ``VirtualMachine.Provisioning.Clone``.
        """
        return self._invoke('clone',
                            {
                            'spec': spec,
                            })

    def clone_task(self,
              spec,
              ):
        """
        Creates a virtual machine from an existing virtual machine. 
        This method was added in **vSphere API 7.0.0.0**.

        :type  spec: :class:`VM.CloneSpec`
        :param spec: Virtual machine clone specification.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec could not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to clone the virtual machine could
            not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.DiskCloneSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.folder` requires
              ``VirtualMachine.Inventory.CreateFromExisting``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.ClonePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
            * The resource ``VirtualMachine`` referenced by the attribute
              :attr:`VM.CloneSpec.source` requires
              ``VirtualMachine.Provisioning.Clone``.
        """
        task_id = self._invoke('clone$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='VirtualMachine'))
        return task_instance

    def relocate(self,
                 vm,
                 spec,
                 ):
        """
        Relocates a virtual machine based on the specification. The parts of
        the virtual machine that can move are: FOLDER, RESOURCE_POOL, HOST,
        CLUSTER and DATASTORE of home of the virtual machine and disks. 
        This method was added in **vSphere API 7.0.0.0**.

        :type  vm: :class:`str`
        :param vm: Existing Virtual machine to relocate.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`VM.RelocateSpec`
        :param spec: Relocate specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec or the given "vm" could
            not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``Resource.ColdMigrate``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.RelocatePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
        """
        return self._invoke('relocate',
                            {
                            'vm': vm,
                            'spec': spec,
                            })

    def relocate_task(self,
                 vm,
                 spec,
                 ):
        """
        Relocates a virtual machine based on the specification. The parts of
        the virtual machine that can move are: FOLDER, RESOURCE_POOL, HOST,
        CLUSTER and DATASTORE of home of the virtual machine and disks. 
        This method was added in **vSphere API 7.0.0.0**.

        :type  vm: :class:`str`
        :param vm: Existing Virtual machine to relocate.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`VM.RelocateSpec`
        :param spec: Relocate specification.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec or the given "vm" could
            not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``Resource.ColdMigrate``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.RelocatePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
        """
        task_id = self._invoke('relocate$task',
                                {
                                'vm': vm,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance

    def instant_clone(self,
                      spec,
                      ):
        """
        Create an instant clone of an existing virtual machine.
        This method was added in **vSphere API 6.7.1**.

        :type  spec: :class:`VM.InstantCloneSpec`
        :param spec: Virtual machine InstantCloneSpec.
        :rtype: :class:`str`
        :return: ID of newly-created virtual machine.
            The return value will be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec could not be found
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to create an instant clone could not
            be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the attribute
              :attr:`VM.InstantCloneSpec.source` requires
              ``VirtualMachine.Provisioning.Clone`` and
              ``VirtualMachine.Inventory.CreateFromExisting``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`VM.InstantClonePlacementSpec.folder` requires
              ``VirtualMachine.Interact.PowerOn``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.InstantClonePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.InstantClonePlacementSpec.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Network`` referenced by the attribute
              :attr:`com.vmware.vcenter.vm.hardware_client.Ethernet.BackingSpec.network`
              requires ``Network.Assign``.
        """
        return self._invoke('instant_clone',
                            {
                            'spec': spec,
                            })

    def get(self,
            vm,
            ):
        """
        Returns information about a virtual machine.

        :type  vm: :class:`str`
        :param vm: Virtual machine identifier.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :rtype: :class:`VM.Info`
        :return: Information about the specified virtual machine.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the virtual machine's configuration state cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``System.Read``.
        """
        return self._invoke('get',
                            {
                            'vm': vm,
                            })

    def delete(self,
               vm,
               ):
        """
        Deletes a virtual machine.

        :type  vm: :class:`str`
        :param vm: Virtual machine identifier.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is running (powered on).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the virtual machine is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the virtual machine's configuration state cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.Inventory.Delete``.
        """
        return self._invoke('delete',
                            {
                            'vm': vm,
                            })

    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 4000 visible (subject to permission
        checks) virtual machines in vCenter matching the
        :class:`VM.FilterSpec`.

        :type  filter: :class:`VM.FilterSpec` or ``None``
        :param filter: Specification of matching virtual machines for which information
            should be returned.
            If None, the behavior is equivalent to a :class:`VM.FilterSpec`
            with all attributes None which means all virtual machines match the
            filter.
        :rtype: :class:`list` of :class:`VM.Summary`
        :return: Commonly used information about the virtual machines matching the
            :class:`VM.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the :attr:`VM.FilterSpec.power_states` attribute contains a
            value that is not supported by the server.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if more than 4000 virtual machines match the
            :class:`VM.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def register(self,
                 spec,
                 ):
        """
        Creates a virtual machine from existing virtual machine files on
        storage.
        This method was added in **vSphere API 6.8.7**.

        :type  spec: :class:`VM.RegisterSpec`
        :param spec: Specification of the location of the virtual machine files and the
            placement of the new virtual machine.
        :rtype: :class:`str`
        :return: Identifier of the newly-created virtual machine.
            The return value will be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            if a virtual machine with the specified name already exists or if a
            virtual machine using the specified virtual machine files already
            exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if any of the resources specified in spec could not be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a specified resource (eg. host) is not accessible.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnableToAllocateResource` 
            if any of the resources needed to register the virtual machine
            could not be allocated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``Datastore`` referenced by the attribute
              :attr:`VM.RegisterSpec.datastore` requires ``System.Read``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`VM.InventoryPlacementSpec.folder` requires
              ``VirtualMachine.Inventory.Register``.
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`VM.ComputePlacementSpec.resource_pool` requires
              ``Resource.AssignVMToPool``.
        """
        return self._invoke('register',
                            {
                            'spec': spec,
                            })

    def unregister(self,
                   vm,
                   ):
        """
        Removes the virtual machine corresponding to ``vm`` from the vCenter
        inventory without removing any of the virtual machine's files from
        storage. All high-level information stored with the management server
        (ESXi or vCenter) is removed, including information such as statistics,
        resource pool association, permissions, and alarms.
        This method was added in **vSphere API 6.8.7**.

        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine to be unregistered.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the virtual machine is running (powered on).
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no virtual machine associated with ``vm`` in the
            system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceBusy` 
            if the virtual machine is busy performing another operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``VirtualMachine`` referenced by the parameter
              ``vm`` requires ``VirtualMachine.Inventory.Unregister``.
        """
        return self._invoke('unregister',
                            {
                            'vm': vm,
                            })
class Deployment(VapiInterface):
    """
    The ``Deployment`` class provides methods to get the status of the vCenter
    appliance deployment.
    This class was added in **vSphere API 6.7**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.deployment'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _DeploymentStub)
        self._VAPI_OPERATION_IDS = {}

    class Task(VapiStruct):
        """
        The ``Deployment.Task`` class contains attributes to describe a particular
        deployment task.
        This class was added in **vSphere API 6.7**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'RUNNING' : [('progress', True), ('result', False), ('start_time', True)],
                    'BLOCKED' : [('progress', True), ('result', False), ('start_time', True)],
                    'SUCCEEDED' : [('progress', True), ('result', False), ('start_time', True), ('end_time', True)],
                    'FAILED' : [('progress', True), ('result', False), ('error', False), ('start_time', True), ('end_time', True)],
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     progress=None,
                     result=None,
                     description=None,
                     service=None,
                     operation=None,
                     parent=None,
                     target=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                     user=None,
                    ):
            """
            :type  progress: :class:`com.vmware.cis.task_client.Progress`
            :param progress: The progress info of this deployment task.
                This attribute was added in **vSphere API 6.7**.
                This attribute is optional and it is only relevant when the value
                of ``CommonInfo#status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  result: :class:`com.vmware.vcenter.deployment_client.Notifications` or ``None``
            :param result: Result of the task.
                This attribute was added in **vSphere API 6.7**.
                This attribute will be None if result is not available at the
                current step of the task.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
            :type  service: :class:`str`
            :param service: Identifier of the service containing the operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.service``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.service``.
            :type  operation: :class:`str`
            :param operation: Identifier of the operation associated with the task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.operation``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.operation``.
            :type  parent: :class:`str` or ``None``
            :param parent: Parent of the current task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.task``. When methods return a value of this class
                as a return value, the attribute will be an identifier for the
                resource type: ``com.vmware.cis.task``.
                This attribute will be None if the task has no parent.
            :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param target: Identifier of the target created by the operation or an existing
                one the operation performed on.
                This attribute will be None if the operation has no target or
                multiple targets.
            :type  status: :class:`com.vmware.cis.task_client.Status`
            :param status: Status of the operation associated with the task.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED".
                If None the description of why the operation failed will be
                included in the result of the operation (see
                :attr:`com.vmware.cis.task_client.Info.result`).
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  user: :class:`str` or ``None``
            :param user: Name of the user who performed the operation.
                This attribute will be None if the operation is performed by the
                system.
            """
            self.progress = progress
            self.result = result
            self.description = description
            self.service = service
            self.operation = operation
            self.parent = parent
            self.target = target
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            self.user = user
            VapiStruct.__init__(self)


    Task._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.task', {
            'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
            'result': type.OptionalType(type.ReferenceType('com.vmware.vcenter.deployment_client', 'Notifications')),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'service': type.IdType(resource_types='com.vmware.vapi.service'),
            'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
            'parent': type.OptionalType(type.IdType()),
            'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
            'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'user': type.OptionalType(type.StringType()),
        },
        Task,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Deployment.Info`` class contains attributes to describe the state of
        the appliance.
        This class was added in **vSphere API 6.7**.

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
                    'PENDING' : [],
                }
            ),
        ]



        def __init__(self,
                     state=None,
                     progress=None,
                     subtask_order=None,
                     subtasks=None,
                     description=None,
                     service=None,
                     operation=None,
                     parent=None,
                     target=None,
                     status=None,
                     cancelable=None,
                     error=None,
                     start_time=None,
                     end_time=None,
                     user=None,
                    ):
            """
            :type  state: :class:`com.vmware.vcenter.deployment_client.ApplianceState`
            :param state: State of the vCenter Server Appliance.
                This attribute was added in **vSphere API 6.7**.
            :type  progress: :class:`com.vmware.cis.task_client.Progress`
            :param progress: The progress info of the current appliance status.
                This attribute was added in **vSphere API 6.7**.
                This attribute is optional and it is only relevant when the value
                of ``CommonInfo#status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  subtask_order: :class:`list` of :class:`str` or ``None``
            :param subtask_order: The ordered list of subtasks for this deployment operation.
                This attribute was added in **vSphere API 6.7**.
                Only :class:`set` when the appliance state is RUNNING_IN_PROGRESS,
                FAILED, CANCELLED and SUCCEEDED.
            :type  subtasks: (:class:`dict` of :class:`str` and :class:`Deployment.Task`) or ``None``
            :param subtasks: The map of the deployment subtasks and their status infomation.
                This attribute was added in **vSphere API 6.7**.
                Only :class:`set` when the appliance state is RUNNING_IN_PROGRESS,
                FAILED, CANCELLED and SUCCEEDED.
            :type  description: :class:`com.vmware.vapi.std_client.LocalizableMessage`
            :param description: Description of the operation associated with the task.
            :type  service: :class:`str`
            :param service: Identifier of the service containing the operation.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.service``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.service``.
            :type  operation: :class:`str`
            :param operation: Identifier of the operation associated with the task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vapi.operation``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.vapi.operation``.
            :type  parent: :class:`str` or ``None``
            :param parent: Parent of the current task.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.task``. When methods return a value of this class
                as a return value, the attribute will be an identifier for the
                resource type: ``com.vmware.cis.task``.
                This attribute will be None if the task has no parent.
            :type  target: :class:`com.vmware.vapi.std_client.DynamicID` or ``None``
            :param target: Identifier of the target created by the operation or an existing
                one the operation performed on.
                This attribute will be None if the operation has no target or
                multiple targets.
            :type  status: :class:`com.vmware.cis.task_client.Status`
            :param status: Status of the operation associated with the task.
            :type  cancelable: :class:`bool`
            :param cancelable: Flag to indicate whether or not the operation can be cancelled. The
                value may change as the operation progresses.
            :type  error: :class:`Exception` or ``None``
            :param error: Description of the error if the operation status is "FAILED".
                If None the description of why the operation failed will be
                included in the result of the operation (see
                :attr:`com.vmware.cis.task_client.Info.result`).
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Time when the operation is started.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.RUNNING`,
                :attr:`com.vmware.cis.task_client.Status.BLOCKED`,
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED`, or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: Time when the operation is completed.
                This attribute is optional and it is only relevant when the value
                of ``status`` is one of
                :attr:`com.vmware.cis.task_client.Status.SUCCEEDED` or
                :attr:`com.vmware.cis.task_client.Status.FAILED`.
            :type  user: :class:`str` or ``None``
            :param user: Name of the user who performed the operation.
                This attribute will be None if the operation is performed by the
                system.
            """
            self.state = state
            self.progress = progress
            self.subtask_order = subtask_order
            self.subtasks = subtasks
            self.description = description
            self.service = service
            self.operation = operation
            self.parent = parent
            self.target = target
            self.status = status
            self.cancelable = cancelable
            self.error = error
            self.start_time = start_time
            self.end_time = end_time
            self.user = user
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.deployment.info', {
            'state': type.ReferenceType('com.vmware.vcenter.deployment_client', 'ApplianceState'),
            'progress': type.OptionalType(type.ReferenceType('com.vmware.cis.task_client', 'Progress')),
            'subtask_order': type.OptionalType(type.ListType(type.StringType())),
            'subtasks': type.OptionalType(type.MapType(type.StringType(), type.ReferenceType(__name__, 'Deployment.Task'))),
            'description': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
            'service': type.IdType(resource_types='com.vmware.vapi.service'),
            'operation': type.IdType(resource_types='com.vmware.vapi.operation'),
            'parent': type.OptionalType(type.IdType()),
            'target': type.OptionalType(type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID')),
            'status': type.ReferenceType('com.vmware.cis.task_client', 'Status'),
            'cancelable': type.BooleanType(),
            'error': type.OptionalType(type.AnyErrorType()),
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'user': type.OptionalType(type.StringType()),
        },
        Info,
        False,
        None))



    def get(self):
        """
        Get the current status of the appliance deployment.
        This method was added in **vSphere API 6.7**.


        :rtype: :class:`Deployment.Info`
        :return: Info structure containing the status information about the
            appliance.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if appliance state cannot be determined.
        """
        return self._invoke('get', None)

    def rollback(self):
        """
        Rollback a failed appliance so it can be configured once again.
        This method was added in **vSphere API 6.7**.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the appliance is not in FAILED state.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        """
        return self._invoke('rollback', None)
class Ovfs(VapiInterface):
    """
    The Ovfs class provides methods for deploying Virtual Machines or Virtual
    Appliances.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.ovfs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _OvfsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'deploy_task': 'deploy$task'})

    class DiskProvisioningType(Enum):
        """
        The ``Ovfs.DiskProvisioningType`` class specifies types of disk
        provisioning that can be set for the disk in the deployed OVF package.
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
        MONOLITHIC_SPARSE = None
        """
        A sparse (allocate on demand) monolithic disk. Disks in this format can be
        used with other VMware products.

        """
        MONOLITHIC_FLAT = None
        """
        A preallocated monolithic disk. Disks in this format can be used with other
        VMware products.

        """
        TWO_GB_MAXEXTENT_SPARSE = None
        """
        A sparse (allocate on demand) disk with 2GB maximum extent size. Disks in
        this format can be used with other VMware products. The 2GB extent size
        makes these disks easier to burn to DVD or use on filesystems that don't
        support large files.

        """
        TWO_GB_MAXEXTENT_FLAT = None
        """
        A preallocated disk with 2GB maximum extent size. Disks in this format can
        be used with other VMware products. The 2GB extent size makes these disks
        easier to burn to DVD or use on filesystems that don't support large files.

        """
        THIN = None
        """
        Space required for thin-provisioned virtual disk is allocated and zeroed on
        demand as the space is used.

        """
        THICK = None
        """
        A thick disk has all space allocated at creation time and the space is
        zeroed on demand as the space is used.

        """
        SE_SPARSE = None
        """
        A sparse (allocate on demand) format with additional space optimizations.

        """
        EAGER_ZEROED_THICK = None
        """
        An eager zeroed thick disk has all space allocated and wiped clean of any
        previous contents on the physical media at creation time. Such disks may
        take a longer time during creation compared to other disk formats.

        """
        SPARSE = None
        """
        Depending on the supported Disk types on the target host, Sparse is mapped
        to either MonolithicSparse or Thin.

        """
        FLAT = None
        """
        Depending on the supported Disk types on the target host, Flat is mapped to
        either MonolithicFlat or Thick.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`DiskProvisioningType` instance.
            """
            Enum.__init__(string)

    DiskProvisioningType._set_values({
        'MONOLITHIC_SPARSE': DiskProvisioningType('MONOLITHIC_SPARSE'),
        'MONOLITHIC_FLAT': DiskProvisioningType('MONOLITHIC_FLAT'),
        'TWO_GB_MAXEXTENT_SPARSE': DiskProvisioningType('TWO_GB_MAXEXTENT_SPARSE'),
        'TWO_GB_MAXEXTENT_FLAT': DiskProvisioningType('TWO_GB_MAXEXTENT_FLAT'),
        'THIN': DiskProvisioningType('THIN'),
        'THICK': DiskProvisioningType('THICK'),
        'SE_SPARSE': DiskProvisioningType('SE_SPARSE'),
        'EAGER_ZEROED_THICK': DiskProvisioningType('EAGER_ZEROED_THICK'),
        'SPARSE': DiskProvisioningType('SPARSE'),
        'FLAT': DiskProvisioningType('FLAT'),
    })
    DiskProvisioningType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.ovfs.disk_provisioning_type',
        DiskProvisioningType))


    class NetworkInfo(VapiStruct):
        """
        The ``Ovfs.NetworkInfo`` class defines network information for specifying
        network mappings from the OVF descriptor to a Network in the inventory.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """
        NETWORK_TYPES = ["DistributedVirtualPortgroup", "Network", "OpaqueNetwork"]
        """
        The expected network types allowed.

        """




        def __init__(self,
                     net_type=None,
                     network=None,
                    ):
            """
            :type  net_type: :class:`str`
            :param net_type: Type for the network.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be one of ``DistributedVirtualPortgroup``,
                ``Network``, or ``OpaqueNetwork``. When methods return a value of
                this class as a return value, the attribute will be one of
                ``DistributedVirtualPortgroup``, ``Network``, or ``OpaqueNetwork``.
            :type  network: :class:`str`
            :param network: The identifier of the network in the inventory that is the target
                of the OVF network.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for one of these resource types:
                ``DistributedVirtualPortgroup``, ``Network``, or ``OpaqueNetwork``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for one of these resource types:
                ``DistributedVirtualPortgroup``, ``Network``, or ``OpaqueNetwork``.
            """
            self.net_type = net_type
            self.network = network
            VapiStruct.__init__(self)


    NetworkInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.ovfs.network_info', {
            'net_type': type.StringType(),
            'network': type.IdType(resource_types=["DistributedVirtualPortgroup", "Network", "OpaqueNetwork"], resource_type_field_name="net_type"),
        },
        NetworkInfo,
        False,
        None))


    class DatastoreInfo(VapiStruct):
        """
        The ``Ovfs.DatastoreInfo`` class defines the datastore information used for
        mapping of datastores in the inventory.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     datastore=None,
                    ):
            """
            :type  datastore: :class:`str`
            :param datastore: The identifier of the datastore in the inventory that is the target
                of the OVF datastore mapping.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``Datastore``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``Datastore``.
            """
            self.datastore = datastore
            VapiStruct.__init__(self)


    DatastoreInfo._set_binding_type(type.StructType(
        'com.vmware.vcenter.ovfs.datastore_info', {
            'datastore': type.IdType(resource_types='Datastore'),
        },
        DatastoreInfo,
        False,
        None))


    class DeploySpec(VapiStruct):
        """
        The ``Ovfs.DeploySpec`` class contains parameters supplied at the time the
        OVF deploys onto a specific host. Users must supply some required
        parameters, and may override other default parameters. Customization
        parameters are also provided for Guest OS customization.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     url=None,
                     resource_pool=None,
                     folder=None,
                     name=None,
                     host_system=None,
                     network_mapping=None,
                     vm_home_datastore=None,
                     disk_provisioning=None,
                     pull_from_esx=None,
                     signature_required=None,
                     skip_manifest_check=None,
                     power_on=None,
                     custom_http_headers=None,
                     custom_properties=None,
                     source_certificate=None,
                     deployment_option=None,
                    ):
            """
            :type  url: :class:`str`
            :param url: The HTTP location of the source OVF files or OVA.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: The resource pool where the VM or vApp will deploy. Currently
                required but in the future versions may become optional.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                if None or empty, the deployment will fail.
            :type  folder: :class:`str` or ``None``
            :param folder: The folder where the VirtualMachine will be placed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                if None or empty, the folder will be set to vmFolder in the
                datacenter where the resource pool is.
            :type  name: :class:`str`
            :param name: The name of the VM or vApp being deployed as specified by an OVF.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  host_system: :class:`str` or ``None``
            :param host_system: The identifier of the host being deployed to.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If None, a suitable host will be picked if possible, meeting
                datastore and network constraints.
            :type  network_mapping: (:class:`dict` of :class:`str` and :class:`Ovfs.NetworkInfo`) or ``None``
            :param network_mapping: The ``networkMapping`` defines user choices for mapping of a
                network as specified by the OVF descriptor to a Network in the
                inventory.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no network mapping is used.
            :type  vm_home_datastore: :class:`Ovfs.DatastoreInfo`
            :param vm_home_datastore: The datastore selection for VM's home directory.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  disk_provisioning: :class:`Ovfs.DiskProvisioningType` or ``None``
            :param disk_provisioning: The optional disk provisioning type used upon deployment. If set
                all the disks in the deployed OVF will have the same specified disk
                type (e.g., thin provisioned).
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the type will be set to thick.
            :type  pull_from_esx: :class:`bool` or ``None``
            :param pull_from_esx: Use Push mode for transferring VM files to ESX. Push mode transfers
                files from source to ESXi, whereas in Pull mode ESX "pulls" the
                files directly from source. The user needs privilege
                VApp.PullFromUrls in vCenter to use Pull mode.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default is set to Pull mode.
            :type  signature_required: :class:`bool` or ``None``
            :param signature_required: Require that the OVF package includes both a certificate (.cert)
                file and a manifest (.mf) file. The certificate file contains a
                vendor-supplied public key and the signature of the manifest file
                as signed with the vendor-supplied private key.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default is set to false.
            :type  skip_manifest_check: :class:`bool` or ``None``
            :param skip_manifest_check: Skip manifest validation. The manifest validation involves
                validating format and content of the manifest file. In Push mode of
                deployment all SHA entries present in the manifest file are
                validated against SHA digest of transferred files. If value is true
                and manifest file is not present a warning is generated.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default is set to false.
            :type  power_on: :class:`bool` or ``None``
            :param power_on: Whether to power on the deployed entity.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the default is set to false.
            :type  custom_http_headers: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
            :param custom_http_headers: Use this optional field to specify any custom headers required by
                the source server, including authenticating headers.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no headers are used to access source.
            :type  custom_properties: (:class:`dict` of :class:`str` and :class:`str`) or ``None``
            :param custom_properties: These parameters will apply to OVF Properties to customize the
                guest OS after it is deployed. These parameters specify values for
                corresponding ovf:Property flags. Example: if ovf:Property has
                ovf:key="ip" and desrired value is "1.2.3.4" then an entry would be
                added which would map "ip" to "1.2.3.4".
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no customization is done.
            :type  source_certificate: :class:`str` or ``None``
            :param source_certificate: Optionally used for HTTPS source validation. The source is the
                location where the OVF/OVA files are located. The source server
                certificate in PEM format.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, no certificate is used.
            :type  deployment_option: :class:`str` or ``None``
            :param deployment_option: The key of the chosen deployment option. If empty, the default
                option is chosen. The list of available deployment options can
                optionally be specified in the OVF file being deployed and this key
                specifies which one to use for deployment from that list.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.url = url
            self.resource_pool = resource_pool
            self.folder = folder
            self.name = name
            self.host_system = host_system
            self.network_mapping = network_mapping
            self.vm_home_datastore = vm_home_datastore
            self.disk_provisioning = disk_provisioning
            self.pull_from_esx = pull_from_esx
            self.signature_required = signature_required
            self.skip_manifest_check = skip_manifest_check
            self.power_on = power_on
            self.custom_http_headers = custom_http_headers
            self.custom_properties = custom_properties
            self.source_certificate = source_certificate
            self.deployment_option = deployment_option
            VapiStruct.__init__(self)


    DeploySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.ovfs.deploy_spec', {
            'url': type.URIType(),
            'resource_pool': type.OptionalType(type.IdType()),
            'folder': type.OptionalType(type.IdType()),
            'name': type.StringType(),
            'host_system': type.OptionalType(type.IdType()),
            'network_mapping': type.OptionalType(type.MapType(type.StringType(), type.ReferenceType(__name__, 'Ovfs.NetworkInfo'))),
            'vm_home_datastore': type.ReferenceType(__name__, 'Ovfs.DatastoreInfo'),
            'disk_provisioning': type.OptionalType(type.ReferenceType(__name__, 'Ovfs.DiskProvisioningType')),
            'pull_from_esx': type.OptionalType(type.BooleanType()),
            'signature_required': type.OptionalType(type.BooleanType()),
            'skip_manifest_check': type.OptionalType(type.BooleanType()),
            'power_on': type.OptionalType(type.BooleanType()),
            'custom_http_headers': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
            'custom_properties': type.OptionalType(type.MapType(type.StringType(), type.StringType())),
            'source_certificate': type.OptionalType(type.StringType()),
            'deployment_option': type.OptionalType(type.StringType()),
        },
        DeploySpec,
        False,
        None))


    class DeployResult(VapiStruct):
        """
        The ``Ovfs.DeployResult`` class defines the result of a successful API call
        which will include the ID of the entity created.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """
        RESULT_TYPES = ["VirtualApp", "VirtualMachine"]
        """
        The expected result types allowed.

        """




        def __init__(self,
                     result_type=None,
                     created_entity=None,
                    ):
            """
            :type  result_type: :class:`str`
            :param result_type: Type for the result.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be one of ``VirtualApp`` or ``VirtualMachine``. When
                methods return a value of this class as a return value, the
                attribute will be one of ``VirtualApp`` or ``VirtualMachine``.
            :type  created_entity: :class:`str`
            :param created_entity: Identifier of the deployed Virtual Machine or Virtual Appliance if
                deployment succeeded. In case of a deployment failure an exception
                is thrown instead of returning DeployResult.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for one of these resource types:
                ``VirtualApp`` or ``VirtualMachine``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for one of these resource types: ``VirtualApp`` or
                ``VirtualMachine``.
            """
            self.result_type = result_type
            self.created_entity = created_entity
            VapiStruct.__init__(self)


    DeployResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.ovfs.deploy_result', {
            'result_type': type.StringType(),
            'created_entity': type.IdType(resource_types=["VirtualApp", "VirtualMachine"], resource_type_field_name="result_type"),
        },
        DeployResult,
        False,
        None))




    def deploy_task(self,
               spec,
               ):
        """
        Deploy an OVF on a resource pool. 
        
        Deployment creates a new Virtual Machine(VM) or Virtual
        Appliance(VApp), from an OVF located on a web-server, in the specified
        folder and attached to a resource pool. 
        
        The descriptor OVF is downloaded, parsed and its validity is verified
        against the provided deployment constraints(if any). The files
        referenced in the descriptor are then downloaded and processed. In case
        of OVA, files are extracted and processed. If file-paths in OVF are not
        absolute then they are assumed to be relative to the descriptor URL. 
        
        The import process consists of two parts: 
        
        #. - Create the VMs and/or VApps that make up the entity.
        #. - Upload virtual disk contents.
        
        
        
        In part 1: The server creates all inventory objects. If an error occurs
        while creating inventory objects the import process is aborted, task
        reflects a failure. 
        
        In part 2: The server transfers disk contents using from the URL
        location. 
        
        When the server is done transferring disks, if there are no Guest
        customization or PowerOn specified the task completes, else those
        requested operations are performed. 
        
        If the import process fails or times out, all created inventory objects
        are removed, including all virtual disks. Note: if VC is abruptly
        stopped in the middle of this task cleanup might not be able to happen
        in time. 
        
        This operation only works if the folder's childType includes required
        VM privilege VirtualMachine.Inventory.Create. 
        
        By default Pull mode is leveraged unless user specifies otherwise. On
        vCenter server the privilege VApp.PullFromUrls is required if default
        behaviour is performed.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Ovfs.DeploySpec`
        :param spec: Specification for deployment.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If any of the specified parameters is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the resource pool is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If vCenter Server cannot validate the certificate of the server
            that supplies the OVF file.
            The value of the data attribute of
            :class:`com.vmware.vapi.std.errors_client.Error` will be a class
            that contains all the attributes defined in CertificateInfo.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * The resource ``ResourcePool`` referenced by the attribute
              :attr:`Ovfs.DeploySpec.resource_pool` requires
              ``Resource.AssignVMToPool`` and ``VApp.Import``.
            * The resource ``Datastore`` referenced by the attribute
              :attr:`Ovfs.DatastoreInfo.datastore` requires
              ``Datastore.AllocateSpace``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`Ovfs.DeploySpec.folder` requires
              ``VirtualMachine.Inventory.Create`` and ``VApp.Import``.
        """
        task_id = self._invoke('deploy$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'Ovfs.DeployResult'))
        return task_instance
class _ClusterStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Cluster.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/cluster',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        get_error_dict = {
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
            url_template='/vcenter/cluster/{cluster}',
            path_variables={
                'cluster': 'cluster',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Cluster.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Cluster.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
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
            self, iface_name='com.vmware.vcenter.cluster',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _DatacenterStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Datacenter.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/datacenter',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'datacenter': type.IdType(resource_types='Datacenter'),
            'force': type.OptionalType(type.BooleanType()),
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
            url_template='/vcenter/datacenter/{datacenter}',
            path_variables={
                'datacenter': 'datacenter',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Datacenter.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/datacenter',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'datacenter': type.IdType(resource_types='Datacenter'),
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
            url_template='/vcenter/datacenter/{datacenter}',
            path_variables={
                'datacenter': 'datacenter',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='Datacenter'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Datacenter.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Datacenter.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.datacenter',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _DatastoreStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'datastore': type.IdType(resource_types='Datastore'),
        })
        get_error_dict = {
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
            url_template='/vcenter/datastore/{datastore}',
            path_variables={
                'datastore': 'datastore',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Datastore.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/datastore',
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
                'output_type': type.ReferenceType(__name__, 'Datastore.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Datastore.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.datastore',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _EvcModesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'create_spec': type.ReferenceType(__name__, 'EvcModes.CreateSpec'),
        })
        create_error_dict = {
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
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/evc-modes',
            request_body_parameter='create_spec',
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

        # properties for partition operation
        partition_input_type = type.StructType('operation-input', {
            'evc_mode': type.ReferenceType('com.vmware.vcenter.evc_mode_client', 'EvcMode'),
        })
        partition_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        partition_input_value_validator_list = [
        ]
        partition_output_validator_list = [
        ]
        partition_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/evc-modes?action=partition',
            request_body_parameter='evc_mode',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'partition',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'partition': {
                'input_type': partition_input_type,
                'output_type': type.ReferenceType(__name__, 'EvcModes.PartitionResult'),
                'errors': partition_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': partition_input_value_validator_list,
                'output_validator_list': partition_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'partition': partition_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.evc_modes',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _FolderStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Folder.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/folder',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Folder.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.folder',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _FoundationLoadBalancersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'FoundationLoadBalancers.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/foundation-load-balancers',
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
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
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
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}',
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

        # properties for reset_password operation
        reset_password_input_type = type.StructType('operation-input', {
            'foundation_load_balancer': type.IdType(resource_types='com.vmware.vcenter.FoundationLoadBalancer'),
            'password': type.ReferenceType(__name__, 'FoundationLoadBalancers.PasswordSpec'),
        })
        reset_password_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        reset_password_input_value_validator_list = [
        ]
        reset_password_output_validator_list = [
        ]
        reset_password_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/foundation-load-balancers/{foundationLoadBalancer}?action=reset-password',
            request_body_parameter='password',
            path_variables={
                'foundation_load_balancer': 'foundationLoadBalancer',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'reset-password',
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
                'output_type': type.ReferenceType(__name__, 'FoundationLoadBalancers.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'FoundationLoadBalancers.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'reset_password': {
                'input_type': reset_password_input_type,
                'output_type': type.VoidType(),
                'errors': reset_password_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': reset_password_input_value_validator_list,
                'output_validator_list': reset_password_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'reset_password': reset_password_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.foundation_load_balancers',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _HostStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Host.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.invalid_element_type':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidElementType'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/host',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
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
            url_template='/vcenter/host/{host}',
            path_variables={
                'host': 'host',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Host.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/host',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for connect operation
        connect_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
        })
        connect_error_dict = {
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
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
        connect_input_value_validator_list = [
        ]
        connect_output_validator_list = [
        ]
        connect_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/host/{host}/connect',
            path_variables={
                'host': 'host',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for disconnect operation
        disconnect_input_type = type.StructType('operation-input', {
            'host': type.IdType(resource_types='HostSystem'),
        })
        disconnect_error_dict = {
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
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
        disconnect_input_value_validator_list = [
        ]
        disconnect_output_validator_list = [
        ]
        disconnect_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/host/{host}/disconnect',
            path_variables={
                'host': 'host',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='HostSystem'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidElementType'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'Host.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'connect': {
                'input_type': connect_input_type,
                'output_type': type.VoidType(),
                'errors': connect_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': connect_input_value_validator_list,
                'output_validator_list': connect_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'disconnect': {
                'input_type': disconnect_input_type,
                'output_type': type.VoidType(),
                'errors': disconnect_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': disconnect_input_value_validator_list,
                'output_validator_list': disconnect_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'connect': connect_rest_metadata,
            'disconnect': disconnect_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.host',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _NetworkStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Network.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/network',
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
                'output_type': type.ListType(type.ReferenceType(__name__, 'Network.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.network',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _ResourcePoolStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'resource_pool': type.IdType(resource_types='ResourcePool'),
        })
        get_error_dict = {
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
            url_template='/vcenter/resource-pool/{resource-pool}',
            path_variables={
                'resource_pool': 'resource-pool',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'ResourcePool.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/resource-pool',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'ResourcePool.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/resource-pool',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'resource_pool': type.IdType(resource_types='ResourcePool'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/vcenter/resource-pool/{resource-pool}',
            path_variables={
                'resource_pool': 'resource-pool',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'resource_pool': type.IdType(resource_types='ResourcePool'),
            'spec': type.ReferenceType(__name__, 'ResourcePool.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/resource-pool/{resource-pool}',
            path_variables={
                'resource_pool': 'resource-pool',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        operations = {
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'ResourcePool.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'ResourcePool.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='ResourcePool'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'update': update_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.resource_pool',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SystemStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for hello operation
        hello_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'System.HelloSpec'),
        })
        hello_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),

        }
        hello_input_value_validator_list = [
        ]
        hello_output_validator_list = [
        ]
        hello_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/system?action=hello',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'hello',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'hello': {
                'input_type': hello_input_type,
                'output_type': type.ReferenceType(__name__, 'System.HelloResult'),
                'errors': hello_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).build(),
                'input_value_validator_list': hello_input_value_validator_list,
                'output_validator_list': hello_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'hello': hello_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.system',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VMStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'VM.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.resource_in_use':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for clone operation
        clone_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'VM.CloneSpec'),
        })
        clone_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        clone_input_value_validator_list = [
        ]
        clone_output_validator_list = [
        ]
        clone_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for relocate operation
        relocate_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'VM.RelocateSpec'),
        })
        relocate_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        relocate_input_value_validator_list = [
        ]
        relocate_output_validator_list = [
        ]
        relocate_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
                 },
            query_parameters={
            }
        )

        # properties for instant_clone operation
        instant_clone_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'VM.InstantCloneSpec'),
        })
        instant_clone_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        instant_clone_input_value_validator_list = [
        ]
        instant_clone_output_validator_list = [
        ]
        instant_clone_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
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
            url_template='/vcenter/vm/{vm}',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
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
            url_template='/vcenter/vm/{vm}',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'VM.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
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
            url_template='/vcenter/vm',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for register operation
        register_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'VM.RegisterSpec'),
        })
        register_error_dict = {
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unable_to_allocate_resource':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        register_input_value_validator_list = [
        ]
        register_output_validator_list = [
        ]
        register_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm',
            path_variables={
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        # properties for unregister operation
        unregister_input_type = type.StructType('operation-input', {
            'vm': type.IdType(resource_types='VirtualMachine'),
        })
        unregister_error_dict = {
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_busy':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        unregister_input_value_validator_list = [
        ]
        unregister_output_validator_list = [
        ]
        unregister_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/vm/{vm}',
            path_variables={
                'vm': 'vm',
            },
             header_parameters={
               },
            query_parameters={
            }
        )

        operations = {
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='VirtualMachine'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInUse'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'clone': {
                'input_type': clone_input_type,
                'output_type': type.IdType(resource_types='VirtualMachine'),
                'errors': clone_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': clone_input_value_validator_list,
                'output_validator_list': clone_output_validator_list,
                'task_type': TaskType.TASK,
            },
            'clone$task': {
                'input_type': clone_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': clone_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': clone_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK,
            },
            'relocate': {
                'input_type': relocate_input_type,
                'output_type': type.VoidType(),
                'errors': relocate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': relocate_input_value_validator_list,
                'output_validator_list': relocate_output_validator_list,
                'task_type': TaskType.TASK,
            },
            'relocate$task': {
                'input_type': relocate_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': relocate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': relocate_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK,
            },
            'instant_clone': {
                'input_type': instant_clone_input_type,
                'output_type': type.IdType(resource_types='VirtualMachine'),
                'errors': instant_clone_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': instant_clone_input_value_validator_list,
                'output_validator_list': instant_clone_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'VM.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ListType(type.ReferenceType(__name__, 'VM.Summary')),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'register': {
                'input_type': register_input_type,
                'output_type': type.IdType(resource_types='VirtualMachine'),
                'errors': register_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnableToAllocateResource'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': register_input_value_validator_list,
                'output_validator_list': register_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'unregister': {
                'input_type': unregister_input_type,
                'output_type': type.VoidType(),
                'errors': unregister_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceBusy'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': unregister_input_value_validator_list,
                'output_validator_list': unregister_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'clone': clone_rest_metadata,
            'relocate': relocate_rest_metadata,
            'instant_clone': instant_clone_rest_metadata,
            'get': get_rest_metadata,
            'delete': delete_rest_metadata,
            'list': list_rest_metadata,
            'register': register_rest_metadata,
            'unregister': unregister_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.VM',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _DeploymentStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/deployment',
            path_variables={
            },
             header_parameters={
             },
            query_parameters={
            }
        )

        # properties for rollback operation
        rollback_input_type = type.StructType('operation-input', {})
        rollback_error_dict = {
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        rollback_input_value_validator_list = [
        ]
        rollback_output_validator_list = [
        ]
        rollback_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/deployment?action=rollback',
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
                'output_type': type.ReferenceType(__name__, 'Deployment.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'rollback': {
                'input_type': rollback_input_type,
                'output_type': type.VoidType(),
                'errors': rollback_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': rollback_input_value_validator_list,
                'output_validator_list': rollback_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'rollback': rollback_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.deployment',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _OvfsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for deploy operation
        deploy_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Ovfs.DeploySpec'),
        })
        deploy_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),

        }
        deploy_input_value_validator_list = [
        ]
        deploy_output_validator_list = [
        ]
        deploy_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/ovfs?action=deploy',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'deploy',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'deploy$task': {
                'input_type': deploy_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': deploy_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'), []).build(),
                'input_value_validator_list': deploy_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'deploy': deploy_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.ovfs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Cluster': Cluster,
        'Datacenter': Datacenter,
        'Datastore': Datastore,
        'EvcModes': EvcModes,
        'Folder': Folder,
        'FoundationLoadBalancers': FoundationLoadBalancers,
        'Host': Host,
        'Network': Network,
        'ResourcePool': ResourcePool,
        'System': System,
        'VM': VM,
        'Deployment': Deployment,
        'Ovfs': Ovfs,
        'authorization': 'com.vmware.vcenter.authorization_client.StubFactory',
        'certificate_management': 'com.vmware.vcenter.certificate_management_client.StubFactory',
        'cluster': 'com.vmware.vcenter.cluster_client.StubFactory',
        'consumption_domains': 'com.vmware.vcenter.consumption_domains_client.StubFactory',
        'crypto_manager': 'com.vmware.vcenter.crypto_manager_client.StubFactory',
        'datastore': 'com.vmware.vcenter.datastore_client.StubFactory',
        'deployment': 'com.vmware.vcenter.deployment_client.StubFactory',
        'environment_browser': 'com.vmware.vcenter.environment_browser_client.StubFactory',
        'evc_mode': 'com.vmware.vcenter.evc_mode_client.StubFactory',
        'foundation_load_balancers': 'com.vmware.vcenter.foundation_load_balancers_client.StubFactory',
        'guest': 'com.vmware.vcenter.guest_client.StubFactory',
        'host': 'com.vmware.vcenter.host_client.StubFactory',
        'identity': 'com.vmware.vcenter.identity_client.StubFactory',
        'network': 'com.vmware.vcenter.network_client.StubFactory',
        'services': 'com.vmware.vcenter.services_client.StubFactory',
        'storage': 'com.vmware.vcenter.storage_client.StubFactory',
        'system_config': 'com.vmware.vcenter.system_config_client.StubFactory',
        'tagging': 'com.vmware.vcenter.tagging_client.StubFactory',
        'topology': 'com.vmware.vcenter.topology_client.StubFactory',
        'trusted_infrastructure': 'com.vmware.vcenter.trusted_infrastructure_client.StubFactory',
        'vcha': 'com.vmware.vcenter.vcha_client.StubFactory',
        'vm': 'com.vmware.vcenter.vm_client.StubFactory',
    }

