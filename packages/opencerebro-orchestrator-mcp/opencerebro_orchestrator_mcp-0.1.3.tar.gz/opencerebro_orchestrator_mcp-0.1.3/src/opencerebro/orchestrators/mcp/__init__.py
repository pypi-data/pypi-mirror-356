def coordinate_flow(agent_function, tool_function, data):
    print("Orchestrator: Starting the flow.")
    agent_result = agent_function()
    print(f"Orchestrator: Agent finished with result: {agent_result}")
    tool_result = tool_function(data)
    print(f"Orchestrator: Tool finished with result: {tool_result}")
    print("Orchestrator: Flow complete.")
    return "Flow succeeded"
