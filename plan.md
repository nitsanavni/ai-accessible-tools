# Do

- [ ] build it outside-in, start with the loop structure
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

# Thoughts

- testing each frame of a loop independently
- testing multiple iterations
  - non inline
  - storyboard
    - verify multiple views of the story - each in a separate approved file
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
- tool choice with priority
- tools ideas
  - edit
    - refactor
      - rename
      - extract (introduce)
      - inline
    - replace lines
      - replace line and keep indentation
      - insert
    - replace occurrences
    - move (slide) lines
    - dup lines
- writing a full coherent python function is easier than replacing a single line
