# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.esx.settings.inventory.reports.summary.
#---------------------------------------------------------------------------

"""
The ``com.vmware.esx.settings.inventory.reports.summary_client`` module
provides classes to manage operations summary for entities belonging to vCenter
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
    The ``Clusters`` class provides operations summary report of clusters under
    given inventory.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.inventory.reports.summary.clusters'
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

    class TaskStatus(Enum):
        """
        The ``Clusters.TaskStatus`` class defines the status for an individual
        task.
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
        PENDING = None
        """
        The method is not performed yet.

        """
        RUNNING = None
        """
        The method is in progress.

        """
        CANCELED = None
        """
        The method is canceled.

        """
        SUCCEEDED = None
        """
        The method indicates a success.

        """
        FAILED = None
        """
        The method encountered an unspecified error.

        """
        SKIPPED = None
        """
        The method was skipped.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TaskStatus` instance.
            """
            Enum.__init__(string)

    TaskStatus._set_values({
        'PENDING': TaskStatus('PENDING'),
        'RUNNING': TaskStatus('RUNNING'),
        'CANCELED': TaskStatus('CANCELED'),
        'SUCCEEDED': TaskStatus('SUCCEEDED'),
        'FAILED': TaskStatus('FAILED'),
        'SKIPPED': TaskStatus('SKIPPED'),
    })
    TaskStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.task_status',
        TaskStatus))


    class PrecheckStatus(Enum):
        """
        The ``Clusters.PrecheckStatus`` class defines the status result for a
        particular precheck. Note: This is patterned after values of
        com.vmware.esx.settings.clusters#Status enumeration.
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
        OK = None
        """
        The precheck indicates a success.

        """
        WARNING = None
        """
        The precheck indicates a warning.

        """
        TIMEOUT = None
        """
        The precheck did not return in a timely manner.

        """
        ERROR = None
        """
        The precheck indicates an error.

        """
        RETRY = None
        """
        The precheck failed because of an intermittent error, for example a service
        is overloaded. The client can choose to retry the health precheck before
        considering the precheck as failed.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`PrecheckStatus` instance.
            """
            Enum.__init__(string)

    PrecheckStatus._set_values({
        'OK': PrecheckStatus('OK'),
        'WARNING': PrecheckStatus('WARNING'),
        'TIMEOUT': PrecheckStatus('TIMEOUT'),
        'ERROR': PrecheckStatus('ERROR'),
        'RETRY': PrecheckStatus('RETRY'),
    })
    PrecheckStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.precheck_status',
        PrecheckStatus))


    class ApplyStatus(Enum):
        """
        The ``Clusters.ApplyStatus`` class contains the possible different status
        codes that can be returned while trying to apply the desired software
        specification to hosts within the cluster. Note: This is patterned after
        values of com.vmware.esx.settings.clusters.ApplyStatus#Status enumeration.
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
        RUNNING = None
        """
        The method is in progress.

        """
        OK = None
        """
        The method completed successfully.

        """
        SKIPPED = None
        """
        The method was skipped.

        """
        TIMED_OUT = None
        """
        The method timed out.

        """
        ERROR = None
        """
        The method encountered an unspecified error.

        """
        RETRY_PENDING = None
        """
        The method is being scheduled for retry.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ApplyStatus` instance.
            """
            Enum.__init__(string)

    ApplyStatus._set_values({
        'RUNNING': ApplyStatus('RUNNING'),
        'OK': ApplyStatus('OK'),
        'SKIPPED': ApplyStatus('SKIPPED'),
        'TIMED_OUT': ApplyStatus('TIMED_OUT'),
        'ERROR': ApplyStatus('ERROR'),
        'RETRY_PENDING': ApplyStatus('RETRY_PENDING'),
    })
    ApplyStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.apply_status',
        ApplyStatus))


    class GetParams(VapiStruct):
        """
        The ``Clusters.GetParams`` class contains attributes that are necessary to
        generate the operations summary report of clusters under given inventory.
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
                inventory on which the operations summary report will be generated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  clusters: :class:`set` of :class:`str`
            :param clusters: List of clusters on which the operations summary needs to be
                generated.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Clusters.GetParams.InventoryType.CLUSTER`.
            :type  folders: :class:`set` of :class:`str`
            :param folders: List of folders on which the operations summary needs to be
                generated. Internally the folder entities will be expanded to
                individual clusters which are underneath the designated folder. If
                the list contains the managed object ID of the root folder, the
                specified operation will be executed on all clusters in the
                vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Clusters.GetParams.InventoryType.FOLDER`.
            :type  datacenters: :class:`set` of :class:`str`
            :param datacenters: List of data-centers on which the operations summary needs to be
                generated. Internally the data-center entities will be expanded to
                individual clusters which are underneath the designated
                data-center.
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
            of entities belonging to vCenter's inventory on which the operations
            summary report will be generated.
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
            Type specifying folder within the vCenter's inventory.

            """
            DATACENTER = None
            """
            Type specifying data-center within the vCenter's inventory.

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
            'com.vmware.esx.settings.inventory.reports.summary.clusters.get_params.inventory_type',
            InventoryType))

    GetParams._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.get_params', {
            'type': type.ReferenceType(__name__, 'Clusters.GetParams.InventoryType'),
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        GetParams,
        False,
        None))


    class ComplianceResult(VapiStruct):
        """
        The ``Clusters.ComplianceResult`` class contains attributes to describe the
        compliance result of a cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     compliance_status=None,
                     last_compliance_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Clusters.TaskStatus`
            :param task_status: Provides the status of the compliance task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliance_status: :class:`com.vmware.esx.settings_client.ComplianceStatus`
            :param compliance_status: Overall compliance status of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_compliance_time: :class:`datetime.datetime` or ``None``
            :param last_compliance_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the scan operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.compliance_status = compliance_status
            self.last_compliance_time = last_compliance_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    ComplianceResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.compliance_result', {
            'task_status': type.ReferenceType(__name__, 'Clusters.TaskStatus'),
            'compliance_status': type.ReferenceType('com.vmware.esx.settings_client', 'ComplianceStatus'),
            'last_compliance_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ComplianceResult,
        False,
        None))


    class PrecheckResult(VapiStruct):
        """
        The ``Clusters.PrecheckResult`` class contains attributes that describe
        aggregated status of all prechecks performed.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     precheck_status=None,
                     last_precheck_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Clusters.TaskStatus`
            :param task_status: Provides the status of the precheck task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  precheck_status: :class:`Clusters.PrecheckStatus`
            :param precheck_status: Aggregated status from all prechecks performed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_precheck_time: :class:`datetime.datetime` or ``None``
            :param last_precheck_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.precheck_status = precheck_status
            self.last_precheck_time = last_precheck_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    PrecheckResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.precheck_result', {
            'task_status': type.ReferenceType(__name__, 'Clusters.TaskStatus'),
            'precheck_status': type.ReferenceType(__name__, 'Clusters.PrecheckStatus'),
            'last_precheck_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        PrecheckResult,
        False,
        None))


    class StageResult(VapiStruct):
        """
        The ``Clusters.StageResult`` class contains attributes that describe the
        result of a stage operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     stage_status=None,
                     last_stage_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Clusters.TaskStatus`
            :param task_status: Provides the status of the stage task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  stage_status: :class:`com.vmware.esx.settings_client.StageStatus`
            :param stage_status: Specifies the aggregated status of the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_stage_time: :class:`datetime.datetime` or ``None``
            :param last_stage_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.stage_status = stage_status
            self.last_stage_time = last_stage_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    StageResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.stage_result', {
            'task_status': type.ReferenceType(__name__, 'Clusters.TaskStatus'),
            'stage_status': type.ReferenceType('com.vmware.esx.settings_client', 'StageStatus'),
            'last_stage_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        StageResult,
        False,
        None))


    class ApplyResult(VapiStruct):
        """
        The ``Clusters.ApplyResult`` class contains attributes that describe the
        result of an apply operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     apply_status=None,
                     last_apply_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Clusters.TaskStatus`
            :param task_status: Provides the status of the apply task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  apply_status: :class:`Clusters.ApplyStatus`
            :param apply_status: Specifies the aggregated status of the apply operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_apply_time: :class:`datetime.datetime` or ``None``
            :param last_apply_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.apply_status = apply_status
            self.last_apply_time = last_apply_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    ApplyResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.apply_result', {
            'task_status': type.ReferenceType(__name__, 'Clusters.TaskStatus'),
            'apply_status': type.ReferenceType(__name__, 'Clusters.ApplyStatus'),
            'last_apply_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ApplyResult,
        False,
        None))


    class SoftwareSpecInfo(VapiStruct):
        """
        The ``Clusters.SoftwareSpecInfo`` class contains attributes to describe the
        details regarding the software specification from repository assigned to
        the cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     display_name=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the software specification from repository assigned
                to the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``.
            :type  display_name: :class:`str`
            :param display_name: Display name of the software specification from repository assigned
                to the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.display_name = display_name
            VapiStruct.__init__(self)


    SoftwareSpecInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.software_spec_info', {
            'id': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'display_name': type.StringType(),
        },
        SoftwareSpecInfo,
        False,
        None))


    class ClusterSummary(VapiStruct):
        """
        The ``Clusters.ClusterSummary`` class contains information to summarize the
        operations performed on a cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     software_spec_info=None,
                     compliance_summary=None,
                     precheck_summary=None,
                     stage_summary=None,
                     apply_summary=None,
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
            :type  software_spec_info: :class:`Clusters.SoftwareSpecInfo`
            :param software_spec_info: Information of the software specification from repository assigned
                to the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliance_summary: :class:`Clusters.ComplianceResult` or ``None``
            :param compliance_summary: Summary of the cluster compliance operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the cluster compliance operation is not requested.
            :type  precheck_summary: :class:`Clusters.PrecheckResult` or ``None``
            :param precheck_summary: Summary of the cluster precheck operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the cluster precheck operation is not requested.
            :type  stage_summary: :class:`Clusters.StageResult` or ``None``
            :param stage_summary: Summary of the cluster stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the cluster stage operation is not requested.
            :type  apply_summary: :class:`Clusters.ApplyResult` or ``None``
            :param apply_summary: Summary of the cluster apply operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the cluster apply operation is not requested.
            """
            self.cluster = cluster
            self.software_spec_info = software_spec_info
            self.compliance_summary = compliance_summary
            self.precheck_summary = precheck_summary
            self.stage_summary = stage_summary
            self.apply_summary = apply_summary
            VapiStruct.__init__(self)


    ClusterSummary._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.cluster_summary', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'software_spec_info': type.ReferenceType(__name__, 'Clusters.SoftwareSpecInfo'),
            'compliance_summary': type.OptionalType(type.ReferenceType(__name__, 'Clusters.ComplianceResult')),
            'precheck_summary': type.OptionalType(type.ReferenceType(__name__, 'Clusters.PrecheckResult')),
            'stage_summary': type.OptionalType(type.ReferenceType(__name__, 'Clusters.StageResult')),
            'apply_summary': type.OptionalType(type.ReferenceType(__name__, 'Clusters.ApplyResult')),
        },
        ClusterSummary,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Clusters.IterationSpec`` class contains attributes used to break
        results into pages while returning operations summary of the entities
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
        'com.vmware.esx.settings.inventory.reports.summary.clusters.iteration_spec', {
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Clusters.FilterSpec`` class contains attributes used to filter the
        results while returning the operations summary based on properties
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
        'com.vmware.esx.settings.inventory.reports.summary.clusters.filter_spec', {
        },
        FilterSpec,
        False,
        None))


    class SortCriteria(VapiStruct):
        """
        The ``Clusters.SortCriteria`` class contains attributes that determine how
        a operations summary should be sorted by the values of one or more
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
        'com.vmware.esx.settings.inventory.reports.summary.clusters.sort_criteria', {
        },
        SortCriteria,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Clusters.Info`` class contains the summary about the operations
        performed on the clusters.
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
            :param cluster_summaries: List of cluster summaries.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cluster_summaries = cluster_summaries
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.clusters.info', {
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
        Returns the information about the software specifications from the
        repository assigned to clusters as well as operations summary performed
        on the clusters under inventory defined in the  as an input.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Clusters.GetParams`
        :param spec: Describe the inventory objects on which the specified operation
            will be performed.
        :type  filter: :class:`Clusters.FilterSpec` or ``None``
        :param filter: The filter applied to the operations summary.
            If None, the behavior is equivalent to fetching all the relevant
            records without having any filter criteria.
        :type  iterate: :class:`Clusters.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the behavior is to retrieve all the records
        :type  sort: :class:`Clusters.SortCriteria` or ``None``
        :param sort: The sort criteria applied to the operations summary.
            If None, the results are not sorted.
        :rtype: :class:`Clusters.Info`
        :return: Summary containing the software specifications from the repository
            assigned to clusters and operations summary performed on the
            clusters under inventory passed in as input
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will contain more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If invalid  is passed as an input.
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
    The ``Hosts`` class provides operations summary report of standalone hosts
    under given inventory.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.esx.settings.inventory.reports.summary.hosts'
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

    class TaskStatus(Enum):
        """
        The ``Hosts.TaskStatus`` class defines the status for an individual task.
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
        PENDING = None
        """
        The method is not performed yet.

        """
        RUNNING = None
        """
        The method is in progress.

        """
        CANCELED = None
        """
        The method is canceled.

        """
        SUCCEEDED = None
        """
        The method indicates a success.

        """
        FAILED = None
        """
        The method encountered an unspecified error.

        """
        SKIPPED = None
        """
        The method was skipped.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`TaskStatus` instance.
            """
            Enum.__init__(string)

    TaskStatus._set_values({
        'PENDING': TaskStatus('PENDING'),
        'RUNNING': TaskStatus('RUNNING'),
        'CANCELED': TaskStatus('CANCELED'),
        'SUCCEEDED': TaskStatus('SUCCEEDED'),
        'FAILED': TaskStatus('FAILED'),
        'SKIPPED': TaskStatus('SKIPPED'),
    })
    TaskStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.task_status',
        TaskStatus))


    class PrecheckStatus(Enum):
        """
        The ``Hosts.PrecheckStatus`` class defines the status result for a
        particular precheck. Note: This is patterned after values of
        com.vmware.esx.settings.hosts#Status enumeration.
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
        OK = None
        """
        The precheck indicates a success.

        """
        WARNING = None
        """
        The precheck indicates a warning.

        """
        TIMEOUT = None
        """
        The precheck did not return in a timely manner.

        """
        ERROR = None
        """
        The precheck indicates an error.

        """
        RETRY = None
        """
        The precheck failed because of an intermittent error, for example a service
        is overloaded. The client can choose to retry the health precheck before
        considering the precheck as failed.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`PrecheckStatus` instance.
            """
            Enum.__init__(string)

    PrecheckStatus._set_values({
        'OK': PrecheckStatus('OK'),
        'WARNING': PrecheckStatus('WARNING'),
        'TIMEOUT': PrecheckStatus('TIMEOUT'),
        'ERROR': PrecheckStatus('ERROR'),
        'RETRY': PrecheckStatus('RETRY'),
    })
    PrecheckStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.precheck_status',
        PrecheckStatus))


    class ApplyStatus(Enum):
        """
        The ``Hosts.ApplyStatus`` class contains attributes that describe the
        status of an apply operation. Note: This is patterned after values of
        com.vmware.esx.settings.hosts.ApplyStatus#Status enumeration.
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
        RUNNING = None
        """
        The method is in progress.

        """
        OK = None
        """
        The method completed successfully.

        """
        SKIPPED = None
        """
        The method was skipped.

        """
        TIMED_OUT = None
        """
        The method timed out.

        """
        ERROR = None
        """
        The method encountered an unspecified error.

        """
        RETRY_PENDING = None
        """
        The method is being scheduled for retry.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ApplyStatus` instance.
            """
            Enum.__init__(string)

    ApplyStatus._set_values({
        'RUNNING': ApplyStatus('RUNNING'),
        'OK': ApplyStatus('OK'),
        'SKIPPED': ApplyStatus('SKIPPED'),
        'TIMED_OUT': ApplyStatus('TIMED_OUT'),
        'ERROR': ApplyStatus('ERROR'),
        'RETRY_PENDING': ApplyStatus('RETRY_PENDING'),
    })
    ApplyStatus._set_binding_type(type.EnumType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.apply_status',
        ApplyStatus))


    class GetParams(VapiStruct):
        """
        The ``Hosts.GetParams`` class contains attributes that are necessary to
        generate the operations summary report of standalone hosts under given
        inventory.
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
                inventory on which the operations summary report will be generated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  hosts: :class:`set` of :class:`str`
            :param hosts: List of standalone hosts on which the operations summary needs to
                be generated.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``HostSystem``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Hosts.GetParams.InventoryType.HOST`.
            :type  folders: :class:`set` of :class:`str`
            :param folders: List of folders on which the operations summary needs to be
                generated. Internally the folder entities will be expanded to
                individual standalone hosts which are underneath the designated
                folder. If the list contains the managed object ID of the root
                folder, the specified operation will be executed on all standalone
                hosts in the vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``Folder``. When methods return a value of this class as a return
                value, the attribute will contain identifiers for the resource
                type: ``Folder``.
                This attribute is optional and it is only relevant when the value
                of ``type`` is :attr:`Hosts.GetParams.InventoryType.FOLDER`.
            :type  datacenters: :class:`set` of :class:`str`
            :param datacenters: List of data-centers on which the operations summary needs to be
                generated. Internally the data-center entities will be expanded to
                individual standalone hosts which are underneath the designated
                data-center.
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
            entities belonging to vCenter's inventory on which the operations summary
            report will be generated.
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
            Type specifying folder within the vCenter's inventory.

            """
            DATACENTER = None
            """
            Type specifying data-center within the vCenter's inventory.

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
            'com.vmware.esx.settings.inventory.reports.summary.hosts.get_params.inventory_type',
            InventoryType))

    GetParams._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.get_params', {
            'type': type.ReferenceType(__name__, 'Hosts.GetParams.InventoryType'),
            'hosts': type.OptionalType(type.SetType(type.IdType())),
            'folders': type.OptionalType(type.SetType(type.IdType())),
            'datacenters': type.OptionalType(type.SetType(type.IdType())),
        },
        GetParams,
        False,
        None))


    class ComplianceResult(VapiStruct):
        """
        The ``Hosts.ComplianceResult`` class contains attributes to describe the
        compliance result of a standalone host.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     compliance_status=None,
                     last_compliance_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Hosts.TaskStatus`
            :param task_status: Provides the status of the compliance task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliance_status: :class:`com.vmware.esx.settings_client.ComplianceStatus`
            :param compliance_status: Overall compliance status of the standalone host.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_compliance_time: :class:`datetime.datetime` or ``None``
            :param last_compliance_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the scan operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.compliance_status = compliance_status
            self.last_compliance_time = last_compliance_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    ComplianceResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.compliance_result', {
            'task_status': type.ReferenceType(__name__, 'Hosts.TaskStatus'),
            'compliance_status': type.ReferenceType('com.vmware.esx.settings_client', 'ComplianceStatus'),
            'last_compliance_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ComplianceResult,
        False,
        None))


    class PrecheckResult(VapiStruct):
        """
        The ``Hosts.PrecheckResult`` class contains attributes that describe
        aggregated status of all prechecks performed.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     precheck_status=None,
                     last_precheck_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Hosts.TaskStatus`
            :param task_status: Provides the status of the precheck task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  precheck_status: :class:`Hosts.PrecheckStatus`
            :param precheck_status: Aggregated status from all prechecks performed.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_precheck_time: :class:`datetime.datetime` or ``None``
            :param last_precheck_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.precheck_status = precheck_status
            self.last_precheck_time = last_precheck_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    PrecheckResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.precheck_result', {
            'task_status': type.ReferenceType(__name__, 'Hosts.TaskStatus'),
            'precheck_status': type.ReferenceType(__name__, 'Hosts.PrecheckStatus'),
            'last_precheck_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        PrecheckResult,
        False,
        None))


    class StageResult(VapiStruct):
        """
        The ``Hosts.StageResult`` class contains attributes that describe the
        result of a stage operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     stage_status=None,
                     last_stage_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Hosts.TaskStatus`
            :param task_status: Provides the status of the stage task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  stage_status: :class:`com.vmware.esx.settings_client.StageStatus`
            :param stage_status: Specifies the aggregated status of the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_stage_time: :class:`datetime.datetime` or ``None``
            :param last_stage_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.stage_status = stage_status
            self.last_stage_time = last_stage_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    StageResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.stage_result', {
            'task_status': type.ReferenceType(__name__, 'Hosts.TaskStatus'),
            'stage_status': type.ReferenceType('com.vmware.esx.settings_client', 'StageStatus'),
            'last_stage_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        StageResult,
        False,
        None))


    class ApplyResult(VapiStruct):
        """
        The ``Hosts.ApplyResult`` class contains attributes that describe the
        result of an apply operation.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task_status=None,
                     apply_status=None,
                     last_apply_time=None,
                     notifications=None,
                    ):
            """
            :type  task_status: :class:`Hosts.TaskStatus`
            :param task_status: Provides the status of the apply task.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  apply_status: :class:`Hosts.ApplyStatus`
            :param apply_status: Specifies the aggregated status of the apply operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_apply_time: :class:`datetime.datetime` or ``None``
            :param last_apply_time: Time when the operation performed last time.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the operation has not been run yet.
            :type  notifications: :class:`com.vmware.esx.settings_client.Notifications`
            :param notifications: Notifications returned by the stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.task_status = task_status
            self.apply_status = apply_status
            self.last_apply_time = last_apply_time
            self.notifications = notifications
            VapiStruct.__init__(self)


    ApplyResult._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.apply_result', {
            'task_status': type.ReferenceType(__name__, 'Hosts.TaskStatus'),
            'apply_status': type.ReferenceType(__name__, 'Hosts.ApplyStatus'),
            'last_apply_time': type.OptionalType(type.DateTimeType()),
            'notifications': type.ReferenceType('com.vmware.esx.settings_client', 'Notifications'),
        },
        ApplyResult,
        False,
        None))


    class SoftwareSpecInfo(VapiStruct):
        """
        The ``Hosts.SoftwareSpecInfo`` class contains attributes to describe the
        details regarding the software specification from repository assigned to
        the standalone host.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     display_name=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: Identifier of the software specification from repository assigned
                to the standalone host.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.esx.settings.repository.software_spec``.
            :type  display_name: :class:`str`
            :param display_name: Display name of the software specification from repository assigned
                to the standalone host.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.display_name = display_name
            VapiStruct.__init__(self)


    SoftwareSpecInfo._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.software_spec_info', {
            'id': type.IdType(resource_types='com.vmware.esx.settings.repository.software_spec'),
            'display_name': type.StringType(),
        },
        SoftwareSpecInfo,
        False,
        None))


    class HostSummary(VapiStruct):
        """
        The ``Hosts.HostSummary`` class contains information to summarize the
        operations performed on a standalone host.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host=None,
                     software_spec_info=None,
                     compliance_summary=None,
                     precheck_summary=None,
                     stage_summary=None,
                     apply_summary=None,
                    ):
            """
            :type  host: :class:`str`
            :param host: Identifier of the standalone host.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
            :type  software_spec_info: :class:`Hosts.SoftwareSpecInfo`
            :param software_spec_info: Information of the software specification from repository assigned
                to the standalone host.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  compliance_summary: :class:`Hosts.ComplianceResult` or ``None``
            :param compliance_summary: Summary of the standalone host compliance operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the standalone host compliance operation is not requested.
            :type  precheck_summary: :class:`Hosts.PrecheckResult` or ``None``
            :param precheck_summary: Summary of the standalone host precheck operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the standalone host precheck operation is not requested.
            :type  stage_summary: :class:`Hosts.StageResult` or ``None``
            :param stage_summary: Summary of the standalone host stage operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the standalone host stage operation is not requested.
            :type  apply_summary: :class:`Hosts.ApplyResult` or ``None``
            :param apply_summary: Summary of the standalone host apply operation.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if the standalone host apply operation is not requested.
            """
            self.host = host
            self.software_spec_info = software_spec_info
            self.compliance_summary = compliance_summary
            self.precheck_summary = precheck_summary
            self.stage_summary = stage_summary
            self.apply_summary = apply_summary
            VapiStruct.__init__(self)


    HostSummary._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.host_summary', {
            'host': type.IdType(resource_types='HostSystem'),
            'software_spec_info': type.ReferenceType(__name__, 'Hosts.SoftwareSpecInfo'),
            'compliance_summary': type.OptionalType(type.ReferenceType(__name__, 'Hosts.ComplianceResult')),
            'precheck_summary': type.OptionalType(type.ReferenceType(__name__, 'Hosts.PrecheckResult')),
            'stage_summary': type.OptionalType(type.ReferenceType(__name__, 'Hosts.StageResult')),
            'apply_summary': type.OptionalType(type.ReferenceType(__name__, 'Hosts.ApplyResult')),
        },
        HostSummary,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Hosts.IterationSpec`` class contains attributes used to break results
        into pages while returning operations summary of the entities defined in
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
        'com.vmware.esx.settings.inventory.reports.summary.hosts.iteration_spec', {
        },
        IterationSpec,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Hosts.FilterSpec`` class contains attributes used to filter the
        results while returning the operations summary based on properties
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
        'com.vmware.esx.settings.inventory.reports.summary.hosts.filter_spec', {
        },
        FilterSpec,
        False,
        None))


    class SortCriteria(VapiStruct):
        """
        The ``Hosts.SortCriteria`` class contains attributes that determine how a
        operations summary should be sorted by the values of one or more
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
        'com.vmware.esx.settings.inventory.reports.summary.hosts.sort_criteria', {
        },
        SortCriteria,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Hosts.Info`` class contains the summary about the operations
        performed on standalone hosts.
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
            :param host_summaries: List of host summaries.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.host_summaries = host_summaries
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.esx.settings.inventory.reports.summary.hosts.info', {
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
        Returns the information about the software specifications from the
        repository assigned to standalone hosts as well as operations summary
        performed on the standalone hosts under inventory defined in the  as an
        input.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Hosts.GetParams`
        :param spec: Describe the inventory objects on which the specified operation
            will be performed.
        :type  filter: :class:`Hosts.FilterSpec` or ``None``
        :param filter: The filter applied to the operations summary.
            If None, the behavior is equivalent to fetching all the relevant
            records without having any filter criteria.
        :type  iterate: :class:`Hosts.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the behavior is to retrieve all the records
        :type  sort: :class:`Hosts.SortCriteria` or ``None``
        :param sort: The sort criteria applied to the operations summary.
            If None, the results are not sorted.
        :rtype: :class:`Hosts.Info`
        :return: Summary containing the software specifications from the repository
            assigned to standalone hosts and operations summary performed on
            the standalone hosts under inventory passed in as input.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error. The accompanying error message
            will contain more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If invalid  is passed as an input.
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
            url_template='/esx/settings/inventory/reports/summary/clusters',
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
            self, iface_name='com.vmware.esx.settings.inventory.reports.summary.clusters',
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
            url_template='/esx/settings/inventory/reports/summary/hosts',
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
            self, iface_name='com.vmware.esx.settings.inventory.reports.summary.hosts',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Clusters': Clusters,
        'Hosts': Hosts,
    }

