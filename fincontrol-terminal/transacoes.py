"""
MÓDULO DE TRANSAÇÕES  —  Responsável: Integrante 2

Aqui ficam as operações principais do sistema:
  - registrar receitas e despesas
  - listar (com filtros) e excluir transações
  - calcular o saldo total

Cada transação é um dicionário, por exemplo:
  {"id": 1, "tipo": "despesa", "descricao": "Mercado",
   "valor": 150.9, "categoria": "Alimentação", "data": "05/10/2026"}
"""

from dados import (AMARELO, NEGRITO, RESET, VERDE, VERMELHO, confirmar, formatar_moeda,
                   ler_data, ler_mes, ler_opcao, ler_texto, ler_valor, salvar_dados, titulo)

CATEGORIAS = {
    "receita": ["Salário", "Freelance", "Vendas", "Investimentos", "Outros"],
    "despesa": ["Alimentação", "Moradia", "Transporte", "Saúde", "Educação",
                "Lazer", "Contas", "Outros"],
}


# ----------------------------------------------------------------------
# Cálculos
# ----------------------------------------------------------------------

def calcular_totais(transacoes):
    """Percorre a lista e soma receitas e despesas. Retorna (receitas, despesas, saldo)."""
    receitas = 0.0
    despesas = 0.0
    for t in transacoes:
        if t["tipo"] == "receita":
            receitas += t["valor"]
        else:
            despesas += t["valor"]
    return round(receitas, 2), round(despesas, 2), round(receitas - despesas, 2)


def filtrar_por_mes(transacoes, mes_ano):
    """Devolve só as transações do mês 'MM/AAAA'. A data é 'DD/MM/AAAA', então comparamos a partir do 4º caractere."""
    resultado = []
    for t in transacoes:
        if t["data"][3:] == mes_ano:
            resultado.append(t)
    return resultado


def filtrar_por_tipo(transacoes, tipo):
    resultado = []
    for t in transacoes:
        if t["tipo"] == tipo:
            resultado.append(t)
    return resultado


def chave_data(transacao):
    """Transforma 'DD/MM/AAAA' em 'AAAAMMDD' para conseguir ordenar por data."""
    dia, mes, ano = transacao["data"].split("/")
    return ano + mes + dia


def proximo_id(transacoes):
    """Procura o maior id existente e soma 1."""
    maior = 0
    for t in transacoes:
        if t["id"] > maior:
            maior = t["id"]
    return maior + 1


# ----------------------------------------------------------------------
# Registrar
# ----------------------------------------------------------------------

def escolher_categoria(tipo):
    """Mostra as categorias numeradas e devolve a escolhida."""
    lista = CATEGORIAS[tipo]
    print("\nCategorias:")
    for numero, nome in enumerate(lista, start=1):
        print(f"  {numero}. {nome}")
    opcao = ler_opcao("Escolha a categoria: ", 1, len(lista))
    return lista[opcao - 1]


def registrar_transacao(dados, tipo):
    """Pergunta os dados, cria a transação, salva no arquivo e a devolve."""
    titulo("NOVA RECEITA" if tipo == "receita" else "NOVA DESPESA")

    descricao = ler_texto("Descrição: ")
    valor = ler_valor("Valor (R$): ")
    categoria = escolher_categoria(tipo)
    data = ler_data("Data (DD/MM/AAAA) [Enter = hoje]: ")

    transacao = {
        "id": proximo_id(dados["transacoes"]),
        "tipo": tipo,
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria,
        "data": data,
    }
    dados["transacoes"].append(transacao)
    salvar_dados(dados)

    cor = VERDE if tipo == "receita" else VERMELHO
    print(cor + f"\n✔ {tipo.capitalize()} de {formatar_moeda(valor)} registrada!" + RESET)
    return transacao


# ----------------------------------------------------------------------
# Listar / excluir
# ----------------------------------------------------------------------

