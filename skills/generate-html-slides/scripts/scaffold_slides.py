#!/usr/bin/env python3
"""Create a single-file HTML slide deck scaffold using TailwindCSS."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


THEME_CONFIG = """{
  theme: {
    extend: {
      colors: {
        deck: {
          bg: '#0b0d10',
          panel: '#111318',
          text: '#f3f4f6',
          muted: '#a1a1aa',
          accent: '#3ecf8e',
          accentHover: '#2fb67b',
          border: '#22262e'
        }
      },
      boxShadow: {
        deck: '0 24px 60px rgba(0,0,0,.35)'
      }
    }
  }
}"""


def parse_slide(raw: str) -> tuple[str, list[str]]:
    if "|" not in raw:
        raise ValueError("Slide must use 'Title|line1\\nline2' format")
    title, body = raw.split("|", 1)
    lines = [line.strip() for line in body.split("\\n") if line.strip()]
    return title.strip(), lines


def render_inline_svg(seed: int) -> str:
    offset = 20 + (seed % 4) * 12
    return f"""
      <svg viewBox=\"0 0 640 280\" role=\"img\" aria-label=\"示意图\" class=\"w-full max-w-[760px] rounded-2xl border border-deck-border bg-black/30\">
        <defs>
          <linearGradient id=\"g{seed}\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">
            <stop offset=\"0%\" stop-color=\"#3ecf8e\"/>
            <stop offset=\"100%\" stop-color=\"#2fb67b\"/>
          </linearGradient>
        </defs>
        <rect x=\"0\" y=\"0\" width=\"640\" height=\"280\" fill=\"#0b0d10\"/>
        <path d=\"M0 238 C120 {170 + offset}, 220 {210 - offset}, 320 180 C420 150, 520 205, 640 120\" fill=\"none\" stroke=\"url(#g{seed})\" stroke-width=\"7\"/>
        <circle cx=\"120\" cy=\"{172 + offset}\" r=\"6\" fill=\"#3ecf8e\"/>
        <circle cx=\"320\" cy=\"180\" r=\"6\" fill=\"#3ecf8e\"/>
        <circle cx=\"520\" cy=\"205\" r=\"6\" fill=\"#3ecf8e\"/>
        <text x=\"26\" y=\"38\" fill=\"#a1a1aa\" font-size=\"18\">Inline SVG Visual</text>
      </svg>
""".strip()


def render_slide(index: int, title: str, lines: list[str]) -> str:
    escaped_title = html.escape(title)
    if not lines:
        body = '<p class="text-2xl text-deck-muted">TODO: 补充内容</p>'
    elif len(lines) == 1:
        body = f'<p class="text-3xl leading-relaxed text-deck-text">{html.escape(lines[0])}</p>'
    else:
        items = "".join(
            f'<li class="text-2xl leading-relaxed text-deck-text">{html.escape(line)}</li>'
            for line in lines
        )
        body = f'<ul class="space-y-3 pl-8 list-disc marker:text-deck-accent">{items}</ul>'

    return f"""
    <section class=\"slide hidden h-full w-full flex-col justify-between p-12 md:p-16\" data-slide>
      <div class=\"space-y-7\">
        <h2 class=\"text-5xl md:text-6xl font-semibold tracking-tight text-balance text-deck-text\">{escaped_title}</h2>
        {body}
      </div>
      <div class=\"pt-6\">{render_inline_svg(index)}</div>
      <aside class=\"notes hidden\">TODO: 讲者备注</aside>
    </section>
