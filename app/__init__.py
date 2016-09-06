import flask
import flask.views


app = flask.Flask('app')
app.config.from_pyfile('../config.cfg')

from flask_restful import Api

api = Api(app)

from app.modules.host.api import GetHostVarsAPI, HostsAPI, GetHostsSearchAPI, GetHostGroupsAPI
from app.modules.host.add_host import AddHost
from app.modules.host.get_host import GetHost, GetAllHosts
from app.modules.host.edit_host import EditHost, EditHostSubmit

from app.modules.group.api import GroupsAPI, GetGroupsSearchAPI, GetGroupVarsAPI, GetGroupChildrenAPI, GetGroupHostsAPI, DescribeGroupsAPI
from app.modules.group.get_group import GetGroup, GetAllGroups
from app.modules.group.add_group import AddGroup
from app.modules.group.edit_group import EditGroup, EditGroupSubmit

# from app.modules.tag.api import TagsAPI
# from app.modules.tag.get_tag import GetAllTags, GetTag
# from app.modules.tag.add_tag import AddTag

from app.modules.role.add_role import AddRole
from app.modules.role.get_role import GetRole, GetAllRoles
from app.modules.role.api import GetRolesSearchAPI, GetRoleTagsAPI, RolesAPI

from remove import Remove


class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        pass


api.add_resource(GetHostVarsAPI, '/api/hosts/<string:hostname>/vars')
api.add_resource(GetHostGroupsAPI, '/api/hosts/<string:hostname>/groups')
api.add_resource(GetHostsSearchAPI, '/api/hosts/search/<string:search_term>')
api.add_resource(HostsAPI, '/api/hosts')

api.add_resource(GetGroupChildrenAPI, '/api/groups/<string:groupname>/children')
api.add_resource(GetGroupVarsAPI, '/api/groups/<string:groupname>/vars')
api.add_resource(GetGroupHostsAPI, '/api/groups/<string:groupname>/hosts')
api.add_resource(GetGroupsSearchAPI, '/api/groups/search/<string:search_term>')
api.add_resource(GroupsAPI, '/api/groups')

# api.add_resource(TagsAPI,'/api/tags')

api.add_resource(RolesAPI,'/api/roles')
api.add_resource(GetRoleTagsAPI,'/api/roles/<string:rolename>/tags')
api.add_resource(GetRolesSearchAPI,'/api/roles/search/<string:search_term>')

app.add_url_rule('/', view_func=Main.as_view('index'), methods=['GET', 'POST'])

app.add_url_rule('/addhost', view_func=AddHost.as_view('addhost'), methods=['GET', 'POST'])
app.add_url_rule('/gethostinfo', view_func=GetHost.as_view('gethostinfo'), methods=['GET', 'POST'])
app.add_url_rule('/getallhosts', view_func=GetAllHosts.as_view('getallhosts'), methods=['POST','GET'])
app.add_url_rule('/edithost', view_func=EditHost.as_view('edithost'), methods=['GET', 'POST'])
app.add_url_rule('/edithostsubmit', view_func=EditHostSubmit.as_view('edithostsubmit'), methods=['GET', 'POST'])

app.add_url_rule('/editgroup', view_func=EditGroup.as_view('editgroup'), methods=['GET', 'POST'])
app.add_url_rule('/editgroupsubmit', view_func=EditGroupSubmit.as_view('editgroupsubmit'), methods=['GET', 'POST'])
app.add_url_rule('/getgroup', view_func=GetGroup.as_view('getgroup'), methods=['GET', 'POST'])
app.add_url_rule('/getallgroups', view_func=GetAllGroups.as_view('getallgroups'), methods=['GET', 'POST'])
app.add_url_rule('/addgroups', view_func=AddGroup.as_view('addgroup'), methods=['GET', 'POST'])

# app.add_url_rule('/addtag', view_func=AddTag.as_view('addtag'), methods=['GET', 'POST'])
# app.add_url_rule('/getalltags', view_func=GetAllTags.as_view('getalltags'), methods=['GET', 'POST'])
# app.add_url_rule('/gettaginfo', view_func=GetTag.as_view('gettaginfo'), methods=['GET', 'POST'])

app.add_url_rule('/addrole', view_func=AddRole.as_view('addrole'), methods=['GET', 'POST'])
app.add_url_rule('/getroleinfo', view_func=GetRole.as_view('getroleinfo'), methods=['GET', 'POST'])
app.add_url_rule('/getallroles', view_func=GetAllRoles.as_view('getallroles'), methods=['GET', 'POST'])

app.add_url_rule('/remove', view_func=Remove.as_view('remove'), methods=['GET', 'POST'])

