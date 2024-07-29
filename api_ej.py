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
                    <category id="1">1 - Justice weaponization: The use of justice rhetoric to oppose climate/environmental action.</category>
                    <category id="1.1">1.1 - Fossil fuels / Deregulation help marginalized people: Fossil fuels, deregulation, and the BAU help marginalized people or otherwise bring them justice.</category>
                    <category id="1.1.1">1.1.1 - Developing countries need fossil fuels: Developing countries deserve fossil fuels in order to provide for themselves and/or grow their economies.</category>
                    <category id="1.2">1.2 - Pro-environment policies hurt marginalized people: Environmental regulation and climate action hurt marginalized people or otherwise do them an injustice.</category>
                    <category id="1.2.1">1.2.1 - Pro-environment policies increase the cost of goods and services: Environmental regulation and climate action increase the cost of goods and services, thus disproportionately harming marginalized communitites.</category>
                    <category id="1.2.2">1.2.2 - The energy transition will disproportionately hurt the developing world: The clean energy transition will hurt people in the developing world, whether by preventing them from accessing affordable energy or forcing them to engage in harmful labor in order to gather the resources necessary for clean energy technology</category>
                    <category id="2">2 - EJ as waste: Environmental or climate justice policies are a waste of government resources.</category>
                    <category id="2.1">2.1 - EJ initiatives add unnecessary bureaucracy: Adding social justice into environmental regulation creates further bureacratic burden that slows projects or is otherwise unfair to businesses.</category>
                    <category id="2.1.1">2.1.1 - EJ initiatives will slow processes down necessary to address the climate emergency: The bureacratic burden created by EJ policies will hamper the development of renewable energy infrastructure.</category>
                    <category id="3">3 - EJ doubt: Environmental/climate injustice are not real; policies to address these injustices are unnecessary.</category>
                    <category id="3.1">3.1 - Questioning the science: There is not a scientific consensus that confirms the disproportionate impacts of environmental harm on marginalized communities.</category>
                    <category id="3.2">3.2 - Envs and justice don't mix: Social justice does not belong in environmental policies or movements.</category>
                    <category id="3.3">3.3 - Marginalized people are to blame for their own problems: Marginalized people suffer disparate health outcomes or other negative environmental impacts as a result of their own choices.</category>
                    <category id="3.4">3.4 - EJ is silly: The concept of environmenatal/climate in/justice is ridiculous and even laughable, including sarcastic attitude to the EJ movement.</category>
                    <category id="4">4 - EJ mischaracterization: Environmental justice movements/policies don't concern [blank], they actually concern [blank].</category>
                    <category id="4.1">4.1 - EJ is racist: Environmental/climate justice movements/policies will only sew further division or otherwise lead to further marginalization.</category>
                    <category id="4.2">4.2 - EJ has no clear definition</category>
                    <category id="4.3">4.3 - EJ as trojan horse: Environmental/climate justice movements/policies are simply a way for politicians/activists to assert a malicious ulterior motive.</category>

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
