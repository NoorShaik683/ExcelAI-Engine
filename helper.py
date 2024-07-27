import pandas as pd
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

def modify_dataframe(df, modification_code, df2=None):
    exec(modification_code, globals())
    if 'modify_dataframe' in globals():
        df = modify_dataframe(df, df2)
    return df

def save_dataframe_to_file(df, file_path):
    df.to_excel(file_path, index=False)
    print(f"DataFrame saved to {file_path}")



def generate_modification_code(df, objective, df2=None, operation=None):
    # Initialize OpenAI API client
    client = OpenAI()

    # Prepare the content for the prompt
    if operation == 'joins' and df2 is not None:
        df2_content = df2.head().to_dict()  # Convert the second DataFrame to a dictionary for the prompt
        prompt = f"Here is the head of the first File DataFrame:\n{df.head()}\n Here is the head of the second file DataFrame:\n{df2.head()}\n Here is the instruction: {objective}."
        
    else:
        prompt = f"Here is the head of the DataFrame:\n{df.head()}\n Here is the instruction: {objective}."
        
    
    # Generate completion with OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content":  '''You are a Python developer tasked with writing a function to customize a DataFrame according to user-defined requirements. Your solution should meet the following criteria:

                1. Simplicity and Clarity: Write clean and straightforward code that is easy to understand. Avoid unnecessary complexity. Avoid unnecessary explanations.
                2. Handling Missing Values: Ensure that any missing (NA) values in the DataFrame are managed appropriately.
                3. Precise Customization: Implement the modifications exactly as specified by the user. 
                4. Final Output: The function should return the modified DataFrame.

                Your function should be named modify_dataframe(df, df2=None) and must include only the necessary code to perform the described modifications. No additional comments or usage examples are needed. Ensure that your code accurately reflects the user’s instructions and performs the required transformations on the DataFrame.

                The solution must be executable as provided.
                Note : Use df2 when you receive secondfile dataframe only'''
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    
    # Return the code, removing unnecessary parts
    return completion.choices[0].message.content.replace("```", '').replace("python", '')
 


def process_chunk(chunk, objective, chain):
    # Convert the chunk to dictionary format for JSON
    chunk_dict = chunk.to_dict(orient='records')
    prompt = f"Here is a chunk of the DataFrame in JSON format:\n{chunk_dict}\n Here is the instruction: {objective}.\n Please process the data and return the result in JSON format."

    chunk_data = chain.invoke({"query": prompt})
    return chunk_data


def process_dataframe_in_chunks(df,objective, chunk_size=50):
    # Initialize OpenAI API client
    model = ChatOpenAI(model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None)

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template='''You are a Data Analyzer tasked with processing the given data according to user-defined requirements. Your solution should meet the following criteria:

                    1. Handling Missing Values: Ensure that any missing (NA) values in the Data are managed appropriately.
                    2. Precise Customization: Process the data exactly as specified by the user.
                    3. Final Output: Return the result in JSON format.

                    The function should handle the Data and return a result in JSON format. No additional code or comments are needed.\n{format_instructions}\n{query}\n''',
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    # Define a ThreadPoolExecutor
    json_responses = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        # Loop over the DataFrame in chunks
        for start in range(0, len(df), chunk_size):
            end = min(start + chunk_size, len(df))
            chunk = df.iloc[start:end]
            
            # Submit the chunk processing task to the executor
            futures.append(executor.submit(process_chunk, chunk, objective, chain))
        
        # Collect results as they complete
        for future in as_completed(futures):
            try:
                result = future.result()
                json_responses.extend(result)
            except Exception as e:
                print(f"An error occurred: {e}")
    
    return pd.DataFrame(json_responses)
    
