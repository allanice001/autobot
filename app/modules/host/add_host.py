#!/usr/bin/python
import flask
import flask.views
import yaml
from app import common
from app.common import db


class AddHost(flask.views.MethodView):
    def get(self):
        groups = common.get_all_groups()
        # return everything to the template
        return flask.render_template('addhost.html', groups=groups)

    def post(self):
        hostname = str(flask.request.form['add_host'])
        # check if hostname already exists
        if len(hostname) == 0:
            flask.flash('Empty hostname given')
            return flask.redirect(flask.url_for('addhost'))
        elif hostname == self.get_hostname(hostname):
            # add the option to edit the given hostname
            flask.flash('Host already exists')
            return flask.redirect(flask.url_for('addhost'))
        else:
            # add the host
            self.add_host(hostname)
            # add the host to selected groups
            self.add_host_to_groups(hostname)
            flask.flash('Host added successfully')
            return flask.redirect(flask.url_for('addhost'))

    def get_hostname(self,hostname):
        host = [str(item) for item in db.hosts.find({"hostname": hostname}).distinct("hostname")]
        if not host:
            host = None
        else:
            host = host[0]
        return host

    def add_host(self,hostname):
        # Get the ansible vars from the form
        yamlvars = flask.request.form['hyaml']
        try:
            if not yamlvars:
                y = yaml.load('{}')
            else:
                y = yaml.load(yamlvars)
        except yaml.YAMLError, exc:
            print "Yaml syntax error"


        post = {"hostname": hostname,
                "vars": y,
        }
        try:
            db.hosts.insert(post)
        except:
            pass

    def add_host_to_groups(self, hostname):
        select_groups = flask.request.form.getlist('selectedgroups')
        #remove unicode tags
        select_groups = [str(group) for group in select_groups]
        # Add host as member to each selecred group
        for group in select_groups:
            db.groups.update({'groupname': group}, {'$push':{'hosts': hostname}},upsert=False,multi=False)

    def add_host_to_tags(self, hostname):
        select_tags = flask.request.form.getlist('selectedtags')
        select_tags = [str(tag) for tag in select_tags]
        for tag in select_tags:
            db.tags.update({'tagname': tag}, {'$push': {'hosts': hostname}}, upsert=False,multi=False)