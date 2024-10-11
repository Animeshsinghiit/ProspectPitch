import os
from dotenv import load_dotenv
import re
import json
load_dotenv()
from prompt import extract_prompt,intent_score_prompt,probing_questions_prompt,inmail_prompt
from groq import Groq
from langchain_groq import ChatGroq
from langchain.output_parsers import ResponseSchema, StructuredOutputParser



def extract_inputs():

    

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    

    prompt = extract_prompt()
    output = llm.invoke(prompt)
    # print(output)
    return output.content

def get_intent_details():

    reponse_schemas = [ResponseSchema(name= "company_name", type="str", description= "name of company"),
                       ResponseSchema(name= "solution_area", type="str", description= "As instructed above"),
                       ResponseSchema(name= "intent_score", type="int", description= "calculated normalised score"),
                       ResponseSchema(name= "key_indicators", type="str", description= "As instructed above"),
                       ]
    
    output_parser = StructuredOutputParser.from_response_schemas(reponse_schemas)

    extracted_input = extract_inputs()

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    prompt = intent_score_prompt(extracted_input)
    output = llm.invoke(prompt)

    final_output = output_parser.parse(output.content)
    print(final_output)
    return final_output

def get_probing_questions():
    company_details = extract_inputs()
    intent_score_analysis = get_intent_details()
    response_schemas = [ResponseSchema(name="company_name", type="str",description="name of the company"),
                        ResponseSchema(name="probing_questions", type="list",description="list of 6 to 7 probing questions probing questions that aim to uncover the company's need for the predicted solution area(s)."),
                        ResponseSchema(name="talking_points", type="list",description="A set of talking points that pitch these solutions in a hyper-personalized manner based on the available information."),
                        ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    prompt = probing_questions_prompt(company_details=company_details,
                                      intent_score_analysis=intent_score_analysis)
    output = llm.invoke(prompt)

    final_output = output_parser.parse(output.content)
    print(final_output)
    return final_output

def get_inmails():
    response_schemas = [ResponseSchema(name="inmail_1", type="str",description="Address the prospect's most pressing data storage challenge, introducing the most relevant Dell NAS or SAN solution."),
                        ResponseSchema(name="inmail_2", type="str",description="Highlight a secondary challenge or growth area, showcasing how another Dell NAS or SAN product can support their goals."),
                        ResponseSchema(name="inmail_3", type="str",description="Focus on long-term value, discussing how Dell's ecosystem of NAS and SAN products can future-proof their storage infrastructure."),
                        ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt = inmail_prompt()

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    output = llm.invoke(prompt)
    
    final_output = output_parser.parse(output.content)
    
    return final_output



# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )


# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": extraction_prompt,
#         }
#     ],
#     model="llama3-8b-8192",
# )

# print(chat_completion.choices[0].message.content)


if __name__ =="__main__":
    get_inmails()
