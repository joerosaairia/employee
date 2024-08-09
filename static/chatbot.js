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
        fetch('https://demo.airia.com/platform/api/PipelineExecution/employee_assistant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'd465b2d3-4b4c-4167-83ee-e7c144664b35'  // replace with the actual API key
            },
            body: JSON.stringify({
                userInput: userInput,
                debug: true
            })
        })
        .then(response => response.json())
        .then(data => { console.log(userInput)})
        .then(data => {
            console.log(data);
        });
    }
});
