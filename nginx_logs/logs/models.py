from django.db import models


class NginxLog(models.Model):
    log_time = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    http_method = models.CharField(max_length=10)
    uri = models.TextField()
    response_code = models.IntegerField()
    response_size = models.IntegerField()
    http_version = models.CharField(max_length=10)
    remote_user = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_time} {self.ip_address} {self.http_method} {self.uri} {self.response_code} {self.response_size}"


class FileProgress(models.Model):
    file_path = models.CharField(max_length=255, unique=True)
    position = models.BigIntegerField(default=0)  # BigInteger for big files

    def __str__(self):
        return f"{self.file_path} - {self.position}"
