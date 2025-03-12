#!/usr/bin/env python3
# Adapted from: How to Build a Real-Time Intrusion Detection System with Python and Open-Source Libraries -> https://www.freecodecamp.org/news/build-a-real-time-intrusion-detection-system-with-python/
import queue
from packet_capture import PacketCapture, TrafficAnalyser
from detection_engine import DetectionEngine
from alert_system import AlertSystem

class IntrusionDetectionSystem:
    def __init__(self, interface="eth0"):
        self.packet_capture = PacketCapture()
        self.traffic_analyser = TrafficAnalyser()
        self.detection_engine = DetectionEngine()
        self.alert_system = AlertSystem()
        self.interface = interface

    def start(self):
        print(f"Starting IDS on interface {self.interface}")
        self.packet_capture.start_capture(self.interface)

        while True:
            try:
                packet = self.packet_capture.packet_queue.get(timeout=1)
                features = self.traffic_analyser.analyse_packet(packet)
                if features:
                    threats = self.detection_engine.detect_threats(features)
                    for threat in threats:
                        packet_info = {
                            "source_ip": packet[IP].src,
                            "destination_ip": packet[IP].dst,
                            "source_port": packet[TCP].sport,
                            "destination_port": packet[TCP].dport,
                        }
                        self.alert_system.generate_alert(threat, packet_info)
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                print("Stopping IDS...")
                self.packet_capture.stop()
                break

if __name__ == "__main__":
    ids = IntrusionDetectionSystem()
    ids.start()

