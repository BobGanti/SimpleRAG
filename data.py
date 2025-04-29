# data.py
import os
import syntaxmatrix as smx
from syntaxmatrix.plottings import figure, plotly
import numpy as np
import mpl_toolkits.mplot3d  # noqa: F401
from sklearn.decomposition import PCA
from sklearn import datasets

#//////////////// Visualisation Demo ////////////////////////#
# Test error, success, warning, and info outputs.
def writing():
    smx.success(f'{5} > {3}: Yes')
    smx.error(f'{8} < {5}: No')
    smx.warning("Warning: This is a warning message.")
    smx.info("Info: This is an informational message.")

def markdown():
    smx.markdown(
        "# Markdown Header\n\n"
        "This is a test of **bold** and *italic* text\n\n"
        "- Item A\n"
        "- Item B\n"
        "- Item C\n\n"
        "## Subheading\n\n"
        "Some more text here."
    )

def latex():
    # LaTeX Examples
    # --------------
    smx.markdown("### Mathematical Expressions using LaTeX")

    smx.latex(r"x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")
    smx.latex("e^{i\\pi} + 1 = 0")
    smx.latex("\\int_{0}^{\\infty} e^{-x} dx = 1")
    smx.latex("\\frac{d}{dx}(x^2) = 2x")
    smx.latex("\\lim_{x \\to 0} \\frac{\\sin(x)}{x} = 1")
    smx.latex("\\sum_{n=1}^{\\infty}\\frac{1}{n^2} = \\frac{\\pi^2}{6}")

def plt_plottings():
    # ---------------------------------------------------
    # Matplotlib Visualizations
    # -------------------------
    plt_plots = []
    # Matplotlib Line Plot
    fig_line = figure()
    ax_line = fig_line.add_subplot(111)
    ax_line.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o', linestyle='-', color='blue')
    ax_line.set_title("Matplotlib Line Plot")
    ax_line.set_xlabel("X-axis")
    ax_line.set_ylabel("Y values")
    ax_line.grid(True)
    smx.plt_plot(fig_line)

    # Matplotlib Bar Chart (separate figure!)
    fig_bar = figure()
    ax_bar = fig_bar.add_subplot(111)
    ax_bar.bar(['A', 'B', 'C'], [5, 10, 15], color='green')
    ax_bar.set_title("Matplotlib Bar Chart")
    ax_bar.set_xlabel("Categories")
    ax_bar.set_ylabel("Values")
    smx.plt_plot(fig_bar)

    # # Matplotlib Histogram
    # random_data = np.random.randn(1000)
    # fig_hist = figure()
    # ax_hist = fig_hist.add_subplot(111)
    # ax_hist.hist(random_data, bins=20, color='purple')
    # ax_hist.set_title("Matplotlib Histogram")
    # ax_hist.set_xlabel("Bins")
    # ax_hist.set_ylabel("Frequency")
    # plt_plots.append(smx.plt_plot(fig_hist))

    # iris = datasets.load_iris()
    # fig = figure(1, figsize=(8, 6))
    # ax = fig.add_subplot(111, projection="3d", elev=-150, azim=110)
    # X_reduced = PCA(n_components=3).fit_transform(iris.data)
    # ax.scatter(
    #     X_reduced[:, 0],
    #     X_reduced[:, 1],
    #     X_reduced[:, 2],
    #     c=iris.target,
    #     s=40,
    # )
    # ax.set_title("First three PCA dimensions")
    # ax.set_xlabel("1st Eigenvector")
    # ax.xaxis.set_ticklabels([])
    # ax.set_ylabel("2nd Eigenvector")
    # ax.yaxis.set_ticklabels([])
    # ax.set_zlabel("3rd Eigenvector")
    # ax.zaxis.set_ticklabels([])
    # smx.plt_plot(fig)

    # return plt_plots

def plotly_plottings():
    ply_plots = []
    # Plotly Scatter Plot (Interactive with Hover)
    px = plotly()
    df_iris = px.data.iris()
    fig_scatter = px.scatter(
        df_iris, 
        x="sepal_width", 
        y="sepal_length", 
        color="species", 
        title="Plotly Iris Scatter Plot",
        labels={"sepal_width": "Sepal Width", "sepal_length": "Sepal Length"}
    )
    ply_plots.append(smx.plotly_plot(fig_scatter))

    # Plotly Boxplot
    fig_box = px.box(
        df_iris, 
        x="species", 
        y="petal_length", 
        color="species", 
        title="Plotly Boxplot"
    )
    ply_plots.append(smx.plotly_plot(fig_box))

    # Plotly Histogram
    fig_hist = px.histogram(
        df_iris, 
        x="sepal_width", 
        nbins=20, title="Plotly Sepal Width Histogram",
        color="species", barmode='overlay', opacity=0.75
    )
    ply_plots.append(smx.plotly_plot(fig_hist))

    return ply_plots

# //////////// End Visualisation Demo /////////////////////////#