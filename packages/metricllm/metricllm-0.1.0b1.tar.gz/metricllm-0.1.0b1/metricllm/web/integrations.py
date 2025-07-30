"""
Integration components for external services and webhooks.
"""

import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import os
from urllib.parse import urljoin

from metricllm.utils.logging import get_logger


class WebhookHandler:
    """Handle webhook notifications for MetricLLM events."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.webhooks = {}

    def register_webhook(self, name: str, url: str, events: List[str], headers: Optional[Dict] = None):
        """Register a webhook endpoint."""
        self.webhooks[name] = {
            "url": url,
            "events": events,
            "headers": headers or {},
            "active": True
        }
        self.logger.info(f"Registered webhook '{name}' for events: {events}")

    def send_webhook(self, event: str, data: Dict[str, Any]):
        """Send webhook notification for an event."""
        for name, config in self.webhooks.items():
            if not config["active"] or event not in config["events"]:
                continue

            try:
                payload = {
                    "event": event,
                    "timestamp": datetime.now().isoformat(),
                    "data": data
                }

                response = requests.post(
                    config["url"],
                    json=payload,
                    headers=config["headers"],
                    timeout=10
                )

                if response.status_code == 200:
                    self.logger.info(f"Webhook '{name}' sent successfully for event '{event}'")
                else:
                    self.logger.warning(f"Webhook '{name}' failed with status {response.status_code}")

            except Exception as e:
                self.logger.error(f"Failed to send webhook '{name}': {str(e)}")

    def notify_llm_call(self, trace_id: str, provider: str, model: str, status: str, metrics: Dict):
        """Send notification for LLM call completion."""
        self.send_webhook("llm_call_completed", {
            "trace_id": trace_id,
            "provider": provider,
            "model": model,
            "status": status,
            "execution_time": metrics.get("execution_time_seconds", 0),
            "tokens": metrics.get("total_tokens", 0),
            "cost": metrics.get("estimated_cost_usd", 0)
        })

    def notify_safety_alert(self, trace_id: str, safety_score: float, safety_level: str, recommendations: List[str]):
        """Send notification for safety alerts."""
        if safety_level in ["high_risk", "critical_risk"]:
            self.send_webhook("safety_alert", {
                "trace_id": trace_id,
                "safety_score": safety_score,
                "safety_level": safety_level,
                "recommendations": recommendations,
                "severity": "high" if safety_level == "critical_risk" else "medium"
            })


class SlackIntegration:
    """Integration with Slack for notifications."""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        self.logger = get_logger(__name__)

    def send_message(self, message: str, channel: Optional[str] = None, username: str = "MetricLLM"):
        """Send a message to Slack."""
        if not self.webhook_url:
            self.logger.warning("Slack webhook URL not configured")
            return False

        try:
            payload = {
                "text": message,
                "username": username,
                "icon_emoji": ":robot_face:"
            }

            if channel:
                payload["channel"] = channel

            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code == 200:
                self.logger.info("Slack message sent successfully")
                return True
            else:
                self.logger.warning(f"Slack message failed with status {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to send Slack message: {str(e)}")
            return False

    def send_metric_alert(self, metric_name: str, value: float, threshold: float, severity: str = "warning"):
        """Send a metric alert to Slack."""
        severity_emojis = {
            "info": ":information_source:",
            "warning": ":warning:",
            "error": ":exclamation:",
            "critical": ":rotating_light:"
        }

        emoji = severity_emojis.get(severity, ":information_source:")
        message = f"{emoji} *MetricLLM Alert*\n"
        message += f"Metric: {metric_name}\n"
        message += f"Current Value: {value}\n"
        message += f"Threshold: {threshold}\n"
        message += f"Severity: {severity.upper()}\n"
        message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        return self.send_message(message)

    def send_safety_alert(self, trace_id: str, safety_score: float, safety_level: str):
        """Send a safety alert to Slack."""
        emoji = ":rotating_light:" if safety_level == "critical_risk" else ":warning:"
        message = f"{emoji} *MetricLLM Safety Alert*\n"
        message += f"Trace ID: {trace_id}\n"
        message += f"Safety Score: {safety_score:.2f}\n"
        message += f"Safety Level: {safety_level.replace('_', ' ').title()}\n"
        message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += "Please review the content for potential issues."

        return self.send_message(message)

    def send_daily_summary(self, summary_data: Dict[str, Any]):
        """Send a daily summary to Slack."""
        message = ":chart_with_upwards_trend: *MetricLLM Daily Summary*\n"
        message += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        message += f"• Total Calls: {summary_data.get('total_calls', 0):,}\n"
        message += f"• Total Tokens: {summary_data.get('total_tokens', 0):,}\n"
        message += f"• Total Cost: ${summary_data.get('total_cost', 0):.4f}\n"
        message += f"• Average Response Time: {summary_data.get('avg_response_time', 0):.3f}s\n"
        message += f"• Success Rate: {summary_data.get('success_rate', 0):.1f}%\n"

        providers = summary_data.get('providers', {})
        if providers:
            message += f"\n*Top Providers:*\n"
            for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True)[:3]:
                message += f"• {provider}: {count:,} calls\n"

        return self.send_message(message)


class EmailNotifier:
    """Email notification service for MetricLLM."""

    def __init__(self, smtp_server: Optional[str] = None, smtp_port: int = 587,
                 smtp_username: Optional[str] = None, smtp_password: Optional[str] = None):
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER")
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username or os.getenv("SMTP_USERNAME")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.logger = get_logger(__name__)

    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: Optional[str] = None):
        """Send an email notification."""
        if not all([self.smtp_server, self.smtp_username, self.smtp_password]):
            self.logger.warning("Email configuration incomplete")
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_username
            msg['To'] = ', '.join(to_emails)

            # Add plain text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)

            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            self.logger.info(f"Email sent successfully to {len(to_emails)} recipients")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_alert_email(self, to_emails: List[str], alert_type: str, details: Dict[str, Any]):
        """Send an alert email."""
        subject = f"MetricLLM Alert: {alert_type.replace('_', ' ').title()}"

        body = f"MetricLLM Alert\n"
        body += f"================\n\n"
        body += f"Alert Type: {alert_type.replace('_', ' ').title()}\n"
        body += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        body += "Details:\n"

        for key, value in details.items():
            body += f"- {key.replace('_', ' ').title()}: {value}\n"

        body += f"\nPlease check the MetricLLM dashboard for more information."

        html_body = f"""
        <html>
        <body>
            <h2>MetricLLM Alert</h2>
            <p><strong>Alert Type:</strong> {alert_type.replace('_', ' ').title()}</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h3>Details:</h3>
            <ul>
        """

        for key, value in details.items():
            html_body += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"

        html_body += """
            </ul>
            <p>Please check the MetricLLM dashboard for more information.</p>
        </body>
        </html>
        """

        return self.send_email(to_emails, subject, body, html_body)

    def send_weekly_report(self, to_emails: List[str], report_data: Dict[str, Any]):
        """Send a weekly report email."""
        subject = f"MetricLLM Weekly Report - {datetime.now().strftime('%Y-%m-%d')}"

        body = f"MetricLLM Weekly Report\n"
        body += f"=======================\n\n"
        body += f"Week ending: {datetime.now().strftime('%Y-%m-%d')}\n\n"

        # Summary statistics
        body += "Summary Statistics:\n"
        body += f"- Total LLM Calls: {report_data.get('total_calls', 0):,}\n"
        body += f"- Total Tokens Used: {report_data.get('total_tokens', 0):,}\n"
        body += f"- Total Cost: ${report_data.get('total_cost', 0):.2f}\n"
        body += f"- Average Response Time: {report_data.get('avg_response_time', 0):.3f}s\n"
        body += f"- Success Rate: {report_data.get('success_rate', 0):.1f}%\n\n"

        # Top providers
        providers = report_data.get('providers', {})
        if providers:
            body += "Top Providers:\n"
            for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True)[:5]:
                body += f"- {provider}: {count:,} calls\n"

        # Create HTML version
        html_body = f"""
        <html>
        <body>
            <h2>MetricLLM Weekly Report</h2>
            <p><strong>Week ending:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            
            <h3>Summary Statistics</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr><td><strong>Total LLM Calls</strong></td><td>{report_data.get('total_calls', 0):,}</td></tr>
                <tr><td><strong>Total Tokens Used</strong></td><td>{report_data.get('total_tokens', 0):,}</td></tr>
                <tr><td><strong>Total Cost</strong></td><td>${report_data.get('total_cost', 0):.2f}</td></tr>
                <tr><td><strong>Average Response Time</strong></td><td>{report_data.get('avg_response_time', 0):.3f}s</td></tr>
                <tr><td><strong>Success Rate</strong></td><td>{report_data.get('success_rate', 0):.1f}%</td></tr>
            </table>
        """

        if providers:
            html_body += "<h3>Top Providers</h3><ul>"
            for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True)[:5]:
                html_body += f"<li>{provider}: {count:,} calls</li>"
            html_body += "</ul>"

        html_body += "</body></html>"

        return self.send_email(to_emails, subject, body, html_body)


class AlertManager:
    """Centralized alert management for MetricLLM."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.webhook_handler = WebhookHandler()
        self.slack_integration = SlackIntegration()
        self.email_notifier = EmailNotifier()
        self.alert_rules = {}

    def add_alert_rule(self, name: str, condition: Callable, actions: List[str], cooldown: int = 300):
        """Add an alert rule."""
        self.alert_rules[name] = {
            "condition": condition,
            "actions": actions,
            "cooldown": cooldown,
            "last_triggered": None
        }

    def check_alerts(self, data: Dict[str, Any]):
        """Check all alert rules against current data."""
        current_time = datetime.now()

        for rule_name, rule in self.alert_rules.items():
            try:
                # Check cooldown
                if rule["last_triggered"]:
                    time_since_last = (current_time - rule["last_triggered"]).total_seconds()
                    if time_since_last < rule["cooldown"]:
                        continue

                # Check condition
                if rule["condition"](data):
                    self._trigger_alert(rule_name, data, rule["actions"])
                    rule["last_triggered"] = current_time

            except Exception as e:
                self.logger.error(f"Error checking alert rule '{rule_name}': {str(e)}")

    def _trigger_alert(self, rule_name: str, data: Dict[str, Any], actions: List[str]):
        """Trigger alert actions."""
        self.logger.warning(f"Alert triggered: {rule_name}")

        for action in actions:
            try:
                if action == "webhook":
                    self.webhook_handler.send_webhook("alert_triggered", {
                        "rule_name": rule_name,
                        "data": data
                    })
                elif action == "slack":
                    self.slack_integration.send_message(
                        f"🚨 Alert: {rule_name}\nDetails: {json.dumps(data, indent=2)}"
                    )
                elif action == "email":
                    email_recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "").split(",")
                    if email_recipients and email_recipients[0]:
                        self.email_notifier.send_alert_email(
                            email_recipients,
                            rule_name,
                            data
                        )
            except Exception as e:
                self.logger.error(f"Failed to execute alert action '{action}': {str(e)}")
