# Testing Expenditure API - Quick Guide

## 🧪 Method 1: Using Python Test Script (Recommended)

### **File Created:** `test_expenditure.py`

This script automatically tests all HTTP methods in sequence.

### **Steps to Run:**

1. **Make sure Django server is running:**
   ```bash
   cd c:\Users\rakshith bandi\OneDrive\Desktop\HT_frontend\backend
   python manage.py runserver
   ```

2. **Update credentials in test_expenditure.py:**
   ```python
   USERNAME = "admin"  # Your admin username
   PASSWORD = "admin"  # Your admin password
   ```

3. **Run the test script:**
   ```bash
   python test_expenditure.py
   ```

### **What It Tests:**
- ✅ **LOGIN** - Authenticates with the API
- ✅ **GET ALL** - Retrieves all expenditures
- ✅ **POST** - Creates a new test expenditure
- ✅ **GET SINGLE** - Retrieves the created expenditure by ID
- ✅ **PUT** - Updates the expenditure
- ✅ **DELETE** - Deletes the expenditure
- ✅ **VERIFY** - Confirms deletion was successful

---

## 🌐 Method 2: Using Browser (Manual Testing)

### **1. GET - View All Expenditures**
Open in browser:
```
http://localhost:8000/api/expenditure/
```
**Expected:** JSON list of all expenditures

### **2. GET - View Single Expenditure**
```
http://localhost:8000/api/expenditure/1/
```
**Expected:** JSON object with expenditure details

---

## 🔧 Method 3: Using Postman/Thunder Client

### **Setup:**
1. Create a new request collection
2. Set base URL: `http://localhost:8000`

### **Test Requests:**

#### **1. Login First (Required for POST/PUT/DELETE)**
```
POST http://localhost:8000/api/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

#### **2. GET All Expenditures**
```
GET http://localhost:8000/api/expenditure/
```

#### **3. POST Create Expenditure**
```
POST http://localhost:8000/api/expenditure/
Content-Type: application/json

{
  "year": "2025",
  "purpose": "Test expense from Postman",
  "amountSpent": 1500.50
}
```

#### **4. PUT Update Expenditure**
```
PUT http://localhost:8000/api/expenditure/1/
Content-Type: application/json

{
  "year": "2025",
  "purpose": "Updated expense",
  "amountSpent": 2000.00
}
```

#### **5. DELETE Expenditure**
```
DELETE http://localhost:8000/api/expenditure/1/
```

---

## 🖥️ Method 4: Using cURL (Command Line)

### **1. GET All**
```bash
curl http://localhost:8000/api/expenditure/
```

### **2. POST Create**
```bash
curl -X POST http://localhost:8000/api/expenditure/ \
  -H "Content-Type: application/json" \
  -d "{\"year\":\"2025\",\"purpose\":\"Test\",\"amountSpent\":1000}"
```

### **3. PUT Update**
```bash
curl -X PUT http://localhost:8000/api/expenditure/1/ \
  -H "Content-Type: application/json" \
  -d "{\"year\":\"2025\",\"purpose\":\"Updated\",\"amountSpent\":2000}"
```

### **4. DELETE**
```bash
curl -X DELETE http://localhost:8000/api/expenditure/1/
```

---

## 🎯 Method 5: Using Frontend UI (End-to-End Test)

### **Steps:**

1. **Start both servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python manage.py runserver
   
   # Terminal 2 - Frontend
   cd ht_portal
   npm run dev
   ```

2. **Open browser:**
   ```
   http://localhost:5173
   ```

3. **Login** with your credentials

4. **Navigate to Expenditures** from sidebar

5. **Test operations:**
   - ✅ View existing expenditures (GET)
   - ✅ Click "Add Expenditure" (POST)
   - ✅ Fill form and save
   - ✅ Click delete icon (DELETE)

---

## 📊 Expected Results

### **Successful Responses:**

| Method | Status Code | Response |
|--------|-------------|----------|
| GET | 200 | JSON array/object |
| POST | 201 | Created object with ID |
| PUT | 200 | Updated object |
| DELETE | 204 | No content |

### **Error Responses:**

| Status | Meaning |
|--------|---------|
| 400 | Bad Request (invalid data) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not Found (ID doesn't exist) |
| 500 | Server Error |

---

## 🔍 Troubleshooting

### **If tests fail:**

1. **Check Django server is running:**
   ```bash
   python manage.py runserver
   ```

2. **Check database migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Verify app is installed:**
   Check `settings.py` → `INSTALLED_APPS` → `'expenditure'`

4. **Check URL routing:**
   Check `urls.py` → `path('api/expenditure/', ...)`

5. **Test database connection:**
   ```bash
   python manage.py dbshell
   SELECT * FROM expenditure_expenditure;
   ```

6. **Check permissions:**
   - Make sure you're logged in as Admin or Manager
   - Check `IsAdminOrManagerOrReadOnly` permission

---

## ✅ Quick Verification Checklist

- [ ] Django server running on port 8000
- [ ] Can access `http://localhost:8000/api/expenditure/`
- [ ] Can see JSON response
- [ ] Can login successfully
- [ ] Can create expenditure (POST)
- [ ] Can update expenditure (PUT)
- [ ] Can delete expenditure (DELETE)
- [ ] Data persists in PostgreSQL
- [ ] Frontend UI works correctly

---

## 🎉 Success Indicators

**All HTTP methods are working if:**
- ✅ Python test script shows all tests PASSED
- ✅ Browser shows JSON data for GET requests
- ✅ POST creates new records in database
- ✅ PUT updates existing records
- ✅ DELETE removes records
- ✅ Frontend UI can perform all operations
- ✅ Data persists after server restart

---

**Recommended:** Run the Python test script first for automated verification!
