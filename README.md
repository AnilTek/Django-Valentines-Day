# 📌 Short Django Project Setup Guide

This is a simple Django-based project that allows users to modify templates, configure authentication settings, and customize quiz data.

---

## 🚀 Installation

### 1️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Database Setup
```bash
python manage.py migrate
```

### 4️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

### 5️⃣ Configuration
Modify the following settings in the **views.py** file according to your preferences:
```python
PASSWORD_HASH = ""  # Set your password here (not hashed)
SECRET_ENTRANCE = ""  # Set your custom secret entrance
```

### 6️⃣ Customization
- **Templates**: Modify templates to customize the UI.
- **Quiz Data**: Update `quiz_data.json` to add your own quiz questions.

### 7️⃣ Admin Panel
Most configurations and modifications can be managed through:
```bash
http://127.0.0.1:8000/admin/
```
Log in with the superuser credentials to access the host/admin panel.

---

🚀 **Your customized Django project is now ready!**
