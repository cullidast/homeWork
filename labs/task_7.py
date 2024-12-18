import csv

def read_csv(file_path):
    """Чтение данных из CSV-файла."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def transform_data(data):
    """Преобразование данных (если требуется)."""
    # В данном случае преобразования могут не понадобиться,
    # но функция оставлена для модификаций.
    return data

def generate_description(row):
    """Генерация текстового описания покупателя."""
    sex_translation = {"female": "женского пола", "male": "мужского пола"}
    device_translation = {
        "mobile": "мобильного",
        "tablet": "планшетного",
        "laptop": "ноутбука",
        "desktop": "стационарного компьютера"
    }

    sex = sex_translation.get(row["sex"], row["sex"])
    device = device_translation.get(row["device_type"], row["device_type"])
    return (
        f"Пользователь {row['name']} {sex}, {row['age']} лет "
        f"совершил(а) покупку на {row['bill']} у.е. с {device} "
        f"браузера {row['browser']}. Регион, из которого совершалась покупка: {row['region']}."
    )

def write_to_txt(file_path, descriptions):
    """Запись описаний в TXT-файл."""
    with open(file_path, mode='w', encoding='utf-8') as file:
        for description in descriptions:
            file.write(description + "\n")

def main(input_csv, output_txt):
    """Основной процесс программы."""
    data = read_csv(input_csv)
    data = transform_data(data)
    descriptions = [generate_description(row) for row in data]
    write_to_txt(output_txt, descriptions)

# Пример запуска
if __name__ == "__main__":
    input_csv = "web_clients_correct.csv"  # Путь к входному файлу
    output_txt = "descriptions.txt"  # Путь к выходному файлу
    main(input_csv, output_txt)
