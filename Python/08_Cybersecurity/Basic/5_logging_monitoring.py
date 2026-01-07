#!/usr/bin/env python3
"""
Logging, Monitoring & Alerting Examples
-------------------------------------
This script demonstrates logging, monitoring, and alerting concepts in Python:
1. Secure event logging with timestamps
2. System resource monitoring
3. Log anomaly detection
4. Alert notification mechanisms
"""

import os
import sys
import time
import json
import smtplib
import logging
import datetime
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psutil
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
import ssl


# ---- 1. Secure Event Logging ----

class SecureLogger:
    """Secure logging implementation with proper formatting and output options"""
    
    def __init__(self, app_name, log_dir=None, log_level=logging.INFO, 
                 max_size_mb=10, backup_count=5, use_json=True):
        """Initialize secure logger"""
        self.app_name = app_name
        self.log_level = log_level
        self.use_json = use_json
        
        # Set log directory
        if log_dir is None:
            self.log_dir = os.path.join(os.getcwd(), 'logs')
        else:
            self.log_dir = log_dir
            
        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
                print(f"Created log directory: {self.log_dir}")
            except OSError as e:
                print(f"Error creating log directory: {e}")
                self.log_dir = os.getcwd()
                
        # Set log file path
        self.log_file = os.path.join(self.log_dir, f"{app_name.lower().replace(' ', '_')}.log")
        
        # Set up logger
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Create rotating file handler
        max_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Set log format based on preference
        if use_json:
            # JSON formatter for structured logging
            json_formatter = jsonlogger.JsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s',
                rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
            )
            file_handler.setFormatter(json_formatter)
            console_handler.setFormatter(json_formatter)
        else:
            # Standard formatter
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log initialization
        self.info(f"Logger initialized for {app_name}")
    
    def debug(self, message, **kwargs):
        """Log debug message with optional context data"""
        self._log(logging.DEBUG, message, kwargs)
        
    def info(self, message, **kwargs):
        """Log info message with optional context data"""
        self._log(logging.INFO, message, kwargs)
        
    def warning(self, message, **kwargs):
        """Log warning message with optional context data"""
        self._log(logging.WARNING, message, kwargs)
        
    def error(self, message, **kwargs):
        """Log error message with optional context data"""
        self._log(logging.ERROR, message, kwargs)
        
    def critical(self, message, **kwargs):
        """Log critical message with optional context data"""
        self._log(logging.CRITICAL, message, kwargs)
        
    def _log(self, level, message, context=None):
        """Internal method to handle logging with context"""
        if context:
            # If using JSON logger, we can just pass the context dict
            if self.use_json:
                self.logger.log(level, message, extra=context)
            else:
                # Format context data for standard logger
                context_str = ' '.join([f"{k}={v}" for k, v in context.items()])
                self.logger.log(level, f"{message} - {context_str}")
        else:
            self.logger.log(level, message)
    
    def get_log_file_path(self):
        """Return the current log file path"""
        return self.log_file


# ---- 2. System Resource Monitoring ----

