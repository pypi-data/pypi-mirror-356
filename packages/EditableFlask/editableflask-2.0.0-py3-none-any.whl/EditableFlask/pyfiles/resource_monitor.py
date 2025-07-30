def ENABLE_RESOURCE_MONITER(app, edits):
    import psutil
    import platform
    import socket
    import subprocess
    from flask import jsonify, render_template
    from datetime import datetime, timedelta

    @edits.route('/monitor')
    def monitor():
        return render_template("monitor.html")

    @edits.route('/monitor/stats')
    def monitor_stats():
        def get_gpu_info():
            try:
                if platform.system() == "Windows":
                    output = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
                    return output.decode().strip().split("\n")[1:]
                elif platform.system() == "Linux":
                    output = subprocess.check_output("lspci | grep VGA", shell=True)
                    return output.decode().strip().split("\n")
                elif platform.system() == "Darwin":
                    output = subprocess.check_output("system_profiler SPDisplaysDataType | grep 'Chipset Model'", shell=True)
                    return output.decode().strip().split("\n")
                else:
                    return ["Unknown GPU"]
            except Exception as e:
                return [str(e)]

        def get_uptime():
            try:
                if platform.system() == "Windows":
                    boot_time = datetime.fromtimestamp(psutil.boot_time())
                    uptime = datetime.now() - boot_time
                    return str(uptime).split('.')[0]  # Remove microseconds
                else:
                    output = subprocess.check_output("uptime -p", shell=True)
                    return output.decode().strip()
            except Exception as e:
                return str(e)

        stats = {
            "cpu_usage": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": [{"device": d.device, "usage": psutil.disk_usage(d.mountpoint).percent} for d in psutil.disk_partitions()],
            "total_processes": len(psutil.pids()),
            "os_name": platform.system(),
            "os_version": platform.version(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "uptime": get_uptime(),
            "python_version": platform.python_version(),
            "running_users": len(psutil.users()),
            "wifi_ssid": subprocess.check_output("iwgetid -r", shell=True).decode().strip() if platform.system() == "Linux" else "N/A",
            "gpu_info": get_gpu_info(),
            "host_ip": socket.gethostbyname(socket.gethostname()),
            "processor_info": platform.processor(),
        }
        return jsonify(stats)