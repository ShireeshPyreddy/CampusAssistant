from langchain_community.document_loaders import PyPDFLoader
import os
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from uuid import uuid4
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore


embeddings_model = "sentence-transformers/all-mpnet-base-v2"

hf_model = HuggingFaceEmbeddings(model_name=embeddings_model)

data = []

for each in os.listdir("data"):

    loader = PyPDFLoader("data/"+each)
    pages = loader.load_and_split()
    print(len(pages))

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=500, chunk_overlap=150, length_function=len
    )

    docs = text_splitter.split_documents(pages)

    print("Pages in the original document: ", len(pages))
    print("Length of chunks after splitting pages: ", len(docs))

    print(docs)

    data.extend(docs)

print(len(data), data)

index = faiss.IndexFlatL2(len(hf_model.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=hf_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

uuids = [str(uuid4()) for _ in range(len(data))]

vector_store.add_documents(documents=data, ids=uuids)

vector_store.save_local("vectordatabase/faiss_index")


docsearch = FAISS.load_local("vectordatabase/faiss_index", hf_model, allow_dangerous_deserialization=True)

results = docsearch.similarity_search(
    "When we should I apply for OPT",
    k=2,
)

print("###################################################")

for res in results:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(res.page_content)

