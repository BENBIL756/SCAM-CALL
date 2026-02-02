# Start the server detached (runs start_server.py)
$python = "C:/Users/benbi/OneDrive/Documents/hackathon/.venv/Scripts/python.exe"
$workDir = "C:\Users\benbi\OneDrive\Documents\hackathon"
Start-Process -FilePath $python -ArgumentList "start_server.py" -WorkingDirectory $workDir -NoNewWindow -WindowStyle Hidden
Write-Host "Server start requested (detached)."