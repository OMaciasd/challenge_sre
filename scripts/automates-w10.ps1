$VerbosePreference = "Continue"

$apps = @("App1", "App2", "App3")

foreach ($app in $apps) {
    Try {
        Write-Host "Installing $app..."
        Start-Process "msiexec.exe" -ArgumentList "/i $app.msi /quiet /norestart" -Wait -ErrorAction Stop -Verbose
        Write-Host "$app has been installed successfully."
    }
    Catch {
        Write-Host "Error installing $app: $($_.Exception.Message)"
    }
}