""".rstrip()


def build_document(deck_title: str, slide_blocks: list[str]) -> str:
    safe_title = html.escape(deck_title)
    slides_html = "\\n".join(slide_blocks)
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{safe_title}</title>
  <script src=\"https://cdn.tailwindcss.com\"></script>
  <script>
    tailwind.config = {THEME_CONFIG};
  </script>
  <style>
    .text-balance {{ text-wrap: balance; }}
  </style>
</head>
<body class=\"m-0 min-h-screen bg-deck-bg text-deck-text antialiased\">
  <main class=\"mx-auto grid min-h-screen w-full place-items-center p-3 md:p-6\">
    <section class=\"relative h-[calc(100vh-2rem)] max-h-[920px] w-full max-w-[1600px] overflow-hidden rounded-2xl border border-deck-border bg-gradient-to-b from-[#10131a] to-[#0b0d10] shadow-deck\">
      <section class=\"slide h-full w-full flex-col justify-between p-12 md:p-16\" data-slide>
        <div class=\"space-y-8\">
          <p class=\"inline-flex rounded-full border border-deck-border bg-white/5 px-4 py-1 text-sm font-medium tracking-wide text-deck-muted\">Single HTML + TailwindCSS</p>
          <h1 class=\"max-w-5xl text-6xl md:text-7xl lg:text-8xl font-semibold leading-[1.05] tracking-tight text-balance\">
            {safe_title}<br/><span class=\"text-deck-accent\">投屏清晰，可直接演示</span>
          </h1>
          <p class=\"max-w-4xl text-2xl md:text-3xl leading-relaxed text-deck-muted\">默认使用大字号、深色高对比主题和内联 SVG 图形，适配课堂与会议投屏。</p>
        </div>
        <div class=\"grid gap-8\">
          <svg viewBox=\"0 0 820 220\" role=\"img\" aria-label=\"封面示意图\" class=\"w-full max-w-[980px] rounded-2xl border border-deck-border bg-black/30\">
            <defs>
              <linearGradient id=\"coverGradient\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">
                <stop offset=\"0%\" stop-color=\"#3ecf8e\"/>
                <stop offset=\"100%\" stop-color=\"#2fb67b\"/>
              </linearGradient>
            </defs>
            <rect width=\"820\" height=\"220\" fill=\"#0b0d10\"/>
            <path d=\"M40 166 L200 106 L360 140 L520 80 L780 132\" stroke=\"url(#coverGradient)\" stroke-width=\"8\" fill=\"none\"/>
            <circle cx=\"200\" cy=\"106\" r=\"7\" fill=\"#3ecf8e\"/>
            <circle cx=\"360\" cy=\"140\" r=\"7\" fill=\"#3ecf8e\"/>
            <circle cx=\"520\" cy=\"80\" r=\"7\" fill=\"#3ecf8e\"/>
            <text x=\"36\" y=\"42\" fill=\"#a1a1aa\" font-size=\"20\">Inline SVG Visual</text>
          </svg>
          <aside class=\"notes hidden\">开场：先给目标，再讲结构。</aside>
        </div>
      </section>
{slides_html}
      <output id=\"pager\" class=\"absolute bottom-4 right-4 rounded-full border border-deck-border bg-black/40 px-4 py-2 text-base text-deck-muted\" aria-live=\"polite\">1 / 1</output>
    </section>
  </main>

  <script>
    (() => {{
      const slides = [...document.querySelectorAll('[data-slide]')];
      const pager = document.getElementById('pager');
      let index = 0;

      function render() {{
        slides.forEach((slide, i) => {{
          slide.classList.toggle('hidden', i !== index);
          slide.classList.toggle('flex', i === index);
        }});
        pager.textContent = `${{index + 1}} / ${{slides.length}}`;
      }}

      function go(next) {{
        index = Math.max(0, Math.min(slides.length - 1, next));
        render();
      }}

      document.addEventListener('keydown', (event) => {{
        const key = event.key;
        if (key === 'ArrowRight' || key === 'PageDown') go(index + 1);
        else if (key === 'ArrowLeft' || key === 'PageUp') go(index - 1);
        else if (key === 'Home') go(0);
        else if (key === 'End') go(slides.length - 1);
      }});

      render();
    }})();
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a single-file HTML slide deck")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", required=True, help="Deck title")
    parser.add_argument(
        "--slide",
        action="append",
        default=[],
        metavar="TITLE|LINE1\\nLINE2",
        help="Slide content definition. Repeat for multiple slides.",
    )

    args = parser.parse_args()

    slide_blocks = []
    for i, raw_slide in enumerate(args.slide, start=1):
        title, lines = parse_slide(raw_slide)
        slide_blocks.append(render_slide(i, title, lines))

    if not slide_blocks:
        slide_blocks = [
            render_slide(
                1,
                "任务定义",
                ["目标：预测未来 30 天流失用户", "业务收益：提升留存与营销投放效率", "核心指标：AUC、Recall@TopK"],
            ),
            render_slide(
                2,
                "数据与特征",
                ["样本规模：120 万用户记录", "特征：活跃度、支付行为、客服交互", "风险：类别不平衡与时间泄漏"],
            ),
            render_slide(
                3,
                "模型评估与迭代",
                ["基线 LR：AUC 0.73", "当前 XGBoost：AUC 0.81", "下一步：阈值优化 + 线上 A/B 验证"],
            ),
        ]

    doc = build_document(args.title, slide_blocks)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
