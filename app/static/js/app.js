class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
        this.questions = [
            "Cual es su edad? (Adult, Elderly, Teenager)",
            "Cual es el clima? (Warm, Temperate, Cold)",
            "Cual es su genero? (Masculine, Femenine)",
            "Cual es el tipo de evento? (Marriage, Baptism, Stag-party, Quinceanera_party, Graduation, Funeral)"
        ];
        this.currentQuestionIndex = 0;
        this.answers = {};
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active');
            // Saludar y preguntar si está listo para comenzar
            this.addMessageToChat("Bot", "¡Hola! ¿Estás listo para comenzar? (responde sí o no)");
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const userMessage = textField.value.trim();
    
        if (userMessage !== '') {
            // Agregar el mensaje del usuario al chat
            this.addMessageToChat("User", userMessage);
            textField.value = "";
    
            // Si es la primera pregunta, no enviarla al servidor, solo guardar la respuesta
            if (this.currentQuestionIndex === 0) {
                this.saveAnswer(userMessage);
                this.askNextQuestion(chatbox);
            } else {
                // Construir el objeto con las respuestas del usuario
                const userData = {
                    Age: this.answers['Cual es su edad?'] || 'Adult',
                    Weather: this.answers['Cual es el clima? (Warm, Temperate, Cold)'] || 'Cold',
                    Sex_gender: this.answers['Cual es su genero? (Masculine, Femenine)'] === 'Femenine' ? 'F' : 'M',
                    Event: this.answers['Cual es el tipo de evento? (Marriage, Baptism, Stag-party, Quinceanera_party, Graduation, Funeral)'] || 'Marriage'
                };
    
                console.log('Datos enviados al servidor:', userData);
                
                // Enviar mensaje del usuario al servidor Flask
                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                })
                    .then(response => {
                        // Verificar el estado de la respuesta
                        if (!response.ok) {
                            throw new Error('Ocurrió un error al enviar los datos al servidor.');
                        }
                        // Si la respuesta es exitosa, devolver los datos en formato JSON
                        return response.json();
                    })
                    .then(data => {
                        // Mostrar la respuesta del bot en el chat
                        this.addMessageToChat("Bot", data.prediction);
                        // Guardar la respuesta del usuario
                        this.saveAnswer(userMessage);
                        // Hacer la siguiente pregunta
                        this.askNextQuestion(chatbox);
                    })
                    .catch(error => {
                        console.error('Error:', error.message);
                        // Mostrar un mensaje de error en el chat
                        this.addMessageToChat("Bot", "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.");
                    });
            }
        }
    }
    
    askNextQuestion(chatbox) {
        if (this.currentQuestionIndex < this.questions.length) {
            const nextQuestion = this.questions[this.currentQuestionIndex];
            this.addMessageToChat("Bot", nextQuestion);
            this.currentQuestionIndex++;
        } else {
            // Finalizar la conversación
            this.addMessageToChat("Bot", "¡Espero que disfrutes tu elección! ¡Adiós!");
            this.toggleState(chatbox); // Cerrar el chat
        }
    }

    saveAnswer(answer) {
        const question = this.questions[this.currentQuestionIndex - 1];

        // Validar las respuestas para cada pregunta
        switch(question) {
            case "Cual es su edad? (Adult, Elderly, Teenager)":
                const validAges = ['Adult', 'Elderly', 'Teenager'];
                if (!validAges.includes(answer.trim().toUpperCase())) {
                    console.error('Error: Valor de edad no válido');
                    return;
                }
                break;
            case "Cual es el clima? (Warm, Temperate, Cold)":
                const validWeathers = ['Warm', 'Temperate', 'Cold'];
                const weatherInput = answer.trim().toUpperCase();
                const weatherValidated = validWeathers.find(validWeather => validWeather.toUpperCase() === weatherInput);
                if (!weatherValidated) {
                    console.error('Error: Valor de clima no válido');
                    return;
                }
                break;
            case "Cual es su genero? (Masculine, Femenine)":
                const validGenders = ['Masculine', 'Femenine'];
                const genderInput = answer.trim().toUpperCase();
                const genderValidated = validGenders.find(validGender => validGender.toUpperCase() === genderInput);
                if (!genderValidated) {
                    console.error('Error: Valor de género no válido');
                    return;
                }
                break;
            case "Cual es el tipo de evento? (Marriage, Baptism, Stag-party, Quinceanera_party, Graduation, Funeral)":
                const validEvents = ['Marriage', 'Baptism', 'Stag-party', 'Quinceanera_party', 'Graduation', 'Funeral'];
                const eventInput = answer.trim().toLowerCase();
                const eventValidated = validEvents.find(validEvent => validEvent.toLowerCase() === eventInput);
                if (!eventValidated) {
                    console.error('Error: Valor de evento no válido');
                    return;
                }
                break;
            default:
                break;
        }

        this.answers[question] = answer.toLowerCase(); 
    }

    addMessageToChat(name, message) {
        this.messages.push({ name, message });
        this.updateChatText();
    }

    updateChatText() {
        const chatbox = this.args.chatBox;
        let html = '';
        for (let i = this.messages.length - 1; i >= 0; i--) {
            const item = this.messages[i];
            if (item.name === "User") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        }
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
