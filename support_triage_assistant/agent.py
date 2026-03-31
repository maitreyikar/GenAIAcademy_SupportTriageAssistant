import json
from google.adk.agents import SequentialAgent, Agent


SUPPORT_CATEGORIES = {
    'billing': 'Invoices, payments, subscriptions, or refunds.',
    'technical_support': 'Bugs, error messages, or integration issues.',
    'account_management': 'Passwords, profile updates, or team seats.',
    'general_inquiry': 'Product features or company info.',
    'product_feedback': 'Feature requests and improvements.',
    'sales_inquiry': 'Pricing plans or enterprise options.',
    'cancellation_request': 'Service termination requests.'
}


CATEGORIZER_INSTRUCTION = f"""
Analyze the user support message and identify the category.
Output ONLY a JSON object in this format: {{"category": "label"}}
Choose from: {list(SUPPORT_CATEGORIES.keys())}
"""

categorization_agent = Agent(
    model='gemini-2.5-flash',
    name='categorizer',
    description='Identifies the intent category of the message.',
    instruction=CATEGORIZER_INSTRUCTION
)


PRIORITY_INSTRUCTION = """
Review the user message and the category assigned by the previous agent.
Assess the priority: 'low', 'medium', 'high', or 'urgent'.
- 'urgent': Outages, security, or legal threats.
- 'high': Broken core features or high frustration.
- 'medium': General bugs or questions with workarounds.
- 'low': General feedback or feature requests.

Output ONLY a JSON object containing both the existing category and the new priority.
Format: {"category": "label", "priority": "level"}
"""

priority_agent = Agent(
    model='gemini-2.5-flash',
    name='prioritizer',
    description='Adds priority level based on sentiment and context.',
    instruction=PRIORITY_INSTRUCTION
)


root_agent = SequentialAgent(
    sub_agents=[categorization_agent, priority_agent],
    name='smart_support_triage_pipeline'
)

