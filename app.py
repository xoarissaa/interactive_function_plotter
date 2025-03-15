import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
import matplotlib.colors as mcolors
import os  # Import os to handle file paths

def hex_to_rgb(hex_color):
    """Convert HEX color (e.g., '#ff5733') to an RGB tuple for Matplotlib."""
    if hex_color is None:  # If no color is selected, default to black
        hex_color = "#000000"
    rgb = mcolors.hex2color(hex_color)  # Convert HEX to RGB
    return rgb

def plot_function(func_str, x_min, x_max, resolution, color, linestyle, grid):
    try:
        x_values = np.linspace(x_min, x_max, resolution)
        functions = func_str.split(",")

        plt.figure(figsize=(6, 4), dpi=300)  # High-resolution image

        for func_text in functions:
            func_text = func_text.strip()
            func = lambda x: eval(func_text, {"x": x, "np": np})
            y_values = func(x_values)

            # Ensure a valid color is provided, defaulting to black
            rgb_color = hex_to_rgb(color)

            plt.plot(x_values, y_values, label=f"f(x) = {func_text}", color=rgb_color, linestyle=linestyle)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.legend()

        if grid:
            plt.grid()

        # Save the plot as an absolute path
        plot_filename = "high_res_plot.png"
        abs_path = os.path.abspath(plot_filename)  # Convert to absolute path
        plt.savefig(abs_path, dpi=300)
        plt.close()

        return abs_path, abs_path  # Return the absolute path for Gradio to use

    except Exception as e:
        return f"Error: {e}", None

# Using gr.Blocks() for better UI layout
with gr.Blocks() as demo:
    gr.Markdown("# Interactive Function Plotter 📈")

    with gr.Row():
        with gr.Column():
            func_str = gr.Textbox(label="Function (e.g., x**2, np.sin(x), np.exp(-x))")
            x_min = gr.Number(label="X Min", value=-10)
            x_max = gr.Number(label="X Max", value=10)
            resolution = gr.Slider(10, 1000, step=10, label="Resolution", value=100)
            color = gr.ColorPicker(label="Line Color", value="#000000")  # Set default to black
            linestyle = gr.Dropdown(["solid", "dashed", "dotted", "dashdot"], label="Line Style")
            grid = gr.Checkbox(label="Show Grid", value=True)
            submit_button = gr.Button("Plot Function")

        with gr.Column():
            output_image = gr.Image(label="Function Plot")
            download_button = gr.File(label="Download High-Res Plot")

    submit_button.click(
        plot_function, 
        inputs=[func_str, x_min, x_max, resolution, color, linestyle, grid], 
        outputs=[output_image, download_button]
    )

demo.launch()
