import streamlit as st 
import pandas as pd  
import requests

BASE_URL = "http://127.0.0.1:5000"

def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params)

        elif method == "POST":
            response = requests.post(url, json=data)

        elif method == "PUT":
            response = requests.put(url, json=data)

        elif method == "DELETE":
            response = requests.delete(url, params=params)

        else:
            st.error("Método HTTP não suportado.")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")

        return None

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        return None

def usuario(metodo, id, nome, cpf, nasc):
    if metodo == 'C':
        dados = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': nasc
        }

        result = fazer_requisicao('/usuarios', method='POST', data=dados)
        if result == None:
            return
        if 'id' in result:
            st.write(result['id'])
        else:
            st.write(result['erro'])
    
    if metodo == 'R':
        result = fazer_requisicao('/usuarios', method='GET')
        if result == None:
            return
        st.write(result['usuarios'])
    
    if metodo == 'R1':
        result = fazer_requisicao(f'/usuarios/{id}', method='GET')
        if result == None:
            return
        if 'usuario' in result:
            st.write(result['usuario'])
        elif 'usuarios' in result:
            st.write(result['usuarios'])
        else:
            st.write(result['erro'])
    
    if metodo == 'U':
        dados = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': nasc
        }

        result = fazer_requisicao(f'/usuarios/{id}', method='PUT', data=dados)
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['sucesso'])
    
    if metodo == 'D':
        result = fazer_requisicao(f'/usuarios/{id}', method='DELETE')
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['sucesso'])

def bikes(metodo, id, marca, modelo, cidade):
    if metodo == 'C':
        dados = {
            'marca': marca,
            'modelo': modelo,
            'cidade_alocada': cidade
        }

        result = fazer_requisicao('/bikes', method='POST', data=dados)
        if result == None:
            return
        if 'id' in result:
            st.write(result['id'])
        else:
            st.write(result['erro'])
    
    if metodo == 'R':
        result = fazer_requisicao('/bikes', method='GET')
        if result == None:
            return
        st.write(result['bicicletas'])
    
    if metodo == 'R1':
        result = fazer_requisicao(f'/bikes/{id}', method='GET')
        if result == None:
            return
        if 'bicicleta' in result:
            st.write(result['bicicleta'])
        elif 'bicicletas' in result:
            st.write(result['bicicletas'])
        else:
            st.write(result['erro'])
    
    if metodo == 'U':
        dados = {
            'marca': marca,
            'modelo': modelo,
            'cidade_alocada': cidade
        }

        result = fazer_requisicao(f'/bikes/{id}', method='PUT', data=dados)
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['sucesso'])
    
    if metodo == 'D':
        result = fazer_requisicao(f'/bikes/{id}', method='DELETE')
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['sucesso'])


def emprestimo(metodo, id, id_usuario, id_bike, data_alugada):
    if metodo == 'C':
        dados = {
            'data_alugada': data_alugada
        }

        result = fazer_requisicao(f'/emprestimos/usuarios/{id_usuario}/bikes/{id_bike}', method='POST', data=dados)
        if result == None:
            return
        if 'id' in result:
            st.write(result['id'])
        else:
            st.write(result['erro'])
    
    if metodo == 'R':
        result = fazer_requisicao('/emprestimos', method='GET')
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['emprestimos'])
    
    if metodo == 'D':
        result = fazer_requisicao(f'/emprestimos/{id}', method='DELETE')
        if result == None:
            return
        if 'erro' in result:
            st.write(result['erro'])
        else:
            st.write(result['sucesso'])


st.title("Aluguel de Bicicletas")
st.subheader("Hora de alugar uma bicicleta!")

st.sidebar.header('Filtros')

tipo_pesquisa = st.sidebar.selectbox(
    'Tipo', [
        'Usuário',
        'Bicicleta',
        'Empréstimo'
    ], placeholder='Escolha o seu filtro...', index=None
)

