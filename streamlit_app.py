#!/usr/bin/env python3
"""
Streamlit Frontend for Loan Default Predictor
3D Interactive Interface with Animations
"""

import streamlit as st
import time
import math
from simple_loan_predictor import predict_loan_default
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Loan Approval System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: #2c3e50;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 600;
    }
    
    .main-header p {
        color: #ecf0f1;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .approval-card {
        background: #27ae60;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .rejection-card {
        background: #e74c3c;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .result-text {
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .stButton > button {
        background: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background: #2980b9;
    }
    
    .stSlider > div > div > div > div {
        background: #3498db !important;
    }
    
    .stCheckbox > label {
        font-weight: 400;
    }
    
    .score-meter {
        height: 20px;
        background: #ecf0f1;
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .score-fill {
        height: 100%;
        background: #3498db;
        transition: width 0.5s ease;
        border-radius: 10px;
    }
    
    .score-label {
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f1c40f;
        opacity: 0;
    }
</style>

<script>
function createConfetti() {
    const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6'];
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '9999';
    
    document.body.appendChild(container);
    
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.top = '-20px';
        confetti.style.transform = 'rotate(' + (Math.random() * 360) + 'deg)';
        container.appendChild(confetti);
        
        const animation = confetti.animate([
            { top: '-20px', opacity: 0 },
            { opacity: 1 },
            { top: '100vh', opacity: 0 }
        ], {
            duration: 2000 + Math.random() * 3000,
            delay: Math.random() * 2000,
            easing: 'cubic-bezier(0.1, 0.8, 0.3, 1)'
        });
        
        animation.onfinish = () => {
            confetti.remove();
            if (container.children.length === 0) {
                container.remove();
            }
        };
    }
    
    setTimeout(() => {
        container.remove();
    }, 5000);
}
</script>
""", unsafe_allow_html=True)

def create_3d_risk_visualization(probability, risk_level):
    """Create 3D visualization of risk assessment"""
    
    # Create 3D sphere representing risk
    fig = go.Figure()
    
    # Create sphere data
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Color based on risk level
    if risk_level == "Low Risk":
        color = "green"
        opacity = 0.3 + probability * 0.7
    elif risk_level == "Medium Risk":
        color = "orange" 
        opacity = 0.4 + probability * 0.6
    elif risk_level == "High Risk":
        color = "red"
        opacity = 0.5 + probability * 0.5
    else:  # Very High Risk
        color = "darkred"
        opacity = 0.6 + probability * 0.4
    
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, color], [1, color]],
        opacity=opacity,
        showscale=False
    ))
    
    # Add risk indicator particles
    n_particles = int(probability * 100)
    if n_particles > 0:
        particle_x = np.random.uniform(-2, 2, n_particles)
        particle_y = np.random.uniform(-2, 2, n_particles)
        particle_z = np.random.uniform(-2, 2, n_particles)
        
        fig.add_trace(go.Scatter3d(
            x=particle_x, y=particle_y, z=particle_z,
            mode='markers',
            marker=dict(
                size=3,
                color=color,
                opacity=0.6
            ),
            name="Risk Particles"
        ))
    
    fig.update_layout(
        title=f"3D Risk Visualization - {risk_level}",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y", 
            zaxis_title="Z",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, showbackground=False),
            yaxis=dict(showgrid=False, showbackground=False),
            zaxis=dict(showgrid=False, showbackground=False)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400
    )
    
    return fig

def create_probability_gauge(probability):
    """Create 3D-style probability gauge"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Default Probability (%)"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=300
    )
    
    return fig

def show_approval_animation(probability):
    """Show approval message with confetti animation and score meter"""
    score = int(probability * 100)
    risk_level = "High Risk"
    if score <= 30:
        risk_level = "Low Risk"
        color = "#2ecc71"  # Green
    elif score <= 70:
        risk_level = "Medium Risk"
        color = "#f39c12"  # Yellow
    else:
        risk_level = "High Risk"
        color = "#e74c3c"  # Red
    
    st.markdown(f"""
    <div class="approval-card">
        <div class="result-text">LOAN APPROVED</div>
        <p style="color: white; font-size: 1.1rem; margin: 1rem 0 0.5rem 0;">
            Your loan application has been approved successfully.
        </p>
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Risk Level: <strong>{risk_level}</strong></span>
                <span><strong>{score}%</strong></span>
            </div>
            <div class="score-meter" style="background: #ecf0f1; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="width: {score}%; height: 100%; background: {color}; transition: all 0.5s ease; border-radius: 10px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                <span>0%</span>
                <span>100%</span>
            </div>
        </div>
    </div>
    <script>createConfetti();</script>
    """, unsafe_allow_html=True)

