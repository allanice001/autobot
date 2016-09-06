from flask import json
from flask_restful import reqparse, Resource
from app import common
import yaml

parser = reqparse.RequestParser()
parser.add_argument('tagname', type=str, location='json')
parser.add_argument('groups', type=list, location='json')
parser.add_argument('hosts', type=list, location='json')


def delete_tag(tagname):
    common.db.tags.remove({'tagname': tagname})

    groups = common.db.groups.find({'tags': tagname}).distinct('groupname')
    for item in groups:
        common.db.groups.update({'groupname': item}, {'$pull':{'tags': tagname}})

    hosts = common.db.hosts.find({'tags': tagname}).distinct('hostname')
    for item in hosts:
        common.db.hosts.update({'hostname': item}, {'$pull': {'tags': tagname}})


def add_tag(tagname):
    post = dict(tagname=tagname)
    try:
        common.db.tags.insert(post)
    except:
        print('Tag insert Error')
        pass


class TagsAPI(Resource):
    def get(self):
        result = common.get_all_tags()
        if result:
            data = {'tags': [tag for tag in result]}
        else:
            data = {'tags': ''}
        return data

    def post(self):
        args = parser.parse_args()
        tagname = args['tagname']
        hosts = args['hosts']
        groups = args['groups']

        exists = [str(item) for item in common.get_search_tags(tagname)]
        if exists:
            return 'Tag already Exists', 201

        add_tag(tagname)
        add_tag_to_groups(tagname, groups)
        add_tag_to_hosts(tagname, hosts)
        return '', 200