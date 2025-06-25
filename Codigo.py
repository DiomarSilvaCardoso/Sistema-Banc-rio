import textwrap

# listas globais para armazenar usuarios e contas

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
        print("\nDeposito realizado com sucesso!")

    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return saldo, extrato

#função para saque (somente argumentos nomeado)
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Saldo insuficiente.")

    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excedeu o limite.")

    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")

    else:
        print("\nOperação falhou! O valor informado é invalido.")
    return saldo, extrato, numero_saques

#função para exibir extrato (posição e nomeados)
def exibir_extrato(saldo, /, *, extrato):
        print("\n====================EXTRATO====================")
        print("\nNão foram realizada movimenatções hoje." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=================================================")

# função para cadastrar usuarios
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\nUsuario já existente!")
        return
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa):").strip()
    endereço = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    print("\nUsuário criado com sucesso!")

# Função para criar conta corrente
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("\nInforme o CPF do usuario: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\nUsuario não encontrado. Conta não criada.")
        return None

    # Verifica se o usuário já possui uma conta
    for conta in contas:
        if conta['usuario']['cpf'] == cpf:
            print("\nEste usuário já possui uma conta.")
            return None

    print("\nConta criada com sucesso!")
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    # Função auxiliar para buscar usuarios pelo cpf.
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

#Função para listar contas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência: {conta['agencia']}
        C/C: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}
    """
        print("=" * 40)
        print(textwrap.dedent(linha))

#Programa principal

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo   = 0
    limite  = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas   = []

    while True:
        menu = """

    =====================MENU=====================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo usuario
        [nc] Nova conta
        [lc] Listar contas
        [q] Sair
        => """

        opcao = input(menu).strip().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do Deposito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            # Passa a lista 'contas' para a função criar_conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "q":
            print("Saindo do sistema. Volte sempre!")
            break
        else:
            print("Operação inválida. Por favor, selecione novamente.")

if __name__ == '__main__':
    main()

