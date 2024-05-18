- [ ] replace_until
  - [ ] replace and black
- [ ] a view-based execution loop
  - the agent only sees a narrow view
- [ ] register test[s] -> revert the edit on failure
  - e.g. `black <file>`
- [ ] replace - start_line: `7\t|    # TODO:...`
- [ ] replace - multi replace order: make sure to perform multiple replaces starting from the last one in terms of line number
- [x] extract to separate files
- [x] replace in file

Thoughts

- `tool` vs. `ai-tool`: `ai-tool` means at least one more prompt iteration
- `dashboard watch [--list] [--add <glob>|<>] --remove <glob>`
- timebox / iterations-box / reties
- higher horizon "accepts/rejects" lower horizon result
- one prompt per horizon
- execution loop
  - feedback
- next action = f(dashboard)
- dashboard components
  - recent actions
  - recent files
  - pwd
