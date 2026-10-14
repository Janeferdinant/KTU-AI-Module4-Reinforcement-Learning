import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Set up assets directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Load fonts
FONT_DIR = "C:/Windows/Fonts"
try:
    font_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 18)
    font_heading = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 14)
    font_body = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 12)
    font_mono = ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), 12)
    font_mono_sm = ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), 10)
    font_sm = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 10)
except Exception:
    font_title = font_heading = font_body = font_mono = font_mono_sm = font_sm = ImageFont.load_default()

def draw_glass_card(draw, box, fill=(15, 23, 42, 220), outline=(56, 189, 248, 80), radius=10):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=1)

def draw_header(draw, title, subtitle, badge_text, badge_color=(56, 189, 248)):
    # Header badge
    draw.rounded_rectangle([25, 14, 25 + len(badge_text)*7 + 16, 32], radius=4, fill=(15, 23, 42), outline=badge_color, width=1)
    draw.text((33, 17), badge_text, font=font_mono_sm, fill=badge_color)
    draw.text((25 + len(badge_text)*7 + 26, 14), title, font=font_title, fill=(241, 245, 249))
    draw.text((25, 38), subtitle, font=font_sm, fill=(148, 163, 184))

# -------------------------------------------------------------------------
# 1. RL AGENT-ENVIRONMENT CLOSED LOOP ANIMATION
# -------------------------------------------------------------------------
def create_rl_loop_gif():
    w, h = 800, 420
    frames = []
    n_frames = 36

    for f in range(n_frames):
        img = Image.new("RGBA", (w, h), (11, 15, 25, 255))
        draw = ImageDraw.Draw(img)

        # Background subtle grid
        for gx in range(0, w, 40):
            draw.line([(gx, 0), (gx, h)], fill=(20, 28, 45, 120), width=1)
        for gy in range(0, h, 40):
            draw.line([(0, gy), (w, gy)], fill=(20, 28, 45, 120), width=1)

        # Header
        draw_header(draw, "Reinforcement Learning Closed-Loop Dynamic", 
                    "Agent-Environment Feedback Cycle & Bellman Bootstrapping", 
                    "MARKOV DECISION PROCESS (MDP)", (56, 189, 248))

        # Pulse phase
        phase = (f / n_frames) * 2 * math.pi
        pulse = 0.5 + 0.5 * math.sin(phase)

        # Left Card: AGENT
        agent_box = [40, 70, 310, 370]
        agent_glow = int(120 + 80 * math.sin(phase))
        draw_glass_card(draw, agent_box, fill=(15, 23, 42, 240), outline=(56, 189, 248, agent_glow), radius=12)
        
        # Agent Title & Icon
        draw.rounded_rectangle([55, 85, 95, 125], radius=8, fill=(14, 165, 233, 40), outline=(56, 189, 248, 200))
        draw.text((63, 93), "AI", font=font_heading, fill=(56, 189, 248))
        draw.text((105, 88), "AGENT SYSTEM", font=font_heading, fill=(241, 245, 249))
        draw.text((105, 108), "Policy pi(a|s) & Value Q(s,a)", font=font_sm, fill=(148, 163, 184))

        # Agent Telemetry
        tele_box = [55, 140, 295, 260]
        draw_glass_card(draw, tele_box, fill=(11, 15, 25, 220), outline=(56, 189, 248, 50), radius=6)
        
        # Simulated states changing over time
        cur_angle = round(-0.15 + 0.3 * math.sin(phase), 3)
        cur_vel = round(1.2 + 0.8 * math.cos(phase), 3)
        td_err = round(0.42 * math.exp(-0.05 * f) * math.cos(phase), 3)
        q_val = round(14.8 + 2.4 * math.sin(phase), 2)

        draw.text((65, 148), "STATE VECTOR s_t:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((65, 164), f"  Angle: {cur_angle:+.3f} rad", font=font_mono, fill=(248, 250, 252))
        draw.text((65, 182), f"  Velocity: {cur_vel:+.3f} m/s", font=font_mono, fill=(248, 250, 252))
        
        draw.text((65, 206), "BELLMAN TD TARGET:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((65, 222), f"  delta: {td_err:+.3f} | Q*(s,a): {q_val}", font=font_mono, fill=(56, 189, 248))
        draw.text((65, 240), "  Loss: L_DQN -> 0.0084 (Grad Desc)", font=font_mono_sm, fill=(74, 222, 128))

        # Action Selector Widget
        draw.text((55, 275), "ACTION PROBABILITIES (Softmax):", font=font_mono_sm, fill=(148, 163, 184))
        actions = ["a0: Steer Left", "a1: Maintain", "a2: Accelerate"]
        probs = [0.15 + 0.1*math.sin(phase), 0.25, 0.60 - 0.1*math.sin(phase)]
        for i, (act, p) in enumerate(zip(actions, probs)):
            y_bar = 295 + i * 22
            draw.text((55, y_bar), act, font=font_sm, fill=(203, 213, 225))
            draw.rounded_rectangle([150, y_bar+2, 290, y_bar+12], radius=3, fill=(30, 41, 59))
            bar_color = (56, 189, 248) if i == 2 else (100, 116, 139)
            draw.rounded_rectangle([150, y_bar+2, 150 + int(140 * p), y_bar+12], radius=3, fill=bar_color)

        # Right Card: ENVIRONMENT
        env_box = [490, 70, 760, 370]
        env_glow = int(120 + 80 * math.cos(phase))
        draw_glass_card(draw, env_box, fill=(15, 23, 42, 240), outline=(168, 85, 247, env_glow), radius=12)

        # Environment Title & Icon
        draw.rounded_rectangle([505, 85, 545, 125], radius=8, fill=(168, 85, 247, 40), outline=(168, 85, 247, 200))
        draw.text((513, 93), "ENV", font=font_heading, fill=(192, 132, 252))
        draw.text((555, 88), "PHYSICAL WORLD", font=font_heading, fill=(241, 245, 249))
        draw.text((555, 108), "Dynamics P(s'|s,a) & Reward R(s,a)", font=font_sm, fill=(148, 163, 184))

        # Environment Telemetry
        env_tele = [505, 140, 745, 260]
        draw_glass_card(draw, env_tele, fill=(11, 15, 25, 220), outline=(168, 85, 247, 50), radius=6)
        
        cur_reward = round(10.0 - abs(cur_angle) * 20.0 + (1.0 if cur_vel > 1.0 else -2.0), 2)
        r_color = (74, 222, 128) if cur_reward >= 0 else (244, 63, 94)

        draw.text((515, 148), "MARKOV TRANSITION LOG:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((515, 164), f"  s_{{t+1}} ~ T(s_{{t+1}} | s_t, a_t)", font=font_mono, fill=(248, 250, 252))
        draw.text((515, 182), f"  Markovian: P(s'|History) = P(s'|s,a)", font=font_mono_sm, fill=(192, 132, 252))
        
        draw.text((515, 206), "SCALAR REWARD SIGNAL r_t:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((515, 222), f"  Reward r: {cur_reward:+.2f} pts", font=font_mono, fill=r_color)
        draw.text((515, 240), f"  Discounted Return G_t: sum(gamma^k r)", font=font_mono_sm, fill=(251, 191, 36))

        # Simulated mini physical world canvas inside Environment
        draw.rounded_rectangle([505, 275, 745, 355], radius=6, fill=(15, 23, 42), outline=(51, 65, 85))
        draw.line([(515, 335), (735, 335)], fill=(71, 85, 105), width=2)
        # Cart pole simulation
        cart_x = int(625 + 60 * math.sin(phase))
        draw.rectangle([cart_x - 20, 320, cart_x + 20, 335], fill=(56, 189, 248))
        pole_len = 45
        pole_end_x = int(cart_x + pole_len * math.sin(cur_angle * 3))
        pole_end_y = int(320 - pole_len * math.cos(cur_angle * 3))
        draw.line([(cart_x, 320), (pole_end_x, pole_end_y)], fill=(244, 63, 94), width=3)
        draw.ellipse([pole_end_x - 4, pole_end_y - 4, pole_end_x + 4, pole_end_y + 4], fill=(251, 191, 36))
        draw.text((515, 280), "CartPole-v1 Gym Sandbox", font=font_mono_sm, fill=(100, 116, 139))

        # ----------------- ARROWS & FLOWING PARTICLES -----------------
        # TOP ARROW: Agent -> Environment (Action a_t)
        arrow_y = 100
        draw.line([(310, arrow_y), (490, arrow_y)], fill=(56, 189, 248, 80), width=3)
        # Flowing particles rightward
        p_offset = (f / n_frames) * 180
        for i in range(4):
            px = 310 + int((p_offset + i * 45) % 180)
            draw.ellipse([px - 4, arrow_y - 4, px + 4, arrow_y + 4], fill=(56, 189, 248, 255))
        # Top Label
        draw.rounded_rectangle([340, arrow_y - 24, 460, arrow_y - 4], radius=4, fill=(15, 23, 42), outline=(56, 189, 248, 180))
        draw.text((352, arrow_y - 20), "Action a_t -->", font=font_mono_sm, fill=(56, 189, 248))

        # BOTTOM ARROW: Environment -> Agent (Reward r & State s_{t+1})
        arrow_y2 = 330
        draw.line([(310, arrow_y2), (490, arrow_y2)], fill=(74, 222, 128, 80), width=3)
        # Flowing particles leftward
        p_offset_left = 180 - ((f / n_frames) * 180)
        for i in range(4):
            px2 = 310 + int((p_offset_left + i * 45) % 180)
            draw.ellipse([px2 - 4, arrow_y2 - 4, px2 + 4, arrow_y2 + 4], fill=(74, 222, 128, 255))
        # Bottom Label
        draw.rounded_rectangle([330, arrow_y2 + 8, 470, arrow_y2 + 28], radius=4, fill=(15, 23, 42), outline=(74, 222, 128, 180))
        draw.text((338, arrow_y2 + 12), "<-- r_{t+1} & s_{t+1}", font=font_mono_sm, fill=(74, 222, 128))

        # Central Formula HUD
        hub_box = [325, 175, 475, 255]
        draw_glass_card(draw, hub_box, fill=(15, 23, 42, 230), outline=(168, 85, 247, 120), radius=8)
        draw.text((345, 185), "BELLMAN EQUATION", font=font_mono_sm, fill=(192, 132, 252))
        draw.text((335, 203), "Q(s,a) = R + gamma*max Q'", font=font_mono_sm, fill=(241, 245, 249))
        draw.text((340, 225), "Gradient Backprop Active", font=font_mono_sm, fill=(56, 189, 248))

        # Footer Credit
        draw.text((30, 395), "KTU S5 AI Module 4: Reinforcement Learning | System Architecture", font=font_sm, fill=(100, 116, 139))
        draw.text((630, 395), "Author: Jane Rose (Janeferdinant)", font=font_mono_sm, fill=(56, 189, 248))

        frames.append(img.convert("RGB"))

    out_path = os.path.join(ASSETS_DIR, "rl_agent_loop.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
    print(f"Created {out_path} ({os.path.getsize(out_path)} bytes)")

# -------------------------------------------------------------------------
# 2. CLIFF WALKING ARENA: Q-LEARNING VS SARSA ANIMATION
# -------------------------------------------------------------------------
def create_cliff_walking_gif():
    w, h = 800, 420
    frames = []
    n_frames = 40

    # Grid: 4 rows x 12 cols
    # Row 3 is bottom (cliff), row 0 is top (perimeter)
    # Q-Learning path: (3,0) -> (2,0) -> (2,1..11) -> (3,11) [13 steps]
    # SARSA path: (3,0) -> (2,0) -> (1,0) -> (0,0) -> (0,1..11) -> (1,11) -> (2,11) -> (3,11) [17 steps]
    
    q_path = [(3, 0), (2, 0)] + [(2, c) for c in range(1, 12)] + [(3, 11)]
    sarsa_path = [(3, 0), (2, 0), (1, 0), (0, 0)] + [(0, c) for c in range(1, 12)] + [(1, 11), (2, 11), (3, 11)]

    for f in range(n_frames):
        img = Image.new("RGBA", (w, h), (11, 15, 25, 255))
        draw = ImageDraw.Draw(img)

        # Header
        draw_header(draw, "Cliff Walking Arena: Q-Learning vs. SARSA", 
                    "Off-Policy Greedy Edge Path vs. On-Policy Safe Conservative Policy", 
                    "ACTIVE REINFORCEMENT LEARNING", (244, 63, 94))

        # Grid coordinates
        gx0, gy0 = 40, 75
        cell_w, cell_h = 58, 48

        # Draw Grid
        for r in range(4):
            for c in range(12):
                x1 = gx0 + c * cell_w
                y1 = gy0 + r * cell_h
                x2 = x1 + cell_w - 4
                y2 = y1 + cell_h - 4

                if r == 3 and c == 0:
                    # START
                    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=(14, 165, 233, 50), outline=(56, 189, 248, 200), width=2)
                    draw.text((x1 + 14, y1 + 14), "START", font=font_mono_sm, fill=(56, 189, 248))
                elif r == 3 and c == 11:
                    # GOAL
                    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=(34, 197, 94, 50), outline=(74, 222, 128, 200), width=2)
                    draw.text((x1 + 16, y1 + 14), "GOAL", font=font_mono_sm, fill=(74, 222, 128))
                elif r == 3 and 1 <= c <= 10:
                    # CLIFF
                    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=(225, 29, 72, 60), outline=(244, 63, 94, 150), width=1)
                    # Hazard lines
                    draw.line([(x1+4, y2-4), (x2-4, y1+4)], fill=(244, 63, 94, 80), width=1)
                    draw.text((x1 + 8, y1 + 16), "CLIFF -100", font=font_mono_sm, fill=(251, 113, 133))
                else:
                    # Normal cell
                    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill=(15, 23, 42, 200), outline=(51, 65, 85, 120), width=1)
                    draw.text((x1 + 8, y1 + 6), f"-1", font=font_mono_sm, fill=(71, 85, 105))

        # Agent step positions
        q_idx = min(int((f / (n_frames - 5)) * len(q_path)), len(q_path) - 1)
        s_idx = min(int((f / (n_frames - 5)) * len(sarsa_path)), len(sarsa_path) - 1)

        # Draw Q-Learning trajectory trail (Red/Pink)
        for i in range(q_idx):
            r1, c1 = q_path[i]
            r2, c2 = q_path[i+1]
            p1 = (gx0 + c1 * cell_w + cell_w//2 - 2, gy0 + r1 * cell_h + cell_h//2 - 2)
            p2 = (gx0 + c2 * cell_w + cell_w//2 - 2, gy0 + r2 * cell_h + cell_h//2 - 2)
            draw.line([p1, p2], fill=(244, 63, 94, 160), width=3)

        # Draw SARSA trajectory trail (Cyan/Blue)
        for i in range(s_idx):
            r1, c1 = sarsa_path[i]
            r2, c2 = sarsa_path[i+1]
            p1 = (gx0 + c1 * cell_w + cell_w//2 - 2, gy0 + r1 * cell_h + cell_h//2 - 2)
            p2 = (gx0 + c2 * cell_w + cell_w//2 - 2, gy0 + r2 * cell_h + cell_h//2 - 2)
            draw.line([p1, p2], fill=(56, 189, 248, 160), width=3)

        # Draw Current Q-Learning Agent Avatar
        qr, qc = q_path[q_idx]
        qx = gx0 + qc * cell_w + cell_w//2 - 2
        qy = gy0 + qr * cell_h + cell_h//2 - 2
        draw.ellipse([qx - 11, qy - 11, qx + 11, qy + 11], fill=(244, 63, 94, 230), outline=(255, 255, 255, 255), width=2)
        draw.text((qx - 4, qy - 6), "Q", font=font_mono_sm, fill=(255, 255, 255))

        # Draw Current SARSA Agent Avatar
        sr, sc = sarsa_path[s_idx]
        sx = gx0 + sc * cell_w + cell_w//2 - 2
        sy = gy0 + sr * cell_h + cell_h//2 - 2
        draw.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(56, 189, 248, 230), outline=(255, 255, 255, 255), width=2)
        draw.text((sx - 4, sy - 6), "S", font=font_mono_sm, fill=(255, 255, 255))

        # Comparison Legend & Performance Cards
        card1 = [40, 280, 390, 375]
        draw_glass_card(draw, card1, fill=(15, 23, 42, 230), outline=(244, 63, 94, 120), radius=8)
        draw.ellipse([55, 292, 69, 306], fill=(244, 63, 94))
        draw.text((75, 290), "Q-LEARNING (Off-Policy TD Control)", font=font_heading, fill=(244, 63, 94))
        draw.text((55, 312), "Update: Q(s,a) += a[r + gamma*max Q(s',a') - Q(s,a)]", font=font_mono_sm, fill=(226, 232, 240))
        draw.text((55, 330), "- Behavior: Learns the shortest optimal path (13 steps).", font=font_sm, fill=(148, 163, 184))
        draw.text((55, 348), "- Risk: Hugs cliff edge. High variance under epsilon-greedy.", font=font_sm, fill=(251, 113, 133))

        card2 = [410, 280, 760, 375]
        draw_glass_card(draw, card2, fill=(15, 23, 42, 230), outline=(56, 189, 248, 120), radius=8)
        draw.ellipse([425, 292, 439, 306], fill=(56, 189, 248))
        draw.text((445, 290), "SARSA (On-Policy TD Control)", font=font_heading, fill=(56, 189, 248))
        draw.text((425, 312), "Update: Q(s,a) += a[r + gamma*Q(s',a') - Q(s,a)]", font=font_mono_sm, fill=(226, 232, 240))
        draw.text((425, 330), "- Behavior: Learns conservative safe detour (17 steps).", font=font_sm, fill=(148, 163, 184))
        draw.text((425, 348), "- Safety: Accounts for exploration slips. Zero cliff falls.", font=font_sm, fill=(74, 222, 128))

        # Footer Credit
        draw.text((40, 395), "KTU S5 AI Module 4: Watkins (1989) vs. Rummery & Niranjan (1994)", font=font_sm, fill=(100, 116, 139))
        draw.text((630, 395), "Author: Jane Rose (Janeferdinant)", font=font_mono_sm, fill=(56, 189, 248))

        frames.append(img.convert("RGB"))

    out_path = os.path.join(ASSETS_DIR, "cliff_walking_demo.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)
    print(f"Created {out_path} ({os.path.getsize(out_path)} bytes)")

# -------------------------------------------------------------------------
# 3. DQN REAL-TIME ALGORITHMIC TRADING ANIMATION
# -------------------------------------------------------------------------
def create_trading_agent_gif():
    w, h = 800, 420
    frames = []
    n_frames = 36

    # Base price sequence mimicking crypto/stock market with cyclic swings
    random.seed(42)
    base_prices = []
    p = 64000.0
    for i in range(60):
        p += 280.0 * math.sin(i * 0.28) + 120.0 * math.cos(i * 0.45) + random.uniform(-80, 80)
        base_prices.append(p)

    for f in range(n_frames):
        img = Image.new("RGBA", (w, h), (11, 15, 25, 255))
        draw = ImageDraw.Draw(img)

        # Header
        draw_header(draw, "Deep Q-Learning Real-Time Algorithmic Trading", 
                    "Kaggle BTC/USDT Stream: Autonomous Position Execution & PnL Optimization", 
                    "REAL-TIME FINANCIAL RL", (16, 185, 129))

        # Main Chart Window: [40, 70, 560, 370]
        chart_box = [40, 70, 560, 370]
        draw_glass_card(draw, chart_box, fill=(15, 23, 42, 240), outline=(56, 189, 248, 80), radius=10)

        # Chart Grid
        for y in range(100, 360, 40):
            draw.line([(45, y), (555, y)], fill=(30, 41, 59, 100), width=1)
            # Price label
            price_val = int(66500 - (y - 100) * 12)
            draw.text((48, y - 12), f"${price_val:,}", font=font_mono_sm, fill=(71, 85, 105))

        # Slice of candles visible at frame f
        visible_candles = 22
        start_idx = f % (len(base_prices) - visible_candles)
        candles = base_prices[start_idx : start_idx + visible_candles]

        # Draw Candlesticks
        min_p, max_p = 63200.0, 66800.0
        def p_to_y(price):
            return int(340 - ((price - min_p) / (max_p - min_p)) * 220)

        cw = 18
        candle_points = []
        for i, cp in enumerate(candles):
            cx = 100 + i * (cw + 3)
            # Open, High, Low, Close
            co = cp - (15.0 if i % 2 == 0 else -15.0)
            ch = cp + 65.0
            cl = cp - 65.0
            cc = cp + (25.0 if i % 2 == 0 else -25.0)

            yo, yh, yl, yc = p_to_y(co), p_to_y(ch), p_to_y(cl), p_to_y(cc)
            candle_color = (34, 197, 94) if cc >= co else (244, 63, 94)
            # Wick
            draw.line([(cx, yh), (cx, yl)], fill=candle_color, width=1)
            # Body
            top_y, bot_y = min(yo, yc), max(yo, yc)
            draw.rectangle([cx - cw//2, top_y, cx + cw//2, bot_y], fill=candle_color)
            candle_points.append((cx, yc))

        # Moving Average Line
        if len(candle_points) > 1:
            for i in range(len(candle_points) - 1):
                draw.line([candle_points[i], candle_points[i+1]], fill=(56, 189, 248, 180), width=2)

        # Overlay BUY / SELL Executions at specific frame stages
        cur_action = "HOLD"
        action_color = (148, 163, 184)
        if 8 <= f <= 16:
            cur_action = "BUY EXECUTION"
            action_color = (34, 197, 94)
            # Draw Buy Marker
            bx, by = candle_points[min(12, len(candle_points)-1)]
            draw.polygon([(bx, by + 22), (bx - 7, by + 34), (bx + 7, by + 34)], fill=(34, 197, 94))
            draw.rounded_rectangle([bx - 26, by + 36, bx + 26, by + 50], radius=3, fill=(34, 197, 94), outline=(255, 255, 255))
            draw.text((bx - 16, by + 38), "BUY", font=font_mono_sm, fill=(11, 15, 25))
        elif 24 <= f <= 32:
            cur_action = "SELL EXECUTION"
            action_color = (244, 63, 94)
            # Draw Sell Marker
            sx, sy = candle_points[min(18, len(candle_points)-1)]
            draw.polygon([(sx, sy - 22), (sx - 7, sy - 34), (sx + 7, sy - 34)], fill=(244, 63, 94))
            draw.rounded_rectangle([sx - 26, sy - 50, sx + 26, sy - 36], radius=3, fill=(244, 63, 94), outline=(255, 255, 255))
            draw.text((sx - 18, sy - 48), "SELL", font=font_mono_sm, fill=(255, 255, 255))

        # Right HUD Dashboard [580, 70, 760, 370]
        hud_box = [580, 70, 760, 370]
        draw_glass_card(draw, hud_box, fill=(15, 23, 42, 240), outline=(56, 189, 248, 80), radius=10)

        draw.text((595, 85), "PORTFOLIO HUD", font=font_heading, fill=(241, 245, 249))
        draw.text((595, 105), "BTC/USDT Spot Agent", font=font_sm, fill=(148, 163, 184))

        # PnL Metrics
        draw.rounded_rectangle([595, 130, 745, 180], radius=6, fill=(11, 15, 25), outline=(34, 197, 94, 80))
        draw.text((605, 138), "CUMULATIVE PnL:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((605, 154), "+$28,450.00 (+22.8%)", font=font_mono, fill=(74, 222, 128))

        # Current Agent Action Pill
        draw.rounded_rectangle([595, 195, 745, 235], radius=6, fill=(11, 15, 25), outline=action_color)
        draw.text((605, 202), "CURRENT ACTION:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((605, 217), cur_action, font=font_mono, fill=action_color)

        # Q-Values Bar Graph
        draw.text((595, 250), "Q-VALUES Q(s, a):", font=font_mono_sm, fill=(148, 163, 184))
        q_acts = [("BUY", 0.75 if "BUY" in cur_action else 0.25, (34, 197, 94)),
                  ("HOLD", 0.85 if "HOLD" in cur_action else 0.30, (56, 189, 248)),
                  ("SELL", 0.80 if "SELL" in cur_action else 0.20, (244, 63, 94))]
        for i, (aname, qp, qcol) in enumerate(q_acts):
            ay = 270 + i * 22
            draw.text((595, ay), aname, font=font_mono_sm, fill=(203, 213, 225))
            draw.rounded_rectangle([640, ay+2, 740, ay+12], radius=3, fill=(30, 41, 59))
            draw.rounded_rectangle([640, ay+2, 640 + int(100 * qp), ay+12], radius=3, fill=qcol)

        # Additional KPI
        draw.text((595, 345), "Sharpe: 2.45 | Win: 78.4%", font=font_mono_sm, fill=(192, 132, 252))

        # Footer Credit
        draw.text((40, 395), "KTU S5 AI Module 4: Real-Time DQN Financial Portfolio Optimization", font=font_sm, fill=(100, 116, 139))
        draw.text((630, 395), "Author: Jane Rose (Janeferdinant)", font=font_mono_sm, fill=(56, 189, 248))

        frames.append(img.convert("RGB"))

    out_path = os.path.join(ASSETS_DIR, "trading_agent_live.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)
    print(f"Created {out_path} ({os.path.getsize(out_path)} bytes)")

# -------------------------------------------------------------------------
# 4. 4-WAY ADAPTIVE TRAFFIC SIGNAL CONTROLLER ANIMATION
# -------------------------------------------------------------------------
def create_traffic_control_gif():
    w, h = 800, 420
    frames = []
    n_frames = 36

    for f in range(n_frames):
        img = Image.new("RGBA", (w, h), (11, 15, 25, 255))
        draw = ImageDraw.Draw(img)

        # Header
        draw_header(draw, "Deep RL 4-Way Adaptive Traffic Signal Controller", 
                    "SUMO Simulation: Dynamic Phase Switching Minimizing Intersection Delay", 
                    "AUTONOMOUS INFRASTRUCTURE RL", (251, 191, 36))

        # Intersection Canvas [40, 70, 520, 370]
        sim_box = [40, 70, 520, 370]
        draw_glass_card(draw, sim_box, fill=(15, 23, 42, 240), outline=(56, 189, 248, 80), radius=10)

        # Center of Intersection
        cx, cy = 280, 220
        road_w = 90

        # Draw Roads (Asphalt Gray)
        # Vertical road
        draw.rectangle([cx - road_w//2, 70, cx + road_w//2, 370], fill=(24, 32, 47))
        # Horizontal road
        draw.rectangle([40, cy - road_w//2, 520, cy + road_w//2], fill=(24, 32, 47))
        # Center junction
        draw.rectangle([cx - road_w//2, cy - road_w//2, cx + road_w//2, cy + road_w//2], fill=(30, 41, 59))

        # Road Markings
        # Center yellow lines
        draw.line([(cx, 70), (cx, cy - road_w//2)], fill=(234, 179, 8), width=2)
        draw.line([(cx, cy + road_w//2), (cx, 370)], fill=(234, 179, 8), width=2)
        draw.line([(40, cy), (cx - road_w//2, cy)], fill=(234, 179, 8), width=2)
        draw.line([(cx + road_w//2, cy), (520, cy)], fill=(234, 179, 8), width=2)

        # Stop Lines
        draw.line([(cx - road_w//2, cy - road_w//2), (cx, cy - road_w//2)], fill=(255, 255, 255), width=3)
        draw.line([(cx, cy + road_w//2), (cx + road_w//2, cy + road_w//2)], fill=(255, 255, 255), width=3)
        draw.line([(cx - road_w//2, cy), (cx - road_w//2, cy + road_w//2)], fill=(255, 255, 255), width=3)
        draw.line([(cx + road_w//2, cy - road_w//2), (cx + road_w//2, cy)], fill=(255, 255, 255), width=3)

        # Phase timing:
        # Frames 0-17: North-South GREEN, East-West RED
        # Frames 18-35: East-West GREEN, North-South RED
        is_ns_green = f < 18
        ns_light_col = (34, 197, 94) if is_ns_green else (244, 63, 94)
        ew_light_col = (244, 63, 94) if is_ns_green else (34, 197, 94)

        # Traffic Signal Lights (4 corners of junction)
        # North light
        draw.rounded_rectangle([cx - road_w//2 - 16, cy - road_w//2 - 20, cx - road_w//2 - 4, cy - road_w//2], radius=3, fill=(15, 23, 42), outline=ns_light_col)
        draw.ellipse([cx - road_w//2 - 13, cy - road_w//2 - 15, cx - road_w//2 - 7, cy - road_w//2 - 5], fill=ns_light_col)
        # South light
        draw.rounded_rectangle([cx + road_w//2 + 4, cy + road_w//2, cx + road_w//2 + 16, cy + road_w//2 + 20], radius=3, fill=(15, 23, 42), outline=ns_light_col)
        draw.ellipse([cx + road_w//2 + 7, cy + road_w//2 + 5, cx + road_w//2 + 13, cy + road_w//2 + 15], fill=ns_light_col)
        # East light
        draw.rounded_rectangle([cx + road_w//2, cy - road_w//2 - 20, cx + road_w//2 + 20, cy - road_w//2 - 4], radius=3, fill=(15, 23, 42), outline=ew_light_col)
        draw.ellipse([cx + road_w//2 + 5, cy - road_w//2 - 15, cx + road_w//2 + 15, cy - road_w//2 - 9], fill=ew_light_col)
        # West light
        draw.rounded_rectangle([cx - road_w//2 - 20, cy + road_w//2 + 4, cx - road_w//2 - 4, cy + road_w//2 + 20], radius=3, fill=(15, 23, 42), outline=ew_light_col)
        draw.ellipse([cx - road_w//2 - 15, cy + road_w//2 + 7, cx - road_w//2 - 9, cy + road_w//2 + 17], fill=ew_light_col)

        # Vehicles Animation
        # If NS is green, cars move vertically; EW cars queue
        if is_ns_green:
            # Moving NS cars
            offset_ns = (f % 18) * 16
            draw.rounded_rectangle([cx - 30, 80 + offset_ns, cx - 12, 105 + offset_ns], radius=3, fill=(56, 189, 248))
            draw.rounded_rectangle([cx + 12, 350 - offset_ns, cx + 30, 375 - offset_ns], radius=3, fill=(168, 85, 247))
            # Queuing EW cars
            draw.rounded_rectangle([cx - road_w//2 - 35, cy + 12, cx - road_w//2 - 10, cy + 30], radius=3, fill=(244, 63, 94))
            draw.rounded_rectangle([cx - road_w//2 - 65, cy + 12, cx - road_w//2 - 40, cy + 30], radius=3, fill=(251, 146, 60))
            draw.rounded_rectangle([cx - road_w//2 - 95, cy + 12, cx - road_w//2 - 70, cy + 30], radius=3, fill=(234, 179, 8))
            draw.rounded_rectangle([cx + road_w//2 + 10, cy - 30, cx + road_w//2 + 35, cy - 12], radius=3, fill=(244, 63, 94))
            draw.rounded_rectangle([cx + road_w//2 + 40, cy - 30, cx + road_w//2 + 65, cy - 12], radius=3, fill=(251, 146, 60))
        else:
            # Moving EW cars
            offset_ew = ((f - 18) % 18) * 18
            draw.rounded_rectangle([80 + offset_ew, cy + 12, 105 + offset_ew, cy + 30], radius=3, fill=(34, 197, 94))
            draw.rounded_rectangle([500 - offset_ew, cy - 30, 525 - offset_ew, cy - 12], radius=3, fill=(56, 189, 248))
            # Queuing NS cars
            draw.rounded_rectangle([cx - 30, cy - road_w//2 - 35, cx - 12, cy - road_w//2 - 10], radius=3, fill=(244, 63, 94))
            draw.rounded_rectangle([cx + 12, cy + road_w//2 + 10, cx + 30, cy + road_w//2 + 35], radius=3, fill=(251, 146, 60))

        # Sensor Queue Overlays
        draw.text((50, 80), "RADAR QUEUE SENSOR", font=font_mono_sm, fill=(56, 189, 248))
        draw.text((cx + road_w//2 + 25, 80), "CAM 01: ACTIVE", font=font_mono_sm, fill=(74, 222, 128))

        # Right HUD Panel [540, 70, 760, 370]
        hud_box = [540, 70, 760, 370]
        draw_glass_card(draw, hud_box, fill=(15, 23, 42, 240), outline=(251, 191, 36, 100), radius=10)

        draw.text((555, 85), "TRAFFIC RL CONTROLLER", font=font_heading, fill=(241, 245, 249))
        draw.text((555, 105), "SUMO / CityFlow Environment", font=font_sm, fill=(148, 163, 184))

        # Current Phase
        phase_name = "PHASE 1: N-S GREEN" if is_ns_green else "PHASE 2: E-W GREEN"
        p_col = (34, 197, 94) if is_ns_green else (56, 189, 248)
        draw.rounded_rectangle([555, 130, 745, 175], radius=6, fill=(11, 15, 25), outline=p_col)
        draw.text((565, 138), "ACTIVE SIGNAL PHASE:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((565, 153), phase_name, font=font_mono, fill=p_col)

        # Real-time Metrics
        wait_time = round(48.2 - (f / n_frames) * 36.8, 1)
        queue_len = max(2, int(38 - (f / n_frames) * 34))

        draw.rounded_rectangle([555, 188, 745, 260], radius=6, fill=(11, 15, 25), outline=(51, 65, 85))
        draw.text((565, 196), "TELEMETRY METRICS:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((565, 214), f"Avg Wait: {wait_time}s (-76.4%)", font=font_mono, fill=(74, 222, 128))
        draw.text((565, 234), f"Intersection Queue: {queue_len} cars", font=font_mono, fill=(56, 189, 248))

        # Reward & Efficiency
        draw.text((555, 275), "RL OPTIMIZATION IMPACT:", font=font_mono_sm, fill=(148, 163, 184))
        draw.text((555, 295), "- CO2 Emission: -34.2%", font=font_sm, fill=(74, 222, 128))
        draw.text((555, 315), "- Throughput: +42.8% veh/hr", font=font_sm, fill=(56, 189, 248))
        draw.text((555, 335), "- Fuel Idle Cost: -61.5%", font=font_sm, fill=(251, 191, 36))

        # Footer Credit
        draw.text((40, 395), "KTU S5 AI Module 4: Real-Time Traffic Intersection Optimization", font=font_sm, fill=(100, 116, 139))
        draw.text((630, 395), "Author: Jane Rose (Janeferdinant)", font=font_mono_sm, fill=(56, 189, 248))

        frames.append(img.convert("RGB"))

    out_path = os.path.join(ASSETS_DIR, "traffic_control_live.gif")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)
    print(f"Created {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    print("Generating animated GIFs for KTU S5 AI Module 4...")
    create_rl_loop_gif()
    create_cliff_walking_gif()
    create_trading_agent_gif()
    create_traffic_control_gif()
    print("All animations generated successfully!")
