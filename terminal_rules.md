# Terminal Hanging Prevention Rules

## 🚨 CRITICAL RULES TO PREVENT TERMINAL HANGS

### 1. ALWAYS Use Timeouts
- **NEVER** run `curl` without `--max-time` parameter
- **NEVER** run `docker logs` without `--tail` parameter
- **NEVER** run long-running commands without background execution

### 2. Docker Container Management
- **ALWAYS** check container status before running commands
- **ALWAYS** use `./manage_docker.sh status` to verify containers are healthy
- **NEVER** run commands against restarting containers
- **ALWAYS** wait for containers to be "Up" and "healthy" before testing

### 3. API Testing Protocol
```bash
# ✅ CORRECT - Always use timeout
curl -s --max-time 10 -X POST http://localhost:5000/api/endpoint

# ❌ WRONG - No timeout, can hang indefinitely
curl -X POST http://localhost:5000/api/endpoint
```

### 4. Log Checking Protocol
```bash
# ✅ CORRECT - Limit log output
docker logs landscaper-web --tail 20

# ❌ WRONG - Can hang if container is restarting
docker logs landscaper-web
```

### 5. Debugging Workflow
1. **Check container status first**
2. **If container is restarting, check logs with limits**
3. **Fix the issue before testing**
4. **Rebuild only when necessary**
5. **Test with timeouts**

### 6. Emergency Break Commands
```bash
# Stop all containers
./manage_docker.sh stop

# Kill hanging processes
pkill -f curl
pkill -f docker

# Clear terminal
clear
```

### 7. Testing Checklist
- [ ] Container status is "Up" and "healthy"
- [ ] Using `--max-time` with curl
- [ ] Using `--tail` with docker logs
- [ ] Have emergency break commands ready
- [ ] Testing one endpoint at a time

### 8. When Container is Restarting
1. **STOP** all testing
2. **Check logs** with `--tail 20`
3. **Identify the error**
4. **Fix the code**
5. **Rebuild container**
6. **Wait for healthy status**
7. **Then test**

### 9. Code Changes Protocol
1. **Make small, incremental changes**
2. **Test syntax locally first** (`python3 -c "import ast; ast.parse(open('file.py').read())"`)
3. **Rebuild container**
4. **Wait for healthy status**
5. **Test with timeout**

### 10. Recovery from Hangs
```bash
# If terminal is hanging:
# 1. Press Ctrl+C
# 2. Run emergency break commands
# 3. Check container status
# 4. Fix the root cause
# 5. Resume with proper timeouts
```

## 🎯 CURRENT ISSUE: Materials Calculator Division by Zero

### Problem Analysis
- Container keeps restarting due to syntax errors
- Division by zero error in materials calculation
- Terminal hangs when testing broken endpoints

### Solution Strategy
1. **Fix syntax errors first**
2. **Add proper error handling**
3. **Test locally before Docker**
4. **Use timeouts for all API calls**
5. **Implement proper logging**

### Immediate Actions
1. Stop current testing
2. Fix the syntax error in `landscaping_materials.py`
3. Add proper error handling for division by zero
4. Test locally first
5. Rebuild container
6. Test with timeouts

## 📋 RULES SUMMARY
- **ALWAYS** use timeouts
- **NEVER** test against restarting containers
- **ALWAYS** check status first
- **ALWAYS** fix syntax errors before testing
- **ALWAYS** have emergency break commands ready
