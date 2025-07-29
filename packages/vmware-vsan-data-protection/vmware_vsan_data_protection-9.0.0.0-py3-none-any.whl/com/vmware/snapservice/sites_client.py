# Copyright (c) 2023-2024 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright (c) 2025 Broadcom.  All rights reserved.
# The term "Broadcom" refers to Broadcom Inc. and/or its subsidiaries.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.snapservice.sites.
#---------------------------------------------------------------------------

"""
The ``com.vmware.snapservice.sites_client`` module provides classes for
configuring and managing sites.

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


class Clusters(VapiInterface):
    """
    The ``Clusters`` class provides methods for managing clusters in a site
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.sites.clusters'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _ClustersStub)
        self._VAPI_OPERATION_IDS = {}

    class FilterSpec(VapiStruct):
        """
        The ``Clusters.FilterSpec`` class contains attributes used to filter the
        results when listing clusters in the specified site. If multiple attributes
        are specified, only clusters matching all of the attributes will be
        returned.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     clusters=None,
                     names=None,
                    ):
            """
            :type  clusters: :class:`set` of :class:`str` or ``None``
            :param clusters: Identifiers of clusters that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                When clients pass a value of this class as a parameter, the
                attribute must contain identifiers for the resource type:
                ``ClusterComputeResource``. When methods return a value of this
                class as a return value, the attribute will contain identifiers for
                the resource type: ``ClusterComputeResource``.
                If None or empty, clusters with any identifier match the filter.
            :type  names: :class:`set` of :class:`str` or ``None``
            :param names: Names of clusters that can match the filter.
                This attribute was added in **vSphere API 9.0.0.0**.
                If None or empty, clusters with any name match the filter.
            """
            self.clusters = clusters
            self.names = names
            VapiStruct.__init__(self)


    FilterSpec._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.clusters.filter_spec', {
            'clusters': type.OptionalType(type.SetType(type.IdType())),
            'names': type.OptionalType(type.SetType(type.StringType())),
        },
        FilterSpec,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Clusters.Info`` class contains details regarding the cluster.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     name=None,
                    ):
            """
            :type  name: :class:`str`
            :param name: Name of the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.name = name
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.clusters.info', {
            'name': type.StringType(),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Clusters.ListItem`` class contains information about a cluster
        returned by :func:`Clusters.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     cluster=None,
                     info=None,
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
            :type  info: :class:`Clusters.Info`
            :param info: Information regarding the cluster.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.cluster = cluster
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.clusters.list_item', {
            'cluster': type.IdType(resource_types='ClusterComputeResource'),
            'info': type.ReferenceType(__name__, 'Clusters.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Clusters.ListResult`` class represents the result of
        :func:`Clusters.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Clusters.ListItem`
            :param items: List of clusters.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.clusters.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Clusters.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self,
             site,
             filter=None,
             ):
        """
        List the clusters for the specified site.
        This method was added in **vSphere API 9.0.0.0**.

        :type  site: :class:`str`
        :param site: Identifier of the site.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.site``.
        :type  filter: :class:`Clusters.FilterSpec` or ``None``
        :param filter: Specification of matching clusters for which information should be
            returned.
            If None, the behavior is equivalent to a
            :class:`Clusters.FilterSpec` with all attributes None which means
            all clusters match the filter.
        :rtype: :class:`Clusters.ListResult`
        :return: Information about the clusters matching the
            :class:`Clusters.FilterSpec`.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.InvalidArgument` 
            If validation of the ``filter`` fails.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no site associated with ``site`` in the system.
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
                            'site': site,
                            'filter': filter,
                            })