if tipo_pesquisa == 'Usuário':
    metodo = st.sidebar.selectbox(
        'Ação', [
            'Criar usuário',
            'Ver lista de usuários',
            'Buscar usuário',
            'Atualizar usuário',
            'Deletar usuário'
        ], placeholder='Escolha o seu filtro...', index=None
    )

    if metodo == 'Criar usuário':
        nome = st.sidebar.text_input('Nome:')
        cpf = st.sidebar.text_input('CPF:')
        nasc = st.sidebar.text_input('Data de nascimento:')
        btn = st.sidebar.button('Criar usuário')
        if btn:
            usuario('C', 0, nome, cpf, nasc)

    elif metodo == 'Ver lista de usuários':
        btn = st.sidebar.button('Buscar')
        if btn:
            usuario('R', 0, 0, 0, 0)

    
    elif metodo == 'Buscar usuário':
        id = st.sidebar.text_input('ID:')
        btn = st.sidebar.button('Buscar usuário')
        if btn:
            usuario('R1', id, 0, 0, 0)
    
    elif metodo == 'Atualizar usuário':
        id = st.sidebar.text_input('ID:')
        nome = st.sidebar.text_input('Nome:')
        cpf = st.sidebar.text_input('CPF:')
        nasc = st.sidebar.text_input('Data de nascimento:')
        btn = st.sidebar.button('Atualizar usuário')
        if btn:
            usuario('U', id, nome, cpf, nasc)
    
    elif metodo == 'Deletar usuário':
        id = st.sidebar.text_input('ID:')
        btn = st.sidebar.button('Deletar usuário')
        if btn:
            usuario('D', id, 0, 0, 0)


if tipo_pesquisa == 'Bicicleta':
    metodo = st.sidebar.selectbox(
        'Ação', [
            'Criar bicicleta',
            'Ver lista de bicicletas',
            'Buscar bicicleta',
            'Atualizar bicicleta',
            'Deletar bicicleta'
        ], placeholder='Escolha o seu filtro...', index=None
    )

    if metodo == 'Criar bicicleta':
        marca = st.sidebar.text_input('Marca:')
        modelo = st.sidebar.text_input('Modelo:')
        cidade = st.sidebar.text_input('Cidade alocada:')
        btn = st.sidebar.button('Criar bicicleta')
        if btn:
            bikes('C', 0, marca, modelo, cidade)

    elif metodo == 'Ver lista de bicicletas':
        btn = st.sidebar.button('Buscar')
        if btn:
            bikes('R', 0, 0, 0, 0)
    
    elif metodo == 'Buscar bicicleta':
        id = st.sidebar.text_input('ID:')
        btn = st.sidebar.button('Buscar bicicleta')
        if btn:
            bikes('R1', id, 0, 0, 0)
    
    elif metodo == 'Atualizar bicicleta':
        id = st.sidebar.text_input('ID:')
        marca = st.sidebar.text_input('Marca:')
        modelo = st.sidebar.text_input('Modelo:')
        cidade = st.sidebar.text_input('Cidade alocada:')
        btn = st.sidebar.button('Atualizar bicicleta')
        if btn:
            bikes('U', id, marca, modelo, cidade)
    
    elif metodo == 'Deletar bicicleta':
        id = st.sidebar.text_input('ID:')
        btn = st.sidebar.button('Deletar bicicleta')
        if btn:
            bikes('D', id, 0, 0, 0)


if tipo_pesquisa == 'Empréstimo':

    metodo = metodo = st.sidebar.selectbox(
        'Ação', [
            'Criar empréstimo',
            'Ver lista de empréstimos',
            'Deletar empréstimo'
        ], placeholder='Escolha o seu filtro...', index=None
    )

    if metodo == 'Criar empréstimo':
        id_usuario = st.sidebar.text_input('ID do usuário:')
        id_bike = st.sidebar.text_input('ID da bicicleta:')
        data_alugada = st.sidebar.text_input('Data do aluguel:')
        btn = st.sidebar.button('Criar empréstimo')
        if btn:
            emprestimo('C', 0, id_usuario, id_bike, data_alugada)
    
    elif metodo == 'Ver lista de empréstimos':
        btn = st.sidebar.button('Buscar')
        if btn:
            emprestimo('R', 0, 0, 0, 0)
    
    elif metodo == 'Deletar empréstimo':
        id_emprestimo = st.sidebar.text_input('ID do empréstimo:')
        btn = st.sidebar.button('Deletar empréstimo')
        if btn:
            emprestimo('D', id_emprestimo, 0, 0, 0)
