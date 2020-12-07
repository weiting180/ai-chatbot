# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ActionReverted, EventType, FollowupAction, SlotSet, UserUtteranceReverted
from rasa_sdk.forms import FormValidationAction
from rasa.nlu.utils import write_json_to_file
from _datetime import datetime
import yaml
import re


class ValidateUserProfileForm(FormValidationAction):
    def name(self):
        return "validate_user_profile_form"
    
    def validate_name(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the name format: is it composed of alphabets?
        """
        if slot_value.replace(" ", "").isalpha() == False:
            dispatcher.utter_message("Name should be composed of alphabets, please enter again.")
            return {"name": None}
        else:
            return {"name": slot_value}

    def validate_birth(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the birth format: is it in mm/dd/yyyy format?
        """
        try:
            datetime.strptime(slot_value, "%m/%d/%Y")
        except ValueError:
            dispatcher.utter_message("Wrong date format. Please enter again.")
            return {"birth": None}
        else:
            return {"birth": slot_value}
        
    def validate_city(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the city value: does it exist in our city lookup table?
        """
        with open("data/city.yml") as file:
            city_list = yaml.load(file, Loader=yaml.FullLoader)
            
        city_list = city_list.get('nlu')[0].get('examples')
        city_list = city_list[2:-1].split('\n- ')
        
        if slot_value.title() in city_list:
            return {"city": slot_value.title()}
        else:
            dispatcher.utter_message("City doesn't exist. Please try again.")
            return {"city": None}
        
    def validate_state(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the state value: does it exist in our state lookup table?
        """
        with open("data/state.yml") as file:
            state_list = yaml.load(file, Loader=yaml.FullLoader)
            
        state_list = state_list.get('nlu')[0].get('examples')
        state_list = state_list[2:-1].lower().split('\n- ')
        
        if slot_value.lower() in state_list:
            if len(slot_value) == 2:      
                return {"state": slot_value.upper()}
            else:
                return {"state": slot_value.title()}
        else:
            dispatcher.utter_message("State doesn't exist. Please try again.")
            return {"state": None}
    
    def validate_zipcode(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the zipcode format: does it match the 5-digit format?
        """
        pattern = re.compile('\d{5}')
        if pattern.fullmatch(slot_value) != None:
            return {"zipcode": slot_value}
        else:
            dispatcher.utter_message("Invalid zipcode. Please try again.")
            return {"zipcode": None}
    
    def validate_phone(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the phone format: does it match the 10-digit format?
        """
        pattern = re.compile('\d{10}')
        slot_value = slot_value.replace("-", "").replace("(", "").replace(")", "")
        if pattern.fullmatch(slot_value) != None:
            return {"phone": slot_value}
        else:
            dispatcher.utter_message("Invalid phone number. Please enter again.")
            return {"phone": None}
    
    def validate_email(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the email format: is it a valid email format?
        """
        pattern = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if pattern.search(slot_value) == None:
            dispatcher.utter_message("Invalid email format. Please enter again.")
            return {"email": None}
        else:
            return {"email": slot_value}
    
class ValidateCoapplicantForm(FormValidationAction):
    def name(self):
        return "validate_coapplicant_form"
    
    def validate_coname(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's name format: is it composed of alphabets?
        """
        if slot_value.replace(" ", "").isalpha() == False:
            dispatcher.utter_message("Name should be composed of alphabets, please enter again.")
            return {"coname": None}
        else:
            return {"coname": slot_value}
        
    def validate_cobirth(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's birth date format: is it in mm/dd/yyyy format?
        """
        try: 
            datetime.strptime(slot_value, "%m/%d/%Y")
        except ValueError:
            dispatcher.utter_message("Wrong date format. Please enter again.")
            return {"cobirth": None}
        else:
            return {"cobirth": slot_value}
        
    def validate_coemail(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's email format: is it a valid email format?
        """
        pattern = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if pattern.search(slot_value) == None:
            dispatcher.utter_message("Invalid email format. Please enter again.")
            return {"coemail": None}
        else:
            return {"coemail": slot_value}
        
    def validate_cophone(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's phone format: does it match the 10-digit format?
        """
        pattern = re.compile('\d{10}')
        slot_value = slot_value.replace("-", "").replace("(", "").replace(")", "")
        if pattern.fullmatch(slot_value) != None:
            return {"cophone": slot_value}
        else:
            dispatcher.utter_message("Invalid phone number. Please enter again.")
            return {"cophone": None}
        
    def validate_cocity(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's city value: does it exist in our city lookup table?
        """
        with open("data/city.yml") as file:
            city_list = yaml.load(file, Loader=yaml.FullLoader)
            
        city_list = city_list.get('nlu')[0].get('examples')
        city_list = city_list[2:-1].split('\n- ')
        
        if slot_value.title() in city_list:
            return {"cocity": slot_value.title()}
        else:
            dispatcher.utter_message("City doesn't exist. Please try again.")
            return {"cocity": None}
        
    def validate_costate(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's state value: does it exist in our state lookup table?
        """
        with open("data/state.yml") as file:
            state_list = yaml.load(file, Loader=yaml.FullLoader)
            
        state_list = state_list.get('nlu')[0].get('examples')
        state_list = state_list[2:-1].lower().split('\n- ')
        
        if slot_value.lower() in state_list:
            if len(slot_value) == 2:      
                return {"costate": slot_value.upper()}
            else:
                return {"costate": slot_value.title()}
        else:
            dispatcher.utter_message("State doesn't exist. Please try again.")
            return {"costate": None}
    
    def validate_cozipcode(self, slot_value: Any, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict"):
        """
        Validate the coapplicant's zipcode format: does it match the 5-digit format?
        """
        pattern = re.compile('\d{5}')
        if pattern.fullmatch(slot_value) != None:
            return {"cozipcode": slot_value}
        else:
            dispatcher.utter_message("Invalid zipcode. Please try again.")
            return {"cozipcode": None}

class ValidatePurposeForm(FormValidationAction):
    def name(self):
        return "validate_purpose_form"
    
    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict") -> List[Text]:
        if tracker.get_slot("loan") == "student":
            return ["education", "gpa"]
        elif tracker.get_slot("loan") == "personal":
            if tracker.get_slot("empstatus") in ["Working Full-Time", "Working Part-Time"]:
                return ["empstatus", "empname", "salary"]
            elif tracker.get_slot("empstatus") == "Self-Employed":
                return ["empstatus", "salary"]
            else:
                return ["empstatus"]
        elif tracker.get_slot("debt") == "credit card":
            if tracker.get_slot("agreement") == "Yes":
                return ["agreement", "ssn"]
            else:
                return ["agreement"]
        elif tracker.get_slot("debt") == "mortgage":
            return ["amount", "period"]
        elif tracker.get_slot("purchase") == "car":
            return ["insurance", "owncar", "record", "drivexp"]
        elif tracker.get_slot("purchase") == "house":
            return ["housestat", "household", "marital", "dependents"]
        elif tracker.get_slot("purpose") == "retirement":
            return ["retiredate", "salary", "expense", "anydebt"]
        
class ActionSlotReset(Action):
    def name(self):
        return "action_reset_slot"
    
    def run(self, dispatcher, tracker, domain):
        message_obtained = tracker.latest_message.get("text")

        if message_obtained == "Name is wrong.":
            return [SlotSet("name", None)]
        elif message_obtained == "Gender is wrong.":
            return [SlotSet("gender", None)]
        elif message_obtained == "Birthday is wrong.":
            return [SlotSet("birth", None)]
        elif message_obtained == "Street is wrong.":
            return [SlotSet("street", None)]
        elif message_obtained == "City is wrong.":
            return [SlotSet("city", None)]
        elif message_obtained == "State is wrong.":
            return [SlotSet("state", None)]
        elif message_obtained == "Zipcode is wrong.":
            return [SlotSet("zipcode", None)]
        elif message_obtained == "Country is wrong.":
            return [SlotSet("country", None)]
        elif message_obtained == "Phone is wrong.":
            return [SlotSet("phone", None)]
        elif message_obtained == "Email is wrong.":
            return [SlotSet("email", None)]
        elif message_obtained == "Education level is wrong.":
            return [SlotSet("education", None)]
        elif message_obtained == "Employment status is wrong.":
            return [SlotSet("empstatus", None)]
        elif message_obtained == "Employment name is wrong.":
            return [SlotSet("empname", None)]
        elif message_obtained == "Number of dependents is wrong.":
            return [SlotSet("dependents", None)]
        elif message_obtained == "Number of household member is wrong.":
            return [SlotSet("household", None)]
        elif message_obtained == "House status is wrong.":
            return [SlotSet("housestat", None)]
        elif message_obtained == "Marital status is wrong.":
            return [SlotSet("marital", None)]
        elif message_obtained == "Co-applicant's name is wrong.":
            return [SlotSet("coname", None)]
        elif message_obtained == "Co-applicant's birthday is wrong.":
            return [SlotSet("cobirth", None)]
        elif message_obtained == "Co-applicant's email is wrong.":
            return [SlotSet("coemail", None)]
        elif message_obtained == "Co-applicant's phone number is wrong.":
            return [SlotSet("cophone", None)]
        elif message_obtained == "Co-applicant's street name is wrong.":
            return [SlotSet("costreet", None)]
        elif message_obtained == "Co-applicant's city name is wrong.":
            return [SlotSet("cocity", None)]
        elif message_obtained == "Co-applicant's country name is wrong.":
            return [SlotSet("cocountry", None)]
        elif message_obtained == "Co-applicant's state name is wrong.":
            return [SlotSet("costate", None)]
        elif message_obtained == "Co-applicant's zipcode is wrong.":
            return [SlotSet("cozipcode", None)]
        elif message_obtained == "GPA is wrong.":
            return [SlotSet("gpa", None)]
        elif message_obtained == "Salary is wrong.":
            return [SlotSet("gpa", None)]
        elif message_obtained == "Change the consent on the agreement.":
            return [SlotSet("agreement", None)]
        elif message_obtained == "SSN is wrong.":
            return [SlotSet("ssn", None)]
        elif message_obtained == "Period is wrong.":
            return [SlotSet("period", None)]
        elif message_obtained == "Loan amount is wrong.":
            return [SlotSet("amount", None)]
        elif message_obtained == "Item is wrong.":
            return [SlotSet("item", None)]
        elif message_obtained == "Insurance slot needs change.":
            return [SlotSet("insurance", None)]
        elif message_obtained == "Record slot needs change.":
            return [SlotSet("record", None)]
        elif message_obtained == "Drive experience slot needs change.":
            return [SlotSet("drivexp", None)]
        elif message_obtained == "Own cars slot needs change.":
            return [SlotSet("owncar", None)]
        elif message_obtained == "Retirement date is wrong.":
            return [SlotSet("retiredate", None)]
        elif message_obtained == "Salary needs change.":
            return [SlotSet("salary", None)]
        elif message_obtained == "Any debt records needs change.":
            return [SlotSet("anydebt", None)]
        
class ActionCheckPurpose(Action):
    def name(self):
        return "action_check_purpose"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        message = tracker.latest_message.get("text")
        if "back" in message.lower():
            if tracker.get_slot("debt") != None:
                return [SlotSet("debt", None)]
            elif tracker.get_slot("purpose") != None:
                return [SlotSet("purpose", None)]
        elif "debt" in message.lower():
            return [SlotSet("purpose", "debt")]
        elif "purchase" in message.lower():
            return [SlotSet("purpose", "purchase")]
        elif "retirement" in message.lower():
            return [SlotSet("purpose", "retirement")]
        elif "bankruptcy" in message.lower():
            return [SlotSet("purpose", "bankruptcy")]
        elif "loan" in message.lower():
            return [SlotSet("debt", "loan")]
        elif "credit card" in message.lower():
            return [SlotSet("debt", "credit card")]
        elif "mortgage" in message.lower():
            return [SlotSet("debt", "mortgage")]
        elif "car" in message.lower():
            return [SlotSet("purchase", "car")]
        elif "house" in message.lower():
            return [SlotSet("purchase", "house")]
        elif "student" in message.lower():
            return [SlotSet("loan", "student")]
        elif "personal" in message.lower():
            return [SlotSet("loan", "personal")]

class ActionSwitchPurpose(Action):
    def name(self):
        return "action_switch_purpose"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        purpose = tracker.get_slot("purpose")
        debt = tracker.get_slot("debt")
        loan = tracker.get_slot("loan")
        purchase = tracker.get_slot("purchase")
        
        if purpose == None:
            dispatcher.utter_message(template="utter_ask_purpose")
        elif loan != None:
            dispatcher.utter_message(template="utter_confirm_purpose1")
        elif purpose == "debt" and debt != "loan" and debt != None:
            dispatcher.utter_message(template="utter_confirm_purpose2")
        elif purchase != None:
            dispatcher.utter_message(template="utter_confirm_purpose3")
        elif debt == "loan":
            dispatcher.utter_message(template="utter_ask_loan")
        elif purpose == "debt":
            dispatcher.utter_message(template="utter_ask_debt")
        elif purpose == "purchase":
            dispatcher.utter_message(template="utter_ask_purchase")      
        else:
            dispatcher.utter_message(template="utter_confirm_purpose4")
            
class ActionResetPurposeForm(Action):
    def name(self):
        return "action_reset_purpose_slots"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        return [SlotSet("purpose", None), SlotSet("debt", None), SlotSet("loan", None), SlotSet("purchase", None)]

class ActionExportSlots(Action):
    def name(self):
        return "action_export_slots"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict):
        write_json_to_file("out.json", tracker.slots)
        dispatcher.utter_message(template="utter_submit", attachment="out.json")
        return []