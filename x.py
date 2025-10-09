user_prompt = f"""
    Please evaluate sctrictly for the following transcript:
    ```text
    {dialogue_data[i]}
    ```
    Explain your reasoning as if you are a difficult evaluator for customer service dialogues. 
    Think step by step, and then give an overall score for each dialogue in the end inside <score> (example <52>).

    Examples:
    - This is a bad dialougue:
    Overall score negative: {score[1]['score']} : {dialogue[1]['text']}
    - This is an average dialougue:
    Overall score negative: {score[0]['score']} : {dialogue[0]['text']}
    This is a slightly slightly good dialougue:
    Overall score negative: {score[2]['score']} : {dialogue[2]['text']}
"""