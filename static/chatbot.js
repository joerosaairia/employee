document.addEventListener('DOMContentLoaded', function() {
    const chatbot = document.getElementById('chatbot');
    const openChatbotButton = document.getElementById('open-chatbot');
    const closeChatbotButton = document.getElementById('close-chatbot');
    const sendChatbotButton = document.getElementById('send-chatbot');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotMessages = document.getElementById('chatbot-messages');

    openChatbotButton.addEventListener('click', () => {
        chatbot.style.display = 'flex';
        openChatbotButton.style.display = 'none';
    });

    closeChatbotButton.addEventListener('click', () => {
        chatbot.style.display = 'none';
        openChatbotButton.style.display = 'block';
    });

    sendChatbotButton.addEventListener('click', () => {
        const userMessage = chatbotInput.value.trim();
        if (userMessage !== '') {
            addMessage(userMessage, 'user-message');
            chatbotInput.value = '';
            sendToApi(userMessage);
        }
    });

    function addMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        messageElement.textContent = message;
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function sendToApi(userInput) {
        fetch('/api/employee_assistant', {  // Call the Flask backend API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userInput: userInput,
                debug: true
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Unknown error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received:", data); // Log the data for debugging
            if (data.result) {
                addMessage(`Bot: ${data.result}`, 'bot-message');  // Display the result
            } else if (data.report) {
                const firstReport = Object.values(data.report)[0];
                if (firstReport && firstReport.result) {
                    addMessage(`Bot: ${firstReport.result}`, 'bot-message');  // Display the nested result
                } else {
                    addMessage('Sorry, there was an error processing your request.', 'bot-message');
                }
            } else {
                addMessage('Sorry, there was an error processing your request.', 'bot-message');
            }
        })
        .catch(error => {
            addMessage(`Bot: ${error.message}`, 'bot-message');  // Display the error message
        });
    }
});
