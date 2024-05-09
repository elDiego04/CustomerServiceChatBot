class Chatbox {
  constructor() {
      this.args = {
          openButton: document.querySelector('.chatbox__button'),
          chatBox: document.querySelector('.chatbox__support'),
          sendButton: document.querySelector('.send__button')
      }

      this.state = false;
      this.messages = [];
      this.questions = [
        "Cual es su edad?",
        "Cual es el clima? (Calido, Templado, Frio)",
        "Cual es su genero? (Masculino, Femenino)",
        "Cual es el tipo de evento? (Matrimonio, Bautizo, Despedida de soltero, Fiesta de quinces, Graduacion, Funeral)"
      ];    
      this.currentQuestionIndex = 0;
      this.answers = {};
  }

  display() {
      const {openButton, chatBox, sendButton} = this.args;

      openButton.addEventListener('click', () => this.toggleState(chatBox));

      sendButton.addEventListener('click', () => this.onSendButton(chatBox));

      const node = chatBox.querySelector('input');
      node.addEventListener("keyup", ({key}) => {
          if (key === "Enter") {
              this.onSendButton(chatBox);
          }
      });
  }

  toggleState(chatbox) {
      this.state = !this.state;

      // show or hides the box
      if(this.state) {
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
              Age: this.answers['Cual es su edad?'],
              Weather: this.answers['Cual es el clima? (Calido, Templado, Frio)'],
              Sex_gender: this.answers['Cual es su genero? (Masculino, Femenino)'] === 'masculino' ? 'M' : 'F',
              Event: this.answers['Cual es el tipo de evento? (Matrimonio, Bautizo, Despedida de soltero, Fiesta de quinces, Graduacion, Funeral)']
          };

            console.log('Datos enviados al servidor:', userData); // Agrega este registro

            // Enviar mensaje del usuario al servidor Flask
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data: userData })
            })
            .then(response => response.json())
            .then(data => {
                // Mostrar la respuesta del bot en el chat
                this.addMessageToChat("Bot", data.prediction);
                // Guardar la respuesta del usuario
                this.saveAnswer(userMessage);
                // Hacer la siguiente pregunta
                this.askNextQuestion(chatbox);
            })
            .catch(error => console.error('Error:', error));
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
  this.answers[question] = answer.toLowerCase(); // Convertir la respuesta a minúsculas
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