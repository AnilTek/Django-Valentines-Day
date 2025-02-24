# 📌 Short Django-Valentines-Day Project Setup Guide
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
![Image](https://github.com/user-attachments/assets/5cacf47b-3c63-42fa-b280-0e823996384e)

![Image](https://github.com/user-attachments/assets/1de58185-3e2f-4d46-b47e-bd9ec5ff5cc9)

![Image](https://github.com/user-attachments/assets/38d0b4a5-2bb6-44f1-99f0-c9300cb689ed)
