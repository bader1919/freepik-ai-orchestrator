# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues with the Freepik AI Orchestrator.

## Quick Diagnostics

### System Health Check

Before diving into specific issues, run these quick checks:

1. **Application Status**
   ```bash
   curl http://localhost:8501/health
   ```

2. **API Connectivity**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        https://api.freepik-orchestrator.com/v1/health
   ```

3. **Database Connection**
   - Check if database is accessible
   - Verify connection string
   - Test with simple query

4. **Environment Variables**
   ```bash
   # Check if required variables are set
   echo $FREEPIK_API_KEY
   echo $OPENAI_API_KEY
   ```

## Common Issues and Solutions

### 1. Application Won't Start

#### Issue: "Port 8501 already in use"

**Symptoms:**
- Error message about port being occupied
- Application fails to start
- Cannot access web interface

**Solutions:**

**Option A: Kill existing process**
```bash
# Find process using port 8501
netstat -tulpn | grep 8501
# Or on Windows
netstat -ano | findstr 8501

# Kill the process (replace PID with actual ID)
kill -9 PID
# Or on Windows
taskkill /PID PID /F
```

**Option B: Use different port**
```bash
streamlit run app.py --server.port 8502
```

**Option C: Update configuration**
```toml
# .streamlit/config.toml
[server]
port = 8502
```

#### Issue: "Import errors" or "Module not found"

**Symptoms:**
- Python import errors on startup
- Missing module messages
- Application crashes during initialization

**Solutions:**

1. **Check Python version**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check virtual environment**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Verify installation
   pip list
   ```

4. **Clear Python cache**
   ```bash
   find . -type d -name "__pycache__" -delete
   find . -name "*.pyc" -delete
   ```

#### Issue: "Environment variables not found"

**Symptoms:**
- Missing API key errors
- Configuration errors
- Application starts but features don't work

**Solutions:**

1. **Verify .env file exists**
   ```bash
   ls -la .env
   cat .env  # Check contents
   ```

2. **Check file format**
   ```bash
   # Correct format
   FREEPIK_API_KEY=your_key_here
   OPENAI_API_KEY=your_openai_key
   
   # Incorrect (avoid spaces around =)
   FREEPIK_API_KEY = your_key_here
   ```

3. **Load environment manually**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   import os
   print(os.getenv('FREEPIK_API_KEY'))
   ```

### 2. Image Generation Issues

#### Issue: "Generation failed" errors

**Symptoms:**
- Images fail to generate
- Error messages in UI
- API returns 500 errors

**Diagnostic Steps:**

1. **Check API key validity**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        https://api.freepik.com/v1/account
   ```

2. **Verify prompt content**
   - Check for prohibited content
   - Ensure prompt is not empty
   - Try simpler prompts

3. **Test different models**
   - Switch from auto to specific model
   - Try Classic Fast for testing
   - Compare results across models

**Common Solutions:**

**Invalid API Key**
```python
# Verify in Python
import os
from core.freepik_client import FreepikClient

api_key = os.getenv('FREEPIK_API_KEY')
print(f"API Key: {api_key[:10]}...")  # Show first 10 chars

client = FreepikClient(api_key)
# Test connection
```

**Content Policy Violations**
- Remove sensitive content from prompts
- Avoid copyrighted material references
- Use general descriptions instead of specific people

**Rate Limiting**
```python
# Add delays between requests
import time
time.sleep(2)  # Wait 2 seconds between generations
```

#### Issue: "Poor quality results"

**Symptoms:**
- Generated images don't match expectations
- Low quality or distorted results
- Inconsistent outputs

**Optimization Strategies:**

1. **Improve prompt quality**
   ```
   # Poor prompt
   "person"
   
   # Better prompt
   "Professional headshot of a businesswoman, confident expression, 
   modern office background, natural lighting, high resolution"
   ```

2. **Use LLM enhancement**
   - Enable prompt optimization
   - Review enhanced prompts
   - Learn from successful patterns

3. **Try different models**
   - Imagen3 for photorealism
   - Mystic for artistic content
   - Flux Dev for balanced results

4. **Adjust quality settings**
   ```python
   generation_params = {
       "quality_level": 9,  # Higher quality (1-10)
       "style": "photorealistic",
       "enhance_prompt": True
   }
   ```

#### Issue: "Slow generation times"

**Symptoms:**
- Long wait times for results
- Timeouts
- Poor user experience

**Solutions:**

1. **Choose faster models**
   - Use Classic Fast for testing
   - Reserve premium models for final output
   - Consider batch processing

2. **Optimize infrastructure**
   ```yaml
   # docker-compose.yml
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
   ```

3. **Use async processing**
   ```python
   # Generate with webhook
   result = client.generate_async(
       prompt="Your prompt",
       webhook_url="https://your-app.com/webhook"
   )
   ```

