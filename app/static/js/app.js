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
        this.userData = {};
    }
    capitalizeFirstLetter(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
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
            console.log( 'antes', this.currentQuestionIndex);
            console.log(userMessage);
            // Agregar el mensaje del usuario al chat
            this.addMessageToChat("User", userMessage);
            textField.value = "";
    
            // Si es la primera pregunta, no enviarla al servidor, solo guardar la respuesta
            // if (this.currentQuestionIndex === 0) {
                
                this.saveAnswer(userMessage);
                if (this.currentQuestionIndex == 1){
                    this.userData.Age = this.capitalizeFirstLetter(userMessage);
                }
                if (this.currentQuestionIndex == 2){
                    this.userData.Weather = this.capitalizeFirstLetter(userMessage);
                }
                if (this.currentQuestionIndex == 3){
                    this.userData.Sex_gender = this.capitalizeFirstLetter(userMessage) == 'Masculine' ? 'M' : 'F';
                }
    

                this.askNextQuestion(chatbox);
                console.log('despues', this.currentQuestionIndex)
            // }
            
            if (this.currentQuestionIndex - 1 == 4){
                console.log(this.currentQuestionIndex);
                this.saveAnswer(userMessage);
                // Construir el objeto con las respuestas del usuario
                if (this.currentQuestionIndex - 1 == 4){
                    this.userData.Event = this.capitalizeFirstLetter(userMessage);
                }

    
                console.log('Datos enviados al servidor:', this.userData);
                
                // Enviar mensaje del usuario al servidor Flask
                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.userData)
                })
                    .then(response => {
                        // Verificar el estado de la respuesta
                        if (!response.ok) {
                            throw new Error('Ocurrió un error al enviar los datos al servidor.');
                        }
                        this.userData = {};
                        this.currentQuestionIndex = 0;
                        // Si la respuesta es exitosa, devolver los datos en formato JSON
                        return response.json();
                    })
                    // Inside the fetch('/predict') callback
                    .then(data => {
                        // Load image data from productos.json
                        fetch('./static/js/productos.json')
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Failed to fetch image data.');
                                }
                                return response.json();
                            })
                            .then(imagenes => {
                                let matchedImage = imagenes.find(imagen => imagen.categoria.evento === data.prediction);
                    
                                if (matchedImage) {
                                    // Create an image element
                                    const imageElement = document.createElement('img');
                                    imageElement.src = matchedImage.imagen;
                    
                                    // Add the image to the chat
                                    this.addMessageToChat("Bot", imageElement);
                    
                                    // Save the user's response
                                    this.saveAnswer(userMessage);
                    
                                    // Update the chat display
                                    this.updateChatText();
                                } else {
                                    // If no matching image found, display a message
                                    this.addMessageToChat("Bot", "No se encontró ninguna imagen para la predicción.");
                                }
                    
                                
                            })
                            .catch(error => {
                                console.error('Error:', error.message);
                                // Mostrar un mensaje de error en el chat
                                this.addMessageToChat("Bot", "Lo siento, ocurrió un error al cargar los datos de imagen. Por favor, inténtalo de nuevo.");
                                this.userData = {};
                                this.currentQuestionIndex = 0;
                            });
                    })
                    .catch(error => {
                        console.error('Error:', error.message);
                        // Mostrar un mensaje de error en el chat
                        this.addMessageToChat("Bot", "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.");
                        this.userData = {};
                        this.currentQuestionIndex = 0;
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
            this.currentQuestionIndex++;
            // this.toggleState(chatbox); // Cerrar el chat
        }
    }

    saveAnswer(answer) {
        const question = this.questions[this.currentQuestionIndex - 1];

        // Validar las respuestas para cada pregunta
        switch(question) {
            case "Cual es su edad? (Adult, Elderly, Teenager)":
                const validAges = ['Adult', 'Elderly', 'Teenager'];
                let age = this.capitalizeFirstLetter(answer.trim());
                if (!validAges.includes(age)) {
                    console.error('Error: Valor de edad no válido');
                    return;
                }
                break;
            case "Cual es el clima? (Warm, Temperate, Cold)":
                const validWeathers = ['Warm', 'Temperate', 'Cold'];
                let weather = this.capitalizeFirstLetter(answer.trim());
                if (!validWeathers.includes(weather)) {
                    console.error('Error: Valor de clima no válido');
                    return;
                }
                break;
            case "Cual es su genero? (Masculine, Femenine)":
                const validGenders = ['Masculine', 'Femenine'];
                let genero = this.capitalizeFirstLetter(answer.trim());
                if (!validGenders.includes(genero)) {
                    console.error('Error: Valor de género no válido');
                    return;
                }
                break;
            case "Cual es el tipo de evento? (Marriage, Baptism, Stag-party, Quinceanera_party, Graduation, Funeral)":
                const validEvents = ['Marriage', 'Baptism', 'Stag-party', 'Quinceanera_party', 'Graduation', 'Funeral'];
                let evento = this.capitalizeFirstLetter(answer.trim());
                if (!validEvents.includes(evento)) {
                    console.error('Error: Valor de evento no válido');
                    return;
                }
                break;
            default:
                break;
        }

        // this.answers[question] = answer.toLowerCase(); 
    }

    addMessageToChat(name, message) {
        if (typeof message === 'string') {
            this.messages.push({ name, message });
        } else if (message instanceof HTMLImageElement) {
            this.messages.push({ name, message: message.outerHTML });
        }
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
