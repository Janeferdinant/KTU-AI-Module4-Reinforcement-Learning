import os
import sys

output_path = r"c:\Users\Asus\Downloads\AI-MOD4\index.html"

# Read current index.html to preserve styling and existing theory/demo content
with open(output_path, "r", encoding="utf-8") as f:
    orig = f.read()

print("Original index.html length:", len(orig))
