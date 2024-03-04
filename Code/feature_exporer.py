from sklearn.metrics import mean_squared_error, r2_score
from itertools import combinations
import numpy as np


feature_categories = {
    'frequency_based': ['f1_mean', 'f2_mean', 'f3_mean', 'f4_mean', 'meanF0'],
    'shimmer': ['local_shimmer', 'localdb_shimmer', 'apq3_shimmer', 'apq5_shimmer', 'apq11_shimmer', 'dda_shimmer'],
    'jitter': ['local_jitter', 'local_absolute_jitter', 'rap_jitter', 'ppq5_jitter', 'ddp_jitter'],
    'energy_intensity': ['mean_spectral_energy', 'intensity_mean', 'intensity_min', 'intensity_max', 'intensity_range', 'intensity_sd']
}


def evaluate_feature_category(features, X_train, X_test, y_train, y_test, model):
    # Filter training and test sets for the selected features
    X_train_filtered = X_train[features]
    X_test_filtered = X_test[features]

    # Train the model
    model.fit(X_train_filtered, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_filtered)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    return {'rmse': rmse, 'r2': r2}

def improvement_detected(new_metrics, baseline_metrics):
    # Simple improvement detection based on R-squared value
    return new_metrics['r2'] > baseline_metrics['r2']

def generate_subsets(features):
    # Generate all non-empty subsets of the features list
    subsets = []
    for i in range(1, len(features) + 1):
        subsets.extend(combinations(features, i))
    return subsets


best_metrics = {'rmse': float('inf'), 'r2': -float('inf')}
best_features = []

for category, features in feature_categories.items():
    # Evaluate the current category
    category_metrics = evaluate_feature_category(features, X_train, X_test, y_train, y_test, LinearRegression())
    
    # Check for improvement
    if improvement_detected(category_metrics, best_metrics):
        best_metrics = category_metrics
        best_features = features
        
        # Experiment further within this category
        for subset in generate_subsets(features):
            subset_metrics = evaluate_feature_category(subset, X_train, X_test, y_train, y_test, LinearRegression())
            
            if improvement_detected(subset_metrics, best_metrics):
                best_metrics = subset_metrics
                best_features = subset

# Output the best performing feature set and its metrics
print(f'Best Feature Subset: {best_features}')
print(f'Best Metrics: RMSE: {best_metrics["rmse"]}, R-squared: {best_metrics["r2"]}')
