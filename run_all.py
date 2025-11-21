import multiprocessing
import signal
import sys
from run_web import main as web_main
from run_worker import main as worker_main

def signal_handler(signum, frame):
    print("Отримано сигнал зупинки. Завершуємо процеси...")
    web_process.terminate()
    worker_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Запускаємо веб-сервер у окремому процесі
    web_process = multiprocessing.Process(target=web_main, daemon=True)
    web_process.start()

    # Запускаємо воркер у окремому процесі
    worker_process = multiprocessing.Process(target=worker_main, daemon=True)
    worker_process.start()

    # Чекаємо завершення (але оскільки нескінченні, це буде чекати Ctrl+C)
    web_process.join()
    worker_process.join()