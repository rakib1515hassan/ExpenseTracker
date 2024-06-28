from django.conf import settings

from datetime import datetime
import requests


##NOTE:- For GET Requests
# def sms_sender(phone, msg):
#     try:
#         provider  = settings.TP_SMS_PROVIDER
#         api_key   = settings.TP_API_KEY
#         sender_id = settings.TP_SENDER_ID

#         # Validate phone number length
#         to = "+880" + phone[-10:]
#         if len(to) != 14:
#             raise ValueError('Invalid phone number length!')

#         # Construct the full URL with query parameters
#         params = {
#             'action'  : 'send-sms',
#             'api_key' : api_key,
#             'from': sender_id,
#             'to'  : '8801680764590',
#             # 'sms' : f'Digital A.H.M Packaging\n{msg}'
#             'sms' : f'Digital A.H.M Packaging'
#         }

#         # Send GET request
#         response = requests.get(provider, params=params)

#         # Parse JSON response
#         response_data = response.json()
#         print(f"Response status code: {response.status_code}")
#         print(f"Response JSON: {response_data}")

#         # Handle response
#         if response_data.get('code') == 'ok':
#             return response_data['message']
#         else:
#             raise Exception(response_data.get('message'))

#     except Exception as e:
#         print(f"Error sending SMS: {e}")
#         return None





##NOTE:- For POST Requests
def sms_sender(phone, msg):
    try:
        provider  = settings.TP_SMS_PROVIDER
        api_key   = settings.TP_API_KEY
        sender_id = settings.TP_SENDER_ID

        
        # Check phone number length
        to = "+880" + phone[-10:]
        if len(to) != 14:
            raise ValueError('Invalid phone number length!')

        # Data payload
        data = {
            'action'  : 'send-sms',
            'api_key' : api_key,
            'from' : sender_id,

            'to'   : to,
            'sms'  : msg,
            'unicode' : 1,
        }

        # print("------------------------")
        # print("Phone Number =", to)
        # print("provider =", provider)
        # print("data =", data)
        # print("------------------------")

        ## NOTE:- Send POST request
        response = requests.post(url=provider, data=data)

        # Parse JSON response
        response_data = response.json()
        print(f"Response status code: {response.status_code}")
        print(f"Response JSON: {response_data}")

        ## Message History Save
        # MessageHistory.objects.create(send_to=to, message=msg)

        """NOTE:- Response Is Look Like
            {"code":"ok","message":"Successfully Send","balance":"50000","user":"Robin"}
        """

        # Handle response
        if response_data.get('code') == 'ok':
            # return response_data['message']
            return True
        else:
            raise Exception(response_data.get('message'))

    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None






def sms_sender_multiple_number(phones, msg):
    try:
        provider = settings.TP_SMS_PROVIDER
        api_key  = settings.TP_API_KEY
        sender_id = settings.TP_SENDER_ID

        # Format phone numbers as comma-separated string
        to = ','.join(["+880" + phone[-10:] for phone in phones])

        # Data payload
        data = {
            'action'  : 'send-sms',
            'api_key' : api_key,
            'from' : sender_id,
            'to'   : to,
            'sms': msg,
            'unicode': 1,
        }

        # Send POST request
        response = requests.post(url=provider, data=data)

        # Parse JSON response
        response_data = response.json()
        print(f"Response status code: {response.status_code}")
        print(f"Response JSON: {response_data}")

        # Save message history
        for phone in phones:
            formatted_phone = "+880" + phone[-10:]
            MessageHistory.objects.create(send_to=formatted_phone, message=msg)

        # Handle response
        if response_data.get('code') == 'ok':
            return True
        else:
            raise Exception(response_data.get('message'))

    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

        







# def sms_sender(phone, msg):
#     try:
#         greenweburl = "http://api.greenweb.com.bd/api.php"
#         token = "b32c40d07064593e7576f55802b46b1d"

#         # sms receivers number here (separated by comma)
#         to = "+880" + phone[-10:]

#         if len(to) != 14:
#             raise Exception('Invalid phone number!')

#         data = {
#             'token': token,
#             'to': to,
#             'message': 'Konnect\n' + msg,
#         }

#         responses = requests.post(url=greenweburl, data=data)
#         return responses.text

#     except Exception as e:
#         print(e)
#         return None
    

