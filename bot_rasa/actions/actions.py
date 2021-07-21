# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
#import sendgrid
import os
#from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Any, Text, Dict, List, Union
#
#from twilio.rest import Client
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, FollowupAction
#
#import js2py
import smtplib
from spacy import displacy
#from collections import Counter
import en_core_web_md
nlp = en_core_web_md.load()
import re
#from pprint import pprint
import requests
import json
import jwt
#from requests.auth import HTTPBasicAuth 

class ActionHelloWorld(Action):
#
    def name(self) -> Text:
        return "action_hello_world"
#
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
        headers = {'X-Auth-Token':'hJNgMSX8YGBbor1_6ik_NpjN7fiYVok455YND5QXqOg', 'X-User-Id':'Yntowd4YDmsGoXqqh'}
        conversation_id=tracker.sender_id
        dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        response = requests.get("http://localhost:3000/api/v1/channels.messages?roomName=general", headers=headers)
        #response = json.load(response)
        print(response.status_code)
        response = json.loads(response.text)
        #msg = response[0]
        User = []
        Bot = []
        index = []
        i = 0
        while response["messages"][i]["msg"]!="Hey! How are you?":
            if response["messages"][i]["u"]["username"]=="bot_rasa":
                Bot.append(response["messages"][i]["msg"])
                index.append("B")
            else:
                User.append(response["messages"][i]["msg"])
                index.append("U")
            i = i+1
        Bot.append(response["messages"][i]["msg"])
        index.append("B")
        i = i+1
        User.append(response["messages"][i]["msg"])
        #index.append("U")
        b = len(Bot)-1
        u = len(User)-1
        ind = len(index)-1
        strz = ("User: " + User[u] + "\n")
        u = u-1
        while ind>=0:
            if index[ind]=="U":
                       strz = strz + ("User: " + User[u] + "\n")
                       u = u-1
            if index[ind]=="B":
                       strz = strz + ("Bot: " + Bot[b] + "\n")
                       b = b-1
            ind = ind -1
        


        #    print(response["messages"][0]["msg"])
         #   print(response["messages"][1]["msg"])
        s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
        s.starttls()
  
# Authentication
        s.login("nslsample123@gmail.com", "a1b2c3d4!")
  
# message to be sent
        #message = "Message_you_need_to_send"
        message = "Chat Details: {}\n".format(strz)
        #message = "ssss"
# sending the mail
        s.sendmail("nslsample123@gmail.com", "nslsample123@gmail.com", message)
  
# terminating the session
        s.quit()
        print(strz)
        dispatcher.utter_message(text="Hello World!")
        
        return []


class ActionCreateUser(Action):

     def name(self) -> Text:
         return "action_create_user"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         #AllUsers()
         Body = {'client_id': 'ptest', 'username': 'ptesttenantadmin', 'password': 'test', 'grant_type': 'password'}
    
         headers = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'Content-Type' :'application/x-www-form-urlencoded', 'Accept-Language': 'en'}
    
         response = requests.post("https://iam.nslhub.com/auth/realms/ptest/protocol/openid-connect/token", headers=headers, data = Body)
         print(response.status_code)
         auth_response_json = response.json()
         auth_token = auth_response_json["access_token"]
         auth_token_header_value = "bearer %s" % auth_token
         dispatcher.utter_message(text="See users details")


         headers1 = {'authority' : 'ptest.qa3.nslhub.com', 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"', 'traceparent': '00-2b29240176c0f89ead3e743c85736650-774d330740f0dddf-01', 'accept-language': 'en', 'sec-ch-ua-mobile': '?0', 'authorization':auth_token_header_value, 'content-type':'application/json', 'accept':'application/json, text/plain, */*', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'origin':'https://ptest.qa3.nslhub.com', 'sec-fetch-site':'same-origin', 'sec-fetch-mode':'cors', 'sec-fetch-dest':'empty', 'referer':'https://ptest.qa3.nslhub.com/admin/adduser','cookie':'_ga=GA1.1.738583816.1615352728; _ga_GSGN4DSWQV=GS1.1.1615352728.1.1.1615352744.0'}
         Body1 = json.dumps({
            "isEnabled": True,
            "name": tracker.get_slot("firstperson"),
            "password": "test",
            "firstName": tracker.get_slot("firstperson"),
            "lastName": tracker.get_slot("lastperson"),
            "email": tracker.get_slot("email"),
            "environments": [
            "development"
            ]
         })
         response1 = requests.post("https://ptest.qa3.nslhub.com/dsd-orch/cdm/api/cdm/create/user", headers=headers1, data = Body1)
         print(response1.status_code)
         print(response1.text)
         dispatcher.utter_message(text="See users details")
         return []


class ActionGetUser(Action):

     def name(self) -> Text:
         return "action_get_user"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#tracker.get_slot("firstperson"), tracker.get_slot("lastperson"), tracker.get_slot("email"), tracker.get_slot("phno")         
         
         Body = {'client_id': 'ptest', 'username': 'ptesttenantadmin', 'password': 'test', 'grant_type': 'password'}
    
         headers = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'Content-Type' :'application/x-www-form-urlencoded', 'Accept-Language': 'en'}
    
         response = requests.post("https://iam.nslhub.com/auth/realms/ptest/protocol/openid-connect/token", headers=headers, data = Body)
         print(response.status_code)
         auth_response_json = response.json()
         auth_token = auth_response_json["access_token"]
         auth_token_header_value = "bearer %s" % auth_token

         headers1 = {'authority' : 'ptest.qa3.nslhub.com', 'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"', 'accept':'application/json, text/plain, */*', 'authorization':auth_token_header_value, 'traceparent': '00-7c0803f0e0e8dcc07f3b54a61f4b974a-7acef0c7ec0d62ed-01', 'accept-language': 'en', 'sec-ch-ua-mobile': '?0', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 'sec-fetch-site':'same-origin', 'sec-fetch-mode':'cors', 'sec-fetch-dest':'empty', 'referer':'https://ptest.qa3.nslhub.com/admin/adduser'}
         response1 = requests.get("https://ptest.qa3.nslhub.com/dsd-orch/cdm/api/cdm/users", headers=headers1)
         print(response1.status_code)
         print(response1)
         response1 = json.loads(response1.text)
         print(type(response1))
         print("aaaaaaaaa")
         print(response1)
         #print(response1['result'][0])
         dispatcher.utter_message(text="See users details")

         return []



