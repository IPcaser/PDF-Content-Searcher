from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai_tools import PDFSearchTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["GOOGLE_API_KEY"] = "Your API KEY"
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    verbose=True,
    temperature=0.7,
    google_api_key="Your API key"
)

querry = input("Enter your querry: ");
tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini-1.5-flash-latest",
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/msmarco-distilbert-base-v4"
                
            ),
        ),
    ),
   pdf="LabManual_cnn.pdf"
)

analyser=Agent(
    role='PDF searcher',
    goal='To find the appropriate data inside PDF that solves the problem',
    backstory="""You are a PDF specialist responsible for finding the appropriate data from the PDF to solve the users problem.
    You should provide in detail results based on the PDF provided and the problem of the user.
    You are highly skilled and allways return the best and easy to understand results""",
    tools=[tool],
    allow_delegation=False,
    verbose=True,
    llm=llm
)

writer=Agent(
    role='Content Writer',
    goal='To produce higly accurate and easy to understand information',
    backstory="""You are an content specialist and are respinsible to generate reliable and easy to understand content or information based on the summary of data.
    You should provide indetail results on the summary data.""",
    verbose=True,
    llm=llm
)

task_read=Task(
    description=f'{querry}',
    agent=analyser,
    expected_output=f'A detailed information on {querry}'
)

task_write=Task(
    description=f'{querry}',
    agent=writer,
    expected_output=f'A detailed step by step Description'
)

mycrew=Crew(
    tasks=[task_read,task_write],
    agents=[analyser,writer],
    verbose=True
)

results=mycrew.kickoff();

print(results)