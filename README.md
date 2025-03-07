# Flask Task Management API 🚀

A **secure, scalable, and production-ready** Task Management API built with **Flask, SQLAlchemy, JWT Authentication, and AWS S3** for data visualization.

## **📌 Features**
✅ **Task Management** - Perform CRUD operations on tasks.
✅ **User Authentication** - Secure authentication using JWT tokens.
✅ **Data Visualization** - Generate insights & charts (Matplotlib, Seaborn).
✅ **Cloud Storage** - Store analytics images on AWS S3.
✅ **Database Support** - Uses PostgreSQL (AWS RDS) for persistence.
✅ **Security Best Practices** - Includes CORS, secure cookies, and rate limiting.
✅ **Dockerized Deployment** - Supports Docker & Gunicorn for production.

---

## **🚀 Getting Started**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/flask-task-api.git
cd flask-task-api
```

### **2️⃣ Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file:
```ini
DATABASE_URL=postgresql://your-username:your-password@your-rds-endpoint:5432/your-database
JWT_SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=your-bucket-name
DEBUG=False
```

### **5️⃣ Run the Flask App**
```bash
flask run
```
The API will be available at:
📌 **`http://127.0.0.1:5000`**

---

## **🛠 API Endpoints**

### **🔹 Authentication**
| Method | Endpoint         | Description       |
|--------|-----------------|------------------|
| `POST` | `/auth/login`    | User Login       |
| `POST` | `/auth/register` | User Registration |

### **🔹 Task Management**
| Method   | Endpoint          | Description              |
|----------|------------------|--------------------------|
| `POST`   | `/tasks/`         | Create a new task       |
| `GET`    | `/tasks/`         | Retrieve all tasks      |
| `GET`    | `/tasks/{id}/`    | Retrieve a specific task |
| `PUT`    | `/tasks/{id}/`    | Update a task           |
| `DELETE` | `/tasks/{id}/`    | Delete a task           |

### **🔹 Analytics**
| Method | Endpoint          | Description                   |
|--------|------------------|------------------------------|
| `GET`  | `/tasks/analytics/` | View task completion insights |

---

## **📦 Deployment with Docker**

### **1️⃣ Build and Run the Container**
```bash
docker build -t flask-task-api .
docker run -p 5000:5000 --env-file .env flask-task-api
```

### **2️⃣ Docker Compose (For Multi-Service Setup)**
Create `docker-compose.yml`:
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      - db
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: taskdb
```
Run with:
```bash
docker-compose up --build
```

---

## **🔍 Testing**
Run unit tests using:
```bash
python -m unittest discover tests/
```

---

## **📜 License**
This project is **MIT Licensed**. Feel free to use and modify.

---

### **🌟 Contribute**
- Feel free to **open issues** or submit **pull requests**.
- Contributions are welcome! 🚀
