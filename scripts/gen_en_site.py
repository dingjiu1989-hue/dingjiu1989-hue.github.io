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

BODIES['developer-side-hustles-2026'] = '''
<p>Software developers have an unfair advantage in the side hustle economy. You can build things. Most people can't. Here are 10 developer side hustles that generate real income in 2026, ranked by barrier to entry and earning potential.</p>

<h2>1. Freelance Development</h2>
<p>Platforms like Upwork, Toptal, and Arc connect developers with clients worldwide. Rates for experienced developers range from $50-150/hour. Specialize in one stack (React, Python/Django, or mobile) rather than marketing yourself as a generalist. The freelancers earning the most on these platforms all have deep expertise in a specific niche.</p>

<h2>2. Build a SaaS Product</h2>
<p>Bootstrapped SaaS companies like Carrd, Plausible, and Bunce generate millions in ARR with tiny teams. The playbook: identify a painful problem in a niche you understand, build an MVP in 4-6 weeks, launch on Product Hunt and Hacker News, and charge $10-50/month. The bar is higher than it was in 2020, but solo-founded SaaS businesses are still the highest-leverage side hustle for developers.</p>

<h2>3. Create and Sell Boilerplates</h2>
<p>Developers pay for code that saves them time. ShipFast ($199, Next.js starter) and MarsX ($249, full-stack boilerplate) have both done 7 figures. If you've built a SaaS, you already have a boilerplate — extract the reusable parts, document them well, and list on Gumroad or your own site.</p>

<h2>4. Sell Code Templates and Themes</h2>
<p>The Themeforest and Creative Market ecosystems still generate millions in revenue. But in 2026, the bigger opportunity is selling functional templates: Notion templates for project management, Airtable bases for marketing teams, Tailwind component libraries for frontend developers. These take days to build, not months.</p>

<h2>5. Build and Monetize APIs</h2>
<p>If you can solve a data problem at scale, developers will pay for API access. ScrapingBird ($49/mo, web scraping), Hunter.io ($49/mo, email finding), and Abstract API ($19/mo, IP geolocation) all started as solo projects. The key: pick a narrow data problem, solve it well, and price for developers.</p>

<h2>6. Technical Content Creation</h2>
<p>Developer content is in massive demand. Write tutorials on your blog (monetize with ads and affiliate links), create video courses for Udemy or YouTube, or build a paid newsletter on Substack. Developers who can explain complex topics clearly are rare — and brands pay $500-2,000 for a single sponsored post from a developer with a decent following.</p>

<h2>7. Sell Digital Products on Gumroad</h2>
<p>Ebooks, cheatsheets, and code snippet packs sell surprisingly well. A well-designed Git cheatsheet PDF at $5 sold over 40,000 copies. A Notion template for software architecture at $29 sold 2,000+ copies. The formula: pick a topic developers struggle with, package the solution beautifully, and price between $5-49.</p>

<h2>8. Build a Niche Job Board</h2>
<p>Remote tech jobs, React-specific roles, AI/ML positions — niche job boards can charge $200-400 per listing. Using a WordPress theme or Bubble, you can launch one in a weekend. Traffic takes time to build, but once established, job boards become mostly passive income.</p>

<h2>9. Code Review as a Service</h2>
<p>Companies and solo developers pay for expert code review. Platforms like PullRequest.com and CodeMentor handle matching, but you can also build a personal brand on Twitter/LinkedIn and offer code review subscriptions directly. Senior developers charge $100-300 per review session.</p>

<h2>10. Browser Extensions with Premium Features</h2>
<p>Build a useful Chrome extension, distribute it for free, and charge for premium features. Extensions like VidIQ (YouTube analytics) and Grammarly follow this model. A simple dev tool extension with 10,000 free users converting at 2-3% to a $5/month plan generates $1,000-1,500/month in mostly passive income.</p>

<h2>Which One Should You Start With?</h2>
<table>
<tr><th>If You Want</th><th>Start With</th></tr>
<tr><td>Fastest cash (weeks)</td><td>Freelancing (#1) or Templates (#4)</td></tr>
<tr><td>Passive income (months)</td><td>Digital Products (#7) or APIs (#5)</td></tr>
<tr><td>Long-term wealth (years)</td><td>SaaS (#2) or Job Board (#8)</td></tr>
<tr><td>Build audience + income</td><td>Content Creation (#6)</td></tr>
</table>
<p>Pick one. Ship it in two weeks. The only failed side hustle is the one you never start.</p>
'''

