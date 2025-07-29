# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice_client`` module provides classes for configuring
and managing vSAN protection groups and snapshots

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

class PrecheckStatus(Enum):
    """
    The ``PrecheckStatus`` class contains the validation status for a given
    precheck.
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
    Precheck validation succeeded.

    """
    WARNING = None
    """
    Precheck validation warning.

    """
    ERROR = None
    """
    Precheck validation error.

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
    'ERROR': PrecheckStatus('ERROR'),
})
PrecheckStatus._set_binding_type(type.EnumType(
    'com.vmware.snapservice.precheck_status',
    PrecheckStatus))



class TimeUnit(Enum):
    """
    The ``TimeUnit`` class contains the supported values for how often
    snapshots are taken.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    MINUTE = None
    """
    Minutes.

    """
    HOUR = None
    """
    Hours.

    """
    DAY = None
    """
    Day.

    """
    WEEK = None
    """
    Weeks.

    """
    MONTH = None
    """
    Months.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`TimeUnit` instance.
        """
        Enum.__init__(string)

TimeUnit._set_values({
    'MINUTE': TimeUnit('MINUTE'),
    'HOUR': TimeUnit('HOUR'),
    'DAY': TimeUnit('DAY'),
    'WEEK': TimeUnit('WEEK'),
    'MONTH': TimeUnit('MONTH'),
})
TimeUnit._set_binding_type(type.EnumType(
    'com.vmware.snapservice.time_unit',
    TimeUnit))



class TimeFrequency(Enum):
    """
    The ``TimeFrequency`` class contains the supported values for frequency to
    be used for snapshot retention.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    HOURLY = None
    """
    Keep hourly snapshots.

    """
    DAILY = None
    """
    Keep daily snapshots.

    """
    WEEKLY = None
    """
    Keep weekly snapshots.

    """
    MONTHLY = None
    """
    Keep monthly snapshots.

    """
    YEARLY = None
    """
    Keep yearly snapshots.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`TimeFrequency` instance.
        """
        Enum.__init__(string)

TimeFrequency._set_values({
    'HOURLY': TimeFrequency('HOURLY'),
    'DAILY': TimeFrequency('DAILY'),
    'WEEKLY': TimeFrequency('WEEKLY'),
    'MONTHLY': TimeFrequency('MONTHLY'),
    'YEARLY': TimeFrequency('YEARLY'),
})
TimeFrequency._set_binding_type(type.EnumType(
    'com.vmware.snapservice.time_frequency',
    TimeFrequency))



class ProtectionGroupStatus(Enum):
    """
    The ``ProtectionGroupStatus`` class contains the different states for the
    protection group.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    ACTIVE = None
    """
    Active

    """
    PAUSED = None
    """
    Paused

    """
    MARKED_FOR_DELETE = None
    """
    Marked for delete, 
    
    Indicates that the PG is soft deleted but has some PG snapshots and VM
    snapshots which are not yet expired. 

    """
    DEMOTED = None
    """
    Indicates that the protection group is in a demoted state. While in this
    state, there are no outgoing or incoming replications and local snapshots
    (if any) are also stopped.

    """
    DORMANT = None
    """
    
    
    Indicates that the PG is in dormant state.  
    
    In this state, all local protection and outgoing replications for the
    members are disabled. Members belonging to this protection group will be
    replica members for active incoming replications. 
    This class attribute was added in **vSphere API 9.0.0.0**.

    """
    RECOVERY = None
    """
    Recovery state. 
    
    Indicates the protection group is in a recovery state. In this state site
    recovery operations can be initiated in case of planned migration and
    unplanned failover. 
    This class attribute was added in **vSphere API 9.0.0.0**.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`ProtectionGroupStatus` instance.
        """
        Enum.__init__(string)

ProtectionGroupStatus._set_values({
    'ACTIVE': ProtectionGroupStatus('ACTIVE'),
    'PAUSED': ProtectionGroupStatus('PAUSED'),
    'MARKED_FOR_DELETE': ProtectionGroupStatus('MARKED_FOR_DELETE'),
    'DEMOTED': ProtectionGroupStatus('DEMOTED'),
    'DORMANT': ProtectionGroupStatus('DORMANT'),
    'RECOVERY': ProtectionGroupStatus('RECOVERY'),
})
ProtectionGroupStatus._set_binding_type(type.EnumType(
    'com.vmware.snapservice.protection_group_status',
    ProtectionGroupStatus))




class PrecheckResultItem(VapiStruct):
    """
    The ``PrecheckResultItem`` class contains attributes that provide details
    about individual precheck validation result.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """

    _validator_list = [
        UnionValidator(
            'status',
            {
                'WARNING' : [('errors', True)],
                'ERROR' : [('errors', True)],
                'OK' : [],
            }
        ),
    ]



    def __init__(self,
                 type=None,
                 desc=None,
                 status=None,
                 errors=None,
                ):
        """
        :type  type: :class:`str`
        :param type: Identifier of precheck performed. TODO: Add enum with each type
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  desc: :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param desc: Details about the precheck validation.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  status: :class:`PrecheckStatus`
        :param status: Status for precheck validation performed.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  errors: :class:`list` of :class:`Reason`
        :param errors: List of localized errors associated with the precheck.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional and it is only relevant when the value
            of ``status`` is one of :attr:`PrecheckStatus.WARNING` or
            :attr:`PrecheckStatus.ERROR`.
        """
        self.type = type
        self.desc = desc
        self.status = status
        self.errors = errors
        VapiStruct.__init__(self)


PrecheckResultItem._set_binding_type(type.StructType(
    'com.vmware.snapservice.precheck_result_item', {
        'type': type.StringType(),
        'desc': type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage'),
        'status': type.ReferenceType(__name__, 'PrecheckStatus'),
        'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Reason'))),
    },
    PrecheckResultItem,
    False,
    None))



class PrecheckResult(VapiStruct):
    """
    The ``PrecheckResult`` class contains attributes that provide details about
    all the prechecks performed.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 prechecks=None,
                ):
        """
        :type  prechecks: :class:`list` of :class:`PrecheckResultItem`
        :param prechecks: List of precheck with details.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.prechecks = prechecks
        VapiStruct.__init__(self)


PrecheckResult._set_binding_type(type.StructType(
    'com.vmware.snapservice.precheck_result', {
        'prechecks': type.ListType(type.ReferenceType(__name__, 'PrecheckResultItem')),
    },
    PrecheckResult,
    False,
    None))



class TargetEntities(VapiStruct):
    """
    The ``TargetEntities`` class contains attributes specifying the target
    entities to be protected. The initial release will only support virtual
    machines.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 vm_name_patterns=None,
                 vms=None,
                ):
        """
        :type  vm_name_patterns: :class:`list` of :class:`str` or ``None``
        :param vm_name_patterns: One or more match patterns for virtual machines to be protected. 
            
            Uses standard POSIX Shell globbing pattern. See also, the POSIX
            Shell language:
            http://pubs.opengroup.org/onlinepubs/009695399/utilities/xcu_chap02.html#tag_02_13_01
            If None, :attr:`TargetEntities.vms` must be specified.
        :type  vms: :class:`set` of :class:`str` or ``None``
        :param vms: List of virtual machines to be protected.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``VirtualMachine``. When methods return a value of this class as a
            return value, the attribute will contain identifiers for the
            resource type: ``VirtualMachine``.
            If None, the virtual machines to be protected will be determined
            based on the :attr:`TargetEntities.vm_name_patterns`.
        """
        self.vm_name_patterns = vm_name_patterns
        self.vms = vms
        VapiStruct.__init__(self)


TargetEntities._set_binding_type(type.StructType(
    'com.vmware.snapservice.target_entities', {
        'vm_name_patterns': type.OptionalType(type.ListType(type.StringType())),
        'vms': type.OptionalType(type.SetType(type.IdType())),
    },
    TargetEntities,
    False,
    None))



class SnapshotSchedule(VapiStruct):
    """
    The ``SnapshotSchedule`` class contains attributes that define the
    frequency at which snapshots must be taken.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 unit=None,
                 interval=None,
                ):
        """
        :type  unit: :class:`TimeUnit`
        :param unit: Units for the interval.
        :type  interval: :class:`long`
        :param interval: Interval between each snapshot.
        """
        self.unit = unit
        self.interval = interval
        VapiStruct.__init__(self)


SnapshotSchedule._set_binding_type(type.StructType(
    'com.vmware.snapservice.snapshot_schedule', {
        'unit': type.ReferenceType(__name__, 'TimeUnit'),
        'interval': type.IntegerType(),
    },
    SnapshotSchedule,
    False,
    None))



