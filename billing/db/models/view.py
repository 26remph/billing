from sqladmin import ModelView

from billing.db.models import Content, SubscriberChanel, ContentUser, Task, TemplateStatic


class ContentAdmin(ModelView, model=Content):
    column_list = [Content.id]


class SubscriberChanelAdmin(ModelView, model=SubscriberChanel):
    column_list = [SubscriberChanel.id]


class ContentUserAdmin(ModelView, model=ContentUser):
    column_list = [ContentUser.id]


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id]


class TemplateStaticAdmin(ModelView, model=TemplateStatic):
    column_list = [TemplateStatic.id]


