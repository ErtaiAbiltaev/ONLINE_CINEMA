import subprocess
import time
import sys
import os

print("=" * 80)
print("🎬 ПРИВЕТ АЙНАРА - ЗАПУСК СЕРВЕРА ДЛЯ ИНТЕРНЕТА")
print("=" * 80)

print("\n⏳ Запуск Django сервера...\n")

# Запуск Django в фоне
django_process = subprocess.Popen(
    [sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000']
)

time.sleep(4)

print("✅ Django запущен на http://127.0.0.1:8000")
print("\n" + "=" * 80)
print("🌐 ЗАПУСК ПУБЛИЧНОГО ТУННЕЛЯ ДЛЯ ИНТЕРНЕТА")
print("=" * 80)
print("\n⏳ Генерируем публичную ссылку...\n")
print("💡 Вскоре появится ссылка вида: https://xxx.loca.lt\n")

try:
    # Используем powershell для запуска lt
    subprocess.run(['powershell', '-Command', 'lt --port 8000'])
except KeyboardInterrupt:
    print("\n\n❌ Остановка сервера...")
    django_process.terminate()
    print("✅ Сервер остановлен")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\n💡 Альтернатива: откройте новый PowerShell и выполните:")
    print("   lt --port 8000")
    django_process.terminate()
