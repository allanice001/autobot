from flask import render_template, request, flash, redirect, url_for
from flask.views import MethodView
from app import common
from app.common import db
import yaml


class AddTag(MethodView):
    def get(self):
        tags = common.get_all_tags()
        return render_template('addtag.html', tags=tags)

    def post(self):
        tagname = str(request.form['add_tag'])
        if len(tagname) == 0:
            flash('Empty tag name given')
            return redirect(url_for('addtag'))
        elif tagname == self.get_tagname(tagname):
            flash('Tag already exists')
            return redirect(url_for('addtag'))
        else:
            self.add_tag(tagname)
            self.add_host_to_tags(tagname)
            self.add_group_to_tags(tagname)
            self.add_role_to_tags(tagname)
            flash('Tag created successfully')
            return redirect(url_for('addtag'))

    def get_tagname(self, tagname):
        tag = [str(item) for item in db.tags.find({'tagname': tagname}).distinct('tagname')]
        if not tag:
            tag = None
        else:
            tag = tag[0]
        return tag

    def add_tag(self, tagname):
        post = {'tagname': tagname}
        try:
            db.tags.insert(post)
        except:
            pass

    def add_host_to_tags(self, tagname):
        select_hosts = request.form.getlist('selectedhosts')
        select_hosts = [str(tag) for tag in select_hosts]
        for item in select_hosts:
            db.hosts.update({'hostname': item}, {'$push': {'tags': tagname}}, upsert=False, multi=False)
            db.tags.update({'tagname': tagname}, {'$push':{'hosts': item}}, upsert=False, multi=False)


    def add_group_to_tags(self, groupname):
        select_tags = request.form.getlist('selectedtags')
        select_tags = [str(tag) for tag in select_tags]

        for tag in select_tags:
            db.tags.update({'tagname': tag}, {'$push': {'groups': groupname}}, upsert=False, multi=False)

    def add_role_to_tags(self, rolename):
        pass