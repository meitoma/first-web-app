from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from __init__ import db,app
from flask_login import current_user
from bbs_app.models import Users,Messages,Threads,UserAccess,FCMToken,WorkSpaces,WSAccessUser

# adminページ
admin = Admin(
    app,
    name='Flask-admin laboratory',
    template_mode='bootstrap4',
    index_view=AdminIndexView(template='bbs_app/admin/index.html')
)

class MyModelView1(sqla.ModelView):
    can_view_details = True
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin

class MyModelView2(sqla.ModelView):
    can_view_details = True
    column_list = ["message","sendtime","user_id","thread_id"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin
    
class MyModelView3(sqla.ModelView):
    can_view_details = True
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin

class MyModelView4(sqla.ModelView):
    can_view_details = True
    column_list = ["user_id","thread_id"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin
    
class MyModelView5(sqla.ModelView):
    can_view_details = True
    column_list = ["user_id","token"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin
    
class MyModelView6(sqla.ModelView):
    can_view_details = True
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin
        
class MyModelView7(sqla.ModelView):
    can_view_details = True
    column_list = ["user_id","ws_id"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin
    
UsersAdminView = MyModelView1(Users, db.session)
MessagesAdminView = MyModelView2(Messages, db.session)
ThreadsAdminView = MyModelView3(Threads, db.session)
UserAccessAdminView = MyModelView4(UserAccess, db.session)
FCMTokenAdminView = MyModelView5(FCMToken, db.session)
WorkSpacesAdminView = MyModelView6(WorkSpaces, db.session)
WSAccessUserAdminView = MyModelView7(WSAccessUser, db.session)

admin.add_views(UsersAdminView,MessagesAdminView,ThreadsAdminView,
                UserAccessAdminView,FCMTokenAdminView,WorkSpacesAdminView,
                WSAccessUserAdminView
                )