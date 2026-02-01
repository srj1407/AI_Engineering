📓 Day 05: Documentation & Portfolio Excellence
1. What makes a README compelling vs. just informative?
A compelling README focuses on the Problem and Solution.

Informative: "This script uses asyncio." (Features)

Compelling: "This system ensures 99.9% data delivery despite flaky APIs." (Benefits) It includes a "Wow" factor: clear usage examples, a visual architecture diagram, and a direct explanation of the value it provides to the user.

2. What's the difference between code comments and documentation?
We can organize this as a clear distinction of intent:

Documentation (README/Docstrings): Targeted at the User. It explains what the code does and how to use the interface correctly.

Code Comments: Targeted at the Maintainer. It explains the "tricky" bits or why a specific implementation detail was chosen over another.

3. Why do design decisions matter in documentation?
Documenting design decisions shows Architectural Empathy.

It proves you thought about trade-offs (e.g., "I chose a Semaphore of 5 to avoid triggering the server's rate-limiting firewall"). 🛡️

It allows future engineers to understand the constraints you were working under so they don't break the system by accident.

🚀 The Final Polish: Docstrings & Type Hints
To make your code truly "portfolio ready," we need to add Type Hints and Docstrings. Type hints tell the editor (and the senior engineer) exactly what kind of data is flowing through your functions.