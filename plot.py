from pyaxidraw import axidraw  # Import the module


def plot_svg(filename: str):
    ad = axidraw.AxiDraw()  # connect to AxiDraw
    ad.moveto(0, 0)  # Move to the origin to start clean
    ad.plot_setup(filename)  # Load the SVG file
    ad.plot_run()  # Plot the SVG file
