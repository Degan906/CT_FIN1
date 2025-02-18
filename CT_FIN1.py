import streamlit as st
import pandas as pd
from openpyxl import load_workbook

# Dados de login (usuário e senha)
credenciais = {
    "henrique.degan": "12345",
    "vanessa.degan": "12345"
}

# Função para carregar os tipos de receita do Excel via URL
def carregar_tipos_receita():
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xlsx"
    try:
        # Carrega a planilha Excel e acessa a aba "Tipo"
        df = pd.read_excel(url, sheet_name="Tipo", engine="openpyxl")
        return df["Tipo"].tolist()  # Retorna os tipos como uma lista
    except Exception as e:
        st.error(f"Erro ao carregar os tipos de receita: {e}")
        return []

# Função para registrar uma nova receita na aba "Base"
def registrar_receita(resumo, tipo):
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
        sheet.cell(row=proxima_linha, column=1, value=resumo)  # Coluna 1: Resumo
        sheet.cell(row=proxima_linha, column=2, value=tipo)    # Coluna 2: Tipo
        
        # Salva o arquivo Excel
        workbook.save(arquivo_excel)
        return True
    except Exception as e:
        st.error(f"Erro ao registrar a receita: {e}")
        return False

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
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Início", "Criar Receitas"])

        if opcao == "Início":
            st.write("Bem-vindo à tela inicial!")
            st.write("Use o menu lateral para navegar.")

        elif opcao == "Criar Receitas":
            st.header("Criar Nova Receita")

            # Carrega os tipos de receita do Excel
            tipos = carregar_tipos_receita()

            if tipos:
                resumo = st.text_input("Resumo da Receita")
                tipo = st.selectbox("Tipo de Receita", tipos)

                if st.button("Salvar Receita"):
                    if resumo.strip() == "":
                        st.error("O campo 'Resumo' é obrigatório.")
                    else:
                        # Registra a receita na aba "Base"
                        if registrar_receita(resumo, tipo):
                            st.success(f"Receita salva com sucesso!\nResumo: {resumo}\nTipo: {tipo}")
                        else:
                            st.error("Não foi possível salvar a receita.")
            else:
                st.error("Não foi possível carregar os tipos de receita. Verifique o arquivo no repositório.")

# Executa o aplicativo
if __name__ == "__main__":
    main()
