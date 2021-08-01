# This function reads Shadow data (temperature in fahrenheit) from 
# IOT Core and returns it as a value for Amazon Connect to consume 
# and speak out. Adjust the regeion, thing name, and specific values
# to match your use case if you'll be using it. 

import json
import boto3
import logging
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Change region if different   
client = boto3.client('iot-data', region_name='us-east-1')
 
def lambda_handler(event, context):
    
    # Plenty of logging for troubleshooting purposes 
    logger.info("Attempting to fetch Shadow State")
    
    # Query Shadow and convert to Python Dictionary 
    # Change thingName to match your device if reusing
    response = client.get_thing_shadow(thingName='RaspberryPi')
    logger.info("Shadow State Received")
    res = response['payload'].read()
    res_json = json.loads(res)

    # status is all of the Shadow data.  Keeping for logging but not using
    status = res_json['state']['reported']
    # temperaturef is the specific value we want to isolate and return 
    temperaturef = res_json['state']['reported']['temp']

    # Log all of the data received and then the specific temperature
    logger.info("Received From IoT: " + json.dumps(status))
    logger.info("Returning temperaturef: " + temperaturef)
    logger.info("All done!\n")
     
    #Return temperature to Amazon Connect
    return {'message': 'Success',
            'temperaturef' : temperaturef,
    }
   