BODIES['affiliate-marketing-developers'] = '''
<p>Most affiliate marketing advice is written for lifestyle bloggers — pick a niche, write 50 product reviews, pray for Google rankings. Developers can do better. Much better. This guide covers the technical approach to affiliate marketing that leverages your coding skills for an unfair advantage.</p>

<h2>Why Developers Have an Edge in Affiliate Marketing</h2>
<p>Affiliate marketing at scale is an engineering problem. It involves: crawling product data, generating comparison pages programmatically, A/B testing conversion rates, tracking clicks and commissions, and automating content updates. These are all tasks that developers can automate while non-technical affiliates do them manually.</p>

<h2>Step 1: Pick a Profitable Niche with Affiliate Programs</h2>
<p>Not all niches pay equally. Here are the affiliate niches where technical skill creates the biggest moat:</p>
<table>
<tr><th>Niche</th><th>Avg Commission</th><th>Cookie Duration</th><th>Why Developers Win</th></tr>
<tr><td>SaaS tools</td><td>20-30% recurring</td><td>30-90 days</td><td>Comparison engines, API integration</td></tr>
<tr><td>Web hosting</td><td>$50-150/sale</td><td>30-90 days</td><td>Performance benchmarks, uptime monitoring</td></tr>
<tr><td>Developer tools</td><td>15-30%</td><td>30-60 days</td><td>Deep product knowledge, code examples</td></tr>
<tr><td>Online courses</td><td>20-50%</td><td>30 days</td><td>Course aggregator automation</td></tr>
<tr><td>APIs & dev services</td><td>15-25% recurring</td><td>30-90 days</td><td>Integration demos, benchmarks</td></tr>
</table>

<h2>Step 2: Build Programmatic Content Sites</h2>
<p>Instead of writing 100 individual product reviews by hand, build a system that generates useful, unique comparison pages programmatically. For example:</p>
<ul>
<li><strong>SaaS comparison engine:</strong> Pull pricing, features, and G2/Capterra ratings via APIs or scraping. Generate comparison tables for every pair of tools.</li>
<li><strong>Hosting benchmarks:</strong> Spin up VPS instances, run speed/uptime tests automatically, and publish results with affiliate links to each host.</li>
<li><strong>Course aggregator:</strong> Aggregate courses from Udemy, Coursera, and Pluralsight with prices, ratings, and your affiliate links.</li>
</ul>
<p>One developer built a hosting comparison site with automated benchmarks that generates $15,000/month in affiliate commissions with near-zero ongoing content costs.</p>

<h2>Step 3: Automate Content Updates</h2>
<p>The biggest problem with traditional affiliate sites is staleness. Prices change. Products get discontinued. Reviews become outdated. Developers can solve this by building automated content refresh pipelines:</p>
<ul>
<li>Cron jobs that check product prices daily and update display</li>
<li>API integrations that pull the latest product features and screenshots</li>
<li>Automated "last updated" date stamps that signal freshness to Google</li>
</ul>

<h2>Step 4: Optimize Conversion with Data</h2>
<p>Non-technical affiliates guess what converts. Developers measure it:</p>
<ul>
<li>A/B test CTA button text, placement, and design</li>
<li>Track which comparison tables drive the most clicks</li>
<li>Use heatmaps to understand where users click and scroll</li>
<li>Analyze conversion funnels per traffic source</li>
</ul>
<p>A 1% improvement in conversion rate on a site making $5,000/month is $50/month in additional recurring income — compounded over years.</p>

<h2>Step 5: Diversify Traffic Beyond Google</h2>
<p>SEO is important but risky (algorithm updates can wipe out your traffic overnight). Developers have additional channels:</p>
<ul>
<li><strong>GitHub README badges:</strong> Build a useful open-source tool, add a README with affiliate links to related paid tools</li>
<li><strong>Stack Overflow answers:</strong> Answer questions thoroughly, link to your in-depth guides with affiliate monetization</li>
<li><strong>API documentation:</strong> Create unofficial SDK docs that include affiliate links to relevant services</li>
<li><strong>VS Code extensions:</strong> Build a free extension, recommend paid tools in the marketplace description</li>
</ul>

<h2>Affiliate Programs to Join First</h2>
<table>
<tr><th>Program</th><th>Commission</th><th>Best For</th></tr>
<tr><td>ShareASale / Impact</td><td>Varies</td><td>General marketplace access</td></tr>
<tr><td>PartnerStack</td><td>20-30% recurring</td><td>SaaS products specifically</td></tr>
<tr><td>Amazon Associates</td><td>1-10%</td><td>Physical products, low commission but high trust</td></tr>
<tr><td>Direct SaaS programs</td><td>20-50%</td><td>Check footer links on SaaS sites for "Affiliates"</td></tr>
</table>

<h2>Common Mistakes</h2>
<ul>
<li><strong>Building content sites with no unique value.</strong> Google's 2024-2026 updates heavily penalize sites that only aggregate without adding original analysis. Your programmatic content must include unique data (benchmarks, comparisons, analysis) that generic AI content can't replicate.</li>
<li><strong>Over-optimizing before traffic.</strong> Ship a useful site with 20-30 pages first. Optimize after you have 1,000+ monthly visitors.</li>
<li><strong>Getting attached to one traffic source.</strong> Diversify to GitHub, YouTube, newsletters, and direct traffic from day one.</li>
</ul>
'''

BODIES['sell-digital-products'] = '''
<p>Selling digital products is the highest-margin business model available to developers. No inventory, no shipping, no customer support at 3 AM. You build once, sell infinitely. This guide covers what to build, how to price it, and where to sell it.</p>

<h2>What Digital Products Can Developers Sell?</h2>

<h3>1. Code Templates and Starter Kits</h3>
<p>Every time you set up a new project, you're doing work someone would pay to skip. Next.js starter with auth + payments + database already configured: $99-199. React Native app template with navigation + push notifications + in-app purchases: $149-249. The best templates solve the "blank canvas" problem — giving developers a working foundation instead of a from-scratch setup.</p>

<h3>2. UI Component Libraries</h3>
<p>Tailwind UI charges $299 for a component library. TailwindUI Kit, Float UI, and Preline have all built businesses selling pre-styled components. You don't need hundreds of components — a focused library of 30-50 polished, accessible, well-documented components in one framework is worth charging for.</p>

<h3>3. Ebooks and Technical Guides</h3>
<p>Don't underestimate written content. "Refactoring UI" by Adam Wathan and Steve Schoger reportedly generated millions. "The Pragmatic Programmer" is a textbook example. Ebooks work best when they solve one specific, painful problem: "Deploying Machine Learning Models in Production" or "Passing the AWS Solutions Architect Exam in 30 Days."</p>

<h3>4. Cheatsheets and Quick References</h3>
<p>A well-designed, printable cheatsheet for Git, Docker, or SQL commands at $5-15 sells surprisingly well. Developers buy them as desk references, onboarding materials for new team members, and study aids. Design quality matters — a beautiful, well-organized cheatsheet sells 10x more than a text-heavy list.</p>

<h3>5. Notion Templates for Developers</h3>
<p>Notion's marketplace has created a new category of digital product. Software architecture documentation templates, sprint planning dashboards, bug tracking systems, and personal knowledge management setups. These sell for $15-49 and take a few days to build and polish.</p>

<h3>6. Online Courses and Workshops</h3>
<p>Udemy, Skillshare, and Teachable make distribution easy — but they take a 30-50% cut. For maximum margin, host on your own platform using Gumroad or Podia. Developer courses that perform well: "Learn X Framework by Building Y Project" (where X is React, Flutter, or Go, and Y is a real working app).</p>

<h2>How to Price Digital Products</h2>
<table>
<tr><th>Product Type</th><th>Sweet Spot</th><th>Rationale</th></tr>
<tr><td>Cheatsheets / Shorter PDFs</td><td>$5-19</td><td>Impulse purchase territory</td></tr>
<tr><td>Ebooks / Guides</td><td>$29-49</td><td>Comparable to a technical book</td></tr>
<tr><td>Notion / Airtable Templates</td><td>$15-49</td><td>Price to the value of time saved</td></tr>
<tr><td>Code Templates / Starters</td><td>$49-199</td><td>Days or weeks of dev time saved</td></tr>
<tr><td>Component Libraries</td><td>$99-299</td><td>Professional tool pricing</td></tr>
<tr><td>Online Courses</td><td>$49-199</td><td>Compare to Udemy/Pluralsight pricing</td></tr>
</table>

<h2>Where to Sell</h2>
<table>
<tr><th>Platform</th><th>Fees</th><th>Best For</th></tr>
<tr><td>Gumroad</td><td>10%</td><td>Digital everything — ebooks, templates, code</td></tr>
<tr><td>Lemon Squeezy</td><td>5% + 50c</td><td>Developer-focused, handles EU VAT, great API</td></tr>
<tr><td>Notion Marketplace</td><td>0% (for now)</td><td>Notion templates only</td></tr>
<tr><td>ThemeForest</td><td>45-75%</td><td>Website themes and templates (high fees, high traffic)</td></tr>
<tr><td>Your own site + Stripe</td><td>2.9% + 30c</td><td>Maximum margin, requires driving your own traffic</td></tr>
</table>

<h2>The Launch Playbook</h2>
<ol>
<li><strong>Build the product in public.</strong> Tweet your progress, share screenshots, get early feedback. By launch day, you should have 50-100 people who already want to buy it.</li>
<li><strong>Give away a free version or sample.</strong> A free cheatsheet PDF builds an email list. A free chapter of your ebook convinces people the paid version is worth it. A GitHub repo with a basic template brings traffic to your premium version.</li>
<li><strong>Launch on Product Hunt, Hacker News, and relevant subreddits.</strong> Time your launch for Tuesday-Thursday morning US Eastern time. Prepare your launch assets (screenshots, description, first comment) in advance.</li>
<li><strong>Build a reviews page.</strong> Offer free copies to 5-10 developers in exchange for honest testimonials. Display these prominently on your sales page.</li>
<li><strong>Keep marketing.</strong> The launch is day 1, not the finish line. Write guest posts, appear on podcasts, create YouTube tutorials that feature your product. Digital products have a long tail — a product launched today can still sell 3 years later.</li>
</ol>
'''

