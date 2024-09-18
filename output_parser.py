from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

##################### Salida para identificar marca, elemento, caracteristicas ########################

marca_schema = ResponseSchema(name="marca",
                              description="esta es la marca del elemento sobre el cual se esta realizando la busqueda")

elemento_schema = ResponseSchema(name="elemento",
                              description="este es el elemento que el usuario esta buscando")

caracteristicas_schema = ResponseSchema(name="caracteristicas",
                              description="estas son las caracteristicas especificas del elemento")

response_schemas_identificacion = [marca_schema,elemento_schema,caracteristicas_schema]

output_parser_identificacion = StructuredOutputParser.from_response_schemas(response_schemas_identificacion)

format_instructions_identificacion = output_parser_identificacion.get_format_instructions()

############################### Salida para respuesta de una sola variable#######################

lista_schema = ResponseSchema(name="answer",
                              description="esta es la respuesta de forma amable de la lista")

response_schemas_lista = [lista_schema]

output_parser_lista = StructuredOutputParser.from_response_schemas(response_schemas_lista)

format_instructions_lista = output_parser_lista.get_format_instructions()


