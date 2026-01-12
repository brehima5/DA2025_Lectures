# 💎 Diamond Price Prediction Streamlit App

Production-ready web application for AI-powered diamond price estimation using LightGBM.

## Features

- **Interactive Price Prediction**: Real-time diamond price estimates based on 8 key features
- **Confidence Intervals**: Shows prediction uncertainty with ±1σ confidence bands
- **Visual Analytics**: Gauge charts and price range visualizations
- **Model Card**: Complete model documentation, performance metrics, and limitations
- **Business Insights**: Retail pricing strategies and market guidance

## Quick Start

### 1. Generate Model Artifacts

First, run the Jupyter notebook to train the model and generate required artifacts:

```bash
jupyter notebook Mod7L3_AIAssistedWorkflows.ipynb
```

Run all cells through the "Model Persistence" section. This creates:
- `diamond_price_model.pkl` (trained LightGBM model)
- `feature_scaler.pkl` (StandardScaler for preprocessing)
- `model_metadata.json` (model configuration and metrics)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with conda:
```bash
conda install --file requirements.txt
```

### 3. Launch the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## App Structure

### Input Features (Sidebar)
- **Carat Weight**: 0.2 - 5.0 carats
- **Cut Quality**: Fair, Good, Very Good, Premium, Ideal
- **Color Grade**: J (worst) → D (best)
- **Clarity Grade**: I1 (worst) → IF (best)
- **Depth %**: 50-75%
- **Table %**: 50-70%
- **Z Dimension**: Depth in millimeters

### Outputs
- **Predicted Price**: Point estimate with confidence interval
- **Gauge Visualization**: Visual price indicator with confidence band
- **Quality Summary**: Encoded feature scores
- **Model Performance**: RMSE, MAE, R² metrics
- **Limitations**: Known constraints and proper use cases

## Model Information

- **Algorithm**: LightGBM Gradient Boosting Regressor
- **Training Samples**: ~53,000 diamonds
- **Test RMSE**: ~$550
- **Test R²**: 0.98+
- **Features**: 8 (4 categorical, 4 numerical, 1 engineered)

### Key Pricing Drivers
1. **Carat** (45-50% importance): Non-linear pricing premium
2. **Volume** (20-25%): Physical size matters
3. **Clarity** (10-15%): Quality grade impact
4. **Color** (8-12%): Grade-specific pricing

## File Structure

```
Mod7/
├── app.py                              # Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── Mod7L3_AIAssistedWorkflows.ipynb   # Training notebook
├── diamond_price_model.pkl            # Trained model (generated)
├── feature_scaler.pkl                 # Preprocessing scaler (generated)
└── model_metadata.json                # Model config (generated)
```

## Usage Examples

### Basic Prediction
1. Enter diamond specifications in sidebar
2. Click "Predict Price"
3. View predicted price with confidence interval

### Understanding Results
- **Predicted Price**: Best estimate based on input features
- **Confidence Band**: ±$550 range (1 standard error)
- **Quality Scores**: Ordinal encoding shows relative quality

## Known Limitations

⚠️ **Important Considerations:**
- Higher error on luxury diamonds (>$10,000)
- Does not capture brand/certification premiums
- Assumes GIA-equivalent grading standards
- Not suitable for legal appraisals or insurance valuations

✅ **Appropriate Use Cases:**
- Retail pricing guidance
- Inventory valuation estimates
- Market trend analysis
- Educational demonstrations

## Model Performance

| Metric | Value |
|--------|-------|
| Test RMSE | ~$550 |
| Test MAE | ~$400 |
| Test R² | 0.98+ |
| CV RMSE | ~$560 (±$20) |

**Interpretation**: Model explains 98%+ of price variance with average error of $400 per diamond.

## Business Insights

### Pricing Strategy
1. **Carat Premium**: Target 0.9-1.0ct for value buyers, premium marketing for 1.5ct+
2. **Cut Quality**: Emphasize Ideal/Premium grades (15-20% premium justified)
3. **Color Grading**: Position G-H as "best value" near-colorless
4. **Volume Metric**: Highlight face-up appearance for well-proportioned stones

## Troubleshooting

### "Model files not found"
→ Run the notebook to generate model artifacts first

### Import errors
→ Install all dependencies: `pip install -r requirements.txt`

### Prediction errors
→ Ensure input values are within valid ranges

## Technical Stack

- **Frontend**: Streamlit
- **ML Framework**: LightGBM, scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data**: Pandas, NumPy
- **Persistence**: Joblib

## Development

To modify the model:
1. Edit training pipeline in notebook
2. Re-run model training cells
3. Update `model_metadata.json` if features change
4. Test app with new artifacts

## License

Educational project for data science demonstration.

## Contact

For questions or issues, refer to the course materials or instructor.

---

**Version**: 1.0  
**Last Updated**: January 12, 2026  
**Model Type**: LightGBM Regressor
