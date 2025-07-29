# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.reports.clusters.protection_groups.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice.reports.clusters.protection_groups_client`` module
provides classes to fetch reports for protection group snapshots.

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


class Snapshots(VapiInterface):
    """
    The ``Snapshots`` provides methods for protection group snapshot reports.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.reports.clusters.protection_groups.snapshots'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SnapshotsStub)
        self._VAPI_OPERATION_IDS = {}

    class Status(Enum):
        """
        The ``Snapshots.Status`` enumeration contains valid statuses for protection
        group snapshot operation.
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
        All VM snapshots in the current protection group are successfully created.

        """
        ERROR = None
        """
        All VM snapshots in current protection group have failed.

        """
        WARNING = None
        """
        Some of the VM snapshots in the current protection group have failed.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`Status` instance.
            """
            Enum.__init__(string)

    Status._set_values({
        'SUCCESS': Status('SUCCESS'),
        'ERROR': Status('ERROR'),
        'WARNING': Status('WARNING'),
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.status',
        Status))


    class FilterSpec(VapiStruct):
        """
        The ``Snapshots.FilterSpec`` class contains attributes used to filter the
        results when listing protection group snapshots for the reports. If
        multiple attributes are specified, only protection group snapshots matching
        all of the attributes match the filter are returned. If the time range is
        not specified, the data existed over the last retention period which is
        used for reporting purpose is returned, by default retention period is set
        to 90 days.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     start_time=None,
                     end_time=None,
                     pgs=None,
                    ):
            """
            :type  start_time: :class:`datetime.datetime` or ``None``
            :param start_time: Start time for the time range for which the snapshot report has to
                be generated.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to 90 days from the current time.
            :type  end_time: :class:`datetime.datetime` or ``None``
            :param end_time: End time for the time range for which the snapshot report has to be
                generated.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to current time.
            :type  pgs: :class:`set` of :class:`str` or ``None``
            :param pgs: Identifiers of protection groups that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``.
                If None or empty, protection groups with any identifier match the
                filter.
            """
            self.start_time = start_time
            self.end_time = end_time
            self.pgs = pgs
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.filter_spec', {
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'pgs': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Snapshots.IterationSpec`` class contains attributes used to break
        results into pages when listing protection group snapshots for report. see
        :func:`Snapshots.list`.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     page_size=None,
                     offset=None,
                    ):
            """
            :type  page_size: :class:`long` or ``None``
            :param page_size: Specifies the maximum number of results to return.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None defaults to a size defined by the service.
            :type  offset: :class:`long` or ``None``
            :param offset: Used to retrieve paged data for larger result sets. The offset
                indicates how many starting elements to be skipped in a sorted list
                of items. If the offset is greater than or equal to the number of
                items in the list, empty response is returned by the server.
                This attribute was added in **vSphere API 9.0.0.0**.
                None the offset will start from 0
            """
            self.page_size = page_size
            self.offset = offset
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.iteration_spec', {
            'page_size': type.OptionalType(type.IntegerType()),
            'offset': type.OptionalType(type.IntegerType()),
        },
        IterationSpec,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Snapshots.ListResult`` class represents the result of
        :func:`Snapshots.list` method. The result list is pre sorted by
        :attr:`Snapshots.ListItem.creation_time` of the protection group snapshot.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     snapshots=None,
                     total_count=None,
                    ):
            """
            :type  snapshots: :class:`list` of :class:`Snapshots.ListItem`
            :param snapshots: List of items
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  total_count: :class:`long`
            :param total_count: The paginated list may contain partial result, this field provides
                total number of items with the given filters applied.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.snapshots = snapshots
            self.total_count = total_count
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.list_result', {
            'snapshots': type.ListType(type.ReferenceType(__name__, 'Snapshots.ListItem')),
            'total_count': type.IntegerType(),
        },
        ListResult,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Snapshots.ListItem`` class contains information about a protection
        group snapshot returned by :func:`Snapshots.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'SUCCESS' : [('snapshot', False), ('snapshot_type', False)],
                    'WARNING' : [('snapshot', False), ('warnings', True), ('snapshot_type', False)],
                    'ERROR' : [('errors', True)],
                }
            ),
        ]



        def __init__(self,
                     pg=None,
                     name=None,
                     snapshot=None,
                     status=None,
                     errors=None,
                     warnings=None,
                     creation_time=None,
                     expiration_time=None,
                     snapshot_type=None,
                     deleted=None,
                    ):
            """
            :type  pg: :class:`str`
            :param pg: ID of the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  name: :class:`str`
            :param name: Name of the protection group snapshot. If no snapshot is available
                for pg due to error, a dummy name will be returned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  snapshot: :class:`str` or ``None``
            :param snapshot: Identifier of the protection group snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group.snapshot``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group.snapshot``.
                If None no snapshot is available for pg due to error.
            :type  status: :class:`Snapshots.Status`
            :param status: Status of the protection group snapshot operation.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  errors: :class:`list` of :class:`com.vmware.snapservice_client.Reason`
            :param errors: List of snapshot operation errors for the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`Snapshots.Status.ERROR`.
            :type  warnings: :class:`list` of :class:`com.vmware.snapservice_client.Reason`
            :param warnings: List of snapshot operation warnings for the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`Snapshots.Status.WARNING`.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Creation time of protection group snapshot. If the snapshot
                operation fails, start time of the operation is returned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  expiration_time: :class:`datetime.datetime` or ``None``
            :param expiration_time: Expiration time of protection group snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None no expiry time is set for the protection group snapshot.
            :type  snapshot_type: :class:`com.vmware.snapservice.clusters.protection_groups_client.Snapshots.Type` or ``None``
            :param snapshot_type: Type of protection group snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None snapshot and its type is not available for pg due to error.
            :type  deleted: :class:`bool`
            :param deleted: Whether the protection group snapshot is deleted.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.pg = pg
            self.name = name
            self.snapshot = snapshot
            self.status = status
            self.errors = errors
            self.warnings = warnings
            self.creation_time = creation_time
            self.expiration_time = expiration_time
            self.snapshot_type = snapshot_type
            self.deleted = deleted
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.list_item', {
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'name': type.StringType(),
            'snapshot': type.OptionalType(type.IdType()),
            'status': type.ReferenceType(__name__, 'Snapshots.Status'),
            'errors': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.snapservice_client', 'Reason'))),
            'warnings': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.snapservice_client', 'Reason'))),
            'creation_time': type.DateTimeType(),
            'expiration_time': type.OptionalType(type.DateTimeType()),
            'snapshot_type': type.OptionalType(type.ReferenceType('com.vmware.snapservice.clusters.protection_groups_client', 'Snapshots.Type')),
            'deleted': type.BooleanType(),
        },
        ListItem,
        False,
        None))


    class StatusByTimeSliceItem(VapiStruct):
        """
        The ``Snapshots.StatusByTimeSliceItem`` class contains information about
        aggregated status count of all the snapshots for the filtered protection
        groups returned by :func:`Snapshots.list_status_aggregated_by_time_slice`
        method for a given time slice.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     start_time=None,
                     end_time=None,
                     info=None,
                    ):
            """
            :type  start_time: :class:`datetime.datetime`
            :param start_time: Start time of the time slice for which the snapshot status count is
                aggregated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  end_time: :class:`datetime.datetime`
            :param end_time: End time of the time slice for which the snapshots status count is
                aggregated.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  info: :class:`Snapshots.AggregatedStatusInfo`
            :param info: Information about aggregated status counts of the snapshots.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.start_time = start_time
            self.end_time = end_time
            self.info = info
            VapiStruct.__init__(self)


    StatusByTimeSliceItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.status_by_time_slice_item', {
            'start_time': type.DateTimeType(),
            'end_time': type.DateTimeType(),
            'info': type.ReferenceType(__name__, 'Snapshots.AggregatedStatusInfo'),
        },
        StatusByTimeSliceItem,
        False,
        None))


    class AggregatedStatusInfo(VapiStruct):
        """
        The ``Snapshots.AggregatedStatusInfo`` class contains information about
        aggregated status counts of the snapshots.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     error_count=None,
                     warning_count=None,
                     success_count=None,
                    ):
            """
            :type  error_count: :class:`long`
            :param error_count: Aggregated count of protection group snapshots with "ERROR" status.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  warning_count: :class:`long`
            :param warning_count: Aggregated count of protection group snapshots with "WARNING"
                status.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  success_count: :class:`long`
            :param success_count: Aggregated count of protection group snapshots with "SUCCESS"
                status.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.error_count = error_count
            self.warning_count = warning_count
            self.success_count = success_count
            VapiStruct.__init__(self)


    AggregatedStatusInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.aggregated_status_info', {
            'error_count': type.IntegerType(),
            'warning_count': type.IntegerType(),
            'success_count': type.IntegerType(),
        },
        AggregatedStatusInfo,
        False,
        None))


    class StatusByTimeSliceListResult(VapiStruct):
        """
        The ``Snapshots.StatusByTimeSliceListResult`` class represents the result
        of :func:`Snapshots.list_status_aggregated_by_time_slice` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Snapshots.StatusByTimeSliceItem`
            :param items: List of status count items aggregated by time slice.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    StatusByTimeSliceListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.status_by_time_slice_list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Snapshots.StatusByTimeSliceItem')),
        },
        StatusByTimeSliceListResult,
        False,
        None))


    class StatusByProtectionGroupItem(VapiStruct):
        """
        The ``Snapshots.StatusByProtectionGroupItem`` class contains information
        about status counts of protection group snapshots aggregated by protection
        group as returned by
        :func:`Snapshots.list_status_aggregated_by_protection_group` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pg=None,
                     info=None,
                    ):
            """
            :type  pg: :class:`str`
            :param pg: ID of the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  info: :class:`Snapshots.AggregatedStatusInfo`
            :param info: Information about aggregated status counts of the snapshots.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.pg = pg
            self.info = info
            VapiStruct.__init__(self)


    StatusByProtectionGroupItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.status_by_protection_group_item', {
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'info': type.ReferenceType(__name__, 'Snapshots.AggregatedStatusInfo'),
        },
        StatusByProtectionGroupItem,
        False,
        None))


    class StatusByProtectionGroupListResult(VapiStruct):
        """
        The ``Snapshots.StatusByProtectionGroupListResult`` class represents the
        result of :func:`Snapshots.list_status_aggregated_by_protection_group`
        method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Snapshots.StatusByProtectionGroupItem`
            :param items: List of status count items aggregated by protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    StatusByProtectionGroupListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.snapshots.status_by_protection_group_list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Snapshots.StatusByProtectionGroupItem')),
        },
        StatusByProtectionGroupListResult,
        False,
        None))



    def list(self,
             cluster,
             filter=None,
             iterate=None,
             ):
        """
        Paginated list of protection group snapshots for the given cluster used
        for reports which contains historical data.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the list result.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all protection groups match the filter.
        :type  iterate: :class:`Snapshots.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Snapshots.ListResult`
        :return: List of protection group snapshots for report matching the
            :class:`Snapshots.FilterSpec` for the given cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``filter`` or ``iterate`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'filter': filter,
                            'iterate': iterate,
                            })

    def list_status_aggregated_by_time_slice(self,
                                             cluster,
                                             filter=None,
                                             ):
        """
        Get the aggregated status counts of all the snapshots for all the
        filtered protection groups for a given cluster time sliced as defined
        by the service.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the result list.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all protection groups match the filter.
        :rtype: :class:`Snapshots.StatusByTimeSliceListResult`
        :return: List of aggregated counts for protection group snapshot statuses
            for report matching the :class:`Snapshots.FilterSpec` for the given
            cluster.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``filter`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        """
        return self._invoke('list_status_aggregated_by_time_slice',
                            {
                            'cluster': cluster,
                            'filter': filter,
                            })

    def list_status_aggregated_by_protection_group(self,
                                                   cluster,
                                                   filter=None,
                                                   ):
        """
        Get the status counts of protection group snapshots aggregated by
        protection group.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the list result.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all protection groups match the filter.
        :rtype: :class:`Snapshots.StatusByProtectionGroupListResult`
        :return: status counts of protection group snapshots aggregated by
            protection group.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If no cluster associated with ``cluster`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If any input is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        """
        return self._invoke('list_status_aggregated_by_protection_group',
                            {
                            'cluster': cluster,
                            'filter': filter,
                            })
