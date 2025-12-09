import subprocess
import socket
import os

os.chdir('c:\\Users\\ertai\\ONLINE_CINEMA')

# Получить локальный IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print("=" * 60)
print("🚀 ПРИВЕТ АЙНАРА - Запуск сервера")
print("=" * 60)
print(f"\n⏳ Запуск Django сервера...")
print(f"\n💻 Локальный адрес: http://{local_ip}:8000")
print(f"   Или: http://127.0.0.1:8000")
print("\n📱 Ссылка для друзей в одной сети:")
print(f"   http://{local_ip}:8000")
print("\n" + "=" * 60)
print("Нажмите Ctrl+C для остановки сервера")
print("=" * 60 + "\n")

# Запустить Django на всех интерфейсах
subprocess.run(['python', 'manage.py', 'runserver', f'0.0.0.0:8000'])
