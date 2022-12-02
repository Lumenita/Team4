import React, {useState, useEffect } from 'react'
import Menu from './components/Menu'
import MenuItem from './components/Menu'
import axios from 'axios'
import './components/Style.css'
import Latex from 'react-latex-next'
import 'katex/dist/katex.min.css'
 function App() {
  
  
  const [userID, setBackendData] = useState([{}])
  //fetching user id
  //When user opens website run this function
  useEffect(() => {
    //fetches from routing server
    fetch("http://localhost:5000/users/new").then(
      response => response.json()
    ).then(
      data => {
        //sets id in data
        setBackendData(data)
        console.log(data)
      }
    )
  }, [])
  //for text in chat
  const [text, setText] = useState()

  //for querying data from back end
  const[userConvo, setConvo] = useState([])

  //for when submits a query to chat bot
  const handleSubmit = event => {
    console.log('handleSubmit ran')
    //prevents from whole component from refreshing
    event.preventDefault()
    console.log('test submission: ', text)
    //empty header
    let config = {
      headers: {
         
      }
    }
    //puts data in json format
    const userSubmit = {
      sender: userID.users,
      message: text
      
    }


  
    let newText
    //handles post request for submit
    axios.post(`http://localhost:5000/users/${userID.users}`, userSubmit,config)
    .then(function (response) {
          console.log(response.text)
      
          newText = response.data.text
          
          //creating and adding to a list of the conversation
          const newUserConvo = [...userConvo, {chatType: "User", userinput: text}, {chatType: "Bot", userinput: newText}]
          setConvo(newUserConvo)
          
          console.log(newUserConvo)
    })


     
  }
  //for buttons
  const handleClick = (name) => {
    // event.preventDefault();

    //when clicked, adds value of button
    //if chat box is empty, will just set the chatbox to the value
    //otherwise will just add to the string
    if(text !== undefined)
    setText(text + name)
    else
    setText(name)

  }


  //this is the main dom of the website
  return(
    // <div>
    //  <p>{userID.users}</p>
    // </div>

    <div class="mainPage"> 

        <div class="title">
            <span> Team 4 Chat Bot </span>
        </div>

        <div class="chatHistory">
            <ul class="chatList">
                <li class="botOutput botOutput--standard">Hello, I am Chatbot from Team 4</li>
                <li class="botOutput botOutput--standard">I can help</li>
                <li class="botOutput botOutput--standard">User ID: {userID.users}</li>
                <li class="botOutput botOutput--standard">To do math function use |MATH| flair</li>
                {userConvo.map((test) => {
                  //This is for adding to the chatlist
                  //checks if its a undefined variable, a user input or bot input
                  if(test.userinput !== undefined)
                    if(test.chatType === "User")
                    {
                      return(

                          <li class="userInput"><Latex>{test.userinput}</Latex></li>
                          
                      )
                    }
                    else
                    {
                      return(

                        <li class="botOutput botOutput--standard"><Latex>{test.userinput}</Latex></li> 
                    
                      )
                    }
                  else
                  {
                    return(

                      <li class="botOutput botOutput--standard">I can't understand your question, can you ask it differently?</li>  
                  
                    )
                    
                  }


                })}

            </ul>
            
        </div>
        {/* This is for buttons, when the user clicks the button, it will add the value of handleclick in the text box */}
        <div class="calculator">
          <button onClick = {() => handleClick('Ω')} class="calcButton calc1"> Ω </button>
          <button onClick = {() => handleClick('Θ')} class="calcButton calc2"> Θ </button>
          <button onClick = {() => handleClick('big_pi(func, lower, uper)')} class="calcButton calc3"> Π </button>
          <button onClick = {() => handleClick('summation(func,lower ,upper)')} class="calcButton calc4"> Σ </button>
          <button onClick = {() => handleClick('differentiation(function)')} class="calcButton calc5"> dx </button>
          <button onClick = {() => handleClick('evaluate(Solvable Function)')} class="calcButton calc6"> eval </button>
          <button onClick = {() => handleClick('solver(function)')} class="calcButton calc7"> solve </button>
          <button onClick = {() => handleClick('integration(func, start, end)')} class="calcButton calc8"> def ∫ </button>
          <button onClick = {() => handleClick('indef_integral(function)')} class="calcButton calc9"> indef ∫ </button>
          <button onClick = {() => handleClick('^()')} class="calcButton calc10"> exp </button>
        </div>
        <div class="chatboxArea">
            <form action="" id="chatform" onSubmit={handleSubmit}>
              <input class="chatbox" name="chatbox" onChange={event => setText(event.target.value) }value = {text}></input>
              <input class="submit-button" type="submit" value = "send"/> 
            </form>
        </div>



    </div>
            
   
  )
}

export default App