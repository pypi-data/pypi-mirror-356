from setuptools import setup, find_packages

setup(
    name="packet_capture_module",
    version="0.1.0",
    description="Multicast DPI Packet Capture Module",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "pyshark>=0.6.0",
        "scapy>=2.5.0",
        "python-libpcap>=0.3.0",
        "dpkt>=1.9.8",
        "python-pytun>=2.4.1",
        "grpcio>=1.51.1",
        "protobuf>=4.21.12",
        "redis>=4.5.4",
        "pybpf>=0.3.0",
        "PyYAML>=6.0",
        "asyncio>=3.4.3",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.10",
)