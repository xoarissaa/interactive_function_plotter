import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
import os  

# Function to convert HEX color to RGB tuple
def hex_to_rgb(hex_color):
    """Convert HEX color (#RRGGBB) to Matplotlib RGB tuple (R, G, B)."""
    hex_color = hex_color.lstrip("#")  # Remove #
    rgb = tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))  # Convert to (R, G, B)
    return rgb  # Matplotlib expects RGB (not HEX)

def plot_function(func_str, x_min, x_max, resolution, color, linestyle, grid):
    try:
        # Ensure color is valid; fallback to black if empty
        if not color or not color.startswith("#") or len(color) != 7:
            color = "#000000"  # Default to black

        # Convert HEX to RGB
        color_rgb = hex_to_rgb(color)

        x_values = np.linspace(x_min, x_max, resolution)
        functions = func_str.split(",")

        plt.figure(figsize=(6, 4), dpi=300)  

        for func_text in functions:
            func_text = func_text.strip()
            func = lambda x: eval(func_text, {"x": x, "np": np})
            y_values = func(x_values)

            # Use RGB color for Matplotlib
            plt.plot(x_values, y_values, label=f"f(x) = {func_text}", color=color_rgb, linestyle=linestyle)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.legend()
        if grid:
            plt.grid()

        # Save the plot and return absolute path
        plot_filename = "high_res_plot.png"
        abs_path = os.path.abspath(plot_filename)  # Convert to absolute path
        plt.savefig(abs_path, dpi=300)
        plt.close()

        # Ensure the file exists before returning
        if os.path.exists(abs_path):
            return abs_path, abs_path
        else:
            return "Error: Plot file was not created", None

    except Exception as e:
        return f"Error: {e}", None

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Interactive Function Plotter 📈")

    with gr.Row():
        with gr.Column():
            func_str = gr.Textbox(label="Function (e.g., x**2, np.sin(x), np.exp(-x))")
            x_min = gr.Number(label="X Min", value=-10)
            x_max = gr.Number(label="X Max", value=10)
            resolution = gr.Slider(10, 1000, step=10, label="Resolution", value=100)
            color = gr.ColorPicker(label="Line Color", value="#000000")  # Default to black
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
