# Project files and best practices reference

### Project files reference

- **Helm values:** `deploy/helm/monitoring/values.yaml`
- **Alerting rules:** `prometheus/alerting-rules.yaml`
- **Recording rules:** `prometheus/recording-rules.yaml`
- **Grafana dashboards:** `grafana/dashboards/`
- **Terraform module:** `terraform/modules/observability/`

### Best practices

1. Use ServiceMonitors for scrape configuration
2. Set appropriate retention periods (15d default)
3. Configure alert routing correctly (PagerDuty for critical, Teams for warning)
4. Use recording rules for expensive queries
5. Enable persistent storage for Prometheus and Grafana
6. Configure Entra ID SSO for Grafana
7. Monitor ArgoCD and Backstage scrape targets

