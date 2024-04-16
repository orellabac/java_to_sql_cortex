from snowflake.snowpark import Session

def convert_with_cortex(sp_session: Session, user_query: str) -> str:
    # Define the prompt
    instruction_prompt = f'''
    You are an expert Snowflake data analyst, 
    Your task is generate Snowflake compliant SQL statement 
    that is equivalent to the JAVA Apache Spark given as input between the [code] and [/code] tags.
    [code]
    {user_query}
    [/code]
    Put the result between the [resultcode] and [/resultcode] tags
    '''
    sql_stmt = f'''select snowflake.cortex.complete(
                'mistral-large'
                ,'{instruction_prompt}') as llm_reponse;'''
        
    l_rows = sp_session.sql(sql_stmt).collect()

    llm_response = l_rows[0]['LLM_REPONSE']
    return llm_response
