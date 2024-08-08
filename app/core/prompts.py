
def get_prompt_template(category):
    PROMPT_TEMPLATE = f"""
        Analyze the image and determine if it belongs to the category: {category}.
        
        Respond with ONLY one of these two options:
        YES - if the image belongs to the category
        NO - if the image does not belong to the category
        
        YOUR ENTIRE RESPONSE MUST BE EITHER "YES" OR "NO" WITHOUT ANY ADDITIONAL TEXT.
    """
    return PROMPT_TEMPLATE