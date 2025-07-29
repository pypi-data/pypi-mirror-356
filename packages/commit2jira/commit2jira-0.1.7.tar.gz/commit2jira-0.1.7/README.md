
# Commit2Jira

Commit2Jira is a simple Git hook that automatically adds your commit messages as comments on Jira tickets. Just include the ticket ID (e.g. `ABC-123`) in your commit message, and it will post the message directly to the corresponding Jira ticket.

##  Installation

```bash
pip install commit2jira && commit2jira install
```

This installs the Git post-commit hook into your current repository.

##  How to Use

Just commit as usual, including the Jira ticket key in your message:

```bash
git commit -m "ABC-123 Fix login redirect bug"
```

 This will automatically add your commit message as a comment on the `ABC-123` issue in Jira.

##  Notes

- Make sure your `.env` file is configured with your Jira credentials and base URL.
- Only commits containing a Jira ticket ID like `PROJ-456` will trigger the hook.
