# API Governance Automation

##Setup

llm_config = {"model": "gpt-3.5-turbo"}


##The Task

task = '''
       The business team has requested you a REST API related with Books. Write the API Spec in OpenAPI 3.0.0
       standard. Make sure you include only CRUD operations.
       '''

## Create the api_dev agent
import autogen

api_dev = autogen.AssistantAgent(
    name="Designer",
    system_message="You are an API Developer. You develop high quality API " 
        "once the business team has given you the requirements. You must polish your "
        "API specification based on the feedback you receive and give a refined "
        "version. Only return your final work without additional comments.",
    llm_config=llm_config,
)


reply = api_dev.generate_reply(messages=[{"content": task, "role": "user"}])

## Adding reflection
api_governance = autogen.AssistantAgent(
    name=“API Governance”,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a API Governance Expert. You review the work of "
                "the API Developer and provide constructive "
                "feedback to help improve the quality of the content.",
)

res = api_governance.initiate_chat(
    recipient=api_dev,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

## Create the api_architect agent
api_architect = autogen.AssistantAgent(
    name="API Architect",
    llm_config=llm_config,
    system_message="You are an API Architect, known for "
        "your ability to execute API Linting with the design rules defined in your organization, "
        "ensuring that the APIs in your company ecosystem are high quality and compliant with the defined API Governance. " 
        "Your linting rules are that all description fields must be filled to improve documentation quality and all the names of fields must be camelUpperCase."
        "You have to review the API Specification you receive, check the former linting rules and make concise suggestions so that the API will be compliant. "
        "Begin the review by stating your role.",
)
 ## Create the data_expert agent
data_expert = autogen.AssistantAgent(
    name="Data Expert",
    llm_config=llm_config,
    system_message="You are a Data Expert, known for "
        "your ability to ensure that data is high quality "
        "and free from any potential leakes issues. "
        "Your mission is guarantee completeness (absence of missing fields) and consistency (uniformity across the data model). "
        "Make sure your suggestion is concise, "
        "concrete and to the point. "
        "Begin the review by stating your role.",
)
## Create Security Expert agent
security_expert = autogen.AssistantAgent(
    name="Security Expert",
    llm_config=llm_config,
    system_message="You are an security expert, known for "
        "your ability to ensure that content adheres to the security practices defined in your company "
        "and free from any pontential security issues. " 
        "You have to ensure that, apart from security best practices, the API Spec you received are not exposing more than strictly needed."
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

##Create the Ethics Expert Agent
ethics_expert = autogen.AssistantAgent(
    name="Ethics Expert",
    llm_config=llm_config,
    system_message="You are an ethics reviewer, known for "
        "your ability to ensure that content is ethically sound "
        "and free from any potential ethical issues. " 
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

##Create the Meta Reviewer
meta_reviewer = autogen.AssistantAgent(
    name="Meta Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggragate and review "
    "the work of other reviewers and give a final suggestion on the content.",
)

## Create the nested dialog
def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

review_chats = [
    {
     "recipient": api_architect, 
     "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",},
     "max_turns": 1},
    {
    "recipient": data_expert, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
     {"recipient": security_expert, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
    {"recipient": ethics_expert, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into as JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
     {"recipient": meta_reviewer, 
      "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
     "max_turns": 1},
]



## Initiate chat
api_governance.register_nested_chats(
    review_chats,
    trigger=api_dev,
)


res = api_governance.initiate_chat(
    recipient=api_dev,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)
