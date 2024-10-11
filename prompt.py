from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import Docx2txtLoader
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

def extract_prompt():

    firmographics_schema = ResponseSchema(
    name="Firmographics",
    description="""
    {
        "Company Name": "The official name of the company.",
        "Industry": "The sector or field the company operates in.",
        "Employee Count": "One of these ranges: 50-100, 200-500, 500-1000.",
        "Revenue Range": "The revenue range of the company.",
        "Number of Office Locations": "Total number of office locations."
    }
    """
    )

    growth_initiatives_schema = ResponseSchema(
        name="Growth Initiatives",
        description="""
        {
            "Recent Acquisitions": "Y/N",
            "Geographic Expansion": "Y/N",
            "New Product Launches": "Y/N",
            "Partnerships": "Y/N"
        }
        """
    )

    technology_initiatives_schema = ResponseSchema(
        name="Technology Initiatives",
        description="""
        {
            "Cloud Adoption": "Y/N",
            "AI/ML Implementation": "Y/N",
            "Cybersecurity Investments": "Y/N",
            "IoT Deployments": "Y/N",
            "Digital Transformation Projects": "Y/N"
        }
        """
    )

    previous_interactions_schema = ResponseSchema(
        name="Previous Interactions with Tata",
        description="""
        {
            "Existing Customer": "Y/N",
            "Past Sales Interactions": "Y/N",
            "Expressed Interest in Tata Solutions": "Y/N"
        }
        """
    )

    resopnse_schemas = [firmographics_schema,
                        technology_initiatives_schema,
                        previous_interactions_schema,
                        growth_initiatives_schema]
    
    output_parser = StructuredOutputParser.from_response_schemas(resopnse_schemas)
    format_instructions = output_parser.get_format_instructions()

    company_text = extract_company_text()

    extraction_prompt = f"""
    As a data extraction expert, your task is to analyze the provided text and extract relevant company information into a structured JSON format. Ensure accuracy by identifying all the key fields as defined below. 

    ### Data Categories:

    1. **Firmographics:** 
    - "Company Name": The official name of the company.
    - "Industry": The sector or field the company operates in.
    - "Employee Count": Choose one of the following ranges: 50-100, 200-500, 500-1000.
    - "Revenue Range": Annual revenue of the company (mention the range or value).
    - "Number of Office Locations": Total number of physical office locations.

    2. **Growth Initiatives:** (Y/N for each)
    - "Recent Acquisitions": Has the company made any acquisitions recently?
    - "Geographic Expansion": Is the company expanding to new geographical regions?
    - "New Product Launches": Has the company recently launched any new products?
    - "Partnerships": Has the company entered into any new partnerships?

    3. **Technology Initiatives:** (Y/N for each)
    - "Cloud Adoption": Has the company adopted cloud-based solutions?
    - "AI/ML Implementation": Is the company using AI/ML technologies?
    - "Cybersecurity Investments": Is the company investing in cybersecurity measures?
    - "IoT Deployments": Has the company deployed Internet of Things (IoT) solutions?
    - "Digital Transformation Projects": Is the company undergoing any digital transformation projects?

    4. **Previous Interactions with Tata:** (Y/N for each)
    - "Existing Customer": Is the company an existing customer of Tata Communications?
    - "Past Sales Interactions": Have there been any previous sales interactions?
    - "Expressed Interest in Tata Solutions": Has the company shown interest in Tata Communications solutions?

    ### Output Format:{{format_instructions}}

    ### Input Text : {{company_text}}

Do not write any other text in output format only provide JSON.
    """

    prompt = PromptTemplate(
        input_variables=["company_text","format_instructions"],
        template=extraction_prompt
    )


    final_prompt = prompt.format(company_text = company_text,
                                 format_instructions = format_instructions)
    # print(final_prompt)
    return final_prompt

def extract_company_text():
    loader = Docx2txtLoader("./company_text.docx")
    data = loader.load()
    company_text = data
    return company_text[0]


