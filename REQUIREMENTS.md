# Landscaper Project Requirements

## 🎯 **Core Requirements**

### **Frontend Technology Stack**

- **Framework:** React (NOT using Vite)
- **Build Tool:** Webpack or Create React App
- **Styling:** Tailwind CSS
- **State Management:** React Hooks (useState, useEffect, useContext)
- **Routing:** React Router
- **HTTP Client:** Axios or Fetch API

### **Backend Technology Stack**

- **Framework:** Flask (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **API:** RESTful endpoints
- **Authentication:** JWT tokens

### **System Requirements**

- **Port Management:** ALWAYS check port availability before starting servers
- **MCP Integration:** Context Manager and Persona Manager integration
- **Real-time Updates:** WebSocket connections for live data
- **Error Handling:** Comprehensive error handling and logging

## 🚀 **Current Implementation Status**

### **✅ Completed Features**

- Flask backend with PostgreSQL database
- MCP Context Manager and Persona Manager integration
- Materials calculator API
- Database models and migrations
- Docker containerization

### **🔄 In Progress**

- React frontend implementation (needs to be updated from current setup)
- Port checking system implementation
- Materials calculator frontend integration

### **📋 Next Steps**

1. **Create React Frontend:** Set up React app without Vite
2. **Implement Port Checking Rule:** Make it mandatory before server startup
3. **Materials Calculator UI:** Build React components for materials calculation
4. **Dashboard Integration:** Connect React frontend with Flask backend

## 🔧 **System Rules**

### **Port Management Rule**

**MANDATORY:** Before starting any server, always run port availability check:

```bash
./check_ports_and_start.sh
```

**Port Assignments:**

- **Port 5000:** Flask Backend (primary)
- **Port 5001:** Flask Backend (fallback)
- **Port 8000:** Context Manager MCP
- **Port 8001:** Persona Manager MCP
- **Port 5433:** PostgreSQL Database

### **Development Workflow**

1. **Always check ports** before starting development
2. **Use React** for frontend (no Vite)
3. **Test all integrations** before marking features complete
4. **Update MCP context** with progress
5. **Document all changes** and requirements

## 📊 **Feature Priorities**

### **High Priority**

1. ✅ **MCP Integration:** Context and Persona managers working
2. 🔄 **Port Management:** System implemented, needs to be mandatory
3. 🔄 **React Frontend:** Needs to be rebuilt without Vite
4. 🔄 **Materials Calculator:** API working, needs React UI

### **Medium Priority**

1. **Dashboard Components:** React dashboard with real-time data
2. **User Authentication:** JWT-based auth system
3. **Project Management:** Project creation and tracking
4. **Analytics:** Usage analytics and reporting

### **Low Priority**

1. **Mobile Responsiveness:** PWA features
2. **Advanced Features:** Advanced calculations and reporting
3. **Integration Testing:** Comprehensive test suite

## 🛠️ **Technical Specifications**

### **React Frontend Requirements**

- **No Vite:** Use Create React App or custom Webpack setup
- **Component Structure:** Modular, reusable components
- **State Management:** React Hooks for local state, Context for global state
- **API Integration:** Axios for HTTP requests
- **Real-time Updates:** WebSocket integration for live data
- **Error Boundaries:** Proper error handling and user feedback

### **Backend API Requirements**

- **RESTful Design:** Standard HTTP methods and status codes
- **JSON Responses:** Consistent response format
- **Error Handling:** Proper error messages and logging
- **Authentication:** JWT token-based authentication
- **Validation:** Input validation and sanitization

### **Database Requirements**

- **PostgreSQL:** Primary database
- **Migrations:** Version-controlled schema changes
- **Seeding:** Initial data population
- **Backup:** Regular backup procedures

## 📝 **Documentation Requirements**

- **API Documentation:** OpenAPI/Swagger documentation
- **Component Documentation:** React component documentation
- **Setup Instructions:** Clear setup and deployment guides
- **Troubleshooting:** Common issues and solutions
