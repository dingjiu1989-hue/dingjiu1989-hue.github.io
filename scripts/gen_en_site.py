#!/usr/bin/env python3
"""Generate all English site HTML files from /en/articles.json in one pass."""
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / 'en'
ARTICLES_JSON = EN_DIR / 'articles.json'
TODAY = date.today().isoformat()
BASE = 'https://dingjiu1989-hue.github.io'

BOARD_NAMES = {
    'tech': 'Tech Tutorials',
    'sidehustle': 'Side Hustle',
    'tools': 'Tool Recommendations',
    'ai': 'AI Tutorials',
}

# ═══════════════════════════════════════════════════════════════════════
# Article bodies — original English content
# ═══════════════════════════════════════════════════════════════════════

BODIES = {}

BODIES['git-cheatsheet'] = '''
<p>Git is the backbone of modern software development. This cheat sheet covers every command you'll need in daily work — from basic commits to hairy rebase scenarios.</p>

<h2>Setup & Configuration</h2>
<pre><code>git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --list  # show all settings</code></pre>

<h2>Starting a Repository</h2>
<pre><code>git init                    # create a new repo
git clone &lt;url&gt;             # clone an existing repo
git clone -b &lt;branch&gt; &lt;url&gt; # clone a specific branch</code></pre>

<h2>Staging & Committing</h2>
<pre><code>git status                  # what changed?
git add &lt;file&gt;              # stage a file
git add -p                  # stage interactively (hunks)
git commit -m "message"     # commit staged changes
git commit -am "message"    # add tracked files AND commit
git commit --amend          # fix the last commit message</code></pre>

<h2>Branching</h2>
<pre><code>git branch                  # list local branches
git branch &lt;name&gt;           # create a branch
git checkout &lt;name&gt;         # switch to a branch
git checkout -b &lt;name&gt;      # create AND switch
git switch &lt;name&gt;           # modern way to switch
git switch -c &lt;name&gt;        # modern create + switch
git merge &lt;branch&gt;          # merge branch into current
git branch -d &lt;name&gt;        # delete a branch (safe)
git branch -D &lt;name&gt;        # force delete</code></pre>

<h2>Undoing Things</h2>
<pre><code>git restore &lt;file&gt;          # discard working changes
git restore --staged &lt;file&gt; # unstage a file
git reset --soft HEAD~1     # undo last commit, keep changes staged
git reset --hard HEAD~1     # undo last commit, discard changes (DANGER)
git revert &lt;commit&gt;         # safe undo — creates a new commit
git stash                    # save uncommitted changes
git stash pop                # restore stashed changes</code></pre>

<h2>Remote Repositories</h2>
<pre><code>git remote -v                        # list remotes
git remote add origin &lt;url&gt;          # add a remote
git push origin main                 # push to remote
git push -u origin main              # push and set upstream
git pull origin main                 # fetch + merge
git fetch origin                     # fetch without merging
git push origin --delete &lt;branch&gt;    # delete remote branch</code></pre>

<h2>Log & History</h2>
<pre><code>git log --oneline --graph --all      # pretty history graph
git log -p &lt;file&gt;                    # see changes to a file
git blame &lt;file&gt;                     # who changed what line
git diff                             # unstaged changes
git diff --staged                    # staged changes
git show &lt;commit&gt;                    # details of a commit</code></pre>

<h2>Advanced: Interactive Rebase</h2>
<pre><code>git rebase -i HEAD~3                 # squash/reword last 3 commits
git rebase -i --autosquash           # auto-squash fixup commits
git rebase --continue | --abort | --skip</code></pre>

<h2>Quick Reference Card</h2>
<table>
<tr><th>Task</th><th>Command</th></tr>
<tr><td>Create branch</td><td><code>git checkout -b feature/x</code></td></tr>
<tr><td>Save work</td><td><code>git stash</code></td></tr>
<tr><td>Undo last commit</td><td><code>git reset --soft HEAD~1</code></td></tr>
<tr><td>Discard file changes</td><td><code>git restore file.txt</code></td></tr>
<tr><td>See what you did</td><td><code>git log --oneline -10</code></td></tr>
<tr><td>Sync with remote</td><td><code>git pull --rebase</code></td></tr>
</table>

<p>Bookmark this page. You'll be back.</p>
'''

BODIES['python-tutorial'] = '''
<p>Python is the most approachable programming language in the world — and also one of the most powerful. In this tutorial, you'll go from zero to a working program in 30 minutes.</p>

<h2>Installing Python</h2>
<p>Download from <a href="https://www.python.org/downloads/" target="_blank">python.org</a>. During installation on Windows, check <strong>"Add Python to PATH"</strong>. On macOS, <code>brew install python</code> works too. Verify with:</p>
<pre><code>python3 --version  # should print "Python 3.x.x"</code></pre>

<h2>Your First Program</h2>
<pre><code>print("Hello, world!")</code></pre>
<p>Save as <code>hello.py</code> and run with <code>python3 hello.py</code>. That's it — you're a programmer now.</p>

<h2>Variables and Types</h2>
<pre><code>name = "Alice"           # string
age = 30                 # integer
height = 1.68            # float
is_student = False       # boolean

print(f"{name} is {age} years old")  # f-strings!</code></pre>

<h2>Conditionals</h2>
<pre><code>score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("Need improvement")</code></pre>

<h2>Lists and Loops</h2>
<pre><code>fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits[0])          # "apple"

for fruit in fruits:
    print(fruit.upper())

# List comprehension (Python's superpower)
squares = [x**2 for x in range(10)]
# → [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]</code></pre>

<h2>Dictionaries</h2>
<pre><code>user = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}
print(user["name"])
user["city"] = "New York"  # add a key

for key, value in user.items():
    print(f"{key}: {value}")</code></pre>

<h2>Functions</h2>
<pre><code>def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))               # "Hello, Alice!"
print(greet("Bob", "Howdy"))        # "Howdy, Bob!"</code></pre>

<h2>Working with Files</h2>
<pre><code># Read a file
with open("data.txt", "r") as f:
    content = f.read()

# Write a file
with open("output.txt", "w") as f:
    f.write("Hello, file!")</code></pre>

<h2>Error Handling</h2>
<pre><code>try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")
finally:
    print("This always runs")</code></pre>

<h2>A Complete Mini-Program</h2>
<pre><code>import json

def load_todos():
    try:
        with open("todos.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_todos(todos):
    with open("todos.json", "w") as f:
        json.dump(todos, f, indent=2)

def main():
    todos = load_todos()
    while True:
        cmd = input("add/show/quit: ").lower()
        if cmd == "add":
            todos.append(input("Task: "))
            save_todos(todos)
        elif cmd == "show":
            for i, t in enumerate(todos, 1):
                print(f"{i}. {t}")
        elif cmd == "quit":
            break

main()</code></pre>

<h2>Where to Go Next</h2>
<ul>
<li><strong>Automate the Boring Stuff</strong> — free Python book, perfect for practical learners</li>
<li><strong>Real Python</strong> — excellent tutorials from beginner to advanced</li>
<li><strong>Build something</strong> — a CLI tool, a simple web scraper, a TODO app. Anything.</li>
</ul>
<p>The secret to learning Python: start building things immediately. Don't get stuck in tutorial hell.</p>
'''

