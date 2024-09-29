from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

embeddings_model = "sentence-transformers/all-mpnet-base-v2"
hf_model = HuggingFaceEmbeddings(model_name=embeddings_model)

docsearch = FAISS.load_local("vectordatabase/faiss_index", hf_model, allow_dangerous_deserialization=True)


# Load the LlamaCpp language model, adjust GPU usage based on your hardware
llm = LlamaCpp(
    model_path="model/llama-2-7b-chat.Q4_K_M.gguf",
    n_gpu_layers=40,
    n_batch=512,  # Batch size for model processing
    verbose=False,  # Enable detailed logging for debugging
)

# Define the prompt templates with a placeholder for the question
template = """
Context: {context}
Question: {question}

Provide your response only based on the "context". 
Your response should be in 10 words.

Answer:
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Create an LLMChain to manage interactions with the prompt and model
llm_chain = LLMChain(prompt=prompt, llm=llm)

# while True:

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST', 'GET'])
def ask_question():
    try:
        # Get the JSON data from the request body
        print("here")
        print("++++++++++++++++++++++++++++", request)
        data = request.json
        if 'question' not in data:
            return jsonify({"error": "Please provide a 'question' in the request body"}), 400

        # Extract the question
        question = data['question']

        # question = "Whom to reach for academic questions related to computer science at SUNY Poly?"
        results = docsearch.similarity_search(
            question,
            k=3,
        )

        context = ""

        for res in results:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(res.page_content)
            context += res.page_content + "\n"

        answer = llm_chain.run({"context": context, "question": question})
        print(answer, '\n')

        # Return the answer as a JSON response
        return jsonify({"question": question, "answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(host='localhost', port=5555)
