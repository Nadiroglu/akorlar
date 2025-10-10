# 🛠 Akorlar Scripts Directory

This directory contains utility scripts for the Akorlar project.

## 📁 **Available Scripts**

### **Environment & Testing**
- **`verify_environment.py`** - Check if virtual environments and dependencies are properly set up
- **`test_api.py`** - Comprehensive API testing script
- **`test_admin_auth.py`** - Admin authentication testing helper

### **Development**
- **`start_servers.py`** - Start both backend and frontend servers simultaneously

## 🚀 **Quick Start**

### **Check Environment**
```bash
cd /Users/nile/Projects/akorlar
python scripts/verify_environment.py
```

### **Test APIs**
```bash
cd /Users/nile/Projects/akorlar
python scripts/test_api.py
```

### **Test Admin Authentication**
```bash
cd /Users/nile/Projects/akorlar
python scripts/test_admin_auth.py
```

### **Start Both Servers**
```bash
cd /Users/nile/Projects/akorlar
python scripts/start_servers.py
```

## 📋 **Script Details**

### **verify_environment.py**
Checks:
- ✅ Backend virtual environment
- ✅ Python and Django versions
- ✅ Frontend Node.js and npm
- ✅ Dependencies installation
- ✅ API endpoints connectivity

### **test_api.py**
Tests:
- 🔓 All public API endpoints
- 🔍 Filtering and search functionality
- 📝 Song request creation
- 🌐 HTML browsable API
- 🔐 Admin endpoints (authentication required)

### **test_admin_auth.py**
Helps with:
- 🔑 Admin authentication setup
- 🍪 Session cookie extraction
- 🔐 Basic authentication testing
- 📋 Postman setup instructions

### **start_servers.py**
Features:
- 🐍 Starts Django backend (port 8000)
- ⚛️ Starts Vite frontend (port 5173)
- 🛑 Graceful shutdown with Ctrl+C
- ✅ Error handling and status reporting

## 🎯 **Usage Examples**

### **Before Development**
```bash
# Verify everything is set up correctly
python scripts/verify_environment.py
```

### **API Testing**
```bash
# Test all public endpoints
python scripts/test_api.py

# Test admin authentication
python scripts/test_admin_auth.py
```

### **Development Workflow**
```bash
# Start both servers for development
python scripts/start_servers.py

# In another terminal, run tests
python scripts/test_api.py
```

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Script not found**: Make sure you're in the project root directory
2. **Permission denied**: Make sure scripts are executable (`chmod +x script.py`)
3. **Module not found**: Install required dependencies (`pip install requests`)

### **Dependencies**
- **Python**: 3.13+ (with virtual environment)
- **Node.js**: 18+ (with npm)
- **Python packages**: requests (for API testing)

## 📚 **Related Documentation**

- **`../POSTMAN_TESTING_GUIDE.md`** - Detailed Postman API testing guide
- **`../VIRTUAL_ENVIRONMENT_GUIDE.md`** - Virtual environment setup guide
- **`../backend/README.md`** - Backend documentation
- **`../client/README.md`** - Frontend documentation

---

**Happy coding! 🎵**




