param(
  [string]$Root = 'D:\Deepseek Work\SudokuHelper 1.0',
  [string]$Pages = 'solve,editor',
  [string]$OutDir = 'ui',
  [string]$Prefix = ''
)
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'edge-ui'
$spec = @{
  'solve'  = @{ w = 1140; h = 840; html = 'screen_solve.html' }
  'editor' = @{ w = 560;  h = 840; html = 'screen_editor.html' }
  'overview' = @{ w = 1808; h = 1236; html = 'overview.html' }
}
foreach ($p in $Pages.Split(',')) {
  $p = $p.Trim()
  if (-not $spec.ContainsKey($p)) { Write-Output "unknown page $p"; continue }
  $s = $spec[$p]
  $out = Join-Path $Root (Join-Path $OutDir ($Prefix + $p + '.png'))
  $page = Join-Path $Root (Join-Path $OutDir $s.html)
  $url = 'file:///' + $page.Replace('\', '/').Replace(' ', '%20')
  & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --user-data-dir="$tmp\prof-$p" --screenshot="$out" `
    --window-size=$($s.w),$($s.h) $url 2>$null | Out-Null
  if (Test-Path $out) {
    $len = (Get-Item $out).Length
    Write-Output ("OK {0} {1} bytes" -f $out, $len)
  } else {
    Write-Output ("FAIL {0}" -f $out)
  }
}
