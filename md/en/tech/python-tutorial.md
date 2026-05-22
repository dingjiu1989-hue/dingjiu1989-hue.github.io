---
title: "Python Tutorial: From Zero to Your First Program"
description: "A beginner-friendly Python tutorial. Master variables, conditionals, loops, and functions in 30 minutes and write your first working program."
date: 2025-10-01
board: tech
url: https://aidev.fit/en/tech/python-tutorial.html
---

# Python Tutorial: From Zero to Your First Program

Python is the most approachable programming language in the world — and also one of the most powerful. In this tutorial, you'll go from zero to a working program in 30 minutes.

## Installing Python

Download from [python.org](<https://www.python.org/downloads/>). During installation on Windows, check **"Add Python to PATH"**. On macOS, `brew install python` works too. Verify with:
    
    
    python3 --version  # should print "Python 3.x.x"

## Your First Program
    
    
    print("Hello, world!")

Save as `hello.py` and run with `python3 hello.py`. That's it — you're a programmer now.

## Variables and Types
    
    
    name = "Alice"           # string
    age = 30                 # integer
    height = 1.68            # float
    is_student = False       # boolean
    
    print(f"{name} is {age} years old")  # f-strings!

## Conditionals
    
    
    score = 85
    if score >= 90:
        print("A")
    elif score >= 80:
        print("B")
    elif score >= 70:
        print("C")
    else:
        print("Need improvement")

## Lists and Loops
    
    
    fruits = ["apple", "banana", "cherry"]
    fruits.append("date")
    print(fruits[0])          # "apple"
    
    for fruit in fruits:
        print(fruit.upper())
    
    # List comprehension (Python's superpower)
    squares = [x**2 for x in range(10)]
    # → [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

## Dictionaries
    
    
    user = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    }
    print(user["name"])
    user["city"] = "New York"  # add a key
    
    for key, value in user.items():
        print(f"{key}: {value}")

## Functions
    
    
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    print(greet("Alice"))               # "Hello, Alice!"
    print(greet("Bob", "Howdy"))        # "Howdy, Bob!"

## Working with Files
    
    
    # Read a file
    with open("data.txt", "r") as f:
        content = f.read()
    
    # Write a file
    with open("output.txt", "w") as f:
        f.write("Hello, file!")

## Error Handling
    
    
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Can't divide by zero!")
    finally:
        print("This always runs")

## A Complete Mini-Program
    
    
    import json
    
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
    
    main()

## Where to Go Next

  * **Automate the Boring Stuff** — free Python book, perfect for practical learners
  * **Real Python** — excellent tutorials from beginner to advanced
  * **Build something** — a CLI tool, a simple web scraper, a TODO app. Anything.



The secret to learning Python: start building things immediately. Don't get stuck in tutorial hell.
