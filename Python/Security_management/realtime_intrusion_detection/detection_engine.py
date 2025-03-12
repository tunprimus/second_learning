#!/usr/bin/env python3
# Adapted from: How to Build a Real-Time Intrusion Detection System with Python and Open-Source Libraries -> https://www.freecodecamp.org/news/build-a-real-time-intrusion-detection-system-with-python/
import numpy as np
from sklearn.ensemble import IsolationForest

# Monkey patching NumPy >= 1.24 in order to successfully import model from sklearn and other libraries
np.float = np.float64
np.int = np.int_
np.object = np.object_
np.bool = np.bool_


class DetectionEngine:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.signature_rules = self.load_signature_rules()
        self.training_data = []

    def load_signature_rules(self):
        return {
            "syn_flood": {
                "condition": lambda features: (features["tcp_flags"] == 2 and features["packet_rate"] > 100),
                },
            "port_scan": {
                "condition": lambda features: (features["packet_size"] < 100 and features["packet_rate"] > 50),
                },
        }

    def train_anomaly_detector(self, normal_traffic_data):
        self.anomaly_detector.fit(normal_traffic_data)

    def detect_threats(self, features):
        threats = []

        # Signature based detection
        for rule_name, rule in self.signature_rules.items():
            if rule["condition"](features):
                threats.append({
                    "type": "signature",
                    "rule": rule_name,
                    "confidence": 1.0,
                })

        # Anomaly detection
        feature_vector = np.array([[
            features["packet_size"],
            features["packet_rate"],
            features["byte_rate"]
        ]])
        anomaly_score = self.anomaly_detector.score_samples(feature_vector)[0]
        if anomaly_score < -0.5:
            threats.append({
                "type": "anomaly",
                "score": anomaly_score,
                "confidence": min(1.0, abs(anomaly_score)),
            })
        return threats
