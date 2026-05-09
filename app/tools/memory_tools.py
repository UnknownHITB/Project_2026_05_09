from app.tools.registry import registry
from app.core.memory import memory

def store_fact(entity: str, attribute: str, value: str):
    """
    Stores a specific fact about an entity or the user in semantic memory.
    Example: entity='user', attribute='likes', value='Python'
    """
    return memory.store_fact(entity, attribute, value)

def get_user_facts():
    """Retrieves all stored facts about the user."""
    facts = memory.get_facts(entity='user')
    if not facts:
        return "No facts known about the user yet."
    return "\n".join([f"- {attr}: {val}" for attr, val in facts])

def record_episode(summary: str):
    """
    Records a summary of the current interaction or an important event in episodic memory.
    """
    return memory.add_episode(summary)

def search_past_conversations(query: str):
    """
    Performs a semantic search over past conversation summaries to find relevant context.
    """
    results = memory.semantic_search(query)
    if not results:
        return "No relevant past conversations found."
    
    formatted = []
    for item in results:
        if len(item) == 3:
            summary, timestamp, similarity = item
            formatted.append(f"- [{timestamp}] (Similarity: {similarity:.2f}): {summary}")
        else:
            summary, timestamp = item
            formatted.append(f"- [{timestamp}]: {summary}")
    return "\n".join(formatted)

def update_system_rule(rule_name: str, rule_content: str):
    """
    Updates or creates a procedural rule for system behavior.
    Example: rule_name='tone', rule_content='Always be helpful and concise.'
    """
    return memory.set_rule(rule_name, rule_content)

def forget_fact(entity: str, attribute: str):
    """
    Removes a specific fact from semantic memory.
    Example: entity='user', attribute='favorite_color'
    """
    return memory.delete_fact(entity, attribute)

def delete_rule(rule_name: str):
    """
    Removes a system rule from procedural memory.
    """
    return memory.delete_rule(rule_name)

def register_memory_tools():
    registry.register(
        name="store_fact",
        description="Stores a specific fact about an entity (like the user) in semantic memory.",
        parameters={
            "type": "object",
            "properties": {
                "entity": {"type": "string", "description": "The person or object the fact is about (e.g., 'user')."},
                "attribute": {"type": "string", "description": "The attribute being stored (e.g., 'favorite_color')."},
                "value": {"type": "string", "description": "The value of the attribute."}
            },
            "required": ["entity", "attribute", "value"]
        },
        func=store_fact
    )

    registry.register(
        name="get_user_facts",
        description="Retrieves known facts about the user to provide personalized responses.",
        parameters={"type": "object", "properties": {}},
        func=get_user_facts
    )

    registry.register(
        name="record_episode",
        description="Saves a summary of the conversation history to episodic memory for long-term recall.",
        parameters={
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "A concise summary of the key points of the conversation."}
            },
            "required": ["summary"]
        },
        func=record_episode
    )

    registry.register(
        name="search_past_conversations",
        description="Searches for past memories or topics using semantic similarity.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "the topic or question to search for."}
            },
            "required": ["query"]
        },
        func=search_past_conversations
    )

    registry.register(
        name="update_system_rule",
        description="Updates the assistant's core behavior rules in procedural memory.",
        parameters={
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "The name/category of the rule."},
                "rule_content": {"type": "string", "description": "The detailed instruction for the AI to follow."}
            },
            "required": ["rule_name", "rule_content"]
        },
        func=update_system_rule
    )

    registry.register(
        name="forget_fact",
        description="Removes a specific fact from memory (e.g., if it is no longer true).",
        parameters={
            "type": "object",
            "properties": {
                "entity": {"type": "string", "description": "The entity the fact is about (e.g., 'user')."},
                "attribute": {"type": "string", "description": "The attribute to forget (e.g., 'favorite_color')."}
            },
            "required": ["entity", "attribute"]
        },
        func=forget_fact
    )

    registry.register(
        name="delete_rule",
        description="Deletes a system behavior rule from procedural memory.",
        parameters={
            "type": "object",
            "properties": {
                "rule_name": {"type": "string", "description": "The name of the rule to delete."}
            },
            "required": ["rule_name"]
        },
        func=delete_rule
    )
