import subprocess
import time

print("=" * 60)
print("🚀 ПРИВЕТ АЙНАРА - Запуск сервера")
print("=" * 60)

print("\n⏳ Запуск Django сервера...")
django_process = subprocess.Popen(
    ['python', 'manage.py', 'runserver', '127.0.0.1:8000']
)

time.sleep(3)

print("\n🌐 Создание туннеля LocalTunnel...")
print("⏳ Это может занять несколько секунд...\n")

try:
    subprocess.run(['lt', '--port', '8000', '--print-requests'])
except KeyboardInterrupt:
    print("\n\n✅ Сервер остановлен")
    django_process.terminate()
