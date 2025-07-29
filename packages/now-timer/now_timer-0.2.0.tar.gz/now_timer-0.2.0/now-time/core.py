from colorama import Fore, Style
from datetime import datetime
import time

sekarang = datetime.now()
tanggal = sekarang.date()
waktu = sekarang.time()

def time_now_seconds():
  while True:    
     print(f"{Fore.CYAN}Now time in\n seconds:", time.strftime('%S'))
     time.sleep(1)

def time_now_month():
  while True:   
     print(f"{Fore.RED}Now time in\n month:", time.strftime('%m'))
     time.sleep(2592000)  # 30 days        

def time_now_minutes():
   while True:
     print(f"{Fore.YELLOW}Now time in\n minutes:", time.strftime('%M'))
     time.sleep(60)

def time_now_hours():
    while True:
     print(f"{Fore.GREEN}Now time in\n hours:", time.strftime('%H'))
     time.sleep(3600)

def time_now_date():
    while True:
        print(f"{Fore.BLUE}Now date in\n date:", time.strftime('%d'))
        time.sleep(86400)

def time_now_year():
    while True:
        print(f"{Fore.MAGENTA}Now year in\n year:", time.strftime('%Y'))
        time.sleep(31536000)  # 365 days



      


