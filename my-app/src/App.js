import React, { useEffect, useState } from 'react'

function App() {

  const [backEndData, setBackendData] = useState([{}])

  useEffect(() => {
    fetch("/users/new").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, [])

  
  return(
  //  <div>
  //   <p>{backEndData.users}</p>
  //  </div>
  <body>
    <div>
      
    </div>
  </body>
 
   
  )
}

export default App