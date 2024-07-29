from openai import OpenAI, OpenAIError
import re

# Define the APIEJClient class
class APIEJClient():
    def __init__(self, api_key):
        self.api_key = api_key
        self.default_model = "gpt-4-turbo"
        self.temperature = 0
        self.max_tokens = 1500
        self.client = OpenAI(api_key=self.api_key)  # Initialize the OpenAI client here

    def validate_api_key(self):
        try:
            self.client.models.list()
        except Exception as e:
            raise OpenAIError("Invalid API key.") from e

    # Automatic chain of thought. 
    def ACoT_pipeline(self, statement):
        messages = [{"role": "system", "content":f"""
                    You are a climate change communications expert. You will be given a paragraph from a conservative think tank that possibly weaponizes or attacks environmental justice. Use this codebook to assign it a category.
                    
                    TEXT:
                    {statement}
                    
                    CODEBOOK:
                    <category id="1">1 - Justice weaponization</category>
                    <category id="1.1">1.1 - Fossil fuels / Deregulation help marginalized people</category>
                    <category id="1.1.1">1.1.1 - Developing countries need fossil fuels</category>
                    <category id="1.2">1.2 - Pro-environment policies hurt marginalized people</category>
                    <category id="1.2.1">1.2.1 - Pro-environment policies increase the cost of goods and services</category>
                    <category id="1.2.2">1.2.2 - The energy transition will disproportionately hurt the developing world</category>
                    <category id="2">2 - EJ as waste</category>
                    <category id="2.1">2.1 - EJ initiatives add unnecessary bureaucracy</category>
                    <category id="2.1.1">2.1.1 - EJ initiatives will slow processes down necessary to address the climate emergency</category>
                    <category id="3">3 - EJ doubt</category>
                    <category id="3.1">3.1 - Questioning the science</category>
                    <category id="3.2">3.2 - Envs and justice don't mix</category>
                    <category id="3.3">3.3 - Marginalized people are to blame for their own problems</category>
                    <category id="3.4">3.4 - EJ is silly</category>
                    <category id="4">4 - EJ mischaracterization</category>
                    <category id="4.1">4.1 - EJ is racist</category>
                    <category id="4.2">4.2 - EJ has no clear definition</category>
                    <category id="4.3">4.3 - EJ as trojan horse</category>

                    IMPORTANT:
                    - If none of the categories fit, please assign the category of '0.0'. 
                    
                    DESIRED OUTPUT FORMAT:
                    Return a python list of claim numbers (strings). 
                    """},
                    {"role":"user", "content": "A) Let's think step by step"}]

        response_object = self.client.chat.completions.create(model=self.default_model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature)
        
        response = response_object.choices[0].message.content
        result = self.extract_list(response)
        
        return result, response
    
    #Extract the final claim list from the chain of thought response. Using Regex.
    def extract_list(self, text):
        # Define the regular expression pattern to match the list with the specific condition
        pattern = r"\[(.*?\d+\.\d+.*?)\]"
        
        # Search for the pattern in the text
        match = re.search(pattern, text)
        
        if match:
            # Extract the list contents as a string
            list_str = match.group(1)
            
            # Convert the string to a list
            extracted_list = eval(f"[{list_str}]")
            
            return extracted_list
        else:
            return None
