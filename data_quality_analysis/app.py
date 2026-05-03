import os
import json
import pandas as pd
from sqlalchemy import create_engine


def analyze_quality():
    print("Починаємо аналіз якості даних...")

    # Підключаємось до БД
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    try:
        # Зчитуємо дані з таблиці, яку створив твій перший модуль!
        df = pd.read_sql("SELECT * FROM real_estate_data", engine)
        print(f"✅ Зчитано {len(df)} рядків з бази даних.")

        # Виконуємо перевірки якості
        total_rows = len(df)
        duplicates = int(df.duplicated().sum())
        missing_values = df.isnull().sum().to_dict()  # Рахуємо пропуски по кожній колонці

        # Формуємо звіт (словник)
        report = {
            "total_rows": total_rows,
            "duplicates": duplicates,
            "missing_values": missing_values
        }

        # Зберігаємо звіт у спільну папку /app/reports
        os.makedirs("/app/reports", exist_ok=True)
        with open("/app/reports/quality_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=4)

        print("🎉 Звіт про якість успішно збережено у файл: /app/reports/quality_report.json")

    except Exception as e:
        print(f"❌ Помилка під час аналізу: {e}")


if __name__ == "__main__":
    analyze_quality()