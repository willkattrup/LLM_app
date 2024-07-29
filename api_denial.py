from openai import OpenAI, OpenAIError
import re

# Define the APIClient class
class APIClient():
    def __init__(self, api_key):
        self.api_key = api_key
        self.default_model = "gpt-4-turbo"
        self.temperature = 0
        self.max_tokens = 1500
        self.denial_subclaims = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "5.1", "5.2", "5.3"]
        self.delay_subclaims = ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "4.7", "5.4"]
        self.client = OpenAI(api_key=self.api_key)  # Initialize the OpenAI client here

    def validate_api_key(self):
        try:
            self.client.models.list()
        except Exception as e:
            raise OpenAIError("Invalid API key.") from e

    # Automatic chain of thought. 
    def ACoT_pipeline(self, statement):
        messages = [{"role": "system", "content":f"""
                    You are a climate change communications expert. You will be given a paragraph that possibly alludes to climate skepticism. Use this codebook to assign it a category.
                    
                    TEXT:
                    {statement}
                    
                    CODEBOOK:
                    <claim id="1.1">1.1 - Ice isn’t melting </claim id="1.2">
                    <claim id="1.2">1.2 - Heading into ice age</claim id="1.2">
                    <claim id="1.3">1.3 - Weather is cold</claim id="1.3">
                    <claim id="1.4">1.4 - Hiatus in warming</claim id="1.4">
                    <claim id="1.5">1.5 - Oceans are cooling</claim id="1.5">
                    <claim id="1.6">1.6 - Sea level rise exaggerated</claim id="1.6">
                    <claim id="1.7">1.7 - Extremes not increasing</claim id="1.7">
                    <claim id="1.8">1.8 - Changed the name from global warming to climate change</claim id="1.8">
                    <claim id="2.1">2.1 - GHGs are not causing global warming - it’s natural cycles</claim id="2.1">
                    <claim id="2.2">2.2 No evidence for Greenhouse Effect:</claim id="2.2">
                    <claim id="2.3">2.3 - CO₂ not rising</claim id="2.3">
                    <claim id="2.4">2.4 - Emissions not raising CO₂ levels</claim id="2.4">
                    <claim id="3.1">3.1 Climate impacts are not bad - Sensitivity is low</claim id="3.1">
                    <claim id="3.2">3.2 Climate impacts are not bad - No species impact of climate change</claim id="3.2">
                    <claim id="3.3">3.3 Climate impacts are not bad</claim id="3.3">
                    <claim id="3.4">3.4 Climate impacts are not bad - Only a few degrees change</claim id="3.4">
                    <claim id="3.5">3.5 Climate impacts are not bad - No link to conflict</claim id="3.5">
                    <claim id="3.6">3.6 Climate impacts are not bad - Only positive health impacts</claim id="3.6">
                    <claim id="3.7">3.7 Climate impacts are not bad - Only positive economic impacts</claim id="3.7">
                    <claim id="4.1">4.1 - Climate policies are harmful</claim id="4.1">
                    <claim id="4.2">4.2 - Climate policies are ineffective</claim id="4.2">
                    <claim id="4.3">4.3 Mitigation policies are unnecessarily or secondary</claim id="4.3">
                    <claim id="4.4">4.4 Climate policy is too difficult</claim id="4.4">
                    <claim id="4.5">4.5 Climate-friendly alternatives won’t work (harmful or ineffective).</claim id="4.5">
                    <claim id="4.6">4.6 We need fossil fuels (they are good, necessary, or clean)</claim id="4.6">
                    <claim id="4.7">4.7 No need for more climate action</claim id="4.7">
                    <claim id="5.1">5.1 Science is unreliable --No consensus; --Data/proxies are unreliable; --Temperature is unreliable; or --Models are unreliable</claim id="5.1">
                    <claim id="5.2">5.2 Movement is unreliable</claim id="5.2">
                    <claim id="5.3">5.3 Climate science is conspiracy</claim id="5.3">
                    <claim id="5.4">5.4 Climate policy is conspiracy</claim id="5.4">

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
        claims_list = self.extract_list(response)

        if any(subclaim in claims_list for subclaim in self.denial_subclaims):
            result = 2
        elif any(subclaim in claims_list for subclaim in self.delay_subclaims):
            result = 1
        else:
            result = 0
        
        return result, response, claims_list
    
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