BODIES['saas-bootstrapping-guide'] = '''
<p>Building a SaaS product as a solo developer is the closest thing to a wealth-generating machine in software. No investors, no co-founders, no office — just you, your code, and customers who pay you every month. Here's the complete roadmap from idea to first paying customer, based on patterns from successful bootstrapped SaaS founders.</p>

<h2>Phase 1: Find the Right Problem (Week 1-2)</h2>

<h3>What Makes a Good Solo SaaS Idea?</h3>
<table>
<tr><th>Criterion</th><th>Why It Matters</th></tr>
<tr><td>Solves a problem you personally have</td><td>You understand the pain deeply and can build the right solution faster</td></tr>
<tr><td>Target market is a niche, not "everyone"</td><td>Easier to market, less competition, higher willingness to pay</td></tr>
<tr><td>Can be built in 4-6 weeks solo</td><td>If it needs a team and 12 months, it's not a bootstrapped MVP</td></tr>
<tr><td>Monthly recurring revenue model</td><td>Predictable income. One-time purchases are harder to sustain</td></tr>
<tr><td>Customers already pay for similar tools</td><td>If nobody pays for a similar solution, there's probably no market</td></tr>
</table>

<h3>Where to Find SaaS Ideas</h3>
<ul>
<li><strong>Your own workflow.</strong> What repetitive task do you automate with a custom script? That script is probably a product.</li>
<li><strong>Freelance client requests.</strong> If 3 clients ask for the same thing, that's a product signal.</li>
<li><strong>Browse "Alternatives to X" queries.</strong> Tools with unhappy users are opportunities.</li>
<li><strong>Indie Hackers and Hacker News.</strong> See what solo founders are building and look for adjacent problems.</li>
<li><strong>Reddit pain points.</strong> Search for "I wish there was a tool that..." or "frustrated with [tool]"</li>
</ul>

<h2>Phase 2: Validate Before You Build (Week 2-3)</h2>
<p>The #1 mistake: building for 6 months before showing anyone. Instead:</p>
<ol>
<li><strong>Create a landing page</strong> describing the problem and your solution. Use Carrd or a simple HTML page. Include a pricing tier and a "Get Early Access" email signup.</li>
<li><strong>Talk to 10 potential customers.</strong> Not friends or family. Actual people in your target market. Ask: "What do you currently use to solve this problem? What would make you switch?"</li>
<li><strong>Get 50 email signups.</strong> Post your landing page on relevant Reddit communities, Twitter, LinkedIn, and niche forums. If you can't get 50 people to give you their email, you haven't found a painful enough problem.</li>
<li><strong>Pre-sell if possible.</strong> Offer a 50% lifetime discount for the first 20 customers who pay before launch. Pre-sales validate that people will actually open their wallets.</li>
</ol>

<h2>Phase 3: Build the MVP (Week 3-7)</h2>

<h3>Technical Stack Recommendations for Solo SaaS</h3>
<table>
<tr><th>Layer</th><th>Recommended</th><th>Why</th></tr>
<tr><td>Frontend</td><td>Next.js / Remix</td><td>SSR for SEO, rich ecosystem, fast to build</td></tr>
<tr><td>Backend API</td><td>FastAPI (Python) / Hono (Node)</td><td>Lightweight, fast to iterate on</td></tr>
<tr><td>Database</td><td>PostgreSQL (Supabase/Neon)</td><td>Free tier, managed, serverless-friendly</td></tr>
<tr><td>Auth</td><td>Clerk / Supabase Auth / Lucia</td><td>Don't build auth from scratch</td></tr>
<tr><td>Payments</td><td>Stripe + Lemon Squeezy</td><td>Stripe for flexibility, LS for simplicity + tax handling</td></tr>
<tr><td>Hosting</td><td>Vercel / Railway / Fly.io</td><td>Free tier for MVP, scales when needed</td></tr>
<tr><td>Email</td><td>Resend / Loops / Postmark</td><td>Transactional + marketing emails</td></tr>
</table>

<h3>What to Include in the MVP</h3>
<p>Ship the smallest thing someone will pay for:</p>
<ul>
<li>Core feature that solves the main problem (nothing else)</li>
<li>User authentication and account management</li>
<li>Payment integration (Stripe Checkout is fine)</li>
<li>A simple onboarding flow (2-3 steps max)</li>
<li>Basic error messages and loading states</li>
</ul>
<p>Skip: user analytics dashboards, team features, custom domains, white-label, detailed documentation, and anything "nice to have."</p>

<h2>Phase 4: Launch and Get First Customers (Week 7-8)</h2>
<ol>
<li><strong>Launch on Product Hunt.</strong> Even a modest PH launch (50-100 upvotes) brings 500-2,000 visitors and your first paying customers. Prepare thoroughly: a compelling tagline, 5 polished screenshots, a demo video, and an honest first comment from the maker.</li>
<li><strong>Post on Hacker News as a "Show HN".</strong> The HN community values transparency. Share your tech stack, your revenue goal, and what you learned building it. Authentic posts outperform marketing-speak every time.</li>
<li><strong>Write a launch blog post.</strong> "Why I Built X" or "How I Built X in 6 Weeks" — these stories resonate with developers and get shared organically.</li>
<li><strong>Reach out to your pre-launch email list.</strong> These people already expressed interest. Offer them a launch-week discount.</li>
<li><strong>Engage in relevant communities.</strong> Not by spamming your link, but by genuinely helping people and mentioning your tool only when it directly solves their stated problem.</li>
</ol>

<h2>Phase 5: Pricing That Works</h2>
<table>
<tr><th>Tier</th><th>Price</th><th>Purpose</th></tr>
<tr><td>Free</td><td>$0</td><td>Get users in the door. Generous enough to be useful, limited enough to upgrade</td></tr>
<tr><td>Pro</td><td>$15-49/mo</td><td>Your main revenue tier. Where most individual users land</td></tr>
<tr><td>Team/Business</td><td>$49-199/mo</td><td>For companies. Usually 2-5x the Pro price</td></tr>
</table>
<p>Charge monthly by default, offer a 20-30% discount for annual plans. Annual customers have much lower churn — if your monthly churn is 5%, your annual churn on the same product might be only 20-30% (vs. 46% if everyone was monthly).</p>

<h2>Common Bootstrapping Mistakes</h2>
<ul>
<li><strong>Building too much before launching.</strong> Your MVP should feel almost embarrassingly simple. If you're not slightly uncomfortable with how minimal it is, you've built too much.</li>
<li><strong>Pricing too low.</strong> Charge at least $15/month. Anything lower signals "this isn't valuable" and makes customer acquisition costs unsustainable.</li>
<li><strong>Building for yourself, not customers.</strong> Ship based on customer feedback, not what you think is cool. Talk to at least one customer every week.</li>
<li><strong>Giving up too early.</strong> Most successful bootstrapped SaaS products took 12-18 months to reach meaningful revenue. The first 6 months are almost always slow. Keep shipping.</li>
</ul>
'''

