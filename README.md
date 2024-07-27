---

# ExcelAI-Engine
Edit Excels using Natural Language Queries

---

## Creating Environment

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/NoorShaik683/ExcelAI-Engine.git
   cd ExcelAI-Engine
   ```

2. **Create a Python Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Create a `.env` File:**

   Create a file named `.env` in the  directory ExcelAI-Engine. Add the following content, replacing the placeholders with your actual values:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

## Installing Requirements

1. **Install Required Python Packages:**

   Ensure your virtual environment is activated, then run:

   ```bash
   pip install -r requirements.txt
   ```

  
## Running the FastAPI Application

1. **Run the Application Locally Using Uvicorn:**

   With your virtual environment activated, use Uvicorn to start the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```


2. **Access the Application:**

   Open your browser and go to `http://127.0.0.1:8000` to access the ExcelAI-Engine application. The Swagger documentation will be available at `http://127.0.0.1:8000/docs`.

## Using Docker

1. **Build and Run the Docker Image:**

   Make sure you have a `Dockerfile` in your project directory. Then build the Docker image:

   ```bash
   docker build -t excelai-engine .
   ```

   Replace `excelai-engine` with a suitable name for your Docker image.


2. **Run the Docker Container:**

   Start the container using Docker:

   ```bash
   docker run -d -p 8000:8000 --name fastapi-container excelai-engine
   ```

3. **Access the Application:**

   Open your browser and go to `http://127.0.0.1:8000` to access the FastAPI application running inside the Docker container.

4. **Stop and Remove the Container:**

   To stop and remove the container, use:

   ```bash
   docker stop <container-id>
   docker rm <container-id>
   ```

## API Endpoints

### 1. `/process-structured-data`

**Method:** `POST`

**Description:** Processes structured data from an Excel file. Optionally, you can provide a second Excel file for additional data operations(joins).

**Request Body:**

```json
{
  "file_path": "path/to/your/file.xlsx",
  "second_file_path": "path/to/second/file.xlsx",(Optional -> applicable for joins)
  "query": "your query here",
  "operation": "operation type (e.g.basic-math, aggregation, joins, pivot, date-operations)"
}
```


### 2. `/process-unstructured-data`

**Method:** `POST`

**Description:** Processes unstructured data from an Excel file in chunks and applies the user-defined modifications.

**Request Body:**

```json
{
  "file_path": "path/to/your/file.xlsx",
  "query": "your query here"
}
```

---
