import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
import os  
import re  


def rgba_to_hex(rgba_str):
    """Converts an RGBA string (e.g., 'rgba(24.6, 187.3, 155.0, 1)') to a HEX color."""
    match = re.match(r"rgba\((\d+(\.\d+)?),\s*(\d+(\.\d+)?),\s*(\d+(\.\d+)?),\s*\d+(\.\d+)?\)", rgba_str)
    if match:
        r, g, b = map(lambda x: int(float(x)), [match.group(1), match.group(3), match.group(5)])
        return "#{:02x}{:02x}{:02x}".format(r, g, b) 

def plot_function(func_str, x_min, x_max, resolution, color, linestyle, grid):
    try:
        print(f"DEBUG: Received color - {color}")  

        if "rgba" in color:
            color = rgba_to_hex(color)
        print(f"DEBUG: Using fixed color - {color}")  

        x_values = np.linspace(x_min, x_max, resolution)
        functions = func_str.split(",")

        plt.figure(figsize=(6, 4), dpi=300)  

        for func_text in functions:
            func_text = func_text.strip()
            func = lambda x: eval(func_text, {"x": x, "np": np})
            y_values = func(x_values)

            plt.plot(x_values, y_values, label=f"f(x) = {func_text}", color=color, linestyle=linestyle)

        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.legend()
        if grid:
            plt.grid()

        plot_filename = "high_res_plot.png"
        abs_path = os.path.abspath(plot_filename)
        plt.savefig(abs_path, dpi=300)
        plt.close()

        return abs_path, abs_path if os.path.exists(abs_path) else ("Error: Plot file was not created", None)

    except Exception as e:
        print(f"ERROR: {e}")  
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
            color = gr.ColorPicker(label="Line Color", value="#ff0000")  # Default to red
            linestyle = gr.Dropdown(["solid", "dashed", "dotted", "dashdot"], label="Line Style", value="solid")
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
