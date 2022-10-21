//import { v4 as uuidv4 } from 'uuid';
const axios = require('axios');
const e = require('express');
const express = require("express")
const router = express.Router()

//stores all users 
let users = []

router.get("/new", (req, res) => {
    //creates new user id
    const { v4: uuidv4 } = require('uuid');
    const newID = uuidv4()
    let userobj = {"users": [newID]}
    if(!users.includes(newID))
    users.push(newID)

    let userID = JSON.stringify(newID)
    res.json(userobj)
    console.log(newID)
    console.log(users)
    

})

 router.route("/:id").get((req, res) => {
     res.send(`get user with ID ${req.params.id}`)

//When posted 
}).post((req, res) => {
    if(users.includes(req.params.id))
    {
        console.log(req.body)
        let config = {
            headers: {
               
            }
        }
        let data = req.body
    
        let botData
        axios.post('http://localhost:5005/webhooks/rest/webhook', data,config)
      .then(function (response) {
            botData = response.data
            res.send(botData)
            console.log(botData)
      })
    }
    else
    {
        res.status(404).send("user not found")
        
    }
  

//deletes user when requested
}).delete((req, res) => {
        if(users.includes(req.params.id))
        {
            users.splice(users.indexOf(req.params.id), 1)
            res.send("successful deletion")
        }
        else
        {
            res.send("user not found")
        }
        

        
})

module.exports = router