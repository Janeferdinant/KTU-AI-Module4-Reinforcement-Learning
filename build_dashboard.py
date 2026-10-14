import os

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KTU S5 AI Module 4: Reinforcement Learning Master Knowledge System</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- KaTeX for math typesetting -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

  <!-- Chart.js for live metrics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    /* -------------------------------------------------------------
       LIQUID GLASS DESIGN SYSTEM & CSS VARIABLES
       ------------------------------------------------------------- */
    :root {
      --bg-base: #060813;
      --bg-surface: rgba(15, 23, 42, 0.65);
      --bg-surface-elevated: rgba(30, 41, 59, 0.55);
      --bg-glass-card: rgba(18, 24, 40, 0.68);
      --bg-glass-card-hover: rgba(26, 35, 58, 0.82);
      
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-border-bright: rgba(255, 255, 255, 0.28);
      --glass-border-glow: rgba(56, 189, 248, 0.4);
      
      --accent-cyan: #38bdf8;
      --accent-cyan-glow: rgba(56, 189, 248, 0.25);
      --accent-violet: #a855f7;
      --accent-violet-glow: rgba(168, 85, 247, 0.25);
      --accent-emerald: #10b981;
      --accent-emerald-glow: rgba(16, 185, 129, 0.25);
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --font-heading: 'Space Grotesk', -apple-system, sans-serif;
      --font-body: 'DM Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      
      --glass-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.6), inset 0 1px 1px 0 rgba(255, 255, 255, 0.15);
      --glass-shadow-active: 0 24px 50px -10px rgba(56, 189, 248, 0.2), inset 0 1px 2px 0 rgba(255, 255, 255, 0.25);
      --glass-blur: blur(24px) saturate(190%);
      --radius-lg: 20px;
      --radius-md: 14px;
      --radius-sm: 8px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-body);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      position: relative;
    }

    /* Ambient animated background canvas */
    #ambient-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 0;
      pointer-events: none;
    }

    /* App container */
    .app-wrapper {
      position: relative;
      z-index: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 32px 60px;
    }

    /* Liquid Glass Common Class */
    .liquid-glass {
      background: var(--bg-glass-card);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow);
      border-radius: var(--radius-lg);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .liquid-glass:hover {
      border-color: var(--glass-border-bright);
    }

    /* -------------------------------------------------------------
       HEADER & NAVIGATION
       ------------------------------------------------------------- */
    header.main-header {
      padding: 20px 28px;
      margin-bottom: 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .header-brand {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand-icon-box {
      width: 50px;
      height: 50px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(168, 85, 247, 0.3));
      border: 1px solid rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.3);
    }

    .brand-icon-box svg {
      width: 28px;
      height: 28px;
      color: var(--accent-cyan);
    }

    .brand-title h1 {
      font-family: var(--font-heading);
      font-size: 1.45rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
      font-size: 0.85rem;
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 500;
    }

    .badge-pill {
      font-size: 0.72rem;
      padding: 3px 10px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--accent-cyan);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .badge-pill.violet {
      background: rgba(168, 85, 247, 0.15);
      border-color: rgba(168, 85, 247, 0.35);
      color: #c084fc;
    }

    .badge-pill.emerald {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.35);
      color: #34d399;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .glass-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: var(--radius-md);
      font-family: var(--font-heading);
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--glass-border);
      cursor: pointer;
      backdrop-filter: blur(16px);
      transition: all 0.25s ease;
      text-decoration: none;
    }

    .glass-btn:hover {
      background: rgba(255, 255, 255, 0.14);
      border-color: var(--glass-border-bright);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }

    .glass-btn.primary {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.35), rgba(168, 85, 247, 0.35));
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
    }

    .glass-btn.primary:hover {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.55), rgba(168, 85, 247, 0.55));
      border-color: var(--accent-cyan);
      box-shadow: 0 0 28px rgba(56, 189, 248, 0.45);
    }

    /* -------------------------------------------------------------
       TAB NAVIGATION BAR
       ------------------------------------------------------------- */
    .tabs-nav-bar {
      padding: 8px;
      margin-bottom: 28px;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
    }

    .tabs-nav-bar::-webkit-scrollbar {
      display: none;
    }

    .tab-btn {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 22px;
      border-radius: var(--radius-md);
      font-family: var(--font-heading);
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: 1px solid transparent;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.25s ease;
    }

    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .tab-btn.active {
      color: #ffffff;
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.3);
      box-shadow: inset 0 0 16px rgba(56, 189, 248, 0.15), 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .tab-btn svg {
      width: 18px;
      height: 18px;
      opacity: 0.8;
    }

    .tab-btn.active svg {
      opacity: 1;
      color: var(--accent-cyan);
    }

    /* -------------------------------------------------------------
       TAB CONTENT PANELS
       ------------------------------------------------------------- */
    .tab-pane {
      display: none;
      animation: fadeIn 0.4s ease forwards;
    }

    .tab-pane.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* -------------------------------------------------------------
       SECTION STYLES & GRIDS
       ------------------------------------------------------------- */
    .section-title-bar {
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 12px;
    }

    .section-title-bar h2 {
      font-family: var(--font-heading);
      font-size: 1.8rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #ffffff;
    }

    .section-title-bar p {
      color: var(--text-muted);
      font-size: 0.95rem;
      max-width: 720px;
      margin-top: 4px;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    .grid-1-2 {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 24px;
    }

    @media (max-width: 1024px) {
      .grid-2, .grid-3, .grid-1-2 {
        grid-template-columns: 1fr;
      }
    }

    /* Card styling */
    .glass-card {
      padding: 26px;
      border-radius: var(--radius-lg);
      background: var(--bg-glass-card);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow);
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }

    .glass-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    }

    .card-header-flex {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }

    .card-header-flex h3 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .card-header-flex h3 svg {
      width: 20px;
      height: 20px;
      color: var(--accent-cyan);
    }

    /* Callout & Math boxes */
    .math-formula-box {
      background: rgba(10, 15, 29, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin: 16px 0;
      overflow-x: auto;
      text-align: center;
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.4);
    }

    .callout-box {
      border-left: 3px solid var(--accent-cyan);
      background: rgba(56, 189, 248, 0.08);
      padding: 14px 18px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      margin: 14px 0;
      font-size: 0.92rem;
      color: #e2e8f0;
    }

    .callout-box.violet {
      border-left-color: var(--accent-violet);
      background: rgba(168, 85, 247, 0.08);
    }

    .callout-box.emerald {
      border-left-color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.08);
    }

    .callout-box.amber {
      border-left-color: var(--accent-amber);
      background: rgba(245, 158, 11, 0.08);
    }

    /* Comparison Tables */
    .glass-table-wrapper {
      overflow-x: auto;
      margin: 16px 0;
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
    }

    table.glass-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }

    table.glass-table th {
      background: rgba(30, 41, 59, 0.75);
      color: #ffffff;
      font-family: var(--font-heading);
      padding: 14px 16px;
      font-weight: 600;
      border-bottom: 1px solid var(--glass-border-bright);
    }

    table.glass-table td {
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      color: #cbd5e1;
    }

    table.glass-table tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }

    /* Interactive Simulation Canvas Areas */
    .sim-canvas-container {
      background: #030712;
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      position: relative;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.8);
      margin: 16px 0;
    }

    .sim-canvas-container canvas {
      display: block;
      max-width: 100%;
    }

    .controls-strip {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      padding: 12px 16px;
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      margin-top: 14px;
    }

    .ctrl-group {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.84rem;
      color: var(--text-muted);
    }

    .ctrl-group label {
      font-weight: 500;
    }

    .ctrl-slider {
      -webkit-appearance: none;
      height: 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.15);
      outline: none;
      transition: background 0.2s;
    }

    .ctrl-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--accent-cyan);
      cursor: pointer;
      box-shadow: 0 0 10px var(--accent-cyan);
    }

    .stat-badge {
      font-family: var(--font-mono);
      font-size: 0.82rem;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--accent-cyan);
    }

    /* Research Paper Cards */
    .paper-card {
      border: 1px solid var(--glass-border);
      background: rgba(20, 27, 45, 0.6);
      border-radius: var(--radius-lg);
      padding: 24px;
      transition: all 0.3s ease;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .paper-card:hover {
      border-color: rgba(56, 189, 248, 0.45);
      transform: translateY(-4px);
      box-shadow: 0 16px 36px -10px rgba(56, 189, 248, 0.15);
    }

    .paper-rank-tag {
      position: absolute;
      top: 18px;
      right: 18px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
      color: #ffffff;
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    .paper-venue {
      font-size: 0.78rem;
      color: var(--accent-cyan);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }

    .paper-title {
      font-family: var(--font-heading);
      font-size: 1.18rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.35;
      margin-bottom: 8px;
    }

    .paper-authors {
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-bottom: 12px;
    }

    .paper-desc {
      font-size: 0.88rem;
      color: #cbd5e1;
      margin-bottom: 16px;
      line-height: 1.5;
    }

    .paper-innovations {
      list-style: none;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .paper-innovations li {
      font-size: 0.82rem;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .paper-innovations li::before {
      content: '✦';
      color: var(--accent-violet);
    }

    /* Solvers & Input Forms */
    .solver-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin: 16px 0;
    }

    .form-field {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .form-field label {
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .form-input {
      background: rgba(10, 15, 29, 0.75);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      font-family: var(--font-mono);
      font-size: 0.95rem;
      color: #ffffff;
      outline: none;
      transition: all 0.2s;
    }

    .form-input:focus {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }

    .calc-result-box {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(16, 185, 129, 0.35);
      border-radius: var(--radius-md);
      padding: 18px;
      margin-top: 18px;
      display: none;
      animation: fadeIn 0.3s ease;
    }

    .calc-result-box.active {
      display: block;
    }

    /* Code Snippets & Deployment Blocks */
    .code-block-wrapper {
      background: #050814;
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      overflow: hidden;
      margin: 16px 0;
    }

    .code-header {
      background: rgba(30, 41, 59, 0.5);
      padding: 8px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--glass-border);
    }

    .code-filename {
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .copy-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 0.75rem;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.2s;
    }

    .copy-btn:hover {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }

    pre.code-content {
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: #e2e8f0;
      overflow-x: auto;
      line-height: 1.5;
    }

    /* Interactive Terminal Simulator */
    .terminal-window {
      background: #02040a;
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7);
    }

    .terminal-bar {
      background: #0f172a;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .t-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }

    .t-red { background: #ef4444; }
    .t-yellow { background: #f59e0b; }
    .t-green { background: #10b981; }

    .terminal-body {
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      min-height: 220px;
      max-height: 350px;
      overflow-y: auto;
      color: #38bdf8;
    }

    .t-prompt {
      color: #34d399;
    }

    .t-cmd {
      color: #f8fafc;
      font-weight: 600;
    }

    /* -------------------------------------------------------------
       SIGNATURE JANE ROSE FOOTER
       ------------------------------------------------------------- */
    footer.jane-rose-footer {
      margin-top: 48px;
      padding: 32px 36px;
      border-radius: var(--radius-lg);
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.75), rgba(30, 41, 59, 0.6));
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.7), inset 0 1px 2px rgba(255, 255, 255, 0.2);
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .footer-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 20px;
    }

    .footer-brand h4 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 700;
      background: linear-gradient(135deg, #ffffff, #38bdf8, #c084fc);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .footer-brand p {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .author-signature-pill {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 10px 20px;
      border-radius: 9999px;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(168, 85, 247, 0.2));
      border: 1px solid rgba(56, 189, 248, 0.35);
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }

    .signature-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: linear-gradient(135deg, #38bdf8, #a855f7);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-heading);
      font-weight: 700;
      color: #ffffff;
      font-size: 0.85rem;
    }

    .signature-text {
      display: flex;
      flex-direction: column;
    }

    .signature-title {
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .signature-name {
      font-family: var(--font-heading);
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: 0.02em;
    }

    .footer-bottom {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.82rem;
      color: var(--text-dim);
    }

    .footer-links {
      display: flex;
      gap: 20px;
    }

    .footer-links a {
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.2s;
    }

    .footer-links a:hover {
      color: var(--accent-cyan);
    }
  </style>
</head>
<body>

  <!-- Ambient background glow canvas -->
  <canvas id="ambient-canvas"></canvas>

  <div class="app-wrapper">

    <!-- -----------------------------------------------------------
         MAIN HEADER (LIQUID GLASS)
         ----------------------------------------------------------- -->
    <header class="main-header liquid-glass">
      <div class="header-brand">
        <div class="brand-icon-box">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
          </svg>
        </div>
        <div class="brand-title">
          <h1>KTU S5 AI Module 4: Reinforcement Learning</h1>
          <div class="brand-subtitle">
            <span>Autonomous Intelligence & Sequential Decision Making</span>
            <span class="badge-pill">Syllabus Master</span>
            <span class="badge-pill violet">Liquid Glass Engine</span>
          </div>
        </div>
      </div>

      <div class="header-actions">
        <button class="glass-btn" onclick="switchTab('tab-solver')">
          <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 15.75V18m-7.5-6.75h.008v.008H8.25m0 3h.008v.008H8.25m3-3h.008v.008H11.25m0 3h.008v.008H11.25m3-6h.008v.008H14.25m0 3h.008v.008H14.25M6.75 6.75h10.5a2.25 2.25 0 012.25 2.25v10.5a2.25 2.25 0 01-2.25 2.25H6.75a2.25 2.25 0 01-2.25-2.25V9a2.25 2.25 0 012.25-2.25z" />
          </svg>
          Exam Solver
        </button>
        <button class="glass-btn primary" onclick="switchTab('tab-demos')">
          <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347a1.125 1.125 0 01-1.667-.985V5.653z" />
          </svg>
          Live Demos
        </button>
      </div>
    </header>

    <!-- -----------------------------------------------------------
         TOP TABS NAVIGATION
         ----------------------------------------------------------- -->
    <nav class="tabs-nav-bar liquid-glass">
      <button class="tab-btn active" onclick="switchTab('tab-theory')" id="btn-tab-theory">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
        1. Syllabus & Theory (Solve It)
      </button>

      <button class="tab-btn" onclick="switchTab('tab-demos')" id="btn-tab-demos">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
        </svg>
        2. Top 5 Papers & Live Demos
      </button>

      <button class="tab-btn" onclick="switchTab('tab-apps')" id="btn-tab-apps">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" />
        </svg>
        3. Real-World Applications
      </button>

      <button class="tab-btn" onclick="switchTab('tab-solver')" id="btn-tab-solver">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        4. Exam Problem Solver
      </button>

      <button class="tab-btn" onclick="switchTab('tab-deploy')" id="btn-tab-deploy">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25z" />
        </svg>
        5. Local Deployment Guide
      </button>
    </nav>

    <!-- ===========================================================
         TAB 1: SYLLABUS & COMPLETE THEORY ("SOLVE IT")
         =========================================================== -->
    <div class="tab-pane active" id="tab-theory">
      <div class="section-title-bar">
        <div>
          <h2>Module 4: Reinforcement Learning Complete Theoretical Solution</h2>
          <p>Comprehensive curriculum notes, mathematical derivations, Bellman formulations, and rigorous comparisons covering KTU S5 Artificial Intelligence.</p>
        </div>
        <span class="badge-pill emerald">Full Syllabus Solved</span>
      </div>

      <!-- Unit 1: Foundations & MDP -->
      <div class="glass-card">
        <div class="card-header-flex">
          <h3>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" /></svg>
            1. Reinforcement Learning Foundations & Markov Decision Process (MDP)
          </h3>
          <span class="badge-pill">Section 1.1 - 1.5</span>
        </div>
        
        <p><strong>Reinforcement Learning (RL)</strong> is an area of machine learning where an autonomous <em>agent</em> learns optimal decision-making policies through trial-and-error interactions with an uncertain dynamic <em>environment</em>, guided exclusively by evaluative scalar feedback signals called <em>rewards</em> or <em>penalties</em>.</p>
        
        <div class="grid-2" style="margin-top: 14px;">
          <div>
            <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">Core Terminology</h4>
            <ul style="padding-left: 20px; color: #cbd5e1; font-size: 0.9rem; line-height: 1.8;">
              <li><strong>Agent:</strong> The decision-making learner selecting actions based on state observations.</li>
              <li><strong>Environment:</strong> The external dynamic world interacting with and responding to the agent.</li>
              <li><strong>State ($s \in S$):</strong> Complete representation of the current configuration of the environment.</li>
              <li><strong>Action ($a \in A$):</strong> Feasible choice/control signal executed by the agent.</li>
              <li><strong>Reward ($r \in \mathbb{R}$):</strong> Scalar feedback measuring the immediate desirability of a transition.</li>
              <li><strong>Policy ($\pi(a|s)$):</strong> The probabilistic or deterministic strategy mapping states to actions.</li>
              <li><strong>Value Function ($V(s)$ / $Q(s,a)$):</strong> The expected cumulative discounted future reward.</li>
            </ul>
          </div>
          <div>
            <h4 style="color: var(--accent-violet); margin-bottom: 8px;">The Markov Property & MDP 5-Tuple</h4>
            <p style="font-size: 0.88rem; color: #cbd5e1;">An MDP is formally defined by the tuple $\mathcal{M} = \langle S, A, T, R, \gamma \rangle$:</p>
            <div class="callout-box violet" style="font-size: 0.84rem;">
              <strong>Markov Property:</strong> The future state is conditionally independent of past history given the current state and action:
              $$P(S_{t+1}=s' \mid S_t=s, A_t=a, S_{t-1}, A_{t-1}, \dots) = P(S_{t+1}=s' \mid S_t=s, A_t=a)$$
            </div>
            <div class="math-formula-box">
              $$\text{Discounted Cumulative Return: } G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots$$
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted);">Where $\gamma \in [0, 1)$ is the <em>discount factor</em>. When $\gamma \to 0$, the agent behaves myopically (focusing on immediate reward); when $\gamma \to 1$, the agent acts far-sighted.</p>
          </div>
        </div>

        <div class="glass-table-wrapper" style="margin-top: 18px;">
          <table class="glass-table">
            <thead>
              <tr>
                <th>RL Paradigm Type</th>
                <th>Core Behavioral Concept</th>
                <th>Environment Model Requirement</th>
                <th>Policy Optimization Mode</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color: var(--accent-cyan);">Passive RL</strong></td>
                <td>Policy $\pi$ is fixed. Agent evaluates utility $U^\pi(s)$ of states without altering decisions.</td>
                <td>Model-free (Direct / TD) or Model-based (ADP)</td>
                <td>Policy Evaluation only</td>
              </tr>
              <tr>
                <td><strong style="color: var(--accent-emerald);">Active RL</strong></td>
                <td>Agent actively selects actions to balance exploration vs exploitation and discover optimal policy $\pi^*$.</td>
                <td>Can be Model-Free (Q-Learning, SARSA) or Model-Based</td>
                <td>Policy Control & Improvement</td>
              </tr>
              <tr>
                <td><strong style="color: var(--accent-violet);">Model-Based RL</strong></td>
                <td>Agent learns/uses transition probability $T(s,a,s')$ and reward $R(s,a,s')$ models for planning.</td>
                <td>Explicit transition and reward matrices required</td>
                <td>Dynamic Programming / Value Iteration</td>
              </tr>
              <tr>
                <td><strong style="color: var(--accent-amber);">Model-Free RL</strong></td>
                <td>Agent learns state utilities or action-values directly from raw experiential sample trajectories.</td>
                <td>No prior or learned model needed</td>
                <td>Bootstrapped experiential updates</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Unit 2: Passive Reinforcement Learning -->
      <div class="glass-card">
        <div class="card-header-flex">
          <h3>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>
            2. Passive Reinforcement Learning: Methods & Bellman Dynamics
          </h3>
          <span class="badge-pill violet">Section 2.1 - 2.3</span>
        </div>

        <p>In <strong>Passive Reinforcement Learning</strong>, the agent's behavior is dictated by a fixed, immutable policy $\pi$. The objective is purely <em>policy evaluation</em>: determining the expected utility $U^\pi(s)$ of each visited state under policy $\pi$. Three primary mathematical approaches exist:</p>

        <div class="grid-3" style="margin-top: 16px;">
          <div style="background: rgba(15, 23, 42, 0.45); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <h4 style="color: var(--accent-cyan); font-size: 1.05rem; margin-bottom: 8px;">A. Direct Utility Estimation</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 10px;">A Monte Carlo sample-averaging method. The agent executes full episodes and calculates total observed returns from each state, maintaining a running sample mean.</p>
            <div class="math-formula-box" style="font-size: 0.82rem;">
              $$U(s) \leftarrow \frac{1}{N(s)} \sum_{i=1}^{N(s)} G_i(s)$$
            </div>
            <p style="font-size: 0.8rem; color: var(--accent-emerald);"><strong>Advantage:</strong> Unbiased estimates; trivially simple.</p>
            <p style="font-size: 0.8rem; color: var(--accent-rose); margin-top: 4px;"><strong>Limitation:</strong> Misses Bellman state constraints; high variance; cannot bootstrap within an episode.</p>
          </div>

          <div style="background: rgba(15, 23, 42, 0.45); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <h4 style="color: var(--accent-violet); font-size: 1.05rem; margin-bottom: 8px;">B. Adaptive Dynamic Programming (ADP)</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 10px;">A model-based paradigm. The agent empirically counts transition frequencies to learn $\hat{T}(s,\pi(s),s')$ and solves the system of linear Bellman equations:</p>
            <div class="math-formula-box" style="font-size: 0.82rem;">
              $$U^\pi(s) = R(s) + \gamma \sum_{s'} \hat{T}(s, \pi(s), s') U^\pi(s')$$
            </div>
            <p style="font-size: 0.8rem; color: var(--accent-emerald);"><strong>Advantage:</strong> Optimal sample efficiency (extracts maximum info from each transition).</p>
            <p style="font-size: 0.8rem; color: var(--accent-rose); margin-top: 4px;"><strong>Limitation:</strong> Solving system is $O(|S|^3)$, computationally intractable for large state spaces.</p>
          </div>

          <div style="background: rgba(15, 23, 42, 0.45); padding: 18px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <h4 style="color: var(--accent-emerald); font-size: 1.05rem; margin-bottom: 8px;">C. Temporal-Difference TD(0) Learning</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 10px;">Model-free bootstrapping. Updates state utility immediately upon making a transition from $s$ to $s'$ using the TD error between successive predictions:</p>
            <div class="math-formula-box" style="font-size: 0.82rem;">
              $$U(s) \leftarrow U(s) + \alpha \underbrace{[R(s) + \gamma U(s') - U(s)]}_{\text{TD Error } \delta}$$
            </div>
            <p style="font-size: 0.8rem; color: var(--accent-emerald);"><strong>Advantage:</strong> Online, model-free, fast, low computational overhead.</p>
            <p style="font-size: 0.8rem; color: var(--accent-rose); margin-top: 4px;"><strong>Limitation:</strong> Biased initial estimates; convergence rate relies sensitively on learning rate $\alpha$.</p>
          </div>
        </div>
      </div>

      <!-- Unit 3: Active RL (Q-Learning vs SARSA) -->
      <div class="glass-card">
        <div class="card-header-flex">
          <h3>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" /></svg>
            3. Active Reinforcement Learning: Q-Learning (Off-Policy) vs SARSA (On-Policy)
          </h3>
          <span class="badge-pill">Section 3.1 - 3.5</span>
        </div>

        <p>In <strong>Active Reinforcement Learning</strong>, the agent must simultaneously solve two fundamental problems: <strong>1) Exploration vs Exploitation</strong> (trying novel actions to discover better returns versus capitalizing on known rewarding actions via $\epsilon$-greedy strategies), and <strong>2) Policy Improvement</strong> (learning the optimal action-value function $Q^*(s,a)$).</p>

        <div class="grid-2" style="margin-top: 16px;">
          <div style="background: rgba(15, 23, 42, 0.45); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(56, 189, 248, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <h4 style="color: var(--accent-cyan); font-size: 1.1rem;">Q-Learning (Watkins 1989 / 1992)</h4>
              <span class="badge-pill">Off-Policy TD Control</span>
            </div>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 12px;">Updates $Q(s,a)$ assuming the agent will follow the greedy optimal action $\max_{a'} Q(s',a')$ in the next state, independent of the actual exploratory action taken.</p>
            <div class="math-formula-box">
              $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R(s,a) + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$
            </div>
            <ul style="padding-left: 20px; font-size: 0.84rem; color: #94a3b8; line-height: 1.6;">
              <li><strong>Target Policy:</strong> Greedy with respect to current $Q$.</li>
              <li><strong>Behavior Policy:</strong> $\epsilon$-greedy (can be any exploratory distribution).</li>
              <li><strong>Path Characteristic:</strong> Learns the strictly shortest/optimal path directly adjacent to hazards (e.g. cliff edge), even though exploratory slips might cause catastrophic penalties during training!</li>
            </ul>
          </div>

          <div style="background: rgba(15, 23, 42, 0.45); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(168, 85, 247, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <h4 style="color: var(--accent-violet); font-size: 1.1rem;">SARSA (Rummery & Niranjan 1994)</h4>
              <span class="badge-pill violet">On-Policy TD Control</span>
            </div>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 12px;">Represents tuple $(s, a, r, s', a')$. Updates $Q(s,a)$ based on the <em>actual action</em> $a'$ chosen by the agent's ongoing behavioral policy (including exploration randomness).</p>
            <div class="math-formula-box">
              $$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R(s,a) + \gamma Q(s', a') - Q(s, a) \right]$$
            </div>
            <ul style="padding-left: 20px; font-size: 0.84rem; color: #94a3b8; line-height: 1.6;">
              <li><strong>Target Policy:</strong> Identical to behavior policy ($\epsilon$-greedy).</li>
              <li><strong>Safety Awareness:</strong> Penalizes states near cliffs because exploratory random moves from those states frequently fall off.</li>
              <li><strong>Path Characteristic:</strong> Learns a longer, conservative path routed safely away from dangers.</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Unit 4, 5, 6: Generalization, Policy Search, Inverse RL -->
      <div class="grid-3">
        <!-- Unit 4 -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3 style="font-size: 1.1rem;">4. Generalization & Function Approx</h3>
            <span class="badge-pill">Section 4</span>
          </div>
          <p style="font-size: 0.84rem; color: #94a3b8; margin-bottom: 10px;">Real-world state spaces are astronomically large or continuous; tabular lookup tables fail due to memory and experience deficits.</p>
          <div class="callout-box" style="font-size: 0.82rem;">
            <strong>Linear Feature Approx:</strong>
            $$\hat{U}(s) = \mathbf{w}^T \mathbf{x}(s) = \sum_{i=1}^d w_i f_i(s)$$
            Where $f_i(s)$ are engineered features (e.g. distance to wall, velocity).
          </div>
          <div class="callout-box emerald" style="font-size: 0.82rem;">
            <strong>Deep Neural Approx:</strong>
            $$\hat{Q}(s, a; \mathbf{w}) \approx Q^*(s,a)$$
            Trained via gradient descent minimizing mean squared Bellman error.
          </div>
        </div>

        <!-- Unit 5 -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3 style="font-size: 1.1rem;">5. Policy Search & Gradients</h3>
            <span class="badge-pill violet">Section 5</span>
          </div>
          <p style="font-size: 0.84rem; color: #94a3b8; margin-bottom: 10px;">Directly parameterizes the policy $\pi_\theta(a|s)$ rather than deriving actions from a value function. Essential for continuous action spaces.</p>
          <div class="callout-box violet" style="font-size: 0.82rem;">
            <strong>Policy Gradient Update:</strong>
            $$\theta \leftarrow \theta + \alpha \nabla_\theta J(\theta)$$
            Where $J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [R(\tau)]$ is expected return.
          </div>
          <p style="font-size: 0.8rem; color: #cbd5e1;">Uses the <em>Policy Gradient Theorem</em> (REINFORCE) to compute $\nabla_\theta \log \pi_\theta(a|s) G_t$ without needing environment dynamics!</p>
        </div>

        <!-- Unit 6 -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3 style="font-size: 1.1rem;">6. Apprenticeship & Inverse RL</h3>
            <span class="badge-pill emerald">Section 6</span>
          </div>
          <p style="font-size: 0.84rem; color: #94a3b8; margin-bottom: 10px;">In complex real-world tasks, engineering an explicit reward function is intractable (risk of reward hacking). Agents learn from expert demonstrations.</p>
          <div class="callout-box emerald" style="font-size: 0.82rem;">
            <strong>Inverse RL (Ng & Russell 2000):</strong>
            Given expert trajectories $\mathcal{D} = \{\tau_1, \tau_2, \dots\}$, deduce the hidden reward function $R^*(s)$ that explains why the expert's policy is optimal.
          </div>
          <p style="font-size: 0.8rem; color: var(--accent-amber);"><strong>Ambiguity:</strong> Multiple reward functions can produce identical trajectories (e.g. $R(s) = 0$ everywhere is trivial).</p>
        </div>
      </div>
    </div>

    <!-- ===========================================================
         TAB 2: TOP 5 RESEARCH PAPERS & LIVE WORKING DEMOS
         =========================================================== -->
    <div class="tab-pane" id="tab-demos">
      <div class="section-title-bar">
        <div>
          <h2>Top 5 Breakthrough Research Papers in Reinforcement Learning</h2>
          <p>Explore seminal foundation papers that shaped modern AI, complete with fully interactive visual simulations of their algorithmic innovations.</p>
        </div>
        <span class="badge-pill violet">Peer-Reviewed Milestones</span>
      </div>

      <!-- DEMO 1: CLIFF WALKING ARENA (Watkins 1992 / Sutton 1988) -->
      <div class="glass-card">
        <div class="card-header-flex">
          <div>
            <span class="badge-pill" style="margin-bottom: 6px; display: inline-block;">Paper 5 Foundation Demo</span>
            <h3>Interactive Arena: Q-Learning (Off-Policy) vs SARSA (On-Policy) Cliff Walking</h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Watch the dramatic divergence in agent survival: Q-Learning optimizes for the theoretical minimum step count along the cliff edge (-100 penalty), while SARSA learns the safe perimeter path!</p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="glass-btn primary" id="btn-toggle-run" onclick="toggleArenaTraining()">
              <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              <span id="txt-run-btn">Start Training</span>
            </button>
            <button class="glass-btn" onclick="stepArenaOne()">Step</button>
            <button class="glass-btn" onclick="resetArenaEnv()">Reset</button>
          </div>
        </div>

        <div class="grid-2">
          <!-- Canvas visualizer -->
          <div>
            <div class="sim-canvas-container" style="height: 280px;">
              <canvas id="cliff-canvas" width="600" height="200"></canvas>
            </div>
            
            <div class="controls-strip">
              <div class="ctrl-group">
                <label>Algorithm:</label>
                <select id="arena-algo-select" class="form-input" style="padding: 4px 10px; font-size: 0.8rem;" onchange="onAlgoChange()">
                  <option value="qlearning">Q-Learning (Off-Policy)</option>
                  <option value="sarsa">SARSA (On-Policy)</option>
                </select>
              </div>
              <div class="ctrl-group">
                <label>$\alpha$ (LR):</label>
                <input type="range" class="ctrl-slider" id="slider-alpha" min="0.05" max="0.9" step="0.05" value="0.2" oninput="updateArenaHyperparams()">
                <span class="stat-badge" id="val-alpha">0.20</span>
              </div>
              <div class="ctrl-group">
                <label>$\epsilon$ (Exploration):</label>
                <input type="range" class="ctrl-slider" id="slider-eps" min="0.01" max="0.5" step="0.02" value="0.1" oninput="updateArenaHyperparams()">
                <span class="stat-badge" id="val-eps">0.10</span>
              </div>
              <div class="ctrl-group">
                <label>Speed:</label>
                <input type="range" class="ctrl-slider" id="slider-speed" min="1" max="100" step="5" value="20" oninput="updateArenaHyperparams()">
              </div>
            </div>
          </div>

          <!-- Live Metrics & Chart -->
          <div>
            <div style="display: flex; gap: 12px; margin-bottom: 12px;">
              <div style="flex: 1; background: rgba(15, 23, 42, 0.5); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--glass-border);">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Episodes Completed</div>
                <div style="font-family: var(--font-heading); font-size: 1.3rem; font-weight: 700; color: var(--accent-cyan);" id="stat-episodes">0</div>
              </div>
              <div style="flex: 1; background: rgba(15, 23, 42, 0.5); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--glass-border);">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Current Episode Reward</div>
                <div style="font-family: var(--font-heading); font-size: 1.3rem; font-weight: 700; color: var(--accent-emerald);" id="stat-reward">0</div>
              </div>
              <div style="flex: 1; background: rgba(15, 23, 42, 0.5); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--glass-border);">
                <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase;">Total Cliff Falls</div>
                <div style="font-family: var(--font-heading); font-size: 1.3rem; font-weight: 700; color: var(--accent-rose);" id="stat-falls">0</div>
              </div>
            </div>

            <div style="height: 200px; background: rgba(10, 15, 29, 0.6); border-radius: var(--radius-md); padding: 8px; border: 1px solid var(--glass-border);">
              <canvas id="arena-chart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- TOP 5 RESEARCH PAPERS SHOWCASE -->
      <div class="grid-2">

        <!-- PAPER 1: MNIH ET AL. (2015) DQN -->
        <div class="paper-card">
          <div class="paper-rank-tag">#1</div>
          <div>
            <div class="paper-venue">Nature 518 (2015) • Google DeepMind</div>
            <h4 class="paper-title">Human-Level Control Through Deep Reinforcement Learning (DQN)</h4>
            <div class="paper-authors">Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A. Rusu, et al.</div>
            <p class="paper-desc">First algorithm to master 49 Atari 2600 video games directly from raw pixel screen inputs without handcrafted features, matching or exceeding professional human performance.</p>
            <ul class="paper-innovations">
              <li><strong>Experience Replay Buffer:</strong> Breaks temporal correlations between consecutive video frames via random mini-batch sampling.</li>
              <li><strong>Target Network ($\theta^-$):</strong> Fixes Q-value targets for $C$ steps to stabilize gradient descent and prevent mathematical divergence.</li>
            </ul>
          </div>
          <!-- Interactive DQN Replay Visualizer -->
          <div style="margin-top: 14px; background: rgba(5, 10, 20, 0.6); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 0.78rem; font-weight: 600; color: var(--accent-cyan);">Live DQN Replay Buffer Simulator</span>
              <button class="glass-btn" style="padding: 3px 8px; font-size: 0.72rem;" onclick="simulateDQNStep()">Push & Sample Batch</button>
            </div>
            <canvas id="dqn-replay-canvas" width="400" height="90" style="width: 100%; border-radius: 4px; background: #000;"></canvas>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; display: flex; justify-content: space-between;">
              <span id="dqn-buffer-status">Buffer: 42/1000 items</span>
              <span id="dqn-loss-status">Bellman MSE Loss: 0.041</span>
            </div>
          </div>
        </div>

        <!-- PAPER 2: SILVER ET AL. (2016) ALPHAGO -->
        <div class="paper-card">
          <div class="paper-rank-tag">#2</div>
          <div>
            <div class="paper-venue">Nature 529 (2016) • Google DeepMind</div>
            <h4 class="paper-title">Mastering the Game of Go with Deep Neural Networks and Tree Search (AlphaGo)</h4>
            <div class="paper-authors">David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Demis Hassabis, et al.</div>
            <p class="paper-desc">Defeated 18-time world Go champion Lee Sedol 4-1. Combined policy networks (pruning search breadth) and value networks (pruning search depth) with Monte Carlo Tree Search (MCTS).</p>
            <ul class="paper-innovations">
              <li><strong>Dual-Head Residual Networks:</strong> Outputs both move probability distribution $P(s,a)$ and scalar position evaluation $V(s)$.</li>
              <li><strong>PUCT Selection Formula:</strong> Balances node exploitation $Q(s,a)$ with exploration bonus $U(s,a) \propto \frac{P(s,a)}{1+N(s,a)}$.</li>
            </ul>
          </div>
          <!-- Interactive MCTS Visualizer -->
          <div style="margin-top: 14px; background: rgba(5, 10, 20, 0.6); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 0.78rem; font-weight: 600; color: var(--accent-violet);">Interactive MCTS Tree Search</span>
              <div style="display: flex; gap: 4px;">
                <button class="glass-btn" style="padding: 3px 8px; font-size: 0.72rem;" onclick="stepMCTS()">+1 Search Iteration</button>
                <button class="glass-btn" style="padding: 3px 8px; font-size: 0.72rem;" onclick="resetMCTS()">Reset</button>
              </div>
            </div>
            <canvas id="mcts-canvas" width="400" height="100" style="width: 100%; border-radius: 4px; background: #000;"></canvas>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; display: flex; justify-content: space-between;">
              <span id="mcts-iter-status">Simulated Rollouts: 14</span>
              <span id="mcts-best-move">Root Best Action: Branch B (Q=0.74)</span>
            </div>
          </div>
        </div>

        <!-- PAPER 3: SCHULMAN ET AL. (2017) PPO -->
        <div class="paper-card">
          <div class="paper-rank-tag">#3</div>
          <div>
            <div class="paper-venue">arXiv:1707.06347 (2017) • OpenAI</div>
            <h4 class="paper-title">Proximal Policy Optimization Algorithms (PPO)</h4>
            <div class="paper-authors">John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov</div>
            <p class="paper-desc">The industry standard algorithm powering modern robotics and Reinforcement Learning from Human Feedback (RLHF) in LLMs (ChatGPT, Gemini, Claude). Eliminates catastrophic policy collapse.</p>
            <ul class="paper-innovations">
              <li><strong>Clipped Surrogate Objective:</strong> Clips probability ratio $r_t(\theta) = \frac{\pi_\theta(a|s)}{\pi_{\theta_{old}}(a|s)}$ to $[1-\epsilon, 1+\epsilon]$.</li>
              <li><strong>First-Order Optimization:</strong> Achieves TRPO trust-region stability with standard Stochastic Gradient Descent (SGD) / Adam.</li>
            </ul>
          </div>
          <!-- Interactive PPO Clipping Visualizer -->
          <div style="margin-top: 14px; background: rgba(5, 10, 20, 0.6); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 0.78rem; font-weight: 600; color: var(--accent-emerald);">PPO Clipped Objective Interactive Visualizer</span>
              <span class="stat-badge" id="ppo-clip-badge">Advantage: +1.5</span>
            </div>
            <canvas id="ppo-canvas" width="400" height="90" style="width: 100%; border-radius: 4px; background: #000;"></canvas>
            <div style="display: flex; gap: 8px; align-items: center; margin-top: 6px;">
              <button class="glass-btn" style="padding: 2px 8px; font-size: 0.7rem;" onclick="setPPOAdvantage(1.5)">Positive Adv ($A>0$)</button>
              <button class="glass-btn" style="padding: 2px 8px; font-size: 0.7rem;" onclick="setPPOAdvantage(-1.5)">Negative Adv ($A<0$)</button>
              <span style="font-size: 0.72rem; color: var(--text-muted);">Clip $\epsilon$: 0.20</span>
            </div>
          </div>
        </div>

        <!-- PAPER 4: NG & RUSSELL (2000) INVERSE RL -->
        <div class="paper-card">
          <div class="paper-rank-tag">#4</div>
          <div>
            <div class="paper-venue">ICML (2000) • UC Berkeley & Stanford</div>
            <h4 class="paper-title">Algorithms for Inverse Reinforcement Learning (IRL)</h4>
            <div class="paper-authors">Andrew Y. Ng, Stuart Russell</div>
            <p class="paper-desc">Seminal foundation paper defining the formal mathematical framework for inferring an underlying hidden reward function from observing expert behavioral trajectories.</p>
            <ul class="paper-innovations">
              <li><strong>Reward Duality:</strong> Inverts the standard MDP formulation to resolve unknown reward matrices $R^*(s)$ via linear programming.</li>
              <li><strong>Maximum Margin Optimization:</strong> Maximizes the performance gap between expert policies and sub-optimal deviations.</li>
            </ul>
          </div>
          <!-- Interactive IRL Demonstration -->
          <div style="margin-top: 14px; background: rgba(5, 10, 20, 0.6); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--glass-border);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 0.78rem; font-weight: 600; color: var(--accent-amber);">Expert Trajectory to Inferred Reward</span>
              <button class="glass-btn" style="padding: 3px 8px; font-size: 0.72rem;" onclick="runIRLInference()">Solve Inferred $R(s)$</button>
            </div>
            <canvas id="irl-canvas" width="400" height="90" style="width: 100%; border-radius: 4px; background: #000;"></canvas>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; display: flex; justify-content: space-between;">
              <span>Demonstration: 3 Expert Paths</span>
              <span id="irl-status" style="color: var(--accent-emerald);">Reward Inferred with Margin $\Delta=1.82$</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ===========================================================
         TAB 3: REAL-WORLD INDUSTRIAL APPLICATIONS
         =========================================================== -->
    <div class="tab-pane" id="tab-apps">
      <div class="section-title-bar">
        <div>
          <h2>Industrial Reinforcement Learning Applications</h2>
          <p>Real-time physics and algorithmic simulations demonstrating Reinforcement Learning deployed across energy storage and autonomous robotics.</p>
        </div>
        <span class="badge-pill emerald">Production Case Studies</span>
      </div>

      <div class="grid-2">
        <!-- APPLICATION A: SMART POWER GRID PEAK SHAVING -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" /></svg>
              Application 1: Smart Grid Battery Energy Storage Dispatch
            </h3>
            <span class="badge-pill emerald">Energy & Cleantech</span>
          </div>
          <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">The RL agent manages a 500 kWh commercial battery system. It observes fluctuating real-time dynamic electricity prices ($/kWh) and solar PV output, learning an optimal policy to charge during surplus hours and discharge during expensive peak demand.</p>
          
          <div class="sim-canvas-container" style="height: 200px;">
            <canvas id="battery-sim-canvas" width="550" height="190"></canvas>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div style="display: flex; gap: 8px;">
              <button class="glass-btn primary" onclick="toggleBatterySim()" id="btn-battery-sim">Pause Simulation</button>
              <button class="glass-btn" onclick="resetBatterySim()">Reset 24h Cycle</button>
            </div>
            <div style="display: flex; gap: 12px; font-size: 0.84rem;">
              <span>Net Cost Savings: <strong style="color: var(--accent-emerald);" id="stat-battery-savings">$428.50</strong></span>
              <span>Battery SoC: <strong style="color: var(--accent-cyan);" id="stat-battery-soc">68%</strong></span>
            </div>
          </div>
        </div>

        <!-- APPLICATION B: AUTONOMOUS ROBOT NAVIGATION -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.129-1.125V14.25m-17.25 4.5v-2.25m17.25 2.25v-2.25M6 10.5h12m-9 3h6m-6-6h6m-9-3h12" /></svg>
              Application 2: Autonomous Mobile Robot LIDAR Obstacle Avoidance
            </h3>
            <span class="badge-pill violet">Robotics & Vehicles</span>
          </div>
          <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">Demonstrating <em>Feature-Based Generalization (Section 4)</em>. The robot receives 8 raycast distance sensors $\mathbf{x}(s) = [d_1, \dots, d_8, \theta_{target}, v]$ and continuously steers towards the goal beacon while avoiding dynamic moving obstacles.</p>

          <div class="sim-canvas-container" style="height: 200px;">
            <canvas id="robot-sim-canvas" width="550" height="190"></canvas>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
            <div style="display: flex; gap: 8px;">
              <button class="glass-btn primary" onclick="toggleRobotSim()" id="btn-robot-sim">Pause Robot</button>
              <button class="glass-btn" onclick="relocateRobotGoal()">Move Goal Beacon</button>
            </div>
            <div style="font-size: 0.84rem; color: var(--text-muted);">
              Goals Reached: <strong style="color: var(--accent-emerald);" id="stat-robot-goals">12</strong> | Collisions: <strong style="color: var(--accent-rose);" id="stat-robot-hits">0</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===========================================================
         TAB 4: INTERACTIVE EXAM NUMERICALS & FORMULA SOLVER
         =========================================================== -->
    <div class="tab-pane" id="tab-solver">
      <div class="section-title-bar">
        <div>
          <h2>KTU University Exam Numerical Problem Solver</h2>
          <p>Instant step-by-step calculator for university exam questions: compute Temporal-Difference TD(0) errors, Q-learning backups, SARSA values, and discounted returns.</p>
        </div>
        <span class="badge-pill">Step-by-Step Derivations</span>
      </div>

      <div class="grid-2">
        <!-- SOLVER 1: TD(0) UPDATE CALCULATOR -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" /></svg>
              1. Temporal-Difference TD(0) Step Calculator
            </h3>
            <span class="badge-pill">Exam Favorite</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-muted);">Formula: $U(s) \leftarrow U(s) + \alpha [R(s) + \gamma U(s') - U(s)]$</p>

          <div class="solver-grid">
            <div class="form-field">
              <label>Current Utility $U(s)$:</label>
              <input type="number" step="0.1" class="form-input" id="td-u-s" value="2.5">
            </div>
            <div class="form-field">
              <label>Observed Reward $R$:</label>
              <input type="number" step="0.1" class="form-input" id="td-r" value="-1.0">
            </div>
            <div class="form-field">
              <label>Next State Utility $U(s')$:</label>
              <input type="number" step="0.1" class="form-input" id="td-u-next" value="4.0">
            </div>
            <div class="form-field">
              <label>Discount Factor $\gamma$:</label>
              <input type="number" step="0.05" min="0" max="1" class="form-input" id="td-gamma" value="0.9">
            </div>
            <div class="form-field">
              <label>Learning Rate $\alpha$:</label>
              <input type="number" step="0.05" min="0" max="1" class="form-input" id="td-alpha" value="0.5">
            </div>
          </div>

          <button class="glass-btn primary" style="width: 100%; margin-top: 10px;" onclick="calculateTD0()">Solve TD(0) Step</button>

          <div class="calc-result-box active" id="td-result-box">
            <div style="font-size: 0.85rem; line-height: 1.8;" id="td-result-content">
              <strong>Calculation Breakdown:</strong><br>
              1. Target Prediction: $R + \gamma U(s') = -1.0 + (0.9 \times 4.0) = 2.60$<br>
              2. TD Error $\delta = 2.60 - 2.50 = \mathbf{+0.10}$<br>
              3. Updated Utility $U(s) = 2.50 + 0.5 \times (0.10) = \mathbf{2.55}$
            </div>
          </div>
        </div>

        <!-- SOLVER 2: Q-LEARNING UPDATE CALCULATOR -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" /></svg>
              2. Q-Learning (Off-Policy) Step Calculator
            </h3>
            <span class="badge-pill violet">Algorithm 3.3</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-muted);">Formula: $Q(s,a) \leftarrow Q(s,a) + \alpha [R + \gamma \max_{a'} Q(s',a') - Q(s,a)]$</p>

          <div class="solver-grid">
            <div class="form-field">
              <label>Current $Q(s,a)$:</label>
              <input type="number" step="0.1" class="form-input" id="ql-q" value="5.0">
            </div>
            <div class="form-field">
              <label>Immediate Reward $R$:</label>
              <input type="number" step="0.1" class="form-input" id="ql-r" value="10.0">
            </div>
            <div class="form-field">
              <label>Candidate $\max_{a'} Q(s',a')$:</label>
              <input type="number" step="0.1" class="form-input" id="ql-max-next" value="8.0">
            </div>
            <div class="form-field">
              <label>Discount $\gamma$:</label>
              <input type="number" step="0.05" class="form-input" id="ql-gamma" value="0.8">
            </div>
            <div class="form-field">
              <label>Learning Rate $\alpha$:</label>
              <input type="number" step="0.05" class="form-input" id="ql-alpha" value="0.2">
            </div>
          </div>

          <button class="glass-btn primary" style="width: 100%; margin-top: 10px;" onclick="calculateQLearning()">Solve Q-Learning Update</button>

          <div class="calc-result-box active" id="ql-result-box">
            <div style="font-size: 0.85rem; line-height: 1.8;" id="ql-result-content">
              <strong>Calculation Breakdown:</strong><br>
              1. Bellman Optimality Target: $R + \gamma \max_{a'} Q(s',a') = 10.0 + (0.8 \times 8.0) = 16.40$<br>
              2. Difference: $16.40 - 5.0 = \mathbf{+11.40}$<br>
              3. Updated $Q(s,a) = 5.0 + 0.2 \times (11.40) = \mathbf{7.28}$
            </div>
          </div>
        </div>

        <!-- SOLVER 3: DISCOUNTED CUMULATIVE RETURN CALCULATOR -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>3. Discounted Return $G_t$ Trajectory Calculator</h3>
            <span class="badge-pill emerald">Equation 1.4</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-muted);">Enter comma-separated sequential rewards $R_{t+1}, R_{t+2}, \dots$</p>
          
          <div class="form-field" style="margin: 10px 0;">
            <label>Reward Sequence (e.g. -1, -1, 0, 10):</label>
            <input type="text" class="form-input" id="ret-seq" value="-1, -1, 0, 10">
          </div>
          <div class="form-field">
            <label>Discount Factor $\gamma$:</label>
            <input type="number" step="0.05" min="0" max="1" class="form-input" id="ret-gamma" value="0.9">
          </div>
          <button class="glass-btn primary" style="width: 100%; margin-top: 14px;" onclick="calculateReturn()">Compute Cumulative $G_t$</button>
          
          <div class="calc-result-box active" id="ret-result-box">
            <div style="font-size: 0.85rem; line-height: 1.8;" id="ret-result-content">
              <strong>Result:</strong> $G_0 = (-1) + 0.9(-1) + 0.81(0) + 0.729(10) = \mathbf{+5.39}$
            </div>
          </div>
        </div>

        <!-- SOLVER 4: SARSA STEP CALCULATOR -->
        <div class="glass-card">
          <div class="card-header-flex">
            <h3>4. SARSA (On-Policy) Step Calculator</h3>
            <span class="badge-pill amber">Equation 3.4</span>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-muted);">Formula: $Q(s,a) \leftarrow Q(s,a) + \alpha [R + \gamma Q(s',a') - Q(s,a)]$</p>

          <div class="solver-grid">
            <div class="form-field">
              <label>Current $Q(s,a)$:</label>
              <input type="number" step="0.1" class="form-input" id="sarsa-q" value="4.0">
            </div>
            <div class="form-field">
              <label>Reward $R$:</label>
              <input type="number" step="0.1" class="form-input" id="sarsa-r" value="-2.0">
            </div>
            <div class="form-field">
              <label>Selected $Q(s',a')$:</label>
              <input type="number" step="0.1" class="form-input" id="sarsa-q-next" value="3.0">
            </div>
            <div class="form-field">
              <label>Discount $\gamma$:</label>
              <input type="number" step="0.05" class="form-input" id="sarsa-gamma" value="0.9">
            </div>
            <div class="form-field">
              <label>Learning Rate $\alpha$:</label>
              <input type="number" step="0.05" class="form-input" id="sarsa-alpha" value="0.3">
            </div>
          </div>
          <button class="glass-btn primary" style="width: 100%; margin-top: 10px;" onclick="calculateSARSA()">Solve SARSA Step</button>

          <div class="calc-result-box active" id="sarsa-result-box">
            <div style="font-size: 0.85rem; line-height: 1.8;" id="sarsa-result-content">
              <strong>Calculation Breakdown:</strong><br>
              1. On-Policy Target: $R + \gamma Q(s',a') = -2.0 + (0.9 \times 3.0) = 0.70$<br>
              2. Updated $Q(s,a) = 4.0 + 0.3 \times (0.70 - 4.0) = \mathbf{3.01}$
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===========================================================
         TAB 5: LOCAL DEPLOYMENT GUIDE & VIRTUAL TERMINAL
         =========================================================== -->
    <div class="tab-pane" id="tab-deploy">
      <div class="section-title-bar">
        <div>
          <h2>Local Deployment & Engineering Architecture</h2>
          <p>Production recipes for deploying Reinforcement Learning agents locally with PyTorch, Gymnasium, FastAPI, Docker, and Web Servers.</p>
        </div>
        <span class="badge-pill emerald">Zero Setup Ready</span>
      </div>

      <div class="grid-2">
        <!-- DEPLOYMENT RECIPES -->
        <div>
          <div class="glass-card">
            <h3 style="margin-bottom: 12px; color: var(--accent-cyan);">1. Python Environment & Gymnasium Setup</h3>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 10px;">Create an isolated Python 3.10+ virtual environment and install standard RL packages:</p>
            <div class="code-block-wrapper">
              <div class="code-header">
                <span class="code-filename">Terminal (PowerShell / Bash)</span>
                <button class="copy-btn" onclick="copyCode(this)">Copy</button>
              </div>
              <pre class="code-content"># 1. Create and activate virtual environment
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# 2. Install PyTorch, Gymnasium & Stable-Baselines3
pip install torch torchvision
pip install gymnasium[classic-control] stable-baselines3 fastapi uvicorn</pre>
            </div>
          </div>

          <div class="glass-card">
            <h3 style="margin-bottom: 12px; color: var(--accent-violet);">2. Standalone Training Script: <code>train_agent.py</code></h3>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 10px;">Complete working PPO training code on Gymnasium CartPole-v1:</p>
            <div class="code-block-wrapper">
              <div class="code-header">
                <span class="code-filename">train_agent.py</span>
                <button class="copy-btn" onclick="copyCode(this)">Copy</button>
              </div>
              <pre class="code-content">import gymnasium as gym
from stable_baselines3 import PPO

# Initialize Gymnasium Environment
env = gym.make("CartPole-v1", render_mode="rgb_array")

# Instantiate PPO Agent (MlpPolicy neural network)
model = PPO(
    policy="MlpPolicy",
    env=env,
    learning_rate=3e-4,
    gamma=0.99,
    verbose=1
)

# Train for 20,000 steps
print("Training PPO Agent...")
model.learn(total_timesteps=20000)

# Save trained policy weights
model.save("ppo_cartpole_model")
print("Model successfully saved to ppo_cartpole_model.zip!")</pre>
            </div>
          </div>

          <div class="glass-card">
            <h3 style="margin-bottom: 12px; color: var(--accent-emerald);">3. Docker Containerization</h3>
            <div class="code-block-wrapper">
              <div class="code-header">
                <span class="code-filename">Dockerfile</span>
                <button class="copy-btn" onclick="copyCode(this)">Copy</button>
              </div>
              <pre class="code-content">FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]</pre>
            </div>
          </div>
        </div>

        <!-- VIRTUAL TERMINAL PLAYGROUND -->
        <div>
          <div class="glass-card">
            <div class="card-header-flex">
              <h3 style="color: #34d399;">Interactive Simulated Deployment Terminal</h3>
              <span class="badge-pill emerald">Live Simulator</span>
            </div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 14px;">Test CLI commands directly in your browser. Click any quick command button below to simulate execution:</p>
            
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px;">
              <button class="glass-btn" style="padding: 5px 12px; font-size: 0.78rem;" onclick="runTerminalCmd('python train_agent.py')">▶ python train_agent.py</button>
              <button class="glass-btn" style="padding: 5px 12px; font-size: 0.78rem;" onclick="runTerminalCmd('uvicorn app:app --port 8000')">▶ uvicorn app:app</button>
              <button class="glass-btn" style="padding: 5px 12px; font-size: 0.78rem;" onclick="runTerminalCmd('docker-compose up --build')">▶ docker-compose up</button>
              <button class="glass-btn" style="padding: 5px 12px; font-size: 0.78rem;" onclick="runTerminalCmd('clear')">Clear Terminal</button>
            </div>

            <div class="terminal-window">
              <div class="terminal-bar">
                <div class="t-dot t-red"></div>
                <div class="t-dot t-yellow"></div>
                <div class="t-dot t-green"></div>
                <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 8px;">bash - JaneRose@rl-server:~/AI-MOD4</span>
              </div>
              <div class="terminal-body" id="term-output">
                <div><span class="t-prompt">jane@rl-box:~$</span> <span class="t-cmd">uname -a</span></div>
                <div style="color: #94a3b8; margin: 4px 0 10px;">Linux rl-master-node 6.1.0-ai-x86_64 #1 SMP PREEMPT_DYNAMIC</div>
                <div><span class="t-prompt">jane@rl-box:~$</span> <span class="t-cmd">python -c "import torch, gymnasium; print('CUDA Ready:', torch.cuda.is_available(), '| Gym:', gymnasium.__version__)"</span></div>
                <div style="color: #34d399; margin: 4px 0 10px;">CUDA Ready: True (NVIDIA RTX 4090) | Gym: 0.29.1</div>
                <div><span class="t-prompt">jane@rl-box:~$</span> <span class="t-cmd">Ready for deployment commands. Click a button above.</span></div>
              </div>
            </div>
          </div>

          <div class="glass-card" style="margin-top: 24px;">
            <h3 style="color: var(--accent-cyan); margin-bottom: 8px;">Local Static Dashboard Hosting</h3>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 12px;">This single-page application is completely zero-dependency and ready to host locally via any web server:</p>
            <div class="code-block-wrapper">
              <div class="code-header">
                <span class="code-filename">Host locally in 5 seconds</span>
                <button class="copy-btn" onclick="copyCode(this)">Copy</button>
              </div>
              <pre class="code-content"># Option A: Python Built-in Web Server
python -m http.server 8080

# Option B: Node.js Serve
npx serve .

# Then open in your browser:
http://localhost:8080/index.html</pre>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- -----------------------------------------------------------
         SIGNATURE JANE ROSE FOOTER (MANDATORY REQUIREMENT)
         ----------------------------------------------------------- -->
    <footer class="jane-rose-footer liquid-glass">
      <div class="footer-top">
        <div class="footer-brand">
          <h4>KTU S5 AI Module 4: Reinforcement Learning Master Knowledge System</h4>
          <p>An elite, interactive optical glass platform bridging classical MDP theory, breakthrough research papers, and industrial deployment.</p>
        </div>

        <div class="author-signature-pill">
          <div class="signature-avatar">JR</div>
          <div class="signature-text">
            <span class="signature-title">Created & Curated By</span>
            <span class="signature-name">Jane Rose</span>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>
          &copy; 2026 Jane Rose. All rights reserved. KTU S5 Artificial Intelligence Educational Platform.
        </div>
        <div class="footer-links">
          <a href="#tab-theory" onclick="switchTab('tab-theory')">Syllabus Theory</a>
          <a href="#tab-demos" onclick="switchTab('tab-demos')">Research Demos</a>
          <a href="#tab-apps" onclick="switchTab('tab-apps')">Industry Applications</a>
          <a href="#tab-solver" onclick="switchTab('tab-solver')">Exam Solver</a>
          <a href="#tab-deploy" onclick="switchTab('tab-deploy')">Local Deployment</a>
        </div>
      </div>
    </footer>

  </div>

  <!-- -----------------------------------------------------------
       JAVASCRIPT LOGIC & SIMULATION ENGINES
       ----------------------------------------------------------- -->
  <script>
    // Tab switching engine
    function switchTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      const targetPane = document.getElementById(tabId);
      if (targetPane) targetPane.classList.add('active');
      
      const btn = document.getElementById('btn-' + tabId);
      if (btn) btn.classList.add('active');

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Copy to clipboard helper
    function copyCode(btn) {
      const pre = btn.closest('.code-block-wrapper').querySelector('pre');
      navigator.clipboard.writeText(pre.innerText).then(() => {
        const orig = btn.innerText;
        btn.innerText = 'Copied!';
        setTimeout(() => btn.innerText = orig, 1800);
      });
    }

    /* -------------------------------------------------------------
       1. AMBIENT FLUID BACKGROUND CANVAS
       ------------------------------------------------------------- */
    const ambCanvas = document.getElementById('ambient-canvas');
    const ambCtx = ambCanvas.getContext('2d');
    let width = ambCanvas.width = window.innerWidth;
    let height = ambCanvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
      width = ambCanvas.width = window.innerWidth;
      height = ambCanvas.height = window.innerHeight;
    });

    const orbs = [
      { x: width * 0.2, y: height * 0.25, r: 350, color: 'rgba(56, 189, 248, 0.12)', dx: 0.4, dy: 0.3 },
      { x: width * 0.8, y: height * 0.4, r: 400, color: 'rgba(168, 85, 247, 0.11)', dx: -0.3, dy: 0.35 },
      { x: width * 0.5, y: height * 0.8, r: 380, color: 'rgba(16, 185, 129, 0.08)', dx: 0.25, dy: -0.3 }
    ];

    function drawAmbient() {
      ambCtx.clearRect(0, 0, width, height);
      orbs.forEach(orb => {
        orb.x += orb.dx;
        orb.y += orb.dy;
        if (orb.x < -100 || orb.x > width + 100) orb.dx *= -1;
        if (orb.y < -100 || orb.y > height + 100) orb.dy *= -1;

        const grad = ambCtx.createRadialGradient(orb.x, orb.y, 0, orb.x, orb.y, orb.r);
        grad.addColorStop(0, orb.color);
        grad.addColorStop(1, 'transparent');
        ambCtx.fillStyle = grad;
        ambCtx.fillRect(0, 0, width, height);
      });
      requestAnimationFrame(drawAmbient);
    }
    drawAmbient();

    /* -------------------------------------------------------------
       2. CLIFF WALKING ARENA (Q-LEARNING VS SARSA)
       ------------------------------------------------------------- */
    const cliffCanvas = document.getElementById('cliff-canvas');
    const cliffCtx = cliffCanvas.getContext('2d');
    const ROWS = 4, COLS = 12;
    const cellW = cliffCanvas.width / COLS;
    const cellH = cliffCanvas.height / ROWS;

    // States: (row, col)
    // Start: (3, 0), Goal: (3, 11), Cliff: row 3, col 1..10
    let agentState = { r: 3, c: 0 };
    let arenaAlgo = 'qlearning';
    let alpha = 0.2;
    let gamma = 0.9;
    let epsilon = 0.1;
    let isRunning = false;
    let runInterval = null;
    let episodesCount = 0;
    let currentEpisodeReward = 0;
    let totalFalls = 0;
    let rewardHistory = [];

    // Q-Table: [ROWS][COLS][4 actions: 0:Up, 1:Right, 2:Down, 3:Left]
    let Q = Array.from({ length: ROWS }, () =>
      Array.from({ length: COLS }, () => [0, 0, 0, 0])
    );

    const actions = [
      { dr: -1, dc: 0 }, // Up
      { dr: 0, dc: 1 },  // Right
      { dr: 1, dc: 0 },  // Down
      { dr: 0, dc: -1 }  // Left
    ];

    function isCliff(r, c) {
      return r === 3 && c >= 1 && c <= 10;
    }

    function isGoal(r, c) {
      return r === 3 && c === 11;
    }

    function chooseAction(r, c) {
      if (Math.random() < epsilon) {
        return Math.floor(Math.random() * 4);
      }
      const qValues = Q[r][c];
      let maxVal = -Infinity, bestAct = 0;
      for (let a = 0; a < 4; a++) {
        if (qValues[a] > maxVal) {
          maxVal = qValues[a];
          bestAct = a;
        }
      }
      return bestAct;
    }

    function stepEnvironment(action) {
      let nr = agentState.r + actions[action].dr;
      let nc = agentState.c + actions[action].dc;
      nr = Math.max(0, Math.min(ROWS - 1, nr));
      nc = Math.max(0, Math.min(COLS - 1, nc));

      let reward = -1;
      let done = false;

      if (isCliff(nr, nc)) {
        reward = -100;
        nr = 3;
        nc = 0; // sent back to start
        totalFalls++;
      } else if (isGoal(nr, nc)) {
        reward = 0;
        done = true;
      }

      return { nextState: { r: nr, c: nc }, reward, done };
    }

    function arenaStep() {
      const s = { ...agentState };
      const a = chooseAction(s.r, s.c);
      const { nextState, reward, done } = stepEnvironment(a);
      currentEpisodeReward += reward;

      if (arenaAlgo === 'qlearning') {
        // Off-policy: max over all actions in s'
        const maxNextQ = Math.max(...Q[nextState.r][nextState.c]);
        Q[s.r][s.c][a] += alpha * (reward + gamma * maxNextQ - Q[s.r][s.c][a]);
      } else {
        // SARSA: on-policy: action chosen by current policy in s'
        const nextAction = chooseAction(nextState.r, nextState.c);
        Q[s.r][s.c][a] += alpha * (reward + gamma * Q[nextState.r][nextState.c][nextAction] - Q[s.r][s.c][a]);
      }

      agentState = nextState;

      if (done || currentEpisodeReward < -500) {
        episodesCount++;
        rewardHistory.push(currentEpisodeReward);
        if (rewardHistory.length > 50) rewardHistory.shift();
        currentEpisodeReward = 0;
        agentState = { r: 3, c: 0 };
        updateArenaChart();
      }

      updateArenaStats();
      drawCliffGrid();
    }

    function drawCliffGrid() {
      cliffCtx.clearRect(0, 0, cliffCanvas.width, cliffCanvas.height);

      for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
          const x = c * cellW;
          const y = r * cellH;

          // Fill cell color
          if (r === 3 && c === 0) {
            cliffCtx.fillStyle = 'rgba(56, 189, 248, 0.25)'; // Start
          } else if (isGoal(r, c)) {
            cliffCtx.fillStyle = 'rgba(16, 185, 129, 0.4)'; // Goal
          } else if (isCliff(r, c)) {
            cliffCtx.fillStyle = 'rgba(239, 68, 68, 0.35)'; // Cliff
          } else {
            // Heatmap by max Q
            const maxQ = Math.max(...Q[r][c]);
            const normalized = Math.max(0, Math.min(1, (maxQ + 50) / 50));
            cliffCtx.fillStyle = `rgba(30, 41, 59, ${0.4 + normalized * 0.4})`;
          }
          cliffCtx.fillRect(x, y, cellW, cellH);

          // Grid borders
          cliffCtx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
          cliffCtx.strokeRect(x, y, cellW, cellH);

          // Text labels
          cliffCtx.font = '10px JetBrains Mono';
          cliffCtx.fillStyle = '#94a3b8';
          if (r === 3 && c === 0) {
            cliffCtx.fillStyle = '#38bdf8';
            cliffCtx.fillText('START', x + 6, y + cellH / 2 + 3);
          } else if (isGoal(r, c)) {
            cliffCtx.fillStyle = '#34d399';
            cliffCtx.fillText('GOAL', x + 8, y + cellH / 2 + 3);
          } else if (isCliff(r, c)) {
            cliffCtx.fillStyle = '#f87171';
            cliffCtx.fillText('CLIFF', x + 6, y + cellH / 2 + 3);
          } else {
            // Draw best action arrow
            const maxVal = Math.max(...Q[r][c]);
            if (maxVal !== 0) {
              const bestAct = Q[r][c].indexOf(maxVal);
              const arrows = ['↑', '→', '↓', '←'];
              cliffCtx.fillStyle = 'rgba(255, 255, 255, 0.6)';
              cliffCtx.font = '14px sans-serif';
              cliffCtx.fillText(arrows[bestAct], x + cellW / 2 - 5, y + cellH / 2 + 5);
            }
          }
        }
      }

      // Draw Agent
      const ax = agentState.c * cellW + cellW / 2;
      const ay = agentState.r * cellH + cellH / 2;
      cliffCtx.beginPath();
      cliffCtx.arc(ax, ay, 10, 0, Math.PI * 2);
      cliffCtx.fillStyle = '#38bdf8';
      cliffCtx.shadowColor = '#38bdf8';
      cliffCtx.shadowBlur = 12;
      cliffCtx.fill();
      cliffCtx.shadowBlur = 0;
    }

    function toggleArenaTraining() {
      isRunning = !isRunning;
      const btn = document.getElementById('btn-toggle-run');
      const txt = document.getElementById('txt-run-btn');
      if (isRunning) {
        txt.innerText = 'Pause Training';
        const speed = parseInt(document.getElementById('slider-speed').value);
        const delay = Math.max(5, 120 - speed);
        runInterval = setInterval(arenaStep, delay);
      } else {
        txt.innerText = 'Start Training';
        clearInterval(runInterval);
      }
    }

    function stepArenaOne() {
      if (isRunning) toggleArenaTraining();
      arenaStep();
    }

    function resetArenaEnv() {
      if (isRunning) toggleArenaTraining();
      agentState = { r: 3, c: 0 };
      episodesCount = 0;
      currentEpisodeReward = 0;
      totalFalls = 0;
      rewardHistory = [];
      Q = Array.from({ length: ROWS }, () =>
        Array.from({ length: COLS }, () => [0, 0, 0, 0])
      );
      updateArenaStats();
      updateArenaChart();
      drawCliffGrid();
    }

    function onAlgoChange() {
      arenaAlgo = document.getElementById('arena-algo-select').value;
      resetArenaEnv();
    }

    function updateArenaHyperparams() {
      alpha = parseFloat(document.getElementById('slider-alpha').value);
      epsilon = parseFloat(document.getElementById('slider-eps').value);
      document.getElementById('val-alpha').innerText = alpha.toFixed(2);
      document.getElementById('val-eps').innerText = epsilon.toFixed(2);
      if (isRunning) {
        clearInterval(runInterval);
        const speed = parseInt(document.getElementById('slider-speed').value);
        runInterval = setInterval(arenaStep, Math.max(5, 120 - speed));
      }
    }

    function updateArenaStats() {
      document.getElementById('stat-episodes').innerText = episodesCount;
      document.getElementById('stat-reward').innerText = currentEpisodeReward;
      document.getElementById('stat-falls').innerText = totalFalls;
    }

    // Chart.js init for arena
    let arenaChart;
    function initArenaChart() {
      const ctx = document.getElementById('arena-chart').getContext('2d');
      arenaChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: 'Episode Return',
            data: [],
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { display: false },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
            }
          }
        }
      });
    }

    function updateArenaChart() {
      if (!arenaChart) return;
      arenaChart.data.labels = rewardHistory.map((_, i) => i + 1);
      arenaChart.data.datasets[0].data = rewardHistory;
      arenaChart.update('none');
    }

    /* -------------------------------------------------------------
       3. DQN REPLAY BUFFER SIMULATION CANVAS
       ------------------------------------------------------------- */
    const dqnCanvas = document.getElementById('dqn-replay-canvas');
    const dqnCtx = dqnCanvas.getContext('2d');
    let dqnBufferCount = 42;

    function drawDQNReplay() {
      dqnCtx.clearRect(0, 0, dqnCanvas.width, dqnCanvas.height);
      const slots = 28;
      const slotW = (dqnCanvas.width - 20) / slots;

      for (let i = 0; i < slots; i++) {
        const x = 10 + i * slotW;
        const filled = i < (dqnBufferCount % slots);
        dqnCtx.fillStyle = filled ? 'rgba(56, 189, 248, 0.7)' : 'rgba(255, 255, 255, 0.08)';
        dqnCtx.fillRect(x, 15, slotW - 3, 35);
      }

      // Sampling brackets
      dqnCtx.strokeStyle = '#c084fc';
      dqnCtx.lineWidth = 1.5;
      dqnCtx.strokeRect(10, 10, dqnCanvas.width - 20, 45);

      dqnCtx.font = '10px JetBrains Mono';
      dqnCtx.fillStyle = '#cbd5e1';
      dqnCtx.fillText('Uniform Random Mini-Batch Sampling → SGD Update Target Net', 12, 75);
    }

    function simulateDQNStep() {
      dqnBufferCount += 7;
      const loss = (0.015 + Math.random() * 0.035).toFixed(3);
      document.getElementById('dqn-buffer-status').innerText = `Buffer: ${dqnBufferCount}/1000 items`;
      document.getElementById('dqn-loss-status').innerText = `Bellman MSE Loss: ${loss}`;
      drawDQNReplay();
    }

    /* -------------------------------------------------------------
       4. MCTS VISUALIZER CANVAS
       ------------------------------------------------------------- */
    const mctsCanvas = document.getElementById('mcts-canvas');
    const mctsCtx = mctsCanvas.getContext('2d');
    let mctsIter = 14;

    function drawMCTS() {
      mctsCtx.clearRect(0, 0, mctsCanvas.width, mctsCanvas.height);

      // Root node
      mctsCtx.fillStyle = '#38bdf8';
      mctsCtx.beginPath();
      mctsCtx.arc(200, 20, 10, 0, Math.PI * 2);
      mctsCtx.fill();

      // Child branches
      const childX = [100, 200, 300];
      const childLabels = ['A', 'B', 'C'];
      const childQ = [0.32, 0.74, 0.48];

      childX.forEach((cx, idx) => {
        mctsCtx.strokeStyle = idx === 1 ? '#a855f7' : 'rgba(255, 255, 255, 0.2)';
        mctsCtx.lineWidth = idx === 1 ? 2.5 : 1;
        mctsCtx.beginPath();
        mctsCtx.moveTo(200, 20);
        mctsCtx.lineTo(cx, 60);
        mctsCtx.stroke();

        mctsCtx.fillStyle = idx === 1 ? '#a855f7' : '#475569';
        mctsCtx.beginPath();
        mctsCtx.arc(cx, 60, 8, 0, Math.PI * 2);
        mctsCtx.fill();

        mctsCtx.font = '10px JetBrains Mono';
        mctsCtx.fillStyle = '#e2e8f0';
        mctsCtx.fillText(`${childLabels[idx]} (Q=${childQ[idx]})`, cx - 18, 85);
      });
    }

    function stepMCTS() {
      mctsIter++;
      document.getElementById('mcts-iter-status').innerText = `Simulated Rollouts: ${mctsIter}`;
      drawMCTS();
    }

    function resetMCTS() {
      mctsIter = 1;
      document.getElementById('mcts-iter-status').innerText = `Simulated Rollouts: ${mctsIter}`;
      drawMCTS();
    }

    /* -------------------------------------------------------------
       5. PPO CLIPPED OBJECTIVE CANVAS
       ------------------------------------------------------------- */
    const ppoCanvas = document.getElementById('ppo-canvas');
    const ppoCtx = ppoCanvas.getContext('2d');
    let ppoAdv = 1.5;

    function drawPPO() {
      ppoCtx.clearRect(0, 0, ppoCanvas.width, ppoCanvas.height);
      const eps = 0.2;
      const w = ppoCanvas.width;
      const h = ppoCanvas.height;

      // Draw Axes
      ppoCtx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
      ppoCtx.beginPath();
      ppoCtx.moveTo(20, h - 20);
      ppoCtx.lineTo(w - 20, h - 20); // x axis (ratio r)
      ppoCtx.stroke();

      // Clipping boundaries at 1 - eps (0.8) and 1 + eps (1.2)
      const x1 = w * 0.35;
      const x2 = w * 0.65;

      ppoCtx.fillStyle = 'rgba(16, 185, 129, 0.12)';
      ppoCtx.fillRect(x1, 10, x2 - x1, h - 30);

      // Draw Clipped function curve
      ppoCtx.strokeStyle = '#10b981';
      ppoCtx.lineWidth = 2.5;
      ppoCtx.beginPath();
      if (ppoAdv > 0) {
        ppoCtx.moveTo(20, h - 20);
        ppoCtx.lineTo(x2, 25);
        ppoCtx.lineTo(w - 20, 25); // flat clip ceiling
      } else {
        ppoCtx.moveTo(20, 30);
        ppoCtx.lineTo(x1, 30);
        ppoCtx.lineTo(w - 20, h - 25);
      }
      ppoCtx.stroke();

      ppoCtx.font = '10px JetBrains Mono';
      ppoCtx.fillStyle = '#94a3b8';
      ppoCtx.fillText('r=1-ε (0.8)', x1 - 20, h - 6);
      ppoCtx.fillText('r=1+ε (1.2)', x2 - 20, h - 6);
      ppoCtx.fillStyle = '#34d399';
      ppoCtx.fillText('Clipped L_CLIP Objective', w / 2 - 50, 22);
    }

    function setPPOAdvantage(adv) {
      ppoAdv = adv;
      document.getElementById('ppo-clip-badge').innerText = `Advantage: ${adv > 0 ? '+' : ''}${adv}`;
      drawPPO();
    }

    /* -------------------------------------------------------------
       6. INVERSE REINFORCEMENT LEARNING CANVAS
       ------------------------------------------------------------- */
    const irlCanvas = document.getElementById('irl-canvas');
    const irlCtx = irlCanvas.getContext('2d');

    function drawIRL() {
      irlCtx.clearRect(0, 0, irlCanvas.width, irlCanvas.height);
      const cols = 8;
      const cw = (irlCanvas.width - 20) / cols;

      for (let i = 0; i < cols; i++) {
        const x = 10 + i * cw;
        // Inferred reward gradient
        const rVal = (i / cols);
        irlCtx.fillStyle = `rgba(16, 185, 129, ${0.15 + rVal * 0.7})`;
        irlCtx.fillRect(x, 15, cw - 4, 45);

        irlCtx.font = '9px JetBrains Mono';
        irlCtx.fillStyle = '#cbd5e1';
        irlCtx.fillText(`+${(rVal * 5).toFixed(1)}`, x + 4, 42);
      }

      // Demonstration Path Arc
      irlCtx.strokeStyle = '#f59e0b';
      irlCtx.lineWidth = 2;
      irlCtx.beginPath();
      irlCtx.moveTo(20, 38);
      irlCtx.bezierCurveTo(120, 10, 250, 60, irlCanvas.width - 25, 38);
      irlCtx.stroke();

      irlCtx.font = '10px JetBrains Mono';
      irlCtx.fillStyle = '#f59e0b';
      irlCtx.fillText('Expert Trajectory Demonstration Overlay', 12, 75);
    }

    function runIRLInference() {
      document.getElementById('irl-status').innerText = 'Re-solving LP Dual: Margin Δ = 2.15 (Optimal)';
      drawIRL();
    }

    /* -------------------------------------------------------------
       7. SMART POWER GRID SIMULATION
       ------------------------------------------------------------- */
    const battCanvas = document.getElementById('battery-sim-canvas');
    const battCtx = battCanvas.getContext('2d');
    let battHour = 0;
    let battSoc = 65;
    let battSavings = 428.5;
    let battTimer = null;
    let battRunning = true;

    function stepBattery() {
      battHour = (battHour + 1) % 24;
      const price = 0.10 + 0.25 * Math.sin((battHour - 14) / 4); // peak at 6pm
      const solar = Math.max(0, Math.sin((battHour - 6) / 6)); // solar peak noon

      // Agent policy
      if (solar > 0.5 && battSoc < 95) {
        battSoc += 4; // charge from solar
      } else if (price > 0.22 && battSoc > 20) {
        battSoc -= 5; // discharge during expensive grid hours
        battSavings += 8.2;
      }

      document.getElementById('stat-battery-soc').innerText = `${battSoc}%`;
      document.getElementById('stat-battery-savings').innerText = `$${battSavings.toFixed(2)}`;

      // Render Battery UI
      battCtx.clearRect(0, 0, battCanvas.width, battCanvas.height);

      // Battery Outline
      battCtx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
      battCtx.lineWidth = 2;
      battCtx.strokeRect(30, 40, 160, 90);
      battCtx.fillRect(190, 65, 10, 40); // terminal

      // Battery Liquid Fill
      const fillW = 150 * (battSoc / 100);
      const grad = battCtx.createLinearGradient(35, 0, 185, 0);
      grad.addColorStop(0, '#38bdf8');
      grad.addColorStop(1, '#10b981');
      battCtx.fillStyle = grad;
      battCtx.fillRect(35, 45, fillW, 80);

      // Metrics display
      battCtx.font = '12px JetBrains Mono';
      battCtx.fillStyle = '#ffffff';
      battCtx.fillText(`Battery SoC: ${battSoc}%`, 45, 90);

      battCtx.fillStyle = '#38bdf8';
      battCtx.fillText(`Simulated Hour: ${battHour}:00`, 240, 55);
      battCtx.fillStyle = '#f59e0b';
      battCtx.fillText(`Solar PV: ${(solar * 100).toFixed(0)} kW`, 240, 85);
      battCtx.fillStyle = '#34d399';
      battCtx.fillText(`Grid Tariff: $${Math.max(0.08, price).toFixed(3)}/kWh`, 240, 115);
    }

    function toggleBatterySim() {
      battRunning = !battRunning;
      document.getElementById('btn-battery-sim').innerText = battRunning ? 'Pause Simulation' : 'Resume Simulation';
      if (battRunning) battTimer = setInterval(stepBattery, 300);
      else clearInterval(battTimer);
    }

    function resetBatterySim() {
      battHour = 0;
      battSoc = 60;
      battSavings = 0;
      stepBattery();
    }

    /* -------------------------------------------------------------
       8. AUTONOMOUS ROBOT SIMULATION
       ------------------------------------------------------------- */
    const robotCanvas = document.getElementById('robot-sim-canvas');
    const robotCtx = robotCanvas.getContext('2d');
    let robot = { x: 50, y: 95, heading: 0, speed: 2 };
    let goal = { x: 480, y: 95 };
    let obstacles = [
      { x: 180, y: 95, r: 24, vy: 1 },
      { x: 320, y: 95, r: 28, vy: -1.2 }
    ];
    let robotGoals = 12;
    let robotHits = 0;
    let robotRunning = true;
    let robotTimer = null;

    function stepRobot() {
      // Dynamic obstacles motion
      obstacles.forEach(ob => {
        ob.y += ob.vy;
        if (ob.y < 40 || ob.y > 150) ob.vy *= -1;
      });

      // Target attraction vector
      const dx = goal.x - robot.x;
      const dy = goal.y - robot.y;
      const targetAngle = Math.atan2(dy, dx);

      // Repulsion from obstacles
      let avoidSteer = 0;
      obstacles.forEach(ob => {
        const odx = ob.x - robot.x;
        const ody = ob.y - robot.y;
        const dist = Math.hypot(odx, ody);
        if (dist < 65) {
          avoidSteer += (ody > 0 ? -1.5 : 1.5) * (1 - dist / 65);
        }
      });

      robot.heading = targetAngle + avoidSteer;
      robot.x += Math.cos(robot.heading) * robot.speed;
      robot.y += Math.sin(robot.heading) * robot.speed;

      // Goal check
      if (Math.hypot(robot.x - goal.x, robot.y - goal.y) < 20) {
        robotGoals++;
        robot.x = 40;
        robot.y = 95;
        document.getElementById('stat-robot-goals').innerText = robotGoals;
      }

      // Render Robot Canvas
      robotCtx.clearRect(0, 0, robotCanvas.width, robotCanvas.height);

      // Obstacles
      obstacles.forEach(ob => {
        robotCtx.fillStyle = 'rgba(239, 68, 68, 0.4)';
        robotCtx.beginPath();
        robotCtx.arc(ob.x, ob.y, ob.r, 0, Math.PI * 2);
        robotCtx.fill();
        robotCtx.strokeStyle = '#ef4444';
        robotCtx.stroke();
      });

      // Goal Beacon
      robotCtx.fillStyle = 'rgba(16, 185, 129, 0.4)';
      robotCtx.beginPath();
      robotCtx.arc(goal.x, goal.y, 16, 0, Math.PI * 2);
      robotCtx.fill();
      robotCtx.fillStyle = '#34d399';
      robotCtx.beginPath();
      robotCtx.arc(goal.x, goal.y, 6, 0, Math.PI * 2);
      robotCtx.fill();

      // LIDAR Rays
      robotCtx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
      for (let a = -0.6; a <= 0.6; a += 0.3) {
        const rayA = robot.heading + a;
        robotCtx.beginPath();
        robotCtx.moveTo(robot.x, robot.y);
        robotCtx.lineTo(robot.x + Math.cos(rayA) * 45, robot.y + Math.sin(rayA) * 45);
        robotCtx.stroke();
      }

      // Robot Body
      robotCtx.fillStyle = '#38bdf8';
      robotCtx.beginPath();
      robotCtx.arc(robot.x, robot.y, 10, 0, Math.PI * 2);
      robotCtx.fill();
    }

    function toggleRobotSim() {
      robotRunning = !robotRunning;
      document.getElementById('btn-robot-sim').innerText = robotRunning ? 'Pause Robot' : 'Resume Robot';
      if (robotRunning) robotTimer = setInterval(stepRobot, 40);
      else clearInterval(robotTimer);
    }

    function relocateRobotGoal() {
      goal.x = 200 + Math.random() * 300;
      goal.y = 40 + Math.random() * 110;
    }

    /* -------------------------------------------------------------
       9. EXAM CALCULATORS & NUMERICAL SOLVERS
       ------------------------------------------------------------- */
    function calculateTD0() {
      const uS = parseFloat(document.getElementById('td-u-s').value);
      const r = parseFloat(document.getElementById('td-r').value);
      const uNext = parseFloat(document.getElementById('td-u-next').value);
      const gamma = parseFloat(document.getElementById('td-gamma').value);
      const alpha = parseFloat(document.getElementById('td-alpha').value);

      const target = r + gamma * uNext;
      const tdError = target - uS;
      const newU = uS + alpha * tdError;

      const resBox = document.getElementById('td-result-content');
      resBox.innerHTML = `
        <strong>Step-by-Step Numerical Derivation:</strong><br>
        1. Target Prediction: $R(s) + \\gamma U(s') = ${r} + (${gamma} \\times ${uNext}) = \\mathbf{${target.toFixed(3)}}$<br>
        2. Temporal-Difference Error $\\delta = ${target.toFixed(3)} - ${uS} = \\mathbf{${tdError >= 0 ? '+' : ''}${tdError.toFixed(3)}}$<br>
        3. Updated Utility: $U(s) \\leftarrow ${uS} + (${alpha} \\times ${tdError.toFixed(3)}) = \\mathbf{${newU.toFixed(3)}}$
      `;
      if (window.renderMathInElement) renderMathInElement(resBox);
    }

    function calculateQLearning() {
      const q = parseFloat(document.getElementById('ql-q').value);
      const r = parseFloat(document.getElementById('ql-r').value);
      const maxNext = parseFloat(document.getElementById('ql-max-next').value);
      const gamma = parseFloat(document.getElementById('ql-gamma').value);
      const alpha = parseFloat(document.getElementById('ql-alpha').value);

      const target = r + gamma * maxNext;
      const diff = target - q;
      const newQ = q + alpha * diff;

      const resBox = document.getElementById('ql-result-content');
      resBox.innerHTML = `
        <strong>Step-by-Step Numerical Derivation:</strong><br>
        1. Bellman Optimality Target: $R + \\gamma \\max_{a'} Q(s',a') = ${r} + (${gamma} \\times ${maxNext}) = \\mathbf{${target.toFixed(3)}}$<br>
        2. Action-Value Error: $Target - Q(s,a) = ${target.toFixed(3)} - ${q} = \\mathbf{${diff >= 0 ? '+' : ''}${diff.toFixed(3)}}$<br>
        3. Updated $Q(s,a) \\leftarrow ${q} + (${alpha} \\times ${diff.toFixed(3)}) = \\mathbf{${newQ.toFixed(3)}}$
      `;
      if (window.renderMathInElement) renderMathInElement(resBox);
    }

    function calculateSARSA() {
      const q = parseFloat(document.getElementById('sarsa-q').value);
      const r = parseFloat(document.getElementById('sarsa-r').value);
      const qNext = parseFloat(document.getElementById('sarsa-q-next').value);
      const gamma = parseFloat(document.getElementById('sarsa-gamma').value);
      const alpha = parseFloat(document.getElementById('sarsa-alpha').value);

      const target = r + gamma * qNext;
      const diff = target - q;
      const newQ = q + alpha * diff;

      const resBox = document.getElementById('sarsa-result-content');
      resBox.innerHTML = `
        <strong>Step-by-Step Numerical Derivation:</strong><br>
        1. On-Policy Target: $R + \\gamma Q(s',a') = ${r} + (${gamma} \\times ${qNext}) = \\mathbf{${target.toFixed(3)}}$<br>
        2. On-Policy Error: $${target.toFixed(3)} - ${q} = \\mathbf{${diff >= 0 ? '+' : ''}${diff.toFixed(3)}}$<br>
        3. Updated $Q(s,a) \\leftarrow ${q} + (${alpha} \\times ${diff.toFixed(3)}) = \\mathbf{${newQ.toFixed(3)}}$
      `;
      if (window.renderMathInElement) renderMathInElement(resBox);
    }

    function calculateReturn() {
      const raw = document.getElementById('ret-seq').value;
      const gamma = parseFloat(document.getElementById('ret-gamma').value);
      const rewards = raw.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

      let total = 0;
      let breakdown = [];
      rewards.forEach((r, idx) => {
        const factor = Math.pow(gamma, idx);
        const term = factor * r;
        total += term;
        breakdown.push(`(${gamma}^${idx} \\times ${r})`);
      });

      const resBox = document.getElementById('ret-result-content');
      resBox.innerHTML = `
        <strong>Trajectory Expansion:</strong><br>
        $$G_0 = ${breakdown.join(' + ')}$$<br>
        <strong>Cumulative Discounted Return:</strong> $\\mathbf{G_0 = ${total.toFixed(4)}}$
      `;
      if (window.renderMathInElement) renderMathInElement(resBox);
    }

    /* -------------------------------------------------------------
       10. TERMINAL SIMULATOR
       ------------------------------------------------------------- */
    function runTerminalCmd(cmd) {
      const term = document.getElementById('term-output');
      if (cmd === 'clear') {
        term.innerHTML = '';
        return;
      }

      const promptDiv = document.createElement('div');
      promptDiv.innerHTML = `<span class="t-prompt">jane@rl-box:~$</span> <span class="t-cmd">${cmd}</span>`;
      term.appendChild(promptDiv);

      const outDiv = document.createElement('div');
      outDiv.style.margin = '4px 0 12px';

      if (cmd.includes('train_agent.py')) {
        outDiv.style.color = '#38bdf8';
        outDiv.innerHTML = `
[PPO-Train] Initializing Gymnasium CartPole-v1...<br>
[PPO-Train] Policy: MlpPolicy (2 hidden layers of 64 units)<br>
-------------------------------------------<br>
| time/total_timesteps | 5000  | ep_rew_mean | 82.4 |<br>
| time/total_timesteps | 10000 | ep_rew_mean | 194.2 |<br>
| time/total_timesteps | 20000 | ep_rew_mean | 500.0 (SOLVED!) |<br>
-------------------------------------------<br>
<span style="color: #34d399;">✓ Model converged. Saved weights to ppo_cartpole_model.zip</span>
        `;
      } else if (cmd.includes('uvicorn')) {
        outDiv.style.color = '#a855f7';
        outDiv.innerHTML = `
INFO: Started server process [PID: 48921]<br>
INFO: Waiting for application startup.<br>
INFO: PyTorch Model weights loaded into CUDA memory.<br>
INFO: Application startup complete.<br>
<span style="color: #34d399;">INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)</span>
        `;
      } else if (cmd.includes('docker-compose')) {
        outDiv.style.color = '#f59e0b';
        outDiv.innerHTML = `
[+] Building 2.4s (8/8) FINISHED<br>
 => [internal] load build definition from Dockerfile<br>
 => => naming to docker.io/library/rl-dashboard-api:latest<br>
[+] Running 2/2<br>
 ✔ Container rl-redis-1 Started<br>
 ✔ Container rl-api-1   Started on port 8000:8000<br>
<span style="color: #34d399;">✓ Production services active and healthy.</span>
        `;
      }

      term.appendChild(outDiv);
      term.scrollTop = term.scrollHeight;
    }

    // Startup initializations
    window.addEventListener('DOMContentLoaded', () => {
      initArenaChart();
      drawCliffGrid();
      drawDQNReplay();
      drawMCTS();
      drawPPO();
      drawIRL();
      battTimer = setInterval(stepBattery, 300);
      robotTimer = setInterval(stepRobot, 40);

      // Render KaTeX across the document
      if (window.renderMathInElement) {
        renderMathInElement(document.body, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ]
        });
      }
    });
  </script>
</body>
</html>
'''

output_path = r"c:\Users\Asus\Downloads\AI-MOD4\index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {output_path} ({len(html_content)} bytes)")
