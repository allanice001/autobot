#!/usr/bin/python
import flask
import flask.views
import yaml
import json
from app import common
from app.common import db


class EditGroup(flask.views.MethodView):

    def post(self):
        groupname = str(flask.request.form['group_get'])
        childgroups = self.get_child_groups(groupname)
        if len(groupname) == 0:
            flask.flash('empty groupname given')
            return flask.render_template('editgroup.html')
        elif self.get_group_info(groupname) == None:
            flask.flash('Group does not exist')
            return flask.redirect(flask.url_for('editgroup'))
        else:
            result = self.get_group_info(groupname)
            hosts = self.get_grouphosts(groupname)
            available_hosts = self.get_availablehosts()
            availablechildgroups = self.get_available_children()
            return flask.render_template('editgroup.html', group=groupname, result=result, hosts=hosts, available_hosts=available_hosts, childgroups=childgroups, availablechildgroups=availablechildgroups)

    def get(self):
        return flask.render_template('editgroup.html')

    def get_group_info(self, groupname):
        result = common.get_group_info(groupname)
        if not result:
            ansiblevar = None
        else:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
        return ansiblevar

    def get_grouphosts(self, groupname):
        '''retrieve all hosts from the group'''
        result = common.get_all_host_for_group(groupname)
        hosts = result[0]["hosts"]
        if not hosts:
            return None
        else:
            return hosts

    def get_availablehosts(self):
        ''' return all hosts not a member of this group'''
        allhosts = common.get_all_hosts()
        # build compared list
        groupname = str(flask.request.form['group_get'])
        hosts = self.get_grouphosts(groupname)
        if hosts:
            s = set(hosts)
            avaiblable = [x for x in allhosts if x not in s]
            return avaiblable
        return allhosts

    def get_child_groups(self, groupname):
        result = db.groups.find({"groupname": groupname}, {'children':1, '_id': 0})
        childgroups = []
        for item in result:
            childgroups = item["children"]
        return childgroups

    def get_parent_groups(self, groupname):
        result = db.groups.find({"groupname": groupname}, {'parents':1, '_id': 0})
        parent_groups = []
        for item in result:
            parent_groups = item["parents"]
        return parent_groups

    def get_available_children(self):
        all_groups = common.get_all_groups()
        # build compared list
        groupname = str(flask.request.form['group_get'])
        child_groups = self.get_child_groups(groupname)
        parent_groups = self.get_parent_groups(groupname)
        c = set(child_groups)
        p = set(parent_groups)
        available_child_groups = [x for x in all_groups if x not in c and x not in groupname and x not in p]
        return available_child_groups

    def get_available_parents(self):
        all_groups = common.get_all_groups()
        group_name = str(flask.request.form['group_get'])
        child_groups = self.get_child_groups(group_name)
        parent_groups = self.get_parent_groups(group_name)
        c = set(child_groups)
        p = set(parent_groups)
        available_parent_groups = [x for x in all_groups if x not in p and x not in group_name and x not in c]
        return available_parent_groups


class EditGroupSubmit(flask.views.MethodView):

    def post(self):
        groupname = str(flask.request.form['group_get2'])
        self.update_group(groupname)
        self.update_hosts(groupname)
        self.update_childgroups(groupname)
        return flask.redirect('getallgroups')

    def get(self):
        return flask.render_template('editgroup.html')

    def update_group(self,groupname):
        yamlvars = flask.request.form['egyaml']
        try:
            y = yaml.load(yamlvars)
        except yaml.YAMLError as exc:
            print("Yaml syntax error")

        try:
            db.groups.update({"groupname": groupname}, {"$set": {'vars': y}}, upsert=False,multi=False)
        except:
            pass

    def update_hosts(self,groupname):
        global add_hosts, rem_hosts
        h = EditGroup()
        current_hosts = h.get_grouphosts(groupname)
        updated_hosts = flask.request.form.getlist('hostselect')
        if current_hosts and len(updated_hosts) > 0:
            addh = set(current_hosts)
            remh = set(updated_hosts)
            add_hosts = [x for x in updated_hosts if x not in addh]
            rem_hosts = [x for x in current_hosts if x not in remh]
        else:
            if len(updated_hosts) > 0:
                add_hosts = [x for x in updated_hosts]
            else:
                add_hosts = None

            if current_hosts:
                rem_hosts = [x for x in current_hosts]
            else:
                rem_hosts = None

        if add_hosts:
            for item in add_hosts:
                db.groups.update({"groupname": groupname}, {"$push": {"hosts": item}})
        if rem_hosts:
            for item in rem_hosts:
                db.groups.update({"groupname": groupname}, {"$pull": {"hosts": item}})
        pass

    def update_childgroups(self, groupname):
        c = EditGroup()
        current_children = c.get_child_groups(groupname)
        updated_children = flask.request.form.getlist('childrenselect')
        addchld = set(current_children)
        remchld = set(updated_children)
        add_chlds = [x for x in updated_children if x not in addchld]
        rem_chlds = [x for x in current_children if x not in remchld]
        for item in add_chlds:
            db.groups.update({"groupname": groupname}, {"$push": {"children": item}})
            db.groups.update({"groupname": item}, {"$push": {"parents": groupname}})
        for item in rem_chlds:
            db.groups.update({"groupname": groupname}, {"$pull": {"children": item}})
            db.groups.update({"groupname": item}, {"$pull": {"parents": groupname}})

