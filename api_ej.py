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
                    You are a climate change communications expert. You will be given a paragraph from a conservative think tank that possibly weaponizi or attacks environmental justice. Use this codebook to assign it a category if the paragraph alludes to any of categories.
                    
                    TEXT:
                    {statement}
                    
                    CODEBOOK:
                    <category id="1">1 - Justice weaponization: The use of justice rhetoric to oppose climate/environmental action.</category id="1">
                    <category id="1.1">1.1 - Fossil fuels / Deregulation help marginalized people</category id="1.1">
                    <category id="1.1.1">1.1.1 - Developing countries need/deserve fossil fuels.</category id="1.1.1">
                    <category id="1.2">1.2 - Pro-environment policies hurt marginalized people: Environmental regulation and climate action hurt marginalized people.</category id="1.2">
                    <category id="1.2.1">1.2.1 - Pro-environment policies increase the cost of goods and services, potentially harming marginalized communities.</category id="1.2.1">
                    <category id="1.2.2">1.2.2 - The energy transition will disproportionately hurt the developing world.</category id="1.2.2">
                    <category id="2">2 - Environmental justice as waste: Environmental or climate justice policies are a waste of government resources.</category id="2">
                    <category id="2.1">2.1 - Environmental justice initiatives add unnecessary bureaucracy</category id="2.1">
                    <category id="2.1.1">2.1.1 - Environmental justice initiatives will slow processes down necessary to address the climate emergency: The bureacratic burden created by EJ policies will hamper the development of renewable energy infrastructure.</category id="2.1.1">
                    <category id="3">3 - Environmental justice doubt: Environmental/climate injustice are not real</category id="3">
                    <category id="3.1">3.1 - Questioning the science: There is not a scientific consensus that confirms the disproportionate impacts of environmental harm on marginalized communities.</category id="3.1">
                    <category id="3.2">3.2 - Environment and justice don't mix: Social justice does not belong in environmental policies or movements.</category id="3.2">
                    <category id="3.3">3.3 - Marginalized people are to blame for their own problems</category id="3.3">
                    <category id="3.4">3.4 - Environmental justice is silly: Environmental justice ridiculous and even laughable, including sarcastic attitude to the EJ movement.</category id="3.4">
                    <category id="4">4 - Environmental justice mischaracterization.</category id="4">
                    <category id="4.1">4.1 - Environmental justice is racist: Environmental/climate justice movements/policies will only sew further division or otherwise lead to further marginalization.</category id="4.1">
                    <category id="4.2">4.2 - Environmental justice has no clear definition</category id="4.2">
                    <category id="4.3">4.3 - Environmental justice as trojan horse: Environmental/climate justice movements/policies are simply a way for politicians/activists to assert a malicious ulterior motive.</category id="4.3">

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
