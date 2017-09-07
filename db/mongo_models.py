import mongoengine

# 消息监控表
class task_monitor(mongoengine.Document):
    '''
    用于存储消息信息
    '''
    _id = mongoengine.ObjectIdField()
    task_id =  mongoengine.StringField()
    task_name =  mongoengine.StringField()
    before_sent_args =  mongoengine.StringField()
    task_prerun_args =  mongoengine.ListField()

    celery_stask_status = mongoengine.IntField() #

    create_time = mongoengine.DateTimeField()
    update_time = mongoengine.DateTimeField(default = None)