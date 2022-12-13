# Virtual TA Project Team 4

This project was made for CS4485 Senior Design Project so some of this readme will talk about the virtual machine. This project is creating a bot that can answer questions a TA could from the class Advanced Algorithms and Data Structure. This project incorporate:

* A front end website component created in React.js
* API/Routing Server created in Express.js
* A chat bot created through the Rasa Framework
* MongoDB database to store relevant information

The only part of the project that has not been included is the MongoDB database

Questions that you can query the chat bot:

 * Algorithms
     * Ask running times of algorithm
     * Compare two algorithms
     * Ask generally how each algorithm works
 * Definitons
     * Ask general definitions of common Advanced Algorithms and Data Structure
     * Over 150 definitions added 
 * Growth Function Comparisons
     * Can compare two growth functions (example O(x^2)) and will show which one will grow faster
     * Can take latex functions
 * Calculator
     * Can solve questions both symbolically and literally
     * Latex Support

## How does it work

There are currently three layers in our infrastructure Front End Layer, Middle Communication Layer, and our Back End 

![image](https://user-images.githubusercontent.com/87556821/206939350-692644fa-8256-4ec1-b491-eb14110a3125.png)

### Front End

Our front end consists of  Java Script, Node.js and React.js (Framework of Node js). Most of the components for the websites are using event hooks to decide what output of the website. The website also has an implementation of inputting math functions with a type of math syntax called latex. This was implemented through a public node module called react-latex-next. Which uses a special CSS library to correctly visually show math functions. Various math functions are shortcutted through buttons that can be clicked below the text box. This website will query all information through a API server.

### Middle Layer

he API server serves two purposes. One is to communicate the front end and back end sending messages back and forth between the two layers. The Second purpose is to log incoming messages from the back end and front end. This can be accessed by listening into the api server in the virtual machine. Although the logging is very rudimentary, the framework was set to create more functional uses for this logging system

### Back End 

There are two components of our back end. First is the Rasa Bot. This bot uses the Rasa Machine Learning Framework. Rasa creates its own data pipeline to handles query. The main component of this pipeline is a entity and intent classifiers called DIETclassifer. What DIETclassifer does, it takes examples from data on what the user is asking then breaks the data to what the user is asking (intent) and what are important keywords that are important to the question (entity). Once the intent and entity has been extracted, it will then be passed off the the action server which will take the appropriate action and send back the information. This whole part was implemented in python. The second part of the back end is the database. The database was created through MongoDB due to not needing complicated database structure. This held information related to questions the bot could be asked. This was used to make it easier to add  additional data. The data held are concepts related to Advanced Algorithm and Data Structure and info regarding to algorithms


## Deployment

This whole project is deployed and hosted through the UTD network in a virtual machine. For the website, we used nginx to host the website into the web server. Also through nginx, our API server was using a reverse proxy to change the port number of the API server. For all the other components, they were implemented as a daemon (background process) server running on the background of the VM. Most of the components had their respective startup scripts just in case the server was rebooted.

### Where is each code in the VM

Most of the code is in the /home/generic folder

/home/generic/bin are just general scripts used for the startup script in the systemctl folder

/home/generic/Bot/rasa_bot is where the rasa_bot is located

/home/generic/Bot/Website is where the Front end website code is located

/var/www/html is where the fully build website is located

/home/generic/Bot/Server is where the API server is located

/var/lib/mongo is where mongoDB data is stored

### Additonal tools and packages installed on the server

Python 3.8
* Modules installed:
    * sympy
    * rasa and its dependencies
    * fuzzywuzzy
    * Mongopy
    * latex2sympy 

Nginx 

MongoDB

Node JS
* Modules installed:
    * React.js
    * Express.js
    * react-latex-next
    * Axios
    * Katex
    * PM2
    * UUID module
    * cors module

### How to access
1. Connect to UTD vpn or be inside UTD's network
2. go to http://10.176.67.67/ or http://csa-4485-04.utdallas.edu/
