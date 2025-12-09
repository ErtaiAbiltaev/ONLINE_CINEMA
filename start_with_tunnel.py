import subprocess
import time
import sys
import socket

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

ip = get_ip()

print("=" * 70)
print("🎬 ПРИВЕТ АЙНАРА - Запуск сервера с туннелем")
print("=" * 70)

# Запуск Django
print("\n⏳ Запуск Django сервера...")
django = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

time.sleep(3)

print("✅ Django запущен на http://127.0.0.1:8000")
print(f"✅ LocalHost в сети: http://{ip}:8000")

# Запуск LocalTunnel
print("\n🌐 Запуск LocalTunnel...")
print("⏳ Ожидание публичной ссылки...\n")

try:
    subprocess.run(['lt', '--port', '8000'])
except FileNotFoundError:
    print("❌ LocalTunnel не установлен!")
    print("Установите: npm install -g localtunnel")
    django.terminate()
except KeyboardInterrupt:
    print("\n\n✅ Сервер остановлен")
    django.terminate()
