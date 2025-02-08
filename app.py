import gradio as gr
import plotly.express as px
import numpy as np
import joblib

def predict_gold_rate(usd_inr_value):
    """
    Predicts the gold rate based on the USD/INR exchange rate using a pre-trained model.
    Returns the predicted gold rate and a simple line chart visualizing the prediction.
    """
    try:
        # Load the pre-trained scaler and model
        scaler = joblib.load('models/scaler.pkl')
        model = joblib.load('models/Regression_model.pkl')

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
            title="Gold Rate Prediction vs USD/INR"
        )
        
        # Return predicted value and figure. The third value (empty string) is for any error messages.
        return predicted_gold_rate[0][0], fig, ""
    
    except FileNotFoundError:
        return 0.0, None, "Error: Model files not found. Please ensure 'scaler.pkl' and 'Regression_model.pkl' are present."
    except Exception as e:
        return 0.0, None, f"An error occurred: {str(e)}"

# Build the Gradio interface using Blocks for a better layout
with gr.Blocks() as demo:
    gr.Markdown("# Gold Rate Prediction 🥇")
    gr.Markdown("Enter the USD/INR exchange rate to predict the gold rate and visualize the trend.")

    with gr.Tabs():
        # Prediction Tab
        with gr.Tab("Prediction"):
            with gr.Row():
                usd_inr_input = gr.Number(label="USD/INR Exchange Rate", precision=2)
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
        inputs=usd_inr_input,
        outputs=[predicted_rate_output, plot_output]
    )

# Launch the app with sharing enabled
demo.launch(share=True)
