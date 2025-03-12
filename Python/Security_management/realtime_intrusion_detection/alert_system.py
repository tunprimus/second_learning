#!/usr/bin/env python3
# Adapted from: How to Build a Real-Time Intrusion Detection System with Python and Open-Source Libraries -> https://www.freecodecamp.org/news/build-a-real-time-intrusion-detection-system-with-python/
import json
import logging
from datetime import datetime
from os.path import realpath as realpath


class AlertSystem:
    def __init__(self, log_file=realpath("./ids_alerts.log")):
        self.logger = logging.getLogger("IDS_Alerts")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def generate_alert(self, threat, packet_info):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "threat_type": threat["type"],
            "source_ip": packet_info.get("source_ip"),
            "destination_ip": packet_info.get("destination_ip"),
            "confidence": threat.get("confidence", 0.0),
            "details": threat,
        }
        self.logger.warning(json.dumps(alert))
        if threat["confidence"] > 0.8:
            self.logger.critical(f"High confidence threat detected: {json.dumps(alert)}")
            # TODO: Implement additional notification methods (e.g. email, Slack, SIEM integration)


