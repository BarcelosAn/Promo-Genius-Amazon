from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate


# Configuração da IA
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key='AIzaSyBvJ4fkQsc6vaZXrs1NMisX98sSVzdtAdo', temperature=0,)

# Prompt
prompt_template = """
Retorne apenas um produto especifico que tem haver com a pergunta. Um produto que realmente poderia ter em alguma loja para pesquisar

exemplo de pergunta: Queria algo para deixar o minha cozinha organizada.

exeplo de resoposta: Organizador de faca

Pergunta:
{text}
"""

# Configuração do template do Langchain
chat_template = ChatPromptTemplate.from_template(prompt_template)

def generate_html_response(question):
    prompt_engineered = chat_template.format_messages(
        text=question
    )
    
    response = llm.invoke(prompt_engineered)
    return response.content

#generate_html_response(input('o que deseja procurar?\n'))
