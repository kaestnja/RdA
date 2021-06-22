$Volumes = Get-Volume | Where-Object { $_.DriveLetter -ne $null -and $_.DriveType -eq "fixed" }
$SpaceMonitorPath = "C:\programdata\SpaceMonitor"
$null = new-item $SpaceMonitorPath -ItemType Directory -Force
foreach ($Volume in $Volumes) {
    if ($Volume.DriveLetter -eq 0) { continue } #fix for server 2012 recovery volume
 
    $Date = (get-date).ToShortDateString()
    $time = (get-date).ToShortTimeString()
    $LastWriteTime = (get-item "C:\programdata\SpaceMonitor\$($volume.DriveLetter).txt" -ErrorAction SilentlyContinue).LastWriteTime
    #$Datapoints = get-content "$SpaceMonitorPath\$($volume.driveletter).txt" | convertfrom-csv -Delimiter ',' -Header "DriveLetter", "SizeUsed", "Date", "Time"
    if (Test-Path -Path “$SpaceMonitorPath\$($volume.driveletter).txt”){$Datapoints = get-content “$SpaceMonitorPath\$($volume.driveletter).txt” | convertfrom-csv -Delimiter ‘,’ -Header “DriveLetter”, “SizeUsed”, “Date”, “Time”}
    if ($LastWriteTime -lt (get-date).AddMinutes(-30)) { 
        write-host "writing datapoint"
        $SizeUsed = $Volume.Size - $volume.SizeRemaining
        Add-Content "$SpaceMonitorPath\$($volume.driveletter).txt" -value "$($volume.DriveLetter),$([math]::round($sizeused /1gb,2)),$Date,$Time" -Force
    }
    if ($datapoints.count -gt 15) {
        $DaysInDP = ($datapoints.Date | Select-Object -Unique).count
 
        $tempnsumxy = 0;
        $sample = 0;
        $sumx = 0;
        $sumy = 0;
        $xsquaredsum = 0;
        foreach ($datapoint in $datapoints) {
            $sumx = $sumx + $sample;
            $sumy = $sumy + $datapoint.SizeUsed;
            $tempnsumxy = $tempnsumxy + ($sample * $datapoint.SizeUsed);
 
            $xsquared = $sample * $sample;
            $xsquaredsum = $xsquaredsum + $xsquared
 
            $sample ++
        }
        $nsumxy = $Datapoints.count * $tempnsumxy;
        $sumxy = $sumx * $sumy;
        $nsumsquaredx = $Datapoints.count * $xsquaredsum;
        $sumxsquared = $sumx * $sumx;
        $slope = ($nsumxy - $sumxy) / ($nsumsquaredx - $sumxsquared);
$slopesumx = $slope * $sumx;
        $trend = ($sumy - $slopesumx) / $Datapoints.count;
        $daysleft = [int]((($volume.Size / 1gb - $trend) / $slope) - $DaysInDP);
        $estimatedFullDate = If ($daysleft -like "-*") { "Disk is gaining space. Cannot calculate date" } else { (get-date).AddDays($daysleft) }
        [PSCustomObject]@{
            Driveletter         = $volume.DriveLetter
            EstimatedFullInDays = $daysleft
            EstimatedFullDate   = $estimatedFullDate
        }
    }
}