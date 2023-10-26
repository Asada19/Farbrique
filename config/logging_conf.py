import json
import logging
from datetime import datetime
from typing import Dict, Any

from pythonjsonlogger import jsonlogger


class CustomLoggerFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super(CustomLoggerFormatter, self).add_fields(log_record, record, message_dict)
        
        log_record.pop('message')
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S:%fZ')
        if not log_record.get('level'):
            log_record['level'] = record.levelname

