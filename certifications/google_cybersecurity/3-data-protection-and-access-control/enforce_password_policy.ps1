# enforce_password_policy.ps1
# Description: Enforces strong password settings on a local system

Import-Module SecurityPolicyDSC

$Params = @{
    PolicySettings = @{
        "MinimumPasswordLength" = 12
        "PasswordComplexity" = 1
        "MaximumPasswordAge" = 30
        "MinimumPasswordAge" = 1
        "EnforcePasswordHistory" = 24
    }
}

Set-SecurityPolicy @Params
