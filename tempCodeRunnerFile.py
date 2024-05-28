writer=Agent(
    role='Content Writer',
    goal='To produce higly accurate and easy to understand information',
    backstory="""You are an content specialist and are respinsible to generate reliable and easy to understand content or information based on the summary of data.
    You should provide indetail results on the summary data.""",
    verbose=True,
    llm=llm
)