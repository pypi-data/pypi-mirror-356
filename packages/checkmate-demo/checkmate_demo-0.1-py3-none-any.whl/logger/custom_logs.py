import logging
import os
import sys
import io
import boto3
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Environment variables
LOG_DESTINATION = os.getenv("LOG_DESTINATION", "file")
LOG_S3_BUCKET = os.getenv("LOG_S3_BUCKET")
LOG_S3_KEY_TEMPLATE = os.getenv("LOG_S3_KEY_TEMPLATE", "logs/%Y/%m/%d/log-%H-%M-%S.log")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/output")
MAX_LOG_FILE_SIZE_KB = int(os.getenv("MAX_LOG_FILE_SIZE_KB", "100"))
UPLOAD_INTERVAL_SECONDS = int(os.getenv("UPLOAD_INTERVAL_SECONDS", "10"))
LOG_ROTATION_INTERVAL_SECONDS = int(os.getenv("LOG_ROTATION_INTERVAL_SECONDS", "60"))
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class S3StreamHandler(logging.Handler):
    def __init__(self, bucket_name, key_template):
        super().__init__()
        self.bucket = bucket_name
        self.key_template = key_template
        self.log_stream = io.StringIO()
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        self._generate_new_key()
        self.last_upload_time = datetime.utcnow()

    def _generate_new_key(self):
        now = datetime.utcnow()
        self.current_key = now.strftime(self.key_template)

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.log_stream.write(log_entry + "\n")
            now = datetime.utcnow()
            if (now - self.last_upload_time).total_seconds() >= UPLOAD_INTERVAL_SECONDS:
                self._upload_logs()
                self.last_upload_time = now
                self._generate_new_key()
        except Exception as e:
            sys.__stderr__.write(f"[ERROR] Failed to write log entry: {e}\n")

    def _upload_logs(self):
        content = self.log_stream.getvalue()
        if content:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=self.current_key,
                Body=content.encode("utf-8")
            )
            self.log_stream = io.StringIO()

    def close(self):
        self._upload_logs()
        super().close()


class CustomTimeRotatingFileHandler(logging.Handler):
    def __init__(self, base_path, rotation_interval_seconds):
        super().__init__()
        self.base_path = base_path
        self.rotation_interval = timedelta(seconds=rotation_interval_seconds)
        self.last_rotation = datetime.now()
        self._rotate_file()

    def _rotate_file(self):
        timestamp = self.last_rotation.strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(os.path.dirname(self.base_path), exist_ok=True)
        self.current_log_file = f"{self.base_path}-{timestamp}.log"
        self.stream = open(self.current_log_file, "a", encoding="utf-8")

    def emit(self, record):
        now = datetime.now()
        if now - self.last_rotation >= self.rotation_interval:
            self.stream.close()
            self.last_rotation = now
            self._rotate_file()
        msg = self.format(record)
        self.stream.write(msg + "\n")
        self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()


class StreamToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
        self.original_stdout = sys.__stdout__

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if line.strip():
                self.logger.log(self.level, line)
                self.original_stdout.write(line + "\n")
                self.original_stdout.flush()

    def flush(self):
        self.original_stdout.flush()


class LoggerConfigurator:
    def __init__(self, name="custom_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._configured = False
        self.s3_handler = None
        self.local_handler = None
        self.console_handler = None
        self._setup_handlers()
        self._redirect_print_once()

    def _setup_handlers(self):
        if self.logger.handlers:  # <-- Checks if handlers already exist
            return

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

        # Local file or S3 handler
        if LOG_DESTINATION.lower() == "s3":
            self.s3_handler = S3StreamHandler(LOG_S3_BUCKET, LOG_S3_KEY_TEMPLATE)
            self.s3_handler = S3StreamHandler(LOG_S3_BUCKET, LOG_S3_KEY_TEMPLATE)
            self.s3_handler.setFormatter(formatter)
            self.logger.addHandler(self.s3_handler)
        else:
            base_path = os.path.splitext(LOG_FILE_PATH)[0]
            self.local_handler = CustomTimeRotatingFileHandler(
                base_path=base_path,
                rotation_interval_seconds=LOG_ROTATION_INTERVAL_SECONDS
            )
            self.local_handler.setFormatter(formatter)
            self.logger.addHandler(self.local_handler)

    def _redirect_print_once(self):
        # Redirect print() output to logger so it goes to log file/S3 AND console
        if not isinstance(sys.stdout, StreamToLogger):
            sys.stdout = StreamToLogger(self.logger, logging.INFO)
        if not isinstance(sys.stderr, StreamToLogger):
            sys.stderr = StreamToLogger(self.logger, logging.ERROR)

    def get_logger(self):
        return self.logger

    def shutdown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        if self.s3_handler:
            try:
                self.s3_handler.flush()
            except Exception as e:
                print(f"Flush failed for S3 handler: {e}")
            self.s3_handler.close()

        # Flush and close local file handler
        if self.local_handler:
            try:
                self.local_handler.flush()
            except Exception as e:
                print(f"Flush failed for local handler: {e}")
            self.local_handler.close()
        if self.console_handler:
            self.console_handler.close()

        logging.shutdown()
