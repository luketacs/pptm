import streamlit as st
import requests

# Definindo os cookies
cookies = {
    'PHPSESSID': '583c7cbd29247c95798c9ec2cdf349ee',  # Insira aqui o cookie PHPSESSID correto
}

# Função para consultar o produto com os cookies
def consultar_produto(codigo):
    url = f"https://utepecem.com.br/sigma/controller/insumo-controller.php/lerproduto?id={codigo}"
    
    # Fazendo a requisição com os cookies
    response = requests.get(url, cookies=cookies, verify=False)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para garantir que valores nulos sejam substituídos por 0
def tratar_valor(valor):
    if valor in [None, 'null', 'None']:
        return 0
    return valor

# Interface do aplicativo Streamlit
st.title("Consulta de Produtos")

# Campo para o código do produto
codigo = st.text_input("Digite o código do produto:", "")

# Botão de pesquisa
if st.button("Buscar Produto"):
    if codigo:
        produto = consultar_produto(codigo)
        
        if produto:
            st.success("Produto encontrado com sucesso!")
            
            # Exibindo as informações do produto de forma organizada
            st.subheader("Informações do Produto:")
            st.write(f"**Código do Produto:** {produto.get('id', 'N/A')}")
            st.write(f"**Nome do Produto:** {produto.get('texto_breve', 'N/A')}")
            st.write(f"**Texto Completo:** {produto.get('texto_completo', 'N/A')}")
            st.write(f"**Unidade de Medida:** {produto.get('unidade', 'N/A')}")
            
            # Tratando os casos em que 'estoque_atual' e 'estoque_seguranca' podem ser nulos ou ausentes
            estoque_atual = tratar_valor(produto.get('estoque_atual'))
            estoque_seguranca = tratar_valor(produto.get('estoque_seguranca'))

            st.write(f"**Estoque Disponível:** {estoque_atual}")
            st.write(f"**Estoque de Segurança:** {estoque_seguranca}")
            
        else:
            st.error("Produto não encontrado ou erro na consulta.")
    else:
        st.warning("Por favor, insira um código válido.")