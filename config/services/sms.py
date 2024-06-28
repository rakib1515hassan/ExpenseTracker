from config.env import env



## SMS Service Configuration (Message Send)
SMS_PROVIDER = env('SMS_PROVIDER', default='')
TWILIO_ACCOUNT_SID  = env('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN   = env('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER', default='')