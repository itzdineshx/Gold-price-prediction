import gradio as gr
import plotly.express as px
import numpy as np
import joblib

# Available models and their file paths
model_paths = {
    "Linear Regression": "/workspaces/Gold-price-prediction/models/Regression_model.pkl",
    "Ridge Regression": "/workspaces/Gold-price-prediction/models/regressor.pkl",
}

def predict_gold_rate(usd_inr_value, model_choice):
    """
    Predicts the gold rate based on the USD/INR exchange rate using a selected pre-trained model.
    Returns the predicted gold rate and a simple line chart visualizing the prediction.
    """
    try:
        # Load the pre-trained scaler and selected model
        scaler = joblib.load('/workspaces/Gold-price-prediction/models/scaler.pkl')
        model_path = model_paths.get(model_choice)
        if not model_path:
            return 0.0, None, f"Error: Selected model '{model_choice}' is not available."
        
        model = joblib.load(model_path)

        # Reshape the input for prediction
        usd_inr_scaled = scaler.transform(np.array([[usd_inr_value]]))

        # Make the prediction
        predicted_gold_rate = model.predict(usd_inr_scaled)

        # Create a trend line chart for the prediction
        data = {
            'USD/INR': [usd_inr_value],
            'Predicted Gold Rate (INR)': [predicted_gold_rate[0][0]]
        }
        fig = px.line(
            data,
            x='USD/INR',
            y='Predicted Gold Rate (INR)',
            title=f"Gold Rate Prediction vs USD/INR ({model_choice})"
        )
        
        return predicted_gold_rate[0][0], fig, ""
    
    except FileNotFoundError:
        return 0.0, None, "Error: Model files not found. Please ensure all model files are present."
    except Exception as e:
        return 0.0, None, f"An error occurred: {str(e)}"

# Build the Gradio interface using Blocks for a better layout
with gr.Blocks() as demo:
    gr.Markdown("# Gold Rate Prediction 🥇")
    gr.Markdown("Enter the USD/INR exchange rate and select a model to predict the gold rate and visualize the trend.")

    with gr.Tabs():
        # Prediction Tab
        with gr.Tab("Prediction"):
            with gr.Row():
                usd_inr_input = gr.Number(label="USD/INR Exchange Rate", precision=2)
            with gr.Row():
                model_selector = gr.Dropdown(label="Select Prediction Model", choices=list(model_paths.keys()), value="Linear Regression")
            with gr.Row():
                predicted_rate_output = gr.Number(label="Predicted Gold Rate (in INR)", precision=2)
            with gr.Row():
                predict_button = gr.Button("Predict")
        
        # Visualization Tab
        with gr.Tab("Visualization"):
            with gr.Row():
                plot_output = gr.Plot(label="Gold Rate Prediction vs USD/INR")

    # Set up the button interaction.
    # The function returns three values but we're only displaying the first two.
    predict_button.click(
        fn=predict_gold_rate,
        inputs=[usd_inr_input, model_selector],
        outputs=[predicted_rate_output, plot_output]
    )

# Launch the app with sharing enabled
demo.launch(share=True)
