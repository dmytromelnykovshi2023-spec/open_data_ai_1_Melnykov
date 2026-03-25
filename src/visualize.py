import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Підключаємо твій скрипт завантаження даних
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_load import load_and_clean_real_estate_data


def plot_properties_by_district(df):
    """Будує графік кількості приміщень за районами та зберігає його."""
    print("Аналізуємо райони та будуємо графік...")

    # Додаємо цей рядок, щоб побачити всі колонки:
    print("Ось які колонки бачить Python:", df.columns.tolist())

    # Створюємо графік заданого розміру
    plt.figure(figsize=(12, 6))

    # Шукаємо колонку 'Район' (враховуємо, що у нас був складний заголовок з 2 рівнів)
    district_col = [col for col in df.columns if 'Район' in str(col)]

    if district_col:
        col_name = district_col[0]
        # Рахуємо кількість приміщень у кожному районі
        district_counts = df[col_name].value_counts()

        # Малюємо стовпчики
        sns.barplot(x=district_counts.index, y=district_counts.values, palette="viridis")

        # Наводимо красу: додаємо підписи
        plt.title('Кількість вільних приміщень за районами', fontsize=16, fontweight='bold')
        plt.xlabel('Район', fontsize=12)
        plt.ylabel('Кількість приміщень', fontsize=12)
        plt.xticks(rotation=45, ha='right')  # Повертаємо назви районів, щоб вони не злипалися
        plt.tight_layout()

        # Створюємо папку для збереження картинок (якщо її ще немає)
        os.makedirs('reports/figures', exist_ok=True)

        # Зберігаємо результат
        save_path = 'reports/figures/districts_count.png'
        plt.savefig(save_path, dpi=300)
        print(f"✅ Графік успішно збережено у файл: {save_path}")

        # Показуємо графік на екрані
        plt.show()
    else:
        print("❌ Помилка: Колонку 'Район' не знайдено.")


if __name__ == "__main__":
    DATA_PATH = "/Users/koristuvac/PycharmProjects/open_data_ai_1_Melnykov/src/vilniploshchi.xlsx"

    df = load_and_clean_real_estate_data(DATA_PATH)

    if df is not None:
        # Вмикаємо красивий стиль для графіків
        sns.set_theme(style="whitegrid")
        plot_properties_by_district(df)