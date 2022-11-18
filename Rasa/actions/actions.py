# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# 
#
from sympy import *
import string
from pymongo import MongoClient
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import *

x, y, z, n = symbols("x y z n")


def summation(arg):
    func = arg.split(',')
    n_start = int(func[1])
    n_end = int(func[2])
    expr = sympify(func[0])
    result = Sum(expr, (n, n_start, n_end)).doit()
    
    return "$ {} = {} $".format(latex(Sum(expr, (n, n_start, n_end))), latex(result))


def big_pi(arg):
    func = arg.split(',')
    n_start = int(func[1])
    n_end = int(func[2])
    expr = sympify(func[0])
    result = Product(expr, (n, n_start, n_end)).doit()
    
    return "$ {} = {} $".format(latex(Product(expr, (n, n_start, n_end))), latex(result))

def integration(arg):
    func = arg.split(',')
    start = int(func[1])
    if func[2].__contains__('oo'):
        end = oo
    else:
        end = int(func[2])
    expr = sympify(func[0])
    LHS = latex(Integral(expr, (x, start, end)))
    result = latex(Integral(expr, (x, start, end)).doit())

    return f'$ {LHS} = {result} $'



def evaluate(func):
    expr = sympify(func, evaluate=False)
    result = expr.evalf()
    return "$ {} = {} $".format(latex(expr), latex(result))

def solver(func):
    expr = sympify(func)
    result = solve(expr)
    
    return "$ {} = {} $".format(latex(expr), latex(result))

def differentiation(func):
    expr = sympify(func)
    result = Derivative(expr).doit()
    
    return "$ {} = {} $".format(latex(Derivative(expr)), latex(result))

def indef_integral(func):
    expr = sympify(func)
    LHS = latex(Integral(expr, x))
    result = latex(integrate(expr, x))

    return f'$ {LHS} = {result} $'




# class TA_Info(Action):

#     def name(self) -> Text:
#         return "TA_Info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="The email for TA is akshay.jha@utdallas.edu")

#         return []

class TA_Info(Action):

    def name(self) -> Text:
        return "ask_Definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="The email for TA is akshay.jha@utdallas.edu")

        return []

testDefinitions_DB = {
    "Big O Notation": "We use O-notation to give an upper bound on a function, The O-notation asymptotically bounds a function from above and below.",
    "Dijkstra's Algorithm":  "Generates a SPT (shortest path tree) with a given source as a root. Maintain two sets, one set contains vertices included in the shortest-path tree, other set includes vertices not yet included in the shortest-path tree. At every step of the algorithm, find a vertex that is in the other set (set not yet included) and has a minimum distance from the source.",
    "Stack": "A stack is a linear data structure that follows the principle of Last In First Out (LIFO). This means the last element inserted inside the stack is removed first.",
    "Queue": "A queue is considered FIFO (First In First Out) to demonstrate the way it accesses data. This means that once a new element is added, all elements that were added before have to be removed before the new element can be removed.",
    "Binary Tree": "Binary Tree is defined as a Tree data structure with at most 2 children",
    "Greedy Algorithm": "A greedy algorithm is a type of algorithm always makes the choice that looks best at the moment.",
    "Dynamic Programming": "Dynamic programming is like the divide-and-conquer method, solves problems by combining the solutions to subproblems."
}
class returnDefinition(Action):
    def name(self) -> Text:
        return "tell_Definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        client = MongoClient('localhost', 27017)
        userDef = next(tracker.get_latest_entity_values("definition"), None)
        if userDef == None:
            msg = "definition not recongnized" 
            dispatcher.utter_message(text=msg)

        userDef = string.capwords(userDef)
        db = client["rasa_data"]
        col =db["definitions"]
        myquery = {"name": userDef}
        data = col.find_one(myquery)
        
        

        dispatcher.utter_message(text = data["desc"])

        return []

class returnAlgo(Action):
    def name(self) -> Text:
        return "sortAlgo"
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userDef = (tracker.latest_message)['text']
        
        userDef = userDef.split()
        bigO = []
        for x in userDef:
            if x.find("(") == 1:
                bigO.append(x.lstrip("OΩθ"))
        
        
        
        
        
        x, y, z, n = symbols("x y z n")
        func1 = bigO[0]
        func2 = bigO[1]
        top = sympify(func1)
        bot = sympify(func2)
        expr = (top / bot)
        result = limit(expr, n, oo)
        top = latex(top)
        bot = latex(bot)
        if (result == 0):
            userDef = f'$ {top} = O({bot}) $'
        elif (result == oo):
            userDef = f'$ {top} = Ω({bot}) $'
        else:
            userDef = f'$ {top} = θ({bot}) $'
        userDef = userDef.replace("**", "^")
        dispatcher.utter_message(text = userDef)
        return[]
    
class compareAlgo(Action):
    def name(self) -> Text:
        return "compareAlgo"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        client = MongoClient('localhost', 27017)

        userDef = tracker.latest_message["entities"]

    
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef[0]["value"])}

        data = col.find_one(myquery)
        myquery = {"name": string.capwords(userDef[1]["value"])}
        data2 = col.find_one(myquery)
        
        if data["speed"] < data2["speed"]:
            dispatcher.utter_message(text = "{} is faster then {}".format(data["name"], data2["name"]))
        elif data["speed"] > data2["speed"]:
            dispatcher.utter_message(text = "{} is faster then {}".format(data2["name"], data["name"]))
        elif data["speed"] == data2["speed"]:
            dispatcher.utter_message(text = "{} equal in speed with {}".format(data2["name"], data["name"]))


        return []
class algoBigO(Action):
    def name(self) -> Text:
        return "algoBigO"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        client = MongoClient('localhost', 27017)
        userDef = next(tracker.get_latest_entity_values("algo"), None)

        
        db = client["rasa_data"]
        col = db["sorting_algo"]
        myquery = {"name": string.capwords(userDef)}

        data = col.find_one(myquery)
        
        dispatcher.utter_message(text = "Worst Running Time of {}: {}".format(data["name"], data["worst"]))

        
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

class calc(Action):
    def name(self) -> Text:
        return "calc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        userDef = (tracker.latest_message)['text']
        userDef = userDef.replace("|MATH|", "")

        #summation('n', 1, 4)
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


