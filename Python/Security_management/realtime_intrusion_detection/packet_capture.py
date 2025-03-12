#!/usr/bin/env python3
# Adapted from: How to Build a Real-Time Intrusion Detection System with Python and Open-Source Libraries -> https://www.freecodecamp.org/news/build-a-real-time-intrusion-detection-system-with-python/
import queue
import threading
from collections import defaultdict
from scapy.all import sniff, IP, TCP


class PacketCapture:
    def __init__(self):
        self.packet_queue = queue.Queue()
        self.stop_capture = threading.Event()

    def packet_callback(self, packet):
        if (IP in packet) and (TCP in packet):
            self.packet_queue.put(packet)

    def start_capture(self, interface="eth0"):
        def capture_thread():
            sniff(
                iface=interface,
                prn=self.packet_callback,
                store=0,
                stop_filter=lambda _: self.stop_capture.is_set(),
            )

        self.capture_thread = threading.Thread(target=capture_thread)
        self.capture_thread.start()

    def stop(self):
        self.stop_capture.set()
        self.capture_thread.join()


class TrafficAnalyser:
    def __init__(self):
        self.connections = defaultdict(list)
        self.flow_stats = defaultdict(lambda: {
            "packet_count": 0,
            "byte_count": 0,
            "start_time": None,
            "last_time": None,
        })

    def analyse_packet(self, packet):
        if (IP in packet) and (TCP in packet):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            port_src = packet[TCP].sport
            port_dst = packet[TCP].dport

            flow_key = (ip_src, ip_dst, port_src, port_dst)
            
            # Update flow stats
            stats = self.flow_stats[flow_key]
            stats["packet_count"] += 1
            stats["byte_count"] += len(packet)
            current_time = packet.time

            if not stats["start_time"]:
                stats["start_time"] = current_time
            stats["last_time"] = current_time

    def extract_features(self, packet, stats):
        return {
            "packet_size": len(packet),
            "flow_duration": stats["last_time"] - stats["start_time"],
            "packet_rate": stats["packet_count"] / (stats["last_time"] - stats["start_time"]),
            "byte_rate": stats["byte_count"] / (stats["last_time"] - stats["start_time"]),
            "tcp_flags": packet[TCP].flags,
            "window_size": packet[TCP].window,
        }