class RetentionPeriod(VapiStruct):
    """
    The ``RetentionPeriod`` class contains attributes that define the duration
    for which each snapshot must be retained.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 unit=None,
                 duration=None,
                ):
        """
        :type  unit: :class:`TimeUnit`
        :param unit: Units for the retention period
        :type  duration: :class:`long`
        :param duration: Duration for the snapshot to be retained
        """
        self.unit = unit
        self.duration = duration
        VapiStruct.__init__(self)


RetentionPeriod._set_binding_type(type.StructType(
    'com.vmware.snapservice.retention_period', {
        'unit': type.ReferenceType(__name__, 'TimeUnit'),
        'duration': type.IntegerType(),
    },
    RetentionPeriod,
    False,
    None))



class SnapshotPolicy(VapiStruct):
    """
    The ``SnapshotPolicy`` class contains attributes that describe the
    frequency and retention for taking snapshots of the protection targets.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 schedule=None,
                 retention=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name for the snapshot policy.
        :type  schedule: :class:`SnapshotSchedule`
        :param schedule: Schedule for the snapshots.
        :type  retention: :class:`RetentionPeriod`
        :param retention: Retention period for the snapshots.
        """
        self.name = name
        self.schedule = schedule
        self.retention = retention
        VapiStruct.__init__(self)


SnapshotPolicy._set_binding_type(type.StructType(
    'com.vmware.snapservice.snapshot_policy', {
        'name': type.StringType(),
        'schedule': type.ReferenceType(__name__, 'SnapshotSchedule'),
        'retention': type.ReferenceType(__name__, 'RetentionPeriod'),
    },
    SnapshotPolicy,
    False,
    None))



class TimePeriod(VapiStruct):
    """
    The ``TimePeriod`` class contains attributes that describes the time period
    and duration
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 unit=None,
                 duration=None,
                ):
        """
        :type  unit: :class:`TimeUnit`
        :param unit: Units for the duration in minutes, hours, days, weeks and years
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  duration: :class:`long`
        :param duration: Duration of time in number
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.unit = unit
        self.duration = duration
        VapiStruct.__init__(self)


TimePeriod._set_binding_type(type.StructType(
    'com.vmware.snapservice.time_period', {
        'unit': type.ReferenceType(__name__, 'TimeUnit'),
        'duration': type.IntegerType(),
    },
    TimePeriod,
    False,
    None))



class RetentionConfig(VapiStruct):
    """
    The ``RetentionConfig`` class contains attributes that describe the
    retention settings for a given protection group with ``ReplicationPolicy``
    enabled.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 frequency=None,
                 retention=None,
                ):
        """
        :type  frequency: :class:`TimeFrequency`
        :param frequency: Frequency of snapshots to be retained. For e.g. DAILY : 1 snapshot
            per day
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  retention: :class:`TimePeriod`
        :param retention: Total retention period for the snapshots.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.frequency = frequency
        self.retention = retention
        VapiStruct.__init__(self)


RetentionConfig._set_binding_type(type.StructType(
    'com.vmware.snapservice.retention_config', {
        'frequency': type.ReferenceType(__name__, 'TimeFrequency'),
        'retention': type.ReferenceType(__name__, 'TimePeriod'),
    },
    RetentionConfig,
    False,
    None))



class ShortTermRetention(VapiStruct):
    """
    The ``ShortTermRetention`` class contains attributes that describe the
    short term retention settings for the snapshots created from member
    entities on the remote cluster specified by {#link clusterPair}
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 keep_last=None,
                ):
        """
        :type  keep_last: :class:`long`
        :param keep_last: Retain the last n snapshots for the member entities created on the
            target replication site. The minimum and default value will be set
            to 1 to retain the last snapshot.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.keep_last = keep_last
        VapiStruct.__init__(self)


ShortTermRetention._set_binding_type(type.StructType(
    'com.vmware.snapservice.short_term_retention', {
        'keep_last': type.IntegerType(),
    },
    ShortTermRetention,
    False,
    None))



class RetentionPolicy(VapiStruct):
    """
    The ``RetentionPolicy`` class contains attributes that describe the policy
    for retention of the snapshots created for protection group members on the
    target replication site.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 short_term=None,
                ):
        """
        :type  short_term: :class:`ShortTermRetention`
        :param short_term: Short term snapshot retention settings for replication policy.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.short_term = short_term
        VapiStruct.__init__(self)


RetentionPolicy._set_binding_type(type.StructType(
    'com.vmware.snapservice.retention_policy', {
        'short_term': type.ReferenceType(__name__, 'ShortTermRetention'),
    },
    RetentionPolicy,
    False,
    None))



class ReplicationPolicy(VapiStruct):
    """
    The ``ReplicationPolicy`` class contains attributes that describe the
    settings to configure replication for a given protection group
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 cluster_pair=None,
                 recovery_point_objective=None,
                 snapshot_retention=None,
                ):
        """
        :type  cluster_pair: :class:`str` or ``None``
        :param cluster_pair: Identifier of the cluster pair. The member entity of the protection
            group will be replicated to the peer cluster part of the cluster
            pair.
            This attribute was added in **vSphere API 9.0.0.0**.
            When clients pass a value of this class as a parameter, the
            attribute must be an identifier for the resource type:
            ``com.vmware.snapservice.cluster_pair``. When methods return a
            value of this class as a return value, the attribute will be an
            identifier for the resource type:
            ``com.vmware.snapservice.cluster_pair``.
            This attribute is being kept optional for future use-cases, but
            mandatory in the current version.
        :type  recovery_point_objective: :class:`TimePeriod`
        :param recovery_point_objective: The RecoveryPointObjective(RPO) is a measure to configure amount of
            data that is acceptable to lose in an event of a disaster or
            failure.
            This attribute was added in **vSphere API 9.0.0.0**.
        :type  snapshot_retention: :class:`RetentionPolicy`
        :param snapshot_retention: Snapshot retention policy for remote site
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.cluster_pair = cluster_pair
        self.recovery_point_objective = recovery_point_objective
        self.snapshot_retention = snapshot_retention
        VapiStruct.__init__(self)


ReplicationPolicy._set_binding_type(type.StructType(
    'com.vmware.snapservice.replication_policy', {
        'cluster_pair': type.OptionalType(type.IdType()),
        'recovery_point_objective': type.ReferenceType(__name__, 'TimePeriod'),
        'snapshot_retention': type.ReferenceType(__name__, 'RetentionPolicy'),
    },
    ReplicationPolicy,
    False,
    None))



class ProtectionGroupSpec(VapiStruct):
    """
    The ``ProtectionGroupSpec`` class contains attributes that describe the
    desired protection group and the snapshot policies associated with it. A
    protection group is a group of entities that vSAN Snapshot Service protects
    together.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 target_entities=None,
                 snapshot_policies=None,
                 locked=None,
                 replication_policies=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the protection group.
        :type  target_entities: :class:`TargetEntities`
        :param target_entities: Target entities for the protection.
        :type  snapshot_policies: :class:`list` of :class:`SnapshotPolicy` or ``None``
        :param snapshot_policies: Snapshot policy for the protection targets.
            if None local protection will be skipped.
        :type  locked: :class:`bool` or ``None``
        :param locked: Indicates if the protection group is to be locked. A locked
            protection group cannot be modified or deleted by the user. All
            snapshots associated with the protection group will be secure and
            cannot be deleted. The system will automatically delete these
            snapshots upon expiry based on the retention period.
            if None the protection group will be considered as unlocked.
        :type  replication_policies: :class:`list` of :class:`ReplicationPolicy` or ``None``
        :param replication_policies: Replication policy for the protection group. Currently, only one
            ReplicationPolicy will be allowed. Additional policies to support
            protecting virtual machines to multiple clusters may be supported
            in the future
            This attribute was added in **vSphere API 9.0.0.0**.
            Set if replication needs to be configured. Currently only one
            policy is supported
        """
        self.name = name
        self.target_entities = target_entities
        self.snapshot_policies = snapshot_policies
        self.locked = locked
        self.replication_policies = replication_policies
        VapiStruct.__init__(self)


ProtectionGroupSpec._set_binding_type(type.StructType(
    'com.vmware.snapservice.protection_group_spec', {
        'name': type.StringType(),
        'target_entities': type.ReferenceType(__name__, 'TargetEntities'),
        'snapshot_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SnapshotPolicy'))),
        'locked': type.OptionalType(type.BooleanType()),
        'replication_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReplicationPolicy'))),
    },
    ProtectionGroupSpec,
    False,
    None))



class ProtectionGroupUpdateSpec(VapiStruct):
    """
    The ``ProtectionGroupUpdateSpec`` class contains attributes that describe
    the desired protection group and the snapshot policies associated with it.
    A protection group is a group of entities that vSAN Snapshot Service
    protects together.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 target_entities=None,
                 snapshot_policies=None,
                 replication_policies=None,
                ):
        """
        :type  name: :class:`str` or ``None``
        :param name: Name of the protection group.
            if None, the current proteciton group name will be retained.
        :type  target_entities: :class:`TargetEntities` or ``None``
        :param target_entities: Target entities for the protection. If :class:`set`, this will
            represent all the target entities for the protection group.
            if None, the existing target entities will be retained.
        :type  snapshot_policies: :class:`list` of :class:`SnapshotPolicy` or ``None``
        :param snapshot_policies: Snapshot policy for the protection targets. If :class:`set`, this
            will represent all the snapshot policies for the protection group.
            Any existing policies will be removed, if not specified in the new
            list.
            if None, existing snapshot policies will be retained.
        :type  replication_policies: :class:`list` of :class:`ReplicationPolicy` or ``None``
        :param replication_policies: Replication policies for the protection group.
            This attribute was added in **vSphere API 9.0.0.0**.
            Set if replication needs to be configured. Currently only one
            policy is supported
        """
        self.name = name
        self.target_entities = target_entities
        self.snapshot_policies = snapshot_policies
        self.replication_policies = replication_policies
        VapiStruct.__init__(self)


ProtectionGroupUpdateSpec._set_binding_type(type.StructType(
    'com.vmware.snapservice.protection_group_update_spec', {
        'name': type.OptionalType(type.StringType()),
        'target_entities': type.OptionalType(type.ReferenceType(__name__, 'TargetEntities')),
        'snapshot_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'SnapshotPolicy'))),
        'replication_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReplicationPolicy'))),
    },
    ProtectionGroupUpdateSpec,
    False,
    None))



