from web3 import Web3
from web3.middleware import geth_poa_middleware
from contratcinfo import abi, contract_adress
import re

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=contract_adress, abi=abi)

def auth():
    public_key = input('Введите публичный ключ: ')
    password = input('Введите пароль: ')
    try:
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        return None
def checkpassword(password):
    if(len(password)<12):
        return False
    if not any(char.isupper() for char in password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву."
    if not any (char.islover() for char in password):
        return False,  "Пароль должен содержать хотя бы одну цифру."
    if not re.search("[!@#$%^&*]", password):
        return False, "Пароль должен содержать хотя бы один специальный символ: !, @, #, $, %, ^, & или *."
    if "password" in password.lower() or "123" in password:
        return False, "Пароль не должен содержать простых шаблонов, таких как 'password' или '123'."

    return True, "Пароль удовлетворяет всем условиям сложности."
    
def register():
    password = input('Введите пароль: ')
    if (checkpassword(password)):
        address = w3.geth.personal.new_account(password)
        print(f"Ваш адрес: {address}")
    
    

def sendEth(account):
    try:
        value = int(input("Введите сумму для перевода на контракт: "))
        tx_hash = contract.functions.sendEth().transact({
        'from': account,
        'value': value,
        })
        print(f"Транзакция отправлена: {tx_hash.hex()}")

    except Exception as e:
        print(f"Ошибка при отправке средств: {e}")

def getBalance(account):
    try:
        balance = contract.functions.getBalance().call({
            'from': account,
        })
        print(f"Ваш баланс на смарт-контракте: {balance} wei")
    except Exception as e:
        print(f"Ошибка при просмотре баланса: {e}")

def  withDraw(account):
    try:
        to = input("Введите адрес аккаунта: ")
        amount = int(input("Введите сумму для перевода на контракт: "))
        tx_hash= contract.functions.withdrawll(to,amount).transact({
            'from': account,
        })
        print(f"Транзакция отправлена: {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка при выводе средств: {e}")

def createEstate(account):
    try:
        square = int(input("Введите площадь недвижемости: "))
        rooms = int(input("Введите количество комнат: "))
        esType = int(input("1.House\n2.Apartments\n3.Fist\n4.Loft"))
        contract.functions.createEstate(square, rooms, esType).transact({"from": account})
        print(F"Недвижемость добавлена")
    except Exception as e:
        print(f"Ошибка: {e}")

def UpdatedStatusEstate(account):
    try:
        id_estate = int(input("Введите id вашей недвижемости: "))
        statusEstate = bool(input("Введите статус недвижемости\nTrue-открыто.\n3.False-закрыто.\n"))
        data = int(input("Введите дату: "))
        contract.UpdatedStatusEstate(id_estate, statusEstate, data)
    except Exception as e:
        print(f"Ошибка: {e}")

def createAd(account):
    try:
        id_estate = int(input("Введите id недвижемости: "))
        price = int(input("Введите сумму: "))
        contract.createAd(id_estate, price).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")

def UpdatedStatusAd(account):
    try:
        id_estate = int(input("Введите id вашей недвижемости: "))
        statusEstate = bool(input("Введите статус недвижемости\nTrue-открыто.\n3.False-закрыто.\n"))
        data = int(input("Введите дату: "))
    except Exception as e:
        print(f"Ошибка as {e}")
def buyEstate(account):
    try:
        value = int(input("Введите сумму: "))
        id = int(input("Введите id недвижемости: "))
        contract.buyEstate(value, id)
    except Exception as e:
        print(f"Ошибка: {e}")
def getEstates():
    estates = contract.functions.getEstates().call()
    for estate in estates:
        print(f"ID: {estate[0]}, Площадь: {estate[1]}, Комнаты: {estate[2]}, Тип: {estate[3]}")
    return estates

def getAds():
    ads = contract.functions.getAds().call()
    for ad in ads:
        print(f"ID: {ad[0]}, ID недвижимости: {ad[1]}, Цена: {ad[2]}, Статус: {'Открыто' if ad[3] == 0 else 'Закрыто'}")
    return ads

def main():
    account = ""
    is_auth = False
    while True:
        if not is_auth:
            choise = input("Выберете:\n1. Авторизация\n2. Регистрация\n")
            match choise:
                case "1":
                    account = auth()
                    if account != None and account != "":
                        is_auth = True
                case "2":
                    register()
                case _:
                    print("Введите корректную команду!")
        elif is_auth:
            choise = input("Выберете:\n1. Отправить эфир\n2. Посмотреть баланс контракта\n3. Вывести средства\n4. Посмотреть баланс аккаунта.\n7.Создать недвижемость.\n8.Изменить обьявления\n9.Купить недвижемость.\n10.Все обьявления\n11.Все недвижемости\n12. Выйти из сис")
            match choise:
                case "1":
                    sendEth(account)
                case "2":
                    getBalance(account)
                case "3":
                    withDraw(account)
                case "4":
                    print(f"Баланс аккаунта : {w3.eth.get_balance(account)}")
                case "12":
                    is_auth = False
                case "5":
                    createEstate(account)
                case "6":
                    createAd(account)
                case "7":
                    UpdatedStatusEstate(account)
                case "8":
                    UpdatedStatusAd(account)
                case "9":
                    buyEstate(account)
                case "10":
                    getAds()
                case "11":
                    getEstates()
                case _:
                    print("Введите корректную команду")

  
a =main()