BODIES['linux-commands'] = '''
<p>A good Linux command-line reference isn't nice to have — it's essential. This cheatsheet covers 50 commands organized by what you're actually trying to do, from file navigation to process management to networking.</p>

<h2>File Navigation</h2>
<pre><code>pwd                     # print working directory
ls -la                  # list all files with details
cd /path/to/dir         # change directory
cd ..                   # go up one level
cd -                    # go back to previous directory
find . -name "*.py"     # find files by name pattern
locate filename         # find file quickly (uses indexed db)</code></pre>

<h2>File Operations</h2>
<pre><code>cp source dest          # copy file
cp -r source dest       # copy directory recursively
mv source dest          # move or rename
rm file                 # remove file
rm -rf dir              # remove directory (DANGER — no undo)
mkdir -p a/b/c          # create nested directories
touch file              # create empty file or update timestamp
ln -s target link       # create symbolic link</code></pre>

<h2>Viewing and Editing Files</h2>
<pre><code>cat file                # print entire file
less file               # scroll through file (q to quit)
head -20 file           # first 20 lines
tail -f file            # follow file as it grows (logs)
wc -l file              # count lines
grep "pattern" file     # search for pattern
grep -r "pattern" dir   # search recursively
nano file               # simple terminal editor
vim file                # advanced editor (:q! to quit)</code></pre>

<h2>Permissions</h2>
<pre><code>chmod 755 script.sh     # rwxr-xr-x (owner full, others read+execute)
chmod +x script.sh      # make executable
chown user:group file   # change owner and group
umask 022               # set default permissions mask</code></pre>

<h2>Process Management</h2>
<pre><code>ps aux                  # list all running processes
ps aux | grep nginx     # find specific process
top                     # real-time process monitor (q to quit)
htop                    # prettier top (install separately)
kill 1234               # terminate process by PID
kill -9 1234            # force kill (SIGKILL)
pkill -f pattern        # kill by name pattern
bg                      # resume suspended job in background
fg                      # bring background job to foreground
jobs                    # list background jobs</code></pre>

<h2>Disk and Storage</h2>
<pre><code>df -h                   # disk free (human-readable)
du -sh dir              # directory size summary
du -sh * | sort -h      # size of each item, sorted
mount                   # show mounted filesystems
lsblk                   # list block devices</code></pre>

<h2>Networking</h2>
<pre><code>ping host               # test connectivity
curl -I url             # fetch headers only
curl -s url | jq        # fetch JSON and pretty-print
wget url                # download file
ssh user@host           # connect to remote server
scp file user@host:path # copy file to remote
netstat -tlnp           # listening ports
ss -tlnp                # modern alternative to netstat
lsof -i :3000           # what's using port 3000</code></pre>

<h2>Text Processing</h2>
<pre><code>sed 's/old/new/g' file  # replace all occurrences
awk '{{print $1}}' file  # print first column
sort file               # sort lines
sort -u file            # sort and deduplicate
uniq -c file            # count occurrences
cut -d',' -f1 file      # extract column 1 from CSV
tr '[:lower:]' '[:upper:]' # convert case</code></pre>

<h2>Compression and Archives</h2>
<pre><code>tar -czf archive.tar.gz dir   # create gzipped tarball
tar -xzf archive.tar.gz       # extract gzipped tarball
gzip file                     # compress single file
gunzip file.gz                # decompress
zip -r archive.zip dir        # create zip</code></pre>

<h2>System Info</h2>
<pre><code>uname -a                # kernel info
whoami                  # current user
who                     # who is logged in
uptime                  # how long system has been up
free -h                 # memory usage
date                    # current date/time
history                 # command history
!!                      # re-run last command
!$                      # last argument of previous command</code></pre>

<h2>Quick Reference by Task</h2>
<table>
<tr><th>Task</th><th>Command</th></tr>
<tr><td>Find large files</td><td><code>find . -type f -size +100M</code></td></tr>
<tr><td>Search in files</td><td><code>grep -rn "TODO" .</code></td></tr>
<tr><td>Count files in directory</td><td><code>ls -1 | wc -l</code></td></tr>
<tr><td>See disk usage of all mounts</td><td><code>df -h</code></td></tr>
<tr><td>Check if a port is open</td><td><code>nc -zv host 443</code></td></tr>
<tr><td>Watch command output every 2s</td><td><code>watch -n 2 command</code></td></tr>
<tr><td>Create alias permanently</td><td><code>echo 'alias ll="ls -la"' >> ~/.bashrc</code></td></tr>
</table>
'''

