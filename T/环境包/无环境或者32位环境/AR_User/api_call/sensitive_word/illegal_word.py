# coding=utf-8
"""
@author: 'jing'
"""
import re
import cof.file as cofFile


def judge_sensitive_word(words):
    app_loc = cofFile.get_app_loc()
    path = app_loc + 'api_call/sensitive_word/sensitiveWord.txt'
    ex_path = cofFile.expand_links(path)
    f = open(ex_path)
    s = f.read()
    s1 = re.split(' ', s)

    for i in s1:
        if i != "":
            if i in words:
                return False
    return True

if __name__ == '__main__':
    word = "囧絲鸍稢紸焆 "
    test = judge_sensitive_word(word)
    print test
