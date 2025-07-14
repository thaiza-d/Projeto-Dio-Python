from datetime import datetime
from abc import ABC, abstractmethod
from functools import wraps

# DECORADOR
def registrar_data(func):
    @wraps(func)
    def wrapper(self, conta):
        resultado = func(self, conta)
        data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        conta.historico.append(f'{data} - {self.__class__.__name__} de R${self.valor:.2f}')
        return resultado
    return wrapper

# CLASSES PRINCIPAIS

class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.conta = None

    def criar_conta(self):
        self.conta = ContaCorrente(numero_conta='001', saldo=0)

class ContaCorrente:
    def __init__(self, numero_conta, saldo):
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.historico = []

    def exibir_extrato(self):
        print("\nExtrato da conta:")
        if self.historico:
            for item in self.historico:
                print(item)
        else:
            print("Nenhuma transação realizada.")

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    @registrar_data
    def registrar(self, conta):
        conta.saldo += self.valor
        print(f'Depósito de R${self.valor:.2f} realizado com sucesso.')

class Saque(Transacao):
    @registrar_data
    def registrar(self, conta):
        if self.valor <= conta.saldo:
            conta.saldo -= self.valor
            print(f'Saque de R${self.valor:.2f} realizado com sucesso.')
        else:
            print('Saldo insuficiente.')

# MENU
def menu():
    nome = input("Seu nome: ").title()
    endereco = input("Seu endereço: ")
    cliente = Cliente(nome, endereco)
    cliente.criar_conta()

    while True:
        print("\n[1] Depositar\n[2] Sacar\n[3] Extrato\n[4] Sair")
        opcao = input("Escolha: ")

        if opcao == '1':
            valor = float(input("Valor do depósito: R$"))
            deposito = Deposito(valor)
            deposito.registrar(cliente.conta)
        elif opcao == '2':
            valor = float(input("Valor do saque: R$"))
            saque = Saque(valor)
            saque.registrar(cliente.conta)
        elif opcao == '3':
            cliente.conta.exibir_extrato()
        elif opcao == '4':
            print("Volte sempre!")
            break
        else:
            print("Opção inválida.")

menu()