BODIES['rest-api-best-practices'] = '''
<p>REST APIs power the modern web, but most APIs are designed with subtle flaws that cause pain months later. This guide covers the conventions, patterns, and anti-patterns that separate production APIs from weekend projects.</p>

<h2>1. Use Nouns, Not Verbs, for Resources</h2>
<pre><code># Good
GET    /users
GET    /users/42
POST   /users
PUT    /users/42
DELETE /users/42

# Bad
GET    /getUsers
POST   /createUser
GET    /users/42/getProfile</code></pre>

<h2>2. Version Your API from Day One</h2>
<p>Use URL prefix versioning (<code>/v1/users</code>) or header-based versioning (<code>Accept: application/vnd.api.v2+json</code>). URL versioning is simpler for public APIs. Choose one and stick with it everywhere — mixing strategies is worse than either alone.</p>

<h2>3. Consistent Naming Conventions</h2>
<pre><code>// JSON: camelCase for properties
{{"userId": 42, "createdAt": "2026-05-07"}}

// URL paths: kebab-case
GET /user-orders/42

// Query parameters: snake_case
GET /users?sort_by=name&page_size=20</code></pre>

<h2>4. Use Proper HTTP Status Codes</h2>
<table>
<tr><th>Code</th><th>When to Use</th></tr>
<tr><td>200 OK</td><td>Successful GET, PUT, PATCH</td></tr>
<tr><td>201 Created</td><td>Successful POST — always include Location header</td></tr>
<tr><td>204 No Content</td><td>Successful DELETE (no body returned)</td></tr>
<tr><td>400 Bad Request</td><td>Malformed input, validation failure</td></tr>
<tr><td>401 Unauthorized</td><td>Missing or expired auth token</td></tr>
<tr><td>403 Forbidden</td><td>Authenticated but not permitted</td></tr>
<tr><td>404 Not Found</td><td>Resource doesn't exist</td></tr>
<tr><td>409 Conflict</td><td>Duplicate or state conflict</td></tr>
<tr><td>422 Unprocessable</td><td>Valid syntax but semantic error</td></tr>
<tr><td>429 Too Many</td><td>Rate limit exceeded — include Retry-After header</td></tr>
<tr><td>500 Internal Error</td><td>Unexpected server failure (never expose stack traces)</td></tr>
</table>

<h2>5. Error Response Format</h2>
<p>Always return errors in a consistent structure:</p>
<pre><code>{{
  "error": {{
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {{"field": "email", "reason": "must not be empty"}},
      {{"field": "age", "reason": "must be positive"}}
    ],
    "requestId": "req_abc123"
  }}
}}</code></pre>

<h2>6. Pagination, Filtering, and Sorting</h2>
<pre><code># Pagination with cursor (preferred for large datasets)
GET /users?cursor=eyJpZCI6NDJ9&limit=20
Response: {{"data": [...], "nextCursor": "eyJpZCI6NjJ9", "hasMore": true}}

# Or offset-based for simpler use cases
GET /users?offset=0&limit=20

# Filtering
GET /users?status=active&role=admin

# Sorting
GET /users?sort=-createdAt  # descending
GET /users?sort=+name       # ascending</code></pre>

<h2>7. Security Checklist</h2>
<ul>
<li><strong>Always use HTTPS.</strong> No exceptions.</li>
<li><strong>Set rate limits.</strong> At minimum: 60 req/min per IP for unauthenticated, 1000 req/min per user for authenticated.</li>
<li><strong>Validate Content-Type.</strong> Reject requests with wrong Content-Type headers.</li>
<li><strong>Set CORS explicitly.</strong> Never use <code>Access-Control-Allow-Origin: *</code> with credentials.</li>
<li><strong>Use API keys or OAuth2.</strong> Never roll your own auth protocol.</li>
<li><strong>Keep secrets out of responses.</strong> Password hashes, internal IDs, stack traces, server versions.</li>
</ul>

<h2>8. API Documentation</h2>
<p>Use OpenAPI 3.1 (Swagger). It's the industry standard and generates interactive docs automatically. Tools like Stoplight, Redoc, and Swagger UI render beautiful docs from a single spec file. If your API doesn't have an OpenAPI spec, it's not ready for production.</p>
'''

BODIES['git-advanced'] = '''
<p>Most developers stop at <code>add</code>, <code>commit</code>, <code>push</code>, and <code>pull</code>. But Git has a set of advanced commands that can save hours of frustration and make your commit history something you're actually proud of. Here's your guide to interactive rebase, cherry-pick, bisect, reflog, and hooks.</p>

<h2>Interactive Rebase: Rewrite History Cleanly</h2>
<p>The most powerful Git feature most developers never learn. Interactive rebase lets you reorder, squash, split, and edit commits before pushing.</p>
<pre><code># Squash last 4 commits into 1 clean commit
git rebase -i HEAD~4

# In the editor, mark commits:
# pick abc1234 First commit message      (keep as-is)
# squash def5678 Fix typo                (merge into previous)
# squash ghi9012 Format code             (merge into previous)
# squash jkl3456 Update tests            (merge into previous)
# Then write a single commit message</code></pre>

<h3>When to Use Interactive Rebase</h3>
<ul>
<li><strong>Before pushing to main:</strong> Squash "WIP" and "fix typo" commits into meaningful units</li>
<li><strong>Before opening a PR:</strong> Reorder commits so they tell a logical story</li>
<li><strong>Never:</strong> On shared branches or commits that have been pushed. Rewriting public history causes chaos.</li>
</ul>

<h2>Cherry-Pick: Apply a Specific Commit Anywhere</h2>
<p>When you need one specific commit from another branch without merging everything:</p>
<pre><code># Apply a single commit to the current branch
git cherry-pick abc1234

# Apply a range of commits
git cherry-pick abc1234..def5678

# Cherry-pick without committing (stage changes only)
git cherry-pick -n abc1234</code></pre>
<p>Common use: a bug fix on a release branch that you need on main, but main has diverged significantly. Cherry-pick the fix commit.</p>

<h2>Git Bisect: Find the Commit That Broke Everything</h2>
<p>Binary search through your commit history to find exactly which commit introduced a bug:</p>
<pre><code># Start bisect session
git bisect start
git bisect bad HEAD          # current commit is broken
git bisect good v2.5.0       # this tag was working

# Git checks out a commit halfway between. Test it.
# If broken:  git bisect bad
# If working: git bisect good

# Repeat until Git identifies the culprit commit.
# Then end the session:
git bisect reset</code></pre>
<p>For automated bisecting, provide a test script:</p>
<pre><code>git bisect run npm test     # Git runs the test on each step
# If the test exits with code 0 → good, non-zero → bad
# Git finds the breaking commit automatically</code></pre>

<h2>Git Reflog: The Ultimate Undo</h2>
<p>Reflog records every movement of HEAD — commits, checkouts, rebases, resets. When you think you've lost work, reflog is your safety net:</p>
<pre><code>git reflog
# Shows: abc1234 HEAD@{{0}}: commit: Add login feature
#        def5678 HEAD@{{1}}: rebase (finish): returning to refs/heads/main
#        ghi9012 HEAD@{{2}}: reset: moving to HEAD~3

# Recover that "lost" commit
git checkout HEAD@{{2}}       # go back to before the reset
git branch recovered-branch   # save it to a branch</code></pre>
<table>
<tr><th>Scenario</th><th>Recovery Command</th></tr>
<tr><td>Undo a bad rebase</td><td><code>git reset --hard HEAD@{{1}}</code></td></tr>
<tr><td>Recover deleted branch</td><td><code>git checkout -b recovered HEAD@{{3}}</code></td></tr>
<tr><td>Undo amend on wrong commit</td><td><code>git reset --soft HEAD@{{1}}</code></td></tr>
</table>

<h2>Git Hooks: Automate Your Workflow</h2>
<p>Hooks are scripts that run automatically on Git events. They live in <code>.git/hooks/</code> and can be written in any language. Use them to prevent mistakes before they happen:</p>
<pre><code>#!/bin/bash
# .git/hooks/pre-commit — run linter before every commit
npm run lint
if [ $? -ne 0 ]; then
  echo "Linting failed. Commit aborted."
  exit 1
fi</code></pre>

<pre><code>#!/bin/bash
# .git/hooks/commit-msg — enforce conventional commits
MSG=$(cat "$1")
if ! echo "$MSG" | grep -qE "^(feat|fix|refactor|test|docs|chore)(\\(.+\\))?: "; then
  echo "Commit message must follow conventional commits format"
  echo "  feat: add feature"
  echo "  fix: resolve bug"
  exit 1
fi</code></pre>

<table>
<tr><th>Hook</th><th>When It Runs</th><th>Use For</th></tr>
<tr><td>pre-commit</td><td>Before commit is created</td><td>Linting, formatting, unit tests</td></tr>
<tr><td>commit-msg</td><td>After message is entered</td><td>Enforce message format</td></tr>
<tr><td>pre-push</td><td>Before push to remote</td><td>Integration tests, security scans</td></tr>
<tr><td>post-checkout</td><td>After checkout/switching branches</td><td>Install dependencies if changed</td></tr>
</table>
'''

