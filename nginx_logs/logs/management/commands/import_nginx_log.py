import json
import re
import requests
from django.core.management.base import BaseCommand
from logs.models import NginxLog, FileProgress
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Import Nginx log file from a URL or local path into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path or URL to the Nginx log file')

    def handle(self, *args, **kwargs):

        # file_path = kwargs['file_path']
        # print('HELLO', file_path)
        # batch = []
        # batch.append(NginxLog(
        #     ip_address='remote_ip',
        #     log_time='time',
        #     http_method='request',
        #     uri='uri',
        #     http_version='http_version',
        #     response_code='response',
        #     response_size='bytes',
        #     remote_user='remote_user',
        #     referrer='referrer',
        #     user_agent='agent'
        # ))
        # NginxLog.objects.bulk_create(batch)

        file_path = kwargs['file_path']
        batch_size = 100
        batch = []

        # Check if file is in database
        file_progress = FileProgress.objects.get_or_create(file_path=file_path)[0]

        # Check whether local file or url
        if file_path.startswith('http://') or file_path.startswith('https://'):
            if 'drive.google.com' in file_path:
                google_id = self.extract_google_drive_id(file_path)
                file_path = 'https://drive.google.com/uc?id=' + google_id
            self.import_from_url(file_path, batch, batch_size, file_progress)
        else:
            self.import_from_local(file_path, batch, batch_size, file_progress)

        self.stdout.write(self.style.SUCCESS('Log file has been imported successfully'))

    def process_line(self, line, batch, batch_size, file_progress):
        """
        Processes a log line and adds it to the batch for saving.
        """
        try:
            line = line.strip()
            if not line:
                return
            log_entry = json.loads(line)

            # Add model in batch
            batch.append(NginxLog(
                ip_address=log_entry.get('remote_ip'),
                log_time=datetime.strptime(log_entry.get('time'), '%d/%b/%Y:%H:%M:%S %z'),
                http_method=log_entry.get('request').split(' ')[0],
                uri=log_entry.get('request').split(' ')[1],
                http_version=log_entry.get('request').split(' ')[2],
                response_code=log_entry.get('response'),
                response_size=log_entry.get('bytes'),
                remote_user=log_entry.get('remote_user') if log_entry.get('remote_user') != '-' else None,
                referrer=log_entry.get('referrer') if log_entry.get('referrer') != '-' else None,
                user_agent=log_entry.get('agent') if log_entry.get('agent') != '-' else None
            ))

            # Update current position
            file_progress.position += len(line) + 1  # +1 for symbol at new line

            # If batch reached batch size insert to database
            if len(batch) >= batch_size:
                NginxLog.objects.bulk_create(batch)
                batch.clear()
                # Update position in database if insert was success
                file_progress.save()

        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Error decoding JSON: {e}"))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f"Missing key in log entry: {e}"))

    def import_from_local(self, file_path, batch, batch_size, file_progress):
        """
        Import logs from local file.
        """
        with open(file_path, 'r') as file:
            file.seek(file_progress.position)  # Move to correct file position
            for line in file:
                self.process_line(line, batch, batch_size, file_progress)

        # Save remain batch
        if batch:
            NginxLog.objects.bulk_create(batch)
            # Update position in database
            file_progress.save()

    def import_from_url(self, file_path, batch, batch_size, file_progress, retries=3, backoff_factor=2):
        """
        Import logs from url with retries in case of network error.
        """
        attempt = 0
        
        while attempt < retries:
            try:
                # Define range for partial load
                headers = {"Range": f"bytes={file_progress.position}-"}  
                response = requests.get(file_path, headers=headers, stream=True, timeout=10)
                response.raise_for_status()

                # Read file line by line from HTTP-response
                for line in response.iter_lines():
                    if line:  # Skip blank lines
                        self.process_line(line.decode('utf-8'), batch, batch_size, file_progress)

                break  # Exit from loop if download was successful

            except (requests.ConnectionError, requests.Timeout) as e:
                attempt += 1
                wait_time = backoff_factor ** attempt
                self.stderr.write(self.style.ERROR(
                    f"Network error: {e}. Retrying {attempt}/{retries} in {wait_time} seconds..."
                ))
                time.sleep(wait_time)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 416:
                    # Handle the 416 Range Not Satisfiable error
                    self.stderr.write(self.style.WARNING(
                        f"Received 416 Error for file: {file_path}. All data is already in database."
                    ))
                    break
        else:
            self.stderr.write(self.style.ERROR("Failed to import file after multiple attempts."))

        # Save remain batch
        if batch:
            NginxLog.objects.bulk_create(batch)
            # Update position in database
            file_progress.save()

    def extract_google_drive_id(self, url):
        # Regular expression to find ID in URL
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
        else:
            return None
