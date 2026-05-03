import os
import json
import pandas as pd
from sqlalchemy import create_engine


def research_data():
    print("Починаємо дослідження даних...")
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    try:
        df = pd.read_sql("SELECT * FROM real_estate_data", engine)

        # Обчислюємо базові статистики для всіх колонок
        # to_dict() перетворить таблицю статистик у словник для JSON
        stats = df.describe(include='all').fillna("NaN").to_dict()

        # Зберігаємо у спільну папку
        os.makedirs("/app/reports", exist_ok=True)
        with open("/app/reports/research_report.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)

        print("🎉 Звіт про дослідження збережено: /app/reports/research_report.json")
    except Exception as e:
        print(f"❌ Помилка: {e}")


if __name__ == "__main__":
    research_data()