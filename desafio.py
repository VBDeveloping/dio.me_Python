import textwrap

def menu():
    menu = """\n
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [c]\tLista de Contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(contas, numero_conta, valor):
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

    if conta:
        if valor > 0:
            conta["saldo"] += valor
            conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nValor inválido para depósito.")
    else:
        print("\nConta não encontrada!")

def sacar(contas, numero_conta, valor, limite, LIMITE_SAQUES):
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

    if conta:
        acima_saldo = valor > conta["saldo"]
        acima_limite = valor > limite
        acima_saques = conta.get("numero_saques", 0) >= LIMITE_SAQUES

        if acima_saldo:
            print("\nSaldo insuficiente!")
        elif acima_limite:
            print("\nValor do saque acima do limite!")
        elif acima_saques:
            print("\nNúmero máximo de saques excedido!")
        elif valor > 0:
            conta["saldo"] -= valor
            conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
            conta["numero_saques"] = conta.get("numero_saques", 0) + 1
            print("\nSaque realizado com sucesso!")
        else:
            print("\nValor inválido para saque.")
    else:
        print("\nConta não encontrada!")

def exibir_extrato(contas, numero_conta):
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

    if conta:
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações" if not conta["extrato"] else conta["extrato"])
        print(f"\nSaldo: R$ {conta['saldo']:.2f}")
        print("===============================")
    else:
        print("\nConta não encontrada!")

def novo_usuario(usuarios):
    cpf = input("Por favor, informe o CPF (digitar somente números): ")
    usuario = selecionar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe um usuário com esse CPF!")
        return

    nome = input("Por favor, informe o nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (rua, número, bairro, cidade, estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\nUsuário criado com sucesso!")

def selecionar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def nova_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = selecionar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "numero_saques": 0}
    else:
        print("\nUsuário não encontrado!")
        return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
        Agência:\t{conta['agencia']}
        C/C:\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))

def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do depósito: "))
            depositar(contas, numero_conta, valor)

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do saque: "))
            limite = 500
            LIMITE_SAQUES = 3
            sacar(contas, numero_conta, valor, limite, LIMITE_SAQUES)

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            exibir_extrato(contas, numero_conta)

        elif opcao == "nu":
            novo_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = nova_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "c":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema bancário!")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")

main()
