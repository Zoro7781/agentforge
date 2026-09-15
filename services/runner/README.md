# Isolated pytest runner

Use a dedicated host. Do not give public users access to this service or mount the Docker socket into generated containers. For hostile multi-tenant workloads use a VM/microVM isolation layer and an authenticated queue instead of this bounded single-host runner.

1. Build the fixed dependency image: `docker build -t agentforge-sandbox:local -f services/runner/Dockerfile.sandbox .`
2. Install `services/runner/requirements.txt` in a virtual environment.
3. Set a random `RUNNER_TOKEN` of at least 32 characters in the host environment.
4. Start `uvicorn services.runner.server:app --host 127.0.0.1 --port 8080 --limit-concurrency 4` behind a TLS reverse proxy.
5. Set `RUNNER_URL` (HTTPS origin) and `RUNNER_TOKEN` in Sites runtime settings, then redeploy the workspace.

A test request includes files and their SHA-256 digest. The runner validates names, counts and bytes; it executes only `python -m pytest -q -p no:cacheprovider` with no network, a read-only filesystem, no capabilities, a non-root user, resource caps and a deadline. It returns evidence for that exact digest. Host temporary files are removed afterward. API requests should be limited to 2 MB at the reverse proxy. This release does not run arbitrary generated shell commands, install project dependencies dynamically, publish applications or self-heal.
