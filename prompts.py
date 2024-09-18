from langchain.prompts import PromptTemplate
from output_parser import format_instructions_identificacion,output_parser_identificacion
from output_parser import format_instructions_lista,output_parser_lista

# Diseño del prompt para la segmentacion
segmentation_prompt = PromptTemplate(
    template='''
Quiero que actues como un auditor de conversaciones entre asesores y los clientes.
La siguiente es la conversación que vas a auditar:
"
Asesor: ¡Hola! ¿Cómo estas? Mi objetivo es ayudarte a solucionar tus consultas.
Cliente: {user_input}
"
Tu objetivo es identificar si existe una marca, producto o caracteristica de un marketplace de tecnologia.
Tu respuesta debe tener un máximo de 5 palabras.
{format_instructions}
''',
input_variables=['user_input'],
partial_variables={'format_instructions':format_instructions_identificacion},
output_parser=output_parser_identificacion
)

# Diseño del prompt para la confirmacion
Confirmation_prompt = PromptTemplate(
    template='''
Eres un asistente de un marketplace de tecnologia.
Debes realizar los siguientes pasos:
1. Debes verificar que {marca} si sea una marca de tecnologia y no de otra cosa.
2. Debes verificar que {elemento} sea en realidad un elemento de tecnologia.
3. Debes verificar que {caracteristicas} sean de un elemento de tecnologia.
{format_instructions}
''',
input_variables=['marca','elemento','caracteristicas'],
partial_variables={'format_instructions':format_instructions_identificacion},
output_parser=output_parser_identificacion
)

# Diseño del prompt para la eleccion del producto
eleccion_prompt = PromptTemplate(
    template='''
Eres un asistente de un marketplace de tecnologia.
Debes responder de forma amable la pregunta del cliente {user_input}
Debes confirmale al cliente que si se encontro el {elemento} y mostrarle/
una lista de las opciones como la que se encuentra entre <>
<1. {opcion1}
2. {opcion2}
3. {opcion3}>

Por ultimo preguntarle de forma amable que si no esta satisfecho con alguno de estos productos/
puede ser mas especifico con la busqueda de su producto.

La respuesta no puede ser mayor a 50 palabras.
{format_instructions}
''',
input_variables=['user_input','elemento','opcion1','opcion2','opcion3'],
partial_variables={'format_instructions':format_instructions_lista},
output_parser=output_parser_lista
)

# Diseño del prompt para la conversacion del producto
conversation_prompt = PromptTemplate(
    template='''
Eres un asistente del marketplace de tecnologia de Impresistem.

Si te realizan una pregunta debes responder de forma amable con la informacion que/
se encuentra entre <>

<Tu labor es guiar a los usuarios para que puedan encontrar el producto que necesitan.
Algunos de los productos de Impresistem son: Computadores, Tablets, mouse, teclados, /
audifonos, parlantes, microfonos entre otros articulos de tecnologia.>

Debes responder de forma amable la pregunta del cliente {user_input}

La respuesta no puede ser mayor a 50 palabras.
{format_instructions}
''',
input_variables=['user_input'],
partial_variables={'format_instructions':format_instructions_lista},
output_parser=output_parser_lista
)

# Diseño del prompt para la seleccion del producto
seleccion_prompt = PromptTemplate(
    template='''
Tienes que identificar de lo que dice el cliente {user_input} 
Cual de estas opciones el cliente esta seleccionando.

1.{opcion1}
2.{opcion2}
3.{opcion3}

Si el cliente indica otro tipo de elementos o caracteristicas de una nueva busqueda tu respuesta debe ser 'nuevo'
Si el cliente no indica con claridad que es alguna de estas opciones tu respuesta debe ser 'NAN'

{format_instructions}
''',
input_variables=['user_input','opcion1','opcion2','opcion3'],
partial_variables={'format_instructions':format_instructions_lista},
output_parser=output_parser_lista
)