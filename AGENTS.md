# AGENTS.md - gov-service
We use wikipush mcp wiki id gov. Further instructions are at
https://gov-wiki.genealogy.net/index.php/GOV-Service/Plan

## Project Style
Use `checkos` to verify project structure compliance — see https://gov-wiki.genealogy.net/index.php/GOV-Service/Plan for details.

## Build & Test
```bash
scripts/install   # install dependencies
scripts/test      # python3 -m unittest discover
```

## Code Style
- All tests extend `tests.basetest.Basetest` (not `unittest.TestCase` directly)
- Call `Basetest.setUp(self, debug=False, profile=True)` in each `setUp`
- Use `self.inPublicCI()` to skip tests requiring live local services
- Google-style docstrings, module header: `Created on YYYY-MM-DD\n\n@author: wf`
- Line length: 120 (black), imports: isort three-group layout
- Run `scripts/blackisort` before committing

## Python Conventions
- Never use `return expr` for multi-line strings — assign to a variable first, then `return` it on its own line
- Multi-line f-strings use `"""` triple quotes assigned to a variable, never a tuple of f-string fragments
- Build HTML with `html = f"..."` / `html += f"..."`, return `html` — no HTML outside `as_html` methods
- No bare `return expression` for anything longer than a single short line