BODIES['docker-quickstart'] = '''
<p>Docker lets you package your application with everything it needs into a lightweight container that runs anywhere. No more "it works on my machine." Let's get you from zero to a running container in 30 minutes.</p>

<h2>What Problem Does Docker Solve?</h2>
<p>Before Docker: you install Python 3.11, your teammate uses 3.10, the server runs 3.9. Your app uses PostgreSQL 15, but production is on 14. Dependency hell. Docker wraps your app AND its exact environment into one portable unit — a container.</p>

<h2>Installation</h2>
<p>Download <strong>Docker Desktop</strong> from <a href="https://docker.com/products/docker-desktop" target="_blank">docker.com</a>. It includes Docker Engine, CLI, Docker Compose, and a GUI dashboard. Verify:</p>
<pre><code>docker --version
docker run hello-world   # should print a welcome message</code></pre>

<h2>Core Concepts</h2>
<table>
<tr><th>Concept</th><th>What It Is</th><th>Analogy</th></tr>
<tr><td><strong>Image</strong></td><td>A blueprint — the files, dependencies, and config</td><td>A recipe</td></tr>
<tr><td><strong>Container</strong></td><td>A running instance of an image</td><td>The dish you cooked</td></tr>
<tr><td><strong>Dockerfile</strong></td><td>Instructions to build an image</td><td>The recipe card</td></tr>
<tr><td><strong>Docker Hub</strong></td><td>Public registry of images</td><td>GitHub for container images</td></tr>
<tr><td><strong>Volume</strong></td><td>Persistent storage outside the container</td><td>An external hard drive</td></tr>
</table>

<h2>Your First Container</h2>
<pre><code># Run nginx web server in a container
docker run -d -p 8080:80 --name my-nginx nginx

# Visit http://localhost:8080 — you'll see the nginx welcome page!

# What's running?
docker ps

# Stop it
docker stop my-nginx

# Remove it
docker rm my-nginx</code></pre>

<h2>Writing a Dockerfile</h2>
<p>Create a simple Python app:</p>
<pre><code># app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)</code></pre>

<pre><code># Dockerfile
FROM python:3.12-slim          # start from a Python image
WORKDIR /app                    # set working directory
COPY requirements.txt .         # copy dependency list
RUN pip install -r requirements.txt
COPY . .                        # copy everything else
EXPOSE 5000                     # document what port we use
CMD ["python", "app.py"]        # what to run on start</code></pre>

<pre><code># requirements.txt
flask==3.1.0</code></pre>

<pre><code># Build and run
docker build -t my-python-app .
docker run -d -p 5000:5000 my-python-app</code></pre>

<h2>Essential Commands</h2>
<pre><code>docker ps                  # list running containers
docker ps -a               # list ALL containers
docker images              # list images
docker logs &lt;container&gt;    # view logs
docker exec -it &lt;c&gt; bash   # shell into a running container
docker rm &lt;container&gt;      # remove a container
docker rmi &lt;image&gt;         # remove an image
docker system prune -a     # clean up everything unused</code></pre>

<h2>Docker Compose (Multi-Container Apps)</h2>
<pre><code># docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:</code></pre>
<pre><code>docker compose up -d       # start everything
docker compose down        # stop everything</code></pre>

<h2>Docker vs VM</h2>
<p>Containers share the host OS kernel, so they start in milliseconds and use minimal RAM. VMs each need their own OS, taking gigabytes. For most web apps, Docker is the clear winner.</p>
'''

BODIES['vscode-extensions'] = '''
<p>A freshly installed VS Code is a blank canvas. The right extensions turn it into the most powerful editor on the planet. Here are the 10 you should install first.</p>

<h2>1. GitHub Copilot / Supermaven</h2>
<p>AI code completion that actually works. Copilot understands your project context and suggests entire functions, not just single lines. If you're looking for a free alternative, <strong>Supermaven</strong> is surprisingly good for tab completions. Install at least one — coding without AI assistance in 2026 feels like coding without autocomplete.</p>

<h2>2. GitLens</h2>
<p>Git superpowers inside VS Code. Hover over any line to see who changed it and when. Inline blame annotations, rich commit history, branch comparison, and an interactive rebase UI. It makes the built-in Git support feel like a demo. Free for individual use.</p>

<h2>3. Prettier</h2>
<p>The formatter that ended all formatting arguments. Set it as your default formatter, enable "Format on Save," and never think about indentation or line wrapping again. Supports JavaScript, TypeScript, HTML, CSS, JSON, Markdown, and a dozen more languages.</p>

<h2>4. ESLint</h2>
<p>Catches bugs before they happen. It's not just about style — ESLint flags unused variables, missing await, unreachable code, and security patterns. Pair with Prettier for the ultimate code quality setup.</p>

<h2>5. Error Lens</h2>
<p>Shows errors and warnings inline, right in your code — not in a separate panel. The error message appears next to the offending line, color-coded. It sounds small, but seeing errors immediately as you type changes everything. Once you try it, you can't go back.</p>

<h2>6. Thunder Client</h2>
<p>A lightweight API client built into VS Code's sidebar. Think Postman, but it lives in your editor, doesn't require an account, and is much faster for quick API testing. Supports collections, environments, and scriptless testing.</p>

<h2>7. Dev Containers</h2>
<p>Define your development environment in a Dockerfile or docker-compose.yml, and VS Code runs inside the container. Every team member gets the exact same tools and versions — no more "works on my machine." Essential for projects with complex dependencies.</p>

<h2>8. Better Comments</h2>
<p>Color-codes your comments: orange for TODOs, red for FIXMEs, green for notes, blue for info. It makes important comments visually scannable instead of blending into a sea of gray. Simple idea, outsized impact.</p>

<h2>9. Path Intellisense</h2>
<p>Autocompletes file paths as you type imports and requires. Saves you from the "wait, was it <code>../../components/Button</code> or <code>../components/Button</code>?" dance.</p>

<h2>10. Project Manager</h2>
<p>Fast switching between projects. Save your favorite repos, assign tags, and jump between them with Ctrl+Shift+P → "Project Manager: Open." If you bounce between multiple codebases, this is a lifesaver.</p>

<h2>Bonus: Color Theme</h2>
<p>Pick one good theme and stick with it. <strong>Catppuccin</strong>, <strong>Dracula</strong>, and <strong>One Dark Pro</strong> are community favorites with excellent language coverage. A theme you enjoy looking at for 8 hours a day is worth the 30 seconds to install.</p>
'''

BODIES['chrome-plugins'] = '''
<p>Your browser is where you spend most of your day. These 15 Chrome extensions make it faster, safer, and more productive — broken down by category so you can pick what matters most to you.</p>

<h2>Productivity & Focus</h2>
<table>
<tr><th>Extension</th><th>What It Does</th></tr>
<tr><td><strong>uBlock Origin</strong></td><td>The only ad blocker you need. Lightweight, open source, and blocks trackers too. Uses far less memory than AdBlock Plus.</td></tr>
<tr><td><strong>OneTab</strong></td><td>Converts all your open tabs into a single list. Click to restore individually or all at once. Saves 95% memory when you have 50 tabs open.</td></tr>
<tr><td><strong>Toby</strong></td><td>Visual tab management with drag-and-drop collections. Organize tabs by project and sync across devices.</td></tr>
<tr><td><strong>Momentum</strong></td><td>Replaces new tab with a beautiful background, clock, and a daily focus prompt. Keeps you from getting sucked into the browser black hole.</td></tr>
</table>

<h2>Security & Privacy</h2>
<table>
<tr><th>Extension</th><th>What It Does</th></tr>
<tr><td><strong>Bitwarden</strong></td><td>Free, open-source password manager. Auto-fills logins, generates strong passwords, syncs across all devices. The best free option by a mile.</td></tr>
<tr><td><strong>Privacy Badger</strong></td><td>From the EFF. Automatically learns which trackers to block based on their behavior. No configuration needed — just install and forget.</td></tr>
<tr><td><strong>HTTPS Everywhere</strong></td><td>Automatically switches sites from HTTP to HTTPS when available. Protection against downgrade attacks.</td></tr>
</table>

<h2>Developer Tools</h2>
<table>
<tr><th>Extension</th><th>What It Does</th></tr>
<tr><td><strong>React Developer Tools</strong></td><td>Inspect React component trees, props, state, and hooks. Essential for React debugging.</td></tr>
<tr><td><strong>JSON Formatter</strong></td><td>Auto-formats JSON responses in the browser with syntax highlighting and collapsible trees. Makes reading API responses bearable.</td></tr>
<tr><td><strong>Wappalyzer</strong></td><td>Shows what technologies a website uses — frameworks, analytics, CDNs, CMS. Great for competitive research and tech curiosity.</td></tr>
<tr><td><strong>VisBug</strong></td><td>A visual design debugging tool. Move, resize, and restyle elements directly on the page. Like Firebug for the modern web.</td></tr>
</table>

<h2>Design & Content</h2>
<table>
<tr><th>Extension</th><th>What It Does</th></tr>
<tr><td><strong>ColorZilla</strong></td><td>Eyedropper tool that picks colors from any webpage. Includes a gradient generator and CSS gradient parser.</td></tr>
<tr><td><strong>GoFullPage</strong></td><td>Captures full-page screenshots — scrolling included. Perfect for documenting designs, creating portfolios, or reporting bugs.</td></tr>
<tr><td><strong>WhatFont</strong></td><td>Hover over any text to identify the font family, size, weight, and line height. Saves you from digging into DevTools just to find a font name.</td></tr>
</table>

<h2>The One Extension to Rule Them All</h2>
<p>If you only install one: <strong>uBlock Origin</strong>. It makes the web faster, cleaner, and safer. Everything else is optimization on top of that foundation.</p>
'''

