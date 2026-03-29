# Job Application Tracking System (ATS-lite)

A scalable, production-grade Applicant Tracking System (ATS-lite) full-stack web application designed to track job applications seamlessly.

## 🏗 Architecture
Follows a decoupled cloud-ready architecture pattern:
- **Backend:** API service built with **FastAPI** (Python) for high performance.
- **Database:** **Amazon RDS (MySQL)** for structured data storage (Users, Job Applications) via SQLAlchemy ORM.
- **File Storage:** **Amazon S3** for secure, direct-to-cloud uploading and downloading of CV documents using short-lived presigned URLs.
- **Frontend:** Single Page Application (SPA) built with **React** and **Vite**, featuring a premium modern Glassmorphism UI using Vanilla CSS.
- **Security:** JWT-based authentication with bcrypt password hashing.

## ✨ Core Features
- **Authentication**: Secure User Registration and Login using JWT Bearer tokens.
- **Dashboard**: View and manage all your job prospects in a clean, responsive grid layout.
- **Application CRUD**: Add, edit, remove, and view detailed job applications.
- **Status Tracking**: Visual, color-coded badges indicating current application status (Applied, Interviewing, Offer, Rejected, Withdrawn).
- **CV Storage**: Upload your CV dynamically to S3. Securely view/download your uploaded CVs anytime you need them.

## 🚀 Getting Started

### Prerequisites
- **Python** (v3.8+)
- **Node.js** (v16+) and **npm**
- **Amazon Web Services (AWS)** Account (S3 Bucket & associated IAM user credentials)
- **MySQL Database** (Amazon RDS instance or a local database)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Copy `.env.example` to `.env` and fill in your AWS credentials, JWT secret, and standard MySQL Database URL connection string.
   ```bash
   cp .env.example .env
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   > The API will be available at `http://localhost:8000`. You can test endpoints via the auto-generated Swagger documentation at `http://localhost:8000/docs`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   > The frontend UI will be securely served at `http://localhost:5173`.
