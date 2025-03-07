from bee import Agent, Message, BeeHive

class OnboardingPersonalInformationAgent(Agent):
    async def setup(self):
        self.name = "Onboarding Personal Information Agent"

    async def run(self):
        message = "Hello, I'm here to help you get started with our product. Could you tell me your name and location?"
        response = await self.send_and_wait("customer_proxy_agent", Message(message))
        
        if response:
            print(f"Collected personal information: {response.content}")
            return "TERMINATE"

class OnboardingTopicPreferenceAgent(Agent):
    async def setup(self):
        self.name = "Onboarding Topic Preference Agent"

    async def run(self):
        message = "Great! Could you tell me what topics you are interested in reading about?"
        response = await self.send_and_wait("customer_proxy_agent", Message(message))
        
        if response:
            print(f"Collected topic preferences: {response.content}")
            return "TERMINATE"

class CustomerEngagementAgent(Agent):
    async def setup(self):
        self.name = "Customer Engagement Agent"

    async def run(self):
        message = "Let's find something fun to read."
        response = await self.send_and_wait("customer_proxy_agent", Message(message))
        
        if response:
            print(f"Engaging content: {response.content}")
            return "TERMINATE"

class CustomerProxyAgent(Agent):
    async def setup(self):
        self.name = "customer_proxy_agent"

    async def on_message(self, sender, message):
        user_input = input(f"{sender}: {message.content}\nUser: ")
        return Message(user_input)

# Creating a beehive and adding agents
beehive = BeeHive()
beehive.add_agent(OnboardingPersonalInformationAgent())
beehive.add_agent(OnboardingTopicPreferenceAgent())
beehive.add_agent(CustomerEngagementAgent())
beehive.add_agent(CustomerProxyAgent())

# Running the beehive
beehive.run()
