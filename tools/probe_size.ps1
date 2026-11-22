param([string]$Root = 'D:\Deepseek Work\SudokuHelper 1.0')
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'edge-probe'
$url = 'file:///' + ((Join-Path $Root 'sudoku.html').Replace('\', '/').Replace(' ', '%20'))
$cases = @(
  @{ n = 'w390-dsf1'; w = 390; h = 900; dsf = 1 },
  @{ n = 'w390-dsf2'; w = 390; h = 900; dsf = 2 },
  @{ n = 'w430-dsf1'; w = 430; h = 900; dsf = 1 }
)
foreach ($c in $cases) {
  $args = @('--headless=new', '--disable-gpu', "--user-data-dir=$tmp\$($c.n)",
            "--window-size=$($c.w),$($c.h)", "--force-device-scale-factor=$($c.dsf)",
            '--virtual-time-budget=2500', '--dump-dom', $url)
  $dom = & $edge @args 2>$null
  $m = [regex]::Match(($dom -join "`n"), '<title>(.*?)</title>')
  Write-Output ("{0,-10} {1}" -f $c.n, $m.Groups[1].Value)
}
