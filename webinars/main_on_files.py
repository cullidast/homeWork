# key - login, value - total money
import json
import os

data = {}
if os.path.isfile("dump.txt"):
    with open("dump.txt", "r") as fin:
        line = fin.readline().strip()
        data = json.loads(line)


while True:
    login = input("Введи логин: ")
    money = int(input("Введи сумму: "))
    if money >= 0:
        if login not in data:
            data[login] = money
        else:
            data[login] += money
    else:
        if login not in data:
            print("Пользователя не существует")
            continue
        else:
            if data[login] >= abs(money):
                data[login] -= abs(money)
            else:
                print("Недостаточно денег на счету")
                continue
    print(f"У {login} на счету {data[login]}")
    with open("dump.txt", 'w') as fout:
        data_str = json.dumps(data) # словарь -> текст
        fout.write(data_str)

