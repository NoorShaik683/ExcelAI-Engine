import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import pandas as pd
import os
from datetime import datetime
from helper import *
from validator import *
from dotenv import load_dotenv

load_dotenv()
# Initialize the FastAPI app
app = FastAPI()

# Set up logging configuration to log to a file
log_file = 'app.log'  # Specify your log file name and path
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Optional: Also print logs to the console
    ]
)
logger = logging.getLogger(__name__)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/process-structured-data")
async def process_data(data: StructuredDataModel):
    try:
        # Validate file paths
        if not data.file_path.lower().endswith('.xlsx'):
            logger.error(f"Invalid file type: {data.file_path}")
            return JSONResponse({"message": "Please Upload a XLSX File only."}, status_code=400)
        
        # Read the primary Excel file
        df = pd.read_excel(data.file_path)
        
        # Read the secondary Excel file if provided
        if data.second_file_path:
            if not data.second_file_path.lower().endswith('.xlsx'):
                logger.error(f"Invalid file type: {data.second_file_path}")
                return JSONResponse({"message": "Please Upload a XLSX File only."}, status_code=400)
            df2 = pd.read_excel(data.second_file_path)
        else:
            df2=None

        # Generate modification code using the provided function
        modification_code = generate_modification_code(df, data.query,df2,data.operation)
      
        # Apply the modifications
        df = modify_dataframe(df, modification_code,df2)
        
        # Save the modified DataFrame to a file
        now = datetime.now()
    
        # Format the date and time
        date_str = now.strftime("%Y-%m-%d_%H-%M")
    
        output_file = f'modified_files/structued_data_{date_str}.xlsx'
        save_dataframe_to_file(df, output_file)

        return JSONResponse({"message": "Data processed successfully","filename":output_file}, status_code=200)

    except Exception as e:
        logger.error(f"An error occurred - Error : {str(e)}", exc_info=True)
        return JSONResponse({"message": "Something went wrong. Please try again later."}, status_code=500)


@app.post("/process-unstructured-data")
async def process_unstructured_data(data: UnstructuredDataModel):
    try:
        # Validate file paths
        if not data.file_path.lower().endswith('.xlsx'):
            logger.error(f"Invalid file type: {data.file_path}")
            return JSONResponse({"message": "Please Upload a XLSX File only."}, status_code=400)
        
        # Read the primary Excel file
        df = pd.read_excel(data.file_path)
        
        # Generate modification code using the provided function
        updated_df = process_dataframe_in_chunks(df, data.query)
        
        # Save the modified DataFrame to a file
        now = datetime.now()
    
        # Format the date and time
        date_str = now.strftime("%Y-%m-%d_%H-%M")
        output_file = f'modified_files/unstructued_data_{date_str}.xlsx'
        save_dataframe_to_file(updated_df, output_file)

        return JSONResponse({"message": "Data processed successfully", "filename":output_file}, status_code=200)

    except Exception as e:
        logger.error(f"An error occurred - Error : {str(e)}", exc_info=True)
        return JSONResponse({"message": "Something went wrong. Please try again later."}, status_code=500)
