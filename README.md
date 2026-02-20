# AsyncIO Asymmetric Stress Tester

## Overview
An enterprise-grade Denial-of-Service simulator built to research web server resource exhaustion. This engine utilizes asynchronous I/O to launch hundreds of concurrent connections on a single thread. It includes a built-in vulnerable testing server to demonstrate the attack lifecycle safely.

## Mechanism
The script initiates a synchronous web server in the background and provides a 15-second grace period to establish a baseline. Once the grace period expires, the AsyncIO event loop launches a starvation attack. It opens hundreds of connections and maintains them with slow keep-alive headers. The server connection pool fills entirely, resulting in an absolute denial of service at the OS network layer.

## Features
* **True Concurrency:** Manages hundreds of simultaneous network locks without GIL bottlenecking.
* **Live Telemetry:** Real-time terminal dashboard tracking active locks, dropped connections, and server latency.
* **Self-Contained Architecture:** Houses both the vulnerable target and the attacker engine in a single execution flow for localized testing.

## Execution Guide
1. Clone the repository:
   ```bash
   git clone [https://github.com/this-is-the-invincible-meghnad/Async-DoS-Engine.git](https://github.com/this-is-the-invincible-meghnad/Async-DoS-Engine.git)
   cd Async-DoS-Engine
   ```
## Execution

```bash
python sandbox.py
```