class ActionGetSpecificUser(Action):

     def name(self) -> Text:
         return "action_get_specific_user"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#tracker.get_slot("firstperson"), tracker.get_slot("lastperson"), tracker.get_slot("email"), tracker.get_slot("phno")         
         
         Body = {'client_id': 'ptest', 'username': 'ptesttenantadmin', 'password': 'test', 'grant_type': 'password'}
    
         headers = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'Content-Type' :'application/x-www-form-urlencoded', 'Accept-Language': 'en'}
    
         response = requests.post("https://iam.nslhub.com/auth/realms/ptest/protocol/openid-connect/token", headers=headers, data = Body)
         print(response.status_code)
         auth_response_json = response.json()
         auth_token = auth_response_json["access_token"]
         #auth_token_header_value = "bearer %s" % auth_token
         decoded = jwt.decode(auth_token, options={"verify_signature": False}) # works in PyJWT >= v2.0
         print (decoded)
         #print (decoded["azp"])

         return []



class FirstDetailsForm(FormAction):
    
    def name(self):
        return "first_details_form"

    @staticmethod
    def required_slots(tracker):
            return ["firstperson"]
    

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "firstperson": [
                #self.from_entity(entity="firstperson", intent="myname"),
                self.from_text(),
            ]

        }

    def validate_firstperson(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        

        str = value
        x = str.split(" ")
        if len(x) == 1:
            print("hello")
            dispatcher.utter_message(template="utter_confirm_firstname", firstperson = value)
            return {"firstperson": value}
        find = 0
        for y in x:
            if(y.isupper()):
                find = find + 1
        
        if find == len(x):
            dispatcher.utter_message(template="utter_confirm_firstname", firstperson = value)
            return {"firstperson": value}
        
        tex = value
        doc = nlp(tex)
      #  pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])
        tagged_sent = [(w.text, w.tag_) for w in doc]
        normalized_sent = [w.capitalize() if t in ["NN","NNS","NNP","NNPS","JJ","FW","XX","ADD"] else w for (w,t) in tagged_sent]
        normalized_sent[0] = normalized_sent[0].capitalize()
        stri = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
        print(stri)
        #print(doc)
        doc = nlp(stri)
      #  pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc]) 
        
        for entity in doc.ents:
            print(entity.text + ' - ' + entity.label_)

        for entity in doc.ents:
            if entity.label_=="PERSON":
                print(entity.text + ' - ' + entity.label_)
                dispatcher.utter_message(template="utter_confirm_firstname", firstperson = entity.text)
                return {"firstperson": entity.text}        
            

        for entity in doc.ents:
            str1 = entity.text
            str2 = "Kumar"
            str3 = "Kumar is my name"
            s1 = str1 + ' ' + str2
            s2 = str1 + ' ' + str3
            s3 = str2 + ' ' + str1
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            doc3 = nlp(s3)

            count = 0
            for entity1 in doc1.ents:
              if entity1.label_=="PERSON" and entity1.text!="Kumar":
                  count  = count + 1
                  break
            for entity2 in doc2.ents:
              if entity2.label_=="PERSON" and entity2.text!="Kumar":
                  count = count + 1
                  break
            for entity3 in doc3.ents:
              if entity3.label_=="PERSON" and entity3.text!="Kumar":
                  count = count + 1
                  break
            if count == 3:
                dispatcher.utter_message(template="utter_confirm_firstname", firstperson = entity.text)
                return {"firstperson": entity.text}
        #if len(x) == 2 and x[0]!="name" and x[0].lower()!="i" and x[0].lower() != "i'm" and x[0].lower() != "me":

       # dispatcher.utter_message(template="utter_exact_first_name")
        print("Not present")
        return {"firstperson": None}

    
                 
                 
                 

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
         print("hello2")
         return []




class LastDetailsForm(FormAction):

    def name(self):
        return "last_details_form"

    @staticmethod
    def required_slots(tracker):
            return ["lastperson"]
    

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "lastperson": [
                #self.from_entity(entity="lastperson", intent="myname_last"),
                self.from_text(),
            ]

        }

    def validate_lastperson(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        str = value
        x = str.split(" ")
        if len(x) == 1:
            dispatcher.utter_message(template="utter_confirm_lastname", lastperson = value)
            return {"lastperson": value}

        find = 0
        for y in x:
            if(y.isupper()):
                find = find + 1
        
        if find == len(x):
            dispatcher.utter_message(template="utter_confirm_lastname", lastperson = value)
            return {"lastperson": value}

        tex = value
        doc = nlp(tex)
       # pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])
        tagged_sent = [(w.text, w.tag_) for w in doc]
        normalized_sent = [w.capitalize() if t in ["NN","NNS","NNP","NNPS","JJ","FW","XX","ADD"] else w for (w,t) in tagged_sent]
        normalized_sent[0] = normalized_sent[0].capitalize()
        stri = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
        print(stri)
        #print(doc)
        doc = nlp(stri)
       # pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])

        for entity in doc.ents:
            if entity.label_=="PERSON":
                print(entity.text + ' - ' + entity.label_)
                dispatcher.utter_message(template="utter_confirm_lastname", lastperson = entity.text)
                return {"lastperson": entity.text}        
            
        for entity in doc.ents:
            str1 = entity.text
            str2 = "Kumar"
            str3 = "Kumar is my name"
            s1 = str1 + ' ' + str2
            s2 = str1 + ' ' + str3
            s3 = str2 + ' ' + str1
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            doc3 = nlp(s3)

            count = 0
            for entity1 in doc1.ents:
              if entity1.label_=="PERSON" and entity1.text!="Kumar":
                  count  = count + 1
                  break
            for entity2 in doc2.ents:
              if entity2.label_=="PERSON" and entity2.text!="Kumar":
                  count = count + 1
                  break
            for entity3 in doc3.ents:
              if entity3.label_=="PERSON" and entity3.text!="Kumar":
                  count = count + 1
                  break
            if count == 3:
                dispatcher.utter_message(template="utter_confirm_lastname", lastperson = entity.text)
                return {"lastperson": entity.text}


        #if len(x) == 2 : #& x[0]!="name" & x[0].lower()!="i" & x[0].lower() != "i'm" 
    #    dispatcher.utter_message(template="utter_exact_last_name")
        print("Not present")
        return {"lastperson": None}
                 
                 
                 

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
         return []







class DetailsForm(FormAction):

    def name(self):
        return "details_form"

    @staticmethod
    def required_slots(tracker):
            return ["email","phno"]
    

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "email": [
                self.from_entity(entity="email", intent="emailid"),
                self.from_text(),
            ],
            "phno": [
                self.from_entity(entity="phno"),
                self.from_text(),
            ]

        }

    
    def validate_email(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        str = value
        x = str.split(" ")
        for y in x:
            print(y)
            if(re.search(regex, y)):
                return {"email": y}
        
        dispatcher.utter_message(text="please enter a valid email")
        return{"email": None}

    def validate_phno(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        regex = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        str = value
        x = str.split(" ")
        for y in x:
            print(y)
            if(re.search(regex, y)):
                return {"phno": y}
        
        dispatcher.utter_message(text="please enter a valid phone number")
        return{"phno": None}


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
         return []



class ActionLastName(Action):

     def name(self) -> Text:
         return "action_set"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
         #dispatcher.utter_message(text="Hello World!")
         intent= tracker.latest_message["intent"].get("name")
         if intent == "deny":
           #dispatcher.utter_message(text="Yes!")
           #return [SlotSet('lastperson', None), FollowupAction(name='last_details_form')]
           return [SlotSet('lastperson', None)]
         #else:
           #dispatcher.utter_message(text="No!")

         return []


class ActionFirstName(Action):

     def name(self) -> Text:
         return "action_set_first"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
         #dispatcher.utter_message(text="Hello World!")
         intent= tracker.latest_message["intent"].get("name")
         if intent == "deny":
           #dispatcher.utter_message(text="Yes!")
           #return [SlotSet('lastperson', None), FollowupAction(name='last_details_form')]
           return [SlotSet('firstperson', None)]
         #else:
           #dispatcher.utter_message(text="No!")

         return []