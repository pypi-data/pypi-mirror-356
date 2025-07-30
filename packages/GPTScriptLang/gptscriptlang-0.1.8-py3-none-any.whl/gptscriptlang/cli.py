import sys
import re

class WrongUsage(Exception):
    pass

if len(sys.argv) != 2:
    raise WrongUsage("Usage: gptscript file.gpt")
    
class ScriptNotFound(Exception):
    pass

path = sys.argv[1]
try:
    with open(path, "r") as f:
        lines = f.read().strip().split('\n')
except FileNotFoundError:
    raise ScriptNotFound()

python = []
i = 0
in_func = False

while i < len(lines):
    line = lines[i].strip()
    indent = "    " if in_func else ""

    if line.startswith("Hello, how can I assist you today?"):
        i += 1
        continue

    elif line.startswith("Let me store the number"):
        m = re.match(r"Let me store the number (\d+) as (\w+)\.", line)
        if m:
            num, var = m.groups()
            python.append(f"{indent}{var} = {num}")

    elif line.startswith("Let me store the text"):
        m = re.match(r'Let me store the text "(.+)" as (\w+)\.', line)
        if m:
            txt, var = m.groups()
            python.append(f'{indent}{var} = "{txt}"')

    elif line.startswith("Now, let's kindly display:"):
        content = line.split("display:")[1].strip()
        python.append(f"{indent}print({content})")

    elif line.startswith("I would like to fetch from"):
        m = re.match(r'I would like to fetch from "([^"]+)" and store it as (\w+)\.', line)
        if m:
            url, var = m.groups()
            if "import requests" not in python:
                python.insert(0, "import requests")
            python.append(f'{indent}{var} = requests.get("{url}").json()')

    elif line.startswith("Kindly post to"):
        m = re.match(r'Kindly post to "([^"]+)" with the content:', line)
        if m:
            url = m.group(1)
            i += 1
            json_lines = []
            while i < len(lines) and lines[i].strip() != "":
                json_lines.append(lines[i])
                i += 1
            json_body = '\n'.join(json_lines)
            if "import requests" not in python:
                python.insert(0, "import requests")
            python.append(f'{indent}requests.post("{url}", json={json_body})')

    elif line.startswith("With all due respect, define"):
        m = re.match(r'With all due respect, define (\w+):', line)
        if m:
            fname = m.group(1)
            python.append(f"def {fname}():")
            in_func = True

    elif in_func and line == "End definition.":
        in_func = False

    elif re.match(r"Please invoke (\w+)\.", line):
        m = re.match(r"Please invoke (\w+)\.", line)
        python.append(f"{indent}{m.group(1)}()")

    elif line.startswith("Thank you for your patience."):
        break

    else:
        if in_func:
            python.append(f"{indent}{line}")

    i += 1

code = '\n'.join(python)
exec_globals = {}
exec(code, exec_globals)