def show_rejection_message(probability):
    """Show rejection message with score meter"""
    score = int(probability * 100)
    risk_level = "High Risk"
    if score <= 30:
        risk_level = "Low Risk"
        color = "#2ecc71"  # Green
    elif score <= 70:
        risk_level = "Medium Risk"
        color = "#f39c12"  # Yellow
    else:
        risk_level = "High Risk"
        color = "#e74c3c"  # Red
    
    st.markdown(f"""
    <div class="rejection-card">
        <div class="result-text">LOAN NOT APPROVED</div>
        <p style="color: white; font-size: 1.1rem; margin: 1rem 0 0.5rem 0;">
            We're sorry, your loan application was not approved at this time.
        </p>
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Risk Level: <strong>{risk_level}</strong></span>
                <span><strong>{score}%</strong></span>
            </div>
            <div class="score-meter" style="background: #ecf0f1; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="width: {score}%; height: 100%; background: {color}; transition: all 0.5s ease; border-radius: 10px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.9rem; color: #7f8c8d;">
                <span>0%</span>
                <span>100%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; padding: 0;">Loan Approval System</h1>
        <p style="color: #ecf0f1; margin: 0.5rem 0 0 0;">
            AI-Powered Credit Risk Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Month options for the selectbox
    month_options = {
        "January": {"month_jan": 1}, "February": {"month_feb": 1}, "March": {"month_mar": 1},
        "April": {"month_apr": 1}, "May": {"month_may": 1}, "June": {"month_jun": 1},
        "July": {"month_jul": 1}, "August": {"month_aug": 1}, "September": {"month_sep": 1},
        "October": {"month_oct": 1}, "November": {"month_nov": 1}, "December": {"month_dec": 1}
    }
    
    # Main content area with form in a centered container
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:  # Center column with form
        with st.container():
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #2c3e50; margin-bottom: 0.5rem;">Loan Application Form</h2>
                <p style="color: #7f8c8d; margin-top: 0;">Please fill in your details for loan assessment</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Form in a card with improved styling
            with st.container():
                st.markdown("""
                <style>
                    .form-card {
                        background: #ffffff;
                        padding: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                        margin-bottom: 2rem;
                        border: 1px solid #e0e0e0;
                    }
                    .form-section {
                        margin-bottom: 2rem;
                        padding-bottom: 1.5rem;
                        border-bottom: 1px solid #f0f0f0;
                    }
                    .form-section:last-child {
                        border-bottom: none;
                        margin-bottom: 0;
                        padding-bottom: 0;
                    }
                    .form-section h4 {
                        color: #2c3e50;
                        margin-bottom: 1.2rem;
                        font-size: 1.1rem;
                        font-weight: 600;
                        letter-spacing: 0.5px;
                    }
                    .stSelectbox, .stNumberInput, .stSlider {
                        margin-bottom: 1.2rem;
                    }
                    .stCheckbox > label {
                        font-weight: 400;
                    }
                </style>
                <div class="form-card">
                """, unsafe_allow_html=True)
                
                # Personal Information
                st.markdown("<div class='form-section'><h4>Personal Information</h4></div>", unsafe_allow_html=True)
                
                # Use columns to organize the form
                c1, c2, c3 = st.columns(3)
                with c1:
                    age = st.number_input("Age", min_value=18, max_value=100, value=30)
                with c2:
                    job = st.selectbox("Job Type", ["admin.", "blue-collar", "entrepreneur", "housemaid", 
                                                 "management", "retired", "self-employed", "services", 
                                                 "student", "technician", "unemployed"])
                with c3:
                    marital = st.selectbox("Marital Status", ["single", "married", "divorced"])
                    
                # Add month selection
                selected_month = st.selectbox("Month of Application", list(month_options.keys()))
                    
                # Add education level
                education = st.selectbox("Education Level", ["university.degree", "high.school", "basic.9y", "basic.6y", "basic.4y", "illiterate"])
                education_university = 1 if education == "university.degree" else 0
                    
                # Set job and marital status flags
                job_management = 1 if job == "management" else 0
                job_technician = 1 if job == "technician" else 0
                marital_married = 1 if marital == "married" else 0
                    
                # Contact Information
                st.markdown("<div class='form-section'><h4>Contact Information</h4></div>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    contact_cellular = st.checkbox("Cellular Contact", value=True)
                with c2:
                    contact_telephone = st.checkbox("Telephone Contact")
                
                campaign = st.slider("Number of Contacts During Campaign", min_value=1, max_value=50, value=3)
                pdays = st.slider("Days Since Last Contact", min_value=0, max_value=1000, value=300)
                
                # Employment & Financial
                st.markdown("<div class='form-section'><h4>Employment & Financial</h4></div>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    default_no = st.checkbox("No Previous Default", value=True)
                with c2:
                    housing_no = st.checkbox("No Housing Loan", value=True)
                with c3:
                    loan_no = st.checkbox("No Personal Loan", value=True)
                
                previous = st.slider("Previous Campaigns", min_value=0, max_value=5, value=0,
                                  help="Number of previous campaigns")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Close form-card
                
                # Centered submit button with custom styling
                st.markdown("""
                <style>
                    .stButton > button {
                        display: block;
                        margin: 0 auto;
                        max-width: 300px;
                        padding: 0.8rem 2rem;
                        font-size: 1.1rem;
                        font-weight: 500;
                        border-radius: 8px;
                        transition: all 0.3s ease;
                    }
                    .stButton > button:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
                    }
                </style>
                """, unsafe_allow_html=True)
                
                submit_btn = st.button("Analyze Loan Risk", 
                                    type="primary",
                                    use_container_width=False,
                                    help="Click to analyze your loan application")
                
                if submit_btn:
                    # Prepare features
                    features = {
                        'age': float(age),
                        'job': job,
                        'marital': marital,
                        'pdays': float(pdays), 
                        'previous': float(previous),
                        'contact_cellular': float(contact_cellular),
                        'month_mar': float(selected_month == "March"),
                        'month_oct': float(selected_month == "October"),
                        'default_no': float(default_no),
                        'job_management': float(job_management),
                        'job_technician': float(job_technician),
                        'marital_married': float(marital_married),
                        'education_university.degree': float(education_university),
                        'housing_no': float(housing_no),
                        'loan_no': float(loan_no)
                    }
                    
                    # Add month features
                    for month, month_dict in month_options.items():
                        for key in month_dict:
                            features[key] = float(selected_month == month)
                    
                    # Make prediction
                    with st.spinner("AI is analyzing your application..."):
                        time.sleep(2)  # Dramatic pause
                        result = predict_loan_default(features)
                    
                    # Display results
                    probability = result['probability']
                    risk_level = result['risk_level']
                    recommendation = result['recommendation']
                    
                    # Show result with animation and score meter
                    if recommendation == "APPROVE":
                        show_approval_animation(probability)
                    else:
                        show_rejection_message(probability)
                    
                    # 3D Visualizations
                    st.markdown("### Risk Analysis")
                    
                    # Create two columns for visualizations
                    viz_col1, viz_col2 = st.columns(2)
                    
                    with viz_col1:
                        # Risk visualization
                        st.markdown("#### Risk Level")
                        risk_fig = create_3d_risk_visualization(probability, risk_level)
                        st.plotly_chart(risk_fig, use_container_width=True)
                    
                    with viz_col2:
                        # Probability gauge
                        st.markdown("#### Default Probability")
                        gauge_fig = create_probability_gauge(probability)
                        st.plotly_chart(gauge_fig, use_container_width=True)
                    
                    # Model Information
                    st.markdown("### Model Information")
                    
                    # Create columns for model info
                    info_col1, info_col2, info_col3 = st.columns(3)
                    
                    with info_col1:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Model Performance</h4>
                            <p><strong>Accuracy:</strong> 78.8%</p>
                            <p><strong>Dataset:</strong> 41,188 records</p>
                            <p><strong>Default Rate:</strong> 11.3%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with info_col2:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Risk Factors</h4>
                            <p><strong>Cellular Contact:</strong> +43.8%</p>
                            <p><strong>Contact Days:</strong> -27.9%</p>
                            <p><strong>March Apps:</strong> +19.8%</p>
                            <p><strong>October Apps:</strong> +18.5%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with info_col3:
                        st.markdown("""
                        <div class="metric-card">
                            <h4>Tips for Approval</h4>
                            <p>• Maintain good credit history</p>
                            <p>• Reduce existing debt</p>
                            <p>• Increase income stability</p>
                            <p>• Limit credit applications</p>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()