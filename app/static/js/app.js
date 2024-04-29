class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        const optionsDiv = chatbox.querySelector('#options');
        optionsDiv.innerHTML = ''; // Limpiar opciones anteriores
      
        // Definir las opciones
        const opciones = ['Opción 1', 'Opción 2', 'Opción 3'];
      
        // Crear un elemento div para cada opción
        opciones.forEach(opcion => {
          const opcionDiv = document.createElement('div');
          opcionDiv.textContent = opcion;
          opcionDiv.classList.add('opcion');
          opcionDiv.addEventListener('click', () => this.handleOptionClick(opcion, chatbox));
          optionsDiv.appendChild(opcionDiv);
        });
      }

      handleOptionClick(opcion, chatbox) {
        const { sendButton } = this.args;
        const textField = chatbox.querySelector('input');
      
        let msg1 = { name: "User", message: opcion };
        this.messages.push(msg1);
      
        // Simular el clic en el botón "Enviar" para procesar la opción seleccionada
        sendButton.dispatchEvent(new Event('click'));
      
        textField.value = ''; // Limpiar el campo de entrada
        const optionsDiv = chatbox.querySelector('#options');
        optionsDiv.innerHTML = ''; // Limpiar las opciones
      }

      updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
          if (item.name === "Sam") {
            html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
          } else {
            html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
          }
        });
        const chatmessage = chatbox.querySelector('.chatbox__messages > div:first-child');
        chatmessage.innerHTML = html;
      }
}


const chatbox = new Chatbox();
chatbox.display();