# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.deployment.
#---------------------------------------------------------------------------

"""
The { com.vmware.vcenter.lcm.deployment} module provides classes for the
upgrade and deployment needs of a vCSA.

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


class MigrationUpgrade(VapiInterface):
    """
    The ``MigrationUpgrade`` class provides methods to configure and execute
    the migration upgrade of this vCenter Service appliance to a new version. 
    
    The vCenter upgrade should be run directly via the endpoints of the upgrade
    service - "/lcm/api" and "/lcm/rest". It is not recommended to use the
    "/api" endpoint exposed by the vCenter's vAPI endpoint service. The
    "/lcm/api" and "/lcm/rest" endpoints work correctly on any supported source
    version allowing monitoring and controlling the upgrade even during the
    upgrade's switchover. In contrast, the "/api" endpoint does not work during
    the upgrade's switchover and on some of the older supported source vCenter
    versions.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.deployment.migration_upgrade'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _MigrationUpgradeStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'check_task': 'check$task'})

    class SourceShutdownPolicy(Enum):
        """
        The ``MigrationUpgrade.SourceShutdownPolicy`` class defines when the source
        vCenter to be shutdown during the upgrade, if it is to be shutdown.
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
        NO_SHUTDOWN = None
        """
        The source vCenter should not be shutdown by the upgrade process. However,
        the vCenter services will be disabled and the network interfaces will be
        brought down to ensure there are no conflicts during the upgrade

        """
        DURING_UPGRADE = None
        """
        The source vCenter should be shutdown during the upgrade.

        """
        ON_SUCCESSFUL_UPGRADE = None
        """
        The source vCenter should be shutdown after successful upgrade.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`SourceShutdownPolicy` instance.
            """
            Enum.__init__(string)

    SourceShutdownPolicy._set_values({
        'NO_SHUTDOWN': SourceShutdownPolicy('NO_SHUTDOWN'),
        'DURING_UPGRADE': SourceShutdownPolicy('DURING_UPGRADE'),
        'ON_SUCCESSFUL_UPGRADE': SourceShutdownPolicy('ON_SUCCESSFUL_UPGRADE'),
    })
    SourceShutdownPolicy._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.source_shutdown_policy',
        SourceShutdownPolicy))


    class ConnectionType(Enum):
        """
        The ``MigrationUpgrade.ConnectionType`` enum provides available options for
        how to communicate with a machine.
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
        DIRECT = None
        """
        Communicates directly with the the desired machine on a network interface.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConnectionType` instance.
            """
            Enum.__init__(string)

    ConnectionType._set_values({
        'DIRECT': ConnectionType('DIRECT'),
    })
    ConnectionType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.connection_type',
        ConnectionType))


    class CancelType(Enum):
        """
        The ``MigrationUpgrade.CancelType`` class defines the cancel strategy that
        can be used on the vCenter in the case of cancellation.
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
        CLEAN_UP = None
        """
        Performs clean up on the old version vCenter. Does not result in data lost.
        This is the default option for the source cancellation.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`CancelType` instance.
            """
            Enum.__init__(string)

    CancelType._set_values({
        'CLEAN_UP': CancelType('CLEAN_UP'),
    })
    CancelType._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.cancel_type',
        CancelType))


    class PausePolicy(Enum):
        """
        The ``MigrationUpgrade.PausePolicy`` enum defines pause point in the
        upgrade workflow.The :func:`MigrationUpgrade.apply` does not accept already
        passed pause points.
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
        BEFORE_SWITCHOVER = None
        """
        Instructs the upgrade workflow to stop before the switchover operation. The
        option cannot be set together with
        :attr:`MigrationUpgrade.ApplySpec.start_switchover`, if such configuration
        is attempted will result in
        :class:`com.vmware.vapi.std.errors_client.InvalidArgument`. Once the pause
        point is reach, :func:`MigrationUpgrade.apply` needs to be called without a
        pause point (or a pause point that is later in the process) to resume the
        upgrade. The previous pause point is BEFORE_DATA_REPLICATION. 
        
        Stopping before the switchover operation means that the upgrade process
        will only deploy the target machine and replicate the data, but it will not
        do the switchover from the source to the target. The data replication
        continues in the background, so the downtime is minimal once the switchover
        is requested. 
        
        During the switchover the new target vCenter takes control and the old
        source vCenter is decommissioned. First, the services on the old vCenter
        are stopped. Second, the source identity (network, certificates and
        passwords) is transferred to the new machine. Third, the services on the
        new vCenter are started. Finally post health checks and post-upgrade
        configurations are executed. The switchover causes downtime from the stop
        of the services until they are started back on the new vCenter.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`PausePolicy` instance.
            """
            Enum.__init__(string)

    PausePolicy._set_values({
        'BEFORE_SWITCHOVER': PausePolicy('BEFORE_SWITCHOVER'),
    })
    PausePolicy._set_binding_type(type.EnumType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.pause_policy',
        PausePolicy))


    class InitSpec(VapiStruct):
        """
        The ``MigrationUpgrade.InitSpec`` class contains parameters used for
        initialization of the migration upgrade.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     deployment=None,
                     version=None,
                     cancellation_policy=None,
                     source_shutdown_policy=None,
                     repository=None,
                     post_upgrade_configuration_policy=None,
                     vcha_spec=None,
                    ):
            """
            :type  deployment: :class:`com.vmware.vcenter.lcm.deployment.common_client.ApplianceDeploymentConfig`
            :param deployment: Specification to describe the new appliance deployment
                configuration.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  version: :class:`str`
            :param version: Upgrade to vCSA version. The version is part of the metadata for
                each upgrade/update. It can be retrieved via the pending updates
                API.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cancellation_policy: :class:`MigrationUpgrade.CancellationPolicy` or ``None``
            :param cancellation_policy: Provides option to configure additional cancellation support and to
                enable automatic cancellation on error of the upgrade process.
                This attribute was added in **vSphere API 9.0.0.0**.
                cancellationPolicy If None then the default support is provided -
                :attr:`MigrationUpgrade.CancelType.CLEAN_UP` and there is no
                automatic cancellation on error
            :type  source_shutdown_policy: :class:`MigrationUpgrade.SourceShutdownPolicy` or ``None``
            :param source_shutdown_policy: Provides the ability to configure when the source vCenter should be
                shutdown during the upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the source vCenter will be shutdown during the upgrade.
            :type  repository: :class:`Repository.Spec` or ``None``
            :param repository: Provides a configuration for a repository containing vCenter
                deployment packages. Overrides the repository set with
                :func:`Repository.set` only for the upgrade being initialized.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the configured :class:`Repository` is used.
            :type  post_upgrade_configuration_policy: :class:`MigrationUpgrade.PostUpgradeConfigurationPolicy` or ``None``
            :param post_upgrade_configuration_policy: Provides post upgrade configuration options like source VM name
                preservation.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None no additional post upgrade configuration will be done
            :type  vcha_spec: :class:`MigrationUpgrade.VchaSpec` or ``None``
            :param vcha_spec: Provides VMware vCenter High Availability (VCHA) related upgrade
                configuration. Not needed for when VCHA is automatically
                configured. However, in the cases of VCHA with manual setup,
                vCenter containers connection information has to be provided in
                order to recreate Passive and Witness nodes in the same location as
                before upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None in manual VCHA setups, the upgrade process disables VCHA on
                the target machine. It is expected to manually recreate passive and
                witness nodes and enable back VCHA post-upgrade. In this case
                pre-upgrade nodes will remain powered off but not deleted; it is
                recommended to remove these to optimize storage usage. For auto
                VCHA setups this option will be ignored.
            """
            self.deployment = deployment
            self.version = version
            self.cancellation_policy = cancellation_policy
            self.source_shutdown_policy = source_shutdown_policy
            self.repository = repository
            self.post_upgrade_configuration_policy = post_upgrade_configuration_policy
            self.vcha_spec = vcha_spec
            VapiStruct.__init__(self)


    InitSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.init_spec', {
            'deployment': type.ReferenceType('com.vmware.vcenter.lcm.deployment.common_client', 'ApplianceDeploymentConfig'),
            'version': type.StringType(),
            'cancellation_policy': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.CancellationPolicy')),
            'source_shutdown_policy': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.SourceShutdownPolicy')),
            'repository': type.OptionalType(type.ReferenceType(__name__, 'Repository.Spec')),
            'post_upgrade_configuration_policy': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.PostUpgradeConfigurationPolicy')),
            'vcha_spec': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.VchaSpec')),
        },
        InitSpec,
        False,
        None))


    class VchaSpec(VapiStruct):
        """
        The ``MigrationUpgrade.VchaSpec`` class specifies the VMware vCenter High
        Availability (VCHA) configuration required for upgrading vCenter with
        manually configured VCHA. It details the vCenter container locations for
        cloning Passive and Witness nodes post-upgrade, ensuring they are recreated
        in the same locations as before the upgrade. 
        
        Note: This configuration does not support standalone ESX instances. For
        such setups, users are required to manually recreate Passive and Witness
        nodes on the respective ESX instances and then re-enable VCHA on the
        upgraded system.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     passive_node_container=None,
                     witness_node_container=None,
                    ):
            """
            :type  passive_node_container: :class:`com.vmware.vcenter.lcm.deployment.common_client.Connection`
            :param passive_node_container: Specifies connection to vCenter instance where passive node resides
                and will be recreated after successful upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  witness_node_container: :class:`com.vmware.vcenter.lcm.deployment.common_client.Connection`
            :param witness_node_container: Specifies connection to vCenter instance where witness node resides
                and will be recreated after successful upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.passive_node_container = passive_node_container
            self.witness_node_container = witness_node_container
            VapiStruct.__init__(self)


    VchaSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.vcha_spec', {
            'passive_node_container': type.ReferenceType('com.vmware.vcenter.lcm.deployment.common_client', 'Connection'),
            'witness_node_container': type.ReferenceType('com.vmware.vcenter.lcm.deployment.common_client', 'Connection'),
        },
        VchaSpec,
        False,
        None))


    class PostUpgradeConfigurationPolicy(VapiStruct):
        """
        The ``MigrationUpgrade.PostUpgradeConfigurationPolicy`` class contains
        configuration information to be applied on successful upgrade.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     rename_vm_policy=None,
                     delete_vm_policy=None,
                    ):
            """
            :type  rename_vm_policy: :class:`MigrationUpgrade.RenameVmPolicy` or ``None``
            :param rename_vm_policy: Provides options to preserve the original VM name as part of the
                upgrade, and to change the old vCenter VM name.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the VM name will be left as they are.
            :type  delete_vm_policy: :class:`MigrationUpgrade.DeleteVmPolicy` or ``None``
            :param delete_vm_policy: Provides the ability to delete the source vCenter VM after upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the source VM will not be deleted.
            """
            self.rename_vm_policy = rename_vm_policy
            self.delete_vm_policy = delete_vm_policy
            VapiStruct.__init__(self)


    PostUpgradeConfigurationPolicy._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.post_upgrade_configuration_policy', {
            'rename_vm_policy': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.RenameVmPolicy')),
            'delete_vm_policy': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.DeleteVmPolicy')),
        },
        PostUpgradeConfigurationPolicy,
        False,
        None))


    class RenameVmPolicy(VapiStruct):
        """
        The ``MigrationUpgrade.RenameVmPolicy`` class instructs the upgrade to
        preserve the original vCenter VM name on successful upgrade and allows
        changing the old vCenter VM name. The upgrade needs access to the container
        managing the old vCenter VM - either provide
        :attr:`com.vmware.vcenter.lcm.deployment.common_client.ApplianceDeploymentConfig.source_container`
        or ensure that the environment is self managed. Otherwise, the upgrade
        process validation will fail if this option is used.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     preserve_original_vm_name=None,
                     old_vcenter_name=None,
                    ):
            """
            :type  preserve_original_vm_name: :class:`bool`
            :param preserve_original_vm_name: Instructs the upgrade to preserve the old vCenter VM name on the
                new vCenter. In the process the old vCenter VM name will also be
                changed. Use oldVcenterName if you want to set it to a non-default
                name.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  old_vcenter_name: :class:`str` or ``None``
            :param old_vcenter_name: Allows changing the old vCenter VM name post upgrade. When the old
                VC VM name is preserved on new VC, the original VM itself needs to
                be renamed to avoid name collision with the new version.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None and preserveOriginalVmName is set to False the name of the
                original vCenter will be left as is. If None and
                preserveOriginalVmName is set to True the name will be changed to
                the old name appended with -old-<version>.
            """
            self.preserve_original_vm_name = preserve_original_vm_name
            self.old_vcenter_name = old_vcenter_name
            VapiStruct.__init__(self)


    RenameVmPolicy._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.rename_vm_policy', {
            'preserve_original_vm_name': type.BooleanType(),
            'old_vcenter_name': type.OptionalType(type.StringType()),
        },
        RenameVmPolicy,
        False,
        None))


    class DeleteVmPolicy(VapiStruct):
        """
        The ``MigrationUpgrade.DeleteVmPolicy`` class is used to instruct the
        upgrade process to delete the source vCenter VM on a successful upgrade. 
        
        To use this provide the container managing the source vCenter by setting
        :attr:`com.vmware.vcenter.lcm.deployment.common_client.ApplianceDeploymentConfig.source_container`
        in :attr:`MigrationUpgrade.InitSpec.deployment` or ensure the source
        vCenter is self-managed. The upgrade process will be prevented to start
        without such access, if this option is used.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     source_vc=None,
                    ):
            """
            :type  source_vc: :class:`bool`
            :param source_vc: Provides the ability to delete the source vCenter VM on a
                successful upgrade. This is executed immediately before successful
                upgrade is declared and the source machine will not be usable as a
                backup afterwards. Any failures during the deletion will be
                reported as warnings and will not break the upgrade.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.source_vc = source_vc
            VapiStruct.__init__(self)


    DeleteVmPolicy._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.delete_vm_policy', {
            'source_vc': type.BooleanType(),
        },
        DeleteVmPolicy,
        False,
        None))


    class ValidationResult(VapiStruct):
        """
        The ``MigrationUpgrade.ValidationResult`` class contains validation
        information for a given upgrade
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     notifications=None,
                    ):
            """
            :type  notifications: :class:`com.vmware.vcenter.lcm_client.Notifications` or ``None``
            :param notifications: Lists of the information messages, issues and warnings regarding
                the specified upgrade version.
                This attribute was added in **vSphere API 9.0.0.0**.
                notifications Only :class:`set` when there are notifications
            """
            self.notifications = notifications
            VapiStruct.__init__(self)


    ValidationResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.validation_result', {
            'notifications': type.OptionalType(type.ReferenceType('com.vmware.vcenter.lcm_client', 'Notifications')),
        },
        ValidationResult,
        False,
        None))


    class SourceConnection(VapiStruct):
        """
        The ``MigrationUpgrade.SourceConnection`` class provides the needed
        parameters for the target vCenter to talk with the source vCenter when
        there is such need.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'connection_type',
                {
                    'DIRECT' : [],
                }
            ),
        ]



        def __init__(self,
                     connection_type=None,
                    ):
            """
            :type  connection_type: :class:`MigrationUpgrade.ConnectionType`
            :param connection_type: What type of communication is to be done. The
                :attr:`MigrationUpgrade.ConnectionType.DIRECT` cannot be used
                together with
                :attr:`MigrationUpgrade.SourceShutdownPolicy.DURING_UPGRADE`.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.connection_type = connection_type
            VapiStruct.__init__(self)


    SourceConnection._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.source_connection', {
            'connection_type': type.ReferenceType(__name__, 'MigrationUpgrade.ConnectionType'),
        },
        SourceConnection,
        False,
        None))


    class CancellationPolicy(VapiStruct):
        """
        The ``MigrationUpgrade.CancellationPolicy`` class defines the configuration
        for the upgrade cancellation policy. Some options require specific handling
        during the upgrade thus they need to be known in advance.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     automatic=None,
                     method=None,
                     source_connection=None,
                    ):
            """
            :type  automatic: :class:`bool` or ``None``
            :param automatic: Indicates that the upgrade should be automatically cancelled on
                error.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the system will not trigger cancel workflow on error and
                will wait for additional input.
            :type  method: :class:`list` of :class:`MigrationUpgrade.CancelType` or ``None``
            :param method: Indicates which cancel methods to be used during the upgrade on the
                source vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None only the default method is used -
                :attr:`MigrationUpgrade.CancelType.CLEAN_UP`.
            :type  source_connection: :class:`MigrationUpgrade.SourceConnection` or ``None``
            :param source_connection: Indicates how to communicate with the source vCenter from the
                target vCenter if needed.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the system will only stop the upgrade on the target vCenter
                but it would not put the source vCenter in operational state, once
                the :func:`MigrationUpgrade.cancel` is called post switchover from
                source to target vCenter.
            """
            self.automatic = automatic
            self.method = method
            self.source_connection = source_connection
            VapiStruct.__init__(self)


    CancellationPolicy._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.cancellation_policy', {
            'automatic': type.OptionalType(type.BooleanType()),
            'method': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'MigrationUpgrade.CancelType'))),
            'source_connection': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.SourceConnection')),
        },
        CancellationPolicy,
        False,
        None))


    class ApplySpec(VapiStruct):
        """
        The ``MigrationUpgrade.ApplySpec`` class provides the
        :func:`MigrationUpgrade.apply` configuration. It allows configurations such
        as stopping at specific points of the upgrade or to configure a time window
        for the switchover. For more information about the upgrade process refer to
        :func:`MigrationUpgrade.apply`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pause=None,
                     start_switchover=None,
                    ):
            """
            :type  pause: :class:`MigrationUpgrade.PausePolicy` or ``None``
            :param pause: Allows the upgrade to be stopped at predefine points of the
                process. For more information about the available pause options
                check :class:`MigrationUpgrade.PausePolicy`.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade process will complete without stopping.
            :type  start_switchover: :class:`datetime.datetime` or ``None``
            :param start_switchover: Instructs the upgrade process to start the switchover operation
                after the given time. If the upgrade process is not ready for the
                switchover at the given time and end switchover is not provided the
                upgrade will wait for the preparation to complete to start the
                switchover thus resulting in the shortest possible switchover
                duration. The option cannot be set if
                :attr:`MigrationUpgrade.ApplySpec.pause` is set with value
                :attr:`MigrationUpgrade.PausePolicy.BEFORE_SWITCHOVER`, if such
                configuration is attempted will result in
                :class:`com.vmware.vapi.std.errors_client.InvalidArgument`.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None the upgrade process will execute the switchover operation
                as soon as possible.
            """
            self.pause = pause
            self.start_switchover = start_switchover
            VapiStruct.__init__(self)


    ApplySpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.migration_upgrade.apply_spec', {
            'pause': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.PausePolicy')),
            'start_switchover': type.OptionalType(type.DateTimeType()),
        },
        ApplySpec,
        False,
        None))



    def set(self,
            spec,
            ):
        """
        Initializes the upgrade workflow with upgrade parameters
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`MigrationUpgrade.InitSpec`
        :param spec: InitSpec parameters for the initialization of the upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if the appliance upgrade has started i.e it is in different state
            than INITIALIZED, CANCELED or UPGRADED
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the upgrade process. The
            accompanying error message will give more details about the
            failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('set',
                            {
                            'spec': spec,
                            })

    def get(self):
        """
        Gets the  parameters used to configure the ongoing appliance upgrade.
        The  will have its password masked. Returns the  if there is an upgrade
        process initialized, otherwise returns NotFound error.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`MigrationUpgrade.InitSpec`
        :return: Parameters being used to configure appliance upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if there is no configured upgrade.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised. The accompanying error message will
            give more details about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('get', None)


    def check_task(self,
              spec=None,
              ):
        """
        Runs sanity checks using the provided InitSpec or against running
        upgrade.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`MigrationUpgrade.InitSpec` or ``None``
        :param spec: InitSpec parameters to run sanity check on.
            If not provided will run sanity checks against the initialized
            upgrade process parameters. In that situation if there is no
            upgrade precheck will fail.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no upgrade process initialized and there is no InitSpec
            passed as input or if the upgrade process is in switchover or
            cancellation phase.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the upgrade process. The
            accompanying error message will give more details about the
            failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        task_id = self._invoke('check$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'MigrationUpgrade.ValidationResult'))
        return task_instance

    def apply(self,
              spec=None,
              ):
        """
        Executes the migration based upgrade by applying the upgrade
        configuration() set via the :func:`MigrationUpgrade.set`. The apply can
        be called multiple times while the upgrade is ongoing. In that case,
        the apply will try to override the old spec with the newly given
        parameters and will fail with
        :class:`com.vmware.vapi.std.errors_client.InvalidArgument` if that is
        not possible. The upgrade process executes several operations to reach
        the desired state of upgraded vCenter. 
        
        #. The upgrade process runs prechecks to ensure that the source vCenter
           health and the information provide will allow successful upgrade.
        #. The upgrade process deploys the new vCenter and configures it to be
           part of the upgrade. The services of the source vCenter are operational
           at that time and there is no disruption to the operations.
        #. The upgrade process configures the source vCenter and replicates its
           data to the new vCenter, without stopping the source vCenter or
           preventing its use. The services of the source vCenter are operational
           at that time and there is no disruption to the operations.
        #. The upgrade process executes the switchover which stops the service
           on the source vCenter, transfers the identity (network, certificates
           and passwords) to the new vCenter and starts the services on the new
           vCenter. This is the only phase of the upgrade which causes downtime to
           the vCenter operations.
        #. The upgrade process checks that the new vCenter is healthy before
           continuing forward.
        #. Finally the upgrade process performs any requested post-upgrade
           actions. The services of the source vCenter are operational at that
           time and there is no disruption to the operations.
        
        
        
        The  allows the upgrade execution to be configured to stop before the
        switchover operation or to start the switchover phase of the upgrade at
        a specific time. The apply will verify the  provided and if it is unset
        or incorrect the operation will fail. The  can be validated before that
        using the :func:`MigrationUpgrade.check`. 
        
        The upgrade progress can be monitored via
        :func:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.get`.
        More information about the progress of the upgrade can be found in
        :attr:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.Info.upgrade_info`
        and
        :attr:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.Info.subtasks`.
        
        The upgrade process can be manually cancelled by invoking the
        :func:`MigrationUpgrade.cancel` or can be configured to automatically
        cancel on error by
        :attr:`MigrationUpgrade.CancellationPolicy.automatic`. 
        
        If the upgrade process fails and the upgrade does not use
        :attr:`MigrationUpgrade.CancellationPolicy.automatic` it can be resumed
        again after fixing the problem and calling the same
        :func:`MigrationUpgrade.apply`. If the process cannot be fixed use
        :func:`MigrationUpgrade.cancel` to cancel the upgrade and start from
        the beginning.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`MigrationUpgrade.ApplySpec` or ``None``
        :param spec: allows the upgrade execution to be configured to stop before the
            switchover operation or to configure a switchover for a specific
            time window.
            The upgrade will be started and executed immediately.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no upgrade set on the system or the upgrade process is
            running cancellation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the upgrade process. The
            accompanying error message will give more details about the
            failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('apply',
                            {
                            'spec': spec,
                            })

    def cancel(self):
        """
        Cancels running vCenter upgrade. The cancellation cleans any actions
        done by the upgrade on the source vCenter without removing any
        production data generated during the upgrade. A new upgrade can be
        started after successful cancellation. The upgrade can be canceled
        explicitly at all points except in post-upgrade actions using this API.
        
        The cancellation process described above requires the
        :attr:`MigrationUpgrade.CancellationPolicy.source_connection` to
        complete successfully, depending when it is called. However, if the
        upgrade's cancellation policy cannot be used due to resource
        constraints, KB Article needs to be followed to ensure the vCenter is
        reverted to previous stable and consistent state. 
        
        If the vCenter being canceled is part of the Enhanced Linked Mode (ELM)
        environment, ensure the ELM is healthy after the cancellation. If not,
        take the necessary actions to restore the environment to its correct
        state following KB Article. 
        
        The cancellation progress can be monitored via
        :func:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.get`.
        More information about the progress of the upgrade can be found in
        :attr:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.Info.upgrade_info`
        and
        :attr:`com.vmware.vcenter.lcm.deployment.migration_upgrade_client.Status.Info.subtasks`.
        
        If the cancellation process fails, check what the problem is and fix
        it. After that, call the API again to ensure the removal of any
        information generated by the upgrade process and future upgradability
        of the vCenter.
        This method was added in **vSphere API 9.0.0.0**.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            if there is no upgrade process running or the upgrade is in
            post-upgrade actions.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the upgrade process. The
            accompanying error message will give more details about the
            failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('cancel', None)
class Repository(VapiInterface):
    """
    The ``Repository`` class provides methods to configure repository for the
    upgrade of the vCenter.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.lcm.deployment.repository'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RepositoryStub)
        self._VAPI_OPERATION_IDS = {}

    class Spec(VapiStruct):
        """
        The ``Repository.Spec`` class contains the repository configuration
        parameters.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     address=None,
                     username=None,
                     password=None,
                    ):
            """
            :type  address: :class:`str`
            :param address: The address of the repository.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  username: :class:`str` or ``None``
            :param username: The username used to authenticate with the repository,
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set`, when the repository requires authentication.
            :type  password: :class:`str` or ``None``
            :param password: The password used to authenticate with the repository,
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set`, when the repository requires authentication.
            """
            self.address = address
            self.username = username
            self.password = password
            VapiStruct.__init__(self)


    Spec._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.repository.spec', {
            'address': type.URIType(),
            'username': type.OptionalType(type.StringType()),
            'password': type.OptionalType(type.SecretType()),
        },
        Spec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Repository.Info`` class contains the repository configuration
        information.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     address=None,
                     username=None,
                    ):
            """
            :type  address: :class:`str`
            :param address: The address of the repository.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  username: :class:`str` or ``None``
            :param username: The username used to authenticate with the repository,
                This attribute was added in **vSphere API 9.0.0.0**.
                Only :class:`set`, when the repository requires authentication.
            """
            self.address = address
            self.username = username
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.lcm.deployment.repository.info', {
            'address': type.URIType(),
            'username': type.OptionalType(type.StringType()),
        },
        Info,
        False,
        None))



    def set(self,
            spec,
            ):
        """
        Configures the upgrade repository. If the upgrade repository requires
        credentials they will be validated.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Repository.Spec`
        :param spec: Set repository to be used by the lifecycle service.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if passed arguments are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the setting of the
            repository. The accompanying error message will give more details
            about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('set',
                            {
                            'spec': spec,
                            })

    def get(self):
        """
        Gets the currently configured repository for upgrade.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Repository.Info`
        :return: The upgrade repository configuration.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the caller is not authorized.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is other error raised as part of the getting of the
            repository. The accompanying error message will give more details
            about the failure.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized`
            if you do not have all of the privileges described as follows: 
            
            * Method execution requires ``VcLifecycle.Upgrade``.
        """
        return self._invoke('get', None)
