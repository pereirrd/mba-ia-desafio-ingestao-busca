# Sistema de Ingestão e Busca com RAG

Este projeto implementa um sistema completo de RAG (Retrieval-Augmented Generation) que processa PDFs, cria embeddings e armazena no PostgreSQL com pgVector usando LangChain.

## 🛠️ Configuração

### 1. Dependências
```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar dependências adicionais
pip install langchain-openai langchain-postgres psycopg[binary] psycopg-pool
```

### 2. Banco de Dados
```bash
# Iniciar PostgreSQL com pgVector
docker-compose up -d

# Verificar se está rodando
docker ps
```

### 3. Variáveis de Ambiente
Configure o arquivo `.env` com as configurações necessárias:
```env
# PDF Configuration
PDF_PATH=/caminho/para/seu/documento.pdf

# PGVector Configuration
PGVECTOR_COLLECTION=document_embeddings
PGVECTOR_URL=postgresql://postgres:postgres@localhost:5432/rag

# OpenAI Configuration (necessária para embeddings e LLM)
OPENAI_API_KEY=sua_chave_api_openai_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_MODEL=gpt-3.5-turbo
```

### 4. Estrutura do Banco de Dados

```sql
CREATE TABLE document_embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Testando o Sistema de Busca

#### Primeiro, execute a ingestão:
```bash
python src/ingest.py
```

#### Depois, teste a busca:
```bash
python src/chat.py
```

#### Exemplo de saída esperada:
```
=== Chat Interativo - Busca Vetorial ===
Digite sua pergunta (ou 'sair' para encerrar):

Você: Qual é o conteúdo do documento?

Processando...

Resposta: Com base no contexto fornecido, o documento contém informações sobre [resposta gerada pelo LLM baseada no conteúdo encontrado nos documentos].

==================================================

Você: sair
Encerrando chat...
```

---

## 📄 ingest.py - Sistema de Ingestão de Documentos

### 🚀 Funcionalidades Implementadas

✅ **Tarefas Concluídas:**
1. **PDF dividido em chunks** - Chunks de 1000 caracteres com overlap de 150
2. **Cada chunk convertido em embedding** - Usando OpenAI text-embedding-3-small
3. **Vetores armazenados no PostgreSQL** - Com pgVector usando LangChain PGVector

### 📈 Pipeline de Processamento

1. **Carregamento**: PDF é carregado usando PyPDFLoader
2. **Chunking**: Texto dividido em chunks de 1000 caracteres (overlap 150)
3. **Enriquecimento**: Documentos enriquecidos com metadados e IDs únicos
4. **Embedding**: Cada chunk convertido em vetor usando OpenAI
5. **Armazenamento**: Vetores salvos no PostgreSQL usando LangChain PGVector

### 🏃‍♂️ Como Executar

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar o pipeline de ingestão
python src/ingest.py
```

### 📝 Logs de Execução

O sistema fornece logs detalhados de cada etapa:
- Número de chunks processados
- Documentos enriquecidos com IDs únicos
- Status de criação do store PGVector
- Armazenamento dos embeddings

**Exemplo de Execução:**
```
Processando 67 chunks...

1. Criando store PGVector...
Store PGVector criado com sucesso!

2. Enriqueceendo documentos...
Documento enriquecido: Nome da empresa Faturamento Ano de fundação... (ID: 4bf7fefa-b3b2-4cde-8059-c26ede6198ec)
Documentos enriquecidos: 67

3. Adicionando documentos ao store...
✅ 67 documentos armazenados com sucesso!

✅ Pipeline de ingestão concluído com sucesso!
📊 Dados armazenados no PostgreSQL com pgVector usando LangChain
```

---

## 🔍 search.py - Sistema de Busca Semântica

### 🎯 Funcionalidades Implementadas
- ✅ **Busca semântica nos embeddings armazenados** - Usando PGVector com similarity_search_with_score
- ✅ **Retrieval de documentos relevantes** - Baseado na pergunta do usuário
- ✅ **Separação de responsabilidades** - Busca em search.py, LLM em chat.py
- ✅ **Configuração automática do store PGVector** - Conexão com PostgreSQL
- ✅ **Template de prompt estruturado** - Para respostas baseadas em contexto
- ✅ **Tratamento de erros robusto** - Fallbacks sem logs desnecessários
- ✅ **Interface limpa** - Apenas prints essenciais para navegação

### 🏃‍♂️ Como Usar

#### Função de Busca: `search_prompt(question)`
```python
from search import search_prompt

# Buscar contexto e formatar prompt
formatted_prompt = search_prompt("Qual é o conteúdo do documento?")
print(formatted_prompt)  # Prompt formatado pronto para LLM
```

#### Função de Resposta: `generate_response_with_llm(question)`
```python
from chat import generate_response_with_llm

# Buscar contexto e gerar resposta final com LLM
resposta = generate_response_with_llm("Qual é o conteúdo do documento?")
print(resposta)  # Resposta final formatada
```

#### Exemplo de uso no chat:
```python
# No chat interativo, a função já está integrada
from chat import interactive_chat
interactive_chat()
```

### 📊 Características Técnicas
- **Embeddings**: OpenAI text-embedding-3-small
- **Busca**: PGVector similarity_search_with_score
- **Configuração**: Variáveis de ambiente (PGVECTOR_URL, PGVECTOR_COLLECTION)
- **Retorno**: Prompt formatado pronto para LLM
- **Responsabilidade**: Apenas busca e formatação de contexto

---

## 💬 chat.py - Interface de Chat RAG

### 🎯 Funcionalidades Implementadas
- ✅ **Chat interativo completo** - Para testes em tempo real
- ✅ **Integração com OpenAI LLM** - Usa generate_response_with_llm
- ✅ **Geração de respostas inteligentes** - Baseadas no contexto dos documentos
- ✅ **Tratamento de erros** - Validação de entrada e fallbacks
- ✅ **Interface limpa** - Apenas mensagens essenciais para navegação
- ✅ **Separação de responsabilidades** - LLM isolado do sistema de busca

### 🏃‍♂️ Como Usar

#### Execução Direta
```bash
# Executar chat interativo
python src/chat.py
```

#### Uso Programático
```python
# Importar e usar diretamente
from chat import interactive_chat
interactive_chat()

# Ou usar apenas a função de geração de resposta
from chat import generate_response_with_llm
resultado = generate_response_with_llm("Sua pergunta aqui")
print(resultado)
```

### 📝 Funcionalidades Disponíveis

1. **`interactive_chat()`** - Chat interativo completo para testes
2. **`generate_response_with_llm(question)`** - Geração de resposta com LLM
3. **Integração com search.py** - Busca + LLM + resposta final
4. **Respostas inteligentes** - Baseadas no contexto dos documentos

### 📊 Características Técnicas
- **LLM**: OpenAI gpt-5-nano (configurável via OPENAI_MODEL)
- **Configuração**: Variáveis de ambiente (OPENAI_MODEL)
- **Responsabilidade**: Execução do LLM e interface de chat
- **Integração**: Usa search_prompt do search.py

---

## ⚠️ Observações Gerais

- Certifique-se de ter uma API key válida do OpenAI
- O banco PostgreSQL deve estar rodando antes da execução
- A extensão pgvector deve estar instalada no banco
- Apenas as configurações necessárias estão no arquivo `.env`
- Configurações não utilizadas foram removidas para manter o projeto limpo