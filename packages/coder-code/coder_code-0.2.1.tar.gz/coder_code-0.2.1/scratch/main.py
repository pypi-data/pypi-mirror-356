from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


def write_code(user_prompt: str, existing_code: str = None):
    if existing_code:
        prompt = PromptTemplate(
            input_variables=["existing_doer", "user_prompt"],
            template="""Given this existing code {existing_code}. Write code to {user_prompt}. 
                Use or rewrite the existing code in a logical way without losing any of the functionality of the existing code.
                 Output code only. No description.""",
        )
    else:
        prompt = PromptTemplate(input_variables=["user_prompt"], template="""Write code to {user_prompt}. Output the code only. No description.""")
    llm = OpenAI(model_name="gpt-4")
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(us)
    return text_response



pprompt = PromptTemplate(input_variables=["user_prompt"], template="""Write code to {user_prompt}. Output the code only. No description.""")



