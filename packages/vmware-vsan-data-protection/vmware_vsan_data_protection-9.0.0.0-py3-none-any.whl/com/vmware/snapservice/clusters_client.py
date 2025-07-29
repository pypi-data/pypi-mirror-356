# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.clusters.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice.clusters_client`` module provides classes for
managing protection groups and snapshots in a vSAN cluster.

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


class ProtectionGroups(VapiInterface):
    """
    The ``ProtectionGroups`` class provides methods for managing protection
    groups created for a cluster.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.clusters.protection_groups'
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
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'pause_task': 'pause$task'})
        self._VAPI_OPERATION_IDS.update({'resume_task': 'resume$task'})
        self._VAPI_OPERATION_IDS.update({'demote_task': 'demote$task'})
        self._VAPI_OPERATION_IDS.update({'promote_task': 'promote$task'})
        self._VAPI_OPERATION_IDS.update({'activate_task': 'activate$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class FilterSpec(VapiStruct):
        """
        The ``ProtectionGroups.FilterSpec`` class contains attributes used to
        filter the results when listing protection groups for a cluster If multiple
        attributes are specified, only protection groups matching all of the
        attributes match the filter. See :func:`ProtectionGroups.list`.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     pgs=None,
                     names=None,
                     states=None,
                     vms=None,
                     cluster_pairs=None,
                    ):
            """
            :type  pgs: :class:`set` of :class:`str` or ``None``
            :param pgs: Identifiers of protection groups that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``.
                If None or empty, protection groups with any identifier match the
                filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names of protection groups that can match the filter.
                If None or empty, protection groups with any name match the filter.
            :type  states: :class:`set` of :class:`com.vmware.snapservice_client.ProtectionGroupStatus` or ``None``
            :param states: States of protection groups that can match the filter.
                If None or empty, protection groups with any state match the
                filter.
            :type  vms: :class:`set` of :class:`str` or ``None``
            :param vms: Identifiers of the virtual machines which belong to the protection
                groups that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``.
                If None or empty, protection groups with any virtual machines match
                the filter.
            :type  cluster_pairs: :class:`set` of :class:`str` or ``None``
            :param cluster_pairs: Identifiers of the cluster pairs configured for protection groups
                that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``.
                If None or empty, protection groups with any or no cluster pairs
                match the filter.
            """
            self.pgs = pgs
            self.names = names
            self.states = states
            self.vms = vms
            self.cluster_pairs = cluster_pairs
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.protection_groups.filter_spec', {
            'pgs': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
            'states': type.OptionalType(type.SetType(type.ReferenceType('com.vmware.snapservice_client', 'ProtectionGroupStatus'))),
            'vms': type.OptionalType(type.SetType(type.IdType())),
            'cluster_pairs': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class DeleteSpec(VapiStruct):
        """
        The ``ProtectionGroups.DeleteSpec`` class contains attributes used to
        specify the parameters for deleting a protection group See
        :func:`ProtectionGroups.delete`.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     force=None,
                    ):
            """
            :type  force: :class:`bool` or ``None``
            :param force: Indicates if force delete to be performed. If set to True
                protection group and all associated snapshots will be deleted
                immediately
                If None, All the snapshots associated with the protection group
                will be retained till expiry.
            """
            self.force = force
            VapiStruct.__init__(self)


    DeleteSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.protection_groups.delete_spec', {
            'force': type.OptionalType(type.BooleanType()),
        },
        DeleteSpec,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``ProtectionGroups.ListItem`` class contains information about a
        protection group returned by :func:`ProtectionGroups.list` method

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
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  info: :class:`com.vmware.snapservice_client.ProtectionGroupInfo`
            :param info: Information regarding the protection group.
            """
            self.pg = pg
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.protection_groups.list_item', {
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'info': type.ReferenceType('com.vmware.snapservice_client', 'ProtectionGroupInfo'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``ProtectionGroups.ListResult`` class represents the result of
        :func:`ProtectionGroups.list` method.

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
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.protection_groups.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'ProtectionGroups.ListItem')),
        },
        ListResult,
        False,
        None))




    def create_task(self,
               cluster,
               spec,
               ):
        """
        Create a protection group for the given cluster.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  spec: :class:`com.vmware.snapservice_client.ProtectionGroupSpec`
        :param spec: specification for the protection group.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('create$task',
                                {
                                'cluster': cluster,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.snapservice.protection_group'))
        return task_instance

    def list(self,
             cluster,
             filter=None,
             ):
        """
        List the protection groups for the given cluster.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`ProtectionGroups.FilterSpec` or ``None``
        :param filter: Specification of matching protection groups for which information
            should be returned.
            If None, the behavior is equivalent to a
            :class:`ProtectionGroups.FilterSpec` with all attributes None which
            means all protection groups match the filter.
        :rtype: :class:`ProtectionGroups.ListResult`
        :return: Information about the protection groups matching the
            :class:`ProtectionGroups.FilterSpec` for the given cluster.
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
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'filter': filter,
                            })

    def get(self,
            cluster,
            pg,
            ):
        """
        Get the detailed information regarding the specified protection group.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :rtype: :class:`com.vmware.snapservice_client.ProtectionGroupInfo`
        :return: Information about the specified protection group.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If no cluster associated with ``cluster`` or protection group
            associated with ``pg`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If any input is invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        return self._invoke('get',
                            {
                            'cluster': cluster,
                            'pg': pg,
                            })


    def update_task(self,
               cluster,
               pg,
               spec,
               ):
        """
        Update a protection group for the given cluster.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :type  spec: :class:`com.vmware.snapservice_client.ProtectionGroupUpdateSpec`
        :param spec: specification for updting the protection group.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the specified protection group is locked.
        """
        task_id = self._invoke('update$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def pause_task(self,
              cluster,
              pg,
              ):
        """
        Pause the specified proteciton group. This action pauses all periodic
        snapshot operations and deletion of expired snapshots. Any ongoing
        snapshot creation or deletion operations will not be paused.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            If the protection group is already paused.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the specified protection group is locked.
        """
        task_id = self._invoke('pause$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def resume_task(self,
               cluster,
               pg,
               ):
        """
        Resume the specified proteciton group. This action resumes all periodic
        snapshot operations and deletion of expired snapshots.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            If the protection group is already active.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the specified protection group is locked.
        """
        task_id = self._invoke('resume$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def demote_task(self,
               cluster,
               pg,
               ):
        """
        Demote the specified protection group. This operation demotes a
        protection group into a demoted state. 
        
        When the protection group goes from an Active state to demoted, all
        local protection and remote rpelication operations will be paused.  
        
        While in this state, there will be no local protection or remote
        replication operations performed by the system.  The protection group
        goes into a dormant state once the user activates the dormant PG in the
        remote site.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            If the protection group is already in demoted state.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the specified protection group is not in a valid state for the
            transition or if there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the protection group is not configured for replication.
        """
        task_id = self._invoke('demote$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def promote_task(self,
                cluster,
                pg,
                ):
        """
        Promote the specified protection group. This operation promotes a
        protection group from a dormant state to recovery. 
        
        While in this state, there will be no local protection or remote
        replication operations performed by the system.  User can promote the
        protection group into recovery state in order to start recovery
        workflows of the members that belong to this protection group.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            If the protection group is already in recovery state.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the specified protection group is not in a valid state for the
            transition or if there are incoming replications for members that
            belong to the protection group or if there is another operation in
            progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the protection group is not configured for replication.
        """
        task_id = self._invoke('promote$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def activate_task(self,
                 cluster,
                 pg,
                 ):
        """
        Activate the specified protection group. This operation activates a
        protection group from a recovery state putting it into an active state.
        
        This will result in enabling local protection and remote replication
        for the members in the protection group. 
        This method was added in **vSphere API 9.0.0.0**.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyInDesiredState` 
            If the protection group is already in active state.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the specified protection group is not in a valid state for the
            transition or if there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or protection
            group associated with ``pg`` in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('activate$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               cluster,
               pg,
               spec=None,
               ):
        """
        Delete the specified protection group. Default bahaviour:

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  pg: :class:`str`
        :param pg: Identifier of the protection group.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.protection_group``.
        :type  spec: :class:`ProtectionGroups.DeleteSpec` or ``None``
        :param spec: Specifies the additional parameters for the delete operation.
            If None, protection group status is set to marked as deleted and
            will be be deleted permanently once all its associated snapshots
            are deleted.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there is another operation in progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If no cluster associated with ``cluster`` or protection group
            associated with ``pg`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the specified protection group is locked.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cluster': cluster,
                                'pg': pg,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class VirtualMachines(VapiInterface):
    """
    The ``VirtualMachines`` class provides methods to manage virtual machines.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.clusters.virtual_machines'
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
        self._VAPI_OPERATION_IDS.update({'revert_task': 'revert$task'})
        self._VAPI_OPERATION_IDS.update({'restore_task': 'restore$task'})
        self._VAPI_OPERATION_IDS.update({'linked_clone_task': 'linked_clone$task'})

    class ReplicationStatus(Enum):
        """
        The ``VirtualMachines.ReplicationStatus`` class contains the supported
        values for the replication status of a virtual machine.
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
        ERROR = None
        """
        The group has replication or configuration errors

        """
        MOVING = None
        """
        The group is in the process of being moved to a different HBR server

        """
        CONFIGURING = None
        """
        The group is in the process of being configured or re-configured

        """
        PAUSED = None
        """
        The replication for this group is being paused

        """
        FULL_SYNC = None
        """
        Full sync is performed on this group

        """
        INITIAL_FULL_SYNC = None
        """
        Initial full sync is performed, this state happens only once in a group's
        lifetime

        """
        SYNC = None
        """
        There is live replication traffic for this group

        """
        NOT_ACTIVE = None
        """
        There is no replication trafic for this group and there are no opened
        connecitons for it.

        """
        OK = None
        """
        The group is configured properly, no configuration or replication errors
        are present. But no actual replication traffic is taking place at the
        moment.

        """
        UNKNOWN = None
        """
        The group's status cannot be determined.

        """
        RECOVERING = None
        """
        A recovery is being performed on this group.

        """
        RECOVERED = None
        """
        The replication group has been successfully recovered.

        """
        DISK_RESIZING = None
        """
        Some of the target disks are currently resizing

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ReplicationStatus` instance.
            """
            Enum.__init__(string)

    ReplicationStatus._set_values({
        'ERROR': ReplicationStatus('ERROR'),
        'MOVING': ReplicationStatus('MOVING'),
        'CONFIGURING': ReplicationStatus('CONFIGURING'),
        'PAUSED': ReplicationStatus('PAUSED'),
        'FULL_SYNC': ReplicationStatus('FULL_SYNC'),
        'INITIAL_FULL_SYNC': ReplicationStatus('INITIAL_FULL_SYNC'),
        'SYNC': ReplicationStatus('SYNC'),
        'NOT_ACTIVE': ReplicationStatus('NOT_ACTIVE'),
        'OK': ReplicationStatus('OK'),
        'UNKNOWN': ReplicationStatus('UNKNOWN'),
        'RECOVERING': ReplicationStatus('RECOVERING'),
        'RECOVERED': ReplicationStatus('RECOVERED'),
        'DISK_RESIZING': ReplicationStatus('DISK_RESIZING'),
    })
    ReplicationStatus._set_binding_type(type.EnumType(
        'com.vmware.snapservice.clusters.virtual_machines.replication_status',
        ReplicationStatus))


    class FilterSpec(VapiStruct):
        """
        The ``VirtualMachines.FilterSpec`` class contains attributes used to filter
        the results when listing virtual machines for a cluster If multiple
        attributes are specified, only virtual machines matching all of the
        attributes match the filter. See :func:`VirtualMachines.list`.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vms=None,
                     name_patterns=None,
                     local_protection_enabled=None,
                    ):
            """
            :type  vms: :class:`set` of :class:`str` or ``None``
            :param vms: Identifiers of virtual machines that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will contain identifiers for the
                resource type: ``VirtualMachine``.
                If None or empty, virtual machines with any identifier match the
                filter.
            :type  name_patterns: :class:`list` of :class:`str` or ``None``
            :param name_patterns: One or more match patterns for virtual machine name that can match
                the filter. Uses standard POSIX Shell globbing pattern.
                If None or empty virtual machines with any name match the filter.
            :type  local_protection_enabled: :class:`bool` or ``None``
            :param local_protection_enabled: Status of the local protection that must match the filter.
                If None or empty, virtual machines with any local protection status
                can match the filter.
            """
            self.vms = vms
            self.name_patterns = name_patterns
            self.local_protection_enabled = local_protection_enabled
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.filter_spec', {
            'vms': type.OptionalType(type.SetType(type.IdType())),
            'name_patterns': type.OptionalType(type.ListType(type.StringType())),
            'local_protection_enabled': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class ReplicationInfo(VapiStruct):
        """
        The ``VirtualMachines.ReplicationInfo`` class contains attributes that
        provide information regarding the replication configuration for a virtual
        machine.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'ERROR' : [('errors', True), ('license_failure', True)],
                    'MOVING' : [],
                    'CONFIGURING' : [],
                    'PAUSED' : [],
                    'FULL_SYNC' : [],
                    'INITIAL_FULL_SYNC' : [],
                    'SYNC' : [],
                    'NOT_ACTIVE' : [],
                    'OK' : [],
                    'UNKNOWN' : [],
                    'RECOVERING' : [],
                    'RECOVERED' : [],
                    'DISK_RESIZING' : [],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     errors=None,
                     license_failure=None,
                     cluster_pair=None,
                    ):
            """
            :type  status: :class:`VirtualMachines.ReplicationStatus`
            :param status: Replication state for the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  errors: :class:`list` of :class:`com.vmware.snapservice_client.Reason`
            :param errors: List of replication configuration errors for the virtual machine.
                If None no failure reason is available for the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`VirtualMachines.ReplicationStatus.ERROR`.
            :type  license_failure: :class:`bool`
            :param license_failure: Virtual machine replication configuration failed due to invalid
                license.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``status`` is :attr:`VirtualMachines.ReplicationStatus.ERROR`.
            :type  cluster_pair: :class:`str`
            :param cluster_pair: Cluster pair for which the virtual machine replication is
                configured.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.cluster_pair``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.cluster_pair``.
            """
            self.status = status
            self.errors = errors
            self.license_failure = license_failure
            self.cluster_pair = cluster_pair
            VapiStruct.__init__(self)


    ReplicationInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.replication_info', {
            'status': type.ReferenceType(__name__, 'VirtualMachines.ReplicationStatus'),
            'errors': type.OptionalType(type.ListType(type.ReferenceType('com.vmware.snapservice_client', 'Reason'))),
            'license_failure': type.OptionalType(type.BooleanType()),
            'cluster_pair': type.IdType(resource_types='com.vmware.snapservice.cluster_pair'),
        },
        ReplicationInfo,
        False,
        None))


    class RemoteProtectionInfo(VapiStruct):
        """
        The ``VirtualMachines.RemoteProtectionInfo`` class contains attributes that
        provide information regarding the remote protection for a virtual machine.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     incoming_replication=None,
                     outgoing_replications=None,
                    ):
            """
            :type  incoming_replication: :class:`VirtualMachines.ReplicationInfo` or ``None``
            :param incoming_replication: Provides the information rergarding the incoming replication for
                the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if there is no incoming replication for the virtual machine.
            :type  outgoing_replications: :class:`list` of :class:`VirtualMachines.ReplicationInfo` or ``None``
            :param outgoing_replications: Provides the information rergarding the outgoing replications for
                the virtual machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if there are no outgoing replications for the virtual machine.
            """
            self.incoming_replication = incoming_replication
            self.outgoing_replications = outgoing_replications
            VapiStruct.__init__(self)


    RemoteProtectionInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.remote_protection_info', {
            'incoming_replication': type.OptionalType(type.ReferenceType(__name__, 'VirtualMachines.ReplicationInfo')),
            'outgoing_replications': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'VirtualMachines.ReplicationInfo'))),
        },
        RemoteProtectionInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``VirtualMachines.Info`` class contains attributes that provide
        information regarding a virtual machine.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     local_protection_enabled=None,
                     protection_groups=None,
                     last_snapshot_time=None,
                     oldest_snapshot_time=None,
                     snapshot_count=None,
                     in_cluster=None,
                     remote_protection_info=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the virtual machine.
            :type  local_protection_enabled: :class:`bool`
            :param local_protection_enabled: Whether or not local protection is enabled. Local protection is
                considered to be enabled when the virtual machine belongs to at
                least one active protection group.
            :type  protection_groups: :class:`set` of :class:`str`
            :param protection_groups: List of protection groups that this virtual machine belongs to.
                Empty list when the virtual machine is not part of any protection
                group.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.protection_group``.
            :type  last_snapshot_time: :class:`datetime.datetime` or ``None``
            :param last_snapshot_time: Time of the last snapshot for the virtual machine.
                None if there are no snapshots taken for the virtual machine.
            :type  oldest_snapshot_time: :class:`datetime.datetime` or ``None``
            :param oldest_snapshot_time: Time of the oldest snapshot for the virtual machine.
                None if there are no snapshots taken for the virtual machine.
            :type  snapshot_count: :class:`long`
            :param snapshot_count: Number of snapshots available for the virtual machine.
            :type  in_cluster: :class:`bool`
            :param in_cluster: Indicates whether or not the virtual mahcine is currently part of
                the cluster. This can be set to false when there is atleast one
                snapshot for the virtual machine on the target cluster, but the
                virtual machine is not part of the cluster.
            :type  remote_protection_info: :class:`VirtualMachines.RemoteProtectionInfo` or ``None``
            :param remote_protection_info: Information regarding the remote protection for the virtual
                machine.
                This attribute was added in **vSphere API 9.0.0.0**.
                None if remote protection is not configured for the virtual
                machine.
            """
            self.name = name
            self.local_protection_enabled = local_protection_enabled
            self.protection_groups = protection_groups
            self.last_snapshot_time = last_snapshot_time
            self.oldest_snapshot_time = oldest_snapshot_time
            self.snapshot_count = snapshot_count
            self.in_cluster = in_cluster
            self.remote_protection_info = remote_protection_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.info', {
            'name': type.StringType(),
            'local_protection_enabled': type.BooleanType(),
            'protection_groups': type.SetType(type.IdType()),
            'last_snapshot_time': type.OptionalType(type.DateTimeType()),
            'oldest_snapshot_time': type.OptionalType(type.DateTimeType()),
            'snapshot_count': type.IntegerType(),
            'in_cluster': type.BooleanType(),
            'remote_protection_info': type.OptionalType(type.ReferenceType(__name__, 'VirtualMachines.RemoteProtectionInfo')),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``VirtualMachines.ListItem`` class contains information about a virtual
        machine returned by :func:`VirtualMachines.list` method.

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
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``VirtualMachine``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``VirtualMachine``.
            :type  info: :class:`VirtualMachines.Info`
            :param info: Information regarding the virtual machine.
            """
            self.vm = vm
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.list_item', {
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
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'VirtualMachines.ListItem')),
        },
        ListResult,
        False,
        None))


    class RevertSpec(VapiStruct):
        """
        The ``VirtualMachines.RevertSpec`` class contains attributes to revert the
        virtual machine to a given snapshot point.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     snapshot=None,
                    ):
            """
            :type  snapshot: :class:`str`
            :param snapshot: Identifier of the virtual machine snapshot to which the virtual
                machine shall be reverted.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``.
            """
            self.snapshot = snapshot
            VapiStruct.__init__(self)


    RevertSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.revert_spec', {
            'snapshot': type.IdType(resource_types='com.vmware.snapservice.vm.snapshot'),
        },
        RevertSpec,
        False,
        None))


    class RestorePlacementSpec(VapiStruct):
        """
        The ``VirtualMachines.RestorePlacementSpec`` class contains attributes used
        to place restored virtual machine on to resources within the vcenter
        inventory.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the restored virtual machine
                should be placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If attribute is None, the system will use the default virtual
                machine folder of the datacenter. If this results in a conflict due
                to other placement parameters, the virtual machine restore
                operation will fail.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the restored virtual machine should be
                placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If attribute is None, the system will use the other placement
                parameters to create virtual machine. If this results in a conflict
                due to other placement parameters, the virtual machine restore
                operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the restored virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` is specified, ``host`` must be a member of cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If this attribute is unset, if ``resourcePool`` is set, and the
                target is a DRS cluster, a host will be picked by DRS. if
                ``resourcePool`` is unset, and the target is a DRS cluster, a host
                will be picked by DRS. if ``resourcePool`` is set, and the target
                is a cluster without DRS, InvalidArgument will be thrown.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            VapiStruct.__init__(self)


    RestorePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.restore_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
        },
        RestorePlacementSpec,
        False,
        None))


    class RestoreSpec(VapiStruct):
        """
        The ``VirtualMachines.RestoreSpec`` class contains attributes to restore
        deleted virtual machine to a given snapshot point.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     snapshot=None,
                     name=None,
                     placement=None,
                    ):
            """
            :type  snapshot: :class:`str`
            :param snapshot: Identifier of the virtual machine snapshot using which the virtual
                machine shall be restored. ``snapshot`` must be a snapshot of a
                virtual machine on the same cluster where virtual machine being
                restored.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``.
            :type  name: :class:`str` or ``None``
            :param name: New name for the virtual machine being restored.
                If None, will use the name of the virtual machine when the snapshot
                was taken.
            :type  placement: :class:`VirtualMachines.RestorePlacementSpec` or ``None``
            :param placement: Virtual machine placement information. 
                
                Each field in the spec will be used for placement. If the fields
                result in disjoint placement the operation will fail.
                If None, and the cluster is DRS enabled the system will create the
                virtual machine under the default vitual machine folder. If the DRS
                is not enabled on the cluster the operation will fail.
            """
            self.snapshot = snapshot
            self.name = name
            self.placement = placement
            VapiStruct.__init__(self)


    RestoreSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.restore_spec', {
            'snapshot': type.IdType(resource_types='com.vmware.snapservice.vm.snapshot'),
            'name': type.OptionalType(type.StringType()),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VirtualMachines.RestorePlacementSpec')),
        },
        RestoreSpec,
        False,
        None))


    class LinkedClonePlacementSpec(VapiStruct):
        """
        The ``VirtualMachines.LinkedClonePlacementSpec`` class contains attributes
        used to place cloned virtual machine on to resources within the vcenter
        inventory.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     folder=None,
                     resource_pool=None,
                     host=None,
                    ):
            """
            :type  folder: :class:`str` or ``None``
            :param folder: Virtual machine folder into which the cloned virtual machine should
                be placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type: ``Folder``.
                When methods return a value of this class as a return value, the
                attribute will be an identifier for the resource type: ``Folder``.
                If attribute is None, the system will use the default virtual
                machine folder of the datacenter. If this results in a conflict due
                to other placement parameters, the virtual machine clone operation
                will fail.
            :type  resource_pool: :class:`str` or ``None``
            :param resource_pool: Resource pool into which the cloned virtual machine should be
                placed.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ResourcePool``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``ResourcePool``.
                If attribute is None, the system will use the other placement
                parameters to create virtual machine. If this results in a conflict
                due to other placement parameters, the virtual machine clone
                operation will fail.
            :type  host: :class:`str` or ``None``
            :param host: Host onto which the cloned virtual machine should be placed. 
                
                If ``host`` and ``resourcePool`` are both specified,
                ``resourcePool`` must belong to ``host``. 
                
                If ``host`` is specified, ``host`` must be a member of cluster.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``HostSystem``. When methods return a value of this class as a
                return value, the attribute will be an identifier for the resource
                type: ``HostSystem``.
                If this attribute is unset, if ``resourcePool`` is set, and the
                target is a DRS cluster, a host will be picked by DRS. if
                ``resourcePool`` is unset, and the target is a DRS cluster, a host
                will be picked by DRS. if ``resourcePool`` is set, and the target
                is a cluster without DRS, InvalidArgument will be thrown.
            """
            self.folder = folder
            self.resource_pool = resource_pool
            self.host = host
            VapiStruct.__init__(self)


    LinkedClonePlacementSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.linked_clone_placement_spec', {
            'folder': type.OptionalType(type.IdType()),
            'resource_pool': type.OptionalType(type.IdType()),
            'host': type.OptionalType(type.IdType()),
        },
        LinkedClonePlacementSpec,
        False,
        None))


    class LinkedCloneSpec(VapiStruct):
        """
        The ``VirtualMachines.LinkedCloneSpec`` class contains attributes to create
        linked clone virtual machine from the given snapshot.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     snapshot=None,
                     name=None,
                     placement=None,
                    ):
            """
            :type  snapshot: :class:`str`
            :param snapshot: Identifier of the virtual machine snapshot using which the virtual
                machine shall be cloned. ``snapshot`` must be a snapshot of a
                virtual machine on the same cluster where virtual machine being
                cloned.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``. When methods return a value
                of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.vm.snapshot``.
            :type  name: :class:`str`
            :param name: Name of the cloned virtual machine.
            :type  placement: :class:`VirtualMachines.LinkedClonePlacementSpec` or ``None``
            :param placement: Virtual machine placement information. 
                
                Each field in the spec will be used for placement. If the fields
                result in disjoint placement the operation will fail.
                If None, and the cluster is DRS enabled the system will create the
                virtual machine under the default vitual machine folder. If the DRS
                is not enabled on the cluster the operation will fail.
            """
            self.snapshot = snapshot
            self.name = name
            self.placement = placement
            VapiStruct.__init__(self)


    LinkedCloneSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.clusters.virtual_machines.linked_clone_spec', {
            'snapshot': type.IdType(resource_types='com.vmware.snapservice.vm.snapshot'),
            'name': type.StringType(),
            'placement': type.OptionalType(type.ReferenceType(__name__, 'VirtualMachines.LinkedClonePlacementSpec')),
        },
        LinkedCloneSpec,
        False,
        None))



    def list(self,
             cluster,
             filter=None,
             ):
        """
        List the virtual machines for the given cluster.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  filter: :class:`VirtualMachines.FilterSpec` or ``None``
        :param filter: Specification of matching virtual machines for which information
            should be returned.
            If None, the behavior is equivalent to a
            :class:`VirtualMachines.FilterSpec` with all attributes None which
            means all virtual machines match the filter.
        :rtype: :class:`VirtualMachines.ListResult`
        :return: Information about the virtual machines matching the
            :class:`VirtualMachines.FilterSpec` for the given cluster.
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
        """
        return self._invoke('list',
                            {
                            'cluster': cluster,
                            'filter': filter,
                            })


    def revert_task(self,
               cluster,
               vm,
               spec,
               ):
        """
        Revert the virtual machine to a given snapshot point. The system takes
        an additional snapshot to preserve the state prior to performing a
        revert. The system snapshot does not preserve the in-memory state of
        the virtual machine. The virtual machine will be left in a powered off
        state after the revert operation.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the Cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`VirtualMachines.RevertSpec`
        :param spec: specification for the revert operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or no virtual
            machine associated with ``vm`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If the virtual machine has moved to another cluster or if there are
            more than max allowed revert operations in-progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('revert$task',
                                {
                                'cluster': cluster,
                                'vm': vm,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def restore_task(self,
                cluster,
                vm,
                spec,
                ):
        """
        Restore deleted virtual machine to a given snapshot point. The virtual
        machine will be left in a powered off state after the restore
        operation.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the Cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`VirtualMachines.RestoreSpec`
        :param spec: specification for the restore operation.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or no virtual
            machine associated with ``vm`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there are more than max allowed restore operations in-progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('restore$task',
                                {
                                'cluster': cluster,
                                'vm': vm,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='VirtualMachine'))
        return task_instance


    def linked_clone_task(self,
                     cluster,
                     vm,
                     spec,
                     ):
        """
        Creates a linked clone virtual machine from the given snapshot. The
        virtual machine will be left in a powered off state after the clone
        operation.

        :type  cluster: :class:`str`
        :param cluster: Identifier of the Cluster.
            The parameter must be an identifier for the resource type:
            ``ClusterComputeResource``.
        :type  vm: :class:`str`
        :param vm: Identifier of the virtual machine.
            The parameter must be an identifier for the resource type:
            ``VirtualMachine``.
        :type  spec: :class:`VirtualMachines.LinkedCloneSpec`
        :param spec: specification for the clone operation.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no cluster associated with ``cluster`` or no virtual
            machine associated with ``vm`` is found in the system.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If a virtual machine with the specified name already exists.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If there are more than max allowed clone operations in-progress.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the service is not available.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('linked_clone$task',
                                {
                                'cluster': cluster,
                                'vm': vm,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='VirtualMachine'))
        return task_instance
class _ProtectionGroupsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'spec': type.ReferenceType('com.vmware.snapservice_client', 'ProtectionGroupSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups',
            request_body_parameter='spec',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'ProtectionGroups.FilterSpec')),
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
            url_template='/snapservice/clusters/{cluster}/protection-groups',
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

        # properties for get operation
        get_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        get_error_dict = {
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
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
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
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'spec': type.ReferenceType('com.vmware.snapservice_client', 'ProtectionGroupUpdateSpec'),
        })
        update_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
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

        # properties for pause operation
        pause_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        pause_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        pause_input_value_validator_list = [
        ]
        pause_output_validator_list = [
        ]
        pause_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}?action=pause',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'pause',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for resume operation
        resume_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        resume_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        resume_input_value_validator_list = [
        ]
        resume_output_validator_list = [
        ]
        resume_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}?action=resume',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'resume',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for demote operation
        demote_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        demote_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        demote_input_value_validator_list = [
        ]
        demote_output_validator_list = [
        ]
        demote_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}?action=demote',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'demote',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for promote operation
        promote_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        promote_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
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
        promote_input_value_validator_list = [
        ]
        promote_output_validator_list = [
        ]
        promote_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}?action=promote',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'promote',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for activate operation
        activate_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
        })
        activate_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.already_in_desired_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        activate_input_value_validator_list = [
        ]
        activate_output_validator_list = [
        ]
        activate_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}?action=activate',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'activate',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'pg': type.IdType(resource_types='com.vmware.snapservice.protection_group'),
            'spec': type.OptionalType(type.ReferenceType(__name__, 'ProtectionGroups.DeleteSpec')),
        })
        delete_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/snapservice/clusters/{cluster}/protection-groups/{pg}',
            path_variables={
                'cluster': 'cluster',
                'pg': 'pg',
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
            'create$task': {
                'input_type': create_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'ProtectionGroups.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType('com.vmware.snapservice_client', 'ProtectionGroupInfo'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'pause$task': {
                'input_type': pause_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': pause_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': pause_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'resume$task': {
                'input_type': resume_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': resume_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': resume_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'demote$task': {
                'input_type': demote_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': demote_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': demote_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'promote$task': {
                'input_type': promote_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': promote_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': promote_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'activate$task': {
                'input_type': activate_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': activate_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyInDesiredState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': activate_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'pause': pause_rest_metadata,
            'resume': resume_rest_metadata,
            'demote': demote_rest_metadata,
            'promote': promote_rest_metadata,
            'activate': activate_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.clusters.protection_groups',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _VirtualMachinesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'VirtualMachines.FilterSpec')),
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
            url_template='/snapservice/clusters/{cluster}/virtual-machines',
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

        # properties for revert operation
        revert_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'VirtualMachines.RevertSpec'),
        })
        revert_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        revert_input_value_validator_list = [
        ]
        revert_output_validator_list = [
        ]
        revert_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/virtual-machines/{vm}?action=revert',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'revert',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for restore operation
        restore_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'VirtualMachines.RestoreSpec'),
        })
        restore_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        restore_input_value_validator_list = [
        ]
        restore_output_validator_list = [
        ]
        restore_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/virtual-machines/{vm}?action=restore',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'restore',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for linked_clone operation
        linked_clone_input_type = type.StructType('operation-input', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'vm': type.IdType(resource_types='VirtualMachine'),
            'spec': type.ReferenceType(__name__, 'VirtualMachines.LinkedCloneSpec'),
        })
        linked_clone_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        linked_clone_input_value_validator_list = [
        ]
        linked_clone_output_validator_list = [
        ]
        linked_clone_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/clusters/{cluster}/virtual-machines/{vm}?action=linked-clone',
            request_body_parameter='spec',
            path_variables={
                'cluster': 'cluster',
                'vm': 'vm',
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'linked-clone',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'revert$task': {
                'input_type': revert_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': revert_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': revert_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'restore$task': {
                'input_type': restore_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': restore_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': restore_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'linked_clone$task': {
                'input_type': linked_clone_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': linked_clone_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': linked_clone_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'revert': revert_rest_metadata,
            'restore': restore_rest_metadata,
            'linked_clone': linked_clone_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.clusters.virtual_machines',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ProtectionGroups': ProtectionGroups,
        'VirtualMachines': VirtualMachines,
        'protection_groups': 'com.vmware.snapservice.clusters.protection_groups_client.StubFactory',
        'virtual_machines': 'com.vmware.snapservice.clusters.virtual_machines_client.StubFactory',
    }