def intent_score_prompt(company_details):

    reponse_schemas = [ResponseSchema(name= "company_name", type="str", description= "name of company"),
                       ResponseSchema(name= "solution_area", type="str", description= "As instructed above"),
                       ResponseSchema(name= "intent_score", type="int", description= "calculated normalised score"),
                       ResponseSchema(name= "key_indicators", type="str", description= "As instructed above"),
                       ]
    
    output_parser = StructuredOutputParser.from_response_schemas(reponse_schemas)
    
    format_instructions = output_parser.get_format_instructions()
   
    prompt = """
Your task is to extract and provide the following information:

1. Company Name
2. Solution Area
3. Intent Score
4. Key Indicators

### Scoring Criteria:

        1. **Industry Relevance (3 points):**
        - **Applicable Solutions:**
            - Cloud Computing, Unified Communications, Security Solutions:
                - Relevant Industries: Pharmaceuticals, BFSI, BPO/Telecom, MES, IT/ITES, E-commerce, Healthcare, Hospitality, Travel & Tourism.
            - Networking Solutions:
                - Relevant Industries: Manufacturing, Pharmaceuticals, BFSI, BPO/Telecom, MES, EdTech, IT/ITES, Food & Beverage, E-commerce, Healthcare, Hospitality, Travel & Tourism, ISPs.

        2. **Employee Count (2 points):**
        - Cloud Computing, Unified Communications: 500-1000 employees
        - Security Solutions: 200-500 employees
        - Networking Solutions: 50-100 employees

        3. **Multiple Office Locations (1 point):**
        - Assign 1 point if the company has multiple office locations.

        4. **Growth Initiatives (1 point each, max 4 points):**
        - Recent Acquisitions
        - Geographic Expansion
        - New Product Launches
        - Partnerships

        5. **Technology Initiatives (2 points each, max 10 points):**
        - Cloud Adoption
        - AI/ML Implementation
        - Cybersecurity Investments
        - IoT Deployments
        - Digital Transformation Projects

        6. **Previous Interactions with Tata (2 points each, max 6 points):**
        - Existing Customer
        - Past Sales Interactions
        - Expressed Interest in Tata Solutions

    ### Final Scoring:

    - **Intent Score**: Sum of points across all criteria (Max 26 points).
    - **Normalized Intent Score**: (Intent Score / 26) * 10, rounded to the nearest integer.

    ### Solution Area:
    - Determined by the category with the highest score based on:
    - Industry Relevance
    - Employee Count
    - Technology Initiatives
    - Previous Interactions with Tata.

    ### Key Indicators:
    - List the top 3 factors contributing to the intent score.


    ### Input Company Details: {company_details}
    ### Output Format Instructions: {format_instructions} 

    Do not write any other text in output format only provide JSON.
        
        """
    prompt = PromptTemplate(
        input_variables=["company_details","format_instructions"],
        template=prompt
    )

    final_prompt = prompt.format(company_details = company_details,
                                 format_instructions = format_instructions)
    # print(final_prompt)
    return final_prompt


