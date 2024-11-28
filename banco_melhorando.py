import textwrap
from abc import ABC, abstractclassmethod, abstractproperty

# Primeiro colocar todas as classes que estão sendo solicitadas no desafio, são elas: Cliente, pessoa fisica, conta, conta corrente,...
# ... históico de transações, transação, Saque e Depósito

# Cliente irá possuir endereço, conta
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.conta = []

# adicionar realizar transação e adicionar conta como manda no mapa    
    def realizar_transacao(self, transacao, conta ):
        transacao.registrar(conta)
 
    def adicionar_conta(self, conta):
        self.conta.append(conta)

# Pessoa fisica terá cpf, nome e data de nascimento
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):   
       super().__init__(endereco)
       self.cpf = cpf
       self.nome = nome
       self.data_nascimento = data_nascimento

# conta saldo: float, numero sempre inteiro (acima de 0), agencia (0001), cliente, histórico
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        passou_limite = valor > saldo

        if passou_limite:
            print("Você não possui limite para esse valor!")

        elif valor > 0:
            print ("Saque realizado com sucesso!")
            return True
        
        else:
            print("Operação impossível! Valor negativo, tente novamente!")
            
        return False
        
    def depositar(self, valor):
        if valor > 0:
            print("Depósito realizado!")
        else:
            print("Operação impossível! Valor negativo, tente novamente!")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([ transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("Valor de saque excede o limite!")

        elif excedeu_saques:
            print("Número de saque máximo excedido")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacao.append(
            {
                "tipo": transacao._class__.__name__,
                "valor": transacao.valor,
                }
        )

# Tudo que for feito de deposito e saque deve ser registrado 
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Saque valor float desde que tenha o valor para tirar
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Deposito valor float desde que seá um numero acima de 0
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# copiar o projeto que fiz em relação a banco da parte do menu e reajustar para o atual projeto
# a opção do menu será a mesma coisa
def menu():
    menu = """\n
    ---------- MENU ----------
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [c]\tLista de Contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# filtrar cliente: aqui é feito usando será feito a partir de uma instancia da classe cliente
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# caso o cliente esteja com dificuldade de acessar, pode o cliente recuperar a conta
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Você não possui conta ainda!")
        return
    # FIXME: não permite cliente escolher conta!
    return cliente.contas[0]

# primeiro verificar se o cliente possui conta para poder realizar o deposito
def depositar (clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
# caso o cliente exista permite ser realizado a transação
    valor = float(input("Informe valor a ser depositado:"))
    transacao = Deposito(valor)

# caso o cleinte esteja com dificuldade de acessar, pode o cliente recuperar a conta
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
        
    cliente.realizar_transacao(transacao, conta)

# primeiro verificar se o cliente possui conta para poder realizar o saque
def sacar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return

# caso o cliente exista permite ser realizado a transação
    valor = float(input("Informe valor a ser sacado:"))
    transacao = Saque(valor)

# caso o cleinte esteja com dificuldade de acessar, pode o cliente recuperar a conta
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
        
    cliente.realizar_transacao(transacao, conta)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(clientes, cpf)

# primeiro verificar se o cliente possui conta
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n-------------- EXTRATO --------------")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não possui movimentação!"

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f]}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("\n------------------------------------")

def criar_cliente(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe um cliente com esse CPF!")
        return

    nome = input("Informe nome completo: ")
    data_nascimento = input("Informe data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe endereco: ")

# Nesse modelo estamos tratando só de pessoa fisica então irá só receber endereço, nome, nascimento e cpf
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,endereco=endereco,cpf=cpf)
    clientes.append(cliente)

    print("Cliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(clientes, cpf)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
# semelhante ao que trabalhei, para criar uma conta seguir a sequencia de acordo com a ordem cronologica
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    clientes.contas.append(conta)

    print("Conta criada com Sucesso! Bem vindo!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# O main é muito parecido com o projeto do desafio, contudo só foi ajustado para deixar o projeto mais dinâmico e realista
def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            numero_conta = len(contas) + 1
            criar_conta(clientes, numero_conta, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação Impossível, selecione direito uma das opções!")

main()

# Acredito que um dos proximos passos do projeto será a criação do banco de dados para salvar os dados das transações
# provavelmente usar sql, ansioso pra começar a usar essa parte de Banco de Dados