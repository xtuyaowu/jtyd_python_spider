from celery_tasks.weibo import comment

if __name__ == '__main__':
    comment.excute_comment_task()