#!/usr/bin/python
import flask
import flask.views
import yaml
from app import common
from app.common import db


class AddGroup(flask.views.MethodView):

    def get(self):
        '''logic to return a list of all available ansible hosts'''
        hosts = common.get_all_hosts()
        childgroups = common.get_all_groups()
        return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)

    def post(self):
        groupname = str(flask.request.form['add_group'])
        hosts = common.get_all_hosts()
        childgroups = common.get_all_groups()
        if len(groupname) == 0:
            flask.flash('empty groupname')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)
        elif groupname == self.get_group_name(groupname):
            flask.flash('groupname already exists')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)
        else:
            # insert logic to see if group already exists (get_groupname)
            self.add_group(groupname)
            flask.flash('Group added successfully')
            return flask.render_template('addgroup.html', hosts=hosts, childgroups=childgroups)

    # this checks if the groupname is already defined.
    # need better implementation
    def get_group_name(self, groupname):
        group = [str(item) for item in db.groups.find({"groupname": groupname}).distinct("groupname")]
        if not group:
            group = None
        else:
            group = group[0]
        return group

    def add_group(self, groupname):
        yamlvars = flask.request.form['gyaml']
        # return empty list in inventory output when no vars
        if not yamlvars:
            y = {}
        else:
            y = yaml.load(yamlvars)
        selectedhosts = flask.request.form.getlist('selectedhosts')
        selectedchildren = flask.request.form.getlist('selectedchildren')
        # create a list with the DNs from the selected hostnames
        children = []
        members = []
        parents = []

        for host in selectedhosts:
            members.append(host)

        for child in selectedchildren:
            print(child)
            children.append(child)

        post = {"groupname": groupname,
                "hosts": members,
                "vars": y,
                "children": children,
                "parents": parents
        }
        try:
            db.groups.insert(post)
        except:
            pass
