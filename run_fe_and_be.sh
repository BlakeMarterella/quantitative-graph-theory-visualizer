#! /bin/bash

# Run the back-end development server
cd backend
source venv/bin/activate
# Run it in the background
python3 app.py &

# Run the front-end development server
cd ../frontend
npm run dev