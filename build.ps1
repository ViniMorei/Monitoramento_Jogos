$exclude = @("venv", "Monitoramento_Jogos.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "Monitoramento_Jogos.zip" -Force