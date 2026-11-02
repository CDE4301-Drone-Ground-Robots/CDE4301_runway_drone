param([Parameter(Mandatory=$true)][string]$Workbook)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
$file = [IO.File]::Open($Workbook, 'Open', 'Read', 'ReadWrite')
$zip = [IO.Compression.ZipArchive]::new($file)
function Read-Xml($path) {
  $reader = [IO.StreamReader]::new($zip.GetEntry($path).Open())
  try { [xml]$reader.ReadToEnd() } finally { $reader.Dispose() }
}
try {
  $strings = Read-Xml 'xl/sharedStrings.xml'
  $shared = @($strings.sst.si | ForEach-Object { $_.InnerText })
  $sheet = Read-Xml 'xl/worksheets/sheet2.xml'
  $cells = @($sheet.worksheet.sheetData.row | ForEach-Object {
    foreach ($c in $_.c) {
      $value = [string]$c.v
      if ($c.t -eq 's') { $value = $shared[[int]$value] }
      if ($c.t -eq 'inlineStr') { $value = $c.is.InnerText }
      [ordered]@{ ref = [string]$c.r; style = [string]$c.s; value = $value }
    }
  })
  $relevant = @($cells | Where-Object { $row = [int]($_.ref -replace '[A-Z]', ''); $row -eq 5 -or ($row -ge 32 -and $row -le 73) })
  [ordered]@{ cells = $relevant; merges = @($sheet.worksheet.mergeCells.mergeCell | ForEach-Object { [string]$_.ref }) } | ConvertTo-Json -Depth 8
} finally { $zip.Dispose(); $file.Dispose() }
