from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate,
    PromptTemplate
)
from src.utils.config_loader import config_loader
from src.examples.example_selector import get_example_selector

class PromptBuilder:
    def __init__(self):
        self.config = config_loader.get_prompts_config()
        self.system_prompts = self.config['system_prompts']
        self.templates = self.config['prompt_templates']

    def create_example_prompt(self) -> ChatPromptTemplate:
        """Create the example prompt template"""
        return ChatPromptTemplate.from_messages([
            ("human", self.templates['example']['human']),
            ("ai", self.templates['example']['ai']),
        ])

    def create_few_shot_prompt(self) -> FewShotChatMessagePromptTemplate:
        """Create the few-shot prompt template"""
        return FewShotChatMessagePromptTemplate(
            example_selector=get_example_selector(),
            example_prompt=self.create_example_prompt(),
            input_variables=["input"]
        )

    def create_final_prompt(self) -> ChatPromptTemplate:
        """Create the final prompt template"""
        messages = []
        for msg in self.templates['final']:
            if msg['role'] == 'system':
                content = msg['content'].format(
                    system_prompt=self.system_prompts['sql_expert'],
                    table_info="{table_info}"
                )
                messages.append(("system", content))
            else:
                messages.append((msg['role'], msg['content']))

        messages.insert(1, self.create_few_shot_prompt())
        messages.insert(2, MessagesPlaceholder(variable_name="messages"))
        
        return ChatPromptTemplate.from_messages(messages)

    def create_answer_prompt(self) -> PromptTemplate:
        """Create the answer formatting prompt"""
        return PromptTemplate.from_template(
            self.templates['answer']['template']
        ) 