from agent.agent_runner import ask_agent

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    response = ask_agent(user_input)
    print(f"Bot: {response}")