BODIES['editor-comparison-2026'] = '''
<p>The code editor market in 2026 has consolidated around three heavyweights: Microsoft's VS Code, JetBrains' IntelliJ-based IDEs, and the AI-native Cursor. Each takes a fundamentally different approach to helping you write code. Here's how to pick.</p>

<h2>VS Code</h2>
<p><strong>The Swiss Army Knife.</strong> Lightweight, extensible, and free. With 40,000+ extensions, there's almost nothing it can't do — but you need to assemble your own IDE from parts. The remote development features (SSH, containers, WSL) are genuinely best-in-class.</p>
<ul>
<li><strong>Price:</strong> Free (Microsoft)</li>
<li><strong>Best for:</strong> Full-stack web dev, TypeScript/JavaScript, polyglot developers, remote work</li>
<li><strong>Weakness:</strong> Java/C# support isn't as deep as JetBrains. AI features require extensions (Copilot).</li>
</ul>

<h2>JetBrains IDEs (IntelliJ IDEA / WebStorm / PyCharm)</h2>
<p><strong>The Specialist.</strong> Each JetBrains IDE is tailored to a specific language ecosystem, and it shows. Refactoring tools that actually understand your code. A debugger that just works. Database tools built in. The trade-off: heavier, more expensive, and slower to start.</p>
<ul>
<li><strong>Price:</strong> Free (Community) / $169+/year (Professional)</li>
<li><strong>Best for:</strong> Java/Kotlin, C#, PHP, large enterprise codebases, complex refactoring</li>
<li><strong>Weakness:</strong> Heavier resource usage. AI features (JetBrains AI) are decent but not as strong as Cursor or Copilot.</li>
</ul>

<h2>Cursor</h2>
<p><strong>The AI-Native Editor.</strong> A VS Code fork rebuilt from the ground up around AI interaction. Instead of asking AI for code and pasting it in, you describe what you want and Cursor writes it in your codebase — understanding your existing files, types, and patterns. The "Tab to accept" model for multi-line edits is so natural it feels like telepathy.</p>
<ul>
<li><strong>Price:</strong> Free (limited) / $20/mo (Pro)</li>
<li><strong>Best for:</strong> Greenfield projects, rapid prototyping, solo developers, AI-first workflows</li>
<li><strong>Weakness:</strong> Lacks some VS Code extensions. Not ideal for large enterprise projects. AI-generated code still needs careful review.</li>
</ul>

<h2>Head-to-Head Comparison</h2>
<table>
<tr><th>Dimension</th><th>VS Code</th><th>JetBrains</th><th>Cursor</th></tr>
<tr><td>Startup speed</td><td>Fast</td><td>Slow</td><td>Fast</td></tr>
<tr><td>Memory usage</td><td>~300-800MB</td><td>~1-3GB</td><td>~400-900MB</td></tr>
<tr><td>Extension ecosystem</td><td>40,000+</td><td>3,000+</td><td>Most VS Code extensions</td></tr>
<tr><td>AI integration</td><td>Via extensions</td><td>Built-in (decent)</td><td>Core feature (excellent)</td></tr>
<tr><td>Refactoring</td><td>Good</td><td>Excellent</td><td>Good (AI-assisted)</td></tr>
<tr><td>Database tools</td><td>Via extensions</td><td>Built-in</td><td>Via extensions</td></tr>
<tr><td>Best for</td><td>General purpose</td><td>Enterprise/Java</td><td>AI-first workflow</td></tr>
</table>

<h2>My Recommendation</h2>
<p><strong>Start with VS Code</strong> — it's the safest default and costs nothing. If you work primarily with Java, C#, or large enterprise codebases, JetBrains is worth every dollar. If you're an indie dev or early-stage startup, try Cursor — the AI-first approach genuinely makes you faster once you adjust your workflow.</p>
<p>Truth is, many experienced developers use two: JetBrains for deep refactoring sessions, VS Code/Cursor for quick edits and frontend work. Don't be dogmatic — use the right tool for the task.</p>
'''

BODIES['online-tools-2026'] = '''
<p>Not every task needs a full app. Sometimes you just need to convert a file, resize an image, or format some JSON — and you need it done in 10 seconds. These 10 free online tools do exactly that. No signup, no download, no nonsense.</p>

<h2>1. TinyPNG / Squoosh</h2>
<p><strong>Image compression that actually works.</strong> <a href="https://tinypng.com" target="_blank">TinyPNG</a> shrinks PNGs and JPEGs by 50-80% with no visible quality loss by using smart compression algorithms. For more control, <a href="https://squoosh.app" target="_blank">Squoosh</a> (from Google) lets you compare compression codecs side-by-side before downloading. Both are free, browser-based, and require zero registration.</p>

<h2>2. Excalidraw</h2>
<p><strong>The hand-drawn diagram tool.</strong> <a href="https://excalidraw.com" target="_blank">Excalidraw</a> creates diagrams that look hand-drawn — which makes them feel approachable and unfinished in exactly the right way. Perfect for architecture sketches, flowcharts, and wireframes. End-to-end encrypted, collaborative, and open source. Your diagrams are saved as shareable links.</p>

<h2>3. CyberChef</h2>
<p><strong>The "Cyber Swiss Army Knife."</strong> <a href="https://gchq.github.io/CyberChef/" target="_blank">CyberChef</a> lets you chain together 300+ data operations: Base64 decode → decompress → parse JSON → extract fields — all in a drag-and-drop pipeline. Built by GCHQ (yes, the British intelligence agency) and completely open source. It runs entirely in your browser — no data ever leaves your machine.</p>

<h2>4. JSON Crack</h2>
<p><strong>JSON → beautiful visual graph.</strong> Paste any JSON and <a href="https://jsoncrack.com" target="_blank">JSON Crack</a> turns it into an interactive tree or graph visualization. Far easier to understand complex nested structures than reading raw JSON. Free tier is generous, and the VS Code extension integrates it into your editor.</p>

<h2>5. Photopea</h2>
<p><strong>Photoshop in your browser.</strong> <a href="https://photopea.com" target="_blank">Photopea</a> is a near-perfect clone of Photoshop CS6 — layers, filters, blending modes, everything. It opens PSD, Sketch, XD, and GIMP files natively. Free with ads. If you only need Photoshop twice a year, uninstall the Creative Cloud bloat and bookmark Photopea.</p>

<h2>6. Image Color Picker</h2>
<p><strong>Upload → click → get hex code.</strong> Upload any image to <a href="https://imagecolorpicker.com" target="_blank">imagecolorpicker.com</a>, click on a pixel, and get the exact color code in HEX, RGB, and HSL. Also generates a color palette from the image. Faster than opening Photoshop just to sample a color.</p>

<h2>7. Remove.bg</h2>
<p><strong>Remove image backgrounds in 5 seconds.</strong> <a href="https://remove.bg" target="_blank">remove.bg</a> uses AI to cut out subjects from backgrounds. One free HD download per account. For bulk use, the API is reasonably priced. The quality on photos of people is shockingly good.</p>

<h2>8. PDF24 Tools</h2>
<p><strong>Everything PDF.</strong> <a href="https://tools.pdf24.org" target="_blank">PDF24</a> offers 30+ PDF tools: merge, split, compress, convert to/from Word/Excel/PPT, OCR, sign, and protect. Free, no limits, no registration. Runs locally in your browser — your documents never hit their servers. The best PDF toolset on the web, bar none.</p>

<h2>9. CodePen / JSFiddle</h2>
<p><strong>Instant frontend playgrounds.</strong> When you need to test a CSS trick, debug a JavaScript snippet, or share a working demo, these sandboxes let you write HTML/CSS/JS and see results instantly. CodePen is better for sharing/showcasing; JSFiddle is faster for quick tests.</p>

<h2>10. Shields.io</h2>
<p><strong>Badges for your README.</strong> <a href="https://shields.io" target="_blank">shields.io</a> generates those little status badges you see on GitHub repos — build passing, coverage 95%, license MIT, etc. Dynamic badges that update automatically from your CI/CD pipeline. The URL-based API is dead simple once you learn the pattern.</p>
'''

