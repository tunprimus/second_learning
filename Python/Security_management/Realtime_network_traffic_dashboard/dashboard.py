#!/usr/bin/env python3
# Adapted from: How to Build a Real-time Network Traffic Dashboard with Python and Streamlit -> https://www.freecodecamp.org/news/build-a-real-time-network-traffic-dashboard-with-python-and-streamlit/
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import socket
import streamlit as st
import threading
import time
import warnings
from collections import defaultdict
from datetime import datetime
from os.path import realpath as realpath
from scapy.all import *
from typing import Dict, List, Optional

pd.set_option("mode.copy_on_write", True)

RANDOM_SAMPLE_SIZE = 13

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Packet Processor

class PacketProcessor:
    """Process and analyse network packets"""

    def __init__(self):
        self.protocol_map = {
            1: "ICMP",
            6: "TCP",
            17: "UDP",
            53: "DNS",
            69: "TFTP",
            80: "HTTP",
            443: "HTTPS",
            8080: "HTTP",
        }
        self.packet_data = []
        self.start_time = datetime.now()
        self.packet_count = 0
        self.lock = threading.Lock()

    def get_protocol_name(self, protocol_num):
        """Convert protocol number to name"""
        return self.protocol_map.get(protocol_num, f"OTHER({protocol_num})")

    def process_packet(self, packet):
        """Process a single packet and extract relevant information"""
        try:
            if IP in packet:
                with self.lock:
                    packet_info = {
                        "timestamp": datetime.now(),
                        "source": packet[IP].src,
                        "destination": packet[IP].dst,
                        "protocol": self.get_protocol_name(packet[IP].proto),
                        "size": len(packet),
                        "time_relative": (datetime.now() - self.start_time).total_seconds(),
                    }
                    # Add TCP-specific information
                    if TCP in packet:
                        packet_info.update({
                            "src_port": packet[TCP].sport,
                            "dst_port": packet[TCP].dport,
                            "tcp_flags": packet[TCP].flags,
                        })
                    # Add UDP-specific information
                    elif UDP in packet:
                        packet_info.update({
                            "src_port": packet[UDP].sport,
                            "dst_port": packet[UDP].dport,
                        })
                    self.packet_data.append(packet_info)
                    self.packet_count += 1
                    # Keep only last 10000 packets to prevent memory issues
                    if len(self.packet_data) > 10_000:
                        self.packet_data.pop(0)
        except Exception as exc:
            logger.error(f"Error processing packet: {str(exc)}")

    def get_dataframe(self):
        """Convert packet data to pandas DataFrame"""
        with self.lock:
            return pd.DataFrame(self.packet_data)


# Function to Visualised Packet Data
def create_visualisation(df):
    """Create all dashboard visualisations"""
    if len(df) > 0:
        # Protocol distribution
        protocol_counts = df["protocol"].value_counts()
        fig_protocol = px.pie(values=protocol_counts.values, names=protocol_counts.index, title="Protocol Distribution")
        st.plotly_chart(fig_protocol, use_container_width=True)

        # Packets timeline
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df_grouped = df.groupby(df["timestamp"].dt.floor("S")).size()
        fig_timeline = px.line(x=df_grouped.index, y=df_grouped.values, title="Packets per Second")
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Top source IPs
        top_sources = df["source"].value_counts().head(RANDOM_SAMPLE_SIZE)
        fig_sources = px.bar(x=top_sources.index, y=top_sources.values, title="Top Source IP Addresses")
        st.plotly_chart(fig_sources, use_container_width=True)


# Function to Capture Network Data
def start_packet_capture():
    """Start packet capture in a separate thread"""
    processor = PacketProcessor()
    def capture_packets():
        sniff(prn=processor.process_packet, store=False)
    capture_thread = threading.Thread(target=capture_packets, daemon=True)
    capture_thread.start()
    return processor


# Main Function to Run Everything
def main():
    """Main function to run the dashboard"""
    st.set_page_config(page_title="Network Traffic Analysis", layout="wide")
    st.title("Real-time Network Traffic Analysis")
    # Initialise packet processor in session state
    if "processor" not in st.session_state:
        st.session_state.processor = start_packet_capture()
        st.session_state.start_time = time.time()
    # Create dashboard layout
    col01, col02 = st.columns(2)
    # Get current data
    df = st.session_state.processor.get_dataframe()
    # Display metrics
    with col01:
        st.metric("Total Packets:", len(df))
    with col02:
        duration = time.time() - st.session_state.start_time
        st.metric("Capture Duration:", f"{duration:.2f}s")
    # Display visualisation
    create_visualisation(df)
    # Display recent packets
    st.subheader("Recent Packets")
    if len(df) > 0:
        st.dataframe(df.tail(RANDOM_SAMPLE_SIZE)[["timestamp", "source", "destination", "protocol", "size"]], use_container_width=True)
    # Add refresh button
    if st.button("Refresh Data"):
        st.rerun()
    # Auto refresh
    time.sleep(2)
    st.rerun()


if __name__ == "__main__":
    main()

