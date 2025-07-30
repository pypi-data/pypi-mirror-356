# -*- coding: utf-8 -*-
from datetime import datetime
import json
import bottle
import asyncio

from typing import List
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_commons.errors import BadRequestException
from pip_services4_data.query import FilterParams
from pip_services4_components.context import Context

from eic_aichat_users.groupmemberships.data.GroupMembershipV1 import GroupMembershipV1
from eic_aichat_users.groupmemberships.logic.IGroupMembershipsService import IGroupMembershipsService
from eic_aichat_users.groups.logic.IGroupsService import IGroupsService
from eic_aichat_users.partialfacade.operations.version1.Authorize import AuthorizerV1
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService


class GroupsMembershipsOperation(RestOperations):
    def __init__(self):
        super().__init__()
        self._group_memberships: IGroupMembershipsService = None
        self._group: IGroupsService = None
        self._accounts_service: IAccountsService = None
        self._dependency_resolver.put('groupmemberships', Descriptor('aichatusers-groupmemberships', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put('groups', Descriptor('aichatusers-groups', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')
        self._group_memberships = self._dependency_resolver.get_one_required('groupmemberships')
        self._group = self._dependency_resolver.get_one_required('groups')

    # def get_memberships(self):
    #     context = Context.from_trace_id(self._get_trace_id())
    #     user_id = bottle.request.user_id

    #     filter_params = self._get_filter_params()
    #     paging = self._get_paging_params()

    #     try:
    #         page = self._group_memberships.get_memberships(context, filter_params, paging)

    #         userIds = []
    #         groupIds = []
    #         for item in page.data:
    #             userIds.append(item.profile_id)
    #             groupIds.append(item.group_id)

    #         userMap = self._accounts_service.get_map_by_ids(context, userIds)
    #         groupMap = self._group.get_map_by_ids(context, groupIds)

    #         for item in page.data:
    #             group = groupMap.get(item.group_id)
    #             user = userMap.get(item.profile_id)

    #             if group:
    #                 item.group_name = group.title
    #             else:
    #                 item.group_name = None  

    #             if user:
    #                 item.profile_name = user.name
    #                 item.profile_email = user.login
    #             else:
    #                 item.profile_name = None
    #                 item.profile_email = None

    #         profile_name = filter_params.get_as_nullable_string('profile_name')
    #         if profile_name:
    #             page.data = [item for item in page.data if item.profile_name == profile_name]

    #         group_name = filter_params.get_as_nullable_string('group_name')
    #         if group_name:
    #             page.data = [item for item in page.data if item.group_name == group_name]

    #         profile_email = filter_params.get_as_nullable_string('profile_email')
    #         if profile_email:
    #             page.data = [item for item in page.data if item.profile_email == profile_email]

    #         return self._send_result(page)
    #     except Exception as err:
    #         return self._send_error(err)

    def get_memberships(self):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id

        filter_params = self._get_filter_params()
        paging = self._get_paging_params()

        try:
            users = None
            if 'name' or 'login' in filter_params.keys():
                users = self._accounts_service.get_accounts(context, filter_params, None)

            if users:
                profileIds = []
                for user in users.data:
                    profileIds.append(user.id)

                filter_params.put('profile_ids', ",".join(profileIds))

            page = self._group_memberships.get_memberships(context, filter_params, paging)

            userIds = []
            groupIds = []
            for item in page.data:
                userIds.append(item.profile_id)
                groupIds.append(item.group_id)

            userMap = self._accounts_service.get_map_by_ids(context, userIds)
            groupMap = self._group.get_map_by_ids(context, groupIds)

            for item in page.data:
                group = groupMap.get(item.group_id)
                user = userMap.get(item.profile_id)

                if group:
                    item.group_name = group.title
                else:
                    item.group_name = None  

                if user:
                    item.profile_name = user.name
                    item.profile_email = user.login
                else:
                    item.profile_name = None
                    item.profile_email = None

            return self._send_result(page)
        except Exception as err:
            return self._send_error(err)

    def get_membership_by_id(self, membership_id: str):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id
        try:
            membership = self._group_memberships.get_membership_by_id(context, membership_id)
            if membership is None or membership.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_ID", "Id does not exist")
            
            user = self._accounts_service.get_account_by_id(context, membership.profile_id)
            group = self._group.get_group_by_id(context, membership.group_id)

            membership.group_name = group.title
            membership.profile_name = user.name
            membership.profile_email = user.login
            return self._send_result(membership)
        except Exception as err:
            return self._send_error(err)

    def create_membership(self):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id

        data = bottle.request.json
        groupMembership_data = data if isinstance(data, dict) else json.loads(data or '{}')
        groupMembership = GroupMembershipV1(**groupMembership_data)

        try:
            group = self._group.get_group_by_id(context, groupMembership.group_id)
            if group is None or group.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_GROUP_ID", "Group id does not exist")
            if group.owner_id != user_id:
                raise BadRequestException(self._get_trace_id(), "WRONG_USER", "User id does not match group owner id")
            
            user = self._accounts_service.get_account_by_id(context, groupMembership.profile_id)
            if user is None or user.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_USER_ID", "User id does not exist")

            group.member_count += 1
            self._group.update_group(context, group)

            memberships = self._group_memberships.create_membership(context, groupMembership)

            memberships.group_name = group.title
            memberships.profile_name = user.name
            memberships.profile_email = user.login
            return self._send_result(memberships)
        except Exception as err:
            return self._send_error(err)
        
    def create_memberships_bulk(self):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id

        data = bottle.request.json
        memberships_data = data if isinstance(data, list) else json.loads(data or '[]')

        if not isinstance(memberships_data, list):
            raise BadRequestException(self._get_trace_id(), "INVALID_INPUT", "Expected a list of memberships")

        results = []
        try:
            for membership_dict in memberships_data:
                groupMembership = GroupMembershipV1(**membership_dict)

                group = self._group.get_group_by_id(context, groupMembership.group_id)
                if group is None or group.id == "":
                    raise BadRequestException(self._get_trace_id(), "WRONG_GROUP_ID", "Group id does not exist")
                if group.owner_id != user_id:
                    raise BadRequestException(self._get_trace_id(), "WRONG_USER", "User id does not match group owner id")
                
                user = self._accounts_service.get_account_by_id(context, groupMembership.profile_id)
                if user is None or user.id == "":
                    raise BadRequestException(self._get_trace_id(), "WRONG_USER_ID", "User id does not exist")
                
                group.member_count += 1
                self._group.update_group(context, group)
                
                created_membership = self._group_memberships.create_membership(context, groupMembership)

                created_membership.group_name = group.title
                created_membership.profile_name = user.name
                created_membership.profile_email = user.login
                results.append(created_membership)

            return self._send_result(results)
        except Exception as err:
            return self._send_error(err)
        
    def update_membership(self):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id
    
        data = bottle.request.json
        groupMembership_data = data if isinstance(data, dict) else json.loads(data or '{}')
        groupMembership = GroupMembershipV1(**groupMembership_data)

        try:
            group = self._group.get_group_by_id(context, groupMembership.group_id)
            if group is None or group.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_GROUP_ID", "Group id does not exist")
            if group.owner_id != user_id:
                raise BadRequestException(self._get_trace_id(), "WRONG_USER", "User id does not match group owner id")
            
            user = self._accounts_service.get_account_by_id(context, groupMembership.profile_id)
            if user is None or user.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_USER_ID", "User id does not exist")
            
            
            memberships = self._group_memberships.update_membership(context, groupMembership)
            if memberships is None or memberships.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_MEMBERSHIP_ID", "Membership id does not exist")

            memberships.group_name = group.title
            memberships.profile_name = user.name
            memberships.profile_email = user.login
            return self._send_result(memberships)
        except Exception as err:
            return self._send_error(err)
        
    def delete_membership_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id
        try:
            membership = self._group_memberships.get_membership_by_id(context, id)
            group = self._group.get_group_by_id(context, membership.group_id)
            if membership is None or membership.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_MEMBERSHIP_ID", "Membership id does not exist")
            if membership.profile_id != user_id and group.owner_id != user_id:
                raise BadRequestException(self._get_trace_id(), "WRONG_USER", "Profile id does not match user id")
            
            group.member_count -= 1
            self._group.update_group(context, group)
            
            memberships = self._group_memberships.delete_membership_by_id(context, id)
            return self._send_result(memberships)
        except Exception as err:
            return self._send_error(err)
        
    def delete_membership_by_filter(self):
        context = Context.from_trace_id(self._get_trace_id())
        filter_params = self._get_filter_params()
        try:
            res = self._group.delete_groups_by_filter(context, filter_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def activate_membership_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id
        try:
            membership = self._group_memberships.get_membership_by_id(context, id)
            if membership is None or membership.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_ID", "Id does not exist")
            
            group = self._group.get_group_by_id(context, membership.group_id)
            if group is None or group.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_GROUP_ID", "Group id does not exist")
            if group.owner_id != user_id:
                raise BadRequestException(self._get_trace_id(), "WRONG_USER", "User id does not match group owner id")
            
            membership.active = True
            membership.member_since = datetime.utcnow()
            
            res = self._group_memberships.update_membership(context, membership)

            user = self._accounts_service.get_account_by_id(context, membership.profile_id)
            res.group_name = group.title
            res.profile_name = user.name
            res.profile_email = user.login

            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def deactivate_membership_by_id(self, id):
        context = Context.from_trace_id(self._get_trace_id())
        user_id = bottle.request.user_id
        try:
            membership = self._group_memberships.get_membership_by_id(context, id)
            if membership is None or membership.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_ID", "Id does not exist")
            
            group = self._group.get_group_by_id(context, membership.group_id)
            if group is None or group.id == "":
                raise BadRequestException(self._get_trace_id(), "WRONG_GROUP_ID", "Group id does not exist")
            if group.owner_id != user_id:
                raise BadRequestException(self._get_trace_id(), "WRONG_USER", "User id does not match group owner id")
            
            membership.active = False
            
            res = self._group_memberships.update_membership(context, membership)

            user = self._accounts_service.get_account_by_id(context, membership.profile_id)
            res.group_name = group.title
            res.profile_name = user.name
            res.profile_email = user.login

            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def get_users_for_memberships(self):
        context = Context.from_trace_id(self._get_trace_id())
        filter_params = self._get_filter_params()
        paging = self._get_paging_params()

        try:
            group_id = filter_params.get_as_nullable_string('group_id')
            if group_id:
                page = self._group_memberships.get_memberships(context, filter_params, None)

                ids = []
                for item in page.data:
                    ids.append(item.profile_id)

                if len(ids) > 0:
                    filter_params.put('not_in_ids', ",".join(ids))

            res = self._accounts_service.get_accounts(context, filter_params, paging)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)
        
    def register_routes(self, controller: RestController, auth: AuthorizerV1):
            controller.register_route_with_auth('get', '/users/groups/memberships', None, auth.signed(), lambda: self.get_memberships())

            controller.register_route_with_auth('get', '/users/groups/memberships/users', None, auth.signed(), lambda: self.get_users_for_memberships())
            
            controller.register_route_with_auth('get', '/users/groups/:id/memberships', None, auth.signed(), lambda id: self.get_membership_by_id(id))

            controller.register_route_with_auth('post', '/users/groups/memberships', None, auth.signed(), lambda: self.create_membership())

            controller.register_route_with_auth('post', '/users/groups/memberships/bulk', None, auth.signed(), lambda: self.create_memberships_bulk())

            controller.register_route_with_auth('put', '/users/groups/memberships', None, auth.signed(), lambda: self.update_membership())

            controller.register_route_with_auth('delete', '/users/groups/:id/memberships', None, auth.signed(), lambda id: self.delete_membership_by_id(id))

            controller.register_route_with_auth('delete', '/users/groups/memberships', None, auth.admin(), lambda: self.delete_membership_by_filter())

            controller.register_route_with_auth('post', '/users/groups/:id/memberships/activate', None, auth.signed(), lambda id: self.activate_membership_by_id(id))

            controller.register_route_with_auth('post', '/users/groups/:id/memberships/deactivate', None, auth.signed(), lambda id: self.deactivate_membership_by_id(id))
            
        
