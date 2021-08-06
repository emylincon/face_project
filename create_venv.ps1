Write-Output "creating python Vscode environment"
python -m venv venv
.\venv\Scripts\activate
pip freeze > requirements.txt
Write-Output "Environment created"
Write-Output "Add python.pythonPath: 'C:~\\venv\\Scripts\\python' to VScode settings"
Write-Output "# README " >> README.md