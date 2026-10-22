Set-Location -LiteralPath $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -m streamlit run main.py --server.address 127.0.0.1 --browser.gatherUsageStats false
