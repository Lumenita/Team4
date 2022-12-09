# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from sympy import *
import string
from pymongo import MongoClient
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from latex2sympy2 import latex2sympy, latex2latex
x, y, z, n = symbols("x y z n")


# These next 7functions are for calculator action

# will solve sumation value
def summation(arg):

    # arg will be formated (symbol), (start), (end)
    # splits by comma and creates array
    func = arg.split(',')
    n_start = int(func[1])
    n_end = int(func[2])

    #converts into sympy notation and simplify function
    expr = sympify(func[0])
    result = Sum(expr, (n, n_start, n_end)).doit()
    
    return "$ {} = {} $".format(latex(Sum(expr, (n, n_start, n_end))), latex(result))

#solves 
def big_pi(arg):
    # arg will be formated (symbol), (start), (end)
    # splits by comma and creates array
    func = arg.split(',')
    n_start = int(func[1])
    n_end = int(func[2])

    #converts into sympy notation and simplify function
    expr = sympify(func[0])
    result = Product(expr, (n, n_start, n_end)).doit()
    
    return "$ {} = {} $".format(latex(Product(expr, (n, n_start, n_end))), latex(result))

def integration(arg):
    # arg will be formated (symbol), (start), (end)
    # splits by comma and creates array
    func = arg.split(',')
    start = int(func[1])

    # infinity is used, converts it to oo value
    if func[2].__contains__('oo'):
        end = oo
    else:
        end = int(func[2])
    expr = sympify(func[0])
    LHS = latex(Integral(expr, (x, start, end)))
    result = latex(Integral(expr, (x, start, end)).doit())

    return f'$ {LHS} = {result} $'


# solvable equations
def evaluate(func):
    expr = sympify(func, evaluate=False)
    result = expr.evalf()
    return "$ {} = {} $".format(latex(expr), latex(result))

# solvable equations
def solver(func):
    expr = latex2sympy(func)
    expr = sympify(expr)
    result = solve(expr)
    
    return "$ {} = {} $".format(latex(expr), latex(result))

# find deriavtive 
def differentiation(func):
    expr = sympify(func)
    result = Derivative(expr).doit()
    
    return "$ {} = {} $".format(latex(Derivative(expr)), latex(result))

# solves for unsolvable symbols
def indef_integral(func):
    expr = sympify(func)
    LHS = latex(Integral(expr, x))
    result = latex(integrate(expr, x))

    return f'$ {LHS} = {result} $'






##################################################################################################################
# This next area defines actions in rasa                                                                         #
# For function name, it will define the name of the explicit action denoted in the rules and domain              #
# For function run, this is the logic of the function, any text outputed by the bot will use dispatcher function #
##################################################################################################################

# When action called, will return a set value
class TA_Info(Action):

    def name(self) -> Text:
        return "ask_Definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="The email for TA is akshay.jha@utdallas.edu")

        return []

# This action when a user ask for a definition. This will query a database and return
# the answer
class returnDefinition(Action):
    def name(self) -> Text:
        return "tell_Definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # connects to Mongodb database
        client = MongoClient('localhost', 27017)
        db = client["rasa_data"]
        col = db["definitions"]

        name = col.find({})
        nameList = []
        for x in name:
            nameList.append(x["name"])

        

        userDef = next(tracker.get_latest_entity_values("definition"), None)
        if userDef == None:
            userDef = next(tracker.get_latest_entity_values("algo"), None)
            
        
        #capitilizing words
        

        
        if userDef != None:
            fuzzSearch = process.extract(userDef, nameList, limit = 2)

            if fuzzSearch[0][1] > 70:
                

                #looks for query
                myquery = {"name": fuzzSearch[0][0]}
                data = col.find_one(myquery)
                
                # returns definition
                dispatcher.utter_message(text = data["desc"])
            else:
                dispatcher.utter_message(text = f"sorry I do not know what {userDef} is")
        else:
            userDef = (tracker.latest_message)['text']
            fuzzSearch = process.extract(userDef, nameList, limit = 2)
            if fuzzSearch[0][1] > 60:
                

                #looks for query
                myquery = {"name": fuzzSearch[0][0]}
                data = col.find_one(myquery)
                
                # returns definition
                dispatcher.utter_message(text = data["desc"])
            else:
                dispatcher.utter_message(text = f"sorry I do not know what what definition you asked there may be a typo")
        return []



class returnAlgo(Action):
    def name(self) -> Text:
        return "sortAlgo"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userDef = (tracker.latest_message)['text']

        var = ""
        if userDef.__contains__("O("):
            var = "O"
        elif userDef.__contains__("Θ("):
            var = "Θ"
        elif userDef.__contains__("Ω("):
            var = "Ω"
        
        userDef = userDef.split()
        bigO = []
        for x in userDef:
            if x.find("(") == 1:
                bigO.append(x.lstrip("OΩΘ"))







        x, y, z, n = symbols("x y z n")
        
        func1 = latex2sympy(bigO[0])
        func2 =  latex2sympy(bigO[1])
        top = sympify(func1)
        bot = sympify(func2)
        expr = (top / bot)
        result = limit(expr, n, oo)
        top = latex(top)
        bot = latex(bot)
        if (result == 0):
            userDef = f'$ {var}({top}) < {var}({bot}) $'
        elif (result == oo):
            userDef = f'$ {var}({top}) > {var}({bot}) $'
        else:
            userDef = f'$ {var}({top}) = {var}({bot}) $'
        userDef = userDef.replace("**", "^")
        dispatcher.utter_message(text = userDef)
        return[]

    