class _MigrationUpgradeStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'MigrationUpgrade.InitSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/lcm/deployment/migration-upgrade',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/lcm/deployment/migration-upgrade',
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

        # properties for check operation
        check_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.InitSpec')),
        })
        check_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        check_input_value_validator_list = [
        ]
        check_output_validator_list = [
        ]
        check_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/deployment/migration-upgrade?action=check',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'check',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for apply operation
        apply_input_type = type.StructType('operation-input', {
            'spec': type.OptionalType(type.ReferenceType(__name__, 'MigrationUpgrade.ApplySpec')),
        })
        apply_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        apply_input_value_validator_list = [
        ]
        apply_output_validator_list = [
        ]
        apply_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/deployment/migration-upgrade?action=apply',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'apply',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for cancel operation
        cancel_input_type = type.StructType('operation-input', {})
        cancel_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        cancel_input_value_validator_list = [
        ]
        cancel_output_validator_list = [
        ]
        cancel_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/vcenter/lcm/deployment/migration-upgrade?action=cancel',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'cancel',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        operations = {
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'MigrationUpgrade.InitSpec'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'check$task': {
                'input_type': check_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': check_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': check_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'apply': {
                'input_type': apply_input_type,
                'output_type': type.VoidType(),
                'errors': apply_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': apply_input_value_validator_list,
                'output_validator_list': apply_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'cancel': {
                'input_type': cancel_input_type,
                'output_type': type.VoidType(),
                'errors': cancel_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': cancel_input_value_validator_list,
                'output_validator_list': cancel_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'get': get_rest_metadata,
            'check': check_rest_metadata,
            'apply': apply_rest_metadata,
            'cancel': cancel_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.deployment.migration_upgrade',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _RepositoryStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Repository.Spec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/lcm/deployment/repository',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {})
        get_error_dict = {
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
            url_template='/vcenter/lcm/deployment/repository',
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
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Repository.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'set': set_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.lcm.deployment.repository',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'MigrationUpgrade': MigrationUpgrade,
        'Repository': Repository,
        'common': 'com.vmware.vcenter.lcm.deployment.common_client.StubFactory',
        'migration_upgrade': 'com.vmware.vcenter.lcm.deployment.migration_upgrade_client.StubFactory',
    }

