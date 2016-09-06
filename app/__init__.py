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


api.add_resource(GetHostVarsAPI, '/api/ironhide/hosts/<string:hostname>/vars')
api.add_resource(GetHostGroupsAPI, '/api/ironhide/hosts/<string:hostname>/groups')
api.add_resource(GetHostsSearchAPI, '/api/ironhide/hosts/search/<string:search_term>')
api.add_resource(HostsAPI, '/api/ironhide/hosts')

api.add_resource(GetGroupChildrenAPI, '/api/ironhide/groups/<string:groupname>/children')
api.add_resource(GetGroupVarsAPI, '/api/ironhide/groups/<string:groupname>/vars')
api.add_resource(GetGroupHostsAPI, '/api/ironhide/groups/<string:groupname>/hosts')
api.add_resource(GetGroupsSearchAPI, '/api/ironhide/groups/search/<string:search_term>')
api.add_resource(GroupsAPI, '/api/ironhide/groups')

# api.add_resource(TagsAPI,'/api/ironhide/tags')

api.add_resource(RolesAPI,'/api/ironhide/roles')
api.add_resource(GetRoleTagsAPI,'/api/ironhide/roles/<string:rolename>/tags')
api.add_resource(GetRolesSearchAPI,'/api/ironhide/roles/search/<string:search_term>')

app.add_url_rule('/', view_func=Main.as_view('index'), methods=['GET', 'POST'])
#app.add_url_rule('/ironhide/', view_func=Main.as_view('index'), methods=['GET', 'POST'])

app.add_url_rule('/ironhide/addhost', view_func=AddHost.as_view('addhost'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/gethostinfo', view_func=GetHost.as_view('gethostinfo'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/getallhosts', view_func=GetAllHosts.as_view('getallhosts'), methods=['POST','GET'])
app.add_url_rule('/ironhide/edithost', view_func=EditHost.as_view('edithost'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/edithostsubmit', view_func=EditHostSubmit.as_view('edithostsubmit'), methods=['GET', 'POST'])

app.add_url_rule('/ironhide/editgroup', view_func=EditGroup.as_view('editgroup'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/editgroupsubmit', view_func=EditGroupSubmit.as_view('editgroupsubmit'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/getgroup', view_func=GetGroup.as_view('getgroup'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/getallgroups', view_func=GetAllGroups.as_view('getallgroups'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/addgroups', view_func=AddGroup.as_view('addgroup'), methods=['GET', 'POST'])

# app.add_url_rule('/addtag', view_func=AddTag.as_view('addtag'), methods=['GET', 'POST'])
# app.add_url_rule('/getalltags', view_func=GetAllTags.as_view('getalltags'), methods=['GET', 'POST'])
# app.add_url_rule('/gettaginfo', view_func=GetTag.as_view('gettaginfo'), methods=['GET', 'POST'])

app.add_url_rule('/ironhide/addrole', view_func=AddRole.as_view('addrole'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/getroleinfo', view_func=GetRole.as_view('getroleinfo'), methods=['GET', 'POST'])
app.add_url_rule('/ironhide/getallroles', view_func=GetAllRoles.as_view('getallroles'), methods=['GET', 'POST'])

app.add_url_rule('/ironhide/remove', view_func=Remove.as_view('remove'), methods=['GET', 'POST'])