class Licenses(VapiInterface):
    """
    The ``Licenses`` class provides methods for managing the licenses for a
    site.
    This class was added in **vSphere API 9.0.0.0**.
    """

    _VAPI_SERVICE_ID = 'com.vmware.snapservice.sites.licenses'
    """
    Identifier of the service in canonical form.
    """
    def __init__(self, config):
        """
        :type  config: :class:`vmware.vapi.bindings.stub.StubConfiguration`
        :param config: Configuration to be used for creating the stub.
        """
        VapiInterface.__init__(self, config, _LicensesStub)
        self._VAPI_OPERATION_IDS = {}

    class LicenseType(Enum):
        """
        The ``Licenses.LicenseType`` class contains the supported values for the
        license types.
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
        VLR = None
        """
        License for VMware Live Recovery

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`LicenseType` instance.
            """
            Enum.__init__(string)

    LicenseType._set_values({
        'VLR': LicenseType('VLR'),
    })
    LicenseType._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.licenses.license_type',
        LicenseType))


    class VlrLicenseType(Enum):
        """
        The ``Licenses.VlrLicenseType`` class contains the supported values for the
        VLR license types.
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
        NONE = None
        """
        No subscription licensing

        """
        CLOUD_SUBSCRIPTION = None
        """
        Subscription-based licensing

        """
        OFFLINE_SUBSCRIPTION = None
        """
        Offline license

        """
        TERM_BASED = None
        """
        Term based license

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`VlrLicenseType` instance.
            """
            Enum.__init__(string)

    VlrLicenseType._set_values({
        'NONE': VlrLicenseType('NONE'),
        'CLOUD_SUBSCRIPTION': VlrLicenseType('CLOUD_SUBSCRIPTION'),
        'OFFLINE_SUBSCRIPTION': VlrLicenseType('OFFLINE_SUBSCRIPTION'),
        'TERM_BASED': VlrLicenseType('TERM_BASED'),
    })
    VlrLicenseType._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.licenses.vlr_license_type',
        VlrLicenseType))


    class VlrMode(Enum):
        """
        The ``Licenses.LicenseType`` class contains the supported values for the
        operation modes based on the license.
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
        OPERATIONAL = None
        """
        Fully operational

        """
        DEGRADED = None
        """
        Degraded mode. Some of the replication features are off

        """
        SUSPENDED = None
        """
        Suspended mode. All replication related features are off

        """

        def __init__(self, string):
            """
            :type  string: :class:`str`
            :param string: String value for the :class:`VlrMode` instance.
            """
            Enum.__init__(string)

    VlrMode._set_values({
        'OPERATIONAL': VlrMode('OPERATIONAL'),
        'DEGRADED': VlrMode('DEGRADED'),
        'SUSPENDED': VlrMode('SUSPENDED'),
    })
    VlrMode._set_binding_type(type.EnumType(
        'com.vmware.snapservice.sites.licenses.vlr_mode',
        VlrMode))


    class VlrInfo(VapiStruct):
        """
        The ``Licenses.VlrInfo`` class contains details regarding the license.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'vlr_license_type',
                {
                    'OFFLINE_SUBSCRIPTION' : [('operational_mode', True), ('available', True), ('total', True)],
                    'CLOUD_SUBSCRIPTION' : [('operational_mode', True)],
                    'NONE' : [],
                    'TERM_BASED' : [],
                }
            ),
        ]



        def __init__(self,
                     vlr_license_type=None,
                     operational_mode=None,
                     available=None,
                     total=None,
                    ):
            """
            :type  vlr_license_type: :class:`Licenses.VlrLicenseType`
            :param vlr_license_type: Type of vlr license
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  operational_mode: :class:`Licenses.VlrMode`
            :param operational_mode: Current operation mode based on the license type
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``vlrLicenseType`` is one of
                :attr:`Licenses.VlrLicenseType.OFFLINE_SUBSCRIPTION` or
                :attr:`Licenses.VlrLicenseType.CLOUD_SUBSCRIPTION`.
            :type  available: :class:`long`
            :param available: Currently avaible number of licenses
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``vlrLicenseType`` is
                :attr:`Licenses.VlrLicenseType.OFFLINE_SUBSCRIPTION`.
            :type  total: :class:`long`
            :param total: Total number of available licenses
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``vlrLicenseType`` is
                :attr:`Licenses.VlrLicenseType.OFFLINE_SUBSCRIPTION`.
            """
            self.vlr_license_type = vlr_license_type
            self.operational_mode = operational_mode
            self.available = available
            self.total = total
            VapiStruct.__init__(self)


    VlrInfo._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.licenses.vlr_info', {
            'vlr_license_type': type.ReferenceType(__name__, 'Licenses.VlrLicenseType'),
            'operational_mode': type.OptionalType(type.ReferenceType(__name__, 'Licenses.VlrMode')),
            'available': type.OptionalType(type.IntegerType()),
            'total': type.OptionalType(type.IntegerType()),
        },
        VlrInfo,
        False,
        None))


    class Info(VapiStruct):
        """
        The ``Licenses.Info`` class contains details regarding the license.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """

        _validator_list = [
            UnionValidator(
                'license_type',
                {
                    'VLR' : [('vlr_license_info', True)],
                }
            ),
        ]



        def __init__(self,
                     license_type=None,
                     vlr_license_info=None,
                    ):
            """
            :type  license_type: :class:`Licenses.LicenseType`
            :param license_type: Type of the license.
                This attribute was added in **vSphere API 9.0.0.0**.
            :type  vlr_license_info: :class:`Licenses.VlrInfo`
            :param vlr_license_info: Information about VLR license type.
                This attribute was added in **vSphere API 9.0.0.0**.
                This attribute is optional and it is only relevant when the value
                of ``licenseType`` is :attr:`Licenses.LicenseType.VLR`.
            """
            self.license_type = license_type
            self.vlr_license_info = vlr_license_info
            VapiStruct.__init__(self)


    Info._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.licenses.info', {
            'license_type': type.ReferenceType(__name__, 'Licenses.LicenseType'),
            'vlr_license_info': type.OptionalType(type.ReferenceType(__name__, 'Licenses.VlrInfo')),
        },
        Info,
        False,
        None))


    class ListItem(VapiStruct):
        """
        The ``Licenses.ListItem`` class contains information about a license
        returned by :func:`Licenses.list` method
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     info=None,
                    ):
            """
            :type  info: :class:`Licenses.Info`
            :param info: Information regarding the license.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.info = info
            VapiStruct.__init__(self)


    ListItem._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.licenses.list_item', {
            'info': type.ReferenceType(__name__, 'Licenses.Info'),
        },
        ListItem,
        False,
        None))


    class ListResult(VapiStruct):
        """
        The ``Licenses.ListResult`` class represents the result of
        :func:`Licenses.list` method.
        This class was added in **vSphere API 9.0.0.0**.

        .. tip::
            The arguments are used to initialize data attributes with the same
            names.
        """




        def __init__(self,
                     items=None,
                    ):
            """
            :type  items: :class:`list` of :class:`Licenses.ListItem`
            :param items: List of licenses.
                This attribute was added in **vSphere API 9.0.0.0**.
            """
            self.items = items
            VapiStruct.__init__(self)


    ListResult._set_binding_type(type.StructType(
        'com.vmware.snapservice.sites.licenses.list_result', {
            'items': type.ListType(type.ReferenceType(__name__, 'Licenses.ListItem')),
        },
        ListResult,
        False,
        None))



    def list(self,
             site,
             ):
        """
        List the licenses for the specified site. VMware live recovery licenses
        are always associated with the peer site. The result for local site
        will not include the VMware live recovery license information. 
        
        VSAN replication features are not supported when the peer site does not
        have any VMware live recovery licenses available.
        This method was added in **vSphere API 9.0.0.0**.

        :type  site: :class:`str`
        :param site: Identifier of the site.
            The parameter must be an identifier for the resource type:
            ``com.vmware.snapservice.site``.
        :rtype: :class:`Licenses.ListResult`
        :return: Information about the licenses for the specified site.
        :raise: :class:`com.vmware.vapi.std.errors_client.Error` 
            If there is unknown internal error.
        :raise: :class:`com.vmware.vapi.std.errors_client.NotFound` 
            If there is no site associated with ``site`` in the system.
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
                            'site': site,
                            })
class _ClustersStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
            'filter': type.OptionalType(type.ReferenceType(__name__, 'Clusters.FilterSpec')),
        })
        list_error_dict = {
            'com.vmware.vapi.std.errors.error':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'),
            'com.vmware.vapi.std.errors.invalid_argument':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'),
            'com.vmware.vapi.std.errors.not_found':
                type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'),
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
            url_template='/snapservice/sites/{site}/clusters',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Clusters.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'InvalidArgument'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.sites.clusters',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)

class _LicensesStub(ApiInterfaceStub):
    def __init__(self, config):
        # properties for list operation
        list_input_type = type.StructType('operation-input', {
            'site': type.IdType(resource_types='com.vmware.snapservice.site'),
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

        }
        list_input_value_validator_list = [
        ]
        list_output_validator_list = [
        ]
        list_rest_metadata = OperationRestMetadata(
            http_method='GET',
            url_template='/snapservice/sites/{site}/licenses',
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
            'list': {
                'input_type': list_input_type,
                'output_type': type.ReferenceType(__name__, 'Licenses.ListResult'),
                'errors': list_error_dict,
                'throws_clause': ThrowsClauseBuilder().add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Error'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'NotFound'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'ServiceUnavailable'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthenticated'), []).add(type.ReferenceType('com.vmware.vapi.std.errors_client', 'Unauthorized'), []).build(),
                'input_value_validator_list': list_input_value_validator_list,
                'output_validator_list': list_output_validator_list,
                'task_type': TaskType.NONE,
            },
        }
        rest_metadata = {
            'list': list_rest_metadata,
        }
        ApiInterfaceStub.__init__(
            self, iface_name='com.vmware.snapservice.sites.licenses',
            config=config, operations=operations, rest_metadata=rest_metadata,
            is_vapi_rest=True)


class StubFactory(StubFactoryBase):
    _attrs = {
        'Clusters': Clusters,
        'Licenses': Licenses,
    }