BODIES['best-free-dev-tools-2026'] = '''
<p>Every developer accumulates a toolkit over time. But if you're starting fresh or wondering what you're missing, here are the best free developer tools across every category — terminal, Git, databases, APIs, and more.</p>

<h2>Terminal & Shell</h2>
<table>
<tr><th>Tool</th><th>What It Is</th><th>Why Use It</th></tr>
<tr><td><a href="https://www.warp.dev" target="_blank" rel="noopener">Warp</a></td><td>Modern terminal with AI and IDE features</td><td>AI command autocomplete, split panes, team sharing. The first terminal that feels like an IDE.</td></tr>
<tr><td><a href="https://ohmyz.sh" target="_blank" rel="noopener">Oh My Zsh</a></td><td>Zsh configuration framework</td><td>300+ plugins, 150+ themes, auto-completion, and git aliases out of the box.</td></tr>
<tr><td><a href="https://starship.rs" target="_blank" rel="noopener">Starship</a></td><td>Cross-shell prompt customizer</td><td>Fast, customizable prompt that shows git status, language versions, and error codes. Works with bash, zsh, fish, and PowerShell.</td></tr>
</table>

<h2>Git GUIs & Diff Tools</h2>
<table>
<tr><th>Tool</th><th>What It Is</th><th>Why Use It</th></tr>
<tr><td><a href="https://github.com/jesseduffield/lazygit" target="_blank" rel="noopener">lazygit</a></td><td>Terminal Git GUI</td><td>Blazing fast. Interactive rebase, cherry-pick, and stash from a single terminal panel. The most efficient Git workflow once you learn the keys.</td></tr>
<tr><td><a href="https://git-fork.com" target="_blank" rel="noopener">Fork</a></td><td>GUI Git client (Mac/Windows)</td><td>Clean interactive rebase UI, conflict resolution, and commit graph. Free for personal use.</td></tr>
<tr><td><a href="https://meld.app" target="_blank" rel="noopener">Meld</a></td><td>Visual diff and merge tool</td><td>Open source. Three-way comparison. Works with git mergetool integration.</td></tr>
</table>

<h2>API Clients & Testing</h2>
<table>
<tr><th>Tool</th><th>What It Is</th><th>Why Use It</th></tr>
<tr><td><a href="https://www.usebruno.com" target="_blank" rel="noopener">Bruno</a></td><td>Open-source API client</td><td>Stores collections as files (git-friendly), no account required. The best Postman alternative in 2026.</td></tr>
<tr><td><a href="https://hoppscotch.io" target="_blank" rel="noopener">Hoppscotch</a></td><td>Web-based API testing</td><td>REST, GraphQL, WebSocket, SSE, and MQTT. Fully in-browser, zero setup, team workspaces.</td></tr>
<tr><td><a href="https://httpie.io/cli" target="_blank" rel="noopener">HTTPie</a></td><td>Terminal HTTP client</td><td>Syntax-colored JSON, sensible defaults, and plugins. The friendlier alternative to curl for API debugging.</td></tr>
</table>

<h2>Database Clients</h2>
<table>
<tr><th>Tool</th><th>What It Is</th><th>Why Use It</th></tr>
<tr><td><a href="https://dbeaver.io" target="_blank" rel="noopener">DBeaver</a></td><td>Universal database tool</td><td>Supports PostgreSQL, MySQL, SQLite, MongoDB, and 80+ others. Free community edition is fully featured.</td></tr>
<tr><td><a href="https://tableplus.com" target="_blank" rel="noopener">TablePlus</a></td><td>Native DB client (Mac/Windows/Linux)</td><td>Beautiful UI, native performance, multiple connection support. Free tier covers daily use.</td></tr>
</table>

<h2>Code Screenshots & Sharing</h2>
<table>
<tr><th>Tool</th><th>What It Is</th><th>Why Use It</th></tr>
<tr><td><a href="https://carbon.now.sh" target="_blank" rel="noopener">Carbon</a></td><td>Beautiful code screenshots</td><td>Dozens of themes, window styling, export as PNG/SVG. The standard for sharing code on social media.</td></tr>
<tr><td><a href="https://ray.so" target="_blank" rel="noopener">Ray.so</a></td><td>Raycast's code image tool</td><td>Fast, beautiful presets, dark/light mode, background customization. Also generates snippet links.</td></tr>
</table>

<h2>Essential Checklist for a New Machine</h2>
<ol>
<li>Terminal: <strong>Warp</strong> or <strong>iTerm2 + Oh My Zsh + Starship</strong></li>
<li>Package manager: <strong>Homebrew</strong> (Mac), <strong>Chocolatey</strong> (Windows), or your system default</li>
<li>Version control: <strong>Git + lazygit</strong></li>
<li>API testing: <strong>Bruno</strong> or <strong>Hoppscotch</strong></li>
<li>Database: <strong>DBeaver</strong> or <strong>TablePlus</strong></li>
<li>Editor: already covered — see <a href="/en/tech/editor-comparison-2026/">Code Editor Showdown</a></li>
</ol>

<p>All tools above are free for individual developers. Bookmark this page and come back next time you set up a new machine.</p>
'''

