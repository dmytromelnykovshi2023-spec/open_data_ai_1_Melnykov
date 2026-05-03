import os
import time
import pandas as pd
from sqlalchemy import create_engine
from prometheus_client import start_http_server, Gauge

# Створюємо метрику: "Датчик", який показуватиме кількість завантажених рядків
ROWS_PROCESSED = Gauge('real_estate_rows_processed_total', 'Number of real estate rows successfully saved to DB')


def load_and_clean_real_estate_data(file_path):
    print(f"Розкриваємо маскування: завантажуємо як справжній Excel з {file_path}...")
    try:
        # Читаємо файл як Excel
        df = pd.read_excel(file_path, header=1)

        # Перевіряємо, чи знайшлася наша колонка
        if 'Район' not in df.columns:
            print(f"❌ Колонку 'Район' не знайдено. Ось що є: {df.columns.tolist()}")
            return None

        # Викидаємо порожні рядки і чистимо текст від пробілів
        df = df.dropna(subset=['Район'])
        df['Район'] = df['Район'].astype(str).str.strip()

        print(f"✅ Успішно зчитано {len(df)} приміщень з файлу.")
        return df

    except Exception as e:
        print(f"❌ Критична помилка при завантаженні: {e}")
        return None


if __name__ == "__main__":
    # 1. ЗАПУСКАЄМО СЕРВЕР МЕТРИК НА ПОРТУ 8000
    print("Запуск Prometheus metrics server на порту 8000...")
    start_http_server(8000)

    # Робимо паузу 5 секунд, щоб PostgreSQL встиг повністю запуститися
    print("Очікування готовності бази даних...")
    time.sleep(5)

    # Шлях до файлу всередині Docker-контейнера!
    DATA_PATH = "/app/data/vilniploshchi.xlsx"

    # Запуск функції очищення
    df_cleaned = load_and_clean_real_estate_data(DATA_PATH)

    if df_cleaned is not None:
        # ВИМОГА ЛАБИ: Завантаження даних у базу PostgreSQL
        try:
            print("Підключаємось до бази даних...")
            db_url = os.getenv("DATABASE_URL")
            engine = create_engine(db_url)

            table_name = "real_estate_data"

            # Зберігаємо DataFrame у таблицю
            df_cleaned.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"🎉 ДАНІ УСПІШНО ЗБЕРЕЖЕНО В БАЗУ ДАНИХ (таблиця '{table_name}')!")

            # 2. ОНОВЛЮЄМО МЕТРИКУ ДЛЯ PROMETHEUS
            ROWS_PROCESSED.set(len(df_cleaned))

        except Exception as e:
            print(f"❌ Помилка при записі в БД: {e}")

            # 3. НЕ ДАЄМО СКРИПТУ ВИМКНУТИСЯ
    # Щоб Prometheus міг постійно збирати метрики, контейнер має працювати постійно
    print("ETL процес завершено. Сервіс залишається активним для збору метрик...")
    while True:
        time.sleep(60)