BODIES['free-api-collection'] = '''
<p>A good API can save you weeks of development. These 30 APIs are either completely free or have generous free tiers that cover personal projects and MVPs. Every entry includes a sample request and rate limit info.</p>

<h2>Weather</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>Open-Meteo</strong></td><td>Unlimited</td><td>Weather forecasts, historical data. No API key required. Open source.</td></tr>
<tr><td><strong>OpenWeatherMap</strong></td><td>1,000 calls/day</td><td>Current weather, 5-day forecast, air pollution data.</td></tr>
<tr><td><strong>WeatherAPI</strong></td><td>1M calls/month</td><td>Real-time, forecast, astronomy, sports, timezone. Very generous.</td></tr>
</table>

<pre><code># Open-Meteo example (no API key needed!)
curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"</code></pre>

<h2>AI & Machine Learning</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>OpenAI API</strong></td><td>$5 credit (expires in 3 months)</td><td>GPT-4o, GPT-4o-mini. Enough for thousands of requests.</td></tr>
<tr><td><strong>Claude API</strong></td><td>$5 credit</td><td>Claude Opus/Sonnet/Haiku. Great for long-context tasks.</td></tr>
<tr><td><strong>Hugging Face</strong></td><td>Free tier with rate limits</td><td>Thousands of open models via Inference API. Text, image, audio.</td></tr>
<tr><td><strong>Cohere</strong></td><td>100 calls/min</td><td>Embeddings, text generation, reranking. Good for RAG pipelines.</td></tr>
</table>

<h2>Translation & Text</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>Google Translate (LibreTranslate)</strong></td><td>Self-host = unlimited</td><td>Open-source alternative. Host on a $5 VPS for unlimited translations.</td></tr>
<tr><td><strong>DeepL API</strong></td><td>500,000 chars/month</td><td>Highest quality machine translation. EU-based.</td></tr>
<tr><td><strong>LanguageTool</strong></td><td>Free (self-host)</td><td>Grammar and style checker. Open source.</td></tr>
</table>

<h2>Data & Knowledge</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>REST Countries</strong></td><td>Unlimited</td><td>Data on all countries: flags, currencies, languages, timezones.</td></tr>
<tr><td><strong>OpenLibrary</strong></td><td>Unlimited</td><td>Book data: covers, authors, editions. Internet Archive project.</td></tr>
<tr><td><strong>PokéAPI</strong></td><td>Unlimited</td><td>All Pokémon data. Great for learning how to consume REST APIs.</td></tr>
<tr><td><strong>NASA APIs</strong></td><td>1,000 calls/hour</td><td>APOD (Astronomy Picture of the Day), Mars rover photos, Earth imagery.</td></tr>
</table>

<h2>Images & Media</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>Unsplash API</strong></td><td>50 requests/hour</td><td>High-quality free photos. Attribution required.</td></tr>
<tr><td><strong>Pexels API</strong></td><td>200 requests/hour</td><td>Free stock photos and videos. No attribution required.</td></tr>
<tr><td><strong>ImgBB</strong></td><td>Unlimited (32MB limit)</td><td>Image upload with auto-generated URLs. Great for quick hosting.</td></tr>
</table>

<h2>Dev & Infrastructure</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>GitHub API</strong></td><td>60 requests/hour (unauth)</td><td>Repos, issues, users, gists. Use a token for 5,000/hr.</td></tr>
<tr><td><strong>ipapi</strong></td><td>1,000/day (or 45/min)</td><td>IP geolocation. City-level accuracy on free tier.</td></tr>
<tr><td><strong>ExchangeRate-API</strong></td><td>1,500/month</td><td>Currency conversion rates. Updated daily.</td></tr>
</table>

<h2>Fun & Niche</h2>
<table>
<tr><th>API</th><th>Free Tier</th><th>What You Get</th></tr>
<tr><td><strong>JokeAPI</strong></td><td>Unlimited</td><td>Programming jokes, dark jokes, puns. Filter by category.</td></tr>
<tr><td><strong>Bored API</strong></td><td>Unlimited</td><td>Random activity suggestions. Filter by type and participants.</td></tr>
<tr><td><strong>Dog API</strong></td><td>Unlimited</td><td>Random dog pictures by breed. The internet's most important resource.</td></tr>
</table>

<h2>API Design Tips</h2>
<ul>
<li><strong>Cache aggressively</strong> — Most free APIs have rate limits. Cache responses so you don't hit them unnecessarily.</li>
<li><strong>Use exponential backoff</strong> — When you get a 429 (rate limited), wait and retry with increasing delays.</li>
<li><strong>Keep keys out of your repo</strong> — Use environment variables. Even for free API keys.</li>
<li><strong>Fallback gracefully</strong> — Free APIs can go down. Your app should still work if the dog picture API is having a bad day.</li>
</ul>
'''

BODIES['remote-work'] = '''
<p>Remote work isn't the future anymore — it's the present. But finding quality remote opportunities requires knowing where to look. Here's a curated guide to the platforms that actually deliver.</p>

<h2>General Freelance Platforms</h2>
<table>
<tr><th>Platform</th><th>Best For</th><th>Fee</th><th>Notes</th></tr>
<tr><td><strong>Upwork</strong></td><td>General freelancing</td><td>10%</td><td>Largest marketplace. Can be a race to the bottom if you compete on price. Build a strong profile and niche down.</td></tr>
<tr><td><strong>Fiverr</strong></td><td>Defined services (gigs)</td><td>20%</td><td>You define packages at fixed prices. Works well for design, writing, and quick coding tasks. Less back-and-forth than Upwork.</td></tr>
<tr><td><strong>Toptal</strong></td><td>Elite developers</td><td>Varies</td><td>Claims to accept top 3%. Rigorous screening process, but the rates reflect it. If you pass, you'll work with serious clients.</td></tr>
<tr><td><strong>Freelancer</strong></td><td>Contest-based work</td><td>10%+</td><td>Similar to Upwork but with a contest system. Good for design portfolios.</td></tr>
</table>

<h2>Developer-Specific Platforms</h2>
<table>
<tr><th>Platform</th><th>Best For</th><th>Model</th></tr>
<tr><td><strong>Gun.io</strong></td><td>Senior devs, US-based</td><td>Vetted, direct hire focus</td></tr>
<tr><td><strong>Arc.dev</strong></td><td>Remote dev jobs</td><td>Apply once, companies reach out</td></tr>
<tr><td><strong>Hired.com</strong></td><td>Tech salaries > $100K</td><td>Reverse marketplace — companies apply to you</td></tr>
</table>

<h2>Remote-First Job Boards</h2>
<table>
<tr><th>Site</th><th>Focus</th><th>Frequency</th></tr>
<tr><td><strong>We Work Remotely</strong></td><td>All remote roles</td><td>100+ new listings/week</td></tr>
<tr><td><strong>Remote OK</strong></td><td>Tech-heavy remote jobs</td><td>Aggregated, high volume</td></tr>
<tr><td><strong>Remotive</strong></td><td>Curated remote jobs</td><td>Hand-picked, quality over quantity</td></tr>
<tr><td><strong>JS Remotely</strong></td><td>JavaScript/TypeScript only</td><td>Niche but focused</td></tr>
</table>

<h2>Niche Platforms</h2>
<ul>
<li><strong>YunoJuno</strong> — UK/EU creative and tech freelancers. Good rates, less competition than US platforms.</li>
<li><strong>CodeMentor</strong> — Get paid to do code reviews and mentoring. Lower volume but high hourly rates.</li>
<li><strong>Working Nomads</strong> — Curated remote job newsletter. Subscribe and get filtered jobs in your inbox.</li>
</ul>

<h2>How to Stand Out</h2>
<ol>
<li><strong>Specialize, don't generalize.</strong> "Full-stack developer" is a commodity. "React developer specializing in real-time dashboards" gets hired at 3x the rate.</li>
<li><strong>Build a portfolio piece, not a portfolio.</strong> One impressive project with a live demo and a case study beats ten todo apps.</li>
<li><strong>Start with smaller projects.</strong> Get 3-4 five-star reviews on Upwork before going after larger contracts. Social proof compounds.</li>
<li><strong>Don't compete on price.</strong> Clients who pay the least are the most demanding. Set your rate at a level that filters out bad clients.</li>
</ol>
'''

