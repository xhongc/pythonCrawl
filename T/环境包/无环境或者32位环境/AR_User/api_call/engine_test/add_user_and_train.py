# coding=utf-8
'''
@author: 'wang'
'''

import os
import csv
import codecs
import sys
import time
sys.path.insert(0, '..')
from api_call.face_api.face_api import FaceApi

reload(sys)
sys.setdefaultencoding('utf8')

face = FaceApi()
group_name = "QA-Test-Group"


def is_group_exist():
    data = face.group_exist(group_name)
    if data["exist"] is True:
        print 'group ' + group_name + ' exist...'
        return True
    else:
        print 'group ' + group_name + ' not exist...'
        return False


def is_person_exist(person_name):
    data = face.person_exist(person_name)
    if data["exist"] is True:
        print 'person ' + person_name + ' exist...'
        return True
    else:
        print 'person ' + person_name + ' not exist...'
        return False


def create_group():
    print 'create group...'
    face.group_create(group_name)


def create_person():
    file_path = "D:\\workspace\\ARScoketTest\\face\\"
    path_dir = os.listdir(file_path)
    for path in path_dir:
        person_name = path
        child_dirs = os.listdir(file_path + path)
        file_name = path + '/' + child_dirs[0]
        person_img = 'http://192.168.239.119:807/' + file_name
        if not is_person_exist(person_name):
            print 'person not exist...'
            time.sleep(2)
            print 'create ' + person_name
            face.person_create(person_name, person_img)
        time.sleep(2)
        print 'add ' + person_name + ' to ' + group_name
        time.sleep(2)
        face.group_add_person(group_name, person_name)


def train_identify():
    print group_name + ' train_identify...'
    face.train_identify(group_name)


def delete_person(person_name):
    print 'delete person...'
    face.person_delete(person_name)


def get_person_info():
    data = face.group_get_info(group_name)
    return data["person_name"]


def remove_persons(names):
    for name in names:
        time.sleep(3)
        print "remove " + name
        face.group_remove_person(group_name, str(name))


def recognition_identify(img):
    return face.recognition_identify(group_name, str(img))


create_person()
train_identify()
