# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.reports.clusters.virtual_machines.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice.reports.clusters.virtual_machines_client`` module
provides classes to get reports for virtual machine snapshots.

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
    The ``Snapshots`` provides methods for virtual machine snapshot reports.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots'
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
        The ``Snapshots.Status`` enumeration contains valid status for virtual
        machine snapshot operation.
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
        Virtual machine snapshot is successfully created.

        """
        ERROR = None
        """
        Virtual machine snapshot has failed.

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
    })
    Status._set_binding_type(type.EnumType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.status',
        Status))


    class FilterSpec(VapiStruct):
        """
        The ``Snapshots.FilterSpec`` class contains attributes used to filter the
        results when listing virtual machines snapshots for the reports. If
        multiple attributes are specified, only virtual machine snapshots matching
        all of the attributes that match the filter are returned. If the time range
        is not specified, the data existed over the last retention period which is
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
                     vms=None,
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
            :type  vms: :class:`set` of :class:`str` or ``None``
            :param vms: Identifiers of virtual machines that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``VirtualMachine``.
                If None or empty, virtual machines with any identifier matches the
                filter.
            """
            self.start_time = start_time
            self.end_time = end_time
            self.vms = vms
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.filter_spec', {
            'start_time': type.OptionalType(type.DateTimeType()),
            'end_time': type.OptionalType(type.DateTimeType()),
            'vms': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class IterationSpec(VapiStruct):
        """
        The ``Snapshots.IterationSpec`` class contains attributes used to break
        results into pages when listing virtual machine snapshots for the reports.
        see :func:`Snapshots.list`.
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
                None the offset will be 0
            """
            self.page_size = page_size
            self.offset = offset
            VapiStruct.__init__(self)


    IterationSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.iteration_spec', {
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
        :attr:`Snapshots.ListItem.creation_time` of the virtual machine snapshot.
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
            :param snapshots: List of virtual machine snapshot items.
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
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.list_result', {
            'snapshots': type.ListType(type.ReferenceType(__name__, 'Snapshots.ListItem')),
            'total_count': type.IntegerType(),
        },
        ListResult,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Snapshots.ListItem`` class contains information about a virtual
        machine snapshot returned by :func:`Snapshots.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'SUCCESS' : [('snapshot', False)],
                    'ERROR' : [('error', True)],
                }
            ),
        ]



        def __init__(self,
                     name=None,
                     snapshot=None,
                     pg_snapshot=None,
                     pg=None,
                     vm=None,
                     status=None,
                     error=None,
                     creation_time=None,
                     expiration_time=None,
                     snapshot_type=None,
                     deleted=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the virtual machine snapshot. If no snapshot is available
                for virtual machine due to error, a dummy name will be returned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  snapshot: :class:`str` or ``None``
            :param snapshot: Identifier of the virtual machine snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``.
                None when virtual machine snapshot operation has failed.
            :type  pg_snapshot: :class:`str`
            :param pg_snapshot: Identifier of the protection group snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group.snapshot``. When methods
                return a value of this class as a return value, the attribute will
                be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group.snapshot``.
            :type  pg: :class:`str`
            :param pg: ID of the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  vm: :class:`str`
            :param vm: MoRef ID of the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  status: :class:`Snapshots.Status`
            :param status: Status of the virtual machine snapshot method.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  error: :class:`com.vmware.snapservice_client.Reason`
            :param error: Failure reason, if the virtual machine snapshot operation has
                failed.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`Snapshots.Status.ERROR`.
            :type  creation_time: :class:`datetime.datetime`
            :param creation_time: Creation time of virtual machine snapshot. If the snapshot
                operation fails, start time of the operation is returned.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  expiration_time: :class:`datetime.datetime` or ``None``
            :param expiration_time: Expiration time of virtual machine snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None no expiry time is set for the virtual machine snapshot.
            :type  snapshot_type: :class:`com.vmware.snapservice.clusters.virtual_machines_client.Snapshots.Type` or ``None``
            :param snapshot_type: Type of virtual machine snapshot.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is being kept optional for future use-cases, but
                mandatory in the current version.
            :type  deleted: :class:`bool`
            :param deleted: Whether the virtual machine snapshot is deleted.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.snapshot = snapshot
            self.pg_snapshot = pg_snapshot
            self.pg = pg
            self.vm = vm
            self.status = status
            self.error = error
            self.creation_time = creation_time
            self.expiration_time = expiration_time
            self.snapshot_type = snapshot_type
            self.deleted = deleted
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.list_item', {
            'name': type.StringType(),
            'snapshot': type.OptionalType(type.IdType()),
            'pg_snapshot': type.IdType(resource_types='com.vmware.snapservice.protection_group.snapshot'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'vm': type.IdType(resource_types='VirtualMachine'),
            'status': type.ReferenceType(__name__, 'Snapshots.Status'),
            'error': type.OptionalType(type.ReferenceType('com.vmware.snapservice_client', 'Reason')),
            'creation_time': type.DateTimeType(),
            'expiration_time': type.OptionalType(type.DateTimeType()),
            'snapshot_type': type.OptionalType(type.ReferenceType('com.vmware.snapservice.clusters.virtual_machines_client', 'Snapshots.Type')),
            'deleted': type.BooleanType(),
        },
        ListItem,
        False,
        None))


    class StatusByTimeSliceItem(VapiStruct):
        """
        The ``Snapshots.StatusByTimeSliceItem`` class contains information about
        aggregated status count of all the snapshots for the filtered virtual
        machines returned by :func:`Snapshots.list_status_aggregated_by_time_slice`
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
            :param end_time: End time of the time slice for which the snapshos status count is
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
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.status_by_time_slice_item', {
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
                     success_count=None,
                    ):
            """
            :type  error_count: :class:`long`
            :param error_count: Aggregated count of virtual machine snapshots with "ERROR" status.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  success_count: :class:`long`
            :param success_count: Aggregated count of virtual machine snapshots with "SUCCESS"
                status.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.error_count = error_count
            self.success_count = success_count
            VapiStruct.__init__(self)


    AggregatedStatusInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.aggregated_status_info', {
            'error_count': type.IntegerType(),
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
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.status_by_time_slice_list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Snapshots.StatusByTimeSliceItem')),
        },
        StatusByTimeSliceListResult,
        False,
        None))


    class StatusByVirtualMachineItem(VapiStruct):
        """
        The ``Snapshots.StatusByVirtualMachineItem`` class contains information
        about status counts of virtual machine snapshots aggregated by virtual
        machine as returned by
        :func:`Snapshots.list_status_aggregated_by_virtual_machine` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vm=None,
                     info=None,
                    ):
            """
            :type  vm: :class:`str`
            :param vm: ID of the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  info: :class:`Snapshots.AggregatedStatusInfo`
            :param info: Information about aggregated status counts of the snapshots.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vm = vm
            self.info = info
            VapiStruct.__init__(self)


    StatusByVirtualMachineItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.status_by_virtual_machine_item', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'info': type.ReferenceType(__name__, 'Snapshots.AggregatedStatusInfo'),
        },
        StatusByVirtualMachineItem,
        False,
        None))


    class StatusByVirtualMachineListResult(VapiStruct):
        """
        The ``Snapshots.StatusByVirtualMachineListResult`` class represents the
        result of :func:`Snapshots.list_status_aggregated_by_virtual_machine`
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
            :type  items: :class:`list` of :class:`Snapshots.StatusByVirtualMachineItem`
            :param items: List of status count items aggregated by virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    StatusByVirtualMachineListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.snapshots.status_by_virtual_machine_list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Snapshots.StatusByVirtualMachineItem')),
        },
        StatusByVirtualMachineListResult,
        False,
        None))



    def list(self,
             cluster,
             filter=None,
             iterate=None,
             ):
        """
        Paginated list of virtual machine snapshots for the given cluster used
        for reports.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the list result.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all virtual machines snapshots match the filter.
        :type  iterate: :class:`Snapshots.IterationSpec` or ``None``
        :param iterate: The specification of a page to be retrieved.
            If None, the first page will be retrieved.
        :rtype: :class:`Snapshots.ListResult`
        :return: List of virtual machine snapshots for report matching the
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
        filtered virtual machines for a given cluster time sliced as defined by
        the service.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the result list.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all virtual machines match the filter.
        :rtype: :class:`Snapshots.StatusByTimeSliceListResult`
        :return: List of aggregated counts for virtual machine snapshot statuses for
            report matching the :class:`Snapshots.FilterSpec` for the given
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

    def list_status_aggregated_by_virtual_machine(self,
                                                  cluster,
                                                  filter=None,
                                                  ):
        """
        Get the status counts of virtual machine snapshots aggregated by
        virtual machine.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`Snapshots.FilterSpec` or ``None``
        :param filter: Contains arguments to filter the list result.
            If None, the behavior is equivalent to a
            :class:`Snapshots.FilterSpec` with all attributes None which means
            all virtual machines match the filter.
        :rtype: :class:`Snapshots.StatusByVirtualMachineListResult`
        :return: status counts of virtual machine snapshots aggregated by virtual
            machine.
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
        return self._invoke('list_status_aggregated_by_virtual_machine',
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

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/virtual-machines/snapshots',
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
            url_template='/snapservice/reports/clusters/{cluster}/virtual-machines/snapshot-status-counts?aggregateBy=time-slice',
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

        # properties for list_status_aggregated_by_virtual_machine operation
        list_status_aggregated_by_virtual_machine_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Snapshots.FilterSpec')),
        })
        list_status_aggregated_by_virtual_machine_error_dict = {
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
        list_status_aggregated_by_virtual_machine_input_value_validator_list = [
        ]
        list_status_aggregated_by_virtual_machine_output_validator_list = [
        ]
        list_status_aggregated_by_virtual_machine_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/virtual-machines/snapshot-status-counts?aggregateBy=virtual-machine',
            path_variables={
                'cluster': 'cluster',
            },
            query_parameters={
            },
            dispatch_parameters={
                'aggregateBy': 'virtual-machine',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
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
            'list_status_aggregated_by_virtual_machine': {
                'input_type': list_status_aggregated_by_virtual_machine_input_type,
                'output_type': type.ReferenceType(__name__, 'Snapshots.StatusByVirtualMachineListResult'),
                'errors': list_status_aggregated_by_virtual_machine_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_status_aggregated_by_virtual_machine_input_value_validator_list,
                'output_validator_list': list_status_aggregated_by_virtual_machine_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'list_status_aggregated_by_time_slice': list_status_aggregated_by_time_slice_rest_metadata,
            'list_status_aggregated_by_virtual_machine': list_status_aggregated_by_virtual_machine_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.reports.clusters.virtual_machines.snapshots',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Snapshots': Snapshots,
    }

