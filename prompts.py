from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)

# Few-shot prompt template with dynamic example selector
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_selector=get_example_selector(),
    example_prompt=example_prompt,
    input_variables=["input"]
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a MySQL expert. Your task is to generate syntactically correct MySQL queries in response to user questions.\n"
            "IMPORTANT:\n"
            "- DO NOT use markdown formatting or code blocks (no triple backticks).\n"
            "- DO NOT include any explanations, comments, or additional text.\n"
            "- Only return the raw SQL query as plain text on a single line or multiple lines, as needed.\n"
            "- Do not wrap the query in quotes or any other formatting.\n\n"
            "Here is the relevant table info: {table_info}\n\n"
            "Below are several examples of questions and their corresponding SQL queries. These are only for reference and should inform how you answer future questions."
        ),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        (
            "human",
            "Provide only the raw SQL query in plain text without any markdown formatting.\n\n{input}"
        ),
    ],
)


answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question in plain text without any markdown formatting or code blocks.
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer:"""
)