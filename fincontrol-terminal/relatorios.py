"""
MÓDULO DE RELATÓRIOS  —  Responsável: Integrante 3

Gera o resumo financeiro e os alertas:
  - totais do período, maior despesa, média de gastos
  - gastos por categoria com gráfico de barras no terminal
  - classificação da saúde financeira (estruturas de decisão)
  - limite mensal de gastos com alerta
"""

from dados import (AMARELO, AZUL, NEGRITO, RESET, VERDE, VERMELHO, formatar_moeda,
                   ler_mes, ler_opcao, ler_valor, mes_atual, salvar_dados, titulo)
from transacoes import calcular_totais, filtrar_por_mes, filtrar_por_tipo

AVISO_LIMITE = 80  # avisa quando o gasto do mês passar de 80% do limite


# ----------------------------------------------------------------------
# Funções de cálculo
# ----------------------------------------------------------------------

def gastos_por_categoria(transacoes):
    """Soma as despesas de cada categoria. Retorna um dicionário {categoria: total}."""
    totais = {}
    for t in transacoes:
        if t["tipo"] == "despesa":
            if t["categoria"] in totais:
                totais[t["categoria"]] += t["valor"]
            else:
                totais[t["categoria"]] = t["valor"]
    return totais


def maior_despesa(transacoes):
    """Encontra a despesa de maior valor (ou None se não houver despesas)."""
    maior = None
    for t in transacoes:
        if t["tipo"] == "despesa":
            if maior is None or t["valor"] > maior["valor"]:
                maior = t
    return maior


def desenhar_barra(valor, maximo, largura=25):
    """Cria uma barra proporcional ao valor. Ex.: '██████████'."""
    if maximo == 0:
        return ""
    tamanho = int(valor / maximo * largura)
    return "█" * max(tamanho, 1)


def classificar_situacao(receitas, despesas):
    """Usa if/elif/else para classificar a saúde financeira pelo % da renda gasto."""
    if receitas == 0 and despesas == 0:
        return AMARELO, "Sem movimentação no período."
    if receitas == 0:
        return VERMELHO, "Há despesas, mas nenhuma receita registrada!"

    percentual = despesas / receitas * 100
    if percentual <= 50:
        return VERDE, f"EXCELENTE: você gastou só {percentual:.0f}% do que ganhou."
    elif percentual <= 80:
        return VERDE, f"BOM: gastou {percentual:.0f}% da renda. Dá para guardar um pouco mais."
    elif percentual <= 100:
        return AMARELO, f"ATENÇÃO: {percentual:.0f}% da renda já foi gasta."
    else:
        return VERMELHO, f"CRÍTICO: gastou {percentual:.0f}% da renda. Está no vermelho!"


# ----------------------------------------------------------------------
# Resumo financeiro
# ----------------------------------------------------------------------

