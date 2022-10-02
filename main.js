window.onload = function() {
    var sendForm = document.querySelector('#chatform'),
    textInput = document.querySelector('.chatbox'),
    chatList = document.querySelector('.chatList'),
    userBubble = document.querySelectorAll('.userInput'),
    chatList = document.querySelector('.chatlist'),
    animateBotBubble = document.querySelectorAll('.bot__input--animation'),
    animationCounter = 1,
    previousInput,

    //Event Listeners
    sendForm.onkeydown = function (ev) {
        if (ev.keyCode == 13) {
            ev.preventDefault();            
            var input = textInput.value; //Retrieve written value
            if (input.length > 0) { //Empty text area
                createBubble(input);
            }
        }
    }
    sendForm.addEventListener('submit', function (ev) {
        ev.preventDefault();    
        var input = textInput.value; //Retrieve written value
        if (input.length > 0) { //Empty text area
            createBubble(input);
        }

    })
    
    //Chat Bubbles 
    var createBubble = function (input) {
        var chatBubble = document.createElement('li'); //Creates new input bubble
        chatBubble.classList.add('userInput');
        chatBubble.innerHTML = input; //Adds input of textarea to the new chatBubble
        chatList.appendChild(chatBubble); //adds chatBubble to chatList
    
        botResponse(input); //Gets chatbot response

    }
    function botResponse(textVal) {        
        var userBubble = document.createElement('li'); //create response bubble
        userBubble.classList.add('botOutput');
    
        if (textVal == "Hello") { //Its Cap sensitive so be careful when testing
            userBubble.innerHTML = chatBotTemp[textVal](); //Call function for Chat bot to respond.
        } else {
            userBubble.innerHTML = responseText("Failed");
            commandReset(0);
        }
    
        chatList.appendChild(userBubble) //Adds chatBubble to chatList
        textInput.value = ""; //Reset text area input
    }

    function responseText(e) {

        var response = document.createElement('li');    
        response.classList.add('botOutput');    
        response.innerHTML = e; //Adds whatever is given to responseText() to the response bubble    
        chatList.appendChild(response);

        animateBotOutput(); //Animates the chatBubble
    
        setTimeout(function () { //Sets chatList scrollbar to the bottom
            chatList.scrollTop = chatList.scrollHeight;
            console.log(response.clientHeight);
        }, 0);
    }
    
    function animateBotOutput() {
        chatList.lastElementChild.style.animationDelay = (animationCounter * 600) + "ms";
        animationCounter++;
        chatList.lastElementChild.style.animationPlayState = "running";
    }

    function commandReset(e) {
        animationCounter = 1;
        previousInput = Object.keys(chatBotTemp)[e];
    }

    var chatBotTemp = {
        "Hello": function () {
            responseText("Hello");
            responseText("This is a test");
            commandReset(0);
            return;
        }
    }

}

