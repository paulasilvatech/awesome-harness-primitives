# Troubleshooting reference

## Troubleshooting

### Troubleshooting commands

```bash
# Check Prometheus logs
kubectl logs -n monitoring -l app.kubernetes.io/name=prometheus --tail=100

# Check Grafana logs
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana --tail=100

# Check for scrape errors
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health != "up") | {job: .labels.job, health, lastError}'
```

