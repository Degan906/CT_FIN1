import streamlit as st
import pandas as pd

# Função para carregar os dados do Excel via URL
def carregar_dados_login():
    # URL "raw" do arquivo no GitHub
    url = "https://raw.githubusercontent.com/Degan906/CT_FIN1/main/FIN_TC1.xls"
    try:
        # Tenta carregar a planilha Excel e acessar a aba "Login"
        df = pd.read_excel(url, sheet_name="Login")
        return df
    except Exception as e:
        # Exibe mensagens de erro específicas
        if "HTTP Error 404" in str(e):
            st.error("Erro: O arquivo não foi encontrado no GitHub. Verifique a URL e a visibilidade do repositório.")
        else:
            st.error(f"Erro ao carregar o arquivo Excel: {e}")
        return None

# Função para verificar login
def verificar_login(usuario, senha, df):
    if df is not None:
        # Filtra o DataFrame para encontrar o usuário e senha correspondentes
        filtro = (df["Usuário"] == usuario) & (df["Senha"] == senha)
        resultado = df[filtro]
        return not resultado.empty
    return False

# Função principal do Streamlit
def main():
    st.title("Sistema de Login")

    # Carrega os dados do Excel
    df_login = carregar_dados_login()

    # Campos de entrada para o login
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    # Botão de login
    if st.button("Entrar"):
        if verificar_login(usuario, senha, df_login):
            st.success("Login realizado com sucesso!")
            # Aqui você pode redirecionar para outra página ou exibir mais opções
        else:
            st.error("Usuário ou senha inválidos.")

# Executa o aplicativo
if __name__ == "__main__":
    main()
