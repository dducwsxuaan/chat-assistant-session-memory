import sys
from pathlib import Path

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from graph.builder import build_graph


def export_graph():
    graph = build_graph()

    png_bytes = graph.get_graph().draw_mermaid_png()

    with open("workflow_graph.png", "wb") as f:
        f.write(png_bytes)

    print("Graph saved as workflow_graph.png")


if __name__ == "__main__":
    export_graph()
