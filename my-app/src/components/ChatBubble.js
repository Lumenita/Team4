import React, {useState, useEffect} from 'react'
import "./Style.css"

function Test(wow)
{
    
    console.log(`wow ${wow}`)
    const testerino = ['Bruce', 'Clark','test']
    if(wow != null)
    {
        
        for(let x = 0; x < wow.length; x++)
        {
            testerino.push(wow[x])
        }
        console.log(testerino)
    }   
    console.log(testerino.map(test => <li key ={test} class="botOutput botOutput--standard">{test}</li>))
    return(
        
        <div>
        {testerino.map(test => <li key ={test} class="botOutput botOutput--standard">{test}</li>)}
        </div>

    
    )
}

class ChatBubble extends React.Component {
    
    


    render(){
        return(
      <div class="chatHistory">
      <ul class="chatList">
          <li class="botOutput botOutput--standard">Hello, I am chatbot 4</li>
          <li class="botOutput botOutput--standard">I can help</li>
          <li class="botOutput botOutput--standard">User ID: {this.props.dataFromParent}</li>
          
         {Test(this.props.dataFromParentTwo)}
        
              {/* <span class="botOutput--second-sentence">You can ask me anything</span>
              <ul>
                  <li class="input__nested-list">User ID: {this.props.dataFromParent}</li>
                  
              </ul> */}
      </ul>
      
    </div>
        )
    }

}
export default ChatBubble