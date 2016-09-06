import flask
import flask.views

from app.modules.host.get_host import GetAllHosts
from app.modules.group.get_group import GetAllGroups
from app.common import db

class Remove(flask.views.MethodView):

    def get(self):
        g = GetAllGroups()
        h = GetAllHosts()
        allgroups = [item['groupname'] for item in g.get_all_groups()]
        allhosts = h.get_all_hosts()
        return flask.render_template('remove.html', allgroups=allgroups, allhosts=allhosts)

    def post(self):
        hremove = flask.request.form.getlist('selectedhostsremove')
        gremove = flask.request.form.getlist('selectedgroupsremove')
        grpdelbtnvalue = flask.request.form.get('removegroup', None)
        hostdelbtnvalue = flask.request.form.get('removehost', None)

        if hremove:
            for item in hremove:
                self.host(item)
        elif gremove:
            for item in gremove:
                self.group(item)
        elif grpdelbtnvalue:
            self.group(grpdelbtnvalue)
            return flask.redirect('getgroup')
        elif hostdelbtnvalue:
            self.host(hostdelbtnvalue)
            return flask.redirect('gethostinfo')

        return flask.redirect('remove')

    def host(self, hostname):
        db.hosts.remove({'hostname': hostname})
        groups = db.groups.find({'hosts': hostname}).distinct('groupname')
        for item in groups:
             db.groups.update({'groupname': item}, {'$pull': {'hosts': hostname}})

    def group(self, groupname):
        db.groups.remove({'groupname': groupname})
        parent_groups = db.groups.find({'children': groupname}).distinct('groupname')
        child_groups = db.groups.find({'parents': groupname}).distinct('groupname')
        for item in parent_groups:
            db.groups.update({'groupname': item}, {'$pull': {'children': groupname}})

    def tag(self, tagname):
        db.tags.remove({'tagname': tagname})
        linked_groups = None # TODO: Define the dependancy chain here
        linked_hosts = None # TODO: Define the dependancy chain here
        linked_roles = None # TODO: Define the dependancy chain here
        
        """
        for item in linked_groups:
            db.groups.update({'groupname': item}, {'$pull': {'tagname': tagname}})
        
        for item in linked_hosts:
            db.hosts.update({'hostname': item}, {'$pull': {'tagname': tagname}})

        for item in linked_roles:
            # TODO: db.roles.update({'rolename': item}, {'$pull': {'tagname': tagname}})
            # Roles don't exist yet - might break if i try this
            pass
        """