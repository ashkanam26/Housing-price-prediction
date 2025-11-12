# GitHub Copilot Instructions for Housing Price Prediction Project

## Project Overview

This is a **California Housing Price Prediction** project that uses machine learning to predict house prices based on various features. The project uses Python, scikit-learn, and XGBoost for model training and evaluation.

## Project Purpose

To build and evaluate predictive models for estimating house prices in California based on features such as:
- Median income
- Average rooms
- Average bedrooms
- Population
- Households
- Latitude/Longitude
- Ocean proximity

## Tech Stack

- **Language**: Python 3.x
- **ML Libraries**: 
  - scikit-learn (v1.6.1)
  - XGBoost (v2.1.3)
- **Data Processing**: 
  - pandas (v2.2.3)
  - numpy (v1.26.4)
- **Visualization**: 
  - matplotlib (v3.10.0)
  - seaborn (v0.13.2)
- **Model Persistence**: joblib (v1.4.2)
- **Development Environment**: Jupyter Notebook

## Key Files

- **`california housing price.ipynb`**: Main Jupyter notebook containing:
  - Data loading and exploration
  - Data preprocessing and feature engineering
  - Model training (Linear Regression, Random Forest, XGBoost)
  - Model evaluation and comparison
  - Visualizations
  
- **`xgboost-model.pkl`**: Pre-trained XGBoost model (the best performing model)

- **`requirments.txt`**: Python dependencies list (note: filename has a typo, should be "requirements.txt")

- **Visualization Files**:
  - `actual_vs_predict.png`: Comparison of actual vs predicted house prices
  - `feature_importance.png`: Feature importance from the XGBoost model
  - `housing_price.png`: Distribution of housing prices

## Code Style and Conventions

### Python Style
- Follow PEP 8 guidelines for Python code
- Use lowercase with underscores for variable names (snake_case)
- Keep code in Jupyter notebook cells organized and well-commented

### Machine Learning Best Practices
- Always split data into train/test sets before model training
- Use cross-validation when appropriate
- Document model hyperparameters
- Save trained models using joblib for reproducibility
- Include model evaluation metrics (MAE, MSE, RMSE, R²)

### Data Science Workflow
1. **Data Loading**: Use scikit-learn's `fetch_california_housing()` or load from CSV
2. **Exploratory Data Analysis**: Visualize distributions, correlations, and relationships
3. **Data Preprocessing**: Handle missing values, scale features if needed
4. **Model Training**: Train multiple models and compare performance
5. **Model Evaluation**: Use appropriate metrics and visualizations
6. **Model Selection**: Choose the best performing model
7. **Model Persistence**: Save the final model for future use

## Development Guidelines

### Setting Up the Environment
```bash
# Clone the repository
git clone https://github.com/ashkanam26/Housing-price-prediction.git

# Install dependencies
pip install -r requirments.txt

# Launch Jupyter Notebook
jupyter notebook
```

### Running the Project
1. Open `california housing price.ipynb` in Jupyter Notebook
2. Run cells sequentially from top to bottom
3. Visualizations will be displayed inline
4. The trained model will be saved as `xgboost-model.pkl`

### Adding New Features
When suggesting new features or improvements:
- Keep the focus on housing price prediction
- Consider adding new features to the dataset
- Suggest hyperparameter tuning for existing models
- Propose new visualization techniques
- Consider model interpretability (SHAP values, feature importance)

### Model Improvements
When improving models:
- Test new algorithms (e.g., Gradient Boosting, Neural Networks)
- Perform hyperparameter tuning using GridSearchCV or RandomizedSearchCV
- Try feature engineering techniques
- Implement ensemble methods
- Add model validation techniques (k-fold cross-validation)

### Documentation
- Add markdown cells in notebooks to explain code sections
- Include comments for complex operations
- Document model parameters and their reasoning
- Keep README.md updated with new features or changes

## Common Tasks

### Training a New Model
```python
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
```

### Saving and Loading Models
```python
import joblib

# Save model
joblib.dump(model, 'model-name.pkl')

# Load model
loaded_model = joblib.load('model-name.pkl')
```

### Creating Visualizations
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')

# Create plots
plt.figure(figsize=(10, 6))
plt.scatter(y_test, predictions)
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted Housing Prices')
plt.show()
```

## Known Issues and Notes

1. **Filename Typo**: The requirements file is named `requirments.txt` instead of `requirements.txt`
2. **Dataset**: Uses the California Housing Dataset from scikit-learn
3. **Best Model**: XGBoost Regressor was selected as the best performing model

## Contact

For questions or contributions, contact: ashkanam6731@gmail.com
