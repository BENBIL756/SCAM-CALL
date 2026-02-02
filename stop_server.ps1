# Stop server listening on port 9000 (safe stop)
$port = 9000
try {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        $pid = $conn.OwningProcess
        if ($pid) {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process listening on port $port (PID: $pid)."
        } else {
            Write-Host "No owning process found for port $port."
        }
    } else {
        Write-Host "No process is listening on port $port."
    }
} catch {
    Write-Host "Failed to stop server: $_"
}