# Karakana Configuration

Karakana works without a configuration file. Defaults are safe and local.

## Config Files

Karakana reads the first available file:

- `karakana.yml`
- `karakana.yaml`
- `.karakana/config.json`

## Environment Variables

Provider credentials may be present in the environment, but they are optional for local tests and dry-run workflows. Secret values are redacted in summaries and artifacts.

Supported local overrides:

- `KARAKANA_DEFAULT_PROVIDER`
- `KARAKANA_DEFAULT_MODEL`

## Safe Defaults

- Live models are disabled by default.
- GitHub writes are disabled by default.
- Write operations require explicit flags.
- Artifacts default to `.karakana/`.

## Commands

```bash
karakana config show
karakana config validate
karakana config paths
```
