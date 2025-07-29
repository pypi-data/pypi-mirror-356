# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.tagging.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.tagging_client`` module provides classes for managing
tags.

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


class Associations(VapiInterface):
    """
    The ``Associations`` class provides methods to list tag associations.
    This class was added in **vSphere API 7.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.tagging.associations'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _AssociationsStub)
        self._VAPI_OPERATION_IDS = {}

    class LastIterationStatus(Enum):
        """
        The last status for the iterator. A field of this type is returned as part
        of the result and indicates to the caller of the API whether it can
        continue to make requests for more data. 
        
        The last status only reports on the state of the iteration at the time data
        was last returned. As a result, it not does guarantee if the next call will
        succeed in getting more data or not. 
        
        Failures to retrieve results will be returned as Error responses. These
        last statuses are only returned when the iterator is operating as expected.
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
        READY = None
        """
        Iterator has more data pending and is ready to provide it. The caller can
        request the next page of data at any time. 
        
        The number of results returned may be less than the usual size. In other
        words, the iterator may not fill the page. The iterator has returned at
        least 1 result.

        """
        END_OF_DATA = None
        """
        Iterator has finished iterating through its inventory. There are currently
        no more entities to return and the caller can terminate iteration. If the
        iterator returned some data, the marker may be set to allow the iterator to
        continue from where it left off when additional data does become available.
        This value is used to indicate that all available data has been returned by
        the iterator.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`LastIterationStatus` instance.
            """
            Enum.__init__(string)

    LastIterationStatus._set_values({
        'READY': LastIterationStatus('READY'),
        'END_OF_DATA': LastIterationStatus('END_OF_DATA'),
    })
    LastIterationStatus._set_binding_type(type.EnumType(
        'com.vmware.vcenter.tagging.associations.last_iteration_status',
        LastIterationStatus))


    class IterationSpec(VapiStruct):
        """
        The ``Associations.IterationSpec`` class contains attributes used to break
        results into pages when listing tags associated to objects see
        :func:`Associations.list`).
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque token that allows the caller to request the
                next page of tag associations.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``.
                If None or empty, first page of tag associations will be returned.
            """
            self.marker = marker
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.iteration_spec', {
            'marker': type.OptionalType(type.IdType()),
        },
        IterationSpec,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Associations.Summary`` describes a tag association.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tag=None,
                     object=None,
                    ):
            """
            :type  tag: :class:`str`
            :param tag: The identifier of a tag.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.tagging.Tag``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.cis.tagging.Tag``.
            :type  object: :class:`com.vmware.vapi.std_client.DynamicID`
            :param object: The identifier of an associated object.
                This attribute was added in **vSphere API 7.0.0.0**.
            """
            self.tag = tag
            self.object = object
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.summary', {
            'tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag'),
            'object': type.ReferenceType('com.vmware.vapi.std_client', 'DynamicID'),
        },
        Summary,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Associations.ListResult`` class contains the list of tag associations
        in a page, as well as related metadata fields.
        This class was added in **vSphere API 7.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     associations=None,
                     marker=None,
                     status=None,
                    ):
            """
            :type  associations: :class:`list` of :class:`Associations.Summary`
            :param associations: List of tag associations.
                This attribute was added in **vSphere API 7.0.0.0**.
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of tag associations.
                This attribute was added in **vSphere API 7.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.vcenter.tagging.associations.Marker``.
                If None or empty, there are no more tag associations to request.
            :type  status: :class:`Associations.LastIterationStatus`
            :param status: The last status for the iterator that indicates whether any more
                results can be expected if the caller continues to make requests
                for more data using the iterator.
                This attribute was added in **vSphere API 7.0.0.0**.
            """
            self.associations = associations
            self.marker = marker
            self.status = status
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.associations.list_result', {
            'associations': type.ListType(type.ReferenceType(__name__, 'Associations.Summary')),
            'marker': type.OptionalType(type.IdType()),
            'status': type.ReferenceType(__name__, 'Associations.LastIterationStatus'),
        },
        ListResult,
        False,
        None))



    def list(self,
             iterate=None,
             ):
        """
        Returns tag associations that match the specified iteration spec.
        This method was added in **vSphere API 7.0.0.0**.

        :type  iterate: :class:`Associations.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Associations.ListResult`
        :return: A page of the tag associations matching the iteration spec.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if :attr:`Associations.IterationSpec.marker` is not a marker
            returned from an earlier invocation of this {\\\\@term operation).
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'iterate': iterate,
                            })
class Categories(VapiInterface):
    """
    The ``Categories`` class provides functionality to list categories.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.tagging.categories'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _CategoriesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Categories.Info`` class contains the category Name
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     description=None,
                     cardinality=None,
                     associable_types=None,
                     used_by=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the category.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  description: :class:`str`
            :param description: The description of the category.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cardinality: :class:`Categories.Info.Cardinality`
            :param cardinality: The associated cardinality (SINGLE, MULTIPLE) of the category.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  associable_types: :class:`set` of :class:`str`
            :param associable_types: The types of objects that the tags in this category can be attached
                to. If the :class:`set` is empty, then tags can be attached to all
                types of objects.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  used_by: :class:`set` of :class:`str`
            :param used_by: The :class:`set` of users that can use this category.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.description = description
            self.cardinality = cardinality
            self.associable_types = associable_types
            self.used_by = used_by
            VapiStruct.__init__(self)


        class Cardinality(Enum):
            """
            The ``Categories.Info.Cardinality`` class defines the number of tags in a
            category that can be assigned to an object.
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
            An object can only be assigned one of the tags in this category. For
            example, if a category is "Operating System", then different tags of this
            category would be "Windows", "Linux", and so on. In this case a VM object
            can be assigned only one of these tags and hence the cardinality of the
            associated category here is single.

            """
            MULTIPLE = None
            """
            An object can be assigned several of the tags in this category. For
            example, if a category is "Server", then different tags of this category
            would be "AppServer", "DatabaseServer" and so on. In this case a VM object
            can be assigned more than one of the above tags and hence the cardinality
            of the associated category here is multiple.

            """

            def __init__(self, string):
                """
                :type  string: :class:`str`
                :param string: String value for the :class:`Cardinality` instance.
                """
                Enum.__init__(string)

        Cardinality._set_values({
            'SINGLE': Cardinality('SINGLE'),
            'MULTIPLE': Cardinality('MULTIPLE'),
        })
        Cardinality._set_binding_type(type.EnumType(
            'com.vmware.vcenter.tagging.categories.info.cardinality',
            Cardinality))

    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.categories.info', {
            'name': type.StringType(),
            'description': type.StringType(),
            'cardinality': type.ReferenceType(__name__, 'Categories.Info.Cardinality'),
            'associable_types': type.SetType(type.StringType()),
            'used_by': type.SetType(type.StringType()),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Categories.ListItem`` class contains the category identifier and
        further information about the category.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     category_id=None,
                     info=None,
                    ):
            """
            :type  category_id: :class:`str`
            :param category_id: The identifier of the category.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.tagging.Category``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.cis.tagging.Category``.
            :type  info: :class:`Categories.Info`
            :param info: The information about the category.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.category_id = category_id
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.categories.list_item', {
            'category_id': type.IdType(resource_types='com.vmware.cis.tagging.Category'),
            'info': type.ReferenceType(__name__, 'Categories.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Categories.ListResult`` class contains a set of categories and the
        metadata about them.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                     items=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of categories.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, then all the categories have been returned.
            :type  items: :class:`list` of :class:`Categories.ListItem`
            :param items: List of categories.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.marker = marker
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.categories.list_result', {
            'marker': type.OptionalType(type.StringType()),
            'items': type.ListType(type.ReferenceType(__name__, 'Categories.ListItem')),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Categories.FilterSpec`` class contains attributes used to filter the
        results when listing categories, see :func:`Categories.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     names=None,
                    ):
            """
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Categories need to have a name equal to one of the strings in this
                set to match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, then categories with any name match this filter.
            """
            self.names = names
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.categories.filter_spec', {
            'names': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Categories.IterationSpec`` class contains attributes used to break
        results into pages when listing categories.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                     page_size=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of categories.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the first page of categories will be returned.
            :type  page_size: :class:`long` or ``None``
            :param page_size: Used for pagination to fetch given page size
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, then categories will be fetched with default size of 20.
            """
            self.marker = marker
            self.page_size = page_size
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.categories.iteration_spec', {
            'marker': type.OptionalType(type.StringType()),
            'page_size': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))



    def list(self,
             filter=None,
             iterate=None,
             ):
        """
        Returns categories that match the specified filter and iteration.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Categories.FilterSpec` or ``None``
        :param filter: The specification of matching categories.
            If None, all categories will be returned.
        :type  iterate: :class:`Categories.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Categories.ListResult`
        :return: A page of the categories matching the
            :class:`Categories.FilterSpec` and
            :class:`Categories.IterationSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If marker and filter are supplied together.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the supplied marker value is not valid. For example the marker
            value is too old or not returned from prior call to the API.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the request cannot be completed. The message in the error will
            provide more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            })
class Tags(VapiInterface):
    """
    The \\\\@name Tags \\\\@term service provides functionality to list tags.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.vcenter.tagging.tags'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TagsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``Tags.Info`` class contains the tag Name and Category ID
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     category=None,
                     description=None,
                     used_by=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: The name of the tag.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  category: :class:`str`
            :param category: Category Id
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.tagging.Category``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.cis.tagging.Category``.
            :type  description: :class:`str`
            :param description: The description of the Tag.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  used_by: :class:`set` of :class:`str`
            :param used_by: The :class:`set` of users that can use this Tag.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.category = category
            self.description = description
            self.used_by = used_by
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.tags.info', {
            'name': type.StringType(),
            'category': type.IdType(resource_types='com.vmware.cis.tagging.Category'),
            'description': type.StringType(),
            'used_by': type.SetType(type.StringType()),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Tags.ListItem`` class contains the tag identifier and further
        information about the tag.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tag=None,
                     info=None,
                    ):
            """
            :type  tag: :class:`str`
            :param tag: The identifier of the tag.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.cis.tagging.Tag``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``com.vmware.cis.tagging.Tag``.
            :type  info: :class:`Tags.Info`
            :param info: The information about the tag.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.tag = tag
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.tags.list_item', {
            'tag': type.IdType(resource_types='com.vmware.cis.tagging.Tag'),
            'info': type.ReferenceType(__name__, 'Tags.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Tags.ListResult`` class contains a set of tags and the metadata about
        them.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                     items=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of tags.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, then all the tags have been returned.
            :type  items: :class:`list` of :class:`Tags.ListItem`
            :param items: List of tags.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.marker = marker
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.tags.list_result', {
            'marker': type.OptionalType(type.StringType()),
            'items': type.ListType(type.ReferenceType(__name__, 'Tags.ListItem')),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Tags.FilterSpec`` class contains attributes used to filter the
        results when listing tags, see :func:`Tags.list`).
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     names=None,
                    ):
            """
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Tags need to have a name equal to one of the strings in this set to
                match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, then tags with any name match this filter.
            """
            self.names = names
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.tags.filter_spec', {
            'names': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Tags.IterationSpec`` class contains attributes used to break results
        into pages when listing tags.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     marker=None,
                     page_size=None,
                    ):
            """
            :type  marker: :class:`str` or ``None``
            :param marker: Marker is an opaque data structure that allows the caller to
                request the next page of tags.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, the first page of tags will be returned.
            :type  page_size: :class:`long` or ``None``
            :param page_size: Used for pagination to fetch given page size
                This attribute was added in **vSphere API 9.0.0.0**.
                if None, then tags will be fetched with default page size of 20.
            """
            self.marker = marker
            self.page_size = page_size
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.vcenter.tagging.tags.iteration_spec', {
            'marker': type.OptionalType(type.StringType()),
            'page_size': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))



    def list(self,
             filter=None,
             iterate=None,
             ):
        """
        Returns tags that match the specified filter and iteration.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Tags.FilterSpec` or ``None``
        :param filter: The specification of matching tags.
            If None, all tags will be returned.
        :type  iterate: :class:`Tags.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Tags.ListResult`
        :return: A page of the tags matching the :class:`Tags.FilterSpec` and
            :class:`Tags.IterationSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If marker and filter are supplied together.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the supplied marker value is not valid. For example the marker
            value is too old or not returned from prior call to the API.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If the request cannot be completed. The message in the error will
            provide more details.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            'iterate': iterate,
                            })
class _AssociationsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Associations.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/vcenter/tagging/associations',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Associations.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.tagging.associations',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _CategoriesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Categories.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Categories.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/tagging/categories',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Categories.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.tagging.categories',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TagsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Tags.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Tags.IterationSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
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
            url_template='/vcenter/tagging/tags',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Tags.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.vcenter.tagging.tags',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Associations': Associations,
        'Categories': Categories,
        'Tags': Tags,
    }

