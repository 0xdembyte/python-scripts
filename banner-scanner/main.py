# Developer: Demarjio Brady
# Developed on: 03/06/2025 at 12:59pm
# Description: This Python script takes 4 inputs (target host, start port range, end port range, and threads amount) 
#              And scans the target host between the starting and ending port for each port it recieves data in 1024 bytes checking if it returns a banner and outputs the result
# Imports
from sys import exit
from concurrent.futures import ThreadPoolExecutor
from time import time
import socket

# Get the target host
target_host = input("Enter the host you want to target (e.g. google.com or 192.168.1.1): ")

# Check if the target host is empty
if target_host == "":
    exit("Target host can't be empty")

# Get the port range
start_port_range = input("Enter the start port range you want to scan (e.g. 1): ")
end_port_range   = input("Enter the end port range you want to scan (e.g. 1024): ")

# Get how many threads the user wants to use
threads_amount   = input("Enter the amount of threads you want to use (e.g. 100): ")

# Check if the port range contains digits only
if not start_port_range.isdigit() or not end_port_range.isdigit():
    exit("Port range must contain digits only.")

# Check if the threads amount contains digits only
if not threads_amount.isdigit():
    exit("Threads amount must contain digits only.")

# Convert the strings to intergers
start_port_range = int(start_port_range)
end_port_range   = int(end_port_range)
threads_amount   = int(threads_amount)

# Store the start time
start_time = time()

# Functions
# ANSI colour codes used for text formatting:
# 31 - Red
# 32 - Green
# 33 - Yellow
# 36 - Cyan
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def output_log(text, color_code):
    print(color_text(text, color_code))

def scan_banner(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as web_socket:
        # Set a timeout
        web_socket.settimeout(1.0)

        # Get the web socket response
        response = web_socket.connect_ex((target_host, port))

        # Check if the response returned successfully or not
        if response == 0:
            # Add a try block to prevent timeout errors
            try:
                # Get the incoming data of 1024 bytes or below
                # Then decode it and clean it up
                # 1024 is a standard buffer size
                banner = web_socket.recv(1024).decode().strip()
            except socket.timeout:
                # Set the banner to an empty string
                banner = ""

            if banner != "":
                return color_text(f"[Port {port}] Banner: {banner}", "32")
            else:
                return color_text(f"[Port {port}] Banner: No banner recieved", "33")
        else:
            return color_text(f"[Port {port}] is closed or filtered.", "31")

# Output that we're scanning with the basic details
output_log(f"Scanning {target_host} from port {start_port_range} to {end_port_range} with {threads_amount} threads...", "36")

# Open multithreading with the user defined threads amount
with ThreadPoolExecutor(max_workers=threads_amount) as executor:
    futures = {executor.submit(scan_banner, port): port for port in range(start_port_range, end_port_range + 1)}

# Print the result of each thread
for future in futures:
    print(future.result())

# Store the end time
end_time = time()

# Output how long it took for the scan to complete
output_log(f"Scan completed in {end_time - start_time:.2f} seconds", 36)