class ProtectionGroupInfo(VapiStruct):
    """
    The ``ProtectionGroupInfo`` class contains attributes that provide detailed
    information regarding the protection group and the snapshot policies
    associated with it.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 name=None,
                 status=None,
                 target_entities=None,
                 snapshot_policies=None,
                 last_snapshot_time=None,
                 oldest_snapshot_time=None,
                 vms=None,
                 snapshots=None,
                 locked=None,
                 guid=None,
                 replication_policies=None,
                ):
        """
        :type  name: :class:`str`
        :param name: Name of the protection group.
        :type  status: :class:`ProtectionGroupStatus`
        :param status: Current status of the protection group.
        :type  target_entities: :class:`TargetEntities`
        :param target_entities: User provided target entities that must belong to the protection
            group.
        :type  snapshot_policies: :class:`list` of :class:`SnapshotPolicy`
        :param snapshot_policies: Snapshot policies for the protection targets.
        :type  last_snapshot_time: :class:`datetime.datetime` or ``None``
        :param last_snapshot_time: Time at which the last protection group snapshot was taken.
            is None if there are no snapshots taken for the protection group.
        :type  oldest_snapshot_time: :class:`datetime.datetime` or ``None``
        :param oldest_snapshot_time: Time at which the current oldest protection group snapshot was
            taken.
            is None if there are no snapshots taken for the protection group.
        :type  vms: :class:`set` of :class:`str`
        :param vms: List of virtual machines that belong to the protection group. This
            is a combined list of virtual machines from the dynamic vm name and
            the individual list of virtual machines specified during creation
            of the protection group.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``VirtualMachine``. When methods return a value of this class as a
            return value, the attribute will contain identifiers for the
            resource type: ``VirtualMachine``.
        :type  snapshots: :class:`set` of :class:`str`
        :param snapshots: List of snapshots taken for the protection group.
            When clients pass a value of this class as a parameter, the
            attribute must contain identifiers for the resource type:
            ``com.vmware.snapservice.protection_group.snapshot``. When methods
            return a value of this class as a return value, the attribute will
            contain identifiers for the resource type:
            ``com.vmware.snapservice.protection_group.snapshot``.
        :type  locked: :class:`bool`
        :param locked: Indicates if the protection group is to be locked. A locked
            protection group cannot be modified or deleted by the user. All
            snapshots associated with the protection group will be secure and
            cannot be deleted. The system will automatically delete these
            snapshots upon expiry based on the retention period
        :type  guid: :class:`str`
        :param guid: The Global identifier of the protection group, which can be used to
            associate protection groups created on remote sites as part of
            replication configurations
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional because it was added in a newer version
            than its parent node.
        :type  replication_policies: :class:`list` of :class:`ReplicationPolicy`
        :param replication_policies: Replication configuration for the protection group specified by the
            user.
            This attribute was added in **vSphere API 9.0.0.0**.
            This attribute is optional because it was added in a newer version
            than its parent node.
        """
        self.name = name
        self.status = status
        self.target_entities = target_entities
        self.snapshot_policies = snapshot_policies
        self.last_snapshot_time = last_snapshot_time
        self.oldest_snapshot_time = oldest_snapshot_time
        self.vms = vms
        self.snapshots = snapshots
        self.locked = locked
        self.guid = guid
        self.replication_policies = replication_policies
        VapiStruct.__init__(self)


ProtectionGroupInfo._set_binding_type(type.StructType(
    'com.vmware.snapservice.protection_group_info', {
        'name': type.StringType(),
        'status': type.ReferenceType(__name__, 'ProtectionGroupStatus'),
        'target_entities': type.ReferenceType(__name__, 'TargetEntities'),
        'snapshot_policies': type.ListType(type.ReferenceType(__name__, 'SnapshotPolicy')),
        'last_snapshot_time': type.OptionalType(type.DateTimeType()),
        'oldest_snapshot_time': type.OptionalType(type.DateTimeType()),
        'vms': type.SetType(type.IdType()),
        'snapshots': type.SetType(type.IdType()),
        'locked': type.BooleanType(),
        'guid': type.OptionalType(type.StringType()),
        'replication_policies': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'ReplicationPolicy'))),
    },
    ProtectionGroupInfo,
    False,
    None))



class Reason(VapiStruct):
    """
    The ``Reason`` contains the details of the data protection reason for the
    respective error/warning.
    This class was added in **vSphere API 9.0.0.0**.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 messages=None,
                ):
        """
        :type  messages: :class:`list` of :class:`com.vmware.vapi.std_client.LocalizableMessage`
        :param messages: List of localized messages. 
            
            One of the use case is to add the chain of localized
            messages/errors for a single error.
            This attribute was added in **vSphere API 9.0.0.0**.
        """
        self.messages = messages
        VapiStruct.__init__(self)


Reason._set_binding_type(type.StructType(
    'com.vmware.snapservice.reason', {
        'messages': type.ListType(type.ReferenceType('com.vmware.vapi.std_client', 'LocalizableMessage')),
    },
    Reason,
    False,
    None))



