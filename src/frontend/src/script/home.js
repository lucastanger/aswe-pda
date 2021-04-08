// Home.js
// Define all available sidebar pages
let pages = ['home', 'homegb', 'chat', 'history', 'settings'];

/*
    Add some jQuery features to the page.
    e.g. sidebar toggling and specific select effects
 */
$(function () {
    $('#nav').hover(function () {
        $(this).toggleClass('expand');
        $('.chat-expand').toggle('hidden');
        $('#nav').not(this).toggleClass('shrink');
    });
    // Switch between different sides
    $('.btn').click(function () {
        toggleButton(this);
        // Load selected page
        loadPage(this.name);
    });
    // Add Event Listener to Microfon
    $('#mic').click(function () {
        listen();

    });
});

function listen() {

    navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        const audioChunks = [];

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, {'type': 'audio/wav'});

            let reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = function () {
                let base64data = reader.result
                console.log(base64data)

                $.ajax({
                    url: 'http://localhost:5600/rest/api/v1/t2ss2t/recognize',
                    type: 'POST',
                    data: JSON.stringify({
                        'audio': base64data
                    }),
                    crossDomain: true,
                    contentType: 'application/json',
                    beforeSend: setHeader,
                    success: function (response) {
                        if (response.hasOwnProperty('text')) {
                            let input = document.createElement('input');
                            input.value = response.text;
                            console.log(input);
                            loadPage('chat');
                            sendMessage(input).then(function (r) {
                                console.log(r);
                            });
                        } else {
                            alert('Looks like there is no valid response!')
                        }
                    },
                    error: function (error) {
                        console.log('Could not reach the middleware! Error:');
                        console.log(error);
                    }
                })

            }

        });

        setTimeout(() => {
            mediaRecorder.stop();
        }, 3000);
    });
}

function toggleButton(button) {
    $('.btn').each(function () {
        this.classList.remove("dark:bg-green-600", "bg-green-400");
    });
    // Mark according button as selected
    button.classList.add("dark:bg-green-600", "bg-green-400");
}

function stopLoader(id) {
    document.getElementById(id).remove()
}

function loadPage(pageName) {

    // If page is chat, hide top input
    // if (pageName === 'chat') {
    //     headerInput.classList.add('hidden');
    // } else {
    //     headerInput.classList.remove('hidden');
    // }

    // Hide all other pages
    pages.forEach(page => document.getElementById(page).classList.add('hidden'));
    // Show requested page
    document.getElementById(pageName).classList.remove('hidden');
}

function load() {
    $("#modal").load("modal.html");
}

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
});

function onButtonClick(btn) {
    btn.classList.add('active');
}
