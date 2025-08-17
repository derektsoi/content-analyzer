# Python Project Setup Checklist

## Professional Virtual Environment Workflow

### 🚀 Initial Project Setup

1. **Create Project Directory**
   ```bash
   mkdir my-project
   cd my-project
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv (recommended for most projects)
   python3 -m venv venv
   
   # Alternative: Using conda (for data science)
   conda create --name my-project python=3.11
   ```

3. **Activate Virtual Environment**
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   
   # Conda
   conda activate my-project
   ```

4. **Verify Environment**
   ```bash
   which python  # Should point to venv/bin/python
   python --version
   ```

### 📦 Dependency Management

5. **Install Dependencies**
   ```bash
   # Install packages as needed
   pip install requests beautifulsoup4
   
   # Or from requirements.txt
   pip install -r requirements.txt
   ```

6. **Create/Update requirements.txt**
   ```bash
   # Generate exact versions (recommended for production)
   pip freeze > requirements.txt
   
   # Or create manually with flexible versions
   echo "requests>=2.31.0" >> requirements.txt
   echo "beautifulsoup4>=4.12.0" >> requirements.txt
   ```

### 🔧 Project Structure

7. **Create Standard Project Structure**
   ```
   my-project/
   ├── venv/                 # Virtual environment (don't commit)
   ├── src/                  # Source code
   ├── tests/                # Test files
   ├── requirements.txt      # Dependencies
   ├── .gitignore           # Git ignore rules
   ├── README.md            # Project documentation
   └── setup.py             # Package setup (if distributing)
   ```

### 🚫 Git Integration

8. **Create .gitignore**
   ```bash
   # Add Python-specific ignore rules
   curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
   ```

9. **Initialize Git Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial project setup"
   ```

### 🔄 Daily Workflow

10. **Starting Work Session**
    ```bash
    cd my-project
    source venv/bin/activate  # Always activate first!
    ```

11. **Installing New Dependencies**
    ```bash
    pip install new-package
    pip freeze > requirements.txt  # Update requirements
    git add requirements.txt
    git commit -m "Add new-package dependency"
    ```

12. **Ending Work Session**
    ```bash
    deactivate  # Exit virtual environment
    ```

### 🤝 Team Collaboration

13. **Setting Up Teammate's Environment**
    ```bash
    git clone project-repo
    cd project-repo
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

14. **Sharing Environment Updates**
    ```bash
    # After installing new packages
    pip freeze > requirements.txt
    git add requirements.txt
    git commit -m "Update dependencies"
    git push
    ```

### 🚨 Common Pitfalls to Avoid

❌ **DON'T:**
- Install packages globally (`pip install` without virtual environment)
- Commit `venv/` directory to git
- Mix system Python with project dependencies
- Forget to activate virtual environment
- Use `sudo pip install`

✅ **DO:**
- Always activate virtual environment before installing packages
- Use `requirements.txt` for reproducible builds
- Keep virtual environments project-specific
- Document Python version requirements
- Use `.gitignore` to exclude virtual environment

### 🔍 Troubleshooting

**Environment Not Activating:**
```bash
# Check if virtual environment exists
ls venv/bin/activate

# Recreate if corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Wrong Python Version:**
```bash
# Create with specific Python version
python3.11 -m venv venv
# or
virtualenv -p python3.11 venv
```

**Package Conflicts:**
```bash
# Create clean environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🏭 Production Considerations

- **Pin exact versions** in requirements.txt for production
- **Use virtual environments** in Docker containers
- **Consider dependency vulnerability scanning**
- **Document Python version compatibility**
- **Use environment variables** for configuration

### 📝 Environment Variables

Create `.env` file for local configuration:
```bash
# .env (don't commit to git)
DEBUG=True
API_KEY=your-secret-key
DATABASE_URL=sqlite:///local.db
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
```

---

## Quick Reference Commands

```bash
# Create & activate
python3 -m venv venv && source venv/bin/activate

# Install & save dependencies
pip install package-name && pip freeze > requirements.txt

# Clone & setup teammate environment
git clone repo && cd repo && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Deactivate when done
deactivate
```

This checklist ensures consistent, professional Python development workflows! 🐍✨