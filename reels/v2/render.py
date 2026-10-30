import subprocess, sys
from playwright.sync_api import sync_playwright
FPS=30
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file:///home/claude/chart2day-ig-skills/reels/v2/2026-10-30-gold-vs-sensex-race.html"); pg.wait_for_timeout(600)
    total=pg.evaluate("TOTAL"); n=int(total*FPS)
    ff=subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart","-an","2026-10-30-gold-vs-sensex-race-reel.mp4"],stdin=subprocess.PIPE)
    for k in range(n):
        pg.evaluate(f"setT({k/FPS})")
        ff.stdin.write(pg.screenshot(type="jpeg",quality=95))
    ff.stdin.close(); ff.wait(); b.close(); print(n,total)
