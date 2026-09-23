## 🚀 Overview
This tool extracts critical data from Cisco `.txt` log files, including:
*   **Hostname**
*   **Software Version**
*   **Memory Usage** (Used & Free)
*   **CPU Load** (5-minute average)

It features a built-in **Export to Excel** button and a **TSV Copy** function for easy reporting.

---

## 🛠 Manual Installation (Python Terminal)

Use this method to run the app directly on your Ubuntu system.

### 1. Update and Install Pip
```
sudo apt update
sudo apt install python3-pip -y
```

### 2. Install Dependencies

```
sudo pip install -r requirements.txt
```

### 3. Run the App

```
streamlit run ciscologanalyzer.py
```

Access at: http://localhost:8501

## 🐳 Docker Installation
Use this method to run the app in a fully isolated container.

### 1. Build the Image
```
sudo docker build -t cisco-log-app .
```

### 2. Run the Container
```
sudo docker run -d -p 8501:8501 --name cisco-analyzer cisco-log-app
```

### 3. Access the App
Open your browser and navigate to: http://localhost:8501

## 🛡️ Troubleshooting & Maintenance
Open Firewall Port
If you cannot access the dashboard from another machine, open port 8501:

```
sudo ufw allow 8501/tcp
```

### Manage Docker Container
To stop and delete the container:

```
sudo docker stop cisco-analyzer
sudo docker rm cisco-analyzer
```

### Check Docker Logs
If the app fails to start in Docker, check the logs:

```
sudo docker logs cisco-analyzer
```

### 📦 Requirements
streamlit
pandas
openpyxl