BODIES['free-images'] = '''
<p>High-quality images make content 94% more engaging — but stock photos add up fast. These sites offer beautiful, royalty-free images you can use for free, even commercially. Most don't even require attribution (though giving credit is a nice gesture).</p>

<h2>The Big Three (Start Here)</h2>
<table>
<tr><th>Site</th><th>Library Size</th><th>License</th><th>Standout Feature</th></tr>
<tr><td><strong>Unsplash</strong></td><td>3M+ images</td><td>Free for commercial use</td><td>Highest quality curation. The go-to for "professional but not stock-photo-y" images.</td></tr>
<tr><td><strong>Pexels</strong></td><td>3M+ images + video</td><td>Free for commercial use</td><td>Includes free stock videos. Strong search with color filtering.</td></tr>
<tr><td><strong>Pixabay</strong></td><td>4.2M+ images, videos, vectors</td><td>Free for commercial use</td><td>Largest library. Includes illustrations and vector graphics. Quality is more variable.</td></tr>
</table>

<h2>Hidden Gems</h2>
<table>
<tr><th>Site</th><th>What Makes It Special</th></tr>
<tr><td><strong>Burst (by Shopify)</strong></td><td>Business and ecommerce focused. Great for product mockups and entrepreneur content.</td></tr>
<tr><td><strong>Kaboompics</strong></td><td>Curated by one photographer. Cohesive aesthetic — every image works with every other. Includes a color palette for each photo.</td></tr>
<tr><td><strong>Stocksnap</strong></td><td>No repeat images from the big sites. Smaller library (~5K) but uniquely curated.</td></tr>
<tr><td><strong>FoodiesFeed</strong></td><td>Thousands of high-res food photos. All shot by professional food photographers. If you blog about food, this is your goldmine.</td></tr>
<tr><td><strong>Gratisography</strong></td><td>Quirky, surreal images you won't find elsewhere. A rabbit wearing sunglasses. A serious businessman with a rubber chicken. For when stock photos feel too stock.</td></tr>
</table>

<h2>Illustrations & Icons</h2>
<table>
<tr><th>Site</th><th>What You Get</th></tr>
<tr><td><strong>unDraw</strong></td><td>Open-source SVG illustrations. Change the color to match your brand with one click. Download as SVG or PNG.</td></tr>
<tr><td><strong>Humaaans</strong></td><td>Mix-and-match illustrations of people. Customize hair, clothing, pose. All free for commercial use.</td></tr>
<tr><td><strong>Feather Icons</strong></td><td>280+ open-source icons designed on a 24x24 grid. Consistent, minimal, beautiful.</td></tr>
</table>

<h2>The Legal Stuff (in Plain English)</h2>
<ul>
<li><strong>"Free for commercial use"</strong> means you can use it on your blog, in products, in ads — without paying.</li>
<li><strong>"No attribution required"</strong> means you don't need to credit the photographer. But if it's convenient, still do — it helps the ecosystem.</li>
<li><strong>Avoid images with recognizable people or brands</strong> — those may need a model or property release even if the photo is free.</li>
<li><strong>Don't resell the images as-is</strong> — that's the one thing the license doesn't allow. Modifying and using in your work is fine.</li>
</ul>
'''

BODIES['prompt-engineering'] = '''
<p>Prompt engineering isn't about memorizing magic phrases — it's about clearly communicating what you want, how you want it, and what context the AI needs. Master these fundamentals and you'll get dramatically better results from any LLM.</p>

<h2>The Five Elements of a Good Prompt</h2>
<p>Every effective prompt has some combination of these five elements:</p>
<ol>
<li><strong>Role</strong> — Who is the AI? "You are a senior software engineer reviewing code for security vulnerabilities."</li>
<li><strong>Task</strong> — What exactly should it do? "Find SQL injection vulnerabilities in the following code."</li>
<li><strong>Context</strong> — What background matters? "This code runs in a Node.js/Express backend with PostgreSQL."</li>
<li><strong>Format</strong> — How should the output look? "List each vulnerability with: location, severity, and fix."</li>
<li><strong>Constraints</strong> — What are the boundaries? "Only flag HIGH or CRITICAL severity issues. Ignore style concerns."</li>
</ol>

<h2>Before/After: The Same Request, Different Results</h2>

<h3>Bad Prompt</h3>
<pre><code>Write a blog post about Docker.</code></pre>
<p><strong>Result:</strong> Generic 200-word overview that reads like a Wikipedia article. Useless.</p>

<h3>Good Prompt</h3>
<pre><code>You are a senior DevOps engineer writing for an audience of junior
developers who have never used containers.

Write a blog post titled "Docker in 30 Minutes: From Zero to First
Container." Use a friendly, conversational tone. Every concept should
include a hands-on code example. Structure it as:

1. What problem Docker solves (1 paragraph)
2. Installation (2 sentences + command)
3. Core concepts (image, container, Dockerfile — with analogies)
4. Your first container (step-by-step walkthrough)
5. Common gotchas (bullet points)

Keep the post under 800 words. Use simple English — if a high school
student wouldn't understand a sentence, rewrite it.</code></pre>
<p><strong>Result:</strong> A focused, practical tutorial that the target audience would actually find useful.</p>

<h2>Key Techniques</h2>

<h3>1. Chain of Thought</h3>
<p>Ask the model to think step by step before answering. This dramatically improves accuracy on reasoning tasks:</p>
<pre><code>Q: A bat and a ball cost $1.10 total. The bat costs $1.00 more than
the ball. How much does the ball cost?

Think through this step by step before giving the final answer.</code></pre>

<h3>2. Few-Shot Prompting</h3>
<p>Show 2-3 examples of what you want:</p>
<pre><code>Convert these sentences to active voice:

Input: The bug was found by the QA team.
Output: The QA team found the bug.

Input: The deployment was completed by the DevOps engineer.
Output: </code></pre>

<h3>3. Iterative Refinement</h3>
<p>Your first prompt rarely produces a perfect result. Use the conversation like a designer briefing a junior:</p>
<ol>
<li>Start broad: "Write a Python script that processes CSV files."</li>
<li>Add constraints: "The CSV has headers. Skip empty lines. Handle FileNotFoundError."</li>
<li>Refine output: "Make the error messages user-friendly. Add a progress bar."</li>
</ol>

<h2>Common Mistakes</h2>
<ul>
<li><strong>Being too vague</strong> — "Write something about AI" tells the model nothing. Be specific about topic, audience, format, and tone.</li>
<li><strong>Asking for too much at once</strong> — A 5,000-word article with 10 sections will be shallow. Ask for one section at a time.</li>
<li><strong>Not providing examples</strong> — When you care about format or style, show 1-2 examples. It's the most efficient way to communicate what you want.</li>
<li><strong>Accepting the first answer</strong> — The first response is a draft. Push back: "Make it more concise" or "That analogy doesn't work — try another one."</li>
</ul>
'''

