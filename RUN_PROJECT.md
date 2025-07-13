# 🚀 How to Run Workforce Distribution.ai - Complete Beginner Guide

## 📋 What You Need First

1. **Python** - Download and install Python 3.8 or higher from [python.org](https://python.org)
2. **Git** (optional) - Download from [git-scm.com](https://git-scm.com)

## 🎯 Quick Start (3 Simple Steps)

### Step 1: Open Command Prompt/Terminal
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Open Terminal from Applications > Utilities
- **Linux**: Open Terminal

### Step 2: Navigate to Your Project
```bash
cd "C:\Users\Lenovo\Desktop\Intel Proj"
```

### Step 3: Install Dependencies (Python 3.12 Fix)
```bash
python fix_python312.py
```

**OR** if the above doesn't work, try this manual approach:
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install fastapi uvicorn streamlit pandas numpy
```

## 🏃‍♂️ Running the Project

### Option A: Use the Simple Start Scripts (Recommended)

#### 1. Start the Backend (AI Server)
Open a **new** command prompt window and run:
```bash
python start_backend.py
```
You should see: "Backend server is running at http://localhost:8000"

#### 2. Start the Frontend (Web Interface)
Open **another** command prompt window and run:
```bash
python start_frontend.py
```
You should see: "Frontend is running at http://localhost:8501"

### Option B: Manual Start

#### 1. Start Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```

## 🌐 Access Your Application

1. **Open your web browser** (Chrome, Firefox, Edge, etc.)
2. **Go to**: `http://localhost:8501`
3. **You should see** the Workforce Distribution.ai dashboard!

## 📊 Import Your Data (Optional)

### Import Your CSV File
1. In the web interface, click on **"Data Import"** in the sidebar
2. Click **"Get CSV Summary"** to see what data you have
3. Click **"Import CSV Data"** to load your data into the system
4. Your data will be automatically processed and available for analysis!

## 🎮 What You Can Do

### Dashboard
- View workforce analytics and insights
- See job distribution charts
- Monitor candidate skills

### Jobs Management
- Add new job positions
- Set salary ranges
- Define required skills

### Candidates Management
- Add candidate profiles
- Rate their skills
- View candidate matches

### Workforce Analysis
- Get AI-powered insights
- Analyze skill gaps
- Optimize workforce distribution

### Data Import
- Import your CSV data
- Preview data before importing
- Get data summaries

## 🔧 Troubleshooting

### If you get "pip not found":
1. Make sure Python is installed
2. Try: `python -m pip install -r requirements.txt`

### If you get "port already in use":
1. Close other applications using ports 8000 or 8501
2. Or restart your computer

### If the web page doesn't load:
1. Make sure both backend and frontend are running
2. Check that you're using the correct URL: `http://localhost:8501`
3. Try refreshing the page

### If you get import errors:
1. Make sure you're in the correct directory
2. Run: `pip install -r requirements.txt` again
3. Restart your command prompt

## 📞 Need Help?

1. **Check the logs** in your command prompt windows for error messages
2. **Make sure both servers are running** (backend and frontend)
3. **Try restarting** both servers if something doesn't work

## 🎉 Success!

Once everything is running, you should see:
- A beautiful web interface with multiple sections
- Interactive charts and forms
- Your CSV data imported and ready for analysis
- AI-powered workforce insights

## 🔄 Stopping the Project

1. **In each command prompt window**, press `Ctrl + C`
2. **Close the command prompt windows**
3. **Close your web browser**

---

**That's it!** You now have a fully functional AI-powered workforce distribution system running on your computer! 🎊 