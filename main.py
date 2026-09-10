def exibir_menu():
    print("\n================ MENU ================")
    print("[1] Saque")
    print("[2] Depósito")
    print("[3] Extrato")
    print("[0] Sair")
    print("======================================")
    return input("Escolha uma opção: ")

saldo = 0.0
extrato = ""

while True:
    opcao = exibir_menu()

    if opcao == "1":
        valor = float(input("Digite o valor do saque: R$ "))
        
        if valor <= 0:
            print(" O valor informado é inválido.")
        elif valor > saldo:
            print(f"Você não tem saldo suficiente. Saldo atual: R$ {saldo:.2f}")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    elif opcao == "2":
        valor = float(input("Digite o valor do depósito: R$ "))
        
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("O valor informado é inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "0":
        print("\nObrigado por usar nosso sistema bancário. Até logo!")
        break

    else:
        print("Por favor selecione novamente a operação desejada.")