def resumo_financeiro(dados):
    titulo("RESUMO FINANCEIRO")
    print("1. Mês atual")
    print("2. Outro mês")
    print("3. Todo o período")
    opcao = ler_opcao("Escolha: ", 1, 3)

    if opcao == 1:
        periodo = mes_atual()
        transacoes = filtrar_por_mes(dados["transacoes"], periodo)
    elif opcao == 2:
        periodo = ler_mes("Mês (MM/AAAA): ")
        transacoes = filtrar_por_mes(dados["transacoes"], periodo)
    else:
        periodo = "todo o período"
        transacoes = dados["transacoes"]

    if len(transacoes) == 0:
        print(AMARELO + f"\nNenhuma transação em {periodo}." + RESET)
        return

    receitas, despesas, saldo = calcular_totais(transacoes)
    qtd_despesas = len(filtrar_por_tipo(transacoes, "despesa"))

    # --- Totais ---
    print(NEGRITO + f"\nPeríodo: {periodo}" + RESET)
    print(VERDE + f"  Receitas:  {formatar_moeda(receitas):>15}" + RESET)
    print(VERMELHO + f"  Despesas:  {formatar_moeda(despesas):>15}" + RESET)
    cor_saldo = VERDE if saldo >= 0 else VERMELHO
    print(NEGRITO + cor_saldo + f"  Saldo:     {formatar_moeda(saldo):>15}" + RESET)

    # --- Estatísticas ---
    print(NEGRITO + "\nEstatísticas" + RESET)
    print(f"  Transações registradas: {len(transacoes)}")
    if qtd_despesas > 0:
        maior = maior_despesa(transacoes)
        print(f"  Maior despesa: {maior['descricao']} ({formatar_moeda(maior['valor'])})")
        print(f"  Média por despesa: {formatar_moeda(despesas / qtd_despesas)}")
    if receitas > 0 and saldo > 0:
        print(f"  Você economizou {saldo / receitas * 100:.0f}% da sua renda.")

    # --- Gastos por categoria com gráfico ---
    categorias = gastos_por_categoria(transacoes)
    if len(categorias) > 0:
        print(NEGRITO + "\nGastos por categoria" + RESET)
        maior_valor = max(categorias.values())
        # ordena da categoria que mais gastou para a que menos gastou
        for nome in sorted(categorias, key=categorias.get, reverse=True):
            valor = categorias[nome]
            percentual = valor / despesas * 100
            barra = desenhar_barra(valor, maior_valor)
            print(f"  {nome:<12} {AZUL}{barra:<25}{RESET} {formatar_moeda(valor):>13} (" + f"{percentual:4.1f}".replace(".", ",") + "%)")

    # --- Diagnóstico ---
    cor, mensagem = classificar_situacao(receitas, despesas)
    print(NEGRITO + "\nDiagnóstico" + RESET)
    print(cor + "  " + mensagem + RESET)

    # --- Limite mensal (só faz sentido para um mês) ---
    if opcao != 3 and dados["limite_mensal"] > 0:
        mostrar_situacao_limite(despesas, dados["limite_mensal"])


# ----------------------------------------------------------------------
# Limite mensal de gastos
# ----------------------------------------------------------------------

def mostrar_situacao_limite(gasto, limite):
    """Mostra quanto do limite foi usado, com barra e alerta."""
    percentual = gasto / limite * 100
    barra = desenhar_barra(min(gasto, limite), limite, 30)

    if percentual >= 100:
        cor = VERMELHO
        aviso = f"LIMITE ESTOURADO em {formatar_moeda(gasto - limite)}!"
    elif percentual >= AVISO_LIMITE:
        cor = AMARELO
        aviso = f"Atenção: restam só {formatar_moeda(limite - gasto)} do limite."
    else:
        cor = VERDE
        aviso = f"Dentro do limite. Ainda pode gastar {formatar_moeda(limite - gasto)}."

    print(NEGRITO + "\nLimite mensal de gastos" + RESET)
    print(f"  {cor}{barra:<30}{RESET} {percentual:.0f}% de {formatar_moeda(limite)}")
    print(cor + "  " + aviso + RESET)


def definir_limite(dados):
    titulo("LIMITE MENSAL DE GASTOS")
    if dados["limite_mensal"] > 0:
        print(f"Limite atual: {formatar_moeda(dados['limite_mensal'])}")
    else:
        print("Nenhum limite definido.")
    print("\n1. Definir novo limite")
    print("2. Remover limite")
    print("0. Voltar")
    opcao = ler_opcao("Escolha: ", 0, 2)

    if opcao == 1:
        dados["limite_mensal"] = ler_valor("Novo limite mensal (R$): ")
        salvar_dados(dados)
        print(VERDE + f"✔ Limite definido: {formatar_moeda(dados['limite_mensal'])}" + RESET)
    elif opcao == 2:
        dados["limite_mensal"] = 0.0
        salvar_dados(dados)
        print(VERDE + "✔ Limite removido." + RESET)


def verificar_limite(dados, data):
    """Chamada logo após registrar uma despesa: avisa se o mês passou do limite."""
    limite = dados["limite_mensal"]
    if limite <= 0:
        return  # sem limite definido, nada a verificar

    mes = data[3:]  # 'DD/MM/AAAA' -> 'MM/AAAA'
    despesas_mes = calcular_totais(filtrar_por_mes(dados["transacoes"], mes))[1]
    if despesas_mes / limite * 100 >= AVISO_LIMITE:
        mostrar_situacao_limite(despesas_mes, limite)
