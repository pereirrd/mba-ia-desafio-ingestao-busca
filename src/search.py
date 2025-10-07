import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

# Configurações
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

def create_vector_store():
    """Cria o store PGVector para busca"""
    try:
        # Embeddings OpenAI
        embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

        store = PGVector(
            embeddings=embeddings,
            collection_name=PGVECTOR_COLLECTION,
            connection=PGVECTOR_URL,
            use_jsonb=True,
        )
        
        return store
    except Exception as e:
        return None

def search_prompt(question=None):
    """Função principal para busca e geração de resposta"""
    if not question:
        return "Por favor, forneça uma pergunta."
    
    try:
        # Criar store PGVector
        store = create_vector_store()
        if not store:
            return "Erro ao conectar com o banco de dados vetorial."
        
        # Realizar busca por similaridade
        search_results = store.similarity_search_with_score(question, k=10)
        
        if not search_results:
            return "Não encontrei informações relevantes para sua pergunta."
        
        # Extrair contexto dos resultados
        context_parts = []
        for doc, score in search_results:
            context_parts.append(doc.page_content)
        
        contexto = "\n\n".join(context_parts)
        
        # Criar prompt com contexto
        prompt = PromptTemplate(
            input_variables=["contexto", "pergunta"],
            template=PROMPT_TEMPLATE
        )
        
        # Formatar prompt final
        formatted_prompt = prompt.format(contexto=contexto, pergunta=question)
        
        return formatted_prompt
        
    except Exception as e:
        return f"Erro ao processar sua pergunta: {e}"