# this is for comparing two algorithm 
# example: Which is faster Merge Sort or Selection Sort
class compareAlgo(Action):
    def name(self) -> Text:
        return "compareAlgo"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        client = MongoClient('localhost', 27017)

        # looks for entities
        userDef = tracker.latest_message["entities"]

        # querying database for speed of each algorithm
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef[0]["value"])}
        data = col.find_one(myquery)
        myquery = {"name": string.capwords(userDef[1]["value"])}
        data2 = col.find_one(myquery)
        
        # returns which algorithm is faster
        if data["speed"] < data2["speed"]:
            dispatcher.utter_message(text = "{} is faster then {}".format(data["name"], data2["name"]))
        elif data["speed"] > data2["speed"]:
            dispatcher.utter_message(text = "{} is faster then {}".format(data2["name"], data["name"]))
        elif data["speed"] == data2["speed"]:
            dispatcher.utter_message(text = "{} equal in speed with {}".format(data2["name"], data["name"]))


        return []
    
# These next 3 algorithms ask for run time cases of each algorithm
class algoBigO(Action):
    def name(self) -> Text:
        return "algoBigO"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        client = MongoClient('localhost', 27017)
        db = client["rasa_data"]
        col = db["sorting_algo"]

        name = col.find({})
        nameList = []
        for li in name:
            nameList.append(li["name"])


        userDef = next(tracker.get_latest_entity_values("algo"), None)

        if(userDef != None):

            myquery = {"name": string.capwords(userDef)}

            data = col.find_one(myquery)

            dispatcher.utter_message(text = "Worst Running Time of {}: {}".format(data["name"], data["worst"]))
        else:
            userDef = (tracker.latest_message)['text']
            fuzzSearch = process.extract(userDef, nameList, limit = 2)
            if fuzzSearch[0][1] > 60:
                

                #looks for query
                myquery = {"name": fuzzSearch[0][0]}
                data = col.find_one(myquery)
                
                # returns definition
                dispatcher.utter_message(text = "Worst Running Time of {}: {}".format(data["name"], data["worst"]))
            else:
                dispatcher.utter_message(text = "sorry I do not know what you asked, maybe you meant {}".format(data["name"]))
              
        
        return[]
class algoBigTheta(Action):
    def name(self) -> Text:
        return "algoBigTheta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient('localhost', 27017)

        userDef = next(tracker.get_latest_entity_values("algo"), None)

        
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef)}

        data = col.find_one(myquery)
        
        dispatcher.utter_message(text = "Average Running Time of {}: {}".format(data["name"], data["average"]))

        
        return[]
class algoBigOmega(Action):
    def name(self) -> Text:
        return "algoBigOmega"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient('localhost', 27017)

        userDef = next(tracker.get_latest_entity_values("algo"), None)

        
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef)}

        data = col.find_one(myquery)
        
        dispatcher.utter_message(text = "Best Running Time of {}: {}".format(data["name"], data["best"]))

        return[]

# will ouput all runtimes
class theRunTime(Action):
    def name(self) -> Text:
        return "run_time"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient('localhost', 27017)

        userDef = next(tracker.get_latest_entity_values("algo"), None)

        
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef)}

        data = col.find_one(myquery)
        
        dispatcher.utter_message(text = "Best Running Time of {}: {} \nAverage Running Time of {}: {} \nWorst Running Time of {}: {}".format(data["name"], data["best"], data["name"], data["average"], data["name"], data["worst"]))

        return[]

# will calculate math queries by using the 
class calc(Action):
    def name(self) -> Text:
        return "calc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        userDef = (tracker.latest_message)['text']
        userDef = userDef.replace("|MATH|", "")

        # Decides which question is asked
        if userDef.__contains__("summation"):
            userDef = userDef.replace("summation", "")
            userDef = userDef.replace(")", "")
            userDef = userDef.replace("(", "")
            dispatcher.utter_message(text = summation(userDef))
            
        elif userDef.__contains__("big_pi"):
            userDef = userDef.replace("big_pi", "")
            userDef = userDef.replace(")", "")
            userDef = userDef.replace("(", "")
            dispatcher.utter_message(text = big_pi(userDef))

        elif userDef.__contains__("evaluate"):
            userDef = userDef.replace("evaluate", "")
            dispatcher.utter_message(text = evaluate(userDef))

        elif userDef.__contains__("solver"):
            userDef = userDef.replace("solver", "")
            userDef = userDef.replace("$", "")
            dispatcher.utter_message(text = solver(userDef))

        elif userDef.__contains__("differentiation"):
            userDef = userDef.replace("differentiation", "")
            dispatcher.utter_message(text = differentiation(userDef))

        elif userDef.__contains__("indef_integral"):
            userDef = userDef.replace("indef_integral", "")
            dispatcher.utter_message(text = indef_integral(userDef))

        elif userDef.__contains__("integration"):
            userDef = userDef.replace("integration", "")
            userDef = userDef.replace(")", "")
            userDef = userDef.replace("(", "")
            dispatcher.utter_message(text = integration(userDef))
        return[]


