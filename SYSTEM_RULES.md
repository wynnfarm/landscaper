# System Rules and Development Guidelines

## 🚨 **MANDATORY RULES**

### **1. Port Management Rule**

**ALWAYS CHECK PORTS BEFORE STARTING SERVERS**

Before starting any development work or servers, you MUST run:

```bash
./check_ports_and_start.sh
```

**Why this is mandatory:**

- Prevents port conflicts that cause server startup failures
- Ensures all services start on correct ports
- Provides clear status of all running services
- Automates the startup process

**Port Assignments:**

- **Port 5000:** Flask Backend (primary)
- **Port 5001:** Flask Backend (fallback)
- **Port 8000:** Context Manager MCP
- **Port 8001:** Persona Manager MCP
- **Port 5433:** PostgreSQL Database

### **2. React Frontend Rule**

**USE CREATE REACT APP (NOT VITE)**

The frontend MUST use:

- **Create React App** for setup and build tools
- **React Router** for navigation
- **Axios** for API calls
- **Tailwind CSS** for styling

**Current Setup:** ✅ Already using Create React App

### **3. Testing Rule**

**TEST ALL FEATURES BEFORE MARKING COMPLETE**

Before considering any feature complete:

1. Test API endpoints
2. Test React components
3. Test MCP integration
4. Test port availability
5. Update MCP context with progress

## 🔧 **Development Workflow**

### **Daily Startup Process**

1. **Check Ports:** `./check_ports_and_start.sh`
2. **Verify Services:** Confirm all services are running
3. **Test Integration:** Verify MCP tools are working
4. **Start Development:** Begin feature work

### **Feature Completion Process**

1. **Implement Feature:** Code the feature
2. **Test Thoroughly:** Test all aspects
3. **Update Context:** Add to MCP context
4. **Document Changes:** Update documentation
5. **Move to Next:** Identify and start next priority

## 📋 **Current Status**

### **✅ Working Systems**

- **React Frontend:** Create React App setup ✅
- **Flask Backend:** Running on port 5000 ✅
- **MCP Integration:** Context and Persona managers ✅
- **Port Checking:** Script implemented ✅

### **🔄 Current Task**

- **Materials Calculator:** API working, needs frontend integration

### **📊 Next Priorities**

1. **Materials Calculator UI:** Connect React components to Flask API
2. **Dashboard Integration:** Real-time data updates
3. **Error Handling:** Comprehensive error boundaries
4. **Testing:** End-to-end testing suite

## 🛠️ **Technical Standards**

### **Code Quality**

- **ESLint:** Follow React best practices
- **Error Boundaries:** Proper error handling
- **Loading States:** User feedback during operations
- **Responsive Design:** Mobile-friendly interfaces

### **API Integration**

- **RESTful Design:** Standard HTTP methods
- **Error Handling:** Proper error responses
- **Validation:** Input validation
- **Documentation:** API documentation

### **State Management**

- **React Hooks:** useState, useEffect, useContext
- **API Calls:** Axios for HTTP requests
- **Real-time Updates:** WebSocket integration
- **Error States:** Proper error handling

## 📝 **Documentation Requirements**

### **Code Documentation**

- **Component Comments:** Explain complex logic
- **API Documentation:** OpenAPI/Swagger
- **Setup Instructions:** Clear setup guides
- **Troubleshooting:** Common issues and solutions

### **Progress Tracking**

- **MCP Context:** Update with completed features
- **Requirements:** Keep requirements updated
- **Status Reports:** Regular status updates
- **Next Steps:** Clear next priorities

---

**Remember:** Always check ports before starting servers, use React (not Vite), and test thoroughly before marking features complete.
