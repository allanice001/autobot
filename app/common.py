import os
import pymongo
from app import app
SECRET_KEY = os.getenv('SECRET_KEY', app.config['SECRET_KEY'])

# establish connection with mongodb
dbserver = os.getenv('MONGOSRV', app.config['MONGOSRV'])
database = os.getenv('DATABASE', app.config['DATABASE'])
dbserverport = os.getenv('MONGOPORT', app.config['MONGOPORT'])


conn = pymongo.MongoClient(dbserver, dbserverport)
db = conn[database]

db.groups.ensure_index('groupname')
db.tags.ensure_index('tagname')
db.hosts.ensure_index('hostname')
db.roles.ensure_index('rolename')

'''Host'''


def host_exists(hostname):
    if db.hosts.find({'hostname': hostname}).count() > 0:
        return True
    return False


def count_hosts(filter_hostname=None):
    if filter_hostname:
        return db.hosts.find({'hostname': {'$regex': filter_hostname}}).count()
    else:
        return db.hosts.find().count()


def count_groups(filter_groupname=None):
    if filter_groupname:
        return db.groups.find({'groupname': {'$regex': filter_groupname}}).count()
    else:
        return db.groups.find().count()


def get_all_groups_for_host(hostname):
    return db.groups.find({'hosts': hostname}, {'groupname': 1, '_id': 0})


def get_all_tags_for_host(hostname):
    return db.tags.find({'hosts': hostname}, {'tagname': 1, '_id': 0})


def get_hostname_info(hostname):
    return db.hosts.find({'hostname': hostname}, {'hostname': 0, '_id': 0})


def get_search_hosts(search_term):
    return db.hosts.find({'hostname': {'$regex': search_term}})


def get_paged_hosts(skip, number_of_items, filter_hostname=None):
    if filter_hostname:
        return db.hosts.find({'hostname': {'$regex': filter_hostname}}).skip(skip).limit(number_of_items)
    else:
        return db.hosts.find().skip(skip).limit(number_of_items)


def get_all_hosts():
    return db.hosts.find().distinct('hostname')

'''Groups'''


def get_all_host_for_group(groupname):
    return db.groups.find({'groupname': groupname}, {'hosts': 1, '_id': 0})


def get_all_childeren_for_group(groupname):
    return db.groups.find({'groupname': groupname}, {'children': 1, '_id': 0}) #, 'groupname': {'$ne': groupname}})


def get_group_variables(groupname):
    return db.groups.find({'groupname': groupname}, {'vars': 1, '_id': 0})


def get_paged_groups(skip, number_of_items, filter_groupname=None):
    if filter_groupname:
        return db.groups.find({'groupname': {'$regex': filter_groupname}}).skip(skip).limit(number_of_items)
    else:
        return db.groups.find().skip(skip).limit(number_of_items)


def get_all_groups():
    return db.groups.find().distinct('groupname')

'''
def get_other_groups(exclude):
    return db.groups.find({}, {'groupname': {'$ne': exclude}}).distinct('groupname')
'''


def get_group(groupname):
    return db.groups.find({'groupname': groupname}, {'groupname': 1, '_id': 0})


def get_group_info(groupname):
    return db.groups.find({'groupname': groupname}).distinct('vars')


def get_search_groups(search_term):
    return db.groups.find({'groupname': {'$regex': search_term}})


def get_all_tags_for_group(groupname):
    return db.tags.find({'groups': groupname}, {'tagname': 1, '_id':0})


'''Tags'''

'''
def get_all_tags():
    return db.tags.find().distinct('tagname')


def get_tag(tagname):
    return db.tags.find({'tagname': tagname}, {'tagname': 1, '_id': 0})


def get_other_tags(exclude):
    return db.tags.find({}, {'tagname': {'$ne': exclude}}).distinct('tagname')


def get_paged_tags(skip, number_of_items, filter_tagname=None):
    if filter_tagname:
        return db.tags.find({'tagname': {'$regex': filter_tagname}}).skip(skip).limit(number_of_items)
    else:
        return db.tags.find().skip(skip).limit(number_of_items)


def get_tag_info(tagname):
    return db.tags.find({'tagname': tagname}, {'tagname': 0, '_id': 0})


def get_tag_hosts(tagname):
    return db.tags.find({'tagname': tagname}, {'hosts': 1, '_id': 0})


def get_tag_groups(tagname):
    return db.tags.find({'tagname': tagname}, {'groups': 1, '_id': 0})


def get_tag_roles(tagname):
    return db.tags.find({'tagname': tagname}, {'roles': 1, '_id':0})


def get_all_hosts_for_tag(tagname):
    return db.tags.find({'tagname': tagname}, {'hosts': 1, '_id': 0}).distinct('tagname')


def count_tags(filter_tagname=None):
    if filter_tagname:
        return db.tags.find({'tagname': {'$regex': filter_tagname}}).count()
    else:
        return db.tags.find().count()
'''

'''
Roles
'''


def get_all_roles():
    return db.roles.find({},{'_id': 0}).distinct('rolename')


def get_all_tags_for_role(role_name):
    return db.tags.find({'roles': role_name}, {'tagname': 1, '_id': 0}).distinct('tagname')


def count_roles(filter_role_name=None):
    if filter_role_name:
        return db.roles.find({'rolename': {'$regex': filter_role_name}}).count()
    else:
        return db.roles.find().count()


def get_paged_roles(skip, number_of_items, filter_role_name=None):
    if filter_role_name:
        return db.roles.find({'rolename': {'$regex': filter_role_name}}).skip(skip).limit(number_of_items)
    else:
        return db.roles.find().skip(skip).limit(number_of_items)


def get_search_roles(search_term):
    return db.roles.find({'rolename': {'$regex': search_term}})