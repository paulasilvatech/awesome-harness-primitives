# Troubleshooting — Diagnosis and Debugging in Fabric Notebooks

How to diagnose and debug issues in Fabric Notebooks.

> **Public documentation (for user reference, not agent-actionable):**
> - [Python logging in notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/author-execute-notebook#python-logging-in-a-notebook) — `logging.getLogger`, log levels, custom formatters

This file covers **agent-actionable diagnosis behavior**.

---

## Diagnosis Approach

When validating code or fixing notebook code run issues:

1. **Always check notebook cell outputs first** for errors, warnings, or unexpected results
2. Use those outputs to guide diagnosis and fixes
3. If no outputs are available, suggest running the code to gather necessary context
4. Check Spark Advisor warnings (displayed inline beneath cells) for optimization and error hints

---

## How to Access Logs

### In notebook code cells

| Method | How |
|---|---|
| **Python logging** | Use `logging.getLogger()` — set level, format, output structured logs |
| **Cell output** | Read cell output text for errors, stack traces, and Spark Advisor warnings |

### Read log files from within a notebook cell

In Spark notebooks, log files are available on the local filesystem. Agent can generate code to read them:

| Log File | Path | Content |
|---|---|---|
| **Spark driver log** | `/var/log/sparkapp/sparkdriver.log` | Driver-side errors, warnings, Spark plan info, **notebookutils logs** |
| **Spark executor log** | `/var/log/sparkapp/sparkexecutor.log` | Executor-side errors, task failures, OOM |
| **Blobfuse log** | `/var/log/blobfuse/blobfusev2.log` | OneLake/ADLS mount issues, I/O errors |
| **YARN container stdout** | `/var/log/yarn-nm/userlogs/application_*/container_*/stdout` | Application stdout output |

```python
# Read last 50 lines of driver log
!tail -n 50 /var/log/sparkapp/sparkdriver.log
```

```python
# Search for errors in executor log
!grep -i "error\|exception\|oom" /var/log/sparkapp/sparkexecutor.log
```

```python
# Search for notebookutils issues in driver log
!cat /var/log/sparkapp/sparkdriver.log | grep -i notebookutils
```
