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
    Returns the predicted gold rate, a trend line chart visualizing the prediction over a range, 
    and a log/error message.
    """
    # Validate input: USD/INR must be greater than 0.
    if usd_inr_value <= 0:
        return 0.0, None, "Error: USD/INR exchange rate must be greater than 0."
    
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
        try:
            predicted_value = predicted_gold_rate[0][0]
        except (IndexError, TypeError):
            predicted_value = predicted_gold_rate[0]
        predicted_value = round(predicted_value, 2)

        # Generate a range for visualization: ±5% around the input value.
        usd_inr_range = np.linspace(usd_inr_value * 0.95, usd_inr_value * 1.05, 50)
        usd_inr_range_scaled = scaler.transform(usd_inr_range.reshape(-1, 1))
        predictions_range = model.predict(usd_inr_range_scaled).flatten()

        data = {
            'USD/INR': usd_inr_range,
            'Predicted Gold Rate (INR)': predictions_range
        }
        fig = px.line(
            data,
            x='USD/INR',
            y='Predicted Gold Rate (INR)',
            title=f"Gold Rate Prediction vs USD/INR ({model_choice})",
            labels={"USD/INR": "USD/INR Exchange Rate", "Predicted Gold Rate (INR)": "Gold Rate (INR)"}
        )
        
        return predicted_value, fig, ""
    
    except FileNotFoundError:
        return 0.0, None, "Error: Model files not found. Please ensure all model files are present."
    except Exception as e:
        return 0.0, None, f"An error occurred: {str(e)}"

# Build the Gradio interface using Blocks for a better layout with a title.
with gr.Blocks(title="Gold Rate Predictor🥇") as demo:
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
        
        # Logs/Error Messages Tab
        with gr.Tab("Logs"):
            error_output = gr.Textbox(label="Logs / Error Messages")
    
    # Footer HTML for LinkedIn and GitHub profiles
    footer_html = """
    <footer style="text-align: center; margin-top: 20px; font-family: Arial, sans-serif; padding: 10px;">
      <p>Developed ❤️ with Gradio by DINESH S.</p>
      <div style="display: inline-flex; align-items: center; justify-content: center; gap: 10px; margin-top: 10px;">
        <span>Connect with me:</span>
        <a href="https://www.linkedin.com/in/dinesh-x/" target="_blank">
          <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width:32px;">
        </a>
        <a href="https://github.com/itzdineshx/Gold-price-prediction" target="_blank">
          <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="width:32px;">
        </a>
      </div>
    </footer>
    """
    gr.HTML(footer_html)
    
    # Set up the button interaction. The function returns three values.
    predict_button.click(
        fn=predict_gold_rate,
        inputs=[usd_inr_input, model_selector],
        outputs=[predicted_rate_output, plot_output, error_output]
    )

# Launch the app with sharing enabled
demo.launch(share=True)
