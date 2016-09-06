#!/usr/bin/python
from flask import request, redirect, url_for, render_template, flash
from flask.views import MethodView
import yaml
from app import common
from app.common import db


class AddRole(MethodView):
    def get(self):
        tags = common.get_all_tags()
        # return everything to the template
        return render_template('addrole.html', tags=tags)

    def post(self):
        role_name = str(request.form['add_role'])
        # check if role name already exists
        if len(role_name) == 0:
            flash('Empty role name given')
            return redirect(url_for('addrole'))
        elif role_name == self.get_role_name(role_name):
            # add the option to edit the given hostname
            flash('Role already exists')
            return redirect(url_for('addrole'))
        else:
            # add the host
            self.add_role(role_name)
            # add the host to selected groups
            self.add_role_to_tags(role_name)
            flash('Role added successfully')
            return redirect(url_for('addrole'))

    def get_role_name(self, role_name):
        role = [str(item) for item in db.roles.find({"rolename": role_name}).distinct("rolename")]
        if not role:
            role = None
        else:
            role = role[0]
        return role

    def add_role(self, role_name):
        post = {
            "rolename": role_name,
        }
        try:
            db.hosts.insert(post)
        except:
            pass

    def add_role_to_tags(self, role_name):
        select_tags = request.form.getlist('selectedtags')
        #remove unicode tags
        select_tags = [str(tag) for tag in select_tags]
        # Add host as member to each selecred group
        for tag in select_tags:
            db.tags.update({'tagname': tag}, {'$push':{'roles': role_name}}, upsert=False, multi=False)