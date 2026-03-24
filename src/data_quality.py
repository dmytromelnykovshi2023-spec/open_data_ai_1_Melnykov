import pandas as pd
import sys
import os

# Цей рядок дозволяє Python знайти сусідній файл load_data.py всередині папки src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_load import load_and_clean_real_estate_data


def check_missing_values(df):
    """Підраховує кількість та відсоток пропущених значень (NaN) у кожній колонці."""
    print("\n" + "=" * 40)
    print(" АНАЛІЗ ПРОПУЩЕНИХ ЗНАЧЕНЬ")
    print("=" * 40)

    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100

    # Створюємо зручну таблицю
    missing_df = pd.DataFrame({
        'Кількість пропусків': missing_count,
        'Відсоток (%)': missing_percent
    })

    # Фільтруємо лише ті колонки, де є пропуски, і сортуємо за спаданням
    missing_df = missing_df[missing_df['Кількість пропусків'] > 0].sort_values(by='Відсоток (%)', ascending=False)

    if missing_df.empty:
        print("Пропусків не знайдено! Дані ідеальні.")
    else:
        print(missing_df.round(2).to_string())


def check_duplicates(df):
    """Перевіряє наявність повних дублікатів рядків."""
    print("\n" + "=" * 40)
    print(" АНАЛІЗ ДУБЛІКАТІВ")
    print("=" * 40)

    duplicates = df.duplicated().sum()
    print(f"Знайдено повних дублікатів: {duplicates}")
    if duplicates > 0:
        print(f"Відсоток дублікатів: {(duplicates / len(df)) * 100:.2f}%")


def get_basic_statistics(df):
    """Виводить базову інформацію про датасет та типи колонок."""
    print("\n" + "=" * 40)
    print(" БАЗОВА СТАТИСТИКА ТА ТИПИ ДАНИХ")
    print("=" * 40)

    print(f"Загальна кількість записів: {df.shape[0]}")
    print(f"Загальна кількість колонок: {df.shape[1]}")
    print("\nТипи даних у колонках:")
    print(df.dtypes.value_counts())


if __name__ == "__main__":
    # Вказуємо шлях до файлу. Запускати скрипт треба з головної папки проєкту!
    DATA_PATH = "/Users/koristuvac/PycharmProjects/open_data_ai_1_Melnykov/src/vilniploshchi.xlsx"

    print("Запуск модуля перевірки якості даних...")
    df = load_and_clean_real_estate_data(DATA_PATH)

    if df is not None:
        get_basic_statistics(df)
        check_duplicates(df)
        check_missing_values(df)
    else:
        print("Не вдалося завантажити дані для аналізу.")