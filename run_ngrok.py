import subprocess
import time
import os
from pyngrok import ngrok

os.chdir('c:\\Users\\ertai\\ONLINE_CINEMA')

# ВСТАВЬТЕ СЮДА ВАШ AUTHTOKEN
NGROK_AUTHTOKEN = '2nBvM4...'  # Замените на ваш токен

print("=" * 60)
print("🚀 ПРИВЕТ АЙНАРА - Запуск сервера")
print("=" * 60)

# Установить authtoken
if NGROK_AUTHTOKEN != '2nBvM4...':
    ngrok.set_auth_token(NGROK_AUTHTOKEN)
    print("✅ Authtoken установлен")

print("\n⏳ Запуск Django сервера на порту 8000...")
django_process = subprocess.Popen(
    ['python', 'manage.py', 'runserver', '127.0.0.1:8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)

try:
    # Создать туннель через Ngrok БЕЗ domain
    print("🌐 Создание туннеля Ngrok...")
    public_url = ngrok.connect(8000, "http", bind_tls=True)
    
    print("\n" + "=" * 60)
    print("✅ СЕРВЕР ЗАПУЩЕН И ДОСТУПЕН!")
    print("=" * 60)
    print(f"\n📱 Ссылка для друзей: {public_url}")
    print(f"💻 Локальный адрес: http://127.0.0.1:8000")
    print("\n⚠️  Ссылка действует пока работает этот скрипт")
    print("=" * 60)
    print("Нажмите Ctrl+C для остановки сервера")
    print("=" * 60 + "\n")
    
    # Сохраняем ссылку в файл
    with open('ngrok_link.txt', 'w', encoding='utf-8') as f:
        f.write(f"Ссылка для друзей: {public_url}\n")
        f.write(f"Локальный адрес: http://127.0.0.1:8000\n")
        f.write(f"Время создания: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("📄 Ссылка сохранена в ngrok_link.txt\n")
    
    # Держим сервер запущенным
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
    
except KeyboardInterrupt:
    print("\n\n❌ Остановка сервера...")
    ngrok.kill()
    django_process.terminate()
    print("✅ Сервер остановлен")
except Exception as e:
    print(f"\n❌ Ошибка: {str(e)}")
    print("\n💡 Решение: Используйте LocalTunnel вместо Ngrok")
    print("Выполните: python run_localtunnel.py")
    django_process.terminate()
