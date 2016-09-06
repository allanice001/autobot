from flask_restful import reqparse, Resource
from app import common

parser = reqparse.RequestParser()
parser.add_argument('rolename', type=str, location='json')
parser.add_argument('tags', type=list, location='json')


def delete_role(role_name):
    common.db.roles.remove({'rolename': role_name})
    tags = common.db.tags.find({'roles': role_name}).distinct('tagname')
    for item in tags:
        common.db.tags.update({"tagname": item}, {"$pull": {"roles": role_name}})


def add_role(role_name):
    post = dict(rolename=role_name)

    try:
        common.db.roles.insert(post)
    except:
        print "insert error"
        pass


def add_role_to_tags(role_name, tags):
    select_tags = [str(tag) for tag in tags]
    for tag in select_tags:
        common.db.tags.update({'tagname': tag}, {'$push': {'roles': role_name}}, upsert=False, multi=False)


class RolesAPI(Resource):
    def get(self):
        result = common.get_all_roles()
        if result:
            data = {"roles": [role for role in result]}
        else:
            data = {"roles": ""}
        return data

    def post(self):
        args = parser.parse_args()
        role_name = args['rolename']
        tags = args['tags']
        exists = [str(item) for item in common.get_search_roles(role_name)]
        if exists:
            return 'Role already exists', 201

        add_role(role_name)
        add_role_to_tags(role_name, tags)
        return '', 200

    def put(self):
        args = parser.parse_args()
        role_name = args['rolename']
        tags = args['tags']
        delete_role(role_name)
        add_role(role_name)
        add_role_to_tags(role_name, tags)
        return '', 200

    def delete(self):
        args = parser.parse_args()
        role_name = args['rolename']
        delete_role(role_name)
        return '', 200


class GetRoleTagsAPI(Resource):
    def get(self, role_name):
        result = common.get_all_tags_for_role(role_name)
        if  result:
            data = {"tags": [host["tagname"] for host in result]}
        else:
            data = {"tags": ""}
        return data


class GetRolesSearchAPI(Resource):
    def get(self, search_term):
        result = common.get_search_roles(search_term)
        if result:
            data = {"hosts": [host["hostname"] for host in result]}
        else:
            data = {"hosts": ""}
        return data
