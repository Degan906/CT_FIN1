import streamlit as st

# Dados de login (usuário e senha)
credenciais = {
    "henrique.degan": "12345",
    "vanessa.degan": "12345"
}

# Função para verificar login
def verificar_login(usuario, senha):
    # Verifica se o usuário existe e a senha está correta
    if usuario in credenciais and credenciais[usuario] == senha:
        return True
    return False

# Função principal do Streamlit
def main():
    st.title("Sistema de Login")

    # Campos de entrada para o login
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    # Botão de login
    if st.button("Entrar"):
        if verificar_login(usuario, senha):
            st.success("Login realizado com sucesso!")
            # Aqui você pode redirecionar para outra página ou exibir mais opções
        else:
            st.error("Usuário ou senha inválidos.")

# Executa o aplicativo
if __name__ == "__main__":
    main()
