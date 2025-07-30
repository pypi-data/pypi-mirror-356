
---

# Starburst Scheduler

A Python CLI tool to run and schedule SQL queries on **Starburst Galaxy** or **Starburst Enterprise** clusters.

---

## Installation

```bash
pip install starburst-scheduler
```

---

## Requirements

* Starburst Galaxy or Enterprise cluster (e.g., `free-cluster.trino.galaxy.starburst.io`)
* Valid Starburst username and password
* Python 3.9 or above

---

## Usage

### Run a One-Time Query

```bash
starburst-scheduler run-query \
  --host free-cluster.trino.galaxy.starburst.io \
  --user your-user@domain.com \
  --password your-password \
  --catalog tpch \
  --schema tiny \
  --query "SELECT 1"
```

### Use Environment Variable (Secure)

```bash
# macOS/Linux
export STARBURST_PASSWORD=your-password

# Windows
set STARBURST_PASSWORD=your-password

starburst-scheduler run-query \
  --host free-cluster.trino.galaxy.starburst.io \
  --user your-user@domain.com \
  --catalog tpch \
  --schema tiny \
  --query "SELECT 1"
```

> Note: Default `--http-scheme` is `https`. Use `--http-scheme http` only for local insecure clusters.

---

### Schedule a Repeating Query

```bash
starburst-scheduler schedule-query \
  --host free-cluster.trino.galaxy.starburst.io \
  --user your-user@domain.com \
  --password your-password \
  --catalog tpch \
  --schema tiny \
  --query "SELECT * FROM nation" \
  --frequency 60 \
  --time-unit seconds
```

This runs the query every 60 seconds until manually stopped (Ctrl + C).

---

## CLI Options

| Option          | Description                               |
| --------------- | ----------------------------------------- |
| `--host`        | Starburst cluster host                    |
| `--user`        | Starburst username or email               |
| `--password`    | Starburst password (or use env var)       |
| `--catalog`     | Catalog to query                          |
| `--schema`      | Schema to query                           |
| `--query`       | SQL query string                          |
| `--http-scheme` | `https` (default) or `http` for local use |
| `--frequency`   | Frequency for scheduled query             |
| `--time-unit`   | Time unit (`seconds`, `minutes`, `hours`) |

---

## Troubleshooting

### Common Issues

* **Cluster Inactive**
  Start it at: [https://galaxy.starburst.io/home](https://galaxy.starburst.io/home)

* **401 Unauthorized**

  * Wrong credentials
  * Quotes in environment variable
  * Cluster not started

* **Connection Errors**

  * Wrong `--host` or `--http-scheme`

* **Access Denied**

  * User lacks permission on catalog/schema

* **Broken Installation**

  ```bash
  pip install --force-reinstall starburst-scheduler
  ```

---

---

## License

MIT License

---

## Contributing

Contributions are welcome. Submit issues or pull requests at:
[https://github.com/karranikhilreddy99/starburst\_scheduler](https://github.com/karranikhilreddy99/starburst_scheduler)

---

Let me know if you want this delivered as a downloadable `.md` or `.docx` file.
