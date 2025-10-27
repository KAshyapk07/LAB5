### Reflections:

##### 1. Which issues were the easiest to fix, and which were the hardest? Why?
######	Easiest fixes:
o	The formatting and style issues reported by Flake8 and Pylint (like missing blank lines, trailing whitespace, and missing final newline) were very easy to fix.
o	The mutable default argument (logs=[]) and missing docstrings were also simple because they only required small code edits or additional documentation lines.
•	Hardest fixes:
o	The global variable warning  was the hardest conceptually because it required rethinking the program structure. While disabling the warning works, the true fix involves refactoring the code into a class-based design, which is more complex.
o	Handling exceptions properly (replacing bare except) also required more reasoning about which specific exceptions to catch and how to handle them correctly.

##### 2. Did the static analysis tools report any false positives? If so, describe one example.
•	One potential false positive was the warning about the global statement .
In this small standalone script, using a global variable for in-memory inventory data was intentional and safe.
However, Pylint still flagged it because globals are generally discouraged in large-scale software.
This isn’t truly an error in this context but a best-practice warning.

##### 3. How would you integrate static analysis tools into your actual software development workflow?
######	Local development:
o	Use pylint, flake8, and bandit as pre-commit hooks to automatically scan code before pushing to a repository.
o	Configure the IDE (like VS Code) to show linting results in real-time for faster feedback.
•	Continuous Integration (CI):
o	Integrate these tools into a CI pipeline (e.g., GitHub Actions, GitLab CI, or Jenkins).
o	Automatically fail builds if code quality drops below a certain threshold
o	Generate and archive linting and security reports after every build for transparency and auditing.

##### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
•	Improved readability: Consistent formatting, proper naming conventions (snake_case), and meaningful docstrings make the code much easier to understand.
•	Increased robustness: Type validation, safer file handling (with open), and removal of unsafe eval() greatly reduce the risk of runtime and security issues.
•	Better maintainability: Functions now follow clear responsibilities with predictable behavior and informative logging.
•	Higher reliability: Proper exception handling ensures the program doesn’t silently fail, and type checks prevent invalid input early.
