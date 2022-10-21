# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# 
#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher



class TA_Info(Action):

    def name(self) -> Text:
        return "TA_Info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="The email for TA is akshay.jha@utdallas.edu")

        return []

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
    "Stack": "A stack is a linear data structure that follows the principle of Last In First Out (LIFO). This means the last element inserted inside the stack is removed first."

}
class returnDefinition(Action):
    def name(self) -> Text:
        return "tell_Definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        userDef = next(tracker.get_latest_entity_values("definition"), None)
        
        ansDef = testDefinitions_DB.get(userDef)

        dispatcher.utter_message(text = ansDef)

        return []