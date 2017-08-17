# coding:utf-8
from celery_tasks.weibo import user

if __name__ == '__main__':
    # user.excute_user_personal_adver_task('你好,一直在组织大家做数据积累、挖掘、可视化、'
    #                                      '互联网推广方面的应用，多多交流咯，谢谢！ www.wmjtyd.com')
    user.excute_user_personal_adver_task('你好,最近忙什么呢？')