# banco.py

TAXAS_CAMBIO = {"USD": 5.50, "EUR": 6.00, "BTC": 350000.00}

contas = [
    {
        "numero_conta": "0001",
        "nome": "João Silva",
        "chave_pix": "joao@email.com",
        "saldo": 2000.00,
        "extrato": [],
        "caixinhas": {"Reserva": 500.0, "Viagem": 300.0},
        "cartao": {"limite_total": 1500.0, "limite_disponivel": 1500.0, "fatura": 0.0},
        "moedas": {"USD": 0.0, "EUR": 0.0, "BTC": 0.0},
        "bytepoints": 0,
        "emprestimo": {"saldo_devedor": 0.0, "valor_parcela": 0.0, "parcelas_restantes": 0}
    },
    {
        "numero_conta": "0002",
        "nome": "Maria Santos",
        "chave_pix": "11999999999",
        "saldo": 1200.00,
        "extrato": [],
        "caixinhas": {},
        "cartao": {"limite_total": 2000.0, "limite_disponivel": 2000.0, "fatura": 0.0},
        "moedas": {"USD": 0.0, "EUR": 0.0, "BTC": 0.0},
        "bytepoints": 0,
        "emprestimo": {"saldo_devedor": 0.0, "valor_parcela": 0.0, "parcelas_restantes": 0}
    }
]


def buscar_conta_por_pix(chave_pix):
    for conta in contas:
        if conta["chave_pix"].strip().lower() == str(chave_pix).strip().lower():
            return conta
    return None


def buscar_conta_por_numero(numero_conta):
    for conta in contas:
        if conta["numero_conta"].strip() == str(numero_conta).strip():
            return conta
    return None


def acumular_bytepoints(conta, valor_gasto):
    pontos_ganhos = int(valor_gasto // 10)
    if pontos_ganhos > 0:
        conta["bytepoints"] += pontos_ganhos


def realizar_deposito(conta, valor):
    if valor <= 0:
        return False, "Valor inválido para depósito."
    conta["saldo"] += valor
    conta["extrato"].append({
        "tipo": "Depósito",
        "valor": valor,
        "categoria": "Receita",
        "descricao": "Depósito em conta"
    })
    return True, f"Depósito de R$ {valor:.2f} realizado com sucesso!"


def realizar_saque(conta, valor):
    if valor <= 0:
        return False, "Valor inválido para saque."
    if valor > conta["saldo"]:
        return False, "Saldo insuficiente para realizar o saque."

    conta["saldo"] -= valor
    conta["extrato"].append({
        "tipo": "Saque",
        "valor": valor,
        "categoria": "Outros",
        "descricao": "Saque em caixa"
    })
    acumular_bytepoints(conta, valor)
    return True, f"Saque de R$ {valor:.2f} realizado com sucesso!"


def realizar_transferencia_pix(origem, chave_destino, valor):
    if valor <= 0:
        return False, "Valor inválido para transferência."

    if origem["saldo"] < valor:
        return False, "Saldo insuficiente para transferência."

    destino = buscar_conta_por_pix(chave_destino)
    if not destino:
        return False, "Chave PIX não encontrada."

    if origem["chave_pix"].strip().lower() == destino["chave_pix"].strip().lower():
        return False, "Não é possível transferir para a própria conta."

    origem["saldo"] -= valor
    destino["saldo"] += valor

    origem["extrato"].append({
        "tipo": "PIX Enviado",
        "valor": valor,
        "categoria": "Transferência",
        "descricao": f"Para {destino['nome']}"
    })
    destino["extrato"].append({
        "tipo": "PIX Recebido",
        "valor": valor,
        "categoria": "Transferência",
        "descricao": f"De {origem['nome']}"
    })

    acumular_bytepoints(origem, valor)
    return True, f"Transferência de R$ {valor:.2f} enviada para {destino['nome']}!"


def listar_contas():
    return contas


def resumo_conta(conta):
    return {
        "numero": conta["numero_conta"],
        "nome": conta["nome"],
        "saldo": conta["saldo"],
        "bytepoints": conta["bytepoints"],
        "pix": conta["chave_pix"]
    }