def probing_questions_prompt(company_details,intent_score_analysis):

    response_schemas = [ResponseSchema(name="company_name", type="str",description="name of the company"),
                        ResponseSchema(name="probing_questions", type="list",description="list of 6 to 7 probing questions probing questions that aim to uncover the company's need for the predicted solution area(s)."),
                        ResponseSchema(name="talking_points", type="list",description="A set of talking points that pitch these solutions in a hyper-personalized manner based on the available information."),
                        ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = """
Your task is to analyze the intent score, reasoning, and company information to generate tailored probing questions and talking points for each company.

For each company, please provide:
1. A set of 6-7 probing questions that aim to uncover the company's need for the predicted solution area(s).
2. A set of talking points that pitch these solutions in a hyper-personalized manner based on the available information.

Output the results in a json format with the following keys `company_name`, `probing_questions`, `talking_points`:
## Format Instrunctions {format_instructions}

Make sure that the probing questions and talking points are specifically tailored to each company's:
- Industry
- Growth Initiatives
- Technology Initiatives
- Previous Interactions with Tata Communications

Highlight how the recommended solutions can effectively address their unique business needs and challenges.

### Company Details: {company_details}
### Intent Score Analysis {intent_score_analysis}


Do not write any other text in output format only provide JSON.
"""
    prompt = PromptTemplate(
        input_variables=["company_details","format_instructions"],
        template=prompt
    )

    final_prompt = prompt.format(company_details = company_details,
                                 format_instructions = format_instructions,
                                 intent_score_analysis = intent_score_analysis)
    return final_prompt

def inmail_prompt():

    response_schemas = [ResponseSchema(name="inmail_1", type="str",description="Address the prospect's most pressing data storage challenge, introducing the most relevant Dell NAS or SAN solution."),
                        ResponseSchema(name="inmail_2", type="str",description="Highlight a secondary challenge or growth area, showcasing how another Dell NAS or SAN product can support their goals."),
                        ResponseSchema(name="inmail_3", type="str",description="Focus on long-term value, discussing how Dell's ecosystem of NAS and SAN products can future-proof their storage infrastructure."),
                        ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    company_text = extract_company_text()

    prompt = """
Your task is to create a series of 3 hyper-personalized InMail messages for Dell to send to a prospective client on LinkedIn. Follow the guidelines below closely to ensure that each message is tailored, engaging, and reflective of the prospect's needs.

1. **Key Information Extraction**: Use the provided Strategic Intelligence (SI) document to extract essential insights about the prospect, including:
   - Recent business initiatives and challenges
   - Technology stack and IT infrastructure
   - Industry trends affecting the prospect
   - Financial indicators and growth areas

2. **Dell's Products Focus**: Highlight Dell's NAS and SAN products, specifically:
   - Isilon NAS solutions (All-Flash, Hybrid, Archive)
   - Dell SAN solutions

3. **InMail Structure**:
   - **Subject Line**: Craft an attention-grabbing subject line (max 60 characters) that hints at the message's value proposition.
   - **Greeting and Hook**: Start with a personalized greeting and a hook that directly relates to the prospect's role or a specific challenge they are facing.
   - **Body**: Write 2-3 concise paragraphs (max 50 words each):
     - Demonstrate understanding of the prospect's situation.
     - Highlight how a specific Dell NAS or SAN product addresses their needs.
     - Tie the solution to a relevant use case or initiative mentioned in the SI document.
   - **CTA**: Include a clear, action-oriented call-to-action (CTA).
   - **Sign-off**: Close with a professional sign-off.

4. **Message Focus Areas**:
   - **InMail 1**: Address the prospect's most pressing data storage challenge, introducing the most relevant Dell NAS or SAN solution.
   - **InMail 2**: Highlight a secondary challenge or growth area, showcasing how another Dell NAS or SAN product can support their goals.
   - **InMail 3**: Focus on long-term value, discussing how Dell's ecosystem of NAS and SAN products can future-proof their storage infrastructure.

5. **Predictive Product Pitch and Use Cases**:
   - For large-scale unstructured data management: Suggest Isilon NAS solutions.
   - For high-performance block-level storage: Recommend Dell SAN solutions.
   - For data-intensive operations or AI/ML initiatives: Propose Isilon All-Flash.
   - For cost-effective long-term data retention: Suggest Isilon Archive.
   - For unified storage needs: Recommend Isilon Hybrid.

6. **Industry Trends to Consider**:
   - Rapid growth of unstructured data
   - Adoption of AI and machine learning
   - Shift towards hybrid and multi-cloud environments
   - Increasing focus on data security and compliance
   - Edge computing and IoT integration
   - Data lake initiatives
   - Sustainability and energy efficiency in IT

7. **General Guidelines**:
   - Use a professional yet conversational tone suitable for LinkedIn.
   - Avoid technical jargon unless it's industry-specific and relevant.
   - Incorporate specific details from the SI document to demonstrate a deep understanding of the prospect's business.
   - Keep the total InMail length under 150 words.
   - Ensure each InMail builds upon the previous one, creating a cohesive narrative.
   - Tailor the product recommendations to the prospect's industry, size, and specific needs.

8. **Value Propositions to Emphasize**:
   - Massive scalability for growing data volumes.
   - High performance for demanding workloads.
   - Comprehensive data protection and security.
   - Seamless integration with existing systems and cloud environments.
   - Cost efficiency and improved storage utilization.
   - Advanced data management capabilities.
   - Future-proof design and technology.

9. **InMail Style and Engagement**:
   - Keep messages concise, engaging, and tailored to LinkedIn.
   - Use hook lines to create urgency and relevance, such as:
     - "See how industry leaders are revolutionizing their data storage."
     - "Don't let competitors outpace you with superior storage solutions."
     - "Unlock your company's data potential with Dell's cutting-edge storage."
   - Incorporate these hook lines naturally into the message, either in the subject line or opening.
   - Use active voice and powerful verbs to maintain energy throughout the message.
   - Create a sense of exclusivity or insider knowledge when discussing industry trends or competitor actions.

10. **LinkedIn-specific Considerations**:
    - Mention any mutual connections or shared groups if applicable.
    - Reference any recent company news or LinkedIn posts by the prospect.
    - Offer to share relevant whitepapers, case studies, or invite to exclusive webinars.
    - Suggest connecting on LinkedIn as part of the CTA.

Remember, the goal is to create concise, engaging InMail messages that feel personalized and relevant to the prospect's LinkedIn profile and company situation. Demonstrate Dell's understanding of their unique challenges and position Dell's NAS and SAN solutions as critical tools for staying competitive in the prospect's industry. Inspire the prospect to engage further, whether through a reply, accepting a connection request, or agreeing to a call or meeting.


### Input Company Detailed text : {company_text}
### Output Format: {format_instructions}

Do not write any other text in output format only provide JSON.

"""
    prompt = PromptTemplate(
        input_variables=["company_details",
                         "format_instructions"],
        template=prompt
    )

    final_prompt = prompt.format(company_text = company_text,
                                 format_instructions = format_instructions,)
    return final_prompt

if __name__ == '__main__':
    extract_prompt()

