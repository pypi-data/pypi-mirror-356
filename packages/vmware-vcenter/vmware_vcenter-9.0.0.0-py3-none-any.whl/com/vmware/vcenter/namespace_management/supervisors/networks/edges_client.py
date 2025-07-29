# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.supervisors.networks.edges.
#---------------------------------------------------------------------------

"""
The
``com.vmware.vcenter.namespace_management.supervisors.networks.edges_client``
module provides classes and classes to manage Supervisor edges.

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

class EdgeProvider(Enum):
    """
    ``EdgeProvider`` describes the available edge services.
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
    AVI = None
    """
    :attr:`EdgeProvider.AVI` specifies the Avi Load Balancer. This edge
    provider is supported on Supervisors configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.VSPHERE`.

    """
    HAPROXY = None
    """
    :attr:`EdgeProvider.HAPROXY` is an HAProxy load balancer fronted by the
    Data Plane API. This edge provider is supported on Supervisors configured
    with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.VSPHERE`.

    .. deprecated:: vSphere API 9.0.0.0
        This class attribute is deprecated as of **vSphere API 9.0.0.0**. Use
        :attr:`EdgeProvider.VSPHERE_FOUNDATION` or :attr:`EdgeProvider.AVI`
        instead.

    """
    NSX_LB = None
    """
    :attr:`EdgeProvider.NSX_LB` specifies the NSX Load Balancer configured on
    the NSX manager, specific to Supervisors configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSX_VPC`
    or
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSXT`.
    This class attribute was added in **vSphere API 9.0.0.0**.

    """
    NSX_REGISTERED_AVI = None
    """
    :attr:`EdgeProvider.NSX_REGISTERED_AVI` specifies the NSX Advanced Load
    Balancer (Avi Load Balancer) configured on the NSX manager, specific to
    Supervisors configured with network type
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSX_VPC`
    or
    :attr:`com.vmware.vcenter.namespace_management.supervisors.networks.workload_client.NetworkType.NSXT`.
    This class attribute was added in **vSphere API 9.0.0.0**.

    """
    VSPHERE_FOUNDATION = None
    """


    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`EdgeProvider` instance.
        """
        Enum.__init__(string)

EdgeProvider._set_values({
    'AVI': EdgeProvider('AVI'),
    'HAPROXY': EdgeProvider('HAPROXY'),
    'NSX_LB': EdgeProvider('NSX_LB'),
    'NSX_REGISTERED_AVI': EdgeProvider('NSX_REGISTERED_AVI'),
    'VSPHERE_FOUNDATION': EdgeProvider('VSPHERE_FOUNDATION'),
})
EdgeProvider._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.supervisors.networks.edges.edge_provider',
    EdgeProvider))





class StubFactory(StubFactoryBase):
    _attrs = {
    }

