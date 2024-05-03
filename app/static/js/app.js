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
        
        // Enviar mensaje del usuario al servidor Flask
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Mostrar la respuesta del bot en el chat
            this.addMessageToChat("Bot", data.prediction);
            // Hacer la siguiente pregunta o finalizar la conversación
            this.askNextQuestion(chatbox);
        })
        .catch(error => console.error('Error:', error));
    }
}

askNextQuestion(chatbox) {
  if (this.currentQuestionIndex < this.questions.length) {
      const nextQuestion = this.questions[this.currentQuestionIndex];
      this.addMessageToChat("Bot", nextQuestion);
      this.currentQuestionIndex++;
  } else {
      // Si se han hecho todas las preguntas, enviar las respuestas al servidor Flask para obtener la predicción
      fetch('/predict', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ data: this.answers })
      })
      .then(response => response.json())
      .then(data => {
          // Mostrar la predicción en el chat
          this.addMessageToChat("Bot", "¡Basado en tus respuestas, te recomiendo usar: " + data.prediction);
          // Finalizar la conversación
          this.addMessageToChat("Bot", "¡Espero que disfrutes tu elección! ¡Adiós!");
          this.toggleState(chatbox); // Cerrar el chat
      })
      .catch(error => console.error('Error:', error));
  }
}

saveAnswer(answer) {
  // Guardar la respuesta del usuario en el objeto de respuestas
  this.answers[this.currentQuestionIndex - 1] = answer;
}

addMessageToChat(name, message) {
  this.messages.push({ name, message });
  this.updateChatText();
}

updateChatText() {
  const chatbox = this.args.chatBox;
  let html = '';
  this.messages.forEach(item => {
      if (item.name === "User") {
          html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
      } else {
          html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
      }
  });
  const chatmessage = chatbox.querySelector('.chatbox__messages');
  chatmessage.innerHTML = html;
}
}

const chatbox = new Chatbox();
chatbox.display();