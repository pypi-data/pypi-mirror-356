Starburst Scheduler
A Python pip package to run and schedule SQL queries on Starburst Galaxy or Starburst Enterprise clusters.
Installation
pip install starburst-scheduler

Prerequisites

Starburst Galaxy or Enterprise cluster (e.g., your-cluster.trino.galaxy.starburst.io).
Credentials (username, password).
Python 3.9+.

Usage
Run a Single Query
starburst-scheduler run-query --host your-cluster.trino.galaxy.starburst.io --user your-user@domain.com --password your-password --catalog system --schema runtime --query "SELECT 1"

Or use environment variable:
export STARBURST_PASSWORD=your-password  # Linux/macOS
set STARBURST_PASSWORD=your-password     # Windows
starburst-scheduler run-query --host your-cluster.trino.galaxy.starburst.io --user your-user@domain.com --catalog system --schema runtime --query "SELECT 1"

Schedule a Query
starburst-scheduler schedule-query --host your-cluster.trino.galaxy.starburst.io --user your-user@domain.com --password your-password --catalog system --schema runtime --query "SELECT * FROM nodes" --frequency 60 --time-unit seconds

Troubleshooting

Cluster Stopped: Start your cluster at https://your-cluster.galaxy.starburst.io/.
Authentication Error (401): Verify username/password. Ensure no quotes are included in the password when set in the environment variable (e.g., set STARBURST_PASSWORD=your-password).
Table Access: Ensure permissions for catalog/schema.
Installation Error: Ensure all files (e.g., README.md, setup.py) are saved with UTF-8 encoding.

Planned Enhancements

Slack & Mattermost integration
CSV/JSON output
Advanced scheduling (cron expressions)
Email notifications
Error alerting

License
MIT License
Contributing
File issues or PRs at https://github.com/karranikhilreddy99/starburst_scheduler.
