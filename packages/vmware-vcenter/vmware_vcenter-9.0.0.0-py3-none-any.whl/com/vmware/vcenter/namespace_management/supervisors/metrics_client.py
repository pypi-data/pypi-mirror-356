# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.namespace_management.supervisors.metrics.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.namespace_management.supervisors.metrics_client``
module provides classes related to metrics collection for one or more
Supervisors.

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

class RemoteEndpointType(Enum):
    """
    The ``RemoteEndpointType`` enumerates types of remote endpoints supported
    by the Supervisor for sending metrics.
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
    HTTP = None
    """
    Indicates HTTP/HTTPS based remote endpoint.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`RemoteEndpointType` instance.
        """
        Enum.__init__(string)

RemoteEndpointType._set_values({
    'HTTP': RemoteEndpointType('HTTP'),
})
RemoteEndpointType._set_binding_type(type.EnumType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoint_type',
    RemoteEndpointType))




class HttpHeader(VapiStruct):
    """
    The ``HttpHeader`` class represents an HTTP header, consisting of a name
    and its associated value.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 value=None,
                ):
        """
        :type  name: :class:`str`
        :param name: HTTP header name.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  value: :class:`str`
        :param value: HTTP header value.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.name = name
        self.value = value
        VapiStruct.__init__(self)


HttpHeader._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.http_header', {
        'name': type.StringType(),
        'value': type.StringType(),
    },
    HttpHeader,
    False,
    None))



class TlsClientConfigInfo(VapiStruct):
    """
    The ``TlsClientConfigInfo`` class contains TLS configuration used by the
    Supervisor when sending metrics to a remote endpoint.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 certificate_authority_chain=None,
                 client_certificate=None,
                ):
        """
        :type  certificate_authority_chain: :class:`str` or ``None``
        :param certificate_authority_chain: Certificate authority chain holds the trusted roots to be used to
            establish HTTPS connections with the with the remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, HTTPS connections with the remote endpoint will rely on a
            default set of system trusted roots.
        :type  client_certificate: :class:`str` or ``None``
        :param client_certificate: A PEM-encoded x509 certificate used by the Supervisor for TLS
            authentication when sending metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, TLS communication with the remote endpoint will not be
            enabled.
        """
        self.certificate_authority_chain = certificate_authority_chain
        self.client_certificate = client_certificate
        VapiStruct.__init__(self)


TlsClientConfigInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.tls_client_config_info', {
        'certificate_authority_chain': type.OptionalType(type.StringType()),
        'client_certificate': type.OptionalType(type.StringType()),
    },
    TlsClientConfigInfo,
    False,
    None))



class TlsClientConfigCreateSpec(VapiStruct):
    """
    The ``TlsClientConfigCreateSpec`` class contains TLS configuration used by
    the Supervisor when sending metrics to a remote endpoint.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 certificate_authority_chain=None,
                 client_certificate=None,
                 client_private_key=None,
                ):
        """
        :type  certificate_authority_chain: :class:`str` or ``None``
        :param certificate_authority_chain: Certificate authority chain holds the trusted roots to be used to
            establish HTTPS connections with the remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, HTTPS connections with the remote endpoint will rely on a
            default set of system trusted roots.
        :type  client_certificate: :class:`str` or ``None``
        :param client_certificate: A PEM-encoded x509 certificate used by the Supervisor for TLS
            authentication when sending metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, TLS communication with the remote endpoint will not be
            enabled.
        :type  client_private_key: :class:`str` or ``None``
        :param client_private_key: Private key associated with the
            :attr:`TlsClientConfigCreateSpec.client_certificate`.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, TLS communication with the remote endpoint will not be
            enabled.
        """
        self.certificate_authority_chain = certificate_authority_chain
        self.client_certificate = client_certificate
        self.client_private_key = client_private_key
        VapiStruct.__init__(self)


TlsClientConfigCreateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.tls_client_config_create_spec', {
        'certificate_authority_chain': type.OptionalType(type.StringType()),
        'client_certificate': type.OptionalType(type.StringType()),
        'client_private_key': type.OptionalType(type.SecretType()),
    },
    TlsClientConfigCreateSpec,
    False,
    None))



class TlsClientConfigUpdateSpec(VapiStruct):
    """
    The ``TlsClientConfigUpdateSpec`` class contains TLS configuration used by
    the Supervisor when sending metrics to a remote endpoint.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 certificate_authority_chain=None,
                 client_certificate=None,
                 client_private_key=None,
                ):
        """
        :type  certificate_authority_chain: :class:`str` or ``None``
        :param certificate_authority_chain: Certificate authority chain holds the trusted roots to be used to
            establish HTTPS connections with the remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, certificate authority data will not be modified.
        :type  client_certificate: :class:`str` or ``None``
        :param client_certificate: A PEM-encoded x509 certificate used by the Supervisor for TLS
            authentication when sending metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, certificate will not be modified.
        :type  client_private_key: :class:`str` or ``None``
        :param client_private_key: Private key associated with the
            :attr:`TlsClientConfigUpdateSpec.client_certificate`.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, private key will not be modified.
        """
        self.certificate_authority_chain = certificate_authority_chain
        self.client_certificate = client_certificate
        self.client_private_key = client_private_key
        VapiStruct.__init__(self)


TlsClientConfigUpdateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.tls_client_config_update_spec', {
        'certificate_authority_chain': type.OptionalType(type.StringType()),
        'client_certificate': type.OptionalType(type.StringType()),
        'client_private_key': type.OptionalType(type.SecretType()),
    },
    TlsClientConfigUpdateSpec,
    False,
    None))



class TlsClientConfigSetSpec(VapiStruct):
    """
    The ``TlsClientConfigSetSpec`` class represents TLS configuration used by
    the Supervisor when sending metrics to remote endpoint.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 certificate_authority_chain=None,
                 client_certificate=None,
                 client_private_key=None,
                ):
        """
        :type  certificate_authority_chain: :class:`str` or ``None``
        :param certificate_authority_chain: Certificate authority chain holds the trusted roots to be used to
            establish HTTPS connections with the remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, HTTPS connections with the remote endpoint will rely on a
            default set of system trusted roots.
        :type  client_certificate: :class:`str` or ``None``
        :param client_certificate: A PEM-encoded x509 certificate used by the Supervisor for TLS
            authentication when sending metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, TLS communication with the remote endpoint will not be
            enabled.
        :type  client_private_key: :class:`str` or ``None``
        :param client_private_key: Private key associated with the
            :attr:`TlsClientConfigSetSpec.client_certificate`.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, TLS communication with the remote endpoint will not be
            enabled.
        """
        self.certificate_authority_chain = certificate_authority_chain
        self.client_certificate = client_certificate
        self.client_private_key = client_private_key
        VapiStruct.__init__(self)


TlsClientConfigSetSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.tls_client_config_set_spec', {
        'certificate_authority_chain': type.OptionalType(type.StringType()),
        'client_certificate': type.OptionalType(type.StringType()),
        'client_private_key': type.OptionalType(type.SecretType()),
    },
    TlsClientConfigSetSpec,
    False,
    None))



class HttpRemoteEndpointInfo(VapiStruct):
    """
    The ``HttpRemoteEndpointInfo`` class contains information about the
    parameters used to configure Supervisor for sending metrics to a remote
    endpoint via HTTP messages.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 url=None,
                 tls_client_config=None,
                 http_headers=None,
                ):
        """
        :type  url: :class:`str`
        :param url: URL of the remote endpoint where Supervisor should send metrics.
            This can be an HTTP or HTTPS URL, following the format
            http(s)://server.com/path/to/metrics.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  tls_client_config: :class:`TlsClientConfigInfo` or ``None``
        :param tls_client_config: TLS client configuration information used by Supervisor for sending
            metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, Supervisor will not use TLS communication with the remote
            endpoint when sending metrics.
        :type  http_headers: :class:`list` of :class:`HttpHeader` or ``None``
        :param http_headers: HTTP headers to be added when the Supervisor sends metrics to the
            remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no HTTP headers are added when sending metrics to the
            remote endpoint.
        """
        self.url = url
        self.tls_client_config = tls_client_config
        self.http_headers = http_headers
        VapiStruct.__init__(self)


HttpRemoteEndpointInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.http_remote_endpoint_info', {
        'url': type.StringType(),
        'tls_client_config': type.OptionalType(type.ReferenceType(__name__, 'TlsClientConfigInfo')),
        'http_headers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'HttpHeader'))),
    },
    HttpRemoteEndpointInfo,
    False,
    None))



class HttpRemoteEndpointCreateSpec(VapiStruct):
    """
    The ``HttpRemoteEndpointCreateSpec`` class is used for configuring the
    Supervisor to send metrics to a remote endpoint in a HTTP message.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 url=None,
                 tls_client_config=None,
                 http_headers=None,
                ):
        """
        :type  url: :class:`str`
        :param url: URL of the remote endpoint where Supervisor should send metrics.
            This can be an HTTP or HTTPS URL, following the format
            http(s)://server.com/path/to/metrics.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  tls_client_config: :class:`TlsClientConfigCreateSpec` or ``None``
        :param tls_client_config: TLS client configuration information used by Supervisor for sending
            metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, Supervisor will not use TLS communication with the remote
            endpoint when sending metrics.
        :type  http_headers: :class:`list` of :class:`HttpHeader` or ``None``
        :param http_headers: HTTP headers to be added when the Supervisor sends metrics to the
            remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no HTTP headers will be added when sending metrics to the
            remote endpoint.
        """
        self.url = url
        self.tls_client_config = tls_client_config
        self.http_headers = http_headers
        VapiStruct.__init__(self)


HttpRemoteEndpointCreateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.http_remote_endpoint_create_spec', {
        'url': type.StringType(),
        'tls_client_config': type.OptionalType(type.ReferenceType(__name__, 'TlsClientConfigCreateSpec')),
        'http_headers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'HttpHeader'))),
    },
    HttpRemoteEndpointCreateSpec,
    False,
    None))



class HttpRemoteEndpointUpdateSpec(VapiStruct):
    """
    The ``HttpRemoteEndpointUpdateSpec`` class is used to modify the Supervisor
    configuration for sending metrics to a remote endpoint in a HTTP message.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 url=None,
                 tls_client_config=None,
                 http_headers=None,
                ):
        """
        :type  url: :class:`str` or ``None``
        :param url: URL of the remote endpoint where Supervisor should send metrics.
            This can be an HTTP or HTTPS URL, following the format
            http(s)://server.com/path/to/metrics.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, URL will be unchanged.
        :type  tls_client_config: :class:`TlsClientConfigUpdateSpec` or ``None``
        :param tls_client_config: TLS client configuration information used by Supervisor for sending
            metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, the TLS configuration will remain unchanged.
        :type  http_headers: :class:`list` of :class:`HttpHeader` or ``None``
        :param http_headers: HTTP headers to be added when the Supervisor sends metrics to the
            remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, HTTP headers will not be modified.
        """
        self.url = url
        self.tls_client_config = tls_client_config
        self.http_headers = http_headers
        VapiStruct.__init__(self)


HttpRemoteEndpointUpdateSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.http_remote_endpoint_update_spec', {
        'url': type.OptionalType(type.StringType()),
        'tls_client_config': type.OptionalType(type.ReferenceType(__name__, 'TlsClientConfigUpdateSpec')),
        'http_headers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'HttpHeader'))),
    },
    HttpRemoteEndpointUpdateSpec,
    False,
    None))



