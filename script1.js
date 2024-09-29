const chatInput = document.querySelector('.chat-input textarea');
const sendChatBtn = document.querySelector('.chat-input button');
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = `<p>${message}</p>`;
    chatLi.innerHTML = chatContent;
    return chatLi;
};

const generateResponse = (incomingChatLi) => {
    const API_URL = "http://localhost/ask";  // Correct URL
    const messageElement = incomingChatLi.querySelector("p");
    if (userMessage!="hi"){
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"question": userMessage})
        };
    }
    else{
        messageElement.textContent = "Please ask your question..."
    }
    fetch(API_URL, requestOptions)
        .then(res => {
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            return res.json();  // Parse the JSON response
        })
        .then(data => {
            console.log("API Response:", data);  // Log the entire response for debugging

            // Check if 'choices' and the expected message exist in the response
            if (data.answer.length > 0) {
                messageElement.textContent = data.answer;
            } else if (data.error) {
                throw new Error(`API Error: ${data.error}`);  // Handle OpenAI API errors
            } else {
                throw new Error("No response choices found");
            }
        })
        .catch((error) => {
            console.error("Error occurred:", error);
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again!";
        })
        .finally(() => {
            chatbox.scrollTo(0, chatbox.scrollHeight);
        });
};


const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) {
        return;
    }
    chatbox.appendChild(createChatLi(userMessage, "chat-outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    // Clear the input field
    chatInput.value = "";

    setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "chat-incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
};

sendChatBtn.addEventListener("click", handleChat);

function cancel() {
    let chatbotcomplete = document.querySelector(".chatBot");
    if (chatbotcomplete.style.display !== 'none') {
        chatbotcomplete.style.display = "none";
        
        if (!document.querySelector('.lastMessage')) {
            let lastMsg = document.createElement("p");
            lastMsg.textContent = 'Thanks for using our Chatbot!';
            lastMsg.classList.add('lastMessage');
            document.body.appendChild(lastMsg);
        }
    }
}
