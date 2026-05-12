---
title: "Output Encoding"
description: "Guide to output encoding covering context-sensitive encoding, XSS prevention, template engine auto-escaping, and common encoding pitfalls."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/output-encoding.html
---

# Output Encoding

becomes

  


# <script>alert(1)</script>

  


return encoded

  
  
  
  


HTML Attribute Context 

  
  
  


def encode_html_attribute(user_input):

  


"""Encode for HTML attribute values."""

  


# More aggressive than body encoding

  


replacements = {

  


'&': '&',

  


'"': '"',

  


"'": ''',

  


'<': '<',

  


'>': '>',

  


'/': '/', # Prevents attribute closing

  


'`': '`', # Backtick can close attributes in some browsers

  


}

  


for char, replacement in replacements.items():

  


user_input = user_input.replace(char, replacement)

  


return user_input

  
  
  
  


JavaScript Context 

  
  
  


import json

  


import re

  
  
  


def encode_javascript_string(user_input):

  


"""Encode for JavaScript string context."""

  


# JSON encoding is safe for JS string literals

  


encoded = json.dumps(user_input, ensure_ascii=False)

  
  
  


# Additional hardening for
