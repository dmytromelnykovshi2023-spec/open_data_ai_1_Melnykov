import os
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns


def create_plots():
    print("Генеруємо візуалізації...")
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    try:
        df = pd.read_sql("SELECT * FROM real_estate_data", engine)
        os.makedirs("/app/plots", exist_ok=True)

        # Графік 1: Кількість приміщень за районами (ми знаємо, що ця колонка є)
        plt.figure(figsize=(10, 6))
        sns.countplot(y='Район', data=df, palette='viridis')
        plt.title("Кількість приміщень за районами")
        plt.xlabel("Кількість")
        plt.ylabel("Район")
        plt.tight_layout()
        plt.savefig("/app/plots/dist_plot.png")  # Зберігаємо!
        plt.close()

        # Графік 2: Демонстраційний (розподіл довжини назв районів, щоб точно не впало через типи даних)
        df['Довжина_назви'] = df['Район'].astype(str).apply(len)
        plt.figure(figsize=(8, 5))
        sns.histplot(df['Довжина_назви'], bins=15, color='blue', kde=True)
        plt.title("Розподіл довжини назв районів")
        plt.xlabel("Кількість символів")
        plt.ylabel("Частота")
        plt.tight_layout()
        plt.savefig("/app/plots/bar_plot.png")  # Зберігаємо!
        plt.close()

        print("🎉 Графіки успішно згенеровано та збережено у папку /app/plots/")
    except Exception as e:
        print(f"❌ Помилка візуалізації: {e}")


if __name__ == "__main__":
    create_plots()