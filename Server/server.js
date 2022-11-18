const express = require('express')
const app = express()
const http = require("http")
const cors = require('cors');

const axios = require('axios')

app.use(express.json())
app.use(express.urlencoded({extended: false}))
app.use(cors());


app.get("/api", (req, res) => {
    res.send("Server is running")
})

const newRouter = require("./user.js")
app.use('/users', newRouter)


const IP = "172.17.88.170"
app.listen(5000, () => {console.log("Server started")})