


    def test_utf8_logging(self):
        self.logger.error(u("\u00e9").encode("utf8"))
        if issubclass(bytes, basestring_type):
            # on python 2, utf8 byte strings (and by extension ascii byte
            # strings) are passed through as-is.
            self.assertEqual(self.get_output(), utf8(u("\u00e9")))
        else:
            # on python 3, byte strings always get repr'd even if
            # they're ascii-only, so this degenerates into another
            # copy of test_bytes_logging.
            self.assertEqual(self.get_output(), utf8(repr(utf8(u("\u00e9")))))

    def test_bytes_exception_logging(self):
        try:
            raise Exception(b'\xe9')
        except Exception:
            self.logger.exception('caught exception')
        # This will be "Exception: \xe9" on python 2 or
        # "Exception: b'\xe9'" on python 3.
        output = self.get_output()
        self.assertRegexpMatches(output, br'Exception.*\\xe9')
        # The traceback contains newlines, which should not have been escaped.
        self.assertNotIn(br'\n', output)


class UnicodeLogFormatterTest(LogFormatterTest):
    def make_handler(self, filename):
        # Adding an explicit encoding configuration allows non-ascii unicode
        # strings in both python 2 and 3, without changing the behavior
        # for byte strings.
        return logging.FileHandler(filename, encoding="utf8")

    def test_unicode_logging(self):
        self.logger.error(u("\u00e9"))
        self.assertEqual(self.get_output(), utf8(u("\u00e9")))


class EnablePrettyLoggingTest(unittest.TestCase):
    def setUp(self):
        super(EnablePrettyLoggingTest, self).setUp()
        self.options = OptionParser()
        define_logging_options(self.options)
        self.logger = logging.Logger('tornado.test.log_test.EnablePrettyLoggingTest')
        self.logger.propagate = False

    def test_log_file(self):
        tmpdir = tempfile.mkdtemp()
        try:
            self.options.log_file_prefix = tmpdir + '/test_log'

            enable_pretty_logging(options=self.options, logger=self.logger)

            self.assertEqual(1, len(self.logger.handlers))

            self.logger.error('hello')
            self.logger.handlers[0].flush()

            filenames = glob.glob(tmpdir + '/test_log*')

            self.assertEqual(1, len(filenames))

            with open(filenames[0]) as f:
                self.assertRegexpMatches(f.read(), r'^\[E [^]]*\] hello$')

        finally:
            for handler in self.logger.handlers:
                handler.flush()
                handler.close()

            for filename in glob.glob(tmpdir + '/test_log*'):
                os.unlink(filename)

            os.rmdir(tmpdir)


class LoggingOptionTest(unittest.TestCase):
    """
    测试日志选项
    Test the ability to enable and disable Tornado's logging hooks."""
    def logs_present(self, statement, args=None):
        # Each test may manipulate and/or parse the options and then logs
        # a line at the 'info' level.  This level is ignored in the
        # logging module by default, but Tornado turns it on by default
        # so it is the easiest way to tell whether tornado's logging hooks
        # ran.
        IMPORT = 'from tornado.options import options, parse_command_line'

        LOG_INFO = 'import logging; logging.info("hello")'

        program = ';'.join([IMPORT, statement, LOG_INFO])

        proc = subprocess.Popen(
            [sys.executable, '-c', program] + (args or []),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        stdout, stderr = proc.communicate()

        self.assertEqual(proc.returncode, 0, 'process failed: %r' % stdout)

        return b'hello' in stdout

    def test_default(self):
        self.assertFalse(self.logs_present('pass'))

    def test_tornado_default(self):
        self.assertTrue(self.logs_present('parse_command_line()'))

    def test_disable_command_line(self):
        self.assertFalse(self.logs_present('parse_command_line()',
                                           ['--logging=none']))

    def test_disable_command_line_case_insensitive(self):
        self.assertFalse(self.logs_present('parse_command_line()',
                                           ['--logging=None']))

    def test_disable_code_string(self):
        self.assertFalse(self.logs_present(
            'options.logging = "none"; parse_command_line()'))

    def test_disable_code_none(self):
        self.assertFalse(self.logs_present(
            'options.logging = None; parse_command_line()'))

    def test_disable_override(self):
        # command line trumps code defaults
        self.assertTrue(self.logs_present(
            'options.logging = None; parse_command_line()',
            ['--logging=info']))
