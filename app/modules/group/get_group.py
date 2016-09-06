#!/usr/bin/python
import flask
from flask.views import MethodView
from app import common, app
from flask_paginate import Pagination
from flask import request


class GetGroup(MethodView):

    def get(self):
        query = request.args.get('q')
        if query:
            result = common.get_group(query)
            group = [item for item in result]
            if group:
                groupmembers = self.get_group_children(query)
                groupvars = self.get_group_vars(query)
                grouphosts = self.get_group_hosts(query)
                return flask.render_template('getgroup.html', groupname=query, members=groupmembers, groupvars=groupvars, grouphosts=grouphosts)
            else:
                return self.get_search_groups(query)

        return flask.render_template('getgroup.html')

    def post(self):
        groupname = str(flask.request.form['get_group'])
        result = common.get_group(groupname)
        group = [ item for item in result]
        if not group:
            flask.flash('Group ' + groupname + ' not found')
            return flask.redirect(flask.url_for('getgroup'))
        else:
            groupmembers = self.get_group_children(groupname)
            groupvars = self.get_group_vars(groupname)
            grouphosts = self.get_group_hosts(groupname)
            return flask.render_template('getgroup.html', groupname=groupname, members=groupmembers, groupvars=groupvars, grouphosts=grouphosts)

    def get_search_groups(self, groupname):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)

        getallgroups = GetAllGroups()
        searchgroups = getallgroups.get_paged_groups(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'], groupname)

        pagination = Pagination(page=page, total=common.count_groups(groupname), found=groupname, record_name='group', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('getgroup.html', allgroups=searchgroups, pagination=pagination)

    def get_group_children(self,groupname):
        result = common.get_all_childeren_for_group(groupname)
        for item in result:
            child = item
        children = []
        if not child:
            children = []
        else:
            for item in child["children"]:
                children.append(item)
        return children

    def get_group_hosts(self,groupname):
        result = common.get_all_host_for_group(groupname)
        for item in result:
            h = item
        members = []

        if not h:
            member = []
        else:
            for item in h["hosts"]:
                members.append(item)
        return members

    def get_group_vars(self,groupname):
        result = common.get_group_variables(groupname)
        vars = [item for item in result]
        if len(groupname) == 0:
            groupvars = None
        elif not vars:
            groupvars = None
        else:
            for item in vars:
                groupvars = item["vars"]
        return groupvars


class GetAllGroups(MethodView):
    def get(self):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)
        allgroups = self.get_paged_groups(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'])

        pagination = Pagination(css_framework='bootstrap3', page=page, total=common.count_groups(), record_name='group', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('getgroup.html', allgroups=allgroups, pagination=pagination)

    def get_paged_groups(self, skip, number_of_times, filter_group = None):
        result = common.get_paged_groups(skip, number_of_times, filter_group)
        allgroups = []
        group = GetGroup()
        for item in result:
            if type(item) is dict:
                groupname = item["groupname"]
                t = {}
                t["groupname"] = str(groupname)
                t["children"] = group.get_group_children(groupname)
                t["hosts"] = group.get_group_hosts(groupname)
                allgroups.append(t)

        return allgroups

    def get_all_groups(self):
        result = common.get_all_groups()
        allgroups = []

        group = GetGroup()
        for item in result:
            t = {}
            t["groupname"] = str(item)
            t["children"] = group.get_group_children(item)
            t["hosts"] = group.get_group_hosts(item)
            allgroups.append(t)

        return allgroups

