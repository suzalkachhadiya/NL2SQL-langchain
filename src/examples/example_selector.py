from typing import List, Dict, Any
from langchain_core.example_selectors import BaseExampleSelector
# from langchain_core.prompts import PromptValue

class SQLExampleSelector(BaseExampleSelector):
    """Example selector for SQL queries"""
    
    def __init__(self):
        self.examples = [
            {
                "input": "Show me all students who scored above 80 in Math",
                "query": "SELECT * FROM students WHERE math_score > 80"
            },
            {
                "input": "What is the average age of students in each grade?",
                "query": "SELECT grade, AVG(age) as avg_age FROM students GROUP BY grade"
            },
            {
                "input": "How many students are in each grade?",
                "query": "SELECT grade, COUNT(*) as student_count FROM students GROUP BY grade"
            },
            {
                "input": "What are the top 5 students by math score?",
                "query": "SELECT name, math_score FROM students ORDER BY math_score DESC LIMIT 5"
            },
            {
                "input": "Show me students who have both math and science scores above 75",
                "query": "SELECT * FROM students WHERE math_score > 75 AND science_score > 75"
            }
        ]

    def add_example(self, example: Dict[str, str]) -> None:
        """Add an example to the selector"""
        self.examples.append(example)

    def select_examples(self, input_variables: Dict[str, Any]) -> List[Dict[str, str]]:
        """Select examples based on the input"""
        # For now, return all examples
        # In a more sophisticated implementation, you could:
        # 1. Use semantic similarity to find relevant examples
        # 2. Use a fixed number of examples
        # 3. Use different examples based on the type of query
        return self.examples

def get_example_selector() -> BaseExampleSelector:
    """Get an instance of the example selector"""
    return SQLExampleSelector() 