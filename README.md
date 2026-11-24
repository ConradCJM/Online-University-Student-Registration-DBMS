# Online-University-Student-Registration-DBMS
A DBMS made for TMU's CPS510 Database systems course

Powershell setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1


pip install oracledb
pip install python-dotenv

# OR

pip install -r requirements.txt
```

Create a `.env` file in the project root with your Oracle credentials:

```env
ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=your_oracle_dsn
```

## Run the application

Start the FastAPI service from the `connection` directory:

```powershell
cd connection
..\venv\Scripts\python.exe -m uvicorn app:app --reload
```

Start the TypeScript frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (usually `http://localhost:5173`). The frontend reads and adds courses through the API at `http://localhost:8000`. Set `VITE_API_URL` in a `frontend/.env` file to use a different API URL.

