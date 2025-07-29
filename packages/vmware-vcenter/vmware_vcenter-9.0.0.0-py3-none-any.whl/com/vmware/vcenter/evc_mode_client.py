# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.evc_mode.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.evc_mode_client`` module provides classes for creating
custom EVC (Enhanced vMotion Compatibility) modes.

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


class FeatureMask(VapiStruct):
    """
    A mask that is applied to a host feature capability.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 key=None,
                 name=None,
                 value=None,
                ):
        """
        :type  key: :class:`str`
        :param key: Accessor name for the feature mask.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  name: :class:`str`
        :param name: Name of the feature.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  value: :class:`str`
        :param value: Opaque value to change the host feature capability to. Masking
            operation is contained in the value.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.key = key
        self.name = name
        self.value = value
        VapiStruct.__init__(self)


FeatureMask._set_binding_type(type.StructType(
    'com.vmware.vcenter.evc_mode.feature_mask', {
        'key': type.StringType(),
        'name': type.StringType(),
        'value': type.StringType(),
    },
    FeatureMask,
    False,
    None))



class EvcMode(VapiStruct):
    """
    The ``EvcMode`` describes a set of ``FeatureMask`` used for Enhanced
    vMotion Compatibility (EVC). 
    
    An EVC mode is associated with a set of CPU features. When a host is added
    to an EVC-enabled cluster, the vCenter Server determines the CPU
    compatibility to preserve vMotion compatibility within the cluster. If the
    host CPU is compatible with those already in the cluster, the Server adds
    the host to the cluster and configures it for compatible operation. Hosts
    that are not compatible are not allowed to join the cluster.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 key=None,
                 masks=None,
                ):
        """
        :type  key: :class:`str`
        :param key: The system generated unique identifier for the EvcMode.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  masks: :class:`list` of :class:`FeatureMask`
        :param masks: The masks (modifications to a host's feature capabilities) that
            limit a host's capabilities to that of the EVC mode baseline.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.key = key
        self.masks = masks
        VapiStruct.__init__(self)


EvcMode._set_binding_type(type.StructType(
    'com.vmware.vcenter.evc_mode.evc_mode', {
        'key': type.StringType(),
        'masks': type.ListType(type.ReferenceType(__name__, 'FeatureMask')),
    },
    EvcMode,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

