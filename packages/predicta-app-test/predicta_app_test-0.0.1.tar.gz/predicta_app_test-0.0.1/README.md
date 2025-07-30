Integrating FastAPI with React involves creating a full-stack application where FastAPI serves as the backend API and React handles the frontend user interface. The integration primarily relies on API calls between the two.
1. Setting up the Backend (FastAPI):
Project Structure: Create a dedicated folder for your FastAPI backend.
Dependencies: Install FastAPI and a server like Uvicorn.

```console
pip install fastapi uvicorn
```

API Endpoints:
Define your API endpoints in FastAPI to handle data requests and business logic.
CORS Configuration:
Crucially, configure Cross-Origin Resource Sharing (CORS) in FastAPI to allow your React frontend (running on a different origin/port) to make requests to the backend.
Python

```python
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    origins = [
        "http://localhost:3000",  # Replace with your React app's URL
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/data")
    async def get_data():
        return {"message": "Data from FastAPI"}
        
```

Run the FastAPI server.
```console
    uvicorn main:app --reload
```

2. Setting up the Frontend (React):
Project Setup: Create a new React project using Create React App or Vite.

```console
    npx create-react-app frontend
    cd frontend
```

Making API Calls: Use libraries like fetch or axios in your React components to make HTTP requests to your FastAPI backend endpoints.

```js

    import React, { useEffect, useState } from 'react';

    function App() {
      const [data, setData] = useState(null);

      useEffect(() => {
        fetch('http://localhost:8000/api/data') // Replace with your FastAPI backend URL
          .then(response => response.json())
          .then(data => setData(data.message))
          .catch(error => console.error('Error fetching data:', error));
      }, []);

      return (
        <div>
          <h1>React App</h1>
          {data && <p>{data}</p>}
        </div>
      );
    }

    export default App;
```

Run the React development server.
```console
    npm start
```

1. Interaction:
Your React application will run on one port (e.g., localhost:3000).
Your FastAPI backend will run on another port (e.g., localhost:8000).
The React frontend will send requests to the FastAPI backend's API endpoints, and FastAPI will process these requests, interact with databases if needed, and return data to the React application for display.