class ClusterPairs(VapiInterface):
    """
    The ``ClusterPairs`` class provides methods for managing cluster pairs.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.cluster_pairs'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClusterPairsStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'create_task': 'create$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})
        self._VAPI_OPERATION_IDS.update({'create_precheck_task': 'create_precheck$task'})

    class ConnectionStatus(Enum):
        """
        The ``ClusterPairs.ConnectionStatus`` class contains the supported values
        for the cluster pair.
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
        Cluster pair is in a healthy state

        """
        WARNING = None
        """
        There are some warnings related to the cluster pair.

        """
        ERROR = None
        """
        Cluter pair has critical issues.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConnectionStatus` instance.
            """
            Enum.__init__(string)

    ConnectionStatus._set_values({
        'OK': ConnectionStatus('OK'),
        'WARNING': ConnectionStatus('WARNING'),
        'ERROR': ConnectionStatus('ERROR'),
    })
    ConnectionStatus._set_binding_type(type.EnumType(
        'com.vmware.snapservice.cluster_pairs.connection_status',
        ConnectionStatus))


    class FilterSpec(VapiStruct):
        """
        The ``ClusterPairs.FilterSpec`` class contains attributes used to filter
        the results when listing cluster pairs. If multiple attributes are
        specified, only cluster pairs matching all of the attributes will be
        returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster_pairs=None,
                     local_clusters=None,
                    ):
            """
            :type  cluster_pairs: :class:`set` of :class:`str` or ``None``
            :param cluster_pairs: Identifiers of clusters pairs that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.cluster_pair``. When methods return a
                value of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.cluster_pair``.
                If None or empty, cluster pairs with any identifier match the
                filter.
            :type  local_clusters: :class:`set` of :class:`str` or ``None``
            :param local_clusters: Identifier of the local clusters that can match the filter. Only
                cluster pairs with the specified local cluster would be returned.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, clusters with any identifier match the filter.
            """
            self.cluster_pairs = cluster_pairs
            self.local_clusters = local_clusters
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.filter_spec', {
            'cluster_pairs': type.OptionalType(type.SetType(type.IdType())),
            'local_clusters': type.OptionalType(type.SetType(type.IdType())),
        },
        FilterSpec,
        False,
        None))


    class LocalClusterMemberSpec(VapiStruct):
        """
        The ``ClusterPairs.LocalClusterMemberSpec`` class contains attributes that
        describe specification for a local cluster member of the cluster pair. This
        is to be included in the :class:`ClusterPairs.CreateSpec` for creating a
        cluster pair.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                    ):
            """
            :type  cluster: :class:`str`
            :param cluster: Identifier of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            """
            self.cluster = cluster
            VapiStruct.__init__(self)


    LocalClusterMemberSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.local_cluster_member_spec', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        },
        LocalClusterMemberSpec,
        False,
        None))


    class PeerClusterMemberSpec(VapiStruct):
        """
        The ``ClusterPairs.PeerClusterMemberSpec`` class contains attributes that
        describe specification for a peer cluster member of the cluster pair. This
        is to be included in the :class:`ClusterPairs.CreateSpec` for creating a
        cluster pair.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     site=None,
                     cluster=None,
                    ):
            """
            :type  site: :class:`str`
            :param site: Identifier of the site.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  cluster: :class:`str`
            :param cluster: Identifier of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            """
            self.site = site
            self.cluster = cluster
            VapiStruct.__init__(self)


    PeerClusterMemberSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.peer_cluster_member_spec', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
        },
        PeerClusterMemberSpec,
        False,
        None))


    class CreateSpec(VapiStruct):
        """
        The ``ClusterPairs.CreateSpec`` class contains attributes that describe
        specification for creating a cluster pair.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     local_cluster=None,
                     peer_cluster=None,
                    ):
            """
            :type  local_cluster: :class:`ClusterPairs.LocalClusterMemberSpec`
            :param local_cluster: Local cluster member of the cluster pair. Must be a cluster form
                the local site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  peer_cluster: :class:`ClusterPairs.PeerClusterMemberSpec`
            :param peer_cluster: Peer cluster member of the cluster pair. In the first release the
                peer cluster must be from a remote site.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.local_cluster = local_cluster
            self.peer_cluster = peer_cluster
            VapiStruct.__init__(self)


    CreateSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.create_spec', {
            'local_cluster': type.ReferenceType(__name__, 'ClusterPairs.LocalClusterMemberSpec'),
            'peer_cluster': type.ReferenceType(__name__, 'ClusterPairs.PeerClusterMemberSpec'),
        },
        CreateSpec,
        False,
        None))


    class MemberInfo(VapiStruct):
        """
        The ``ClusterPairs.MemberInfo`` class contains details regarding the
        cluster pair member.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     site=None,
                     vcenter=None,
                     cluster=None,
                     cluster_name=None,
                    ):
            """
            :type  site: :class:`str`
            :param site: Identifier of the site that this cluster belongs to.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  vcenter: :class:`str`
            :param vcenter: Identifier of the vcenter. This is the GUID.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  cluster: :class:`str`
            :param cluster: Identifier of the member cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will be an identifier for
                the resource type: ``ClusterComputeResource``.
            :type  cluster_name: :class:`str`
            :param cluster_name: Name of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.site = site
            self.vcenter = vcenter
            self.cluster = cluster
            self.cluster_name = cluster_name
            VapiStruct.__init__(self)


    MemberInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.member_info', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'vcenter': type.StringType(),
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'cluster_name': type.StringType(),
        },
        MemberInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``ClusterPairs.Info`` class contains details regarding the cluster
        pair.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'connection_status',
                {
                    'WARNING' : [('connection_warnings', True)],
                    'ERROR' : [('connection_warnings', True), ('connection_errors', True)],
                    'OK' : [],
                }
            ),
        ]



        def __init__(self,
                     local_cluster=None,
                     peer_cluster=None,
                     connection_status=None,
                     connection_state_updated_at=None,
                     connection_warnings=None,
                     connection_errors=None,
                     in_use=None,
                    ):
            """
            :type  local_cluster: :class:`ClusterPairs.MemberInfo`
            :param local_cluster: First member of the cluster pair. Cluster from the local site that
                is a member of the cluster pair.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  peer_cluster: :class:`ClusterPairs.MemberInfo`
            :param peer_cluster: Second member of the cluster pair. Peer cluster that is a member of
                the clutser pair.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  connection_status: :class:`ClusterPairs.ConnectionStatus`
            :param connection_status: Connection status of the cluster pairing.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  connection_state_updated_at: :class:`datetime.datetime` or ``None``
            :param connection_state_updated_at: Time at which the cluster pair connection state is checked.
                This attribute was added in **vSphere API 9.0.0.0**.
                is None if there is no check cluster pair connection state
            :type  connection_warnings: :class:`list` of :class:`Reason`
            :param connection_warnings: List of localized warnings associated with the cluster pair.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``connectionStatus`` is one of
                :attr:`ClusterPairs.ConnectionStatus.WARNING` or
                :attr:`ClusterPairs.ConnectionStatus.ERROR`.
            :type  connection_errors: :class:`list` of :class:`Reason`
            :param connection_errors: List of localized errors associated with the cluster pair.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``connectionStatus`` is
                :attr:`ClusterPairs.ConnectionStatus.ERROR`.
            :type  in_use: :class:`bool`
            :param in_use: Cluster pair is in use for replication.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.local_cluster = local_cluster
            self.peer_cluster = peer_cluster
            self.connection_status = connection_status
            self.connection_state_updated_at = connection_state_updated_at
            self.connection_warnings = connection_warnings
            self.connection_errors = connection_errors
            self.in_use = in_use
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.info', {
            'local_cluster': type.ReferenceType(__name__, 'ClusterPairs.MemberInfo'),
            'peer_cluster': type.ReferenceType(__name__, 'ClusterPairs.MemberInfo'),
            'connection_status': type.ReferenceType(__name__, 'ClusterPairs.ConnectionStatus'),
            'connection_state_updated_at': type.OptionalType(type.DateTimeType()),
            'connection_warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Reason'))),
            'connection_errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Reason'))),
            'in_use': type.BooleanType(),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``ClusterPairs.ListItem`` class contains information about a site
        returned by :func:`ClusterPairs.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster_pair=None,
                     info=None,
                    ):
            """
            :type  cluster_pair: :class:`str`
            :param cluster_pair: Identifier of the cluster pair.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.cluster_pair``. When methods return a
                value of this class as a return value, the attribute will be an
                identifier for the resource type:
                ``com.vmware.snapservice.cluster_pair``.
            :type  info: :class:`ClusterPairs.Info`
            :param info: Information regarding the cluster pair.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cluster_pair = cluster_pair
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.list_item', {
            'cluster_pair': type.IdType(resource_types='com.vmware.snapservice.cluster_pair'),
            'info': type.ReferenceType(__name__, 'ClusterPairs.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``ClusterPairs.ListResult`` class represents the result of
        :func:`ClusterPairs.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`ClusterPairs.ListItem`
            :param items: List of cluster pairs.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.cluster_pairs.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'ClusterPairs.ListItem')),
        },
        ListResult,
        False,
        None))




    def create_task(self,
               spec,
               ):
        """
        Create a new cluster pair.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`ClusterPairs.CreateSpec`
        :param spec: Specification for creating the cluster pair.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the operation is attempted without a site pair.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If caller tries to create already existing cluster pair.
        """
        task_id = self._invoke('create$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.snapservice.cluster_pair'))
        return task_instance

    def list(self,
             filter=None,
             ):
        """
        List the cluster pairs.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`ClusterPairs.FilterSpec` or ``None``
        :param filter: Specification of matching cluster pairs for which information
            should be returned.
            If None, the behavior is equivalent to a
            :class:`ClusterPairs.FilterSpec` with all attributes None which
            means all cluster pairs match the filter.
        :rtype: :class:`ClusterPairs.ListResult`
        :return: Information about the cluster pairs matching the
            :class:`ClusterPairs.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``filter`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })


    def delete_task(self,
               cp,
               ):
        """
        Delete the specified cluster-pair.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cp: :class:`str`
        :param cp: ClusterPair identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.cluster_pair``.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the ``cp`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If caller tries to delete the cluster-pair with active protection
            groups.
        """
        task_id = self._invoke('delete$task',
                                {
                                'cp': cp,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance

    def get(self,
            cp,
            ):
        """
        Get the detailed information regarding the specified cluster pair.
        This method was added in **vSphere API 9.0.0.0**.

        :type  cp: :class:`str`
        :param cp: Identifier of the cluster pair.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.cluster_pair``.
        :rtype: :class:`ClusterPairs.Info`
        :return: Information about the specified cluster pair.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the ``cp`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If ``cp`` format is not valid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        """
        return self._invoke('get',
                            {
                            'cp': cp,
                            })

    def create_precheck(self,
                        spec,
                        ):
        """
        Precheck validation for creating a new cluster pair.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`ClusterPairs.CreateSpec`
        :param spec: Precheck specification for creating the cluster pair.
        :rtype: :class:`PrecheckResult`
        :return: Precheck result details with validation and status.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If caller tries to create already existing cluster pair.
        """
        return self._invoke('create_precheck',
                            {
                            'spec': spec,
                            })

    def create_precheck_task(self,
                        spec,
                        ):
        """
        Precheck validation for creating a new cluster pair.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`ClusterPairs.CreateSpec`
        :param spec: Precheck specification for creating the cluster pair.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.AlreadyExists` 
            If caller tries to create already existing cluster pair.
        """
        task_id = self._invoke('create_precheck$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.ReferenceType(__name__, 'PrecheckResult'))
        return task_instance
class Sessions(VapiInterface):
    """
    The ``Sessions`` class allows API clients to manage snapservice session
    tokens including creating, deleting and obtaining information about
    sessions. 
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.sessions'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SessionsStub)
        self._VAPI_OPERATION_IDS = {}

    class Info(VapiStruct):
        """
        Represents data associated with an API session.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     user=None,
                     created_time=None,
                     last_accessed_time=None,
                    ):
            """
            :type  user: :class:`str`
            :param user: Fully qualified name of the end user that created the session, for
                example Administrator\\\\@vsphere.local. A typical use case for
                this information is in Graphical User Interfaces (GUI) or logging
                systems to visualize the identity of the current user.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  created_time: :class:`datetime.datetime`
            :param created_time: Time when the session was created.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  last_accessed_time: :class:`datetime.datetime`
            :param last_accessed_time: Last time this session was used by passing the session token for
                invoking an API.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.user = user
            self.created_time = created_time
            self.last_accessed_time = last_accessed_time
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.sessions.info', {
            'user': type.StringType(),
            'created_time': type.DateTimeType(),
            'last_accessed_time': type.DateTimeType(),
        },
        Info,
        False,
        None))



    def create(self):
        """
        Creates a session with the API. This is the equivalent of login. This
        method exchanges user credentials supplied in the security context for
        a session token that is to be used for authenticating subsequent calls.
        
        To authenticate subsequent calls clients are expected to include the
        session token. For REST API calls the HTTP ``vmware-api-session-id``
        header field should be used for this.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`str`
        :return: Newly created session token to be used for authenticating further
            requests.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if session creation fails due to server specific issues, for
            example connection to a back end component is failing. Due to the
            security nature of this API further details will not be disclosed
            in the exception. Please refer to component health information,
            administrative logs and product specific documentation for possible
            causes.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session creation fails due to request specific issues. Due
            to the security nature of the API the details of the error are not
            disclosed. 
            
            Please check the following preconditions if using a SAML token to
            authenticate: 
            
            * the supplied token is delegate-able.
            * the time of client and server system are synchronized.
            * the token supplied is valid.
            * if bearer tokens are used check that system configuration allows
              the API endpoint to accept such tokens.
        """
        return self._invoke('create', None)

    def delete(self):
        """
        Terminates the validity of a session token. This is the equivalent of
        log out. 
        
        A session token is expected as part of the request. 
        This method was added in **vSphere API 9.0.0.0**.


        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session id is missing from the request or the corresponding
            session object cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if session deletion fails due to server specific issues, for
            example connection to a back end component is failing. Due to the
            security nature of this API further details will not be disclosed
            in the exception. Please refer to component health information,
            administrative logs and product specific documentation for possible
            causes.
        """
        return self._invoke('delete', None)

    def get(self):
        """
        Returns information about the current session. This method expects a
        valid session token to be supplied. 
        
        A side effect of invoking this method may be a change to the session's
        last accessed time to the current time if this is supported by the
        session implementation. Invoking any other method in the API will also
        update the session's last accessed time. 
        
        This API is meant to serve the needs of various front end projects that
        may want to display the name of the user. Examples of this include
        various web based user interfaces and logging facilities.
        This method was added in **vSphere API 9.0.0.0**.


        :rtype: :class:`Sessions.Info`
        :return: Information about the session.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the session id is missing from the request or the corresponding
            session object cannot be found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if session retrieval fails due to server specific issues e.g.
            connection to back end component is failing. Due to the security
            nature of this API further details will not be disclosed in the
            error. Please refer to component health information, administrative
            logs and product specific documentation for possible causes.
        """
        return self._invoke('get', None)
class Sites(VapiInterface):
    """
    The ``Sites`` class provides methods for managing site pairing between
    local and remote sites.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.sites'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _SitesStub)
        self._VAPI_OPERATION_IDS = {}
        self._VAPI_OPERATION_IDS.update({'add_task': 'add$task'})
        self._VAPI_OPERATION_IDS.update({'update_task': 'update$task'})
        self._VAPI_OPERATION_IDS.update({'delete_task': 'delete$task'})

    class ConnectionStatus(Enum):
        """
        The ``Sites.ConnectionStatus`` class contains the supported values for the
        paired site connection status.
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
        CONNECTED = None
        """
        Paired site have healthy connection with the local site.

        """
        ERROR = None
        """
        Paired site have connection issues with the local site.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ConnectionStatus` instance.
            """
            Enum.__init__(string)

    ConnectionStatus._set_values({
        'CONNECTED': ConnectionStatus('CONNECTED'),
        'ERROR': ConnectionStatus('ERROR'),
    })
    ConnectionStatus._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.connection_status',
        ConnectionStatus))


    class ServiceType(Enum):
        """
        The ``Sites.ServiceType`` class contains the supported values for the
        service type.
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
        SS = None
        """
        Snapshot Service.

        """
        SRM = None
        """
        Site Recovery Manager.

        """
        HMS = None
        """
        HBR Manager Service.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ServiceType` instance.
            """
            Enum.__init__(string)

    ServiceType._set_values({
        'SS': ServiceType('SS'),
        'SRM': ServiceType('SRM'),
        'HMS': ServiceType('HMS'),
    })
    ServiceType._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.service_type',
        ServiceType))


    class ProbeStatus(Enum):
        """
        The ``Sites.ProbeStatus`` class contains the supported values for the
        remote vCenter and Data Protection Virtual Appliance probe status.
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
        PARTIAL = None
        """
        Probe result for remote vCenter and Data Protection Virtual Appliance is
        partial as the vCenter certificate is not accepted by the user. Probe API
        is expected to be invoked again by passing the vCenter certificate,
        returned by the previous call to the Probe API, as an input. Resending of
        the certificate returned as an input will mean the user has accepted the
        certificate.

        """
        COMPLETED = None
        """
        Probe for remote vCenter and Data Protection Virtual Appliance is
        completed. User can proceed with invoking add site API. If vCenter or Data
        Protection appliance certificates returned by Probe API are already not
        trustred, these certificates need to be accepted by the user and supplied
        as input to add site API.

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`ProbeStatus` instance.
            """
            Enum.__init__(string)

    ProbeStatus._set_values({
        'PARTIAL': ProbeStatus('PARTIAL'),
        'COMPLETED': ProbeStatus('COMPLETED'),
    })
    ProbeStatus._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.probe_status',
        ProbeStatus))


    class CertificateInfo(VapiStruct):
        """
        The ``Sites.CertificateInfo`` class contains attributes that provide the
        site certificate details.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     certificate=None,
                     thumbprint=None,
                     dns_names=None,
                     trusted=None,
                    ):
            """
            :type  certificate: :class:`str`
            :param certificate: PEM format X.509 SSL certificate of the remote site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  thumbprint: :class:`str`
            :param thumbprint: SHA256 thumbprint of the remote site certificate.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  dns_names: :class:`list` of :class:`str` or ``None``
            :param dns_names: This attribute was added in **vSphere API 9.0.0.0**.
                DNS names of the server extracted from the certificate. It is
                :class:`set` if certificate has the DNS information.
            :type  trusted: :class:`bool`
            :param trusted: Is remote site certificate trusted.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.certificate = certificate
            self.thumbprint = thumbprint
            self.dns_names = dns_names
            self.trusted = trusted
            VapiStruct.__init__(self)


    CertificateInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.certificate_info', {
            'certificate': type.StringType(),
            'thumbprint': type.StringType(),
            'dns_names': type.OptionalType(type.ListType(type.StringType())),
            'trusted': type.BooleanType(),
        },
        CertificateInfo,
        False,
        None))


    class UserCredentials(VapiStruct):
        """
        The ``Sites.UserCredentials`` class contains attributes used to provide
        user credentials for the remote vCenter.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     user=None,
                     password=None,
                    ):
            """
            :type  user: :class:`str`
            :param user: Username of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  password: :class:`str`
            :param password: Password of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.user = user
            self.password = password
            VapiStruct.__init__(self)


    UserCredentials._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.user_credentials', {
            'user': type.StringType(),
            'password': type.SecretType(),
        },
        UserCredentials,
        False,
        None))


    class ConnectionState(VapiStruct):
        """
        The ``Sites.ConnectionState`` class contains information regarding
        connection status from local to remote site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'connection_status',
                {
                    'ERROR' : [('errors', True)],
                    'CONNECTED' : [],
                }
            ),
        ]



        def __init__(self,
                     connection_status=None,
                     errors=None,
                     warnings=None,
                    ):
            """
            :type  connection_status: :class:`Sites.ConnectionStatus`
            :param connection_status: Connection status for the site and service. For site, connection
                status represents that no errors are observed for various services
                for both sites. For service, connection status represents that no
                errors are observed for the service in question.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  errors: :class:`list` of :class:`Reason`
            :param errors: List of errors reported for the service or the paired sites.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``connectionStatus`` is :attr:`Sites.ConnectionStatus.ERROR`.
            :type  warnings: :class:`list` of :class:`Reason` or ``None``
            :param warnings: List of warnings reported for the service or the paired sites.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, there are no warnings reported for the service or the
                paired sites.
            """
            self.connection_status = connection_status
            self.errors = errors
            self.warnings = warnings
            VapiStruct.__init__(self)


    ConnectionState._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.connection_state', {
            'connection_status': type.ReferenceType(__name__, 'Sites.ConnectionStatus'),
            'errors': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Reason'))),
            'warnings': type.OptionalType(type.ListType(type.ReferenceType(__name__, 'Reason'))),
        },
        ConnectionState,
        False,
        None))


    class VCenterInfo(VapiStruct):
        """
        The ``Sites.VCenterInfo`` class contains details regarding the vCenter of
        the Site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     host=None,
                     port=None,
                     vcenter=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  host: :class:`str`
            :param host: Host of vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  port: :class:`long` or ``None``
            :param port: This attribute was added in **vSphere API 9.0.0.0**.
                If None, default SSL port will be used for the vCenter.
            :type  vcenter: :class:`str`
            :param vcenter: GUID of vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.host = host
            self.port = port
            self.vcenter = vcenter
            VapiStruct.__init__(self)


    VCenterInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.V_center_info', {
            'name': type.StringType(),
            'host': type.StringType(),
            'port': type.OptionalType(type.IntegerType()),
            'vcenter': type.StringType(),
        },
        VCenterInfo,
        False,
        None))


    class Service(VapiStruct):
        """
        The ``Sites.Service`` class contains details of the service.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     id=None,
                     type=None,
                     name=None,
                     url=None,
                     connection_state=None,
                    ):
            """
            :type  id: :class:`str`
            :param id: ID of service.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  type: :class:`Sites.ServiceType`
            :param type: Type of service.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  name: :class:`str`
            :param name: Name of service.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  url: :class:`str`
            :param url: URL of service;
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  connection_state: :class:`Sites.ConnectionState`
            :param connection_state: Connection status of service.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.id = id
            self.type = type
            self.name = name
            self.url = url
            self.connection_state = connection_state
            VapiStruct.__init__(self)


    Service._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.service', {
            'id': type.IdType(resource_types='com.vmware.snapservice.site'),
            'type': type.ReferenceType(__name__, 'Sites.ServiceType'),
            'name': type.StringType(),
            'url': type.URIType(),
            'connection_state': type.ReferenceType(__name__, 'Sites.ConnectionState'),
        },
        Service,
        False,
        None))


    class PairingSummary(VapiStruct):
        """
        The ``Sites.PairingSummary`` class contains summary of the paired site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     site=None,
                     connection_state=None,
                     paired_services=None,
                    ):
            """
            :type  site: :class:`str`
            :param site: ID of paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  connection_state: :class:`Sites.ConnectionState`
            :param connection_state: Connection status of paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  paired_services: :class:`list` of :class:`Sites.ServiceType`
            :param paired_services: List of services from the local site that are paired with the
                services from the paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.site = site
            self.connection_state = connection_state
            self.paired_services = paired_services
            VapiStruct.__init__(self)


    PairingSummary._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.pairing_summary', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'connection_state': type.ReferenceType(__name__, 'Sites.ConnectionState'),
            'paired_services': type.ListType(type.ReferenceType(__name__, 'Sites.ServiceType')),
        },
        PairingSummary,
        False,
        None))


    class PairingInfo(VapiStruct):
        """
        The ``Sites.PairingInfo`` class contains details of the paired site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     site=None,
                     connection_state=None,
                     services=None,
                    ):
            """
            :type  site: :class:`str`
            :param site: ID of paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  connection_state: :class:`Sites.ConnectionState`
            :param connection_state: Connection status of paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  services: :class:`list` of :class:`Sites.Service`
            :param services: List of services for the paired site.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.site = site
            self.connection_state = connection_state
            self.services = services
            VapiStruct.__init__(self)


    PairingInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.pairing_info', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'connection_state': type.ReferenceType(__name__, 'Sites.ConnectionState'),
            'services': type.ListType(type.ReferenceType(__name__, 'Sites.Service')),
        },
        PairingInfo,
        False,
        None))


    class Summary(VapiStruct):
        """
        The ``Sites.Summary`` class contains details regarding the Site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     local=None,
                     vcenter_info=None,
                     pairing_summaries=None,
                     in_use=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  local: :class:`bool`
            :param local: Is the site local or remote.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vcenter_info: :class:`Sites.VCenterInfo`
            :param vcenter_info: Information of vCenter for the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  pairing_summaries: :class:`list` of :class:`Sites.PairingSummary`
            :param pairing_summaries: Pairing summary for the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  in_use: :class:`bool`
            :param in_use: Site is in use for replication.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.local = local
            self.vcenter_info = vcenter_info
            self.pairing_summaries = pairing_summaries
            self.in_use = in_use
            VapiStruct.__init__(self)


    Summary._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.summary', {
            'name': type.StringType(),
            'local': type.BooleanType(),
            'vcenter_info': type.ReferenceType(__name__, 'Sites.VCenterInfo'),
            'pairing_summaries': type.ListType(type.ReferenceType(__name__, 'Sites.PairingSummary')),
            'in_use': type.BooleanType(),
        },
        Summary,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Sites.Info`` class contains details regarding the Site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                     local=None,
                     vcenter_info=None,
                     pairing_infos=None,
                     services=None,
                     in_use=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  local: :class:`bool`
            :param local: Indicates whether or not a site is local. The current logged-in
                site is considered to be local site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vcenter_info: :class:`Sites.VCenterInfo`
            :param vcenter_info: Information of vCenter for the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  pairing_infos: :class:`list` of :class:`Sites.PairingInfo`
            :param pairing_infos: Pairing details for the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  services: :class:`list` of :class:`Sites.Service`
            :param services: List of services for the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  in_use: :class:`bool`
            :param in_use: Site is in use for replication.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            self.local = local
            self.vcenter_info = vcenter_info
            self.pairing_infos = pairing_infos
            self.services = services
            self.in_use = in_use
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.info', {
            'name': type.StringType(),
            'local': type.BooleanType(),
            'vcenter_info': type.ReferenceType(__name__, 'Sites.VCenterInfo'),
            'pairing_infos': type.ListType(type.ReferenceType(__name__, 'Sites.PairingInfo')),
            'services': type.ListType(type.ReferenceType(__name__, 'Sites.Service')),
            'in_use': type.BooleanType(),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Sites.ListItem`` class contains information about a site returned by
        :func:`Sites.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     site=None,
                     summary=None,
                    ):
            """
            :type  site: :class:`str`
            :param site: Identifier of the site.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.site``.
            :type  summary: :class:`Sites.Summary`
            :param summary: Summary of the site.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.site = site
            self.summary = summary
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.list_item', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'summary': type.ReferenceType(__name__, 'Sites.Summary'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Sites.ListResult`` class represents the result of :func:`Sites.list`
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
            :type  items: :class:`list` of :class:`Sites.ListItem`
            :param items: List of sites.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Sites.ListItem')),
        },
        ListResult,
        False,
        None))


    class FilterSpec(VapiStruct):
        """
        The ``Sites.FilterSpec`` class contains attributes used to filter the
        results when listing sites. If multiple attributes are specified, only
        sites matching all of the attributes will be returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     sites=None,
                     local=None,
                     paired=None,
                    ):
            """
            :type  sites: :class:`set` of :class:`str` or ``None``
            :param sites: Identifiers of sites that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.site``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type: ``com.vmware.snapservice.site``.
                If None or empty, sites with any identifier match the filter.
            :type  local: :class:`bool` or ``None``
            :param local: If set to true it will only match the local site.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or false, will return all sites, local or remote that match
                the filter.
            :type  paired: :class:`bool` or ``None``
            :param paired: If set to true it will include the remote sites that are paired in
                SnapService.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or false, will return all sites, including the ones not
                paired in SnapService, that match the filter.
            """
            self.sites = sites
            self.local = local
            self.paired = paired
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.filter_spec', {
            'sites': type.OptionalType(type.SetType(type.IdType())),
            'local': type.OptionalType(type.BooleanType()),
            'paired': type.OptionalType(type.BooleanType()),
        },
        FilterSpec,
        False,
        None))


    class VcenterConnectionSpec(VapiStruct):
        """
        The ``Sites.VcenterConnectionSpec`` class contains attributes used to
        provide connection specifications for the remote vCenter.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     host=None,
                     port=None,
                    ):
            """
            :type  host: :class:`str`
            :param host: Host of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  port: :class:`long` or ``None``
            :param port: This attribute was added in **vSphere API 9.0.0.0**.
                If None, default SSL port will be used for the remote vCenter.
            """
            self.host = host
            self.port = port
            VapiStruct.__init__(self)


    VcenterConnectionSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.vcenter_connection_spec', {
            'host': type.StringType(),
            'port': type.OptionalType(type.IntegerType()),
        },
        VcenterConnectionSpec,
        False,
        None))


    class ProbeSpec(VapiStruct):
        """
        The ``Sites.ProbeSpec`` class contains attributes used to probe remote site
        vCenter and Data Protection Virtual Appliance connection.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vcenter_connection_spec=None,
                     vcenter_creds=None,
                     vcenter_certificate=None,
                    ):
            """
            :type  vcenter_connection_spec: :class:`Sites.VcenterConnectionSpec`
            :param vcenter_connection_spec: Connection specifications of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vcenter_creds: :class:`Sites.UserCredentials` or ``None``
            :param vcenter_creds: Credentials for the remote site with enough permissions. 
                
                The vCenter credentials are kept optional for future extensibility.
                Currently, API is expected to throw validation error if vCenter
                credentials are not supplied.
                This attribute was added in **vSphere API 9.0.0.0**.
                Must be :class:`set` for current release. Field is set to optional
                for future use cases to support different authentication
                mechanisms.
            :type  vcenter_certificate: :class:`str` or ``None``
            :param vcenter_certificate: Certificate of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If :class:`set`, remote vCenter certificate has been accepted by
                the user. If vCenter Certificate returned by probe API is already
                not trusted, it is expected to be supplied here.
            """
            self.vcenter_connection_spec = vcenter_connection_spec
            self.vcenter_creds = vcenter_creds
            self.vcenter_certificate = vcenter_certificate
            VapiStruct.__init__(self)


    ProbeSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.probe_spec', {
            'vcenter_connection_spec': type.ReferenceType(__name__, 'Sites.VcenterConnectionSpec'),
            'vcenter_creds': type.OptionalType(type.ReferenceType(__name__, 'Sites.UserCredentials')),
            'vcenter_certificate': type.OptionalType(type.StringType()),
        },
        ProbeSpec,
        False,
        None))


    class ProbeResult(VapiStruct):
        """
        The ``Sites.ProbeResult`` class contains information regarding the remote
        vCenter and Data Protection Virtual Appliance connection probe results.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'status',
                {
                    'COMPLETED' : [('va_certificate', False)],
                    'PARTIAL' : [],
                }
            ),
        ]



        def __init__(self,
                     status=None,
                     vcenter_certificate=None,
                     va_certificate=None,
                    ):
            """
            :type  status: :class:`Sites.ProbeStatus`
            :param status: Status of remote vCenter and Data Protection Virtual Appliance
                connection probe.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vcenter_certificate: :class:`Sites.CertificateInfo`
            :param vcenter_certificate: Certificate of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  va_certificate: :class:`Sites.CertificateInfo` or ``None``
            :param va_certificate: Certificate of the remote Data Protection Virtual Appliance.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, probe status is partial and vCenter certificate needs to
                be accepted by the user.
            """
            self.status = status
            self.vcenter_certificate = vcenter_certificate
            self.va_certificate = va_certificate
            VapiStruct.__init__(self)


    ProbeResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.probe_result', {
            'status': type.ReferenceType(__name__, 'Sites.ProbeStatus'),
            'vcenter_certificate': type.ReferenceType(__name__, 'Sites.CertificateInfo'),
            'va_certificate': type.OptionalType(type.ReferenceType(__name__, 'Sites.CertificateInfo')),
        },
        ProbeResult,
        False,
        None))


    class AddSpec(VapiStruct):
        """
        The ``Sites.AddSpec`` class contains attributes to provide the details to
        add the remote site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vcenter_connection_spec=None,
                     vcenter_creds=None,
                     vcenter_certificate=None,
                     va_certificate=None,
                    ):
            """
            :type  vcenter_connection_spec: :class:`Sites.VcenterConnectionSpec`
            :param vcenter_connection_spec: Connection specifications of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vcenter_creds: :class:`Sites.UserCredentials` or ``None``
            :param vcenter_creds: Credentials for the remote site with enough permissions. 
                
                The vCenter credentials are kept optional for future extensibility.
                Currently, API is expected to throw validation error if vCenter
                credentials are not supplied.
                This attribute was added in **vSphere API 9.0.0.0**.
                Must be :class:`set` for current release. Field is set to optional
                for future use cases to support different authentication
                mechanisms.
            :type  vcenter_certificate: :class:`str` or ``None``
            :param vcenter_certificate: Certificate of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote vCenter certificate is already trusted.
            :type  va_certificate: :class:`str` or ``None``
            :param va_certificate: Certificate of the remote Data Protection Virtual Appliance.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote Data Protection Virtual Appliance certificate is
                already trusted.
            """
            self.vcenter_connection_spec = vcenter_connection_spec
            self.vcenter_creds = vcenter_creds
            self.vcenter_certificate = vcenter_certificate
            self.va_certificate = va_certificate
            VapiStruct.__init__(self)


    AddSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.add_spec', {
            'vcenter_connection_spec': type.ReferenceType(__name__, 'Sites.VcenterConnectionSpec'),
            'vcenter_creds': type.OptionalType(type.ReferenceType(__name__, 'Sites.UserCredentials')),
            'vcenter_certificate': type.OptionalType(type.StringType()),
            'va_certificate': type.OptionalType(type.StringType()),
        },
        AddSpec,
        False,
        None))


    class UpdateSpec(VapiStruct):
        """
        The ``Sites.UpdateSpec`` class contains attributes to provide the details
        to update the remote site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vcenter_connection_spec=None,
                     vcenter_creds=None,
                     vcenter_certificate=None,
                     va_certificate=None,
                    ):
            """
            :type  vcenter_connection_spec: :class:`Sites.VcenterConnectionSpec` or ``None``
            :param vcenter_connection_spec: Connection specifications of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, use existing vCenter connection specifications.
            :type  vcenter_creds: :class:`Sites.UserCredentials` or ``None``
            :param vcenter_creds: Credentials for the remote site with enough permissions. 
                
                The vCenter credentials are kept optional for future extensibility.
                Currently, API is expected to throw validation error if vCenter
                credentials are not supplied.
                This attribute was added in **vSphere API 9.0.0.0**.
                Must be :class:`set` for current release. Field is set to optional
                for future use cases to support different authentication
                mechanisms.
            :type  vcenter_certificate: :class:`str` or ``None``
            :param vcenter_certificate: Certificate of the remote vCenter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote vCenter certificate is already trusted.
            :type  va_certificate: :class:`str` or ``None``
            :param va_certificate: Certificate of the remote Data Protection Virtual Appliance.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None, remote Data Protection Virtual Appliance certificate is
                already trusted.
            """
            self.vcenter_connection_spec = vcenter_connection_spec
            self.vcenter_creds = vcenter_creds
            self.vcenter_certificate = vcenter_certificate
            self.va_certificate = va_certificate
            VapiStruct.__init__(self)


    UpdateSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.update_spec', {
            'vcenter_connection_spec': type.OptionalType(type.ReferenceType(__name__, 'Sites.VcenterConnectionSpec')),
            'vcenter_creds': type.OptionalType(type.ReferenceType(__name__, 'Sites.UserCredentials')),
            'vcenter_certificate': type.OptionalType(type.StringType()),
            'va_certificate': type.OptionalType(type.StringType()),
        },
        UpdateSpec,
        False,
        None))


    class DeleteSpec(VapiStruct):
        """
        The ``Sites.DeleteSpec`` class contains attributes used for breaking the
        pair with remote site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     vcenter_creds=None,
                    ):
            """
            :type  vcenter_creds: :class:`Sites.UserCredentials` or ``None``
            :param vcenter_creds: Remote site credentials with enough permissions to remove service
                accounts and permissions. 
                
                The vCenter credentials are kept optional for future extensibility.
                Currently, API is expected to throw validation error if vCenter
                credentials are not supplied.
                This attribute was added in **vSphere API 9.0.0.0**.
                Must be :class:`set` for current release. Field is set to optional
                for future use cases to support different authentication
                mechanisms.
            """
            self.vcenter_creds = vcenter_creds
            VapiStruct.__init__(self)


    DeleteSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.delete_spec', {
            'vcenter_creds': type.OptionalType(type.ReferenceType(__name__, 'Sites.UserCredentials')),
        },
        DeleteSpec,
        False,
        None))


    class DeleteOptions(VapiStruct):
        """
        The ``Sites.DeleteOptions`` class contains attributes to specify options
        used for breaking the pair with remote site.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     exclude_hms=None,
                     remote_site_failed=None,
                    ):
            """
            :type  exclude_hms: :class:`bool` or ``None``
            :param exclude_hms: Indicates whether or not we should skip breaking HMS pair
                This attribute was added in **vSphere API 9.0.0.0**.
                if None HMS pairing is removed.
            :type  remote_site_failed: :class:`bool` or ``None``
            :param remote_site_failed: Indicates whether the remote site failed. Consumer can use this
                option if remote site is no longer available and the remote site
                needs to be deleted. Network errors with remote site will be
                ignored if remoteSiteFailed field is set to true and remote site
                will be deleted from the local site.
                This attribute was added in **vSphere API 9.0.0.0**.
                if None break pair without force.
            """
            self.exclude_hms = exclude_hms
            self.remote_site_failed = remote_site_failed
            VapiStruct.__init__(self)


    DeleteOptions._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.delete_options', {
            'exclude_hms': type.OptionalType(type.BooleanType()),
            'remote_site_failed': type.OptionalType(type.BooleanType()),
        },
        DeleteOptions,
        False,
        None))



    def probe(self,
              spec,
              ):
        """
        Probe SSL connection to a remote vCenter and Data Protection Virtual
        Appliance. This API returns vCenter/Data Protection Virtual Appliance
        certificates. 
        
        If vCenter certificate is already not trusted, the API will return
        vCenter certificate with probe status as partial. User is expected to
        invoke probe API again with the user accepted vCenter certificate. Once
        the vCenter certificate accepted by the user is supplied to probe API,
        the API will return with probe status as completed along with Data
        Protection Virtual Appliance certificate. If Data Protection Virtual
        Appliance certificate is not trusted, user is expected to accept Data
        Protection appliance certificate and supply user accepted vCenter and
        Data Protection Virtual Appliance certificates as input to Add/Update
        site API. 
        
        If vCenter and Data Protection Virtual Appliance certificates are
        already trusted, the API will respond with probe status as completed.
        User can proceed with invoking Add/Update site API with no vCenter and
        Data Protection Virtual Appliance certificates.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Sites.ProbeSpec`
        :param spec: Spec used to probe remote vCenter and Data Protection Virtual
            Appliance connection.
        :rtype: :class:`Sites.ProbeResult`
        :return: Probe result containing remote vCenter and Data Protection Virtual
            Appliance certificates that can be used to call add or update site.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        return self._invoke('probe',
                            {
                            'spec': spec,
                            })


    def add_task(self,
            spec,
            ):
        """
        Add the remote site. As part of this call, local and remote site will
        be paired. In other words, it will setup services on both local and
        remote sites to be able to connect to each other to perform replication
        in either direction. 
        
        The logged in interactive user must be a member of Administrators group
        on local site to execute the operation. The remote user must be a
        member of Administrators group on remote site too. 
        
        If vCenter and Data Protection Virtual appliance certificates returned
        by Probe API are not trusted yet, respective certificate has to be
        accepted by the user and supplied as an input to this API.
        This method was added in **vSphere API 9.0.0.0**.

        :type  spec: :class:`Sites.AddSpec`
        :param spec: Spec used to add site.
        :rtype: :class:  `vmware.vapi.stdlib.client.task.Task`
        :return: Task instance
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            when the local site is already paired to a remote site.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.UnverifiedPeer` 
            If vCenter or virtual appliance certificate is not trusted and has
            not been supplied in the request.
        """
        task_id = self._invoke('add$task',
                                {
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.IdType(resource_types='com.vmware.snapservice.site'))
        return task_instance

    def list(self,
             filter=None,
             ):
        """
        List the local and remote sites.
        This method was added in **vSphere API 9.0.0.0**.

        :type  filter: :class:`Sites.FilterSpec` or ``None``
        :param filter: Specification of matching sites for which information should be
            returned.
            If None, the behavior is equivalent to a :class:`Sites.FilterSpec`
            with all attributes None which means all sites match the filter.
        :rtype: :class:`Sites.ListResult`
        :return: Information about the sites matching the :class:`Sites.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``filter`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            site,
            ):
        """
        Returns information about a site.
        This method was added in **vSphere API 9.0.0.0**.

        :type  site: :class:`str`
        :param site: Site identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.site``.
        :rtype: :class:`Sites.Info`
        :return: Information about the specified site.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the site is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``site`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        return self._invoke('get',
                            {
                            'site': site,
                            })


    def update_task(self,
               site,
               spec,
               ):
        """
        Repair the network connection between the two data protection sites,
        and/or the combined appliances. 
        
        Call this method when there are changes in VC or Data Protection
        Virtual Appliance FQDN/IP address, SSL certificate, or service account
        credentials. 
        
        If vCenter and Data Protection Virtual appliance certificates returned
        by Probe API are not trusted yet, respective certificate has to be
        accepted by the user and supplied as an input to this API. 
        
        The logged in interactive user must be a member of Administrators group
        on local site to execute the operation. The remote user must be a
        member of Administrators group on remote site too.
        This method was added in **vSphere API 9.0.0.0**.

        :type  site: :class:`str`
        :param site: ``vmodl.lang_client.ID`` existing remote site ID.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.site``.
        :type  spec: :class:`Sites.UpdateSpec`
        :param spec: ``Sites.UpdateSpec`` used to update the remote site connection
            info.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if there is any unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if ``site`` points to an unknown site.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        """
        task_id = self._invoke('update$task',
                                {
                                'site': site,
                                'spec': spec,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance


    def delete_task(self,
               site,
               spec,
               options=None,
               ):
        """
        Delete the specified remote site. Deleting a site which is not added
        via SnapService is not supported. 
        
        The logged in interactive user must be a member of Administrators group
        on local site to execute the operation. If the remote site is not
        failed, the remote user must be a member of Administrators group on
        remote site too.
        This method was added in **vSphere API 9.0.0.0**.

        :type  site: :class:`str`
        :param site: Site identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.site``.
        :type  spec: :class:`Sites.DeleteSpec`
        :param spec: Specification used for breaking site pair.
        :type  options: :class:`Sites.DeleteOptions` or ``None``
        :param options: Additional options to for deleting the site.
            If None, additional options :class:`Sites.DeleteOptions` for
            deleting site pair are skipped and default behavior for delete site
            is applied.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If the ``site`` is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``spec`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            If the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            If the caller is not authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unsupported` 
            If the API is not supported.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            If the caller is not authorized to perform the operation.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotAllowedInCurrentState` 
            If caller tries to delete site with active replications or a site
            which is not added via SnapService.
        """
        task_id = self._invoke('delete$task',
                                {
                                'site': site,
                                'spec': spec,
                                'options': options,
                                })
        task_svc = Tasks(self._config)
        task_instance = Task(task_id, task_svc, type.VoidType())
        return task_instance
class Tasks(VapiInterface):
    """
    The ``Tasks`` class provides methods for managing the tasks related to long
    running operations.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.tasks'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _TasksStub)
        self._VAPI_OPERATION_IDS = {}

    class FilterSpec(VapiStruct):
        """
        The ``Tasks.FilterSpec`` class contains attributes used to filter the
        results when listing tasks (see :func:`Tasks.list`). If multiple attributes
        are specified, only tasks matching all of the attributes match the filter. 
        
        Currently at least one of :attr:`Tasks.FilterSpec.tasks` or
        :attr:`Tasks.FilterSpec.services` must be specified and not empty.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     tasks=None,
                     operations=None,
                     services=None,
                     status=None,
                     users=None,
                    ):
            """
            :type  tasks: :class:`set` of :class:`str` or ``None``
            :param tasks: Identifiers of tasks that can match the filter.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.task``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type: ``com.vmware.snapservice.task``.
                This attribute may be None if other filters are specified. If None
                or empty, tasks with any identifier will match the filter.
            :type  operations: :class:`set` of :class:`str` or ``None``
            :param operations: Identifiers of operations. Tasks created by these operations match
                the filter (see
                :attr:`com.vmware.snapservice.tasks_client.CommonInfo.operation`). 
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.operation``. When methods return a value
                of this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.operation``.
                If None or empty, tasks associated with any operation will match
                the filter.
            :type  services: :class:`set` of :class:`str` or ``None``
            :param services: Identifiers of services. Tasks created by operations in these
                services match the filter (see
                :attr:`com.vmware.snapservice.tasks_client.CommonInfo.service`).
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``com.vmware.snapservice.service``. When methods return a value of
                this class as a return value, the attribute will contain
                identifiers for the resource type:
                ``com.vmware.snapservice.service``.
                This attribute may be None if ``tasks`` is specified. If this
                attribute is None or empty, tasks for any service will match the
                filter.
            :type  status: :class:`set` of :class:`com.vmware.snapservice.tasks_client.Status` or ``None``
            :param status: Status that a task must have to match the filter (see
                :attr:`com.vmware.snapservice.tasks_client.CommonInfo.status`).
                If None or empty, tasks with any status match the filter.
            :type  users: :class:`set` of :class:`str` or ``None``
            :param users: Users who must have initiated the operation for the associated task
                to match the filter (see
                :attr:`com.vmware.snapservice.tasks_client.CommonInfo.user`).
                If None or empty, tasks associated with operations initiated by any
                user match the filter.
            """
            self.tasks = tasks
            self.operations = operations
            self.services = services
            self.status = status
            self.users = users
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.tasks.filter_spec', {
            'tasks': type.OptionalType(type.SetType(type.IdType())),
            'operations': type.OptionalType(type.SetType(type.IdType())),
            'services': type.OptionalType(type.SetType(type.IdType())),
            'status': type.OptionalType(type.SetType(type.ReferenceType('com.vmware.snapservice.tasks_client', 'Status'))),
            'users': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Tasks.ListItem`` class contains information about a task returned by
        :func:`Tasks.list` method

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     task=None,
                     info=None,
                    ):
            """
            :type  task: :class:`str`
            :param task: Identifier of the task for which this entry belongs to.
                When clients pass a value of this class as a parameter, the
                attribute must be an identifier for the resource type:
                ``com.vmware.snapservice.task``. When methods return a value of
                this class as a return value, the attribute will be an identifier
                for the resource type: ``com.vmware.snapservice.task``.
            :type  info: :class:`com.vmware.snapservice.tasks_client.Info`
            :param info: Information regarding the task.
            """
            self.task = task
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.tasks.list_item', {
            'task': type.IdType(resource_types='com.vmware.snapservice.task'),
            'info': type.ReferenceType('com.vmware.snapservice.tasks_client', 'Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Tasks.ListResult`` class represents the result of :func:`Tasks.list`
        method.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Tasks.ListItem`
            :param items: List of tasks.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.tasks.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Tasks.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self,
             filter=None,
             ):
        """
        Returns information about at most 1000 visible (subject to permission
        checks) tasks matching the :class:`Tasks.FilterSpec`.

        :type  filter: :class:`Tasks.FilterSpec` or ``None``
        :param filter: Specification of matching tasks.
            if None, the behavior is equivalent to a :class:`Tasks.FilterSpec`
            with all attributes None which means all tasks match the filter.
        :rtype: :class:`Tasks.ListResult`
        :return: ListResult including details of all the tasks.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            if any of the specified parameters are invalid.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if a task's state cannot be accessed or over 1000 tasks matching
            the :class:`Tasks.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('list',
                            {
                            'filter': filter,
                            })

    def get(self,
            task,
            ):
        """
        Returns information about a task.

        :type  task: :class:`str`
        :param task: Task identifier.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.task``.
        :rtype: :class:`com.vmware.snapservice.tasks_client.Info`
        :return: Information about the specified task.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            if the system reports an error while responding to the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            if the task is not found.
        :raise: :class:`com.vmware.vapi.std.errors_client.ResourceInaccessible` 
            if the task's state cannot be accessed.
        :raise: :class:`com.vmware.vapi.std.errors_client.ServiceUnavailable` 
            if the system is unable to communicate with a service to complete
            the request.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthenticated` 
            if the user can not be authenticated.
        :raise: :class:`com.vmware.vapi.std.errors_client.Unauthorized` 
            if the user doesn't have the required privileges.
        """
        return self._invoke('get',
                            {
                            'task': task,
                            })
class _ClusterPairsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'ClusterPairs.CreateSpec'),
        })
        create_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/cluster-pairs',
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

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'ClusterPairs.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            url_template='/snapservice/cluster-pairs',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {
            'cp': type.IdType(resource_types='com.vmware.snapservice.cluster_pair'),
        })
        delete_error_dict = {
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
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/snapservice/cluster-pairs/{cp}',
            path_variables={
                'cp': 'cp',
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
            'cp': type.IdType(resource_types='com.vmware.snapservice.cluster_pair'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/cluster-pairs/{cp}',
            path_variables={
                'cp': 'cp',
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

        # properties for create_precheck operation
        create_precheck_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'ClusterPairs.CreateSpec'),
        })
        create_precheck_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.already_exists':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'),

        }
        create_precheck_input_value_validator_list = [
        ]
        create_precheck_output_validator_list = [
        ]
        create_precheck_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/cluster-pairs?action=create-precheck',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'create-precheck',
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
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'ClusterPairs.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'ClusterPairs.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'create_precheck': {
                'input_type': create_precheck_input_type,
                'output_type': type.ReferenceType(__name__, 'PrecheckResult'),
                'errors': create_precheck_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).build(),
                'input_value_validator_list': create_precheck_input_value_validator_list,
                'output_validator_list': create_precheck_output_validator_list,
                'task_type': TaskType.TASK,
            },
            'create_precheck$task': {
                'input_type': create_precheck_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': create_precheck_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'AlreadyExists'), []).build(),
                'input_value_validator_list': create_precheck_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'list': list_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
            'create_precheck': create_precheck_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.cluster_pairs',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SessionsStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for create operation
        create_input_type = type.StructType('operation-input', {})
        create_error_dict = {
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),

        }
        create_input_value_validator_list = [
        ]
        create_output_validator_list = [
        ]
        create_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/sessions',
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

        # properties for delete operation
        delete_input_type = type.StructType('operation-input', {})
        delete_error_dict = {
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/snapservice/sessions',
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
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/sessions',
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
            'create': {
                'input_type': create_input_type,
                'output_type': type.SecretType(),
                'errors': create_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).build(),
                'input_value_validator_list': create_input_value_validator_list,
                'output_validator_list': create_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'delete': {
                'input_type': delete_input_type,
                'output_type': type.VoidType(),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': delete_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Sessions.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'create': create_rest_metadata,
            'delete': delete_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.sessions',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _SitesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for probe operation
        probe_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Sites.ProbeSpec'),
        })
        probe_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        probe_input_value_validator_list = [
        ]
        probe_output_validator_list = [
        ]
        probe_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/sites?action=probe',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'probe',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for add operation
        add_input_type = type.StructType('operation-input', {
            'spec': type.ReferenceType(__name__, 'Sites.AddSpec'),
        })
        add_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unverified_peer':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'),

        }
        add_input_value_validator_list = [
        ]
        add_output_validator_list = [
        ]
        add_rest_metadata = OperationRestMetadata(
            http_method='POST',
            url_template='/snapservice/sites?action=add',
            request_body_parameter='spec',
            path_variables={
            },
            query_parameters={
            },
            dispatch_parameters={
                'action': 'add',
            },
            header_parameters={
            },
            dispatch_header_parameters={
            },
            use_status_to_std_err_map=False
        )

        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Sites.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.service_unavailable':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'),
            'com.vmware.vapi.std.errors.unauthenticated':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'),
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/sites',
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
        get_input_type = type.StructType('operation-input', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        get_input_value_validator_list = [
        ]
        get_output_validator_list = [
        ]
        get_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/sites/{site}',
            path_variables={
                'site': 'site',
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
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'spec': type.ReferenceType(__name__, 'Sites.UpdateSpec'),
        })
        update_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),

        }
        update_input_value_validator_list = [
        ]
        update_output_validator_list = [
        ]
        update_rest_metadata = OperationRestMetadata(
            http_method='PATCH',
            url_template='/snapservice/sites/{site}',
            request_body_parameter='spec',
            path_variables={
                'site': 'site',
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
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'spec': type.ReferenceType(__name__, 'Sites.DeleteSpec'),
            'options': type.OptionalType(type.ReferenceType(__name__, 'Sites.DeleteOptions')),
        })
        delete_error_dict = {
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
            'com.vmware.vapi.std.errors.unsupported':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'),
            'com.vmware.vapi.std.errors.unauthorized':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'),
            'com.vmware.vapi.std.errors.not_allowed_in_current_state':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'),

        }
        delete_input_value_validator_list = [
        ]
        delete_output_validator_list = [
        ]
        delete_rest_metadata = OperationRestMetadata(
            http_method='DELETE',
            url_template='/snapservice/sites/{site}',
            request_body_parameter='spec',
            path_variables={
                'site': 'site',
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
            'probe': {
                'input_type': probe_input_type,
                'output_type': type.ReferenceType(__name__, 'Sites.ProbeResult'),
                'errors': probe_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': probe_input_value_validator_list,
                'output_validator_list': probe_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'add$task': {
                'input_type': add_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': add_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'UnverifiedPeer'), []).build(),
                'input_value_validator_list': add_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Sites.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType(__name__, 'Sites.Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'update$task': {
                'input_type': update_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': update_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': update_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
            'delete$task': {
                'input_type': delete_input_type,
                'output_type': type.IdType(resource_types='com.vmware.cis.TASK'),
                'errors': delete_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unsupported'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotAllowedInCurrentState'), []).build(),
                'input_value_validator_list': delete_input_value_validator_list,
                'output_validator_list': [],
                'task_type': TaskType.TASK_ONLY,
            },
        }
        rest_metadata = {
            'probe': probe_rest_metadata,
            'add': add_rest_metadata,
            'list': list_rest_metadata,
            'get': get_rest_metadata,
            'update': update_rest_metadata,
            'delete': delete_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.sites',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _TasksStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Tasks.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
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
            url_template='/snapservice/tasks',
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
        get_input_type = type.StructType('operation-input', {
            'task': type.IdType(resource_types='com.vmware.snapservice.task'),
        })
        get_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
            'com.vmware.vapi.std.errors.resource_inaccessible':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'),
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
            url_template='/snapservice/tasks/{task}',
            path_variables={
                'task': 'task',
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
                'output_type': type.ReferenceType(__name__, 'Tasks.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
            'get': {
                'input_type': get_input_type,
                'output_type': type.ReferenceType('com.vmware.snapservice.tasks_client', 'Info'),
                'errors': get_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ResourceInaccessible'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': get_input_value_validator_list,
                'output_validator_list': get_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
            'get': get_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.tasks',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'ClusterPairs': ClusterPairs,
        'Sessions': Sessions,
        'Sites': Sites,
        'Tasks': Tasks,
        'clusters': 'com.vmware.snapservice.clusters_client.StubFactory',
        'info': 'com.vmware.snapservice.info_client.StubFactory',
        'sites': 'com.vmware.snapservice.sites_client.StubFactory',
        'tasks': 'com.vmware.snapservice.tasks_client.StubFactory',
    }

