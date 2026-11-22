param(
  [string]$Root = 'D:\Deepseek Work\SudokuHelper 1.0',
  [string]$Page = 'sudoku.html'
)
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'edge-app'
$url = 'file:///' + ((Join-Path $Root $Page).Replace('\', '/').Replace(' ', '%20'))
$jobs = @(
  @{ name = 'app-desktop'; w = 1180; h = 980 },
  @{ name = 'app-mobile';  w = 390;  h = 900 }
)
foreach ($j in $jobs) {
  $out = Join-Path $Root ('ui\' + $j.name + '.png')
  & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 `
    --user-data-dir="$tmp\p-$($j.name)" --screenshot="$out" `
    --window-size=$($j.w),$($j.h) --virtual-time-budget=3000 $url 2>$null | Out-Null
  if (Test-Path $out) { Write-Output ("OK  {0} {1} bytes" -f $j.name, (Get-Item $out).Length) }
  else { Write-Output ("FAIL {0}" -f $j.name) }
}
$dom = Join-Path $Root 'ui\app-dom.html'
& $edge --headless=new --disable-gpu --user-data-dir="$tmp\p-dom" --virtual-time-budget=3000 `
  --dump-dom $url 2>$null | Out-File -FilePath $dom -Encoding utf8
if (Test-Path $dom) {
  $t = Get-Content $dom -Raw
  Write-Output ("DOM bytes {0}; rects {1}; has error banner: {2}" -f $t.Length, ([regex]::Matches($t, '<rect')).Count, ($t -match '运行出错'))
}
