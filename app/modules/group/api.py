from flask_restful import reqparse, abort, Resource, Api
from flask import json
import yaml
from app import common

parser = reqparse.RequestParser()
parser.add_argument('groupname', type=str, location='json')
parser.add_argument('vars', type=dict, location='json')
parser.add_argument('children', type=list, location='json')
parser.add_argument('hosts', type=list, location='json')


def add_group(groupname, ansiblevars, children, hosts):
    if ansiblevars:
        j = json.dumps(ansiblevars, sort_keys=True, indent=2)
        y = yaml.load(j)
    else:
        y = {}

    c = [str(child) for child in children]
    h = [str(host) for host in hosts]
    post = dict(groupname=groupname, hosts=h, vars=y, children=c)

    try:
        common.db.groups.insert(post)
    except:
        pass


def delete_group(groupname):
    common.db.groups.remove({'groupname': groupname})
    parentgroups = common.db.groups.find({'children': groupname}).distinct('groupname')
    for item in parentgroups:
        common.db.groups.update({"groupname": item}, {"$pull": {"children": groupname}})


class GroupsAPI(Resource):
    def get(self):
        result = common.get_all_groups()
        if result:
            data = {"groups": [group for group in result]}
        else:
            data = {"groups": ""}
        return data

    def post(self):
        args = parser.parse_args()
        groupname = args['groupname']
        ansiblevars = args['vars']
        children = args['children']
        hosts = args['hosts']
        exists = [str(item) for item in common.get_search_groups(groupname)]
        if exists:
            return 'Group already exists', 201

        add_group(groupname, ansiblevars, children, hosts)
        return '', 200

    def put(self):
        args = parser.parse_args()
        groupname = args['groupname']
        ansiblevars = args['vars']
        children = args['children']
        hosts = args['hosts']
        delete_group(groupname)
        add_group(groupname, ansiblevars, children, hosts)
        return '', 200

    def delete(self):
        args = parser.parse_args()
        groupname = args['groupname']
        delete_group(groupname)
        return '', 200


class GetGroupVarsAPI(Resource):
    def get(self, groupname):
        result = common.get_group_variables(groupname)
        if result:
            data = {"vars": [group["vars"] for group in result]}
        else:
            data = {"vars": ""}
        return data


class GetGroupChildrenAPI(Resource):
    def get(self, groupname):
        result = common.get_all_childeren_for_group(groupname)
        if result:
            data = {"children": [group["children"] for group in result]}
        else:
            data = {"children": ""}
        return data


class GetGroupHostsAPI(Resource):
    def get(self, groupname):
        result = common.get_all_host_for_group(groupname)
        if result:
            data = {"hosts": [group["hosts"] for group in result]}
        else:
            data = {"hosts": ""}
        return data


class GetGroupsSearchAPI(Resource):
    def get(self, search_term):
        result = common.get_search_groups(search_term)
        if result:
            data = {"groups": [group["groupname"] for group in result]}
        else:
            data = {"groups": ""}
        return data


class DescribeGroupsAPI(Resource):
    def get(self):
        result = common.get_all_groups()
        allgroups = []
