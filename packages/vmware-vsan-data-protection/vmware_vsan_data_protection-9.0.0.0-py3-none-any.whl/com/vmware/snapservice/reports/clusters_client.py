# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.reports.clusters.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice.reports.clusters_client`` module provides classes
for getting protection groups data for reports.

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


class ProtectionGroups(VapiInterface):
    """
    The ``ProtectionGroups`` provides methods for protection groups report.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.reports.clusters.protection_groups'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ProtectionGroupsStub)
        self._VAPI_OPERATION_IDS = {}

    class ProtectionGroupInfo(VapiStruct):
        """
        The ``ProtectionGroups.ProtectionGroupInfo`` class contains attributes that
        provide information regarding the protection group.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     deleted=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  deleted: :class:`bool`
            :param deleted: Whether the protection group is deleted.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.deleted = deleted
            VapiStruct.__init__(self)


    ProtectionGroupInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.protection_group_info', {
            'name': type.StringType(),
            'deleted': type.BooleanType(),
        },
        ProtectionGroupInfo,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``ProtectionGroups.ListItem`` class contains information about a
        protection group returned by :func:`ProtectionGroups.list` method
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
            :param pg: Identifier of the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  info: :class:`ProtectionGroups.ProtectionGroupInfo`
            :param info: Information regarding the protection group.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.pg = pg
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.list_item', {
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'info': type.ReferenceType(__name__, 'ProtectionGroups.ProtectionGroupInfo'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``ProtectionGroups.ListResult`` class represents the result of
        :func:`ProtectionGroups.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`ProtectionGroups.ListItem`
            :param items: List of items
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.protection_groups.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'ProtectionGroups.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self,
             cluster,
             ):
        """
        List the protection groups for the given cluster used for reports. The
        list contains the protection groups existed over the last retention
        period which is used for reporting purpose, by default retention period
        is set to 90days.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`ProtectionGroups.ListResult`
        :return: Information about the protection groups
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
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
                            })
class VirtualMachines(VapiInterface):
    """
    The ``VirtualMachines`` provides methods for virtual machines report.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.reports.clusters.virtual_machines'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _VirtualMachinesStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        The ``VirtualMachines.Info`` class contains attributes that provide
        information regarding the virtual machine.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     deleted=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  deleted: :class:`bool`
            :param deleted: Whether the virtual machine is deleted.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.deleted = deleted
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.info', {
            'name': type.StringType(),
            'deleted': type.BooleanType(),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``VirtualMachines.ListItem`` class contains information about a virtual
        machine returned by :func:`VirtualMachines.list` method
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
            :param vm: Identifier of the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  info: :class:`VirtualMachines.Info`
            :param info: Information regarding the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.vm = vm
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.list_item', {
            'vm': type.IdType(resource_types='VirtualMachine'),
            'info': type.ReferenceType(__name__, 'VirtualMachines.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``VirtualMachines.ListResult`` class represents the result of
        :func:`VirtualMachines.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`VirtualMachines.ListItem`
            :param items: List of items
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.reports.clusters.virtual_machines.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'VirtualMachines.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self,
             cluster,
             ):
        """
        List the virtual machines for the given cluster used for reports. The
        list contains the virtual machines existed over the last retention
        period which is used for reporting purpose, by default retention period
        is set to 90 days.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :rtype: :class:`VirtualMachines.ListResult`
        :return: Information about the virtual machines
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
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
                            })
class _ProtectionGroupsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        list_error_dict = {
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
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/protection-groups',
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

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'ProtectionGroups.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.reports.clusters.protection_groups',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VirtualMachinesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        })
        list_error_dict = {
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
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/reports/clusters/{cluster}/virtual-machines',
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

        operations = {
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'VirtualMachines.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.reports.clusters.virtual_machines',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ProtectionGroups': ProtectionGroups,
        'VirtualMachines': VirtualMachines,
        'protection_groups': 'com.vmware.snapservice.reports.clusters.protection_groups_client.StubFactory',
        'virtual_machines': 'com.vmware.snapservice.reports.clusters.virtual_machines_client.StubFactory',
    }

