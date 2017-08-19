# coding:utf-8
from apps.celery_init import celery
from page_get import user as user_get
from page_get.basic import send_personal_message
from db.seed_ids import get_seed_ids, get_seed_by_id, insert_seeds, set_seed_other_crawled, get_seed
from time import sleep
import random

@celery.task(ignore_result=True)
def crawl_follower_fans(uid):
    seed = get_seed_by_id(uid)
    if seed.other_crawled == 0:
        rs = user_get.get_fans_or_followers_ids(uid, 1)
        rs.extend(user_get.get_fans_or_followers_ids(uid, 2))
        datas = set(rs)
        # If data already exits, just skip it
        if datas:
            insert_seeds(datas)
        set_seed_other_crawled(uid)


@celery.task(ignore_result=True)
def crawl_person_infos(uid):
    """
    Crawl user info and their fans and followers
    For the limit of weibo's backend, we can only crawl 5 pages of the fans and followers.
    We also have no permissions to view enterprise's followers and fans info
    :param uid: current user id
    :return: None
    """
    if not uid:
        return

    user = user_get.get_profile(uid)
    # If it's enterprise user, just skip it
    if user.verify_type == 2:
        set_seed_other_crawled(uid)
        return

    # Crawl fans and followers
    celery.send_task('celery_tasks.weibo.user.crawl_follower_fans', args=(uid,), queue='fans_followers',
                     routing_key='for_fans_followers')


@celery.task(ignore_result=True)
def excute_user_task():
    seeds = get_seed_ids()
    if seeds:
        for seed in seeds:
            celery.send_task('celery_tasks.weibo.user.crawl_person_infos', args=(seed.uid,), queue='user_crawler',
                             routing_key='for_user_info')


@celery.task(ignore_result=True)
def excute_personal_adver(uid, adver_message):
    send_personal_message(uid, adver_message)


@celery.task(ignore_result=True)
def excute_user_personal_adver_task(adv_message):
    seeds = get_seed()
    if seeds:
        for seed in seeds:
            sleep(random.randint(1, 6))
            print(seed.uid)
            celery.send_task('celery_tasks.weibo.user.excute_personal_adver', args=(seed.uid, adv_message), queue='personal_adver',
                             routing_key='for_adver')
