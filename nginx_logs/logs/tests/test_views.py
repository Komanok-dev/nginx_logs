from rest_framework.test import APIClient, APITestCase
from logs.models import NginxLog


class NginxLogViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        NginxLog.objects.create(
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

    def test_nginx_log_list(self):
        response = self.client.get("/api/logs/")
        self.assertEqual(response.status_code, 200)

        # Check if the response is paginated
        self.assertIn("results", response.data)

        # Make sure only one log is returned in the results
        self.assertEqual(len(response.data["results"]), 1)

        # Verify the content of the log entry
        self.assertEqual(response.data["results"][0]["ip_address"], "127.0.0.1")
        self.assertEqual(response.data["results"][0]["http_method"], "GET")