def mostrar_tabela(transacoes):
    """Imprime as transações em formato de tabela, ordenadas por data."""
    if len(transacoes) == 0:
        print(AMARELO + "\nNenhuma transação encontrada." + RESET)
        return

    print(NEGRITO + f"\n{'ID':>3}  {'DATA':<10}  {'DESCRIÇÃO':<22} {'CATEGORIA':<12} {'VALOR':>14}" + RESET)
    print("-" * 66)
    for t in sorted(transacoes, key=chave_data):
        if t["tipo"] == "receita":
            valor = VERDE + f"{'+ ' + formatar_moeda(t['valor']):>14}" + RESET
        else:
            valor = VERMELHO + f"{'- ' + formatar_moeda(t['valor']):>14}" + RESET
        print(f"{t['id']:>3}  {t['data']:<10}  {t['descricao'][:22]:<22} {t['categoria'][:12]:<12} {valor}")

    receitas, despesas, saldo = calcular_totais(transacoes)
    print("-" * 66)
    print(f"{len(transacoes)} transação(ões) | "
          + VERDE + f"Receitas: {formatar_moeda(receitas)}" + RESET + " | "
          + VERMELHO + f"Despesas: {formatar_moeda(despesas)}" + RESET + " | "
          + NEGRITO + f"Saldo: {formatar_moeda(saldo)}" + RESET)


def listar_transacoes(dados):
    titulo("LISTAR TRANSAÇÕES")
    print("1. Todas")
    print("2. Só receitas")
    print("3. Só despesas")
    print("4. De um mês específico")
    opcao = ler_opcao("Escolha: ", 1, 4)

    lista = dados["transacoes"]
    if opcao == 2:
        lista = filtrar_por_tipo(lista, "receita")
    elif opcao == 3:
        lista = filtrar_por_tipo(lista, "despesa")
    elif opcao == 4:
        mes = ler_mes("Mês (MM/AAAA) [Enter = mês atual]: ")
        lista = filtrar_por_mes(lista, mes)

    mostrar_tabela(lista)


def excluir_transacao(dados):
    titulo("EXCLUIR TRANSAÇÃO")
    if len(dados["transacoes"]) == 0:
        print(AMARELO + "Não há transações para excluir." + RESET)
        return

    mostrar_tabela(dados["transacoes"])
    id_escolhido = ler_opcao("\nID da transação (0 = cancelar): ", 0, proximo_id(dados["transacoes"]))
    if id_escolhido == 0:
        print("Operação cancelada.")
        return

    # Procura a transação com esse id
    for t in dados["transacoes"]:
        if t["id"] == id_escolhido:
            if confirmar(f"Excluir '{t['descricao']}' de {formatar_moeda(t['valor'])}?"):
                dados["transacoes"].remove(t)
                salvar_dados(dados)
                print(VERDE + "✔ Transação excluída." + RESET)
            else:
                print("Operação cancelada.")
            return  # encontrou: sai da função

    print(VERMELHO + "Nenhuma transação com esse ID." + RESET)


# ----------------------------------------------------------------------
# Saldo
# ----------------------------------------------------------------------

def ver_saldo(dados):
    titulo("SALDO TOTAL")
    receitas, despesas, saldo = calcular_totais(dados["transacoes"])

    print(VERDE + f"  Total de receitas: {formatar_moeda(receitas):>15}" + RESET)
    print(VERMELHO + f"  Total de despesas: {formatar_moeda(despesas):>15}" + RESET)
    print("  " + "-" * 34)

    # A cor e a mensagem mudam conforme a situação do saldo
    if saldo > 0:
        print(NEGRITO + VERDE + f"  SALDO:             {formatar_moeda(saldo):>15}" + RESET)
        print(VERDE + "\n  Parabéns! Suas contas estão no azul." + RESET)
    elif saldo == 0:
        print(NEGRITO + AMARELO + f"  SALDO:             {formatar_moeda(saldo):>15}" + RESET)
        print(AMARELO + "\n  Atenção: você gastou exatamente o que recebeu." + RESET)
    else:
        print(NEGRITO + VERMELHO + f"  SALDO:             {formatar_moeda(saldo):>15}" + RESET)
        print(VERMELHO + "\n  Cuidado! Você está gastando mais do que recebe." + RESET)