BODIES['design-tools-for-developers'] = '''
<p>You don't need a design degree to build polished, professional-looking products. Modern design tools have gotten so good — and so free — that a developer can produce designer-quality UI without hiring anyone. Here's every tool you need, organized by what you're actually trying to do.</p>

<h2>UI Design: Figma (Free Tier Is Enough)</h2>
<p><a href="https://figma.com" target="_blank" rel="noopener">Figma</a> is the industry standard for a reason. The free tier includes unlimited personal files, 3 collaborative files, and access to the community template library. You can go from wireframe to pixel-perfect mockup in a few hours.</p>
<ul>
<li>Learn the basics in 2 hours: <strong>Shift + R</strong> (ruler/guides), <strong>Auto Layout</strong> (flexbox equivalent), <strong>Components</strong> (reusable like React components)</li>
<li>Grab free UI kits from the Figma Community: search "iOS UI kit" or "dashboard template"</li>
<li>Export assets at 1x/2x/3x for web and mobile</li>
</ul>

<h2>Color: Never Guess Hex Codes Again</h2>
<table>
<tr><th>Tool</th><th>Use For</th></tr>
<tr><td><a href="https://coolors.co" target="_blank" rel="noopener">Coolors</a></td><td>Generate color palettes. Press spacebar to cycle through endless combinations. Lock colors you like and keep generating.</td></tr>
<tr><td><a href="https://realtimecolors.com" target="_blank" rel="noopener">Realtime Colors</a></td><td>See your palette applied to a real UI preview (buttons, cards, text, nav). The fastest way to validate a color scheme.</td></tr>
<tr><td><a href="https://uicolors.app" target="_blank" rel="noopener">UI Colors</a></td><td>Generate a full Tailwind-compatible color scale from a single hex code. Gives you 50-950 shades instantly.</td></tr>
<tr><td><a href="https://color.adobe.com" target="_blank" rel="noopener">Adobe Color</a></td><td>Extract palette from an image. Useful when you have a hero image and want a matching theme.</td></tr>
</table>

<h2>Icons: Never Draw One from Scratch</h2>
<table>
<tr><th>Library</th><th>Style</th><th>Count</th></tr>
<tr><td><a href="https://lucide.dev" target="_blank" rel="noopener">Lucide</a></td><td>Clean, consistent stroke-based</td><td>1,500+</td></tr>
<tr><td><a href="https://phosphoricons.com" target="_blank" rel="noopener">Phosphor</a></td><td>Playful, 6 weights per icon</td><td>1,300+</td></tr>
<tr><td><a href="https://tabler.io/icons" target="_blank" rel="noopener">Tabler Icons</a></td><td>Pixel-perfect strokes, great for dashboards</td><td>5,200+</td></tr>
<tr><td><a href="https://heroicons.com" target="_blank" rel="noopener">Heroicons</a></td><td>Tailwind team's official set, outline + solid</td><td>300+</td></tr>
<tr><td><a href="https://svgrepo.com" target="_blank" rel="noopener">SVG Repo</a></td><td>Massive searchable collection of SVG logos and icons</td><td>500,000+</td></tr>
</table>

<h2>Illustrations & Visual Polish</h2>
<table>
<tr><th>Resource</th><th>Description</th></tr>
<tr><td><a href="https://undraw.co" target="_blank" rel="noopener">unDraw</a></td><td>Open-source illustrations. Change the accent color to match your brand. SVG download, no attribution.</td></tr>
<tr><td><a href="https://blush.design" target="_blank" rel="noopener">Blush</a></td><td>Mix-and-match illustrations by professional artists. Each illustration is customizable with different characters and scenes.</td></tr>
<tr><td><a href="https://storyset.com" target="_blank" rel="noopener">Storyset</a></td><td>Animated illustrations by Freepik. Great for onboarding flows and empty states. Free with attribution.</td></tr>
</table>

<h2>Typography: Fonts That Look Professional</h2>
<ul>
<li><strong>Google Fonts</strong> — Inter, JetBrains Mono, and Space Grotesk are the developer favorites in 2026</li>
<li><strong>Fontsource</strong> — self-host Google Fonts as npm packages for better performance and GDPR compliance</li>
<li><a href="https://fontpair.co" target="_blank" rel="noopener">Fontpair</a> — curated font pairings. When you can't decide what goes with what.</li>
<li><a href="https://typescale.com" target="_blank" rel="noopener">Type Scale</a> — visual type scale calculator. Set body size → get the perfect h1-h6 scale.</li>
</ul>

<h2>Stock Photos That Don't Look Like Stock Photos</h2>
<p>See our <a href="/en/sidehustle/free-images/">Best Free Stock Photo Sites</a> guide for the full list. Quick picks: Unsplash for natural photos, Pexels for videos too, and Kaboompics for styled flat lays.</p>

<h2>The Developer Design Stack (Save This)</h2>
<ol>
<li><strong>Figma</strong> — wireframe and mockup</li>
<li><strong>Coolors + Realtime Colors</strong> — palette</li>
<li><strong>Lucide or Phosphor</strong> — icons</li>
<li><strong>unDraw or Storyset</strong> — illustrations</li>
<li><strong>Google Fonts (Inter + JetBrains Mono)</strong> — typography</li>
</ol>

<p>You can build a SaaS landing page, portfolio site, or product UI with just these five tools. No design background needed.</p>
'''

