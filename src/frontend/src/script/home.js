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
});

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

