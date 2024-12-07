import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

# Define the function schema
light_control_schema = {
    "name": "set_light_values",
    "description": "Set the brightness and color temperature of a room light",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "integer",
                "description": "Light level from 0 to 100. Zero is off and 100 is full brightness"
            },
            "color_temp": {
                "type": "string",
                "description": "Color temperature of the light fixture (daylight, cool, or warm)"
            }
        },
        "required": ["brightness", "color_temp"]
    }
}

def set_light_values(brightness: int, color_temp: str) -> dict:
    """Set the brightness and color temperature of a room light. (mock API)"""
    return {
        "brightness": brightness,
        "colorTemperature": color_temp
    }

try:
    # Initialize the model with proper function declaration
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{
            "function_declarations": [light_control_schema]
        }]
    )
    
    # Start chat and send message
    chat = model.start_chat()
    response = chat.send_message('Dim the lights so the room feels cozy and warm.')
    print(response)
    
    # Print function call details if available
    try:
        function_call = response.candidates[0].content.parts[0].function_call
        print("\nFunction Call Details:")
        print(f"Function: {function_call.name}")
        print(f"Arguments: {function_call.args}")
    except AttributeError:
        print("No function call was made in this response")

except Exception as e:
    print(f"Error occurred: {str(e)}")