class HttpRemoteEndpointSetSpec(VapiStruct):
    """
    The ``HttpRemoteEndpointUpdateSpec`` class is used to fully replace the
    Supervisor configuration for sending metrics to a remote endpoint in a HTTP
    message.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 url=None,
                 tls_client_config=None,
                 http_headers=None,
                ):
        """
        :type  url: :class:`str`
        :param url: URL of the remote endpoint where Supervisor should send metrics.
            This can be an HTTP or HTTPS URL, following the format
            http(s)://server.com/path/to/metrics.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  tls_client_config: :class:`TlsClientConfigSetSpec` or ``None``
        :param tls_client_config: TLS client configuration information used by Supervisor for sending
            metrics to a remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, Supervisor will not use TLS communication with the remote
            endpoint when sending metrics.
        :type  http_headers: :class:`list` of :class:`HttpHeader` or ``None``
        :param http_headers: HTTP headers to be added when the Supervisor sends metrics to the
            remote endpoint.
            This attribute was added in **vSphere API 9.0.0.0**.
            If None, no HTTP headers will be added when sending metrics to the
            remote endpoint.
        """
        self.url = url
        self.tls_client_config = tls_client_config
        self.http_headers = http_headers
        VapiStruct.__init__(self)


HttpRemoteEndpointSetSpec._set_binding_type(type.StructType(
    'com.vmware.vcenter.namespace_management.supervisors.metrics.http_remote_endpoint_set_spec', {
        'url': type.StringType(),
        'tls_client_config': type.OptionalType(type.ReferenceType(__name__, 'TlsClientConfigSetSpec')),
        'http_headers': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'HttpHeader'))),
    },
    HttpRemoteEndpointSetSpec,
    False,
    None))



class RemoteEndpoints(VapiInterface):
    """
    The ``RemoteEndpoints`` class provides methods for configuring remote
    endpoints that enable Supervisor to send both Supervisor and Workload
    metrics.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _RemoteEndpointsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``RemoteEndpoints.Info`` class details about the parameters used for
        configuring the Supervisor to send metrics to a remote endpoint.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'remote_endpoint_type',
                {
                    'HTTP' : [('http_remote_endpoint', True)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     interval=None,
                     remote_endpoint_type=None,
                     http_remote_endpoint=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A display name to be used for the given remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  interval: :class:`long`
            :param interval: The frequency, in seconds, at which the Supervisor sends metrics to
                the remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  remote_endpoint_type: :class:`RemoteEndpointType`
            :param remote_endpoint_type: Describes the type of remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  http_remote_endpoint: :class:`HttpRemoteEndpointInfo`
            :param http_remote_endpoint: Defines the HTTP or HTTPS remote endpoint configuration for
                Supervisor to send metrics.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``remoteEndpointType`` is :attr:`RemoteEndpointType.HTTP`.
            """
            self.name = name
            self.interval = interval
            self.remote_endpoint_type = remote_endpoint_type
            self.http_remote_endpoint = http_remote_endpoint
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.info', {
            'name': type.StringType(),
            'interval': type.IntegerType(),
            'remote_endpoint_type': type.ReferenceType(__name__, 'RemoteEndpointType'),
            'http_remote_endpoint': type.OptionalType(type.ReferenceType(__name__, 'HttpRemoteEndpointInfo')),
        },
        Info,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``RemoteEndpoints.Summary`` class provides an overview of the remote
        endpoint configured for a Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     remote_endpoint=None,
                     name=None,
                     remote_endpoint_type=None,
                    ):
            """
            :type  remote_endpoint: :class:`str`
            :param remote_endpoint: The immutable identifier of a remote endpoint generated when a
                remote endpoint is registered with a Supervisor.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type:
                ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
            :type  name: :class:`str`
            :param name: A display name to be used for the given remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  remote_endpoint_type: :class:`RemoteEndpointType`
            :param remote_endpoint_type: Describes the type of remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.remote_endpoint = remote_endpoint
            self.name = name
            self.remote_endpoint_type = remote_endpoint_type
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.summary', {
            'remote_endpoint': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
            'name': type.StringType(),
            'remote_endpoint_type': type.ReferenceType(__name__, 'RemoteEndpointType'),
        },
        Summary,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``RemoteEndpoints.ListResult`` class represents the result of a
        :func:`RemoteEndpoints.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     remote_endpoints=None,
                    ):
            """
            :type  remote_endpoints: :class:`list` of :class:`RemoteEndpoints.Summary`
            :param remote_endpoints: List of {#link Summary}.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.remote_endpoints = remote_endpoints
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.list_result', {
            'remote_endpoints': type.ListType(type.ReferenceType(__name__, 'RemoteEndpoints.Summary')),
        },
        ListResult,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``RemoteEndpoints.CreateSpec`` class is used to configure a new remote
        endpoint with the Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'remote_endpoint_type',
                {
                    'HTTP' : [('http_remote_endpoint', True)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     interval=None,
                     remote_endpoint_type=None,
                     http_remote_endpoint=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A display name to be used for the given remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  interval: :class:`long` or ``None``
            :param interval: The frequency, in seconds, at which the Supervisor sends metrics to
                the remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the frequency, will default to 60 seconds.
            :type  remote_endpoint_type: :class:`RemoteEndpointType`
            :param remote_endpoint_type: Describes the type of remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  http_remote_endpoint: :class:`HttpRemoteEndpointCreateSpec`
            :param http_remote_endpoint: Defines the HTTP or HTTPS remote endpoint configuration for
                Supervisor to send metrics.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``remoteEndpointType`` is :attr:`RemoteEndpointType.HTTP`.
            """
            self.name = name
            self.interval = interval
            self.remote_endpoint_type = remote_endpoint_type
            self.http_remote_endpoint = http_remote_endpoint
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.create_spec', {
            'name': type.StringType(),
            'interval': type.OptionalType(type.IntegerType()),
            'remote_endpoint_type': type.ReferenceType(__name__, 'RemoteEndpointType'),
            'http_remote_endpoint': type.OptionalType(type.ReferenceType(__name__, 'HttpRemoteEndpointCreateSpec')),
        },
        CreateSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``RemoteEndpoints.UpdateSpec`` class contains the specification
        required to update the configuration of a remote endpoint configured with
        the Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'remote_endpoint_type',
                {
                    'HTTP' : [('http_remote_endpoint', False)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     interval=None,
                     remote_endpoint_type=None,
                     http_remote_endpoint=None,
                    ):
            """
            :type  name: :class:`str` or ``None``
            :param name: A display name to be used for the given remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote endpoint name will not be modified.
            :type  interval: :class:`long` or ``None``
            :param interval: The frequency, in seconds, at which the Supervisor sends metrics to
                the remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, interval will not be modified.
            :type  remote_endpoint_type: :class:`RemoteEndpointType` or ``None``
            :param remote_endpoint_type: Describes the type of remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote endpoint configuration will not be modified.
            :type  http_remote_endpoint: :class:`HttpRemoteEndpointUpdateSpec` or ``None``
            :param http_remote_endpoint: Defines the HTTP or HTTPS remote endpoint configuration for
                Supervisor to send metrics.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote endpoint configuration will not be modified.
            """
            self.name = name
            self.interval = interval
            self.remote_endpoint_type = remote_endpoint_type
            self.http_remote_endpoint = http_remote_endpoint
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.update_spec', {
            'name': type.OptionalType(type.StringType()),
            'interval': type.OptionalType(type.IntegerType()),
            'remote_endpoint_type': type.OptionalType(type.ReferenceType(__name__, 'RemoteEndpointType')),
            'http_remote_endpoint': type.OptionalType(type.ReferenceType(__name__, 'HttpRemoteEndpointUpdateSpec')),
        },
        UpdateSpec,
        False,
        None))


    class SetSpec(VapiStruct):
        """
        The ``RemoteEndpoints.SetSpec`` class contains the specification required
        to fully replace the configuration of a remote endpoint configured with the
        Supervisor.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'remote_endpoint_type',
                {
                    'HTTP' : [('http_remote_endpoint', True)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     interval=None,
                     remote_endpoint_type=None,
                     http_remote_endpoint=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: A display name to be used for the given remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  interval: :class:`long` or ``None``
            :param interval: The frequency, in seconds, at which the Supervisor sends metrics to
                the remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the frequency, will default to 60 seconds.
            :type  remote_endpoint_type: :class:`RemoteEndpointType`
            :param remote_endpoint_type: Describes the type of remote endpoint.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  http_remote_endpoint: :class:`HttpRemoteEndpointSetSpec`
            :param http_remote_endpoint: Defines the HTTP or HTTPS remote endpoint configuration for
                Supervisor to send metrics.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``remoteEndpointType`` is :attr:`RemoteEndpointType.HTTP`.
            """
            self.name = name
            self.interval = interval
            self.remote_endpoint_type = remote_endpoint_type
            self.http_remote_endpoint = http_remote_endpoint
            VapiStruct.__init__(self)


    SetSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints.set_spec', {
            'name': type.StringType(),
            'interval': type.OptionalType(type.IntegerType()),
            'remote_endpoint_type': type.ReferenceType(__name__, 'RemoteEndpointType'),
            'http_remote_endpoint': type.OptionalType(type.ReferenceType(__name__, 'HttpRemoteEndpointSetSpec')),
        },
        SetSpec,
        False,
        None))



    def get(self,
            supervisor,
            remote_endpoint,
            ):
        """
        Returns information about a remote endpoint configured for a
        Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier for the Supervisor for which the remote endpoint is
            being retrieved.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  remote_endpoint: :class:`str`
        :param remote_endpoint: identifier of the remote endpoint that is being retrieved.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
        :rtype: :class:`RemoteEndpoints.Info`
        :return: An {#link Info} representing the requested remote endpoint.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the given ``remote_endpoint`` or ``supervisor`` cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the System.Read privilege on the Supervisor.
        """
        return self._invoke('get',
                            {
                            'supervisor': supervisor,
                            'remote_endpoint': remote_endpoint,
                            })

    def list(self,
             supervisor,
             ):
        """
        Retrieve a list of remote endpoints configured for a Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier for the Supervisor for which the remote endpoints are
            being retrieved.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :rtype: :class:`RemoteEndpoints.ListResult`
        :return: A list of {#link ListResult} with details about the remote
            endpoints configured for a Supervisor.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the given ``supervisor`` cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the System.Read privilege on the Supervisor.
        """
        return self._invoke('list',
                            {
                            'supervisor': supervisor,
                            })

    def create(self,
               supervisor,
               spec,
               ):
        """
        Configure a new remote endpoint for the Supervisor to send both
        Supervisor and Workload cluster metrics.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier of the Supervisor for which the remote endpoint is being
            created.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  spec: :class:`RemoteEndpoints.CreateSpec`
        :param spec: the {#link CreateSpec} describing the remote endpoint to be
            created.
        :rtype: :class:`str`
        :return: a unique identifier for the remote endpoint that was created.
            The return value will be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``spec`` contains any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            if the specified ``supervisor`` does not exist.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the Namespaces.Manage privilege on the
            Supervisor.
        """
        return self._invoke('create',
                            {
                            'supervisor': supervisor,
                            'spec': spec,
                            })

    def update(self,
               supervisor,
               remote_endpoint,
               spec,
               ):
        """
        Modify an existing remote endpoint configuration used by a Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier for the Supervisor for which the remote endpoint is
            being modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  remote_endpoint: :class:`str`
        :param remote_endpoint: identifier for the remote endpoint that is being modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
        :type  spec: :class:`RemoteEndpoints.UpdateSpec`
        :param spec: the {#UpdateSpec} to be applied to the remote endpoint
            configuration.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``spec`` contains any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the given ``remote_endpoint`` or ``supervisor`` cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the Namespaces.Manage privilege on the
            Supervisor.
        """
        return self._invoke('update',
                            {
                            'supervisor': supervisor,
                            'remote_endpoint': remote_endpoint,
                            'spec': spec,
                            })

    def set(self,
            supervisor,
            remote_endpoint,
            spec,
            ):
        """
        Modify the complete remote endpoint configuration used by a Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier for the Supervisor for which the remote endpoint is
            being modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  remote_endpoint: :class:`str`
        :param remote_endpoint: identifier for the remote endpoint that is being modified.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
        :type  spec: :class:`RemoteEndpoints.SetSpec`
        :param spec: the {#SetSpec} to be applied to the remote endpoint configuration.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if the ``spec`` contains any errors.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the given ``remote_endpoint`` or ``supervisor`` cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the Namespaces.Manage privilege on the
            Supervisor.
        """
        return self._invoke('set',
                            {
                            'supervisor': supervisor,
                            'remote_endpoint': remote_endpoint,
                            'spec': spec,
                            })

    def delete(self,
               supervisor,
               remote_endpoint,
               ):
        """
        Delete a remote endpoint configured for a Supervisor.
        This method was added in **vSphere API 9.0.0.0**.

        :type  supervisor: :class:`str`
        :param supervisor: identifier for the Supervisor for which the remote endpoint is
            being deleted.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.Supervisor``.
        :type  remote_endpoint: :class:`str`
        :param remote_endpoint: identifier for the remote endpoint that is being deleted.
            The parameter must be an identifier for the resource type:
            ``com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the given ``remote_endpoint`` or ``supervisor`` cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user cannot be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user is missing the Namespaces.Manage privilege on the
            Supervisor.
        """
        return self._invoke('delete',
                            {
                            'supervisor': supervisor,
                            'remote_endpoint': remote_endpoint,
                            })
class _RemoteEndpointsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'remote_endpoint': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints/{remoteEndpoint}',
            path_variables={
                'supervisor': 'supervisor',
                'remote_endpoint': 'remoteEndpoint',
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
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints',
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

        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'spec': type.ReferenceType(__name__, 'RemoteEndpoints.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints',
            request_body_parameter='spec',
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

        # properties for update operation
        update_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'remote_endpoint': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
            'spec': type.ReferenceType(__name__, 'RemoteEndpoints.UpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints/{remoteEndpoint}',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
                'remote_endpoint': 'remoteEndpoint',
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

        # properties for set operation
        set_input_type = type.StructType('operation-input', {
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'remote_endpoint': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
            'spec': type.ReferenceType(__name__, 'RemoteEndpoints.SetSpec'),
        })
        set_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        set_input_value_validator_list = [
        ]
        set_output_validator_list = [
        ]
        set_rest_metadata = OperationRestMetadata(
            http_method='PUT',
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints/{remoteEndpoint}',
            request_body_parameter='spec',
            path_variables={
                'supervisor': 'supervisor',
                'remote_endpoint': 'remoteEndpoint',
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
            'supervisor': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.Supervisor'),
            'remote_endpoint': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/vcenter/namespace-management/supervisors/{supervisor}/metrics/remote-endpoints/{remoteEndpoint}',
            path_variables={
                'supervisor': 'supervisor',
                'remote_endpoint': 'remoteEndpoint',
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
                'output_type': type.ReferenceType(__name__, 'RemoteEndpoints.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'RemoteEndpoints.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.vcenter.namespace_management.supervisor.metrics.RemoteEndpoint'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update': {
                'input_type': update_input_type,
                'output_type': type.VoidType(),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': update_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'set': {
                'input_type': set_input_type,
                'output_type': type.VoidType(),
                'errors': set_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': set_input_value_validator_list,
                'output_validator_list': set_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'get': get_rest_metadata,
            'list': list_rest_metadata,
            'create': create_rest_metadata,
            'update': update_rest_metadata,
            'set': set_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.namespace_management.supervisors.metrics.remote_endpoints',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'RemoteEndpoints': RemoteEndpoints,
    }

