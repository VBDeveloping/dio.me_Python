menu = """

[d] Depositar
[s] Sacar
[e] Extrator
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: ")) 
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print ("Valor informado é inválido")


    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        
        acima_saldo = valor > saldo

        acima_limite = valor > limite

        acima_saques = numero_saque >= LIMITE_SAQUE

        if acima_saldo:
            print ("Valor informado é acima do que você possui na conta")

        elif acima_limite:
            print ("Saque acima do que você possui na conta")

        elif acima_saques:
            print ("Número de saques acima da quantidade contratada")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque += 1

        else:
            print ("Valor informado é inválido.")

    elif opcao == "e":
        print ("\n========== EXTRATO ==========")
        print ("Não foram realizadas movimentações" if not extrato else extrato)
        print (f"\nSaldo: R$ {valor:.2f}")
        print ("===============================")

    elif opcao == "q":
        break

    else:
        print ("Operção inválida, por favor selecione novamente a operação desejada")