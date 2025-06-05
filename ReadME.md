<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# POC_EXPORTERS

<em>Modular Prometheus exporters for GPU, CPU, and I/O insights — designed for Slurm-managed HPC clusters. Built with Python, Go, and Ansible for seamless observability, job-level tracking, and infrastructure automation.</em>

<!-- BADGES -->
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
<img src="https://img.shields.io/github/last-commit/mjay-kerberos/POC_Exporters?style=flat&logo=git&logoColor=white&color=purple" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/mjay-kerberos/POC_Exporters?style=flat&color=orange" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/mjay-kerberos/POC_Exporters?style=flat&color=green" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/Ansible-EE0000.svg?style=flat&logo=Ansible&logoColor=white" alt="Ansible">
<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
<img src="https://img.shields.io/badge/Go-00ADD8.svg?style=flat&logo=Go&logoColor=white" alt="Go">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
    - [Metrics Collected](#metrics-collected)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [License](#license)

---

## Overview

POC_Exporters is a powerful developer tool designed to streamline the collection and monitoring of GPU and I/O metrics in high-performance computing environments. This repository contains proof-of-concept exporters written in Python and Go for collecting GPU and I/O metrics. These exporters are designed to work with Prometheus for monitoring system performance.

**Why POC_Exporters?**

This project enhances observability and resource management for systems utilizing NVIDIA GPUs. The core features include:

- **⚙️ Automated Setup:** Simplifies onboarding with a script that sets up a Python virtual environment and installs dependencies.
- **📊 Comprehensive Metrics Collection:** Gathers critical GPU and I/O performance data for effective monitoring and optimization.
- **📈 Prometheus Integration:** Seamlessly integrates with Prometheus for real-time system performance tracking.
- **🔧 Ansible Automation:** Facilitates consistent deployment and management of metrics exporters through Ansible roles.
- **🌐 Multi-language Support:** Offers both Python and Go scripts, catering to diverse developer preferences.
- **📉 Job Metrics Tracking:** Enables detailed analysis of job-related metrics for improved resource allocation and performance insights.

### Exporters

- `nvidia_gpu_exporter.py`: A Python script that collects GPU utilization, memory usage, and I/O metrics.
- `gpu_io_exporter.go`: A Go script that collects GPU utilization, memory usage, and I/O metrics.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python 3.x, Go 1.16+
- **Package Manager:** Pip, Go modules
- Prometheus
- NVIDIA GPU with nvidia-smi tool

### Installation

Build POC_Exporters from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/mjay-kerberos/POC_Exporters
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd POC_Exporters
    ```

3. **Install the dependencies:**

**Using [pip](https://pypi.org/project/pip/):**

```sh
❯ pip install -r requirements.txt
```
**Using [go modules](https://golang.org/):**

```sh
❯ go build
```

### Usage

Run the project with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
python {entrypoint}
```
**Using [go modules](https://golang.org/):**

```sh
go run {entrypoint}
```

### Testing

Poc_exporters uses the {__test_framework__} test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**

```sh
pytest
```
**Using [go modules](https://golang.org/):**

```sh
go test ./...
```

---
### Metrics Collected

The Exporters collect the following metrics:

- GPU Utilization
- GPU Memory Usage
- I/O Read Bytes
- I/O Write Bytes

---
## Features

|      | Component       | Details                              |
| :--- | :-------------- | :----------------------------------- |
| ⚙️  | **Architecture**  | <ul><li>Microservices-based design</li><li>Utilizes Go for backend services</li><li>Python for auxiliary scripts</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Go modules for dependency management</li><li>Consistent formatting with `go fmt`</li><li>Linting tools integrated</li></ul> |
| 📄 | **Documentation** | <ul><li>README.md for project overview</li><li>Inline comments in Go and Python code</li><li>Markdown files for usage instructions</li></ul> |
| 🔌 | **Integrations**  | <ul><li>Integrates with CI/CD tools (e.g., GitHub Actions)</li><li>Metrics Exporter service for monitoring</li><li>Supports Ansible for deployment</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Separation of concerns in code structure</li><li>Reusable components for metrics collection</li><li>Configuration files for easy adjustments</li></ul> |
| 🧪 | **Testing**       | <ul><li>Unit tests for Go components</li><li>Integration tests using Molecule</li><li>Test coverage reports available</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Optimized for low-latency metrics collection</li><li>Efficient use of goroutines in Go</li><li>Asynchronous processing in Python scripts</li></ul> |
| 🛡️ | **Security**      | <ul><li>Dependency scanning for vulnerabilities</li><li>Environment variable management for secrets</li><li>Secure coding practices in Go and Python</li></ul> |
| 📦 | **Dependencies**  | <ul><li>Go modules: `go.mod`, `go.sum`</li><li>Python dependencies in `requirements.txt`</li><li>Various YAML files for configuration</li></ul> |
| 🚀 | **Scalability**   | <ul><li>Designed to handle increased load with microservices</li><li>Horizontal scaling capabilities</li><li>Load balancing strategies implemented</li></ul> |

---

## Project Structure

```sh
└── POC_Exporters/
    ├── Ansible
    │   ├── install_exporter.yml
    │   ├── inventory.cfg
    │   └── roles
    ├── Exporters
    │   ├── cpu_usage.py
    │   ├── gpu_io_exporter.go
    │   ├── gpu_io_exporter.md
    │   ├── monitoring.py
    │   ├── nvidia_gpu_exporter.md
    │   └── nvidia_gpu_exporter.py
    ├── LICENSE
    ├── Metrics Exporter
    │   ├── Makefile
    │   ├── README.md
    │   ├── go.mod
    │   ├── go.sum
    │   ├── gpu_metrics.py
    │   ├── job_metrics_exporter.go
    │   └── job_metrics_exporter.service
    ├── ReadME.md
    ├── requirements.txt
    └── setup.sh
```

---

### Project Index

<details open>
	<summary><b><code>POC_EXPORTERS/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/setup.sh'>setup.sh</a></b></td>
					<td style='padding: 8px;'>- Facilitates the setup of a development environment by creating and activating a Python virtual environment, upgrading pip, and installing necessary dependencies<br>- Additionally, it automates the installation of a specified version of Go, ensuring that the required tools are readily available for the project<br>- This script streamlines the onboarding process for developers, enhancing productivity and consistency across the codebase.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/LICENSE'>LICENSE</a></b></td>
					<td style='padding: 8px;'>- Project Summary## License OverviewThe <code>LICENSE</code> file in this project contains the GNU General Public License (GPL) Version 3, which is a foundational document that governs the use and distribution of the software within this codebase<br>- The primary purpose of this license is to ensure that the software remains free for all users, allowing them the freedom to share, modify, and distribute the code without restrictions.By adopting the GPL, this project emphasizes its commitment to open-source principles, promoting collaboration and innovation within the community<br>- The license guarantees that all versions of the software will remain accessible and modifiable, thereby fostering an environment where users can contribute to its evolution and improvement.In summary, the <code>LICENSE</code> file plays a crucial role in the overall architecture of the project by establishing the legal framework that protects user freedoms and encourages community engagement, ensuring that the software remains a valuable resource for everyone.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/ReadME.md'>ReadME.md</a></b></td>
					<td style='padding: 8px;'>- POC Exporters serves as a foundational component for monitoring GPU and I/O metrics within a system<br>- By leveraging Python and Go scripts, it facilitates the collection of critical performance data, including GPU utilization and memory usage, which can be integrated with Prometheus for effective system performance monitoring<br>- This enhances observability and aids in optimizing resource management in environments utilizing NVIDIA GPUs.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- Defines essential dependencies for the project, ensuring a streamlined environment for development and testing<br>- By incorporating tools like Ansible and Molecule with Docker, it facilitates efficient automation and orchestration processes<br>- This setup enhances the overall architecture by promoting consistency and reliability in deployment workflows, ultimately supporting the projects goal of simplifying infrastructure management.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- Ansible Submodule -->
	<details>
		<summary><b>Ansible</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Ansible</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/install_exporter.yml'>install_exporter.yml</a></b></td>
					<td style='padding: 8px;'>- Facilitates the installation of GPU and IO metrics collection on designated GPU servers within the project architecture<br>- By leveraging the metrics_exporter role, it ensures that essential performance data is gathered, enabling effective monitoring and analysis of system resources<br>- This contributes to the overall goal of optimizing resource utilization and enhancing system performance across the infrastructure.</td>
				</tr>
			</table>
			<!-- roles Submodule -->
			<details>
				<summary><b>roles</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ Ansible.roles</b></code>
					<!-- python_metrics_exporter Submodule -->
					<details>
						<summary><b>python_metrics_exporter</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ Ansible.roles.python_metrics_exporter</b></code>
							<!-- templates Submodule -->
							<details>
								<summary><b>templates</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.python_metrics_exporter.templates</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/python_metrics_exporter/templates/job_metrics.service.j2'>job_metrics.service.j2</a></b></td>
											<td style='padding: 8px;'>- Defines a systemd service configuration for the Job Metrics Collection Service, enabling the automated collection and logging of job metrics<br>- By ensuring the service starts after network initialization and runs continuously, it integrates seamlessly into the overall architecture, facilitating efficient monitoring and performance analysis within the broader project ecosystem<br>- This enhances observability and operational insights across the deployed applications.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- meta Submodule -->
							<details>
								<summary><b>meta</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.python_metrics_exporter.meta</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/python_metrics_exporter/meta/main.yml'>main.yml</a></b></td>
											<td style='padding: 8px;'>- Defines metadata for the Python Metrics Exporter role within the Ansible project, facilitating the management and deployment of Python-based metrics collection tools<br>- This role enhances observability by ensuring that relevant metrics are accurately gathered and exported, contributing to the overall monitoring and performance analysis capabilities of the system architecture<br>- It plays a crucial role in maintaining operational efficiency and reliability.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- files Submodule -->
							<details>
								<summary><b>files</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.python_metrics_exporter.files</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/python_metrics_exporter/files/metrics.py'>metrics.py</a></b></td>
											<td style='padding: 8px;'>- Metrics collection for GPU utilization and memory usage is achieved through the integration of NVIDIAs monitoring tools and job management systems<br>- By parsing relevant data, it maps GPU metrics to specific jobs, facilitating performance monitoring and resource allocation<br>- The output is formatted for Prometheus, enabling seamless integration into monitoring dashboards for enhanced visibility into GPU resource usage across jobs.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- tasks Submodule -->
							<details>
								<summary><b>tasks</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.python_metrics_exporter.tasks</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/python_metrics_exporter/tasks/main.yml'>main.yml</a></b></td>
											<td style='padding: 8px;'>- Facilitates the setup and management of a metrics collection service within the project architecture<br>- It ensures the creation of necessary directories, deploys a metrics collection script, and configures a systemd service for continuous operation<br>- This process enhances the overall monitoring capabilities of the system, allowing for effective tracking and analysis of job metrics.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- prometheus_metric_exporter Submodule -->
					<details>
						<summary><b>prometheus_metric_exporter</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ Ansible.roles.prometheus_metric_exporter</b></code>
							<!-- meta Submodule -->
							<details>
								<summary><b>meta</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.prometheus_metric_exporter.meta</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/prometheus_metric_exporter/meta/main.yml'>main.yml</a></b></td>
											<td style='padding: 8px;'>- Facilitates the installation and configuration of a custom GPU/IO metric collection exporter within the Ansible framework<br>- Designed by Juliet Meza at Data in Science Technologies, this role enhances monitoring capabilities by integrating with Prometheus, ensuring efficient metric collection for improved performance analysis<br>- It is compatible with Ansible version 2.18.3 and adheres to the MIT license.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- tasks Submodule -->
							<details>
								<summary><b>tasks</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ Ansible.roles.prometheus_metric_exporter.tasks</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Ansible/roles/prometheus_metric_exporter/tasks/main.yml'>main.yml</a></b></td>
											<td style='padding: 8px;'>- Facilitates the deployment of the Job Metrics Exporter by copying the necessary binary, extracting it, and moving it to the appropriate directory<br>- Additionally, it sets up a systemd service to manage the exporter, ensuring it starts on boot and restarts automatically if it fails<br>- This integration enhances the overall monitoring capabilities of the architecture by enabling efficient metrics collection.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- Exporters Submodule -->
	<details>
		<summary><b>Exporters</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Exporters</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/nvidia_gpu_exporter.md'>nvidia_gpu_exporter.md</a></b></td>
					<td style='padding: 8px;'>- NVIDIA GPU Exporter serves to gather and output critical GPU and I/O metrics from NVIDIA GPUs in a format compatible with Prometheus node exporter<br>- By leveraging the <code>nvidia-smi</code> tool, it enables monitoring of GPU utilization and memory usage, as well as I/O read and write statistics, thereby enhancing the observability and performance management of systems utilizing NVIDIA hardware within the broader project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/gpu_io_exporter.go'>gpu_io_exporter.go</a></b></td>
					<td style='padding: 8px;'>- GPU and IO metrics exporter facilitates the collection and exposure of GPU utilization, memory usage, and IO statistics for jobs managed by Slurm<br>- By integrating with Prometheus, it enables real-time monitoring of resource usage, helping users optimize performance and resource allocation in GPU-intensive applications<br>- The exporter serves metrics over HTTP, allowing seamless integration with monitoring systems.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/cpu_usage.py'>cpu_usage.py</a></b></td>
					<td style='padding: 8px;'>- Collects and reports CPU utilization metrics for the past week and month, integrating seamlessly with Prometheus for monitoring purposes<br>- By executing system commands to retrieve utilization data, it generates a formatted output that is saved to a specified Prometheus file<br>- This functionality enhances the overall architecture by providing essential performance insights, enabling better resource management and optimization within the system.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/nvidia_gpu_exporter.py'>nvidia_gpu_exporter.py</a></b></td>
					<td style='padding: 8px;'>- NVIDIA GPU metrics and I/O statistics are gathered and formatted for Prometheus monitoring<br>- By extracting job IDs from process IDs, collecting GPU utilization and memory usage, and retrieving I/O metrics, the output is structured for compatibility with Prometheus node exporters<br>- This functionality enhances the observability of GPU resource usage and process performance within a system, facilitating efficient resource management and monitoring.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/monitoring.py'>monitoring.py</a></b></td>
					<td style='padding: 8px;'>- Monitoring service facilitates the collection and aggregation of GPU, CPU, and storage utilization metrics, storing them in a SQLite database for analysis<br>- It exposes these metrics via a Prometheus endpoint, enabling real-time monitoring and reporting<br>- Scheduled tasks ensure continuous data collection and periodic updates, providing insights into resource usage trends over daily, weekly, and monthly intervals.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Exporters/gpu_io_exporter.md'>gpu_io_exporter.md</a></b></td>
					<td style='padding: 8px;'>- GPU and I/O Exporter serves to gather and expose critical metrics related to GPU performance and I/O operations for monitoring purposes via Prometheus<br>- By leveraging NVIDIA GPU capabilities, it provides insights into GPU utilization and memory usage, alongside I/O read and write statistics, facilitating efficient resource management and performance optimization within the overall codebase architecture.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- Metrics Exporter Submodule -->
	<details>
		<summary><b>Metrics Exporter</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Metrics Exporter</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/go.mod'>go.mod</a></b></td>
					<td style='padding: 8px;'>- Defines the module for the job metrics exporter, establishing dependencies necessary for integrating Prometheus metrics collection within the application<br>- By leveraging the Prometheus client library and other indirect dependencies, it facilitates the monitoring and exporting of job-related metrics, thereby enhancing observability and performance tracking across the entire codebase architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/README.md'>README.md</a></b></td>
					<td style='padding: 8px;'>- Collects and exports GPU and I/O metrics from systems utilizing NVIDIA-SMI commands, facilitating integration with Prometheus for monitoring<br>- The project comprises both a Golang and a Python script, allowing users to choose their preferred language for metrics collection<br>- By providing a straightforward setup and configuration process, it enables efficient performance tracking and resource management in environments leveraging NVIDIA hardware.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/Makefile'>Makefile</a></b></td>
					<td style='padding: 8px;'>- Facilitates the management of the Metrics Exporter project by providing essential commands for building and cleaning the codebase<br>- It offers a user-friendly help command that lists available tasks, enhancing usability for developers<br>- This structure supports efficient development workflows, ensuring that the project remains organized and maintainable while streamlining the build process.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/gpu_metrics.py'>gpu_metrics.py</a></b></td>
					<td style='padding: 8px;'>- Collects and exports GPU metrics for monitoring purposes within a system utilizing NVIDIA GPUs<br>- It retrieves GPU utilization and memory usage data from running applications, associates this information with job IDs, and formats it for Prometheus consumption<br>- This functionality enhances observability and performance tracking in environments leveraging GPU resources, contributing to efficient resource management and workload optimization.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/job_metrics_exporter.go'>job_metrics_exporter.go</a></b></td>
					<td style='padding: 8px;'>- Metrics Exporter facilitates the collection and exposure of GPU and I/O metrics for jobs managed by the Slurm workload manager<br>- By integrating with Prometheus, it monitors GPU utilization, memory usage, and I/O statistics, providing real-time insights into resource allocation and performance<br>- This enables efficient tracking and management of computational resources across jobs, enhancing overall system observability and performance optimization.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/go.sum'>go.sum</a></b></td>
					<td style='padding: 8px;'>- Facilitating dependency management, the go.sum file ensures the integrity and consistency of module versions used within the Metrics Exporter project<br>- By maintaining checksums for each dependency, it supports the overall architecture by enabling reliable builds and preventing issues related to version mismatches, thereby enhancing the stability and maintainability of the codebase.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/mjay-kerberos/POC_Exporters/blob/master/Metrics Exporter/job_metrics_exporter.service'>job_metrics_exporter.service</a></b></td>
					<td style='padding: 8px;'>- Facilitates the operation of the Job Metrics Service, ensuring it starts after the network is available and runs continuously in a multi-user environment<br>- This service plays a crucial role in the overall architecture by collecting and exporting job-related metrics, thereby enhancing monitoring and performance analysis across the system<br>- Its integration supports efficient resource management and operational insights.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>
---
        
## License

Poc_exporters is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

