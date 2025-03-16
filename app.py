import os
import torch
import pickle
from dash import Dash, html, dcc, Input, Output, State
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
import fitz  # PyMuPDF
from unstructured.partition.md import partition_md

# --------------------- Document Loading Functions ---------------------
def load_pdf(file_path):
    """Load text from PDF files using PyMuPDF"""
    doc = fitz.open(file_path)
    return " ".join([page.get_text() for page in doc])

def load_markdown(file_path):
    """Load text from Markdown files using Unstructured"""
    return "\n".join(str(el) for el in partition_md(filename=file_path))

# --------------------- Load Documents ---------------------
documents = [
    {"content": load_pdf("resume.pdf"), "source": "resume.pdf"},
    {"content": load_pdf("linkedin_profile.pdf"), "source": "linkedin_profile.pdf"},
    {"content": load_markdown("personal_blog.md"), "source": "personal_blog.md"}
]

# --------------------- Vector Store Setup ---------------------
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.load_local(
    "personal_vector_store",
    embedding_model,
    allow_dangerous_deserialization=True
)

# --------------------- Model Setup ---------------------
tokenizer = AutoTokenizer.from_pretrained("saved_tokenizer_googleT5")
model = AutoModelForSeq2SeqLM.from_pretrained("saved_model_GoogleT5")

with open("saved_pipeline_googleT5.pkl", "rb") as f:
    pipe = pickle.load(f)

llm = HuggingFacePipeline(pipeline=pipe)

# --------------------- Prompt Template Setup ---------------------
personal_prompt_template = """
I'm your friendly AI assistant, here to provide information about my background, education, work experience, and beliefs. 
Feel free to ask me any questions about myself, and I'll do my best to provide accurate and helpful answers.

Context: {context}
Question: {question}
Answer:
""".strip()

PERSONAL_PROMPT = PromptTemplate.from_template(template=personal_prompt_template)

# --------------------- Memory Setup ---------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question",    # Explicit input key
    output_key="answer"      # Explicit output key
)

# --------------------- Chain Setup ---------------------
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    return_source_documents=True,
    output_key="answer"      # Must match memory's output_key
)

# --------------------- Dash App ---------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Chat with Arunya's Personal Chatbot"),
    dcc.Input(id="input-text", type="text", placeholder="Ask about Arunya...", 
             style={"width": "80%", "padding": "10px"}),
    html.Button("Ask", id="submit-button", n_clicks=0,
               style={"marginLeft": "10px", "padding": "10px 20px"}),
    html.Div(id="output-text", style={
        "whiteSpace": "pre-line", 
        "marginTop": "20px",
        "padding": "20px",
        "border": "1px solid #ddd",
        "borderRadius": "5px"
    }),
    html.Div(id="source-documents", style={
        "marginTop": "20px",
        "padding": "20px",
        "backgroundColor": "#f5f5f5",
        "borderRadius": "5px"
    })
])

@app.callback(
    [Output("output-text", "children"), Output("source-documents", "children")],
    [Input("submit-button", "n_clicks")],
    [State("input-text", "value")]
)
def update_output(n_clicks, question):
    if n_clicks > 0 and question:
        try:
            # Retrieve context from the vector store
            docs = vector_store.similarity_search(question, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            
            # Format the prompt using the template
            formatted_prompt = PERSONAL_PROMPT.format(context=context, question=question)
            
            # Get the response from the chain
            response = chain({"question": formatted_prompt})
            answer = response.get("answer", "I couldn't find an answer.")
            sources = [
                html.Div([
                    html.P(f"📄 Source: {doc.metadata['source']}",
                          style={"fontWeight": "bold"}),
                    html.P(f"📝 Excerpt: {doc.page_content[:250]}...")
                ], style={"marginBottom": "15px"})
                for doc in response.get("source_documents", [])
            ]
            return answer, sources
        except Exception as e:
            return f"Error: {str(e)}", ""
    return "Summary of related articles and documents ", ""

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)