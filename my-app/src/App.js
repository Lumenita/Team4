import React, {useState, useEffect } from 'react'
import ChatBubble from './components/ChatBubble'
import axios from 'axios';

import './components/Style.css';

 function App() {
  
  const [userID, setBackendData] = useState([{}])
  //fetching user id
  useEffect(() => {
    fetch("/users/new").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, [])

  const [text, setText] = useState()
  const[userConvo, setConvo] = useState([])
  const[botConvo, setBot] = useState('')

  const handleSubmit = event => {
    console.log('handleSubmit ran')
    event.preventDefault()
    console.log('test submission: ', text)
    
    let config = {
      headers: {
         
      }
    }
    const userSubmit = {
      sender: userID.users,
      message: text
      
    }


  
    let newText
    axios.post('http://localhost:5005/webhooks/rest/webhook', userSubmit,config)
    .then(function (response) {
          console.log(response.data[0].text)

          newText = response.data[0].text

          const newUserConvo = [...userConvo, {chatType: "User", userinput: text}, {chatType: "Bot", userinput: newText}]
          setConvo(newUserConvo)
          
          console.log(newUserConvo)
    })


     
  }

  
  
  return(
    // <div>
    //  <p>{userID.users}</p>
    // </div>

<body>
    <div class="mainPage"> 

        <div class="title">
            <span> Team 4 Chat Bot </span>
        </div>

        <div class="chatHistory">
            <ul class="chatList">
                <li class="botOutput botOutput--standard">Hello, I am chatbot 4</li>
                <li class="botOutput botOutput--standard">I can help</li>
                <li class="botOutput botOutput--standard">User ID: {userID.users}</li>

                {userConvo.map((test) => {
                  if(test.chatType === "User")
                  {
                    return(
                      
                        <li class="userInput">{test.userinput}</li>
                    )
                  }
                  else
                  {
                    return(
                      <div class="chatHistory chatList">
                      <li class="botOutput botOutput">{test.userinput}</li> 
                      </div>          
                    )
                  }


                })}

            </ul>
            
        </div>
        {/* <ChatBubble dataFromParent = {userID.users} dataFromParentTwo = {userConvo}/> */}
        <div class="chatboxArea">

            <div class="calculator">
                <a href="https://www.desmos.com/scientific">calc</a>
            </div>

            <div>
              <form action="" id="chatform" onSubmit={handleSubmit}>
                <input class="text" name="chatbox" onChange={event => setText(event.target.value)}  minLength = "2"  style ={{resize:"none"}}></input>
                <input class="submit-button" type="submit" value = "send" style ={{resize:"none"}}/> 
              </form>
             </div>

        </div>



    </div>
</body>
   
  )
}

export default App