class SystemMonitor:
    """Monitor system resources and log abnormal conditions"""
    
    def __init__(self, logger=None):
        """Initialize with optional logger"""
        self.logger = logger
        
        # Set thresholds for alerts
        self.thresholds = {
            'cpu_percent': 80.0,       # 80% CPU usage
            'memory_percent': 85.0,    # 85% memory usage
            'disk_percent': 90.0,      # 90% disk usage
            'swap_percent': 70.0,      # 70% swap usage
            'net_error_rate': 0.05,    # 5% network error rate
            'load_avg_factor': 1.5     # Load average > 1.5x CPU count
        }
        
        # State tracking
        self.monitoring = False
        self.monitor_thread = None
        self.history = {
            'cpu': [],
            'memory': [],
            'disk': [],
            'network': []
        }
    
    def log(self, level, message, **kwargs):
        """Log a message if a logger is available"""
        if self.logger:
            if level == 'debug':
                self.logger.debug(message, **kwargs)
            elif level == 'info':
                self.logger.info(message, **kwargs)
            elif level == 'warning':
                self.logger.warning(message, **kwargs)
            elif level == 'error':
                self.logger.error(message, **kwargs)
            elif level == 'critical':
                self.logger.critical(message, **kwargs)
        else:
            print(f"[{level.upper()}] {message}")
    
    def get_system_info(self):
        """Get current system resource information"""
        info = {
            'timestamp': datetime.datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'swap': {
                'total': psutil.swap_memory().total,
                'used': psutil.swap_memory().used,
                'percent': psutil.swap_memory().percent
            },
            'disk': {}
        }
        
        # Get disk usage for each mounted partition
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info['disk'][partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'percent': usage.percent
                }
            except (PermissionError, OSError):
                # Skip if we can't access the drive
                pass
        
        # Get network stats
        net_io = psutil.net_io_counters()
        info['network'] = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout
        }
        
        # Record history for trend analysis
        self._update_history(info)
        
        return info
    
    def _update_history(self, info):
        """Update monitoring history"""
        # Keep history limited to prevent memory issues
        max_history = 60  # Keep only 60 data points
        
        # Add current values to history
        self.history['cpu'].append(info['cpu']['percent'])
        self.history['memory'].append(info['memory']['percent'])
        
        # Calculate average disk usage
        if info['disk']:
            avg_disk_percent = sum(d['percent'] for d in info['disk'].values()) / len(info['disk'])
            self.history['disk'].append(avg_disk_percent)
        
        # Add network error data
        net_info = info['network']
        total_packets = net_info['packets_sent'] + net_info['packets_recv']
        total_errors = net_info['errin'] + net_info['errout']
        
        error_rate = 0
        if total_packets > 0:
            error_rate = total_errors / total_packets
            
        self.history['network'].append(error_rate)
        
        # Trim history if needed
        for key in self.history:
            if len(self.history[key]) > max_history:
                self.history[key] = self.history[key][-max_history:]
    
    def check_thresholds(self, info):
        """Check if current metrics exceed thresholds"""
        alerts = []
        
        # Check CPU
        if info['cpu']['percent'] > self.thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'warning',
                'message': f"High CPU usage: {info['cpu']['percent']}%",
                'current': info['cpu']['percent'],
                'threshold': self.thresholds['cpu_percent']
            })
        
        # Check memory
        if info['memory']['percent'] > self.thresholds['memory_percent']:
            alerts.append({
                'type': 'memory_high',
                'severity': 'warning',
                'message': f"High memory usage: {info['memory']['percent']}%",
                'current': info['memory']['percent'],
                'threshold': self.thresholds['memory_percent']
            })
        
        # Check disk
        for mount, data in info['disk'].items():
            if data['percent'] > self.thresholds['disk_percent']:
                alerts.append({
                    'type': 'disk_high',
                    'severity': 'warning',
                    'message': f"High disk usage on {mount}: {data['percent']}%",
                    'current': data['percent'],
                    'threshold': self.thresholds['disk_percent'],
                    'mount': mount
                })
        
        # Check load average (on Unix systems)
        if info['cpu']['load_avg'] is not None:
            cpu_count = info['cpu']['count']
            if cpu_count > 0:  # Avoid division by zero
                load_1min = info['cpu']['load_avg'][0]
                if load_1min > cpu_count * self.thresholds['load_avg_factor']:
                    alerts.append({
                        'type': 'load_high',
                        'severity': 'warning',
                        'message': f"High system load: {load_1min:.2f} (threshold: {cpu_count * self.thresholds['load_avg_factor']:.2f})",
                        'current': load_1min,
                        'threshold': cpu_count * self.thresholds['load_avg_factor']
                    })
        
        return alerts
    
    def detect_anomalies(self):
        """Detect anomalies based on historical data"""
        anomalies = []
        
        # Need enough history for anomaly detection
        if all(len(self.history[key]) >= 10 for key in self.history):
            # Calculate moving averages
            for key in self.history:
                # Skip if not enough data
                if not self.history[key]:
                    continue
                    
                # Get recent and historical values
                current = self.history[key][-1]
                recent_avg = sum(self.history[key][-5:]) / 5
                historical_avg = sum(self.history[key][:-5]) / max(1, len(self.history[key]) - 5)
                
                # Detect sudden spikes (more than 2x recent average)
                if current > recent_avg * 2 and recent_avg > 0:
                    anomalies.append({
                        'type': f"{key}_spike",
                        'severity': 'warning',
                        'message': f"Sudden {key} spike detected: {current:.2f}% (2x above recent average)",
                        'current': current,
                        'recent_avg': recent_avg
                    })
                
                # Detect trend changes (recent avg 50% higher than historical)
                if recent_avg > historical_avg * 1.5 and historical_avg > 0:
                    anomalies.append({
                        'type': f"{key}_trend_up",
                        'severity': 'info',
                        'message': f"Upward trend in {key}: recent avg {recent_avg:.2f}% vs historical {historical_avg:.2f}%",
                        'recent_avg': recent_avg,
                        'historical_avg': historical_avg
                    })
        
        return anomalies
    
    def start_monitoring(self, interval=60):
        """Start monitoring in a background thread"""
        if self.monitoring:
            self.log('info', "Monitoring is already active")
            return False
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        
        self.log('info', f"System monitoring started with {interval}s interval")
        return True
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        if not self.monitoring:
            return False
            
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
            
        self.log('info', "System monitoring stopped")
        return True
    
    def _monitoring_loop(self, interval):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # Get system info
                info = self.get_system_info()
                
                # Check thresholds
                alerts = self.check_thresholds(info)
                
                # Check for anomalies
                anomalies = self.detect_anomalies()
                
                # Log alerts and anomalies
                for alert in alerts:
                    self.log('warning', alert['message'], alert_type=alert['type'])
                
                for anomaly in anomalies:
                    self.log('warning', anomaly['message'], anomaly_type=anomaly['type'])
                    
            except Exception as e:
                self.log('error', f"Error in monitoring loop: {e}")
                
            # Sleep until next check
            time.sleep(interval)


