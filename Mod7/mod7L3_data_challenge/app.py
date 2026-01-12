"""
Diamond Price Prediction Streamlit App
Production-ready application for diamond price estimation
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Diamond Price Predictor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# LOAD MODEL ARTIFACTS
# ========================================
@st.cache_resource
def load_model_artifacts():
    """Load trained model, scaler, and metadata"""
    try:
        model = joblib.load('diamond_price_model.pkl')
        scaler = joblib.load('feature_scaler.pkl')
        
        with open('model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        return model, scaler, metadata
    except FileNotFoundError as e:
        st.error(f"❌ Model files not found. Please run the notebook to generate model artifacts first.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

model, scaler, metadata = load_model_artifacts()

# ========================================
# HELPER FUNCTIONS
# ========================================
def calculate_volume(x, y, z):
    """Calculate diamond volume from dimensions"""
    return x * y * z

def encode_categorical(cut, color, clarity):
    """Encode categorical features using ordinal mapping"""
    cut_map = {cut: i for i, cut in enumerate(metadata['cut_order'])}
    color_map = {color: i for i, color in enumerate(metadata['color_order'])}
    clarity_map = {clarity: i for i, clarity in enumerate(metadata['clarity_order'])}
    
    return cut_map.get(cut, 0), color_map.get(color, 0), clarity_map.get(clarity, 0)

def predict_price(input_features):
    """Make price prediction with confidence interval"""
    # Create feature array
    feature_dict = {
        'carat': input_features['carat'],
        'cut_encoded': input_features['cut_encoded'],
        'color_encoded': input_features['color_encoded'],
        'clarity_encoded': input_features['clarity_encoded'],
        'depth': input_features['depth'],
        'table': input_features['table'],
        'z': input_features['z'],
        'volume': input_features['volume']
    }
    
    X_input = pd.DataFrame([feature_dict])
    
    # Predict
    predicted_price = model.predict(X_input)[0]
    
    # Calculate confidence band (±1 standard error based on test RMSE)
    test_rmse = metadata['performance_metrics']['test_rmse']
    lower_bound = max(0, predicted_price - test_rmse)
    upper_bound = predicted_price + test_rmse
    
    return predicted_price, lower_bound, upper_bound

# ========================================
# MAIN APP LAYOUT
# ========================================

# Header
st.title("💎 Diamond Price Prediction System")
st.markdown("### AI-Powered Diamond Valuation Tool")
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 2])

# ========================================
# SIDEBAR: INPUT FEATURES
# ========================================
with st.sidebar:
    st.header("📊 Diamond Specifications")
    st.markdown("Enter the diamond's characteristics below:")
    
    # Carat weight
    carat = st.number_input(
        "Carat Weight",
        min_value=0.2,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Diamond weight in carats (0.2 - 5.0)"
    )
    
    # Cut quality
    cut = st.selectbox(
        "Cut Quality",
        options=metadata['cut_order'],
        index=4,  # Default to Ideal
        help="Cut quality from Fair to Ideal"
    )
    
    # Color grade
    color = st.selectbox(
        "Color Grade",
        options=metadata['color_order'],
        index=3,  # Default to G
        help="Color grade from J (worst) to D (best)"
    )
    
    # Clarity grade
    clarity = st.selectbox(
        "Clarity Grade",
        options=metadata['clarity_order'],
        index=2,  # Default to SI1
        help="Clarity grade from I1 (worst) to IF (best)"
    )
    
    st.markdown("---")
    st.subheader("Physical Dimensions")
    
    # Depth percentage
    depth = st.slider(
        "Depth %",
        min_value=50.0,
        max_value=75.0,
        value=62.0,
        step=0.1,
        help="Total depth percentage (50-75%)"
    )
    
    # Table percentage
    table = st.slider(
        "Table %",
        min_value=50.0,
        max_value=70.0,
        value=57.0,
        step=0.1,
        help="Table width percentage (50-70%)"
    )
    
    # Z dimension (depth in mm)
    z = st.number_input(
        "Z Dimension (mm)",
        min_value=1.0,
        max_value=10.0,
        value=3.8,
        step=0.1,
        help="Depth dimension in millimeters"
    )
    
    # Estimate X and Y from carat and z (rough approximation)
    # Using typical diamond proportions
    estimated_x = (carat * 100 / z) ** 0.5 * 0.95
    estimated_y = (carat * 100 / z) ** 0.5 * 0.95
    
    st.markdown("---")
    
    # Predict button
    predict_button = st.button("💰 Predict Price", type="primary", use_container_width=True)

# ========================================
# MAIN CONTENT AREA
# ========================================

with col1:
    st.subheader("📈 Prediction Results")
    
    if predict_button:
        # Encode categorical features
        cut_encoded, color_encoded, clarity_encoded = encode_categorical(cut, color, clarity)
        
        # Calculate volume
        volume = calculate_volume(estimated_x, estimated_y, z)
        
        # Prepare input features
        input_features = {
            'carat': carat,
            'cut_encoded': cut_encoded,
            'color_encoded': color_encoded,
            'clarity_encoded': clarity_encoded,
            'depth': depth,
            'table': table,
            'z': z,
            'volume': volume
        }
        
        # Make prediction
        predicted_price, lower_bound, upper_bound = predict_price(input_features)
        
        # Display results
        st.metric(
            label="Predicted Price",
            value=f"${predicted_price:,.0f}",
            delta=None
        )
        
        st.markdown(f"""
        **Confidence Interval (±1σ):**
        - Lower Bound: ${lower_bound:,.0f}
        - Upper Bound: ${upper_bound:,.0f}
        """)
        
        # Confidence gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=predicted_price,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Price Estimate ($)", 'font': {'size': 18}},
            delta={'reference': (lower_bound + upper_bound) / 2, 'relative': False},
            gauge={
                'axis': {'range': [None, upper_bound * 1.2], 'tickformat': ',.0f'},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, lower_bound], 'color': "lightgray"},
                    {'range': [lower_bound, upper_bound], 'color': "lightgreen"},
                    {'range': [upper_bound, upper_bound * 1.2], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': predicted_price
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Feature importance for this prediction
        st.markdown("---")
        st.markdown("**Quality Grade Summary:**")
        st.markdown(f"""
        - Cut: **{cut}** (Score: {cut_encoded}/4)
        - Color: **{color}** (Score: {color_encoded}/6)
        - Clarity: **{clarity}** (Score: {clarity_encoded}/7)
        """)
        
    else:
        st.info("👈 Enter diamond specifications in the sidebar and click 'Predict Price'")

# ========================================
# MODEL CARD & DOCUMENTATION
# ========================================

with col2:
    st.subheader("📋 Model Information Card")
    
    # Model details
    with st.expander("🤖 Model Details", expanded=False):
        st.markdown(f"""
        **Model Type:** {metadata['model_type']}  
        **Version:** {metadata['model_version']}  
        **Training Date:** {metadata['training_date']}  
        **Training Samples:** {metadata['training_data_stats']['n_samples']:,}
        
        **Features Used ({len(metadata['feature_columns'])}):**
        - Carat (weight)
        - Cut Quality (ordinal)
        - Color Grade (ordinal)
        - Clarity Grade (ordinal)
        - Depth % (physical)
        - Table % (physical)
        - Z dimension (physical)
        - Volume (engineered: x × y × z)
        """)
    
    # Performance metrics
    with st.expander("📊 Model Performance", expanded=True):
        perf = metadata['performance_metrics']
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Test RMSE", f"${perf['test_rmse']:,.0f}")
        col_b.metric("Test MAE", f"${perf['test_mae']:,.0f}")
        col_c.metric("R² Score", f"{perf['test_r2']:.4f}")
        
        st.markdown(f"""
        **Cross-Validation (5-fold):**
        - CV RMSE: ${perf['cv_rmse_mean']:,.0f} (±${perf['cv_rmse_std']:,.0f})
        
        **Interpretation:**
        - Model explains **{perf['test_r2']*100:.1f}%** of price variance
        - Average prediction error: **${perf['test_mae']:,.0f}** per diamond
        """)
    
    # Known limitations
    with st.expander("⚠️ Known Limitations & Constraints", expanded=True):
        st.markdown("""
        **Model Limitations:**
        - Higher prediction error for luxury diamonds (>$10,000)
        - Does not capture brand or certification premiums
        - Assumes GIA-equivalent grading standards
        - Based on historical data patterns (may not reflect market shifts)
        
        **Data Constraints:**
        - Removed diamonds with zero dimensions (physical impossibility)
        - Trained on {train_samples:,} samples
        - Price range: ${price_min:,} - ${price_max:,}
        
        **Feature Engineering:**
        - X and Y dimensions dropped to reduce multicollinearity
        - Volume feature engineered from X × Y × Z
        - Ordinal encoding for categorical grades
        - StandardScaler applied to numerical features only
        
        **Use Cases:**
        - ✅ Retail pricing guidance
        - ✅ Inventory valuation estimates
        - ✅ Market trend analysis
        - ❌ Legal appraisals (not certified)
        - ❌ Insurance valuations (requires certified appraisal)
        """.format(
            train_samples=metadata['training_data_stats']['n_samples'],
            price_min=metadata['training_data_stats']['price_min'],
            price_max=metadata['training_data_stats']['price_max']
        ))
    
    # Business insights
    with st.expander("💡 Pricing Insights", expanded=False):
        st.markdown("""
        **Key Pricing Drivers (from model):**
        1. **Carat Weight:** Non-linear premium above 1.0ct
        2. **Cut Quality:** Ideal/Premium cuts command 15-20% premium
        3. **Color Grade:** Each grade improvement adds ~8-12% value
        4. **Clarity Grade:** Moderate impact; VS grades offer best value
        
        **Retail Strategies:**
        - Target 0.9-1.0ct range for value-conscious buyers
        - Emphasize cut quality in premium segments
        - Position G-H color as "best value" near-colorless
        - Highlight face-up appearance for well-proportioned stones
        """)

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
💎 Diamond Price Prediction System v1.0 | Powered by LightGBM<br>
⚠️ For informational purposes only. Not a substitute for professional appraisal.
</div>
""", unsafe_allow_html=True)
