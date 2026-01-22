# Log: SysOps Sentinel

## Historical Background (Synthesized from History)
The SysOps Sentinel orchestrated the containerization and remote deployment of the SPMO Suite.

### Key Milestones
- **Docker Orchestration (Jan 2026)**: Configured `docker-compose.yml` to run four applications and a shared PostgreSQL database.
- **Nginx Subdomain Routing**: Implemented virtual host routing for:
  - `sspmo.up.edu.ph`
  - `gamit.sspmo.up.edu.ph`
  - `lipad.sspmo.up.edu.ph`
  - `suplay.sspmo.up.edu.ph`
- **Remote Server Setup**: Configured the remote server (`172.20.3.91`) with custom SSH port `9913` and optimized resource allocation (15GB RAM).

### Infrastructure Details
- **OS**: Alpine Linux (Containers) / Windows (Local Development).
- **Service Stack**: Django + WhiteNoise + PostgreSQL 15 + Nginx.
- **Network**: Isolated Docker bridge network.
