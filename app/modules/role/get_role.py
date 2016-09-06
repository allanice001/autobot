#!/usr/bin/python
from flask import render_template
from flask.views import MethodView
from app import common, app
from flask_paginate import Pagination
from flask import request


class GetRole(MethodView):

    def get(self):
        query = request.args.get('q')
        if query:
            result = self.get_search_roles(query)
            tags = self.get_role_tags(query)
            if result is None:
                return self.get_search_roles(query)
            else:
                return render_template('getrole.html', res=result, tagres=tags, rolename=query)

        return render_template('getrole.html')

    def post(self):
        role_name = str(request.form['r_get'])
        result = self.get_search_roles(role_name)
        tags = self.get_role_tags(role_name)
        # print groups
        if result is None:
            return self.get_search_roles(role_name)
        else:
            return render_template('getrole.html', res=result, tagres=tags, rolename=role_name)

    def get_search_roles(self, role_name):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)

        get_all_roles = GetAllRoles()
        search_roles = get_all_roles.get_paged_roles(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'], role_name)

        pagination = Pagination(page=page, total=common.count_roles(role_name), found=role_name, record_name='role', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return render_template('getrole.html', allroles=search_roles, pagination=pagination)

    def get_role_tags(self, role_name):
        result = common.get_all_tags_for_role(role_name)
        roles = [ item for item in result]
        role_list = []
        # return empty list when host is not in a group
        if roles:
            for item in roles:
                role_list.append(item['rolename'])

        return role_list


class GetAllRoles(MethodView):

    def get(self):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)
        all_roles = self.get_paged_roles(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'])

        pagination = Pagination(css_framework='bootstrap3', page=page, total=common.count_roles(), record_name='role', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return render_template('getrole.html', allhosts=all_roles, pagination=pagination)

    def get_paged_roles(self, skip, number_of_items, filter_hostname=None):
        result = common.get_paged_roles(skip, number_of_items, filter_hostname)
        all_roles = {}
        role = GetRole()
        for item in result:
            if type(item) is dict:
                role_name = item['rolename']
            else:
                role_name = item

            itemgroups = role.get_role_tags(role_name)
            all_roles[role_name] = [str(x) for x in itemgroups]
        return all_roles

    def get_all_roles(self):
        result = common.get_all_roles()
        all_roles = {}
        role = GetRole()
        for item in result:
            item_roles = role.get_role_tags(item)
            all_roles[item] = [str(x) for x in item_roles]
        return all_roles
