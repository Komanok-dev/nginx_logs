from django.test import TestCase
from logs.models import NginxLog, FileProgress


class NginxLogModelTest(TestCase):

    def setUp(self):
        self.log = NginxLog.objects.create(
            ip_address="127.0.0.1",
            log_time="2023-09-28 12:00:00+00:00",
            http_method="GET",
            uri="/test",
            http_version="HTTP/1.1",
            response_code=200,
            response_size=123,
            remote_user="user",
            referrer="http://example.com",
            user_agent="test-agent",
        )

    def test_nginx_log_creation(self):
        self.assertEqual(self.log.ip_address, "127.0.0.1")
        self.assertEqual(self.log.http_method, "GET")
        self.assertEqual(self.log.response_code, 200)


class FileProgressModelTest(TestCase):

    def setUp(self):
        self.file_progress = FileProgress.objects.create(
            file_path="/path/to/file", position=10
        )

    def test_file_progress_creation(self):
        self.assertEqual(self.file_progress.position, 10)
        self.assertEqual(self.file_progress.file_path, "/path/to/file")
