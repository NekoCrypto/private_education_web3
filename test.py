'''


def add(a, b):
    return a + b

# Получить доступ к атрибуту __code__
code_obj = add.__code__

# Вывести некоторую информацию о объекте кода
print("Код: ", code_obj.co_code.hex())
print("Константы: ", code_obj.co_consts)
print("Переменные: ", code_obj.co_varnames)


date = {'year': 2023, 'day': 20, 'month': 'December'}
print(date.get('year'))
print(date.get('day'))
print(date.get('month'))
print(date['year'], date['day'], date['month'])
print(date.keys())
print(date.items())
print(date.values())

# value in dict.values()
# key in dict

x = 5
print(f'lalalal') if x < 3 else print(f'gogogogo')
range_it = range(0, 5, 2)
print(range_it)
range_it = list(range(0, 5, 2))
print(range_it)
range_it = list(reversed([0, 5, 2]))
print(range_it)
print(type(range_it))

def min(*args):
    res = float('inf')
    for arg in args:
        if arg < res:
            res = arg
        return print(res)


def unique(iterable, seen=None):
    seen = set(seen or [])
    acc = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            acc.append(item)
    return print(acc)


xs = [1, 1, 22, 22, 5, 4, 7]


addr, key = '0x123456', 'acd123'
print(addr)
print(key)

first, *rest, last = range(1, 6)
print(first)
print(rest)
print(last)

# import dis
# dis.dis("first, *rest, last = range(1, 6)")


defaults = {'host': '0.0.0.0', 'port': 8080}
defaults = {**defaults, 'port': 80}
print(defaults)
min = 42
print(globals())
'''


print(30 // 1.5)

minimum = 42


def f():
    global minimum
    minimum += 1
    return minimum


print(f())



'''

Function: SettleAggregateOrder(tuple order,bytes takerSig,tuple[] makerSigs)
0123456789012345678901234567890123456789012345678901234567891234
0x1c2415332559df9e8172ea90efb1030b288b3f6b534511b364b4ec7d70e5f65ed475fd5757eb89a0dac3885d0a96d09839de77f7704f7c1b11bddb74755dc73987
0x1b2c3c5c46fe3f2518658f3945137d192c88f7e8407a2d36833071c7db30e876b3696953b3b508bb0c82ec9de7bd0e4b9c86b77b289c3500a2bb7f3674c69f58ca


takerSig
0123456789012345678901234567890123456789012345678901234567891234
0xe696ae54cc382ee11e906e0f557d9f14c04eae61550e0538ef01d64c5ebedc4d19a9afbec056c5390845404bcb083526606fdc02709c19c41c2bd5e61b5d07621c
0x963470acec78e526dbec70333aea3aadcf75c2877a732761aedd0c295c93f56427bb63b7716609ca002607e34b9dfa09c87b42917a5257d394653b62287ad1331c
'''
