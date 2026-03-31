from google.adk.agents.llm_agent import Agent

# Expanded support categories with detailed descriptions for better classification
SUPPORT_CATEGORIES = {
    'billing': 'Questions about invoices, payments, subscriptions, refunds, or pricing.',
    'technical_support': 'Problems with the product not working, error messages, bugs, or integration issues.',
    'account_management': 'Requests to update user information, change password, delete account, or manage team members.',
    'general_inquiry': 'General questions about product features, company information, or anything that doesn\'t fit other categories.',
    'product_feedback': 'Suggestions for new features, improvements, or general feedback about the product.',
    'sales_inquiry': 'Pre-sales questions from potential customers about which plan to choose or enterprise options.',
    'cancellation_request': 'Direct requests to cancel a subscription, order or service.',
}

PRIORITY_LEVELS = ['low', 'medium', 'high', 'urgent']

# --- Agent Instructions ---

# 1. Instruction for the specialized Categorization Agent
CATEGORIZATION_INSTRUCTION = f"""
You are a specialized Categorization Agent. Your only task is to classify an
incoming user message into ONE of the following categories. DO NOT use any other category other than the ones provided.

Output only the category name as a single string. Do not add any other text.

Here are the categories and their descriptions:
{'\n'.join([f'- **{k}**: {v}' for k, v in SUPPORT_CATEGORIES.items()])}
"""

# 2. Instruction for the specialized Priority Agent
PRIORITY_INSTRUCTION = f"""
You are a specialized Priority Assessment Agent. Your only task is to assess
the priority of a user message based on its sentiment and urgency.

Output only the priority level as a single string from this list: {PRIORITY_LEVELS}.
Do not add any other text.

- Use 'urgent' for issues causing a total service outage, security problems, or
  extremely angry customers threatening legal action.
- Use 'high' for time-sensitive issues, key features not working correctly, or
  very frustrated customers.
- Use 'medium' for standard questions or problems that have workarounds.
- Use 'low' for general inquiries, feature requests, or non-critical questions.
"""

# 3. Instruction for the Root/Supervisor Agent
# SUPERVISOR_INSTRUCTION = """
# Your sole purpose is to produce a JSON object with a 'category' and a 'priority'.

# To do this, you MUST follow this exact plan:
# 1.  Call the `categorization_agent` tool with the user's message.
# 2.  Wait for the `category` result from the `categorization_agent`.
# 3.  Call the `priority_agent` tool with the user's message.
# 4.  Wait for the `priority` result from the `priority_agent`.
# 5.  Once you have received BOTH the category and the priority, and only then,
#     construct a single, final JSON object with the collected values.

# Example Final Output:
# {{"category": "billing", "priority": "high"}}

# Do not respond with anything other than the final, complete JSON object. Do not stop early. You must call both tools.
# """


# Updated Instruction for the Root/Supervisor Agent
# SUPERVISOR_INSTRUCTION = """
# SYSTEM GOAL: You are a JSON-only orchestration agent. Your output MUST always be a single JSON object.

# CRITICAL WORKFLOW RULES:
# 1. You are PROHIBITED from responding to the user until you have results from BOTH sub-agents.
# 2. STEP 1: Call `categorization_agent` using the user's input.
# 3. STEP 2: Call `priority_agent` using the user's input.
# 4. FINAL STEP: Combine the 'category' string and the 'priority' string into the JSON schema below.

# REQUIRED SCHEMA:
# {"category": "<category_result>", "priority": "<priority_result>"}

# DO NOT provide progress updates. DO NOT stop after the first tool call. Your final turn MUST be the completed JSON.
# """

SUPERVISOR_INSTRUCTION = """
You are a Triage Coordinator. Your task is to provide a JSON object with 'category' and 'priority'.

EXECUTION PLAN:
- Call BOTH `categorization_agent` and `priority_agent` simultaneously using the user's input message.
- Once you have BOTH outputs, synthesize them into this format:
  {"category": "result_here", "priority": "result_here"}

CRITICAL: Do not return a partial result. If you only have one value, you must continue until you have both.
"""

# --- Agent Definitions ---

# Sub-agent for classifying the message category
categorization_agent = Agent(
    model='gemini-2.5-flash',
    name='categorization_agent',
    description='Classifies a support message into a predefined category.',
    instruction=CATEGORIZATION_INSTRUCTION,
)

# Sub-agent for assessing the message priority
priority_agent = Agent(
    model='gemini-2.5-flash',
    name='priority_agent',
    description='Assesses the priority of a support message (low, medium, high, urgent).',
    instruction=PRIORITY_INSTRUCTION,
)

# Root agent that orchestrates the sub-agents to produce the final JSON
root_agent = Agent(
    model='gemini-2.5-flash',
    name='smart_support_triage_supervisor',
    description='Supervises the triage process by categorizing and prioritizing a support message.',
    instruction=SUPERVISOR_INSTRUCTION,
    sub_agents=[categorization_agent, priority_agent],
)
