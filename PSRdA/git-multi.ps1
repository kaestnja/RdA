#cd $($(Get-Item "Env:USERPROFILE").Value + "\source\repos") 
#if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\source\repos")) { Get-ChildItem -Directory | foreach { Write-Host "Getting latest for $_ " | git -C $_.FullName pull --all --recurse-submodules --verbose } }
#if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\source\repos")) { cd $($(Get-Item "Env:USERPROFILE").Value + "\source\repos"); Get-ChildItem -Directory -Recurse | foreach { Write-Host "Getting latest for $_ " | git -C $_.FullName pull --all --recurse-submodules --verbose } }
#if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\source\repos")) { Get-ChildItem -Path $($(Get-Item "Env:USERPROFILE").Value + "\source\repos") -Recurse | foreach { Write-Host "Getting latest for $_ " | git -C $_.FullName pull --all --recurse-submodules --verbose } }
#Get-ChildItem -Directory | foreach { Write-Host "Getting latest for $_ " | git -C $_.FullName pull --all --recurse-submodules --verbose }

#cd $($(Get-Item "Env:USERPROFILE").Value + "\source\repos\github.com\kaestnja\RdA\PSRdA") 
#usage:  .\git-multi.ps1 -cmd "pull"
#usage:  .\git-multi.ps1 -baseDir $($(Get-Item "Env:USERPROFILE").Value + "\source\repos") -cmd "pull"
#usage:  .\git-multi.ps1 -baseDir $($(Get-Item "Env:USERPROFILE").Value + "\source\repos") -depth 6 -cmd "pull"
#start it via: Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/git-multi.ps1') } -baseDir $($(Get-Item "Env:USERPROFILE").Value + "\source\repos") -depth 6 -cmd 'pull'"

param (

    # The root directory to perform the pull in
    $baseDir = ".",

    # How deep down you want to look for .git folders
    $depth = 2,

    # The command you want to perform
    $cmd = "status"
)

$gitFolderName = ".git"

function Go () {

    # Finds all .git folders by given path, the -match "h" parameter is for hidden folders 
    $gitFolders = Get-ChildItem -Path $baseDir -Depth $depth -Recurse -Force | Where-Object { $_.Mode -match "h" -and $_.FullName -like "*\$gitFolderName" }
    #echo $gitFolders
    ForEach ($gitFolder in $gitFolders) {

        #If ($gitFolder[-4] -match '.git' ){
        # Remove the ".git" folder from the path 
        #$folder = $gitFolder.FullName -replace $gitFolderName, ""
        $folder = $gitFolder.FullName -replace ".{4}$"

        Write-Host "Performing git $cmd in folder: '$folder'..." -foregroundColor "green"

        # Go into the folder
        Push-Location $folder 

        # Perform the command within the folder
        & git $cmd

        # Go back to the original folder
        Pop-Location
        #    }
    }
}

function Main () {  
    echo $baseDir
    Go   
}

# Executes the main function
Main