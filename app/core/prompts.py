
def get_prompt_template(category):
    PROMPT_TEMPLATE = f"""
        Analyze the image and determine if it belongs to the category: {category}.
        
        Respond with ONLY one of these two options:
        YES - if the image belongs to the category
        NO - if the image does not belong to the category
        
        YOUR ENTIRE RESPONSE MUST BE EITHER "YES" OR "NO" WITHOUT ANY ADDITIONAL TEXT.
    """
    return PROMPT_TEMPLATE

def get_room_condition_prompt():
    PROMPT_TEMPLATE = """
        Analyze the image and determine the condition of the room.
        
        You have to strictly mention these five things:
        1. Percentage of the oldness and newness of the room
        2. The cleanliness of the room with these three options: "clean", "moderate", "messy"
        3. Are there any cracks in the walls? "YES" or "NO"
        4. Is the wall color new or old?
        5. Properly interiored? "YES" or "NO"

        YOUR RESPONSE MUST INCLUDE ALL FIVE OF THESE POINTS AND DON'T INCLUDE ANY ADDITIONAL INFORMATION.

        Example response format 1:
            Condition: 70% old, 30% new,
            Cleanliness: messy,
            Cracks on wall: YES,
            Wall color: new,
            Properly Interior: No
        
        Example response format 2:
            Condition: 20% old, 80% new,
            Cleanliness: clean,
            Cracks on wall: NO,
            Wall color: old,
            Properly Interior: YES
    """
    return PROMPT_TEMPLATE