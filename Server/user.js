//import { v4 as uuidv4 } from 'uuid';
const axios = require('axios');
const e = require('express');
const express = require("express")
const router = express.Router()

//stores all users 
let users = [];
router.get("/new", (req, res) => {
    //creates new user id
    const { v4: uuidv4 } = require('uuid');
    let userobj = {"users": [uuidv4()]}
    if(!users.includes(uuidv4))
    users.push(uuidv4())

    let userID = JSON.stringify(uuidv4())
    res.json(userobj)

    console.log(users)
    

})

 router.route("/:id").get((req, res) => {
     res.send(`get user with ID ${req.params.id}`)

}).post((req, res) => {
    console.log(req.body)
    let config = {
        headers: {
           
        }
    }
    let data = {
        "sender": "test_user",  
        "message": "hello"
    }

    let botData
    axios.post('http://localhost:5005/webhooks/rest/webhook', data,config)
  .then(function (response) {
        botData = response.data
        res.send(botData)
  })


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