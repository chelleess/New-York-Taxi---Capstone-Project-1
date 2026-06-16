$log = "logs/pipeline.log"

function LogMessage($message) {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$time - $message" | Tee-Object -FilePath $log -Append
}

LogMessage "Starting pipeline"

python src\extract.py | Out-Null
LogMessage "Extract completed"

python src\transform.py | Out-Null
LogMessage "Transform completed"

python data\mart\load.py | Out-Null
LogMessage "Load completed"

python scripts\quality_check.py | Out-Null
LogMessage "Data quality check completed"