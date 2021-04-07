import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

# função para carregar o dataset
@st.cache
def get_data():
    return pd.read_csv("train.csv")

# função para treinar o modelo
def train_model():
    data = get_data()
    x = data.drop("fake",axis=1)
    y = data["fake"]
    rf_regressor = RandomForestClassifier()
    rf_regressor.fit(x, y)
    return rf_regressor

# criando um dataframe
data = get_data()

# treinando o modelo
model = train_model()

# título
st.title("Data App - Prevendo perfis fakes no Instagram")

# subtítulo
st.markdown("Este é um Data App utilizado para exibir a solução de Machine Learning para o problema de predição de perfis fakes no Instagram.")

# verificando o dataset
st.subheader("Selecionando apenas um pequeno conjunto de atributos")

# atributos para serem exibidos por padrão
defaultcols = ["profile pic","nums/length username","fullname words","nums/length fullname","name==username"]

# defindo atributos a partir do multiselect
cols = st.multiselect("Features", data.columns.tolist(), default=defaultcols)

# exibindo os top 10 registro do dataframe
st.dataframe(data[cols])


## Barra Lateral
st.sidebar.subheader("Defina as características do perfil para previsão")

# mapeando dados do usuário para cada atributo
pic = st.sidebar.selectbox("Tem foto de perfil?",("Sim","Não"))
# transformando o dado de entrada em valor binário
pic = 1 if pic == "Sim" else 0

private = st.sidebar.selectbox("O perfil é Privado?",("Sim","Não"))
private = 1 if private == "Sim" else 0

seguidores = st.sidebar.number_input("Qual o número de seguidores que o perfil tem?",value=100)
segue = st.sidebar.number_input("Qual o número de pessoas que o perfil segue?",value=100)
posts = st.sidebar.number_input("Qual o número de publicações que o perfil já fez??",value=10)



nome_do_usuario = st.sidebar.text_input('Digite o nome do usuário:')
nome_do_usuario = nome_do_usuario.lower()

nome_real_cadastrado = st.sidebar.text_input('Digite o Nome real cadastrado:')
nome_real_cadastrado = nome_real_cadastrado.lower()

bio = st.sidebar.text_input('Digite a "Bio"(descrição) do instagram do usuário:')
bio = bio.lower()




# inserindo um botão na tela
btn_load = st.sidebar.button("Fazer previsão")

nums_lenght_username,fulname_words,num_lenght_fullname,name_username,description_length,external_url,result = 0,0,0,0,0,0,0
# verifica se o botão foi acionado
if btn_load:

    # calculando a variável "nums/lenght username"
    numeros = sum(c.isdigit() for c in nome_do_usuario)
    letras = sum(c.isalpha() for c in nome_do_usuario)
    espacos = sum(c.isspace() for c in nome_do_usuario)

    if numeros == 0:
        nums_lenght_username= 0
    else:
        nums_lenght_username = numeros / (letras + espacos + numeros)

    # calculando a variável "fulname words"
    fulname_words = len(nome_do_usuario.split())

    # calculando a variável "num/lenght fullname"
    numeros_nome = sum(c.isdigit() for c in nome_real_cadastrado)
    letras_nome = sum(c.isalpha() for c in nome_real_cadastrado)
    espacos_nome = sum(c.isspace() for c in nome_real_cadastrado)

    if numeros_nome == 0 :
        num_lenght_fullname = 0
    else:
        num_lenght_fullname = numeros_nome / len(nome_real_cadastrado.split())


    # Verificando a variável "name==username"
    if nome_do_usuario == nome_real_cadastrado:
        name_username = 1
    else:
        name_username = 0


    # calculando a variável "description_length"
    description_length = len(list(bio.replace(" ",'')))

    # verificanddo a variável "external URL"
    if ("https://" in bio) or ("http://" in bio):
        external_url = 1
    else:
        external_url = 0


    result = model.predict([[pic,nums_lenght_username,fulname_words,num_lenght_fullname,name_username,
                                     description_length,external_url,private,posts,seguidores,segue]])
    result = result[0]

    st.subheader("Este perfil...")
    if result == 1:
        st.write("É Fake!")
    else:
        st.write("Não é Fake!")
