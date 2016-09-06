from flask import request, render_template
from flask.views import MethodView
from app import common, app
from flask_paginate import Pagination


class GetTag(MethodView):
    def get(self):
        query = request.args.get('q')
        if query:
            result = self.get_tag_info(query)
            groups = self.get_tag_groups(query)
            hosts = self.get_tag_hosts(query)
            roles = self.get_tag_roles(query)
            if result is None:
                return self.get_search_tags(query)
            else:
                return render_template('gettag.html', res=result, groupres=groups, hostres=hosts, roleres=roles, tagname=query)

    def post(self):
        tagname = str(request.form['t_get'])

    def get_search_tags(self, tagname):
        try:
            page = int(request.form.get('page', 1))
        except ValueError:
            page = 1

    def get_tag_info(self, tagname):
        result = common.get_tag_info(tagname)
        tag = [item for item in result]
        if len(tagname) == 0:
            return None
        elif not tag:
            return None
        else:
            return tag

    def get_tag_hosts(self, tagname):
        result = common.get_all_hosts_for_tag(tagname)
        hosts = [item for item in result]
        host_list = []
        if hosts:
            for item in hosts:
                host_list.append(str(item))

        return host_list

    def get_tag_groups(self, tagname):
        return common.get_tag_groups(tagname)

    def get_tag_roles(self, tagname):
        return common.get_all_tags_for_host(tagname)


class GetAllTags(MethodView):
    def get(self):
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        skip = app.config['NUMBER_OF_ITEMS_PER_PAGE'] * (page - 1)
        all_tags = self.get_paged_tags(skip, app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        pagination = Pagination(css_framework='bootstrap3', page=page, total=common.count_tags(), record_name='tag',
                                per_page=app.config['NUMBER_OF_ITEMS_PER_PAGE'])
        return render_template('gettag.html', alltags=all_tags, pagination=pagination)

    def get_paged_tags(self, skip, number_of_items, filter_tagname=None):
        result = common.get_paged_tags(skip, number_of_items, filter_tagname)
        all_tags = {}
        tag = GetTag()
        for item in result:
            if type(item) is dict:
                tagname = item['tagname']
            else:
                tagname = item


            tag_hosts = tag.get_tag_hosts(item)
            # tag_groups = tag.get_tag_groups(item)
            # tag_roles = tag.get_tag_roles(item)
            # print tag_hosts
            # print(tagname)
            all_tags[tagname] = [str(x) for x in tag_hosts]
            print(all_tags[tagname])
            for x in tag_hosts:
                print('I get here')
                print(str(x))
            # all_tags[tagname]['groups'] = [str(x) for x in tag_groups]
            # all_tags[tagname]['roles'] = [str(x) for x in tag_roles]
        #print all_tags
        return all_tags

    def get_all_tags(self):
        result = common.get_all_tags()
        all_tags = {}
        tag_hosts = {}
        tag_groups = {}
        tag_roles = {}
        tag = GetTag()
        for item in result:
            item_hosts = tag.get_tag_hosts(item)
            item_group = tag.get_tag_groups(item)
            item_roles = tag.get_tag_roles(item)

            tag_hosts[item] = [str(x) for x in item_hosts]
            tag_groups[item] = [str(x) for x in item_group]
            tag_roles[item] = [str(x) for x in item_roles]
        all_tags = {'roles': tag_roles, 'groups': tag_groups, 'roles': tag_roles}
        return all_tags
