# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.inventory.reports.transition_summary.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.inventory.reports.transition_summary_client``
module provides methods to be executed on entities belonging to vCenter
inventory.

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


class Clusters(VapiInterface):
    """
    The ``Clusters`` class provides operations to fetch the installed image
    report and transition status for given clusters. The transition operation
    refers to transitioning a baseline managed entity to image managed entity.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.inventory.reports.transition_summary.clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClustersStub)
        self._VAPI_OPERATION_IDS = {}

    class TransitionStatus(Enum):
        """
        The ``Clusters.TransitionStatus`` class defines the different type of
        statuses a given cluster can be during the transition or pre-transition.
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
        NOT_DETECTED = None
        """
        Transition workflow first needs the
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method to
        be executed. This status defines that the
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method is
        not executed or the result is not available for a given cluster.

        """
        DETECTING_IMAGE = None
        """
        Defines that
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method is
        in-progress for a given cluster.

        """
        ELIGIBLE = None
        """
        Defines that a given cluster is ready for transition from baseline managed
        to image managed. This also states that the given cluster is also eligible
        to be transitioned through the
        com.vmware.esx.settings.inventory.Inventory#transition workflow. One of the
        criteria is that the given entity has single installed-image.

        """
        CLUSTER_LEVEL_CONVERSION_REQUIRED = None
        """
        Defines that the cluster is not ready for transition from baseline managed
        to image managed using
        com.vmware.esx.settings.inventory.Inventory#transition method. One of the
        possible reasons could be that the given cluster might have multiple
        installed images. In such case, the given cluster cannot be transitioned
        using this workflow but can be done using existing cluster workflow.

        """
        CONVERTING = None
        """
        Defines that for a given cluster is getting converted from baseline managed
        to image managed using
        com.vmware.esx.settings.inventory.Inventory#transition method.

        """
        CONVERTED = None
        """
        Defines the a given cluster is successfully converted from baseline managed
        to image managed.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TransitionStatus` instance.
            """
            Enum.__init__(string)

    TransitionStatus._set_values({
        'NOT_DETECTED': TransitionStatus('NOT_DETECTED'),
        'DETECTING_IMAGE': TransitionStatus('DETECTING_IMAGE'),
        'ELIGIBLE': TransitionStatus('ELIGIBLE'),
        'CLUSTER_LEVEL_CONVERSION_REQUIRED': TransitionStatus('CLUSTER_LEVEL_CONVERSION_REQUIRED'),
        'CONVERTING': TransitionStatus('CONVERTING'),
        'CONVERTED': TransitionStatus('CONVERTED'),
    })
    TransitionStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.transition_status',
        TransitionStatus))


    class GetParams(VapiStruct):
        """
        The ``Clusters.GetParams`` class contains attributes that are necessary to
        generate the summary report for the given entities.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'CLUSTER' : [('clusters', True)],
                    'FOLDER' : [('folders', True)],
                    'DATACENTER' : [('datacenters', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     clusters=None,
                     folders=None,
                     datacenters=None,
                    ):
            """
            :type  type: :class:`Clusters.GetParams.InventoryType`
            :param type: The attribute specifies what type of entity within the vCenter's
                inventory on which the operation will be executed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  clusters: :class:`set` of :class:`str`
            :param clusters: List of clusters on which the specified operation needs to be
                executed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Clusters.GetParams.InventoryType.CLUSTER`.
            :type  folders: :class:`set` of :class:`str`
            :param folders: List of folders on which the specified operation will be executed.
                Internally each folder entity will be expanded to individual
                baseline managed clusters which are underneath the designated
                folder. If the list contains the managed object ID of the root
                folder, the specified operation will be executed on all baseline
                managed clusters.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Clusters.GetParams.InventoryType.FOLDER`.
            :type  datacenters: :class:`set` of :class:`str`
            :param datacenters: List of the data-centers on which the specified operation will be
                executed. Internally each data-center entity will be expanded to
                individual baseline managed clusters which are underneath the
                designated data-center.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Clusters.GetParams.InventoryType.DATACENTER`.
            """
            self.type = type
            self.clusters = clusters
            self.folders = folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


        class InventoryType(Enum):
            """
            The ``Clusters.GetParams.InventoryType`` class contains the possible type
            of entities belonging to vCenter's inventory on which the operation can be
            executed.
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
            CLUSTER = None
            """
            Type specifying cluster within the vCenter's inventory.

            """
            FOLDER = None
            """
            Type specifying folder within the vCenter's inventory. Currently this
            entity type is unsupported. Support for the same will be added in future
            releases and hence provision is being made in API/interfaces.

            """
            DATACENTER = None
            """
            Type specifying data-center within the vCenter's inventory. Currently this
            entity type is unsupported. Support for the same will be added in future
            releases and hence provision is being made in API/interfaces.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`InventoryType` instance.
                """
                Enum.__init__(string)

        InventoryType._set_values({
            'CLUSTER': InventoryType('CLUSTER'),
            'FOLDER': InventoryType('FOLDER'),
            'DATACENTER': InventoryType('DATACENTER'),
        })
        InventoryType._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.get_params.inventory_type',
            InventoryType))

    GetParams._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.get_params', {
            'type': type.ReferenceType(__name__, 'Clusters.GetParams.InventoryType'),
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        GetParams,
        False,
        None))


    class ClusterSummary(VapiStruct):
        """
        The ``Clusters.ClusterSummary`` class contains attributes that describes
        the cluster and what software it is currently running. It fetches the
        software details from all the hosts within the cluster. Along with the
        software details, it also provides the status of a given cluster with
        respect to its transition from baseline managed to image managed.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     last_check_time=None,
                     uniform_image=None,
                     images=None,
                     orphan_vibs=None,
                     status=None,
                     notifications=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifier of the cluster
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  last_check_time: :class:`datetime.datetime`
            :param last_check_time: Defines the timestamp when the last
                com.vmware.esx.settings.inventory.Inventory#extractInstalledImage
                method was executed on a given entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  uniform_image: :class:`bool`
            :param uniform_image: Defines if the given entity is having a single image or not.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  images: :class:`list` of :class:`com.vmware.esx.settings_client.SoftwareInfo`
            :param images: Defines the list of unique images found on a given cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  orphan_vibs: :class:`bool`
            :param orphan_vibs: Defines if any orphan VIBs are found on an entity. If found the
                user is expected to check the detailed installed-image report of a
                given entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Clusters.TransitionStatus`
            :param status: ``Clusters.TransitionStatus`` of a given entity as described in
                #TransitionStatus.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Describes if any notifications were raised for the given entity
                during the execution of the method.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cluster = cluster
            self.last_check_time = last_check_time
            self.uniform_image = uniform_image
            self.images = images
            self.orphan_vibs = orphan_vibs
            self.status = status
            self.notifications = notifications
            VapiStruct.__init__(self)


    ClusterSummary._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.cluster_summary', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'last_check_time': type.DateTimeType(),
            'uniform_image': type.BooleanType(),
            'images': type.ListType(type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareInfo')),
            'orphan_vibs': type.BooleanType(),
            'status': type.ReferenceType(__name__, 'Clusters.TransitionStatus'),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ClusterSummary,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Clusters.IterationSpec`` class contains attributes used to break
        results into pages while returning transition summary of the entities
        defined in the 
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
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.iteration_spec', {
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Clusters.FilterSpec`` class contains attributes used to filter the
        results while returning the transition summary based on properties
        contained in it.
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


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.filter_spec', {
        },
        FilterSpec,
        False,
        None))


    class SortCriteria(VapiStruct):
        """
        The ``Clusters.SortCriteria`` class contains attributes that determine how
        a transition summary should be sorted by the values of one or more
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
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.sort_criteria', {
        },
        SortCriteria,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Clusters.Info`` class contains the summary of clusters and the image
        they are running.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster_summaries=None,
                    ):
            """
            :type  cluster_summaries: :class:`list` of :class:`Clusters.ClusterSummary`
            :param cluster_summaries: List of cluster summaries. Each individual cluster summary contains
                its image and transition details.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cluster_summaries = cluster_summaries
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.clusters.info', {
            'cluster_summaries': type.ListType(type.ReferenceType(__name__, 'Clusters.ClusterSummary')),
        },
        Info,
        False,
        None))



    def get(self,
            spec,
            filter=None,
            iterate=None,
            sort=None,
            ):
        """
        Returns the image and transition summary of the clusters defined in the
        as an input.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Clusters.GetParams`
        :param spec: Describe the inventory objects on which the specified operation
            will be performed.
        :type  filter: :class:`Clusters.FilterSpec` or ``None``
        :param filter: The filter applied to the transition summary.
            If None, the behavior is equivalent to fetching all the relevant
            records without having any filter criteria.
        :type  iterate: :class:`Clusters.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the behavior is to retrieve all the records
        :type  sort: :class:`Clusters.SortCriteria` or ``None``
        :param sort: The sort criteria applied to the transition summary.
            If None, the results are not sorted.
        :rtype: :class:`Clusters.Info`
        :return: Summary containing image details and transition status of the
            entities passed in input
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will contain more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If invalid  is passed as an input
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If some of the provided inventories doesn't exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to invoke the interface.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``ClusterComputeResource`` referenced by the
              attribute :attr:`Clusters.GetParams.clusters` requires
              ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`Clusters.GetParams.folders` requires
              ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``Datacenter`` referenced by the attribute
              :attr:`Clusters.GetParams.datacenters` requires
              ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get',
                            {
                            'spec': spec,
                            'filter': filter,
                            'iterate': iterate,
                            'sort': sort,
                            })
class Hosts(VapiInterface):
    """
    The ``Hosts`` class provides operations to fetch the installed image report
    and transition status for standalone hosts. The transition operation refers
    to transitioning a baseline managed entity to image managed entity.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.inventory.reports.transition_summary.hosts'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _HostsStub)
        self._VAPI_OPERATION_IDS = {}

    class TransitionStatus(Enum):
        """
        The ``Hosts.TransitionStatus`` class defines the different type of statuses
        a given standalone host can be during the transition or pre-transition.
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
        NOT_DETECTED = None
        """
        Transition workflow first needs the
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method to
        be executed. This status defines that the
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method is
        not executed or the result is not available for a given host.

        """
        DETECTING_IMAGE = None
        """
        Defines that
        com.vmware.esx.settings.inventory.Inventory#extractInstalledImage method is
        in-progress for a given host.

        """
        ELIGIBLE = None
        """
        Defines that a given host is ready for transition from baseline managed to
        image managed. This also states that the given host is also eligible to be
        transitioned through the
        com.vmware.esx.settings.inventory.Inventory#transition workflow.

        """
        HOST_LEVEL_CONVERSION_REQUIRED = None
        """
        Defines that the host is not ready for transition from baseline managed to
        image managed using com.vmware.esx.settings.inventory.Inventory#transition
        method. In such case, the given standalone host cannot be transitioned
        using this workflow but can be done using existing standalone host
        workflow.

        """
        CONVERTING = None
        """
        Defines that for a given standalone host is getting converted from baseline
        managed to image managed using
        com.vmware.esx.settings.inventory.Inventory#transition method.

        """
        CONVERTED = None
        """
        Defines the a given standalone host is successfully converted from baseline
        managed to image managed.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TransitionStatus` instance.
            """
            Enum.__init__(string)

    TransitionStatus._set_values({
        'NOT_DETECTED': TransitionStatus('NOT_DETECTED'),
        'DETECTING_IMAGE': TransitionStatus('DETECTING_IMAGE'),
        'ELIGIBLE': TransitionStatus('ELIGIBLE'),
        'HOST_LEVEL_CONVERSION_REQUIRED': TransitionStatus('HOST_LEVEL_CONVERSION_REQUIRED'),
        'CONVERTING': TransitionStatus('CONVERTING'),
        'CONVERTED': TransitionStatus('CONVERTED'),
    })
    TransitionStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.transition_status',
        TransitionStatus))


    class GetParams(VapiStruct):
        """
        The ``Hosts.GetParams`` class contains attributes that are necessary to
        generate the summary report for the given entities.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'type',
                {
                    'HOST' : [('hosts', True)],
                    'FOLDER' : [('folders', True)],
                    'DATACENTER' : [('datacenters', True)],
                }
            ),
        ]



        def __init__(self,
                     type=None,
                     hosts=None,
                     folders=None,
                     datacenters=None,
                    ):
            """
            :type  type: :class:`Hosts.GetParams.InventoryType`
            :param type: The attribute specifies what type of entity within the vCenter's
                inventory on which the operation will be executed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  hosts: :class:`set` of :class:`str`
            :param hosts: List of standalone hosts on which the specified operation needs to
                be executed.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Hosts.GetParams.InventoryType.HOST`.
            :type  folders: :class:`set` of :class:`str`
            :param folders: List of folders on which the specified operation will be executed.
                Internally each folder entity will be expanded to individual
                baseline managed standalone hosts which are underneath the
                designated folder. If the list contains the managed object ID of
                the root folder, the specified operation will be executed on all
                baseline managed standalone hosts.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Hosts.GetParams.InventoryType.FOLDER`.
            :type  datacenters: :class:`set` of :class:`str`
            :param datacenters: List of the data-centers on which the specified operation will be
                executed. Internally each data-center entity will be expanded to
                individual baseline managed standalone hosts which are underneath
                the designated data-center.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Datacenter``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``Datacenter``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Hosts.GetParams.InventoryType.DATACENTER`.
            """
            self.type = type
            self.hosts = hosts
            self.folders = folders
            self.datacenters = datacenters
            VapiStruct.__init__(self)


        class InventoryType(Enum):
            """
            The ``Hosts.GetParams.InventoryType`` class contains the possible type of
            entities belonging to vCenter's inventory on which the operation can be
            executed.
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
            HOST = None
            """
            Type specifying standalone host within the vCenter's inventory.

            """
            FOLDER = None
            """
            Type specifying folder within the vCenter's inventory. Currently this
            entity type is unsupported. Support for the same will be added in future
            releases and hence provision is being made in API/interfaces.

            """
            DATACENTER = None
            """
            Type specifying data-center within the vCenter's inventory. Currently this
            entity type is unsupported. Support for the same will be added in future
            releases and hence provision is being made in API/interfaces.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`InventoryType` instance.
                """
                Enum.__init__(string)

        InventoryType._set_values({
            'HOST': InventoryType('HOST'),
            'FOLDER': InventoryType('FOLDER'),
            'DATACENTER': InventoryType('DATACENTER'),
        })
        InventoryType._set_binding_type(type.EnumType(
            'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.get_params.inventory_type',
            InventoryType))

    GetParams._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.get_params', {
            'type': type.ReferenceType(__name__, 'Hosts.GetParams.InventoryType'),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        GetParams,
        False,
        None))


    class HostSummary(VapiStruct):
        """
        The ``Hosts.HostSummary`` class contains attributes that describes the
        software that is currently running on a given standalone host. Along with
        the software details, it also provides the status of a given host with
        respect to its transition from baseline managed to image managed.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host=None,
                     last_check_time=None,
                     image=None,
                     orphan_vibs=None,
                     status=None,
                     notifications=None,
                    ):
            """
            :type  host: :class:`str`
            :param host: Identifer of the host
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
            :type  last_check_time: :class:`datetime.datetime`
            :param last_check_time: Defines the timestamp when the last
                com.vmware.esx.settings.inventory.Inventory#extractInstalledImage
                method was executed on a given entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  image: :class:`com.vmware.esx.settings_client.SoftwareInfo`
            :param image: Defines image found on a given entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  orphan_vibs: :class:`bool`
            :param orphan_vibs: Defines if any orphan VIBs are found on an entity. If found the
                user is expected to check the detailed installed-image report of a
                given entity.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  status: :class:`Hosts.TransitionStatus`
            :param status: ``Hosts.TransitionStatus`` of a given entity as described in
                #TransitionStatus.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Describes if any notifications were raised for the given entity
                during the execution of the method.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.host = host
            self.last_check_time = last_check_time
            self.image = image
            self.orphan_vibs = orphan_vibs
            self.status = status
            self.notifications = notifications
            VapiStruct.__init__(self)


    HostSummary._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.host_summary', {
            'host': type.IdType(resource_types='HostSystem'),
            'last_check_time': type.DateTimeType(),
            'image': type.ReferenceType('com.vmware.esx.settings_client', 'SoftwareInfo'),
            'orphan_vibs': type.BooleanType(),
            'status': type.ReferenceType(__name__, 'Hosts.TransitionStatus'),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        HostSummary,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Hosts.IterationSpec`` class contains attributes used to break results
        into pages while returning transition summary of the entities defined in
        the 
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
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.iteration_spec', {
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Hosts.FilterSpec`` class contains attributes used to filter the
        results while returning the transition summary based on properties
        contained in it.
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


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.filter_spec', {
        },
        FilterSpec,
        False,
        None))


    class SortCriteria(VapiStruct):
        """
        The ``Hosts.SortCriteria`` class contains attributes that determine how a
        transition summary should be sorted by the values of one or more
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
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.sort_criteria', {
        },
        SortCriteria,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Hosts.Info`` class contains the summary of standalone hosts and the
        image they are running.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host_summaries=None,
                    ):
            """
            :type  host_summaries: :class:`list` of :class:`Hosts.HostSummary`
            :param host_summaries: List of host summaries. Each individual host summary contains its
                image and transition details.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.host_summaries = host_summaries
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.transition_summary.hosts.info', {
            'host_summaries': type.ListType(type.ReferenceType(__name__, 'Hosts.HostSummary')),
        },
        Info,
        False,
        None))



    def get(self,
            spec,
            filter=None,
            iterate=None,
            sort=None,
            ):
        """
        Returns the image and transition summaries of standalone hosts defined
        in the  which is passed as an input.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Hosts.GetParams`
        :param spec: Describe the inventory objects on which the specified operation
            will be performed.
        :type  filter: :class:`Hosts.FilterSpec` or ``None``
        :param filter: The filter applied to the transition summary.
            If None, the behavior is equivalent to fetching all the relevant
            records without having any filter criteria.
        :type  iterate: :class:`Hosts.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the behavior is to retrieve all the records
        :type  sort: :class:`Hosts.SortCriteria` or ``None``
        :param sort: The sort criteria applied to the transition summary.
            If None, the results are not sorted.
        :rtype: :class:`Hosts.Info`
        :return: Summary containing image details and transition status of the
            entities passed in input
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will contain more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If invalid  is passed as an input
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If some of the provided inventories doesn't exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to invoke the interface.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``HostSystem`` referenced by the attribute
              :attr:`Hosts.GetParams.hosts` requires
              ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``Folder`` referenced by the attribute
              :attr:`Hosts.GetParams.folders` requires
              ``VcIntegrity.lifecycleSettings.Read``.
            * The resource ``Datacenter`` referenced by the attribute
              :attr:`Hosts.GetParams.datacenters` requires
              ``VcIntegrity.lifecycleSettings.Read``.
        """
        return self._invoke('get',
                            {
                            'spec': spec,
                            'filter': filter,
                            'iterate': iterate,
                            'sort': sort,
                            })
class _ClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Clusters.GetParams'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Clusters.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Clusters.IterationSpec')),
            'sort': type.OptionalType(type.ReferenceType(__name__, 'Clusters.SortCriteria')),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/inventory/reports/transition-summary/clusters',
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
                'output_type': type.ReferenceType(__name__, 'Clusters.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.inventory.reports.transition_summary.clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _HostsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Hosts.GetParams'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Hosts.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Hosts.IterationSpec')),
            'sort': type.OptionalType(type.ReferenceType(__name__, 'Hosts.SortCriteria')),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/esx/settings/inventory/reports/transition-summary/hosts',
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
                'output_type': type.ReferenceType(__name__, 'Hosts.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.esx.settings.inventory.reports.transition_summary.hosts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Clusters': Clusters,
        'Hosts': Hosts,
    }