BODIES['ai-coding'] = '''
<p>AI coding tools have evolved from "impressive demo" to "I can't work without this" in under two years. But there's a wide gap between using AI to autocomplete lines and building a genuine human-AI development workflow. This guide covers the tools and the workflow.</p>

<h2>The Tool Landscape (2026)</h2>
<table>
<tr><th>Tool</th><th>Strengths</th><th>Best For</th><th>Price</th></tr>
<tr><td><strong>GitHub Copilot</strong></td><td>In-editor completions, chat, agents (Copilot Extensions)</td><td>General coding. Best IDE integration.</td><td>$10/mo (Individual)</td></tr>
<tr><td><strong>Cursor</strong></td><td>AI-native editor, Tab multi-line edits, Composer for multi-file changes</td><td>Greenfield projects, rapid prototyping.</td><td>Free / $20/mo</td></tr>
<tr><td><strong>Claude Code</strong></td><td>Terminal-based agent, understands entire repos, runs commands</td><td>Complex refactoring, debugging, PR reviews.</td><td>API usage / $20/mo (Pro)</td></tr>
<tr><td><strong>ChatGPT Code Interpreter</strong></td><td>Data analysis, visualization, file processing</td><td>Data science, CSV/JSON manipulation.</td><td>Free / $20/mo</td></tr>
<tr><td><strong>Continue.dev</strong></td><td>Open-source, bring-your-own-model</td><td>Privacy-focused, custom models.</td><td>Free</td></tr>
</table>

<h2>How to Actually Use AI When Coding</h2>

<h3>1. Use AI for Boilerplate and Repetition</h3>
<p>AI is excellent at generating repetitive code — CRUD endpoints, unit tests, form components, data models. Describe the pattern once, let AI generate the rest. This is where you'll see the biggest time savings.</p>

<h3>2. Use AI to Explore Unfamiliar Codebases</h3>
<p>Point Claude Code at a new repo and ask "What's the authentication flow?" or "Where is error handling for database connections?" AI that can read your whole codebase is dramatically more useful than AI that only sees one file.</p>

<h3>3. Use AI for First Drafts, Not Final Code</h3>
<p>The best workflow: AI writes a first draft → you review and refine → AI writes tests → you verify edge cases. Think of AI as an extremely fast junior developer who never gets tired but sometimes hallucinates.</p>

<h3>4. Don't Use AI for Architecture Decisions</h3>
<p>AI can explain trade-offs between approaches, but it shouldn't make the final call. It doesn't understand your team's dynamics, your users' needs, or your business constraints.</p>

<h2>Common Pitfalls</h2>
<ul>
<li><strong>Trusting AI-generated code without review.</strong> AI makes plausible-looking mistakes. Always understand what the code does before committing.</li>
<li><strong>Letting AI write tests for code it also wrote.</strong> If the AI misunderstood the requirement, the test will encode the same misunderstanding. Write the test yourself for critical business logic.</li>
<li><strong>Pasting entire files into chat.</strong> This is slow and error-prone. Use tools that read your codebase directly (Claude Code, Cursor).</li>
<li><strong>Over-relying on AI as a beginner.</strong> If you're learning, write the code yourself first. Use AI to explain concepts and review your work, not to do the work for you.</li>
</ul>

<h2>Building a Productive Workflow</h2>
<ol>
<li><strong>Plan in plain English.</strong> Describe what you want to build before writing code.</li>
<li><strong>Generate the scaffold.</strong> Let AI create the file structure, boilerplate, and initial implementation.</li>
<li><strong>Review and refine.</strong> Read every line. Refactor anything unclear. Add error handling.</li>
<li><strong>Write tests.</strong> Tests prove the code works and serve as documentation.</li>
<li><strong>Iterate.</strong> Ask AI to add features, fix bugs, or refactor — in small, reviewable steps.</li>
</ol>
'''

BODIES['midjourney-prompts'] = '''
<p>Midjourney v7 produces stunning images, but only if you speak its language. This guide covers the prompt structure that consistently produces professional results, plus battle-tested templates you can copy and adapt.</p>

<h2>Prompt Structure</h2>
<p>A well-formed Midjourney prompt has four parts:</p>
<pre><code>[Subject] + [Style/Medium] + [Lighting/Composition] + [Parameters]

Example:
Portrait of a female cyberpunk character, digital art style by
WLOP and Artgerm, neon lighting with rim light from the side,
cinematic composition --ar 2:3 --stylize 250 --v 7</code></pre>

<h2>The Parameters That Matter</h2>
<table>
<tr><th>Parameter</th><th>What It Does</th><th>Recommendation</th></tr>
<tr><td><code>--ar &lt;w&gt;:&lt;h&gt;</code></td><td>Aspect ratio</td><td>2:3 for portraits, 16:9 for landscapes, 1:1 for social media</td></tr>
<tr><td><code>--stylize &lt;0-1000&gt;</code></td><td>Artistic flair vs prompt accuracy</td><td>100-250 for realistic, 500-750 for artistic</td></tr>
<tr><td><code>--chaos &lt;0-100&gt;</code></td><td>Variation between the 4 images</td><td>0 for consistency, 30-50 for exploration, 80+ for wild ideas</td></tr>
<tr><td><code>--weird &lt;0-3000&gt;</code></td><td>Unconventional/experimental results</td><td>0 for normal, 500+ for creative/abstract</td></tr>
<tr><td><code>--no &lt;element&gt;</code></td><td>Negative prompt</td><td><code>--no text, watermark, signature, blurry</code></td></tr>
</table>

<h2>10 Battle-Tested Prompt Templates</h2>

<h3>1. Professional Portrait</h3>
<pre><code>Portrait of a [age] [gender] [profession], [setting], soft natural
lighting, shot on 85mm f/1.4, shallow depth of field, professional
headshot style --ar 2:3 --stylize 150</code></pre>

<h3>2. Product Photography</h3>
<pre><code>[Product] on a [color] backdrop, product photography style, studio
lighting with soft shadows, clean and minimal, shot with macro lens,
commercial photography --ar 1:1 --stylize 100</code></pre>

<h3>3. Logo Design</h3>
<pre><code>Minimalist logo for [company/type], vector style, flat design,
[specific symbols/elements], [color palette], white background,
suitable for app icon --ar 1:1 --stylize 50</code></pre>

<h3>4. Architectural Visualization</h3>
<pre><code>[Building type] architecture, [style] design, golden hour lighting,
photorealistic 3D render, wide-angle lens, surrounded by [environment],
architectural photography --ar 16:9 --stylize 200</code></pre>

<h3>5. Food Photography</h3>
<pre><code>[Dish name], overhead flat lay, natural window lighting, styled with
[props/herbs], shallow depth of field, food photography, appetizing,
vibrant colors --ar 4:5 --stylize 100</code></pre>

<h3>6. Fantasy Landscape</h3>
<pre><code>Epic fantasy landscape, [specific features], concept art by [artist
reference], atmospheric lighting with god rays, cinematic composition,
8K ultra detailed --ar 16:9 --stylize 500</code></pre>

<h3>7. UI/UX Mockup</h3>
<pre><code>[App type] mobile app design, clean UI, modern minimal interface,
[color scheme], glassmorphism style, Dribbble featured, dark mode,
figma design --ar 9:16 --stylize 80</code></pre>

<h3>8. Character Design</h3>
<pre><code>[Character description], character design sheet, multiple views
(front, side, back), [art style], clean linework, flat colors,
concept art, turnaround reference --ar 16:9 --stylize 200</code></pre>

<h3>9. Isometric Illustration</h3>
<pre><code>Isometric illustration of a [scene/room/building], [color palette],
clean vector style, 3D isometric view, detailed interior, pastel
colors, soft shadows, illustration --ar 1:1 --stylize 150</code></pre>

<h3>10. Cinematic Scene</h3>
<pre><code>[Scene description], cinematic shot, [lighting description], movie
still from [reference director/film], anamorphic lens, film grain,
color graded --ar 21:9 --stylize 300</code></pre>

<h2>Pro Tips</h2>
<ul>
<li><strong>Use artist references sparingly.</strong> One or two references sharpen the style. Three or more create visual chaos.</li>
<li><strong>Describe what you want, not what you don't want.</strong> Use <code>--no</code> for 1-2 things max. Focus on positive description.</li>
<li><strong>Vary one thing at a time.</strong> When experimenting, change one parameter at a time so you know what caused the difference.</li>
<li><strong>Save your best prompts.</strong> Good prompts are assets. Build a personal library organized by category.</li>
</ul>
'''

