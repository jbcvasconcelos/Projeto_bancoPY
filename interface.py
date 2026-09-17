# interface.py
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, messagebox, Toplevel

from banco import (
    contas,
    buscar_conta_por_numero,
    realizar_deposito,
    realizar_saque,
    realizar_transferencia_pix,
)

COR_FUNDO = "#FFF7F0"
COR_PAINEL = "#FFFFFF"
COR_LARANJA = "#F57C00"
COR_LARANJA_ESCURA = "#E65100"
COR_TEXTO = "#333333"
COR_SUCESSO = "#2E7D32"
COR_ERRO = "#C62828"
COR_BORDA = "#FFD1A3"


class AppBanco:
    def __init__(self, root):
        self.root = root
        self.root.title("JGBANK | Interface")
        self.root.geometry("820x590")
        self.root.minsize(760, 520)
        self.root.configure(bg=COR_FUNDO)

        self.conta_atual = contas[0]

        self.criar_interface()
        self.atualizar_dados_conta()

    def criar_interface(self):
        self.container = Frame(self.root, bg=COR_FUNDO, padx=24, pady=24)
        self.container.pack(fill="both", expand=True)

        cabecalho = Frame(self.container, bg=COR_PAINEL, bd=2, relief="flat")
        cabecalho.pack(fill="x", pady=(0, 20), padx=4)

        Label(
            cabecalho,
            text="JGBANK",
            font=("Arial", 22, "bold"),
            bg=COR_PAINEL,
            fg=COR_LARANJA_ESCURA,
            pady=18,
        ).pack()

        info_conta = Frame(self.container, bg=COR_FUNDO)
        info_conta.pack(fill="x", pady=(0, 20))

        self.lbl_cliente = Label(
            info_conta,
            text="",
            font=("Arial", 12, "bold"),
            bg=COR_FUNDO,
            fg=COR_TEXTO,
        )
        self.lbl_cliente.pack(anchor="w")

        self.lbl_saldo = Label(
            info_conta,
            text="",
            font=("Arial", 16, "bold"),
            bg=COR_FUNDO,
            fg=COR_LARANJA_ESCURA,
        )
        self.lbl_saldo.pack(anchor="w", pady=(6, 0))

        painel = Frame(self.container, bg=COR_PAINEL, bd=2, relief="solid")
        painel.pack(fill="both", expand=True, padx=4)

        Label(
            painel,
            text="Operações",
            font=("Arial", 13, "bold"),
            bg=COR_PAINEL,
            fg=COR_LARANJA_ESCURA,
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(16, 8))

        self.valor_var = StringVar()
        self.pix_var = StringVar()
        self.numero_var = StringVar()
        self.status_var = StringVar(value="Sistema pronto para uso.")

        Label(painel, text="Valor (R$):", bg=COR_PAINEL, fg=COR_TEXTO, font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=16, pady=8)
        Entry(painel, textvariable=self.valor_var, width=18, font=("Arial", 10), bd=2, relief="solid").grid(row=1, column=1, sticky="w", padx=(0, 12), pady=8)

        Label(painel, text="Chave PIX:", bg=COR_PAINEL, fg=COR_TEXTO, font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=16, pady=8)
        Entry(painel, textvariable=self.pix_var, width=30, font=("Arial", 10), bd=2, relief="solid").grid(row=2, column=1, sticky="w", padx=(0, 12), pady=8)

        Label(painel, text="Conta:", bg=COR_PAINEL, fg=COR_TEXTO, font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=16, pady=8)
        Entry(painel, textvariable=self.numero_var, width=18, font=("Arial", 10), bd=2, relief="solid").grid(row=3, column=1, sticky="w", padx=(0, 12), pady=8)

        bts = [
            ("Depositar", self.acao_deposito, COR_LARANJA),
            ("Sacar", self.acao_saque, COR_LARANJA),
            ("Transferir", self.acao_transferencia, COR_LARANJA_ESCURA),
            ("Consultar", self.acao_consultar_conta, COR_LARANJA_ESCURA),
            ("Cadastrar Cliente", self.acao_cadastrar_cliente, COR_LARANJA),
        ]

        for index, (texto, comando, cor) in enumerate(bts):
            Button(
                painel,
                text=texto,
                command=comando,
                bg=cor,
                fg="white",
                activebackground="#FFB266",
                activeforeground="white",
                bd=0,
                font=("Arial", 10, "bold"),
                width=15,
                height=1,
            ).grid(row=1 + (index // 2), column=2 + (index % 2), padx=10, pady=8, sticky="ew")

        painel.grid_propagate(False)

        status = Label(
            painel,
            textvariable=self.status_var,
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("Arial", 10, "italic"),
            wraplength=560,
            justify="left",
        )
        status.grid(row=4, column=0, columnspan=4, sticky="w", padx=16, pady=(22, 16))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        painel.columnconfigure(1, weight=1)

    def atualizar_dados_conta(self):
        self.lbl_cliente.config(text=f"Cliente: {self.conta_atual['nome']}")
        self.lbl_saldo.config(text=f"Saldo atual: R$ {self.conta_atual['saldo']:.2f}")

    def mostrar_status(self, mensagem, cor=COR_TEXTO):
        self.status_var.set(mensagem)
        self.root.update_idletasks()

    def ler_valor(self):
        texto = self.valor_var.get().strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return None

    def acao_deposito(self):
        valor = self.ler_valor()
        if valor is None or valor <= 0:
            self.mostrar_status("Digite um valor válido para depósito.", COR_ERRO)
            return

        ok, mensagem = realizar_deposito(self.conta_atual, valor)
        self.atualizar_dados_conta()
        self.mostrar_status(mensagem, COR_SUCESSO if ok else COR_ERRO)
        self.valor_var.set("")

    def acao_saque(self):
        valor = self.ler_valor()
        if valor is None or valor <= 0:
            self.mostrar_status("Digite um valor válido para saque.", COR_ERRO)
            return

        ok, mensagem = realizar_saque(self.conta_atual, valor)
        self.atualizar_dados_conta()
        self.mostrar_status(mensagem, COR_SUCESSO if ok else COR_ERRO)
        self.valor_var.set("")

    def acao_transferencia(self):
        valor = self.ler_valor()
        chave = self.pix_var.get().strip()

        if valor is None or valor <= 0:
            self.mostrar_status("Digite um valor válido para transferência.", COR_ERRO)
            return

        if not chave:
            self.mostrar_status("Informe a chave PIX do destinatário.", COR_ERRO)
            return

        ok, mensagem = realizar_transferencia_pix(self.conta_atual, chave, valor)
        self.atualizar_dados_conta()
        self.mostrar_status(mensagem, COR_SUCESSO if ok else COR_ERRO)
        self.valor_var.set("")
        self.pix_var.set("")

    def _criar_janela_modal(self, titulo):
        janela = Toplevel(self.root)
        janela.title(titulo)
        janela.transient(self.root)
        janela.grab_set()
        janela.geometry("380x220")
        janela.resizable(False, False)
        return janela

    def acao_consultar_conta(self):
        janela = self._criar_janela_modal("Consultar Cliente")

        Label(janela, text="Número da conta:", font=("Arial", 10, "bold")).pack(pady=(18, 6))
        numero_entry = Entry(janela, width=28, font=("Arial", 10), bd=2, relief="solid")
        numero_entry.pack(pady=(0, 12))

        def confirmar():
            numero = numero_entry.get().strip()
            if not numero:
                messagebox.showerror("Consulta", "Informe o número da conta.")
                return

            conta = buscar_conta_por_numero(numero)
            if not conta:
                messagebox.showerror("Consulta", "Conta não encontrada.")
                return

            mensagem = (
                f"Titular: {conta['nome']}\n"
                f"Saldo: R$ {conta['saldo']:.2f}\n"
                f"PIX: {conta['chave_pix']}"
            )
            messagebox.showinfo("Cliente encontrado", mensagem)
            janela.destroy()

        Button(
            janela,
            text="Consultar",
            command=confirmar,
            bg=COR_LARANJA,
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            width=14,
        ).pack()

        janela.focus_set()
        janela.wait_window()

    def acao_cadastrar_cliente(self):
        janela = self._criar_janela_modal("Cadastrar Cliente")

        campos = {
            "nome": ("Nome do cliente:", 0),
            "numero": ("Número da conta:", 1),
            "pix": ("Chave PIX:", 2),
        }
        variaveis = {}

        for chave, (texto, linha) in campos.items():
            Label(janela, text=texto, font=("Arial", 10, "bold")).grid(row=linha, column=0, padx=(18, 8), pady=(12, 6), sticky="w")
            var = StringVar()
            Entry(janela, textvariable=var, width=28, font=("Arial", 10), bd=2, relief="solid").grid(row=linha, column=1, padx=(0, 18), pady=(12, 6), sticky="ew")
            variaveis[chave] = var

        def salvar():
            nome = variaveis["nome"].get().strip()
            numero = variaveis["numero"].get().strip()
            chave_pix = variaveis["pix"].get().strip()

            if not nome or not numero or not chave_pix:
                messagebox.showerror("Cadastro", "Preencha todos os campos.")
                return

            for conta in contas:
                if conta["numero_conta"].strip() == numero or conta["chave_pix"].strip().lower() == chave_pix.lower():
                    messagebox.showerror("Cadastro", "Já existe uma conta ou chave PIX igual cadastrada.")
                    return

            nova_conta = {
                "numero_conta": numero,
                "nome": nome,
                "chave_pix": chave_pix,
                "saldo": 0.0,
                "extrato": [],
                "caixinhas": {},
                "cartao": {
                    "limite_total": 0.0,
                    "limite_disponivel": 0.0,
                    "fatura": 0.0,
                },
                "moedas": {"USD": 0.0, "EUR": 0.0, "BTC": 0.0},
                "bytepoints": 0,
                "emprestimo": {
                    "saldo_devedor": 0.0,
                    "valor_parcela": 0.0,
                    "parcelas_restantes": 0,
                },
            }

            contas.append(nova_conta)
            self.conta_atual = nova_conta
            self.atualizar_dados_conta()
            self.numero_var.set(numero)
            self.pix_var.set(chave_pix)
            self.mostrar_status(f"Cliente {nome} cadastrado com sucesso na conta {numero}.", COR_SUCESSO)
            messagebox.showinfo("Cadastro", f"Cliente {nome} cadastrado com sucesso!")
            janela.destroy()

        Button(
            janela,
            text="Salvar",
            command=salvar,
            bg=COR_LARANJA,
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            width=14,
        ).grid(row=3, column=0, columnspan=2, pady=(18, 12))

        janela.focus_set()
        janela.wait_window()


def criar_interface():
    root = Tk()
    AppBanco(root)
    root.mainloop()


if __name__ == "__main__":
    criar_interface()