

import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import Flask , render_template, json, request
chatterbot = ChatBot("Patrick")
chatterbot.set_trainer(ListTrainer)
app = Flask(__name__)
accessToken = "EAAQB0iYXKLABAC4NHvGiPIrAdRsVYsgBIkjVbYolxFoSTQKHBRiCNojTVIXHRCwZBvQKIBZBs8JQojmrLjWTCMZAcI8ZC8uXjQ0BDZCjZBv3MJjTxkdLUgZCGls7LCZAUxYLfc2QpBWUDTNZA4z6ci19JqgQZAZCZC03gLi8tcaZBBqqV4QZDZD"
verify_token = "my_vase_token_bra"
hub_verify_token = None



@app.route('/request',methods=['GET'])
def facebookrequest():
    # read the posted values from the UI
    if request.args['hub.challenge'] != None:
       challange = request.args['hub.challenge']
       hub_verify_token = request.args['hub.verify_token']
    if verify_token == hub_verify_token:
        return challange


@app.route('/request', methods=['POST'])
def facebooksendrequest():
    data = request.get_json()
    message_text ="";
    location_list = []

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][ "id"]  # the recipient's ID, which should be your page's facebook ID
		    if messaging_event.get('message',{}).get('text'):
                   	 message_text = messaging_event["message"]["text"]  # the message's text
		
		    if messaging_event.get('message',{}).get('attachments'):
			    lat = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["lat"]
			    lon = messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["long"]
			    
			    #message_text = str(lon)+"_"+str(lat)
                            location_list.append(lat)
			    location_list.append(lon)
			   # print(message_text+"it key attachment")
		    if message_text == "":
			send_message(sender_id, location_list, "user_location")
                    else:
                    	send_message(sender_id, message_text,"user_message")
		
			

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass


    return message_text, 200

def send_message(recipient_id, message_text,message_type):
    location = False
    location_received = False
    print(message_text)
    keyword_list = ['motorcycle', 'bike', 'cycle', 'dirtbike','ride','cab','taxi','driver','pick','up','down','vase','Cab','Taxi']
    if message_type != "user_location":
	    if any(word in message_text for word in keyword_list):
		message_text = "Enter your phone number"
	    elif "09" in message_text:
		location = True
	  
	
	    else:
		chatbot = ChatBot('Ron Obvious',trainer='Patrick')

# Train based on the english corpus
		#chatbot.train("chatterbot.corpus.english")
		# Train based on english greetings corpus
		#chatbot.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
		#chatbot.train("chatterbot.corpus.english.conversations")
		
# Get a response to an input statement
		chatterbot.train([message_text,])
		message_text = str(chatbot.get_response(message_text))
		

		
    else:
	
	url = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+str(message_text[0])+","+str(message_text[1])+"&sensor=true"
	r = requests.get(url)
	data = r.json()
	user_location = data["results"][0]["address_components"][0]["long_name"]
	user_location_city = data["results"][0]["address_components"][2]["long_name"]
	if user_location_city != "Lusaka":
        	message_text = "We are sorry, we don't operate in your area yet :) "
	else :
		message_text = "Sending cab to "+user_location
		print user_location




    if location:
        params = {
            "access_token": accessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Please share your location:",
                "quick_replies": [
                    {
                        "content_type": "location",
                    }
                ]
            }
        })
    else:
        params = {
            "access_token": accessToken
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


if __name__ == '__main__':
    app.run()
