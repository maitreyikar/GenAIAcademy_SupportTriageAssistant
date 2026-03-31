import json
from google.adk.agents import SequentialAgent, Agent
from google.adk.tools.tool_context import ToolContext



def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    return {"status": "success"}


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
Analyze the user's PROMPT and identify the category.
Write the category to the output key.
Do NOT return any explanation or JSON. Only store the value.
Choose from: {list(SUPPORT_CATEGORIES.keys())}

PROMPT:
    {{ PROMPT }}
"""

categorization_agent = Agent(
    model='gemini-2.5-flash',
    name='categorizer',
    description='Identifies the intent category of the message.',
    instruction=CATEGORIZER_INSTRUCTION,
    output_key="CATEGORY"
)


PRIORITY_INSTRUCTION = f"""
Review the user's PROMPT and the CATEGORY assigned by the previous agent.
Assess the priority of the PROMPT: 'low', 'medium', 'high', or 'urgent'.
- 'urgent': Outages, security, or legal threats.
- 'high': Broken core features or high frustration.
- 'medium': General bugs or questions with workarounds.
- 'low': General feedback or feature requests.

Output ONLY a JSON object containing both the existing category and the new priority.
Format: {{"category": "<category>", "priority": "level"}}

PROMPT:
    {{ PROMPT }}

CATEGORY:
    {{ CATEGORY }}
"""

priority_agent = Agent(
    model='gemini-2.5-flash',
    name='prioritizer',
    description='Adds priority level based on sentiment and context.',
    instruction=PRIORITY_INSTRUCTION
)


triage_workflow = SequentialAgent(
    sub_agents=[categorization_agent, priority_agent],
    name='triage_workflow'
)

root_agent = Agent(
    name="root",
    model='gemini-2.5-flash',
    description="The main entry point for the support triage assistant",
    instruction="""
   When the user responds, use the 'add_prompt_to_state' tool to save their response.
    After using the tool, transfer control to the 'triage_workflow' agent.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[triage_workflow]
)

