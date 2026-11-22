#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compose the UI overview board (header + two screens + flow)."""
import base64
from pathlib import Path

from build_ui import ico

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ui"


def b64(name):
    return base64.b64encode((OUT / name).read_bytes()).decode()


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Microsoft YaHei UI","Microsoft YaHei","Segoe UI",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;color:#161B2E;background:#EEF1F8}
.ov{position:relative;overflow:hidden;width:1808px;height:1236px;
  background:radial-gradient(1200px 600px at 8% -6%,#E9E7FF 0%,rgba(233,231,255,0) 60%),
             radial-gradient(900px 500px at 96% 4%,#E3F0FF 0%,rgba(227,240,255,0) 55%),
             linear-gradient(180deg,#F7F8FC 0%,#F1F3F9 55%,#EDEFF7 100%)}
.grid-bg{position:absolute;inset:0;
  background-image:linear-gradient(rgba(99,102,241,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(99,102,241,.055) 1px,transparent 1px);
  background-size:48px 48px;
  -webkit-mask-image:radial-gradient(70% 55% at 50% 22%,#000 40%,transparent 100%)}
.head{position:relative;padding:36px 44px 0;display:flex;align-items:flex-start}
.logo{width:44px;height:44px;border-radius:13px;background:linear-gradient(140deg,#6366F1,#8B5CF6);
  display:grid;grid-template-columns:repeat(3,4px);grid-auto-rows:4px;grid-gap:3px;place-content:center;
  box-shadow:0 10px 22px -8px rgba(99,102,241,.75)}
.logo i{width:4px;height:4px;border-radius:1.5px;background:#fff;display:block}
.h1{font-size:26px;font-weight:700;letter-spacing:.6px;line-height:1.15}
.h1 span{font-size:12px;font-weight:600;color:#9AA1B4;letter-spacing:2.6px;margin-left:12px;
  vertical-align:5px;text-transform:uppercase}
.sub{font-size:12.5px;color:#6B7280;margin-top:7px;letter-spacing:.3px}
.badges{display:flex;gap:8px;margin-left:auto;padding-top:6px}
.badge{height:28px;padding:0 12px;border-radius:9px;background:rgba(255,255,255,.85);
  border:1px solid #E4E7F2;display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;
  color:#4B5265;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.badge i{width:6px;height:6px;border-radius:50%;background:#22C55E;display:block}
.badge.v i{background:#8B5CF6}

.frames{position:relative;display:flex;gap:28px;padding:26px 40px 0}
.col{display:flex;flex-direction:column;gap:10px}
.cap{display:flex;align-items:center;gap:9px;padding-left:2px}
.cap b{font-size:13.5px;font-weight:700;letter-spacing:.2px}
.cap span{font-size:10.5px;color:#8A93A6;font-weight:500}
.cap em{font-style:normal;width:18px;height:18px;border-radius:6px;background:#4F46E5;color:#fff;
  font-size:10px;font-weight:700;display:grid;place-items:center}
.frame{border-radius:16px;overflow:hidden;background:#fff;border:1px solid #DFE3EF;
  box-shadow:0 2px 4px rgba(16,24,40,.05),0 26px 60px -28px rgba(31,41,80,.45)}
.chrome{height:30px;background:#F5F6FA;border-bottom:1px solid #E9ECF4;display:flex;align-items:center;
  padding:0 12px;gap:5px}
.chrome i{width:8px;height:8px;border-radius:50%;display:block}
.chrome .u{margin-left:10px;height:17px;flex:1;max-width:210px;border-radius:5px;background:#fff;
  border:1px solid #E6E9F2;display:flex;align-items:center;padding:0 7px;
  font-size:8.5px;color:#9AA1B4;letter-spacing:.2px}
.frame img{display:block;width:100%;height:auto}

.flow{position:relative;margin:24px 40px 0;background:#fff;border:1px solid #E4E7F2;border-radius:18px;
  box-shadow:0 2px 4px rgba(16,24,40,.04),0 20px 44px -26px rgba(31,41,80,.35);
  padding:22px 24px;display:flex;align-items:center;gap:6px}
.step{display:flex;align-items:center;gap:11px;flex:1;min-width:0}
.step .n{width:34px;height:34px;border-radius:11px;flex:0 0 auto;display:grid;place-items:center;
  background:#EEF0FF;color:#4F46E5}
.step .n.a{background:linear-gradient(140deg,#6366F1,#8B5CF6);color:#fff;
  box-shadow:0 6px 14px -6px rgba(99,102,241,.9)}
.step .tx{min-width:0}
.step .t{font-size:12.5px;font-weight:700;letter-spacing:.2px;display:flex;align-items:center;gap:6px}
.step .d{font-size:10px;color:#8A93A6;margin-top:3px;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis}
.arw{flex:0 0 auto;color:#C9CFDD;display:grid;place-items:center;padding:0 2px}
.note{flex:0 0 auto;margin-left:10px;padding-left:18px;border-left:1px dashed #E2E6F1;
  font-size:10px;color:#7A8296;line-height:1.65;max-width:250px}
.note b{color:#4F46E5}
.foot{position:absolute;left:40px;right:40px;bottom:16px;display:flex;justify-content:space-between;
  font-size:10px;color:#98A0B3;letter-spacing:.2px}
"""


def main():
    solve = b64("solve.png")
    editor = b64("editor.png")

    def step(icon, title, desc, active=False):
        cls = "n a" if active else "n"
        return (f'<div class="step"><div class="{cls}">{ico(icon, 17)}</div>'
                f'<div class="tx"><div class="t">{title}</div><div class="d">{desc}</div></div></div>')

    arw = ('<div class="arw"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
           'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M5 12h13"/><path d="M12.5 6l6 6-6 6"/></svg></div>')

    flow = (step("pencil", "① 画区域", "勾选连通 9 格 · 每区 1–9 各一次", True) + arw +
            step("dots", "② 生成满解", "行 / 列 / 3×3 宫 / 异形区，四重约束") + arw +
            step("eraser", "③ 挖空成题", "保唯一解 · 按技巧链评难度") + arw +
            step("check", "④ 校验 · 分享", "实时查错 · 链接或图片直出"))

    html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="ov">
  <div class="grid-bg"></div>

  <div class="head">
    <div class="logo"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
    <div style="margin-left:15px">
      <div class="h1">数独工坊<span>Jigsaw Sudoku Studio</span></div>
      <div class="sub">异形数独创作与解题平台 · UI 概览 v0.1 · 纯静态可运行</div>
    </div>
    <div class="badges">
      <div class="badge"><i></i>零后端 MVP</div>
      <div class="badge v"><i></i>规则引擎优先</div>
      <div class="badge">AI 按需调用</div>
    </div>
  </div>

  <div class="frames">
    <div class="col" style="width:1140px">
      <div class="cap"><em>1</em><b>解题台</b><span>区域配色 · 冲突高亮 · 候选数 · AI 教练</span></div>
      <div class="frame" style="width:1140px">
        <div class="chrome"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i>
          <i style="background:#28C840"></i><div class="u">sudoku-studio.app/solve/jigsaw-07</div></div>
        <img src="data:image/png;base64,{solve}" alt="solve">
      </div>
    </div>
    <div class="col" style="width:560px">
      <div class="cap"><em>2</em><b>出题工作台</b><span>画区域 · 生成 · 挖空 · 校验</span></div>
      <div class="frame" style="width:560px">
        <div class="chrome"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i>
          <i style="background:#28C840"></i><div class="u">/create/jigsaw</div></div>
        <img src="data:image/png;base64,{editor}" alt="editor">
      </div>
    </div>
  </div>

  <div class="flow">
    {flow}
    <div class="note"><b>AI 只做两件事</b><br>拍照/截图识题，以及把求解器的推理步骤讲成人话。</div>
  </div>

  <div class="foot">
    <span>交互示意 · 非最终视觉稿</span>
    <span>棋盘数据由脚本生成：9 区连通、每区 1–9 各一次、唯一解已校验</span>
  </div>
</div></body></html>"""

    (OUT / "overview.html").write_text(html, encoding="utf-8")
    print("overview written")


if __name__ == "__main__":
    main()
