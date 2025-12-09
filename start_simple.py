import subprocess
import socket
import sys

def get_ip():
    """Получить локальный IP адрес"""
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
print("🎬 ПРИВЕТ АЙНАРА - Запуск сервера")
print("=" * 70)
print(f"\n✅ Сервер запущен!")
print(f"\n💻 Локальный адрес: http://127.0.0.1:8000")
print(f"📱 Адрес в сети: http://{ip}:8000")
print(f"\n📌 Отправьте друзьям в одной сети: http://{ip}:8000")
print("\n" + "=" * 70)
print("Нажмите Ctrl+C для остановки")
print("=" * 70 + "\n")

subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
