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

# OpenAI Configuration (necessária para embeddings)
OPENAI_API_KEY=sua_chave_api_openai_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
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

### 📋 Status Atual
🚧 **Em Desenvolvimento**

### 🎯 Funcionalidades Planejadas
- [ ] Busca semântica nos embeddings armazenados
- [ ] Retrieval de documentos relevantes baseado na query
- [ ] Sistema de ranking de relevância
- [ ] Filtros por metadados

### 📝 Implementação Atual
O arquivo contém um template de prompt para respostas baseadas em contexto, mas a funcionalidade de busca ainda não foi implementada.

### 🔄 Próximos Passos
- Implementar busca vetorial usando PGVector
- Configurar retriever com LangChain
- Adicionar sistema de scoring de relevância
- Integrar com o sistema de chat

---

## 💬 chat.py - Interface de Chat RAG

### 📋 Status Atual
🚧 **Em Desenvolvimento**

### 🎯 Funcionalidades Planejadas
- [ ] Interface interativa de chat
- [ ] Integração com sistema de busca
- [ ] Geração de respostas usando LLM
- [ ] Histórico de conversas
- [ ] Tratamento de erros e validações

### 📝 Implementação Atual
O arquivo possui a estrutura básica para inicializar o chat, mas ainda não implementa a interface completa.

### 🔄 Próximos Passos
- Implementar loop de conversação
- Integrar com search.py para retrieval
- Adicionar geração de respostas com LLM
- Criar interface de usuário amigável

---

## ⚠️ Observações Gerais

- Certifique-se de ter uma API key válida do OpenAI
- O banco PostgreSQL deve estar rodando antes da execução
- A extensão pgvector deve estar instalada no banco
- Apenas as configurações necessárias estão no arquivo `.env`
- Configurações não utilizadas foram removidas para manter o projeto limpo