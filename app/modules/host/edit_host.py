#!/usr/bin/python
from flask import request, flash, render_template, redirect, url_for
from flask.views import MethodView
import yaml
import json
from app import common

from app.common import db


class EditHost(MethodView):

    def post(self):
        hostname = str(request.form['p_get'])
        if len(hostname) == 0:
            flash('empty hostname given')
            return render_template('edithost.html')
        elif not common.host_exists(hostname):
            flash('hostname not found')
            return render_template('edithost.html')
        else:
            result = self.get_hostinfo(hostname)
            available_groups = self.get_availablegroups()
            groups = self.get_hostgroups(hostname)
            return render_template('edithost.html', host=hostname, result=result, groups=groups, available_groups=available_groups)

    def get(self):
        return render_template('edithost.html')

    def get_hostinfo(self, hostname):
        result = db.hosts.find({"hostname": hostname}).distinct("vars")
        if result:
            j = json.dumps(result[0], sort_keys=True, indent=2)
            ansiblevar = yaml.dump(yaml.load(j), default_flow_style=False)
            return ansiblevar
        else:
            return None

    def get_hostgroups(self, hostname):
        # retrieve all groups the host is a member of
        result = common.get_all_groups_for_host(hostname)
        groups = [ item["groupname"] for item in result]
        return groups

    def get_availablegroups(self):
        # return all groups this host is not a member of
        allgroups = common.get_all_groups()
        # build compared list
        hostname = str(request.form['p_get'])
        groups = self.get_hostgroups(hostname)
        s = set(groups)
        availablegroups = [ x for x in allgroups if x not in s ]
        return availablegroups


class EditHostSubmit(MethodView):

    def post(self):
        hostname = str(request.form['p_get2'])
        self.update_host(hostname)
        self.update_groups(hostname)
        return redirect(url_for('getallhosts'))

    def update_host(self,hostname):
            yamlvars = request.form['ehyaml']
            try:
                y = yaml.load(yamlvars)
            except yaml.YAMLError, exc:
                print "Yaml syntax error"
            try:
                db.hosts.update({"hostname": hostname}, {"$set": {'vars': y}}, upsert=False,multi=False)
            except:
                pass

    def update_groups(self,hostname):
            g = EditHost()
            current_groups = g.get_hostgroups(hostname)
            updated_groups = request.form.getlist('groupselect')
            addh = set(current_groups)
            remh = set(updated_groups)
            add_hosts_group = [ x for x in updated_groups if x not in addh ]
            remove_hosts_group = [ x for x in current_groups if x not in remh ]
            for item in add_hosts_group:
                db.groups.update({"groupname": item}, {"$push": {"hosts": hostname}})
            for item in remove_hosts_group:
                db.groups.update({"groupname": item}, {"$pull": {"hosts": hostname}})
            pass

    def get(self):
        return render_template('edithost.html')
