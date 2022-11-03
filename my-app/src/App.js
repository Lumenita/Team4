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


 
  const handleSubmit = event => {
    console.log('handleSubmit ran')
    event.preventDefault()
    console.log('test submission: ', text);
    
    let config = {
      headers: {
         
      }
    }
    const userSubmit = {
      sender: userID.users,
      message: text
      
    }

    
    axios.post('http://localhost:5005/webhooks/rest/webhook', userSubmit,config)
    .then(function (response) {
          console.log(JSON.stringify(response.data))
    })
    
  }

  
  
  return(
    // <div>
    //  <p>{userID.users}</p>
    // </div>

    <body>
      <div>

        <div class="mainPage">
          <div class="title">
            <span> Team 4 Chat Bot </span>
          </div>

          <div class="chatHistory">
            <ul class="chatList">
              <li class="botOutput botOutput--standard">Hello, I am chatbot 4</li>
              <li class="botOutput botOutput--standard">I can help</li>
              <li class="botOutput botOutput--standard">
                <span class="botOutput--second-sentence">You can ask me anything</span>
                <ul>
                  <li class="input__nested-list">User ID: {userID.users}</li>
                </ul>
              </li>
            </ul>
          </div>

          <div class="chatboxArea">
            <div class="calculator">
              <a href="https://www.desmos.com/scientific">Calculator</a>
            </div>

            <div>
              <form action="" id="chatform" onSubmit={handleSubmit}>
                <textarea placeholder="..." class="chatbox" name="chatbox" onChange={event => setText(event.target.value)} minLength="2" style={{ resize: "none" }}></textarea>
                <input class="submit-button" type="submit" value="send" style={{ resize: "none" }} />
              </form>
            </div>
          </div>
        </div>

      </div>
    </body>
   
  )
}

export default App