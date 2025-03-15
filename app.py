import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
import matplotlib.colors as mcolors  # Import color conversion module

def hex_to_rgb(hex_color):
    """Convert HEX color (e.g., '#ff5733') to an RGB tuple for Matplotlib."""
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

            # Convert HEX color to RGB before passing to Matplotlib
            rgb_color = hex_to_rgb(color) 

            plt.plot(x_values, y_values, label=f"f(x) = {func_text}", color=rgb_color, linestyle=linestyle)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.legend()
        
        if grid:
            plt.grid()

        plot_filename = "high_res_plot.png"
        plt.savefig(plot_filename, dpi=300)  # Save high-res plot
        plt.close()

        return plot_filename, plot_filename

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
            color = gr.ColorPicker(label="Line Color")
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