BODIES['perplexity-guide'] = '''
<p>Perplexity isn't just "Google with AI answers." It's a fundamentally different approach to search — one that synthesizes multiple sources into a coherent answer with inline citations, instead of giving you 10 blue links and calling it a day. Here's how to use it like a power user.</p>

<h2>Perplexity vs Google: When to Use Which</h2>
<table>
<tr><th>Task</th><th>Use Perplexity</th><th>Use Google</th></tr>
<tr><td>Getting a quick answer to a factual question</td><td>✅</td><td>OK</td></tr>
<tr><td>Researching a topic with multiple perspectives</td><td>✅✅</td><td>OK</td></tr>
<tr><td>Finding a specific website or product</td><td>OK</td><td>✅</td></tr>
<tr><td>Shopping for the best price</td><td>OK</td><td>✅</td></tr>
<tr><td>Checking real-time news/sports/weather</td><td>✅</td><td>✅</td></tr>
<tr><td>Deep academic literature review</td><td>✅ with Pro Search</td><td>✅ with Scholar</td></tr>
</table>

<h2>Core Features</h2>

<h3>Pro Search</h3>
<p>The free version uses a quick model that's fine for simple questions. <strong>Pro Search</strong> (Pro plan, $20/mo) does multi-step reasoning: it breaks your question into sub-questions, searches each one, synthesizes the findings, and delivers a comprehensive answer with 20+ citations. For research, competitive analysis, or learning a new topic, it's worth the upgrade.</p>
<pre><code>Pro Search query example:
"What are the key differences between Rust's ownership model and
Go's garbage collection, and which performs better for a real-time
data processing pipeline?"

The AI will:
1. Research Rust ownership model
2. Research Go garbage collection
3. Compare performance characteristics
4. Find real-world benchmarks
5. Synthesize into a structured answer with citations</code></pre>

<h3>Collections</h3>
<p>Collections are your personal research libraries. Create a Collection for each project or topic. All searches within a Collection share context — Perplexity remembers what you've already researched and builds on it. You can also add other people to a Collection for collaborative research.</p>

<h3>Focus</h3>
<p>Focus lets you scope searches to specific sources:</p>
<ul>
<li><strong>Web</strong> — general web search (default)</li>
<li><strong>Academic</strong> — scientific papers and journals only</li>
<li><strong>Writing</strong> — generates without searching (like ChatGPT)</li>
<li><strong>Wolfram Alpha</strong> — computational and mathematical queries</li>
<li><strong>YouTube</strong> — search video transcripts</li>
<li><strong>Reddit</strong> — search Reddit discussions</li>
</ul>

<h3>Pages</h3>
<p>Turn any Perplexity thread into a shareable, well-formatted web page with one click. Great for sharing research findings with your team or publishing a quick report.</p>

<h2>Pro Techniques</h2>
<ul>
<li><strong>Chain your searches.</strong> Search broad → identify key angles → search each angle deeply → synthesize. This is how professional researchers work.</li>
<li><strong>Ask for comparisons.</strong> "Compare X and Y in terms of A, B, and C. Use a table." Perplexity excels at structured comparisons with inline citations.</li>
<li><strong>Set up a daily briefing Collection.</strong> Pin searches like "Latest developments in [your industry] today" and refresh daily. Saves scanning 10 news sites.</li>
<li><strong>Challenge the answer.</strong> "Are there any studies that contradict this?" or "What's the counterargument?" Perplexity will find opposing views.</li>
</ul>
'''

BODIES['chatgpt-plus-worth'] = '''
<p>$20/month for ChatGPT Plus. $200/month for Pro. Free is free. Which one actually makes sense for you? After testing all three tiers extensively, here's the honest breakdown.</p>

<h2>The Tiers at a Glance</h2>
<table>
<tr><th>Feature</th><th>Free</th><th>Plus ($20/mo)</th><th>Pro ($200/mo)</th></tr>
<tr><td>Model</td><td>GPT-4o mini (fast)</td><td>GPT-4o (full), o1</td><td>GPT-4o, o1 Pro, unlimited</td></tr>
<tr><td>Messages (GPT-4o)</td><td>~10/day</td><td>~80/3hrs</td><td>Unlimited</td></tr>
<tr><td>DALL·E images</td><td>2/day</td><td>Unlimited</td><td>Unlimited</td></tr>
<tr><td>Web browsing</td><td>Limited</td><td>✅</td><td>✅</td></tr>
<tr><td>File upload</td><td>Images only</td><td>All file types</td><td>All file types</td></tr>
<tr><td>Code Interpreter</td><td>Limited</td><td>✅</td><td>✅</td></tr>
<tr><td>Voice conversations</td><td>Limited</td><td>✅</td><td>✅</td></tr>
<tr><td>o1 Pro mode</td><td>❌</td><td>❌</td><td>✅ (deep reasoning)</td></tr>
</table>

<h2>Free: Good Enough for Most People</h2>
<p>If you use ChatGPT casually — a few questions here and there, help drafting an email, summarizing a short article — the free tier is genuinely fine. GPT-4o mini is fast and surprisingly capable for everyday tasks. The main limitation is the ~10 GPT-4o messages per day cap, but you can plan around it.</p>
<p><strong>Stay free if:</strong> You're a casual user who asks fewer than 10 serious questions a day.</p>

<h2>Plus: The Sweet Spot</h2>
<p>For $20/month, you get significantly more: real GPT-4o with web browsing, file uploads, DALL·E image generation, and Code Interpreter for data analysis. If you use ChatGPT as part of your daily workflow — writing code, analyzing spreadsheets, creating content — Plus pays for itself in the first hour of the month.</p>
<p><strong>Upgrade to Plus if:</strong></p>
<ul>
<li>You hit the GPT-4o message limit on the free tier more than once a week</li>
<li>You need to upload and analyze documents (PDFs, spreadsheets, code)</li>
<li>You create images for presentations or social media regularly</li>
<li>You use ChatGPT as a coding assistant daily</li>
</ul>

<h2>Pro: Only for Power Users</h2>
<p>$200/month is a serious commitment. The main draws are <strong>unlimited access</strong> (no message caps, no throttling) and <strong>o1 Pro mode</strong> — which runs a deeper reasoning process for complex math, science, and coding problems. Unless you're running ChatGPT all day as a core part of your professional workflow, it's hard to justify.</p>
<p><strong>Upgrade to Pro if:</strong></p>
<ul>
<li>You're a researcher who needs the deepest reasoning on complex problems</li>
<li>You use ChatGPT as your primary coding tool for 6+ hours a day</li>
<li>You run a business where ChatGPT usage directly generates revenue</li>
</ul>

<h2>My Recommendation</h2>
<p>Start free. When you find yourself frustrated by limits, upgrade to Plus. If Plus still isn't enough — and you're earning money from the work ChatGPT helps with — consider Pro. The path is: <strong>Free → Plus (when limited) → Pro (when Plus is a bottleneck)</strong>. Most people will never need Pro.</p>
'''

BODIES['claude-vs-chatgpt'] = '''
<p>2026's AI assistant market is a two-horse race between Claude and ChatGPT. Both are excellent, but they have distinct personalities and strengths. Using the right one for the right task can double your productivity.</p>

<h2>Core Capability Comparison</h2>
<table>
<tr><th>Dimension</th><th>ChatGPT</th><th>Claude</th></tr>
<tr><td>Coding</td><td>Strong — especially code completion and Code Interpreter</td><td>Excellent — long context understands entire codebases</td></tr>
<tr><td>Writing quality</td><td>Good</td><td>Best in class — natural tone, nuanced, rarely sounds AI-generated</td></tr>
<tr><td>Long document analysis</td><td>Decent (128K context)</td><td>Best (200K context, precise citations)</td></tr>
<tr><td>Data analysis</td><td>Strong — Code Interpreter is excellent for spreadsheets</td><td>Good — Artifacts for interactive output</td></tr>
<tr><td>Image generation</td><td>✅ DALL·E 3 built in</td><td>❌ No image generation</td></tr>
<tr><td>Web search</td><td>✅ Built-in browsing</td><td>❌ Not natively supported</td></tr>
<tr><td>Multimodal input</td><td>Image understanding + generation</td><td>Image understanding (no generation)</td></tr>
<tr><td>Speed</td><td>Fast (especially 4o mini)</td><td>Slightly slower but more thorough</td></tr>
<tr><td>Cost (Pro tier)</td><td>Free / Plus $20 / Pro $200</td><td>Free / Pro $20 / Team $25</td></tr>
</table>

<h2>Scenario-by-Scenario Best Pick</h2>

<h3>Writing Code</h3>
<p><strong>Winner: Tie, leaning Claude.</strong> Both are excellent. Claude's advantage is understanding large codebases — feed it your entire repo and it grasps patterns and conventions. ChatGPT's advantage is Code Interpreter for data-heavy coding tasks. For everyday web development, you'll be happy with either. For complex refactoring or code review of a large codebase, Claude pulls ahead.</p>

<h3>Writing Articles / Copy</h3>
<p><strong>Winner: Claude.</strong> Claude's writing is noticeably more natural in English and dramatically better in Chinese. It understands tone, voice, and nuance at a level that makes ChatGPT feel slightly generic. If you're a writer, blogger, or content creator, Claude is the clear choice.</p>

<h3>Reading Papers / Long Documents</h3>
<p><strong>Winner: Claude.</strong> The 200K context window means you can feed Claude an entire book or a stack of research papers, and it will cite specific passages with page numbers. ChatGPT can handle long documents too, but Claude's citation accuracy and ability to cross-reference across a massive context is best-in-class.</p>

<h3>Creating Presentations / Visual Content</h3>
<p><strong>Winner: ChatGPT.</strong> Claude cannot generate images. If you need AI-generated visuals — presentation graphics, social media images, concept art — ChatGPT with DALL·E 3 is your only option between the two. For text-heavy slides, Claude's writing quality helps, but you'll need another tool for the visuals.</p>

<h3>Daily Q&A / Assistant Tasks</h3>
<p><strong>Winner: Tie.</strong> Both handle everyday questions well. Claude's answers tend to be more thoughtful and nuanced. ChatGPT's are faster and more concise. Neither is the wrong choice for quick questions.</p>

<h2>The Optimal Setup</h2>
<p><strong>Dual-wield the free tiers.</strong> Claude Free + ChatGPT Free gives you the best of both worlds at zero cost. Use ChatGPT for image generation, web browsing, and quick answers. Use Claude for deep writing, code review, and document analysis.</p>
<p><strong>If you only pay for one:</strong> Choose based on your primary use case. Writing and research → Claude Pro. Visual content and web-connected tasks → ChatGPT Plus.</p>
<p>The gap between these models is narrowing every quarter. Pick one, learn it deeply, and don't obsess over which is slightly better this week. The time you spend comparing tools is time you could spend building something.</p>
'''