4. **Monitor system resources**
   ```bash
   # Check CPU and memory usage
   htop
   # Or
   docker stats
   ```

### 3. Database Issues

#### Issue: "Database connection failed"

**Symptoms:**
- Application crashes on database access
- Connection timeout errors
- Data not persisting

**Diagnostic Steps:**

1. **Test database connection**
   ```bash
   # For PostgreSQL
   psql $DATABASE_URL -c "SELECT 1;"
   
   # For SQLite
   sqlite3 freepik_orchestrator.db ".tables"
   ```

2. **Check database URL format**
   ```bash
   # PostgreSQL
   DATABASE_URL=postgresql://user:password@host:port/database
   
   # SQLite
   DATABASE_URL=sqlite:///path/to/database.db
   ```

3. **Verify database exists**
   ```python
   from database.db import init_db
   init_db()  # Create tables if they don't exist
   ```

**Solutions:**

**Connection Issues**
```python
# Test connection in Python
import psycopg2
from sqlalchemy import create_engine

# Test SQLAlchemy connection
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())
```

**Migration Issues**
```bash
# Reset database (development only)
rm freepik_orchestrator.db  # SQLite
python -c "from database.db import init_db; init_db()"
```

**Permission Issues**
```bash
# Check file permissions (SQLite)
ls -la freepik_orchestrator.db
chmod 664 freepik_orchestrator.db
```

#### Issue: "Slow database queries"

**Symptoms:**
- Application responds slowly
- Database timeouts
- High CPU usage

**Solutions:**

1. **Add database indexes**
   ```sql
   CREATE INDEX idx_task_id ON generations(task_id);
   CREATE INDEX idx_created_at ON generations(created_at);
   ```

2. **Optimize queries**
   ```python
   # Use pagination
   from sqlalchemy import desc
   
   results = session.query(Generation)\
       .order_by(desc(Generation.created_at))\
       .limit(50)\
       .offset(page * 50)
   ```

3. **Connection pooling**
   ```python
   from sqlalchemy import create_engine
   
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=30,
       pool_timeout=30
   )
   ```

### 4. UI and Interface Issues

#### Issue: "Streamlit interface not loading"

**Symptoms:**
- Blank page or loading indefinitely
- JavaScript errors in browser console
- UI components not responding

**Solutions:**

1. **Clear browser cache**
   - Hard refresh (Ctrl+F5)
   - Clear browser cache and cookies
   - Try incognito/private mode

2. **Check browser compatibility**
   - Use modern browsers (Chrome, Firefox, Safari, Edge)
   - Disable browser extensions
   - Check for JavaScript errors in console

3. **Verify Streamlit configuration**
   ```toml
   # .streamlit/config.toml
   [server]
   enableCORS = false
   enableXsrfProtection = true
   
   [browser]
   gatherUsageStats = false
   ```

4. **Restart application**
   ```bash
   # Stop application
   Ctrl+C
   
   # Clear Streamlit cache
   streamlit cache clear
   
   # Restart
   streamlit run app.py
   ```

#### Issue: "UI components not working"

**Symptoms:**
- Buttons don't respond
- Form submissions fail
- State not updating

**Solutions:**

1. **Check Streamlit version**
   ```bash
   pip show streamlit
   pip install streamlit --upgrade
   ```

2. **Review session state**
   ```python
   # Debug session state
   import streamlit as st
   st.write(st.session_state)
   ```

3. **Clear session state**
   ```python
   # Add to app
   if st.button("Clear Session"):
       for key in st.session_state.keys():
           del st.session_state[key]
   ```

### 5. API Integration Issues

#### Issue: "API requests failing"

**Symptoms:**
- 401 Unauthorized errors
- 429 Rate limit errors
- Connection timeouts

**Diagnostic Steps:**

1. **Test API directly**
   ```bash
   curl -X POST "https://api.freepik-orchestrator.com/v1/generate" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "test image"}'
   ```

2. **Check API key format**
   ```python
   # Verify API key format
   import re
   api_key = "your_api_key"
   if re.match(r'^[a-zA-Z0-9_-]+$', api_key):
       print("API key format looks correct")
   ```

**Solutions:**

**Authentication Issues**
```python
# Verify API key is being sent
import requests

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Log headers (remove in production)
print(f"Headers: {headers}")
```

**Rate Limiting**
```python
# Implement exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(delay)
            else:
                raise
```

**Connection Issues**
```python
# Add timeout and retry logic
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

### 6. Webhook Issues

#### Issue: "Webhooks not being received"

**Symptoms:**
- No webhook notifications
- Missing completion callbacks
- Async operations not updating

**Diagnostic Steps:**

1. **Test webhook endpoint**
   ```bash
   # Test if your webhook URL is accessible
   curl -X POST "https://your-app.com/webhook" \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

