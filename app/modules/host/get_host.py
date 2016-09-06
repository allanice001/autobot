#!/usr/bin/python
import flask
from flask.views import MethodView
from app import common, app
from flask_paginate import Pagination
from flask import request


class GetHost(MethodView):

    def get(self):
        query = request.args.get('q')
        if query:
            result = self.get_host_info(query)
            groups = self.get_host_groups(query)
            if result is None:
                return self.get_search_hosts(query)
            else:
                return flask.render_template('gethost.html', res=result, groupres=groups, hostname=query)

        return flask.render_template('gethost.html')

    def post(self):
        hostname = str(flask.request.form['p_get'])
        result = self.get_host_info(hostname)
        groups = self.get_host_groups(hostname)
        # print groups
        if result is None:
            return self.get_search_hosts(hostname)
        else:
            return flask.render_template('gethost.html', res=result, groupres=groups, hostname=hostname)

    def get_search_hosts(self, hostname):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)

        getallhosts = GetAllHosts()
        searchHosts = getallhosts.get_paged_hosts(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'], hostname)

        pagination = Pagination(page=page, total=common.count_hosts(hostname), found=hostname, record_name='host', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('gethost.html', allhosts=searchHosts, pagination=pagination)

    def get_host_info(self, hostname):
        result = common.get_hostname_info(hostname)
        host = [item for item in result]
        if len(hostname) == 0:
            return None
        elif not host:
            return None
        elif host[0]['vars'] == None:
            return None
        else:
            for item in host:
                print item
                ansiblevars = item['vars']
            return ansiblevars

    def get_host_groups(self, hostname):
        result = common.get_all_groups_for_host(hostname)
        groups = [ item for item in result]
        grouplist = []
        # return empty list when host is not in a group
        if not groups:
            return grouplist
        else:
            for item in groups:
                grouplist.append(item['groupname'])
            return grouplist


class GetAllHosts(MethodView):

    def get(self):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)
        all_hosts = self.get_paged_hosts(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'])

        pagination = Pagination(css_framework='bootstrap3', page=page, total=common.count_hosts(), record_name='host', per_page= app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return flask.render_template('gethost.html', allhosts=all_hosts, pagination=pagination)

    def get_paged_hosts(self, skip, number_of_items, filter_hostname=None):
        result = common.get_paged_hosts(skip, number_of_items, filter_hostname)
        all_hosts = {}
        host = GetHost()
        for item in result:
            if type(item) is dict:
                hostname = item['hostname']
            else:
                hostname = item

            itemgroups = host.get_host_groups(hostname)
            all_hosts[hostname] = [str(x) for x in itemgroups]
        return all_hosts

    def get_all_hosts(self):
        result = common.get_all_hosts()
        all_hosts = {}
        host = GetHost()
        for item in result:
            item_groups = host.get_host_groups(item)
            all_hosts[item] = [str(x) for x in item_groups]
        return all_hosts
