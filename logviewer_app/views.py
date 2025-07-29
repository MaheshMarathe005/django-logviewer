from django.shortcuts import render

# Create your views here.
# logviewer_app/views.py

from django.shortcuts import render
import os

from django.shortcuts import render
from .forms import LogSearchForm
from logs.logparser import parse_log

def index(request):
    entries = []
    form = LogSearchForm(request.GET or None)
    if form.is_valid():
        log_file = form.cleaned_data['log_file']
        keyword = form.cleaned_data['keyword']
        entries = parse_log(log_file, keyword)
    return render(request, 'index.html', {'form': form, 'entries': entries})

LOG_FILES = {
    'Squid Access Log': '/var/log/squid/access.log',
    'Squid Cache Log': '/var/log/squid/cache.log',
    'Auth Log': '/var/log/auth.log',  # Authentication and sudo access
    'Syslog': '/var/log/syslog',  # General system messages
    'Kernel Log': '/var/log/kern.log',  # Kernel messages
    'Boot Log': '/var/log/boot.log',  # Boot process
    'Daemon Log': '/var/log/daemon.log',  # Daemon-related logs
    'Cron Log': '/var/log/cron.log',  # Cron job scheduler logs
    'Dmesg Log': '/var/log/dmesg',  # Hardware-related messages during boot
    'Xorg Log': '/var/log/Xorg.0.log',  # Display server (Xorg) logs
    'UFW Firewall Log': '/var/log/ufw.log',  # UFW firewall rules logging
    'APT History Log': '/var/log/apt/history.log',  # Package install/remove
    'APT Term Log': '/var/log/apt/term.log',  # Terminal output of APT
    'Fail2Ban Log': '/var/log/fail2ban.log',  # Banned IPs due to brute-force
    'MySQL Log': '/var/log/mysql/error.log',  # MySQL/MariaDB logs
    'Apache Access Log': '/var/log/apache2/access.log',  # Web server access
    'Apache Error Log': '/var/log/apache2/error.log',
    'Nginx Access Log': '/var/log/nginx/access.log',  # Web server (Nginx)
    'Nginx Error Log': '/var/log/nginx/error.log',
    'Mail Log': '/var/log/mail.log',  # Mail activity log
    'Audit Log': '/var/log/audit/audit.log',  # SELinux/auditd logs
    'Docker Log (systemd)': 'journalctl -u docker',  # Docker service logs
    'Journal Log': 'journalctl -xe',  # Detailed systemd journal log
}

def view_logs(request):
    choices = [(key, key) for key in LOG_FILES.keys()]
    form = LogSearchForm(request.GET or None)
    form.fields['log_file'].choices = choices

    entries = []
    log_content = ""
    selected_log = request.GET.get('log_file')
    keyword = request.GET.get('keyword', '')

    if selected_log in LOG_FILES:
        path = LOG_FILES[selected_log]
        if os.path.exists(path):
            with open(path, 'r') as file:
                lines = file.readlines()
                log_content = "".join(lines)
                for line in lines:
                    if keyword.lower() in line.lower():
                        entries.append({
                            'timestamp': line.split()[0] if line.strip() else '',
                            'content': line.strip()
                        })

    return render(request, 'logviewer_app/index.html',{
        'form': form,
        'entries': entries,
        'selected_log': selected_log,
        'log_content': log_content,
    })