2. **Check webhook logs**
   ```bash
   # Check server logs for webhook attempts
   tail -f /var/log/nginx/access.log | grep webhook
   ```

**Solutions:**

**URL Accessibility**
- Ensure webhook URL is publicly accessible
- Use HTTPS (required for webhooks)
- Check firewall and security group settings

**Signature Verification**
```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)

# In your webhook handler
if not verify_webhook_signature(request.body, request.headers['X-Signature'], WEBHOOK_SECRET):
    return "Invalid signature", 401
```

**Webhook Handler Example**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        event_type = data.get('event')
        
        if event_type == 'generation.completed':
            # Handle completed generation
            handle_generation_complete(data['data'])
        elif event_type == 'generation.failed':
            # Handle failed generation
            handle_generation_failed(data['data'])
            
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500
```

## Performance Optimization

### 1. Slow Application Performance

**Symptoms:**
- High response times
- UI lag
- Resource exhaustion

**Solutions:**

1. **Profile application**
   ```python
   # Add performance monitoring
   import time
   import functools
   
   def timing_decorator(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           end = time.time()
           print(f"{func.__name__} took {end-start:.2f} seconds")
           return result
       return wrapper
   ```

2. **Optimize database queries**
   ```python
   # Use connection pooling
   from sqlalchemy.pool import QueuePool
   
   engine = create_engine(
       DATABASE_URL,
       poolclass=QueuePool,
       pool_size=10,
       max_overflow=20
   )
   ```

3. **Implement caching**
   ```python
   import streamlit as st
   
   @st.cache_data
   def expensive_computation(data):
       # Cached function
       return processed_data
   ```

### 2. High Memory Usage

**Symptoms:**
- Out of memory errors
- System slowdowns
- Container restarts

**Solutions:**

1. **Monitor memory usage**
   ```bash
   # Check memory usage
   free -h
   docker stats
   ```

2. **Optimize image handling**
   ```python
   from PIL import Image
   
   # Resize images before processing
   def optimize_image(image_path, max_size=(1024, 1024)):
       with Image.open(image_path) as img:
           img.thumbnail(max_size, Image.Resampling.LANCZOS)
           return img
   ```

3. **Clean up resources**
   ```python
   # Proper resource cleanup
   try:
       # Process image
       pass
   finally:
       # Clean up temporary files
       if os.path.exists(temp_file):
           os.remove(temp_file)
   ```

## Error Code Reference

### HTTP Status Codes

| Code | Description | Common Causes | Solutions |
|------|-------------|---------------|-----------|
| 400 | Bad Request | Invalid prompt, malformed JSON | Check request format |
| 401 | Unauthorized | Invalid API key | Verify API key |
| 403 | Forbidden | Insufficient permissions | Check account status |
| 429 | Too Many Requests | Rate limit exceeded | Implement backoff |
| 500 | Internal Server Error | Server issues | Contact support |

### Application Error Codes

| Code | Description | Solutions |
|------|-------------|-----------|
| `FREEPIK_001` | API key invalid | Update API key |
| `FREEPIK_002` | Prompt too long | Shorten prompt |
| `FREEPIK_003` | Model unavailable | Try different model |
| `FREEPIK_004` | Content policy violation | Modify prompt |
| `FREEPIK_005` | Generation timeout | Try again or use faster model |

## Getting Help

### Self-Service Options

1. **Check System Status**
   - Visit [status.freepik-orchestrator.com](https://status.freepik-orchestrator.com)
   - Check for known issues

2. **Search Documentation**
   - Use site search
   - Check FAQ section
   - Review API documentation

3. **Community Support**
   - [GitHub Discussions](https://github.com/yourusername/freepik-ai-orchestrator/discussions)
   - [Discord Community](https://discord.gg/freepik-ai)
   - Stack Overflow (tag: freepik-orchestrator)

### Contact Support

Before contacting support, gather this information:

1. **System Information**
   - Operating system and version
   - Python version
   - Application version
   - Browser (if UI issue)

2. **Error Details**
   - Complete error messages
   - Steps to reproduce
   - Screenshots or logs
   - Time when issue occurred

3. **Configuration**
   - Environment variables (without sensitive data)
   - Configuration files
   - Network setup (if relevant)

**Support Channels:**
- **Email**: support@freepik-orchestrator.com
- **Discord**: [Live chat support](https://discord.gg/freepik-ai)
- **Enterprise**: Dedicated support portal

### Emergency Support

For critical production issues:

1. **Enterprise customers**: Use priority support channel
2. **Include "URGENT" in subject line**
3. **Provide full system impact assessment**
4. **Include business impact statement**

Remember: Most issues can be resolved quickly with the right diagnostic information. Take time to gather details before reaching out for help.
