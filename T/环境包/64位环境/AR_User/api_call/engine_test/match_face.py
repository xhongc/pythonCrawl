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
        if is_person_exist(person_name):
            print 'person exist...'
            time.sleep(2)
            delete_person(person_name)
        time.sleep(2)
        face.person_create(person_name, person_img)
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


def init_recognition():
    if not is_group_exist():
        create_group()
        create_person()
        train_identify()

    else:
        names = get_person_info()
        remove_persons(names)
        create_person()
        train_identify()

init_recognition()

for i in range(1):
    result_list = []
    file_path = "D:\\workspace\\ARScoketTest\\face\\"
    pathDir = os.listdir(file_path)
    for path in pathDir:
        child_dir = os.listdir(file_path + path)
        j = 0
        for jpg in child_dir:
            if j == 0:
                j += 1
                continue
            row = []
            filename = path + '/' + jpg
            face_url = 'http://192.168.239.119:807/' + filename
            time.sleep(8)
            web_data = recognition_identify(face_url)
            row.append(filename)
            if web_data["error_code"] is 0:
                row.append(web_data["flag"])
                for scores in web_data["candidate"]:
                    row.append(scores["person_name"])
                    row.append(scores["confidence"])
            else:
                row.append("Error")
                row.append(web_data["error_code"])
                row.append(web_data["error"])
            result_list.append(row)
    print result_list
    with open('result' + str(i) + '.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(["jpg_name", "result", "person_name", "confidence"])
        for result in result_list:
            spamwriter.writerow(result)