# FAQ data for FAQPage schema (slug → list of q/a dicts)
FAQS = {
    'chatgpt-plus-worth': [
        {'q': 'Is ChatGPT Plus worth it in 2026?', 'a': 'For daily users who hit the free tier message limit or need file uploads, web browsing, and DALL-E image generation, ChatGPT Plus at $20/month is worth it. Casual users who ask fewer than 10 serious questions per day can stay on the free tier.'},
        {'q': 'What is the difference between ChatGPT Free, Plus, and Pro?', 'a': 'Free uses GPT-4o mini with limited messages. Plus ($20/mo) gives full GPT-4o, web browsing, file uploads, DALL-E images, and ~80 messages per 3 hours. Pro ($200/mo) adds unlimited access and o1 Pro deep reasoning mode.'},
        {'q': 'Who should upgrade to ChatGPT Pro?', 'a': 'ChatGPT Pro at $200/month is for researchers needing deep reasoning on complex problems, developers using ChatGPT 6+ hours daily as their primary coding tool, and businesses where AI usage directly generates revenue.'},
    ],
    'claude-vs-chatgpt': [
        {'q': 'Which is better for coding — Claude or ChatGPT?', 'a': 'Both are excellent. Claude has an edge for complex refactoring and code review of large codebases due to its 200K context window. ChatGPT has an advantage for data-heavy coding tasks with its Code Interpreter feature.'},
        {'q': 'Which AI assistant writes better — Claude or ChatGPT?', 'a': 'Claude produces noticeably more natural, nuanced writing in English and is dramatically better in Chinese. For bloggers, writers, and content creators, Claude is the clear winner for writing quality.'},
        {'q': 'Can Claude generate images like ChatGPT?', 'a': 'No, Claude cannot generate images. ChatGPT has DALL-E 3 built in for image generation. The recommended setup is to use both: Claude for writing and coding, ChatGPT for image generation and web browsing.'},
        {'q': 'What is the best AI assistant setup in 2026?', 'a': 'Dual-wield the free tiers: Claude Free + ChatGPT Free gives you both strengths at zero cost. If you pay for one, choose based on your primary use case: Claude Pro for writing and research, ChatGPT Plus for visual content and web-connected tasks.'},
    ],
    'developer-side-hustles-2026': [
        {'q': 'What is the most profitable side hustle for developers?', 'a': 'Building a bootstrapped SaaS product has the highest earning potential for developers, with successful solo founders generating $5K-$50K+ monthly recurring revenue. Freelancing offers the fastest cash (weeks), while SaaS and job boards build long-term wealth.'},
        {'q': 'How can a developer make passive income?', 'a': 'Developers can earn passive income by selling digital products (ebooks, cheatsheets, code templates), building and monetizing APIs, creating browser extensions with premium features, or building a niche job board. These require upfront work but generate ongoing revenue with minimal maintenance.'},
        {'q': 'What programming side hustles require no upfront money?', 'a': 'Freelancing, technical content creation (blogging, YouTube), and selling digital products on Gumroad all require $0 upfront — just your time and skills. Building a SaaS or job board may need hosting costs ($5-20/month) but these are minimal.'},
    ],
    'saas-bootstrapping-guide': [
        {'q': 'How much does it cost to bootstrap a SaaS?', 'a': 'A solo developer can bootstrap a SaaS MVP for $0-50/month using free tiers: Vercel/Railway for hosting, Supabase for database/auth, Stripe for payments, and Resend for email. The main investment is time, typically 4-8 weeks of development.'},
        {'q': 'How long does it take to get first paying customers for a SaaS?', 'a': 'Most bootstrapped SaaS products get their first paying customer within 2-4 weeks of launch if they validated the idea first. Reaching meaningful revenue ($2K+ MRR) typically takes 12-18 months of consistent shipping and iteration.'},
        {'q': 'What tech stack is best for a solo SaaS founder?', 'a': 'Recommended stack: Next.js or Remix for frontend, FastAPI or Hono for backend API, PostgreSQL via Supabase or Neon, Clerk or Supabase Auth for authentication, Stripe for payments, and Vercel or Railway for hosting. These have generous free tiers and are fast to develop with.'},
        {'q': 'What is the biggest mistake when bootstrapping a SaaS?', 'a': 'Building too much before launching. Your MVP should feel almost embarrassingly simple — ship after 4-6 weeks with just the core feature, basic auth, and payment integration. Talk to customers weekly and iterate based on feedback rather than building features nobody asked for.'},
    ],
}

# ═══════════════════════════════════════════════════════════════════════
# HTML generators
# ═══════════════════════════════════════════════════════════════════════

def make_article_html(art, board_id, board_name, all_posts):
    tags_h = '\n'.join(f'        <span class="tag-cat">{t}</span>' for t in art['tags'])
    pin_h = '<span class="tag-pin">📌 Pinned</span>\n' if art.get('pinned') else ''
    if art.get('hot'):
        tags_h += '\n        <span class="tag-cat" style="background:#fff3cd;color:#856404;">🔥 Hot</span>'

    slug = art['slug']
    cn_url = f'{BASE}/{board_id}/{slug}.html'
    en_url = f'{BASE}/en/{board_id}/{slug}.html'
    art_url = en_url

    # OG / Twitter Card
    og_tags = f'''    <meta property="og:title" content="{art['title']}">
    <meta property="og:description" content="{art['description']}">
    <meta property="og:url" content="{art_url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="AI Study Room">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{art['title']}">
    <meta name="twitter:description" content="{art['description']}">'''

    # FAQ Schema for articles that have Q&A sections
    faq_schema = ''
    faq_data = FAQS.get(slug)
    if faq_data:
        faq_items = ',\n'.join(
            f'''      {{
        "@type": "Question",
        "name": "{q['q']}",
        "acceptedAnswer": {{"@type": "Answer", "text": "{q['a']}"}}
      }}''' for q in faq_data
        )
        faq_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
    {faq_items}
      ]
    }}
    </script>'''

    # Compute related posts at build time — same board first, up to 4
    same_board = [p for p in all_posts if p['board_id'] == board_id and p['slug'] != slug]
    other_board = [p for p in all_posts if p['board_id'] != board_id and p['slug'] != slug]
    related = (same_board + other_board)[:4]
    related_html = ''
    for r in related:
        r_url = f"/en/{r['board_id']}/{r['slug']}.html"
        related_html += f'<a href="{r_url}" class="related-card">{r["title"]}</a>'

    # Mid-content AdSense — placed after article body at ~60% scroll depth
    ad_mid = f'''<div style="margin:2rem 0;text-align:center;">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-3258394111169733"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="en" data-render="related" data-board="{board_id}" data-exclude="{slug}">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="XzThATs15kR08VOM-tCxIztKjEGW8ft-T75SmH_Wz38" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="base-path" content="/en">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
{og_tags}
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
    </script>{faq_schema}
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
    {ad_mid}
    <section class="related">
      <h3>Related Articles</h3>
      <div class="related-grid">{related_html}</div>
      <div id="related-posts" style="display:none;"></div>
    </section>
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
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <meta property="og:title" content="{site['name']} — {site['tagline']}">
    <meta property="og:description" content="Forum-style resource library aggregating tech tutorials, side hustle ideas, tool recommendations, and AI guides.">
    <meta property="og:url" content="https://dingjiu1989-hue.github.io/en/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="AI Study Room">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{site['name']} — {site['tagline']}">
    <meta name="twitter:description" content="Forum-style resource library aggregating tech tutorials, side hustle ideas, tool recommendations, and AI guides.">
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
    <script>
    // Language auto-redirect — only on English homepage
    (function(){{
      if (window.location.pathname !== '/en/') return;
      var choice = localStorage.getItem('lang');
      if (!choice) {{
        var lang = navigator.language || '';
        if (lang.startsWith('zh')) {{
          window.location.replace('/');
        }}
      }}
    }})();
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
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XGFYGQE9NS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XGFYGQE9NS');
    </script>
    <meta property="og:title" content="{title} — SourceHub">
    <meta property="og:description" content="{board_descs[board_id]}">
    <meta property="og:url" content="{en_url}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="AI Study Room">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} — SourceHub">
    <meta name="twitter:description" content="{board_descs[board_id]}">
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

    # Build flat list of all posts for related posts computation
    all_posts = []
    for board in data['boards']:
        for art in board['posts']:
            all_posts.append({**art, 'board_id': board['id']})

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
            p.write_text(make_article_html(art, board['id'], board_name, all_posts), encoding='utf-8')
            created += 1
            print(f'  HTML: {p}')

    print(f'\nCreated {created} files.')


if __name__ == '__main__':
    main()
