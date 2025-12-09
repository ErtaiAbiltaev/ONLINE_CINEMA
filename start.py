import subprocess
import time
import sys

print("=" * 70)
print("🎬 ПРИВЕТ АЙНАРА - Запуск сервера")
print("=" * 70)

# Запуск Django
print("\n⏳ Запуск Django сервера на порту 8000...")
django = subprocess.Popen([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

time.sleep(3)

# Запуск Ngrok
print("🌐 Запуск Ngrok туннеля...\n")
try:
    subprocess.run(['ngrok', 'http', '8000', '--log=stdout'])
except FileNotFoundError:
    print("❌ Ngrok не установлен!")
    print("Установите: ngrok config add-authtoken YOUR_TOKEN")
    django.terminate()
except KeyboardInterrupt:
    print("\n\n✅ Сервер остановлен")
    django.terminate()
