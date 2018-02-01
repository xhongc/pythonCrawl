#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2012 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, with_statement

import contextlib

import glob

import logging

import os
import re

import subprocess

import sys

import tempfile

import warnings

from tornado.escape import utf8

from tornado.log import LogFormatter, define_logging_options, enable_pretty_logging

from tornado.options import OptionParser

from tornado.test.util import unittest

from tornado.util import u, basestring_type


@contextlib.contextmanager
def ignore_bytes_warning():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=BytesWarning)
        yield


class LogFormatterTest(unittest.TestCase):
    # Matches 
    # the output of a single logging call (which may be multiple lines
    # if a traceback was included, so we use the DOTALL option)
# (?s)
# \x01
# [E]
# \x02
    LINE_RE = re.compile(b"(?s)\x01\\[E [0-9]{6} [0-9]{2}:[0-9]{2}:[0-9]{2} log_test:[0-9]+\\]\x02 (.*)")

    LINE_RE2 = re.compile("(?s)\x01log_test")

    print("对象:")
    print(LINE_RE)

#{{{
    def setUp(self):

        self.formatter = LogFormatter(color=False)

        # Fake color support.  
# We can't guarantee anything about the $TERM
        # variable when the tests are run, so just patch in some values
        # for testing.  (testing with color off fails to expose some potential
        # encoding issues from the control characters)
        self.formatter._colors = {
            logging.ERROR: u("\u0001"),
        }

        self.formatter._normal = u("\u0002")

        # construct a Logger directly to bypass getLogger's caching
        # 定义一个logger，带上标识，标识唯一的logger对象
        #self.logger = logging.Logger('LogFormatterTest')
        self.logger = logging.Logger('test')

        self.logger.propagate = False

        self.tempdir = tempfile.mkdtemp()
        print(self.tempdir)

        # self.filename = os.path.join(self.tempdir, 'log.out')
        self.filename = './log.out'
        print(self.filename)

        self.handler = self.make_handler(self.filename)

        self.handler.setFormatter(self.formatter)

        # 添加日志处理器
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.handler.close()
        #os.unlink(self.filename)
        #os.rmdir(self.tempdir)
#}}}

    def make_handler(self, filename):
        # Base case: default setup without explicit encoding.
        # In python 2, supports arbitrary byte strings and unicode objects
        # that contain only ascii.  In python 3, supports ascii-only unicode
        # strings (but byte strings will be repr'd automatically).
        return logging.FileHandler(filename)

    def get_output(self):
        with open(self.filename, "rb") as f:
            print(self.filename)
            line = f.read().strip()
            print(line)

            #m = LogFormatterTest.LINE_RE2.match(line)
            line2 = "[E 141015 18:02:31 log_test:136] foo"
            line3 = "\x01log_test"
            print(repr(line3))
            print(line3)
            m = LogFormatterTest.LINE_RE2.search(line3)
            #m = LogFormatterTest.LINE_RE2.search(line)
            print("匹配")
            print(m)

            #if m:
                #return m.group(1)
            #else:
                #raise Exception("output didn't match regex: %r" % line)

    def test_basic_logging(self):
        self.logger.error("foo")

        self.assertEqual(self.get_output(), b"foo")

if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
