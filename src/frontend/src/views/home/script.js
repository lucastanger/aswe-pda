let input = document.getElementById('chatInput');
input.addEventListener("keyup", function (event) {
    // TODO: keyCode deprecated
    if (event.keyCode === 13) {
        event.preventDefault()
        sendMessage();
    }
});

$(document).ready(function () {
    // Dark Mode Toggle Function
    $('#darkMode').click(function () {
        let root = document.getElementById('darkSwitch');
        root.classList.contains('dark') ? root.classList.remove('dark') : root.classList.add('dark')
    });
    // Buttons Toggle Function
    $('.btn').click(function () {
        for (let btn of document.getElementsByClassName('btn')) {
            btn.classList.remove('active');
        }
        // Invoke button click function
        onButtonClick(this);
    });
});

function onButtonClick(btn) {
    btn.classList.add('active');


}

function sendMessage() {
    // Retrieve user message
    let chatMessage = input.value;
    // Delete user input
    input.value = "";
    // Log user input for debug purposes
    console.log(chatMessage);
    // Display Chat Message
    let chatElement = createChatElement(chatMessage);
    document.getElementById('chatArea').appendChild(chatElement);

}

function createChatElement(messagePayload) {
    // Create divs
    let div = document.createElement('div');
    let message = document.createElement('div');

    // Assign classes
    div.className = "clearfix";
    message.classList.add("bg-green-300");
    message.classList.add("mx-4");
    message.classList.add("my-2");
    message.classList.add("p-2");
    message.classList.add("rounded-lg");
    message.classList.add("right-0");
    message.classList.add("float-right");

    // Add message payload
    message.innerText = messagePayload;

    // Compose divs and return
    div.appendChild(message);
    return div;
}

// Event Listener for Sidebar Navigation
for (let elem of document.getElementsByClassName('c-sidebar')) {
    // Add Event Listener
    document.getElementById(elem.id).addEventListener("click", function (event) {

        // Define list of all containers
        let containers = ['chatContainer', 'historyContainer', 'profileContainer', 'designContainer'];

        // Enable hidden state on all containers
        for (let c of containers) {
            document.getElementById(c).classList.add('hidden');
        }

        // Remove hidden state from currently displayed container
        document.getElementById(elem.id.replace('link', '')+'Container').classList.remove('hidden');
    });
}