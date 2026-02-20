# Asymmetric Resource Exhaustion Simulator

## Overview
This tool demonstrates the mechanics of a Denial-of-Service (DoS) attack targeting web server connection pools. Instead of utilizing high-bandwidth volumetric flooding, it exploits how servers handle concurrent TCP connections.

## Mechanism
The engine opens a set number of connections to the target server and sends partial HTTP requests. It maintains these connections by sending subsequent headers at extremely slow intervals. Because the server keeps the thread open waiting for the request to complete, the connection pool eventually fills up, denying service to legitimate traffic. 

**Disclaimer:** Built strictly for educational use and defensive research in local environments. Do not deploy on unauthorized infrastructure.

## Execution
Run a local web server (e.g., Flask on port 5000), then execute the simulator:
```bash
python asymmetric_dos.py
```
## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/this-is-the-invincible-meghnad/Asymmetric-DoS.git](https://github.com/this-is-the-invincible-meghnad/Asymmetric-DoS.git)
   cd Asymmetric-DoS
   ```