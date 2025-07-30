# 🍪 CookieFarm - Exploiter Manager

![Language](https://img.shields.io/badge/languages-Python-yellowgreen)
![Keywords](https://img.shields.io/badge/keywords-CTF%2C%20Exploiting%2C%20Attack%20Defense-red)
![License](https://img.shields.io/badge/license-MIT-blue)

> Python decorator for automating exploit execution in CTF Attack & Defense competitions

---

## 📦 What is it?

This package provides a **`@exploit_manager` decorator** designed to automate the parallel execution of exploits in CTF (*Attack & Defense*) settings, specifically for use with the [CookieFarm](https://github.com/BytesTheCookies/CookieFarm) project.

It handles:

* Authentication with the central server
* Retrieving team configuration
* Asynchronous dispatch of exploits to multiple targets
* Automatic flag parsing from `stdout`

> ⚠️ **Note:** This package is **not standalone**. It must be used together with the [CookieFarm client](https://github.com/BytesTheCookies/CookieFarm). The client provides the required APIs and team configurations.

---

## 📦 Installation

To install the package:
```bash
pip install cookiefarm-exploiter
```


## ⚙️ How it works

The `@exploit_manager` decorator takes care of:

* Calling your `exploit(ip, port, name_service)` function
* Capturing your exploit's `stdout`
* Parsing flags via regex
* Logging the result in JSON format, including: team ID, port, service name, and the flag found

All of this is done in parallel using `asyncio` and `ThreadPoolExecutor`, making the process **extremely efficient**, even with dozens of teams.

---

## 🚀 Example usage

```python
from cookiefarm_exploiter import exploit_manager
import requests

@exploit_manager
def exploit(ip, port, name_service):
    # Run your exploit here
    response = requests.get(f"http://{ip}:{port}/")

    # Just print the flag to stdout
    print(response.text)

# Run from the command line with arguments from CookieFarm
# python3 myexploit.py <ip_server> <password> <tick_time> <thread_number> <port> <name_service>
```

For execution, you have to pass the required arguments from the command line, which are provided by the CookieFarm client. The decorator will handle the rest.

```bash

python3 myexploit.py <server_address> <tick_time> <thread_number> <port> <name_service>
```

Where:

* `<server_address>`: The address of the CookieFarm server
* `<tick_time>`: The time interval for the exploit to run
* `<thread_number>`: The number of threads to use for parallel execution
* `<port>`: The port of the service to exploit
* `<name_service>`: The name of the service being exploited

---

## 🛠️ Requirements

* Python ≥ 3.12
* Working CookieFarm client installed


---

## 📝 License

Distributed under the [MIT License](LICENSE). Feel free to use, modify, and contribute.

---

For any questions, suggestions, or issues, feel free to open a [GitHub issue](https://www.github.com/BytesTheCookies/CookieFarmExploiter)!

**Created with ❤️ by ByteTheCookies (feat. @0xMatte)**
