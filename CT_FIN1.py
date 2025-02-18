import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO

# Dados de login (usuário e senha)
credenciais = {
    "henrique.degan": "12345",
    "vanessa.degan": "12345"
}

# Função para carregar os tipos de categoria do Excel via URL
def carregar_categorias():
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xlsx"
    try:
        # Carrega a planilha Excel e acessa a aba "Tipo"
        df = pd.read_excel(url, sheet_name="Tipo", engine="openpyxl")
        return df["Tipo"].tolist()  # Retorna os tipos como uma lista
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

# Função para registrar um novo registro na aba "Base"
def registrar_registro(categoria, data_pagamento, valor, tag, status):
    # Caminho para o arquivo Excel
    arquivo_excel = "FIN_TC1.xlsx"
    
    try:
        # Carrega o arquivo Excel existente
        workbook = load_workbook(arquivo_excel)
        
        # Acessa a aba "Base"
        if "Base" not in workbook.sheetnames:
            st.error("A aba 'Base' não foi encontrada no arquivo Excel.")
            return False
        
        sheet = workbook["Base"]
        
        # Encontra a próxima linha vazia
        proxima_linha = sheet.max_row + 1
        
        # Adiciona os dados na próxima linha
        sheet.cell(row=proxima_linha, column=1, value=categoria)         # Coluna 1: Categoria
        sheet.cell(row=proxima_linha, column=2, value=data_pagamento)   # Coluna 2: Data de Pagamento
        sheet.cell(row=proxima_linha, column=3, value=valor)            # Coluna 3: Valor (R$)
        sheet.cell(row=proxima_linha, column=4, value=tag)              # Coluna 4: Tag
        sheet.cell(row=proxima_linha, column=5, value=status)           # Coluna 5: Status
        
        # Salva o arquivo Excel
        workbook.save(arquivo_excel)
        return True
    except Exception as e:
        st.error(f"Erro ao registrar o registro: {e}")
        return False

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

# Função para baixar a planilha
def baixar_planilha():
    # Caminho para o arquivo Excel
    arquivo_excel = "FIN_TC1.xlsx"
    
    try:
        # Lê o arquivo Excel como bytes
        with open(arquivo_excel, "rb") as f:
            bytes_data = f.read()
        
        # Cria um botão de download
        st.download_button(
            label="Baixar Planilha",
            data=bytes_data,
            file_name="FIN_TC1.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.error("Erro: O arquivo 'FIN_TC1.xlsx' não foi encontrado.")

# Função para verificar login
def verificar_login(usuario, senha):
    if usuario in credenciais and credenciais[usuario] == senha:
        return True
    return False

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
            st.write("Bem-vindo à tela inicial!")
            st.write("Use o menu lateral para navegar.")

        elif opcao == "Criar Registro":
            st.header("Criar Novo Registro")

            # Carrega as categorias e status do Excel
            categorias = carregar_categorias()
            status_list = carregar_status()

            if categorias and status_list:
                categoria = st.selectbox("Categoria", categorias)
                data_pagamento = st.date_input("Data de Pagamento")
                valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
                tag = st.text_input("Tag (Label)")
                status = st.selectbox("Status", status_list)

                if st.button("Salvar Registro"):
                    if not categoria or not data_pagamento or not valor or not status:
                        st.error("Todos os campos obrigatórios devem ser preenchidos.")
                    else:
                        # Registra o registro na aba "Base"
                        if registrar_registro(categoria, data_pagamento, valor, tag, status):
                            st.success("Registro salvo com sucesso!")
                        else:
                            st.error("Não foi possível salvar o registro.")
            else:
                st.error("Não foi possível carregar as categorias ou status. Verifique o arquivo no repositório.")

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