# ═══════════════════════════════════════════════════════════════════════
# HTML generators
# ═══════════════════════════════════════════════════════════════════════

def make_article_html(art, board_id, board_name):
    tags_h = '\n'.join(f'        <span class="tag-cat">{t}</span>' for t in art['tags'])
    pin_h = '<span class="tag-pin">📌 Pinned</span>\n' if art.get('pinned') else ''
    if art.get('hot'):
        tags_h += '\n        <span class="tag-cat" style="background:#fff3cd;color:#856404;">🔥 Hot</span>'

    slug = art['slug']
    cn_url = f'{BASE}/{board_id}/{slug}.html'
    en_url = f'{BASE}/en/{board_id}/{slug}.html'

    return f'''<!DOCTYPE html>
<html lang="en" data-render="related" data-board="{board_id}" data-exclude="{slug}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="/en">
    <title>{art['title']} — SourceHub</title>
    <meta name="description" content="{art['description']}">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="alternate" hreflang="zh-CN" href="{cn_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{art['title']}",
      "description": "{art['description']}",
      "datePublished": "{art['date']}",
      "dateModified": "{art['date']}",
      "author": {{"@type": "Person", "name": "SourceHub"}}
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dingjiu1989-hue.github.io/en/"}},
        {{"@type": "ListItem", "position": 2, "name": "{board_name}", "item": "https://dingjiu1989-hue.github.io/en/{board_id}/"}},
        {{"@type": "ListItem", "position": 3, "name": "{art['title']}"}}
      ]
    }}
    </script>
</head>
<body>
<div id="nav-placeholder"></div>
<main>
  <div class="container article-container">
    <div class="breadcrumb">
      <a href="/en/">Home</a> › <a href="/en/{board_id}/">{board_name}</a> › {art['title']}
    </div>
    <article>
      <div class="article-tags">{pin_h}{tags_h}</div>
      <h1 class="article-title">{art['title']}</h1>
      <div class="article-meta">Published {art['date']} · {art['replies'] * 120} views · {art['replies']} replies</div>
      <div class="article-body">{BODIES[art['slug']].strip()}</div>
    </article>
    <section class="related"><div id="related-posts"></div></section>
  </div>
</main>
<div id="footer-placeholder"></div>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
</body>
</html>'''


def make_homepage(data):
    """Generate /en/index.html"""
    boards = data['boards']
    total_boards = len(boards)
    total_posts = sum(len(b['posts']) for b in boards)
    site = data['site']

    return f'''<!DOCTYPE html>
<html lang="en" data-render="homepage">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="/en">
    <title>{site['name']} — {site['tagline']}</title>
    <meta name="description" content="Forum-style resource library aggregating tech tutorials, side hustle ideas, tool recommendations, and AI guides.">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="alternate" type="application/rss+xml" title="SourceHub RSS" href="/feed.xml">
    <link rel="alternate" hreflang="zh-CN" href="https://dingjiu1989-hue.github.io/">
    <link rel="alternate" hreflang="en" href="https://dingjiu1989-hue.github.io/en/">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "SourceHub",
      "url": "https://dingjiu1989-hue.github.io/en/",
      "description": "{site['tagline']}"
    }}
    </script>
</head>
<body>

<div id="nav-placeholder"></div>

<main>
  <section class="hero">
    <div class="container">
      <h1>📚 Welcome to SourceHub</h1>
      <p>{site['tagline']}</p>
      <div class="hero-stats" id="hero-stats">
        <span class="hero-stat">📂 {total_boards} boards</span>
        <span class="hero-stat">📝 {total_posts} articles</span>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="stats-bar" id="stats-bar">
      <span>📊 Total Posts: {total_posts}</span>
    </div>

    <div id="homepage-boards"></div>
  </div>
</main>

<div id="footer-placeholder"></div>

<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
</body>
</html>'''


def make_category(data, board_id):
    """Generate /en/{board}/index.html"""
    board = next(b for b in data['boards'] if b['id'] == board_id)
    count = len(board['posts'])
    en_url = f'{BASE}/en/{board_id}/'
    cn_url = f'{BASE}/{board_id}/'

    board_titles = {
        'tech': 'Tech Tutorials',
        'sidehustle': 'Side Hustle',
        'tools': 'Tool Recommendations',
        'ai': 'AI Tutorials',
    }
    board_descs = {
        'tech': 'Programming tutorials, developer tools, and productivity guides.',
        'sidehustle': 'Freelancing, remote work, and side income strategies for developers.',
        'tools': 'Curated tool recommendations for productivity, design, and development.',
        'ai': 'AI tools, prompt engineering, and practical guides for working with LLMs.',
    }
    title = board_titles[board_id]

    return f'''<!DOCTYPE html>
<html lang="en" data-render="category" data-board="{board_id}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="/en">
    <title>{title} — SourceHub</title>
    <meta name="description" content="{board_descs[board_id]}">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="alternate" hreflang="zh-CN" href="{cn_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{title}",
      "url": "{en_url}",
      "description": "{board['desc']}"
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dingjiu1989-hue.github.io/en/"}},
        {{"@type": "ListItem", "position": 2, "name": "{title}", "item": "{en_url}"}}
      ]
    }}
    </script>
</head>
<body>

<div id="nav-placeholder"></div>

<main>
  <div class="container">
    <div class="breadcrumb">
      <a href="/en/">Home</a> › {title}
    </div>

    <div class="page-header">
      <div>
        <h2>{board['icon']} {title}</h2>
        <span class="post-count">{board['desc']}（共 {count} 篇）</span>
      </div>
      <select class="sort-select" disabled>
        <option>Sort: Newest ↓</option>
      </select>
    </div>

    <div id="category-posts"></div>
  </div>
</main>

<div id="footer-placeholder"></div>

<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    data = json.loads(ARTICLES_JSON.read_text(encoding='utf-8'))
    created = 0

    # Homepage
    hp = EN_DIR / 'index.html'
    hp.write_text(make_homepage(data), encoding='utf-8')
    created += 1
    print(f'  HTML: {hp}')

    # Category pages
    for board in data['boards']:
        cat_dir = EN_DIR / board['id']
        cat_dir.mkdir(exist_ok=True)
        idx = cat_dir / 'index.html'
        idx.write_text(make_category(data, board['id']), encoding='utf-8')
        created += 1
        print(f'  HTML: {idx}')

    # Article pages
    for board in data['boards']:
        board_name = BOARD_NAMES[board['id']]
        for art in board['posts']:
            slug = art['slug']
            if slug not in BODIES:
                print(f'  WARNING: No body for {slug}, skipping')
                continue
            art_dir = EN_DIR / board['id']
            art_dir.mkdir(exist_ok=True)
            p = art_dir / f'{slug}.html'
            p.write_text(make_article_html(art, board['id'], board_name), encoding='utf-8')
            created += 1
            print(f'  HTML: {p}')

    print(f'\nCreated {created} files.')


if __name__ == '__main__':
    main()
