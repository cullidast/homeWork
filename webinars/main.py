from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/")

mdb = mongo['hsebank']
accounts = mdb['accounts']

while True:
    login = input("Введи логин: ")
    money = int(input("Введи сумму: "))
    if money >= 0:
        info = accounts.find_one({"_id": login})
        if info is None:
            accounts.insert_one({
                "_id": login,
                "money": money
            })
            continue
        else:
            info["money"] += money
            accounts.update_one({
                "_id": info["_id"]
            }, {
                "$set": info
            })
    else:
        info = accounts.find_one({"_id": login})
        if info is None:
            print("Пользователя не существует")
            continue
        else:
            if info["money"] >= abs(money):
                info["money"] -= abs(money)
                accounts.update_one({
                    "_id": info["_id"]
                }, {
                    "$set": info
                })
            else:
                print("Недостаточно денег на счету")
    print(f"У {login} на счету {info['money']}")




























# brew services start mongodb-community@7.0

from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017/")

mdb = mongo['hsebank']
accounts = mdb['accountstmp']

# account = {"_id": "Alex", "money": 0}
# result = accounts.insert_one(account)
# print(result.inserted_id)

info = accounts.find_one({"_id": "Alex"})
print("Вынул с такой инфой:")
print(info)

print("Увеличу на 100")
info["money"] += 100
accounts.update_one({
    "_id": info["_id"]
}, {
    "$set": info
})
print("Сохранил!")