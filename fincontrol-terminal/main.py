"""
FinControl — Sistema de Controle Financeiro (versão terminal)
Hackathon Python — SENAI

Como executar:  python main.py

Arquivos do projeto:
  main.py        -> menu principal (este arquivo)
  dados.py       -> arquivo, validação de entradas e formatação   (Integrante 1)
  transacoes.py  -> registrar, listar, excluir e calcular saldo    (Integrante 2)
  relatorios.py  -> resumo financeiro, gráficos e alertas          (Integrante 3)
"""

from dados import (AZUL, NEGRITO, RESET, VERDE, VERMELHO, ativar_cores, carregar_dados, confirmar,
                   formatar_moeda, gerar_exemplo, ler_opcao, limpar_tela, pausar, salvar_dados)
from relatorios import definir_limite, resumo_financeiro, verificar_limite
from transacoes import calcular_totais, excluir_transacao, listar_transacoes, registrar_transacao, ver_saldo


def mostrar_menu(dados):
    """Exibe o cabeçalho com o saldo atual e as opções do menu."""
    limpar_tela()
    saldo = calcular_totais(dados["transacoes"])[2]
    cor = VERDE if saldo >= 0 else VERMELHO

    print(NEGRITO + AZUL + "╔══════════════════════════════════════════╗")
    print("║        FINCONTROL - CONTROLE FINANCEIRO  ║")
    print("╚══════════════════════════════════════════╝" + RESET)
    print(f"  Saldo atual: {cor}{NEGRITO}{formatar_moeda(saldo)}{RESET}\n")
    print("  1. Registrar receita")
    print("  2. Registrar despesa")
    print("  3. Listar transações")
    print("  4. Ver saldo total")
    print("  5. Resumo financeiro")
    print("  6. Excluir transação")
    print("  7. Limite mensal de gastos")
    print("  8. Carregar dados de exemplo")
    print("  0. Sair")


def carregar_exemplo(dados):
    """Substitui os dados atuais por transações de demonstração."""
    if len(dados["transacoes"]) > 0:
        if not confirmar("Isso vai APAGAR suas transações atuais. Continuar?"):
            print("Operação cancelada.")
            return
    exemplo = gerar_exemplo()
    dados["transacoes"] = exemplo["transacoes"]
    dados["limite_mensal"] = exemplo["limite_mensal"]
    salvar_dados(dados)
    print(VERDE + f"✔ {len(dados['transacoes'])} transações de exemplo carregadas." + RESET)


def main():
    ativar_cores()
    dados = carregar_dados()

    # Laço principal: repete o menu até o usuário escolher 0 (Sair)
    while True:
        mostrar_menu(dados)
        opcao = ler_opcao("\nEscolha uma opção: ", 0, 8)

        if opcao == 0:
            print(AZUL + "\nDados salvos. Até a próxima!" + RESET)
            break
        elif opcao == 1:
            registrar_transacao(dados, "receita")
        elif opcao == 2:
            despesa = registrar_transacao(dados, "despesa")
            verificar_limite(dados, despesa["data"])  # alerta se passou do limite
        elif opcao == 3:
            listar_transacoes(dados)
        elif opcao == 4:
            ver_saldo(dados)
        elif opcao == 5:
            resumo_financeiro(dados)
        elif opcao == 6:
            excluir_transacao(dados)
        elif opcao == 7:
            definir_limite(dados)
        elif opcao == 8:
            carregar_exemplo(dados)

        pausar()


# Só executa o menu quando o arquivo é rodado diretamente (python main.py)
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(AZUL + "\n\nPrograma encerrado. Seus dados estão salvos." + RESET)
