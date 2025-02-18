import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO
from datetime import datetime, timedelta

# Dados de login (usuário e senha)
credenciais = {
    "henrique.degan": "12345",
    "vanessa.degan": "12345"
}

# Função para carregar os tipos da aba "Tipo"
def carregar_tipos():
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xlsx"
    try:
        # Carrega a planilha Excel e acessa a aba "Tipo"
        df = pd.read_excel(url, sheet_name="Tipo", engine="openpyxl")
        return df["Tipo"].tolist()  # Retorna os tipos como uma lista
    except Exception as e:
        st.error(f"Erro ao carregar os tipos: {e}")
        return []

# Função para carregar as categorias da aba "Categoria"
def carregar_categorias():
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xlsx"
    try:
        # Carrega a planilha Excel e acessa a aba "Categoria"
        df = pd.read_excel(url, sheet_name="Categoria", engine="openpyxl")
        return df["Categorias"].tolist()  # Retorna as categorias como uma lista
    except Exception as e:
        st.error(f"Erro ao carregar as categorias: {e}")
        return []

# Função para carregar os status da aba "Status"
def carregar_status():
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xlsx"
    try:
        # Carrega a planilha Excel e acessa a aba "Status"
        df = pd.read_excel(url, sheet_name="Status", engine="openpyxl")
        return df["Status"].tolist()  # Retorna os status como uma lista
    except Exception as e:
        st.error(f"Erro ao carregar os status: {e}")
        return []

# Função para carregar os registros da aba "Base"
def carregar_registros():
    # Caminho para o arquivo Excel
    arquivo_excel = "FIN_TC1.xlsx"
    
    try:
        # Carrega a planilha Excel e acessa a aba "Base"
        df = pd.read_excel(arquivo_excel, sheet_name="Base", engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os registros: {e}")
        return None

# Função para gerar a tabela dinâmica com base no período
def gerar_tabela_periodo(df, num_meses):
    # Filtra os registros dentro do período especificado
    data_atual = datetime.now()
    data_inicio = data_atual - timedelta(days=num_meses * 30)  # Aproximação de meses
    df_filtrado = df[df["Data de PGTO"] >= data_inicio]

    # Converte as datas para o formato "YYYY-MM" para agrupar por mês
    df_filtrado["Mês"] = df_filtrado["Data de PGTO"].dt.to_period("M").astype(str)

    # Agrupa por mês e calcula receitas e despesas
    tabela = df_filtrado.pivot_table(
        index="Categoria",
        columns="Mês",
        values="R$",
        aggfunc="sum",
        fill_value=0
    )

    # Adiciona a linha de saldo (Receitas - Despesas)
    tabela.loc["Saldo"] = tabela.sum(axis=0)

    return tabela

# Função principal do Streamlit
def main():
    st.title("Sistema de Login")

    # Verifica se o usuário já está logado
    if "logado" not in st.session_state:
        st.session_state.logado = False

    # Tela de login
    if not st.session_state.logado:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if verificar_login(usuario, senha):
                st.session_state.logado = True
                st.success("Login realizado com sucesso!")
                st.rerun()  # Recarrega a página após o login
            else:
                st.error("Usuário ou senha inválidos.")
    else:
        # Tela inicial após o login
        st.sidebar.title("Menu")
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Início", "Criar Registro", "Listar Registros", "Baixar Planilha"])

        if opcao == "Início":
            st.header("Resumo Financeiro por Período")

            # Carrega os registros da aba "Base"
            df_registros = carregar_registros()

            if df_registros is not None and not df_registros.empty:
                # Solicita o número de meses ao usuário
                num_meses = st.number_input("Digite o período em meses:", min_value=1, step=1)

                # Gera a tabela dinâmica
                tabela = gerar_tabela_periodo(df_registros, num_meses)

                # Exibe a tabela
                st.dataframe(tabela)
            else:
                st.info("Nenhum registro cadastrado.")

        elif opcao == "Criar Registro":
            st.header("Criar Novo Registro")

            # Carrega os tipos, categorias e status do Excel
            tipos = carregar_tipos()
            categorias = carregar_categorias()
            status_list = carregar_status()

            if tipos and categorias and status_list:
                tipo = st.selectbox("Tipo", tipos)
                categoria = st.selectbox("Categoria", categorias)
                data_pagamento = st.date_input("Data de Pagamento")
                valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
                tag = st.text_input("Tag (Label)")
                status = st.selectbox("Status", status_list)

                # Nova funcionalidade: Tipo de Conta
                tipo_conta = st.selectbox("Tipo de Conta", ["Fixa", "Parcelada"])
                parcelas = None
                if tipo_conta == "Parcelada":
                    parcelas = st.number_input("Número de Parcelas", min_value=1, step=1)

                if st.button("Salvar Registro"):
                    if not tipo or not categoria or not data_pagamento or not valor or not status:
                        st.error("Todos os campos obrigatórios devem ser preenchidos.")
                    else:
                        # Registra o registro na aba "Base"
                        if registrar_registro(tipo, categoria, data_pagamento, valor, tag, status, tipo_conta, parcelas):
                            st.success("Registro salvo com sucesso!")
                        else:
                            st.error("Não foi possível salvar o registro.")
            else:
                st.error("Não foi possível carregar os tipos, categorias ou status. Verifique o arquivo no repositório.")

        elif opcao == "Listar Registros":
            st.header("Registros Cadastrados")

            # Carrega os registros da aba "Base"
            df_registros = carregar_registros()

            if df_registros is not None and not df_registros.empty:
                # Exibe os registros em uma tabela
                st.dataframe(df_registros)
            else:
                st.info("Nenhum registro cadastrado.")

        elif opcao == "Baixar Planilha":
            st.header("Baixar Planilha")
            st.write("Clique no botão abaixo para baixar a planilha atualizada.")
            baixar_planilha()

# Executa o aplicativo
if __name__ == "__main__":
    main()
