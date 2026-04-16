import pandas as pd
import os


def load_and_clean_real_estate_data(file_path):
    print("Розкриваємо маскування: завантажуємо як справжній Excel...")
    try:
        # Читаємо файл саме як Excel!
        df = pd.read_excel(
            file_path,
            header=1  # Кажемо, що нормальні заголовки лежать у другому рядку
        )

        # Перевіряємо, чи знайшлася наша колонка
        if 'Район' not in df.columns:
            print(f"❌ Колонку 'Район' не знайдено. Ось що є: {df.columns.tolist()}")
            return None

        # Викидаємо порожні рядки і чистимо текст від пробілів
        df = df.dropna(subset=['Район'])
        df['Район'] = df['Район'].astype(str).str.strip()

        print(f"✅ Успішно завантажено {len(df)} приміщень для графіка.")
        return df

    except Exception as e:
        print(f"❌ Критична помилка при завантаженні: {e}")
        return None

    try:
        # header=[1, 2] каже pandas, що заголовки знаходяться на 2-му і 3-му рядках
        # (індексація починається з нуля). 1-й рядок з датою автоматично проігнорується.
        df = pd.read_csv(
            file_path,
            header=1,
            sep=';',
            encoding='cp1251',
            encoding_errors='replace',
            on_bad_lines='skip'
        )

        # Об'єднання дворівневих заголовків в один зручний рядок
        # Наприклад: "Вільні приміщення_Загальна площа об'єкта"
        new_columns = []
        for col in df.columns:
            # Якщо другого рівня немає (в pandas це маркується як 'Unnamed'), беремо тільки перший
            if 'Unnamed' in str(col[1]):
                new_columns.append(str(col[0]).strip())
            else:
                new_columns.append(f"{str(col[0]).strip()}_{str(col[1]).strip()}")

        df.columns = new_columns

        print(f"Успішно завантажено {df.shape[0]} записів та {df.shape[1]} колонок.")
        return df

    except Exception as e:
        print(f"Критична помилка при завантаженні: {e}")
        return None


if __name__ == "__main__":
    # Вкажи відносний шлях до файлу.
    # Припускаємо, що ти запускаєш скрипт з головної папки проєкту.
    DATA_PATH = "data/raw/vilniploshchi.xlsx - Sheet.csv"

    # Запуск функції
    df_cleaned = load_and_clean_real_estate_data(DATA_PATH)

    if df_cleaned is not None:
        # Виводимо перші 5 колонок, щоб переконатися, що заголовки склеїлися правильно
        print("\nОтримані колонки (перші 10):")
        for i, col in enumerate(list(df_cleaned.columns)[:10], 1):
            print(f"{i}. {col}")