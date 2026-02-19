amount = int(input("Кол-во капсул: "))
capacity = int(input("Вместимость 1-ой упаковки: "))
package = amount // capacity
remainder = amount % capacity
print(f"--- Отчет фасовочного цеха ---\nПолных упаковок:\t {package}\nОстаток капсул:\t\t {remainder}")