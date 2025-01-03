# Шаг 1: Инициализация списка документов
documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

# Шаг 2: Функция для поиска документа по номеру с отладочными выводами
def find_document_by_number(doc_number):
        for doc in documents:
        print(f"Проверка документа с номером: {doc['number']}")
        if doc['number'] == doc_number:
            print("Совпадение найдено!")
            return doc
    print("Совпадение не найдено.")
    return None

# Шаг 3: Взаимодействие с пользователем
while True:
    search_number = input("Введите номер документа для поиска (или 'q' для выхода): ").strip()
    
    if search_number.lower() == 'q':
        print("Выход из программы.")
        break
    
    found_doc = find_document_by_number(search_number)
    
    if found_doc:
        print(f"\nДокумент найден: {found_doc}\n")
    else:
        print("\nДокумент с таким номером не найден.\n")
