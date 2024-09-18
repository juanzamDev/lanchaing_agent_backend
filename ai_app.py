import numpy as np
import os
from numpy.linalg import norm
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from prompts import segmentation_prompt,Confirmation_prompt,eleccion_prompt,conversation_prompt,seleccion_prompt
from config import OPENAI_KEY
from output_parser import output_parser_identificacion,output_parser_lista
import pandas as pd

# Variables de entorno
os.environ['OPENAI_API_KEY'] = OPENAI_KEY
os.environ['OPENAI_API_BASE'] = "https://impresistem-develop.openai.azure.com/"
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = '2023-07-01-preview'

# Variables de implementaciones
gpt4_deploy = 'impresistem-alix-gpt4-develop'
ada02_deploy = 'impresistem-alix-ada-002'
gpt35_deploy = 'impresistem-alix-develop'

# Definicion de modelos
llm = AzureChatOpenAI(deployment_name=gpt35_deploy, temperature=0, request_timeout=100, max_tokens=800,)
embeddings = AzureOpenAIEmbeddings(deployment=ada02_deploy)

# Base de productos basica
df_grupos = pd.read_csv("tratamiento base/list_embeddings_grupos.csv")
# Base de productos compleja
df_especifico = pd.read_csv("tratamiento base/list_embeddings_productos_prueba.csv")


def segmentacion(user_input: str=None, model: AzureChatOpenAI=None, prompt_a: PromptTemplate=None) -> dict:
    decision_chain = LLMChain(llm=model, prompt=prompt_a)
    response = decision_chain.run({'user_input': user_input})
    parser_response = output_parser_identificacion.parse(response)
    return parser_response

def confirmacion(marca: str=None,elemento: str=None,caracteristicas: str=None, model: AzureChatOpenAI=None, prompt_b: PromptTemplate=None) -> dict:
    decision_chain = LLMChain(llm=model, prompt=prompt_b)
    response = decision_chain.run({'marca': marca,'elemento':elemento,'caracteristicas':caracteristicas})
    
    parser_response = output_parser_identificacion.parse(response)
    if parser_response['marca'] == 'None':
        parser_response['marca'] = None
    if parser_response['elemento'] == 'None':
        parser_response['elemento'] = None
    if parser_response['caracteristicas'] == 'None':
        parser_response['caracteristicas'] = None
    return parser_response

def similaridad_coseno(A,B):
    similarity = np.dot(A,B)/(norm(A)*norm(B))
    return similarity

def text_to_list(str_embedding):
    list_embedding = eval(str_embedding)
    return list_embedding

def obtener_embedding(texto):
    embedded_query = embeddings.embed_query(texto)
    return embedded_query

def busqueda_producto_basica(entrada: dict=None,base: pd=None):
    base['embedding'] = base['embedding'].apply(text_to_list)

    if entrada['elemento'] == None:
        pass
    else:
        text_embedded = obtener_embedding(entrada['elemento'])

        similaridades = np.dot(base['embedding'].tolist(), text_embedded) / (
            np.linalg.norm(base['embedding'].tolist(), axis=1) * np.linalg.norm(text_embedded)
        )

        base['similitud_cosine'] = similaridades
        df_sorted = base.sort_values(by='similitud_cosine', ascending=False)

        if df_sorted['similitud_cosine'].iloc[0] > 0.865:
            print(df_sorted.head(3))
            print("################################### SI se encuentran en las categorias")
            entrada['elemento'] = entrada['elemento']
        else:
            print("################################### NO se encuentran en las categorias")
            entrada['elemento'] = None

    return entrada


def busqueda_producto_compleja(entrada: dict=None,base: pd=None):
    base['embedding'] = base['embedding'].apply(text_to_list)
    op = []
    if entrada['elemento']  == None and entrada['marca']  == None and entrada['caracteristicas']  == None:
        conversation = True
    else:
        if entrada['marca'] == None:
            entrada['marca'] = ""
        if entrada['elemento'] == None:
            entrada['elemento'] = ""
        if entrada['caracteristicas'] == None:
            entrada['caracteristicas'] = ""
        text = entrada['marca'] +" "+ entrada['elemento'] +" "+ entrada['caracteristicas']
        text_embedded = obtener_embedding(text)

        similaridades = np.dot(base['embedding'].tolist(), text_embedded) / (
            np.linalg.norm(base['embedding'].tolist(), axis=1) * np.linalg.norm(text_embedded)
        )

        base['similitud_cosine'] = similaridades
        df_sorted = base.sort_values(by='similitud_cosine', ascending=False)
        if df_sorted['similitud_cosine'].iloc[0] > 0.80:
            print(df_sorted[['TEX_MATERIAL','similitud_cosine']].head(3))
            print("################################### SI se encuentran prodcutos")
            op.append(df_sorted['text'].iloc[0])
            op.append(df_sorted['text'].iloc[1])
            op.append(df_sorted['text'].iloc[2])
            conversation = False
        else:
            print("################################### NO se encuentran prodcutos")
            op = []
            conversation = True

    return conversation,op

def respuesta_lista(user_input: str=None, model: AzureChatOpenAI=None, prompt_c: PromptTemplate=None, opciones: list = None,elemento: str = None) -> dict:
    decision_chain = LLMChain(llm=model, prompt=prompt_c)
    response = decision_chain.run({'user_input': user_input,'elemento':elemento,'opcion1': opciones[0],'opcion2': opciones[1],'opcion3': opciones[2]})
    parser_response = output_parser_lista.parse(response)
    return parser_response

def respuesta_conversacion(user_input: str=None, model: AzureChatOpenAI=None, prompt_d: PromptTemplate=None) -> dict:
    decision_chain = LLMChain(llm=model, prompt=prompt_d)
    response = decision_chain.run({'user_input': user_input})
    parser_response = output_parser_lista.parse(response)
    return parser_response

def respuesta_seleccion(user_input: str=None, model: AzureChatOpenAI=None, prompt_e: PromptTemplate=None,opciones: list = None) -> dict:
    decision_chain = LLMChain(llm=model, prompt=prompt_e)
    response = decision_chain.run({'user_input': user_input,'opcion1': opciones[0],'opcion2': opciones[1],'opcion3': opciones[2]})
    parser_response = output_parser_lista.parse(response)
    return parser_response



def chat_assistant(user_input: str=None):
    answer_segementacion = segmentacion(user_input=user_input,model=llm,prompt_a=segmentation_prompt)
    print("######## Asi entrega los resultados de segmentar ###########")
    print(answer_segementacion)
    answer_busqueda = busqueda_producto_basica(entrada=answer_segementacion ,base = df_grupos)
    conversation,answer_busqueda_compleja = busqueda_producto_compleja(entrada=answer_busqueda,base = df_especifico)
    if conversation:
        answer_conversacion = respuesta_conversacion(user_input = user_input, model = llm, prompt_d = conversation_prompt)
        print(answer_conversacion['answer'])
    else:
        answer_lista = respuesta_lista(user_input = user_input ,model = llm, prompt_c = eleccion_prompt, opciones = answer_busqueda_compleja, elemento = answer_busqueda['elemento'])
        #answer_seleccion = respuesta_seleccion(user_input="no quiero ninguna de estas",prompt_e=seleccion_prompt,opciones=answer_busqueda_compleja)
        #print(answer_seleccion['answer'])
        print(answer_lista['answer'])

chat_assistant(user_input="hola necesito un teclado")