from bedrock_agentcore.runtime import (
    BedrockAgentCoreApp,
)  # ## AGENTCORE RUNTIME - LINE 1 ###
from lab_helpers.lab1_strands_agent import (
    SYSTEM_PROMPT,
    get_product_info,
    get_return_policy,
)
from lab_helpers.lab2_memory import (
    ACTOR_ID,
    SESSION_ID,
    CustomerSupportMemoryHooks,
    create_or_get_memory_resource,
    memory_client,
)
from strands import Agent
from strands.models import BedrockModel

# Lab1 import: Create the Bedrock model #TODO: Guardrail
model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model = BedrockModel(model_id=model_id)

# Lab2 import : Initialize memory via hooks
memory_id = create_or_get_memory_resource()
memory_hooks = CustomerSupportMemoryHooks(
    memory_id, memory_client, ACTOR_ID, SESSION_ID
)

# Lab1 import: Create the agent with all customer support tools
agent = Agent(
    model=model,
    tools=[get_return_policy, get_product_info],
    system_prompt=SYSTEM_PROMPT,
    hooks=[memory_hooks],
)

# Initialize the AgentCore Runtime App
app = BedrockAgentCoreApp()  ### AGENTCORE RUNTIME - LINE 2 ###


@app.entrypoint  ### AGENTCORE RUNTIME - LINE 3 ###
def invoke(payload):
    """AgentCore Runtime entrypoint function"""
    user_input = payload.get("prompt", "")

    # Invoke the agent
    response = agent(user_input)
    return response.message["content"][0]["text"]


if __name__ == "__main__":
    app.run()  ### AGENTCORE RUNTIME - LINE 4 ###
