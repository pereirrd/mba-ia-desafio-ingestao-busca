import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_prompt

load_dotenv()

# Configurações do LLM
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def generate_response_with_llm(question):
    """Gera resposta final usando OpenAI LLM"""
    if not question:
        return "Por favor, forneça uma pergunta."
    
    try:
        # Buscar contexto e formatar prompt
        formatted_prompt = search_prompt(question)
        
        # Verificar se houve erro na busca
        if "Erro ao" in formatted_prompt or "Não encontrei informações" in formatted_prompt:
            return formatted_prompt
        
        # Criar instância do LLM
        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)
        
        # Gerar resposta
        response = llm.invoke(formatted_prompt)
        
        return response.content
        
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

def interactive_chat():
    """Chat interativo para testar a busca"""
    print("=== Chat Interativo - Busca Vetorial ===")
    print("Digite sua pergunta (ou 'sair' para encerrar):\n")
    
    while True:
        user_input = input("Você: ").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando chat...")
            break
            
        if not user_input:
            print("Por favor, digite uma pergunta.")
            continue
            
        print("\nProcessando...")
        response = generate_response_with_llm(user_input)
        print(f"\nResposta: {response}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    interactive_chat()