class _SnapshotsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Snapshots.FilterSpec')),
            'iterate': type.OptionalType(type.ReferenceType(__name__, 'Snapshots.IterationSpec')),
        })
        list_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/protection-groups/snapshots',
            path_variables={
                'cluster': 'cluster',
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

        # properties for list_status_aggregated_by_time_slice operation
        list_status_aggregated_by_time_slice_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Snapshots.FilterSpec')),
        })
        list_status_aggregated_by_time_slice_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_status_aggregated_by_time_slice_input_value_validator_list = [
        ]
        list_status_aggregated_by_time_slice_output_validator_list = [
        ]
        list_status_aggregated_by_time_slice_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/protection-groups/snapshot-status-counts?aggregateBy=time-slice',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'aggregateBy': 'time-slice',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for list_status_aggregated_by_protection_group operation
        list_status_aggregated_by_protection_group_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Snapshots.FilterSpec')),
        })
        list_status_aggregated_by_protection_group_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        list_status_aggregated_by_protection_group_input_value_validator_list = [
        ]
        list_status_aggregated_by_protection_group_output_validator_list = [
        ]
        list_status_aggregated_by_protection_group_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/protection-groups/snapshot-status-counts?aggregateBy=protection-group',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'aggregateBy': 'protection-group',
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
                'output_type': type.ReferenceType(__name__, 'Snapshots.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list_status_aggregated_by_time_slice': {
                'input_type': list_status_aggregated_by_time_slice_input_type,
                'output_type': type.ReferenceType(__name__, 'Snapshots.StatusByTimeSliceListResult'),
                'errors': list_status_aggregated_by_time_slice_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_status_aggregated_by_time_slice_input_value_validator_list,
                'output_validator_list': list_status_aggregated_by_time_slice_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'list_status_aggregated_by_protection_group': {
                'input_type': list_status_aggregated_by_protection_group_input_type,
                'output_type': type.ReferenceType(__name__, 'Snapshots.StatusByProtectionGroupListResult'),
                'errors': list_status_aggregated_by_protection_group_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_status_aggregated_by_protection_group_input_value_validator_list,
                'output_validator_list': list_status_aggregated_by_protection_group_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'list_status_aggregated_by_time_slice': list_status_aggregated_by_time_slice_rest_metadata,
            'list_status_aggregated_by_protection_group': list_status_aggregated_by_protection_group_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.reports.clusters.protection_groups.snapshots',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Snapshots': Snapshots,
    }

