# cursofiap/core.py
def hello_world():
    return "Hello, world!"

# Exercicio 1 - Imprima seu nome e idade
def exercicio_1():
    nome = input('Digite seu nome: ')
    idade = input('Digite sua idade: ')
    print(f'Olá, {nome}! Você tem {idade} anos.')

# Exercicio 2 - Soma de dois números
def exercicio_2():
    num1 = 5
    num2 = 7
    def soma(a, b):
        return a + b
    print(f'A soma de {num1} + {num2} = {soma(num1, num2)}')

# Exercicio 3 - Verifique se o número é par ou ímpar
def exercicio_3():
    numero = float(input('Digite um numero: '))
    resto = numero % 2
    if resto == 0:
        print(f'O numero {numero} é par')
    else:
        print(f'O numero {numero} é impar')

# Exercicio 4 - Calculadora simples
def exercicio_4():
    num1 = int(input('Digite o primeiro numero: '))
    num2 = int(input('Digite o segundo numero: '))
    operador = input("Digite o operador (+, -, *, /): ")
    if operador == "+":
        resultado = num1 + num2
        print(f"{num1} + {num2} = {resultado}")
    elif operador == "-":
        resultado = num1 - num2
        print(f"{num1} - {num2} = {resultado}")
    elif operador == "*":
        resultado = num1 * num2
        print(f"{num1} * {num2} = {resultado}")
    elif operador == "/":
        if num2 != 0:
            resultado = num1 / num2
            print(f"{num1} / {num2} = {resultado}")
        else:
            print("Erro: divisão por zero não é permitida.")
    else:
        print("Operador inválido.")

# Exercicio 5 - Tabuada
def exercicio_5(tabNum):
    print(f'Tabuada do {tabNum}')
    for i in range(1, 11):
        print(f'{tabNum} X {i} = {tabNum * i}')

# Exercicio 6 - Lista de compras
def exercicio_6():
    items = ['m&ms', 'milka', 'coca-zero']
    for i in items:
        print(i)

# Exercicio 7 - Média de notas
def exercicio_7():
    num1 = int(input('Digite a primeira nota: '))
    num2 = int(input('Digite a segunda nota: '))
    num3 = int(input('Digite a terceira nota: '))
    media = (num1 + num2 + num3) / 3
    print(f'A média final é {media}')

# Exercicio 8 - Número maior
def exercicio_8():
    num1 = int(input('Digite o primeiro numero: '))
    num2 = int(input('Digite o segundo numero: '))
    if num1 > num2:
        print(f'{num1} é maior que {num2}')
    elif num2 > num1:
        print(f'{num2} é maior que {num1}')
    else:
        print(f'os numeros {num1} - {num2} são iguais')

# Exercicio 9 - Contagem regressiva
def exercicio_9():
    for i in range(10, 0, -1):
        print(i)

# Exercicio 10 - Verifique se a palavra é um palíndromo
def exercicio_10():
    palavra = input('Digite a palavra: ');
    lengthPalavra = len(palavra)
    novaPalavra = ''
    for i in range(lengthPalavra -1, -1, -1):
        novaPalavra += palavra[i]
    else:
        print(novaPalavra)
    if novaPalavra == palavra:
        print(f'A palvra {palavra} é um palíndromo')
    else:
        print(f'A palvra {palavra} não é palíndromo')
    