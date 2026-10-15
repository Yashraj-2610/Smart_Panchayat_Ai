# Phase 3: GIS Integration Module
# Interacts with existing backend services for geospatial ward data

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import fetch_api, post_api

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000/api/v1")

def render_ward_map():
    """Interactive ward-level map with issue density overlay"""
    st.subheader("🗺 Village Ward Map")

    wards = fetch_api(API_BASE_URL, "sarpanch/analytics/wards")
    if not wards:
        st.info("Ward map data available after database initialization.")
        return

    df = pd.DataFrame(wards)
    # Simple visualization: Ward population vs issues
    fig = px.bar(
        df,
        x="ward_name",
        y=["population", "issues_count"],
        title="Ward Population & Issue Density",
        barmode="group",
        color_discrete_sequence=["#3498db", "#e74c3c"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Issue heat by ward
    if "high_priority_issues" in df.columns:
        st.markdown("### 🔴 High Priority Issues by Ward")
        st.dataframe(df[["ward_name", "issues_count", "high_priority_issues"]], hide_index=True, use_container_width=True)

def render_geospatial_insights():
    """Show ward-level development indicators"""
    st.subheader("📊 Geospatial Development Indicators")

    # Fetch ward analytics
    data = fetch_api(API_BASE_URL, "sarpanch/analytics/wards")

    if data:
        df = pd.DataFrame(data)
        # Metrics cards
        cols = st.columns(3)
        cols[0].metric("Wards Mapped", len(df))
        cols[1].metric("Avg Issues / Ward", round(df["issues_count"].mean(), 1) if "issues_count" in df.columns else 0)
        cols[2].metric("Most Affected Ward", df.loc[df["issues_count"].idxmax(), "ward_name"] if "issues_count" in df.columns else "N/A")

        # Ward comparison chart
        if "population" in df.columns and "issues_count" in df.columns:
            fig = px.scatter(
                df,
                x="population",
                y="issues_count",
                color="high_priority_issues" if "high_priority_issues" in df.columns else None,
                size="population" if "population" in df.columns else None,
                hover_name="ward_name",
                title="Population vs Issue Density (Bubble Size = Population)"
            )
            st.plotly_chart(fig, use_container_width=True)
