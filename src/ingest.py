import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

load_dotenv()

# Configurações
PDF_PATH = os.getenv("PDF_PATH")
PGVECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

def load_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    return documents

def get_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_store():
    """Cria o store PGVector"""
    try:
        # Embeddings OpenAI
        embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

        store = PGVector(
            embeddings=embeddings,
            collection_name=PGVECTOR_COLLECTION,
            connection=PGVECTOR_URL,
            use_jsonb=True,
        )
        
        print("Store PGVector criado com sucesso!")
        
        return store
    except Exception as e:
        print(f"Erro ao criar store PGVector: {e}")
        return None

def enrich_documents(chunks):
    """Enriquece os documentos com IDs únicos"""
    enriched_documents = []
    ids = []
    current_time = datetime.now().isoformat()
    
    for chunk in chunks:
        # Criar ID único para cada chunk
        chunk_id = str(uuid.uuid4())
        
        # Enriquecer documento com metadados adicionais
        enriched_doc = Document(
            page_content=chunk.page_content,
            metadata={
                **chunk.metadata,
                "chunk_id": chunk_id,
                "source": "pdf_document",
                "processed_at": current_time
            }
        )
        
        enriched_documents.append(enriched_doc)
        ids.append(chunk_id)
        print(f"Documento enriquecido: {chunk.page_content[:50]}... (ID: {chunk_id})")
    
    return enriched_documents, ids

def store_embeddings_pgvector(chunks):
    """Armazena os embeddings usando PGVector"""
    try:
        # 1. Criar store PGVector
        print("1. Criando store PGVector...")
        store = create_vector_store()
        if not store:
            print("Falha ao criar store PGVector!")
            return False
        
        # 2. Enriquecer documentos
        print("2. Enriqueceendo documentos...")
        enriched_docs, ids = enrich_documents(chunks)
        print(f"Documentos enriquecidos: {len(enriched_docs)}")
        
        # 3. Adicionar documentos ao store
        print("3. Adicionando documentos ao store...")
        store.add_documents(documents=enriched_docs, ids=ids)
        print(f"✅ {len(enriched_docs)} documentos armazenados com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"Erro ao armazenar embeddings: {e}")
        return False

def ingest_pdf(chunks):
    """Pipeline completo de ingestão usando PGVector"""
    print(f"Processando {len(chunks)} chunks...")
    
    # Armazenar embeddings usando PGVector
    success = store_embeddings_pgvector(chunks)
    
    if success:
        print("\n✅ Pipeline de ingestão concluído com sucesso!")
        print("📊 Dados armazenados no PostgreSQL com pgVector usando LangChain")
    else:
        print("\n❌ Falha no pipeline de ingestão!")

if __name__ == "__main__":
    documents = load_pdf()
    chunks = get_chunks(documents)
    ingest_pdf(chunks)