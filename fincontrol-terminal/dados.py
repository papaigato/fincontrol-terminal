"""
MÓDULO DE DADOS E ENTRADAS  —  Responsável: Integrante 1

Este módulo cuida de três coisas:
  1. Salvar e carregar as transações em um arquivo (financas.json),
     para que nada se perca ao fechar o programa.
  2. Ler o que o usuário digita, repetindo a pergunta até receber
     um valor válido (validação de entrada).
  3. Funções de apoio para a tela: cores, títulos e formato de moeda.
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

ARQUIVO = "financas.json"

# Códigos de cor do terminal (ANSI). Deixam receitas verdes, despesas vermelhas etc.
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[96m"
NEGRITO = "\033[1m"
RESET = "\033[0m"


# ----------------------------------------------------------------------
# Arquivo
# ----------------------------------------------------------------------

def dados_vazios():
    """Estrutura inicial: lista de transações e limite de gastos do mês."""
    return {"transacoes": [], "limite_mensal": 0.0}


def carregar_dados():
    """Lê o arquivo JSON. Se ele não existir ou estiver com erro, começa do zero."""
    if not os.path.exists(ARQUIVO):
        return dados_vazios()
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        print(AMARELO + "Aviso: não foi possível ler o arquivo. Começando do zero." + RESET)
        return dados_vazios()


def salvar_dados(dados):
    """Grava todas as transações no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------
# Leitura de entradas com validação (laço while até a entrada ser válida)
# ----------------------------------------------------------------------

def ler_texto(mensagem):
    """Pede um texto que não pode ficar vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print(VERMELHO + "  Este campo não pode ficar vazio." + RESET)


def ler_valor(mensagem):
    """Pede um valor em reais. Aceita '1.234,56' ou '1234.56'."""
    while True:
        texto = input(mensagem).strip().replace("R$", "").replace(" ", "")

        # Formato brasileiro: tira o ponto de milhar e troca a vírgula por ponto
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")

        try:
            valor = float(texto)
        except ValueError:
            print(VERMELHO + "  Valor inválido. Exemplo: 150,90" + RESET)
            continue  # volta para o início do laço e pergunta de novo

        if valor <= 0:
            print(VERMELHO + "  O valor precisa ser maior que zero." + RESET)
        else:
            return round(valor, 2)


def ler_opcao(mensagem, minimo, maximo):
    """Pede um número inteiro dentro do intervalo [minimo, maximo]."""
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(VERMELHO + f"  Digite um número de {minimo} a {maximo}." + RESET)


def ler_data(mensagem):
    """Pede uma data DD/MM/AAAA. Se o usuário apertar Enter, usa a data de hoje."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            return date.today().strftime("%d/%m/%Y")
        try:
            data = datetime.strptime(texto, "%d/%m/%Y")
            return data.strftime("%d/%m/%Y")
        except ValueError:
            print(VERMELHO + "  Data inválida. Use o formato DD/MM/AAAA (ex.: 05/10/2026)." + RESET)


def ler_mes(mensagem):
    """Pede um mês no formato MM/AAAA. Enter = mês atual."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            return mes_atual()
        try:
            return datetime.strptime(texto, "%m/%Y").strftime("%m/%Y")
        except ValueError:
            print(VERMELHO + "  Mês inválido. Use MM/AAAA (ex.: 09/2026)." + RESET)


def confirmar(mensagem):
    """Pergunta sim/não. Retorna True para 's'."""
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print(VERMELHO + "  Responda com s ou n." + RESET)


# ----------------------------------------------------------------------
# Apoio para a tela
# ----------------------------------------------------------------------

def ativar_cores():
    """No Windows, este comando vazio liga o suporte a cores no terminal."""
    if os.name == "nt":
        os.system("")


def limpar_tela():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input(AZUL + "\nPressione Enter para voltar ao menu..." + RESET)


def titulo(texto):
    print()
    print(NEGRITO + AZUL + "=" * 50)
    print(texto.center(50))
    print("=" * 50 + RESET)


def formatar_moeda(valor):
    """Converte 1234.5 em 'R$ 1.234,50' (padrão brasileiro)."""
    texto = f"{abs(valor):,.2f}"                                   # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")  # 1.234,50
    if valor < 0:
        return "-R$ " + texto
    return "R$ " + texto


def mes_atual():
    return date.today().strftime("%m/%Y")


# ----------------------------------------------------------------------
# Dados de exemplo (para demonstrar o programa na apresentação)
# ----------------------------------------------------------------------

def gerar_exemplo():
    """Cria transações do mês atual e do mês anterior para demonstração."""
    hoje = date.today()
    mes_passado = hoje.replace(day=1) - timedelta(days=1)

    # (tipo, descrição, valor, categoria, dia do mês)
    modelo = [
        ("receita", "Salário", 3500.00, "Salário", 5),
        ("receita", "Bico de manutenção", 450.00, "Freelance", 12),
        ("despesa", "Aluguel", 1200.00, "Moradia", 10),
        ("despesa", "Supermercado", 685.40, "Alimentação", 8),
        ("despesa", "Conta de luz", 187.90, "Contas", 15),
        ("despesa", "Internet", 99.90, "Contas", 15),
        ("despesa", "Combustível", 250.00, "Transporte", 3),
        ("despesa", "Lanche com amigos", 78.50, "Lazer", 1),
        ("despesa", "Curso online", 49.90, "Educação", 20),
    ]

    transacoes = []
    for data_base in (mes_passado, hoje):
        for tipo, descricao, valor, categoria, dia in modelo:
            # evita datas no futuro e dias que não existem no mês
            dia_final = min(dia, data_base.day if data_base == hoje else 28)
            data = data_base.replace(day=dia_final)
            transacoes.append({
                "id": len(transacoes) + 1,
                "tipo": tipo,
                "descricao": descricao,
                "valor": valor,
                "categoria": categoria,
                "data": data.strftime("%d/%m/%Y"),
            })
    return {"transacoes": transacoes, "limite_mensal": 2400.00}
