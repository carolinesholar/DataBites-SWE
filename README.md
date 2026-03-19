## running the project

### backend
1. navigate to backend folder:
   cd Backend
2. install dependencies:
   pip install -r requirements.txt
3. initialize database (only needed once):
   python init_db.py
4. run server:
   python app.py

backend runs on http://127.0.0.1:5000

---

### frontend
1. navigate to frontend folder:
   cd frontend
2. install dependencies (only needed once):
   npm install
3. start the app:
   npm start

frontend runs on http://localhost:3000

---

### notes
- make sure backend is running before using frontend
- login/register is connected to backend endpoints
- user info is stored in localStorage after login
