const express = require('express')
const app = express()

const axios = require('axios')

app.use(express.json())
app.use(express.urlencoded({extended: false}))


app.get("/api", (req, res) => {
    res.json({"users": ["userOne", "userTwo"]})
    console.log(data)
})

const newRouter = require("./user.js")
app.use('/users', newRouter)



app.listen(5000, () => {console.log("Server started")})