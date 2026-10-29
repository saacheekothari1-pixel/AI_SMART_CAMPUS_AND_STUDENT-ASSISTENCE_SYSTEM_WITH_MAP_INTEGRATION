# AI Smart Campus Navigation and Student Assistance System

An AI-powered web application designed to help students navigate their campus, locate buildings and facilities, find faculty and administrative offices, and get instant answers to common campus-related queries.

## Overview

Navigating a large campus can be challenging, especially for new students and visitors. Finding classrooms, laboratories, faculty offices, departments, and administrative services often requires asking multiple people for directions.

The **AI Smart Campus Navigation and Student Assistance System** provides a centralized, student-friendly platform that combines campus information, interactive maps, database-driven search, and AI-assisted support.

## Key Features

- **Smart Campus Search** — Search for campus buildings, classrooms, laboratories, departments, and facilities.
- **Interactive Campus Map** — Explore campus locations and view routes from the main gate to a selected destination using Mapbox.
- **Faculty Information** — Find faculty members and their associated departments, buildings, floors, and room numbers when available.
- **Administrative Assistance** — Identify relevant offices and services for common student requirements, such as certificates and administrative enquiries.
- **AI-Powered Chatbot** — Ask campus-related questions through a conversational interface.
- **Database-Driven Information** — Retrieve campus information from the database rather than relying entirely on hardcoded responses.
- **Structured Campus Dataset** — Organize information about classrooms, faculty, laboratories, offices, departments, and campus locations.
- **Student-Friendly Interface** — Access campus information through a single web application.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Campus Maps | Mapbox GL JS |
| AI Assistance | AI Chatbot integration |
| Dataset Management | Excel and Python |
| Development Environment | Visual Studio Code, Git, GitHub |

*The technologies listed reflect the intended project stack; individual features depend on their current implementation and configuration.*

## System Architecture

```text
             STUDENT / VISITOR
                    |
                    v
          FRONTEND WEB INTERFACE
                    |
          +---------+----------+
          |                    |
          v                    v
   CAMPUS SEARCH         AI CHATBOT
          |                    |
          +---------+----------+
                    |
                    v
             FLASK BACKEND
                    |
          +---------+----------+
          |                    |
          v                    v
      MYSQL DATABASE      GEMINI API
          |
          v
  CAMPUS INFORMATION

  MAPBOX INTEGRATION
  Interactive Map and Routes
```

## Project Structure

```text
AI_SMART_CAMPUS_AND_STUDENT_ASSISTENCE_SYSTEM_WITH_MAP_INTEGRATION/
│
├── BACKEND/
│   ├── app.py
│   ├── db.py
│   ├── import_data.py
│   ├── inspect_db.py
│   └── test_db.py
│
├── DATA/
│   └── Smart_Campus_Complete_Systematic_Dataset.xlsx
│
├── FRONTEND/
│   └── index_main.html
│
├── .gitignore
└── README.md
```

*The dataset filename and project structure may vary slightly depending on the latest version of the repository.*

## Getting Started

### Prerequisites

Install or configure the following before running the application:

- Python 3.11
- MySQL Server
- A modern web browser
- Visual Studio Code (recommended)
- Mapbox public access token
- Gemini API key, if AI chatbot functionality requires it

### 1. Clone the Repository

```bash
git clone https://github.com/saacheekothari1-pixel/AI_SMART_CAMPUS_AND_STUDENT-ASSISTENCE_SYSTEM_WITH_MAP_INTEGRATION.git
```

Navigate to the project directory:

```bash
cd AI_SMART_CAMPUS_AND_STUDENT-ASSISTENCE_SYSTEM_WITH_MAP_INTEGRATION
```

### 2. Configure the Backend

```powershell
cd BACKEND
```

Create a virtual environment if one does not already exist:

```powershell
py -3.11 -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required Python packages:

```powershell
pip install flask python-dotenv mysql-connector-python
```

Install any additional dependencies required by the application.

### 3. Configure Environment Variables

Create a `.env` file inside `BACKEND` and configure your local credentials.

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
GEMINI_API_KEY=your_gemini_api_key
```

Use the actual database name and configuration expected by the application.

**Security:** Never commit `.env` files, database passwords, Gemini API keys, or Mapbox secret tokens to GitHub. Use a Mapbox **public** token for browser-side map rendering.

### 4. Start the Backend

From the `BACKEND` directory, run:

```powershell
python app.py
```

Keep the terminal running while using the application.

### 5. Open the Frontend

Open `FRONTEND/index_main.html` in your browser, or serve it through the local web server configuration used by the project.

Ensure the frontend's API configuration points to the running Flask backend.

### 6. Verify the Database Connection

Use the project's database test script:

```powershell
python test_db.py
```

Make sure MySQL is running and the configured credentials are correct.

## Dataset

The project uses structured campus information to support search and student assistance, including:

- Classroom locations
- Faculty details
- Laboratory information
- Office and administrative service details
- Department information
- Building and floor information
- Seating and location records, where available

The dataset is intended to support consistent, database-driven responses and improve the accuracy of campus searches.

## How It Works

1. A student searches for a campus destination or asks a question.
2. The frontend sends the relevant request to the backend.
3. Flask processes the request and retrieves matching campus information from MySQL.
4. The chatbot can use the configured Gemini integration to assist with natural-language queries.
5. For navigation, Mapbox displays the campus map and the available route to the selected destination.
6. The application presents the resulting information to the student.

## Future Scope

- Indoor navigation with floor-wise maps.
- Voice-based campus assistance.
- Multilingual chatbot support.
- Mobile-friendly and progressive web application features.
- Real-time campus announcements and event information.
- Accessibility-focused navigation.
- An administrative interface for updating campus data.
- Improved natural-language search and location recommendations.

## Project Objective

To develop an intelligent, centralized campus assistance platform that reduces the time and effort required to locate campus facilities, access administrative information, and navigate between campus destinations.


This project is developed for academic and educational purposes. A formal open-source license can be added if the project is intended for public reuse.
