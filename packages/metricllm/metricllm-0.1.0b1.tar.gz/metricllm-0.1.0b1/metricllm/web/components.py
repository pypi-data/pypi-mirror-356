"""
Web UI components for MetricLLM dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
from datetime import datetime


class MetricCard:
    """Component for displaying metric cards."""

    @staticmethod
    def render(title: str, value: str, delta: Optional[str] = None, delta_color: str = "normal"):
        """Render a metric card."""
        col1, col2 = st.columns([3, 1])
        with col1:
            st.metric(label=title, value=value, delta=delta, delta_color=delta_color)


class ChartComponent:
    """Component for rendering various chart types."""

    @staticmethod
    def line_chart(data: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None):
        """Create a line chart."""
        fig = px.line(data, x=x, y=y, color=color, title=title)
        fig.update_layout(
            showlegend=True,
            hovermode='x unified',
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def bar_chart(data: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None):
        """Create a bar chart."""
        fig = px.bar(data, x=x, y=y, color=color, title=title)
        fig.update_layout(
            showlegend=True,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def pie_chart(data: Dict[str, int], title: str):
        """Create a pie chart."""
        if not data:
            st.info("No data available for chart")
            return

        fig = go.Figure(data=[go.Pie(
            labels=list(data.keys()),
            values=list(data.values()),
            hole=0.3
        )])
        fig.update_layout(title=title, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def scatter_plot(data: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None,
                     size: Optional[str] = None):
        """Create a scatter plot."""
        fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title)
        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def heatmap(data: pd.DataFrame, title: str):
        """Create a heatmap."""
        fig = px.imshow(data, title=title, aspect="auto")
        st.plotly_chart(fig, use_container_width=True)


class DataTable:
    """Component for displaying data tables with filtering and pagination."""

    @staticmethod
    def render(data: List[Dict[str, Any]], columns: Optional[List[str]] = None,
               filters: Optional[Dict[str, List]] = None, page_size: int = 50):
        """Render a filterable data table."""

        if not data:
            st.info("No data available")
            return

        df = pd.DataFrame(data)

        # Apply column selection
        if columns:
            df = df[columns] if all(col in df.columns for col in columns) else df

        # Add filters
        if filters:
            filter_cols = st.columns(len(filters))
            for i, (filter_name, filter_options) in enumerate(filters.items()):
                if filter_name in df.columns:
                    with filter_cols[i]:
                        selected = st.multiselect(
                            f"Filter by {filter_name.replace('_', ' ').title()}",
                            options=filter_options,
                            default=filter_options
                        )
                        df = df[df[filter_name].isin(selected)]

        # Pagination
        total_rows = len(df)
        if total_rows > page_size:
            page = st.selectbox("Page", range(1, (total_rows // page_size) + 2))
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            df = df.iloc[start_idx:end_idx]

        # Display table
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Show pagination info
        if total_rows > page_size:
            st.caption(f"Showing {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows} rows")


class AlertComponent:
    """Component for displaying alerts and notifications."""

    @staticmethod
    def success(message: str):
        """Display success alert."""
        st.success(message)

    @staticmethod
    def error(message: str):
        """Display error alert."""
        st.error(message)

    @staticmethod
    def warning(message: str):
        """Display warning alert."""
        st.warning(message)

    @staticmethod
    def info(message: str):
        """Display info alert."""
        st.info(message)

    @staticmethod
    def custom_alert(message: str, alert_type: str = "info", icon: Optional[str] = None):
        """Display custom alert with optional icon."""
        if alert_type == "success":
            st.success(f"{icon + ' ' if icon else ''}{message}")
        elif alert_type == "error":
            st.error(f"{icon + ' ' if icon else ''}{message}")
        elif alert_type == "warning":
            st.warning(f"{icon + ' ' if icon else ''}{message}")
        else:
            st.info(f"{icon + ' ' if icon else ''}{message}")


class FormComponent:
    """Component for creating forms."""

    @staticmethod
    def prompt_form():
        """Create a prompt creation form."""
        with st.form("create_prompt_form"):
            st.subheader("Create New Prompt")

            name = st.text_input("Prompt Name", help="Unique name for the prompt")
            description = st.text_area("Description", help="Brief description of the prompt's purpose")
            template = st.text_area("Template", help="Prompt template with {variable} placeholders", height=150)
            tags = st.text_input("Tags", help="Comma-separated tags for categorization")

            submitted = st.form_submit_button("Create Prompt")

            if submitted:
                return {
                    "name": name,
                    "description": description,
                    "template": template,
                    "tags": [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
                }
        return None

    @staticmethod
    def config_form(current_config: Dict[str, Any]):
        """Create a configuration form."""
        with st.form("config_form"):
            st.subheader("Configuration Settings")

            # Monitoring settings
            st.write("**Monitoring Settings**")
            track_tokens = st.checkbox("Track Tokens", value=current_config.get("track_tokens", True))
            track_cost = st.checkbox("Track Cost", value=current_config.get("track_cost", True))
            evaluate = st.checkbox("Enable Evaluations", value=current_config.get("evaluate", True))
            responsible_ai = st.checkbox("Responsible AI Checks",
                                         value=current_config.get("responsible_ai_check", True))

            # Storage settings
            st.write("**Storage Settings**")
            storage_path = st.text_input("Storage Path", value=current_config.get("storage_path", "data"))
            retention_days = st.number_input("Retention Days", min_value=1,
                                             value=current_config.get("retention_days", 30))

            # Logging settings
            st.write("**Logging Settings**")
            log_level = st.selectbox("Log Level", ["DEBUG", "INFO", "WARNING", "ERROR"],
                                     index=["DEBUG", "INFO", "WARNING", "ERROR"].index(
                                         current_config.get("log_level", "INFO")))

            submitted = st.form_submit_button("Save Configuration")

            if submitted:
                return {
                    "track_tokens": track_tokens,
                    "track_cost": track_cost,
                    "evaluate": evaluate,
                    "responsible_ai_check": responsible_ai,
                    "storage_path": storage_path,
                    "retention_days": retention_days,
                    "log_level": log_level
                }
        return None


class RealtimeComponent:
    """Component for real-time data updates."""

    @staticmethod
    def live_metrics_display(data_callback, refresh_interval: int = 5):
        """Display live updating metrics."""
        placeholder = st.empty()

        # This would be used with st.rerun() in a real implementation
        # For now, we'll just display the current data
        with placeholder.container():
            try:
                data = data_callback()
                if data:
                    cols = st.columns(len(data))
                    for i, (key, value) in enumerate(data.items()):
                        with cols[i]:
                            st.metric(key.replace('_', ' ').title(), value)
            except Exception as e:
                st.error(f"Error loading live data: {str(e)}")

    @staticmethod
    def status_indicator(status: str, label: str = "System Status"):
        """Display a status indicator."""
        status_colors = {
            "healthy": "🟢",
            "warning": "🟡",
            "error": "🔴",
            "unknown": "⚪"
        }

        icon = status_colors.get(status.lower(), "⚪")
        st.write(f"{icon} **{label}:** {status.title()}")


class ExportComponent:
    """Component for data export functionality."""

    @staticmethod
    def export_controls(export_callback):
        """Create export controls."""
        st.subheader("Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            format_type = st.selectbox("Format", ["JSON", "CSV", "Excel"])

        with col2:
            days_back = st.number_input("Days Back", min_value=1, max_value=365, value=7)

        with col3:
            if st.button("Export"):
                try:
                    result = export_callback(format_type.lower(), days_back)
                    if result:
                        st.success(f"Export completed: {result}")
                    else:
                        st.error("Export failed")
                except Exception as e:
                    st.error(f"Export error: {str(e)}")
