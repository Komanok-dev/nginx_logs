from django.test import TestCase
from logs.models import NginxLog
from logs.serializers import NginxLogSerializer


class NginxLogSerializerTest(TestCase):

    def setUp(self):
        self.log_data = {
            "ip_address": "127.0.0.1",
            "log_time": "2023-09-28 12:00:00+00:00",
            "http_method": "GET",
            "uri": "/test",
            "http_version": "HTTP/1.1",
            "response_code": 200,
            "response_size": 123,
            "remote_user": "user",
            "referrer": "http://example.com",
            "user_agent": "test-agent",
        }

    def test_nginx_log_serializer(self):
        serializer = NginxLogSerializer(data=self.log_data)
        self.assertTrue(serializer.is_valid())
