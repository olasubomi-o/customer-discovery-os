# Demo: invoice chasing for agencies

Everything in this folder is invented demo data. The people, quotes and numbers are not real customers. It exists so you can try the commands without your own interviews.

Try it from this folder (replace the path with where the plugin is installed):
```
python3 <plugin>/shared/scripts/ddos.py status
python3 <plugin>/shared/scripts/ddos.py check
```
Then edit a quote in `discovery/synthesis/` so it is not word for word in a transcript and run `check` again. It will fail with exit code 2. Fix the quote and it passes.

Do not copy this folder as a starting point for a real project. Run `ddos.py init --hypothesis "your idea"` in a new project folder instead.
