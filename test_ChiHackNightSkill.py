import ChiHackNightSkill
import json


with open('lambda_test_events/WelcomeIntent.txt') as data_file:    
    event = json.load(data_file)

ChiHackNightSkill.lambda_handler(event, {})