# ---- 3. Alert Notification ----

class AlertNotifier:
    """Send alerts via various notification channels"""
    
    def __init__(self, app_name):
        """Initialize alert notifier"""
        self.app_name = app_name
        self.channels = {}
    
    def add_email_channel(self, smtp_server, port, username, password, use_tls=True):
        """Configure email notification channel"""
        self.channels['email'] = {
            'type': 'email',
            'smtp_server': smtp_server,
            'port': port,
            'username': username,
            'password': password,
            'use_tls': use_tls,
            'recipients': []
        }
        
    def add_email_recipient(self, email):
        """Add email recipient"""
        if 'email' in self.channels:
            if email not in self.channels['email']['recipients']:
                self.channels['email']['recipients'].append(email)
                return True
        return False
    
    def add_slack_channel(self, webhook_url, channel=None):
        """Configure Slack notification channel"""
        self.channels['slack'] = {
            'type': 'slack',
            'webhook_url': webhook_url,
            'channel': channel
        }
    
    def notify(self, subject, message, severity='info', channel_type=None):
        """Send notification to all or specified channels"""
        if not self.channels:
            print("No notification channels configured")
            return False
            
        success = False
        
        # Send to specific channel type or all channels
        if channel_type and channel_type in self.channels:
            channels = {channel_type: self.channels[channel_type]}
        else:
            channels = self.channels
            
        # Send notification through each configured channel
        for name, config in channels.items():
            try:
                if name == 'email':
                    success = self._send_email(subject, message, severity, config)
                elif name == 'slack':
                    success = self._send_slack(subject, message, severity, config)
            except Exception as e:
                print(f"Error sending {name} notification: {e}")
                
        return success
    
    def _send_email(self, subject, message, severity, config):
        """Send email notification"""
        if not config['recipients']:
            return False
            
        # Prepare email
        msg = MIMEMultipart()
        msg['From'] = config['username']
        msg['To'] = ', '.join(config['recipients'])
        msg['Subject'] = f"[{severity.upper()}] {self.app_name}: {subject}"
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>{subject}</h2>
            <p><strong>Severity:</strong> {severity}</p>
            <p><strong>Time:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Application:</strong> {self.app_name}</p>
            <hr>
            <pre>{message}</pre>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server
        try:
            if config['use_tls']:
                context = ssl.create_default_context()
                server = smtplib.SMTP(config['smtp_server'], config['port'])
                server.starttls(context=context)
            else:
                server = smtplib.SMTP(config['smtp_server'], config['port'])
                
            server.login(config['username'], config['password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def _send_slack(self, subject, message, severity, config):
        """Send Slack notification via webhook"""
        # In a real implementation, we would use the Slack API
        # For this demo, we'll just simulate it
        
        # Get color based on severity
        color_map = {
            'info': '#2196F3',     # Blue
            'warning': '#FF9800',  # Orange
            'error': '#F44336',    # Red
            'critical': '#9C27B0'  # Purple
        }
        color = color_map.get(severity.lower(), '#2196F3')
        
        # Create payload
        payload = {
            'attachments': [{
                'fallback': f"{subject}: {message}",
                'color': color,
                'title': subject,
                'text': message,
                'fields': [
                    {
                        'title': 'Severity',
                        'value': severity.upper(),
                        'short': True
                    },
                    {
                        'title': 'Application',
                        'value': self.app_name,
                        'short': True
                    },
                    {
                        'title': 'Time',
                        'value': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'short': True
                    }
                ]
            }]
        }
        
        # Add channel if specified
        if config['channel']:
            payload['channel'] = config['channel']
            
        # In a real implementation, we would send an HTTP POST request like this:
        # response = requests.post(config['webhook_url'], json=payload)
        # return response.status_code == 200
        
        # For demonstration, just print the payload
        print(f"[DEMO] Would send Slack notification: {json.dumps(payload, indent=2)}")
        return True


# ---- Demo ----

def demonstrate_logging_monitoring():
    print("===== LOGGING, MONITORING & ALERTING DEMO =====\n")
    
    # 1. Secure Event Logging
    print("1. Secure Event Logging Demo")
    logger = SecureLogger("SecurityDemoApp", use_json=True)
    
    logger.info("Application started successfully")
    logger.debug("Debug message with context", user="admin", ip="192.168.1.1")
    logger.warning("Unusual login pattern detected", 
                  user="user123", ip="203.0.113.42", attempts=5)
    logger.error("Authentication failure", 
                user="unknown", ip="198.51.100.77", reason="invalid_credentials")
    
    print(f"Log file saved to: {logger.get_log_file_path()}")
    print("")
    
    # 2. System Resource Monitoring
    print("2. System Resource Monitoring Demo")
    monitor = SystemMonitor(logger)
    
    # Get current system info
    system_info = monitor.get_system_info()
    
    # Display system info
    print("\nCurrent System Information:")
    print(f"CPU Usage: {system_info['cpu']['percent']}%")
    print(f"Memory Usage: {system_info['memory']['percent']}%")
    print(f"Swap Usage: {system_info['swap']['percent']}%")
    
    # Show disk usage
    print("\nDisk Usage:")
    for mount, data in system_info['disk'].items():
        print(f"  {mount}: {data['percent']}% used " +
              f"({data['used'] / (1024**3):.1f} GB / {data['total'] / (1024**3):.1f} GB)")
    
    # Demo threshold check
    print("\nChecking resource thresholds...")
    alerts = monitor.check_thresholds(system_info)
    if alerts:
        for alert in alerts:
            print(f"ALERT: {alert['message']} (Threshold: {alert['threshold']})")
    else:
        print("No threshold alerts triggered")
    
    # Short demo of monitoring loop (only for a few seconds)
    print("\nStarting monitoring for 5 seconds...")
    monitor.start_monitoring(interval=1)
    time.sleep(5)
    monitor.stop_monitoring()
    print("")
    
    # 3. Alert Notification
    print("3. Alert Notification Demo")
    notifier = AlertNotifier("Security Monitor")
    
    # Configure email (demonstration only, not actually sending)
    notifier.add_email_channel("smtp.example.com", 587, "alerts@example.com", 
                              "password", use_tls=True)
    notifier.add_email_recipient("admin@example.com")
    
    # Configure Slack (demonstration only)
    notifier.add_slack_channel("https://hooks.slack.com/services/Txxxxxx/Bxxxxxx/xxxxxxxx")
    
    # Send demo alerts
    print("\nSimulating alert notifications (not actually sending):")
    notifier.notify(
        subject="High CPU Usage Detected",
        message="CPU usage has been above 90% for 5 minutes.",
        severity="warning"
    )
    
    notifier.notify(
        subject="Failed Login Attempts",
        message="Multiple failed login attempts detected from IP 203.0.113.42",
        severity="error"
    )
    
    print("\nDemo completed!")


if __name__ == "__main__":
    demonstrate_logging_monitoring()
