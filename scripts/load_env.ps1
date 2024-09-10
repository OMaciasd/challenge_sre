$envFilePath = ".\.env"

if (Test-Path $envFilePath) {
    $lines = Get-Content $envFilePath

    $variables = @{}

    foreach ($line in $lines) {
        if ($line -notmatch '^\s*#' -and $line -match '^[^=\s]+=[^=\s]+') {
            $key, $value = $line -split '=', 2
            $key = $key.Trim()
            $value = $value.Trim()

            $variables[$key] = $value
        }
    }

    foreach ($key in $variables.Keys) {
        $value = $variables[$key]

        foreach ($var in $variables.Keys) {
            $value = $value -replace "\$\{$var\}", $variables[$var]
        }

        [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::User)

        Write-Host "$key = $value"
    }
} else {
    Write-Host "The .env file is not found in the directory."
}
