from flask_restful import reqparse, Resource
from flask import json
import yaml
from app import common

parser = reqparse.RequestParser()
parser.add_argument('hostname', type=str, location='json')
parser.add_argument('vars', type=dict, location='json')
parser.add_argument('groups', type=list, location='json')
parser.add_argument('tags', type=list, location='json')


def delete_host(hostname):
    common.db.hosts.remove({'hostname': hostname})
    groups = common.db.groups.find({'hosts': hostname}).distinct('groupname')
    for item in groups:
        common.db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})


def add_host(hostname, ansiblevars):
    try:
        if ansiblevars:
            j = json.dumps(ansiblevars, sort_keys=True, indent=2)
            y = yaml.load(j)
        else:
            y = yaml.load('{}')
    except yaml.YAMLError, exc:
        print "Yaml syntax error"

    post = dict(hostname=hostname, vars=y)

    try:
        common.db.hosts.insert(post)
    except:
        print "insert error"
        pass


def add_host_to_groups(hostname, groups):
    select_groups = [str(group) for group in groups]
    for group in select_groups:
        common.db.groups.update({'groupname': group}, {'$push': {'hosts': hostname}}, upsert=False, multi=False)


def add_host_to_tags(hostname, tags):
    select_tags = [str(tag) for tag in tags]
    for tag in select_tags:
        common.db.tags.update({'tagname': tag}, {'$push': {'hosts': hostname}}, upsert=False, multi=False)


class HostsAPI(Resource):
    def get(self):
        result = common.get_all_hosts()
        if result:
            data = {"hosts": [host for host in result]}
        else:
            data = {"hosts": ""}
        return data

    def post(self):
        args = parser.parse_args()
        hostname = args['hostname']
        ansiblevars = args['vars']
        groups = args['groups']
        tags = args['tags']
        exists = [str(item) for item in common.get_search_hosts(hostname)]
        if exists:
            return 'Host already exists', 201

        add_host(hostname, ansiblevars)
        add_host_to_groups(hostname, groups)
        add_host_to_tags(hostname, tags)

        return '', 200

    def put(self):
        args = parser.parse_args()
        hostname = args['hostname']
        ansiblevars = args['vars']
        groups = args['groups']
        tags = args['tags']
        delete_host(hostname)
        add_host(hostname, ansiblevars)
        add_host_to_groups(hostname, groups)
        add_host_to_tags(hostname, tags)
        return '', 200

    def delete(self):
        args = parser.parse_args()
        hostname = args['hostname']
        delete_host(hostname)
        return '', 200


class GetHostVarsAPI(Resource):
    def get(self, hostname):
        result = common.get_hostname_info(hostname)
        if result:
            ansible_vars = [host["vars"] for host in result]
            data = {"vars": ansible_vars}
        else:
            data = {"vars": ""}
        return data


class GetHostGroupsAPI(Resource):
    def get(self, hostname):
        result = common.get_all_groups_for_host(hostname)
        if result:
            data = {"groups": [host["groupname"] for host in result]}
        else:
            data = {"groups": ""}
        return data


class GetHostTagsAPI(Resource):
    def get(self, hostname):
        result = common.get_all_tags_for_host(hostname)
        if  result:
            data = {"tags": [host["tagname"] for host in result]}
        else:
            data = {"tags": ""}
        return data


class GetHostsSearchAPI(Resource):
    def get(self, search_term):
        result = common.get_search_hosts(search_term)
        if result:
            data = {"hosts": [host["hostname"] for host in result]}
        else:
            data = {"hosts": ""}

        return data
