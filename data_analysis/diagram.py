from pathlib import Path

import matplotlib.pyplot as plt
from datetime import datetime

def diagram(technology_groups: dict) -> None:
    """
    Create a bar chart to visualize
    the frequency of technologies
    in job descriptions
    """
    diagrams_dir = Path.cwd() / "data" / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diagram_file = diagrams_dir / f"technology_frequencies_chart_{current_time}.png"

    # Sort technologies by frequency
    sorted_technology_groups = sorted(
        technology_groups.items(), key=lambda x: x[1], reverse=True
    )
    technologies = [item[0] for item in sorted_technology_groups]
    frequencies = [item[1] for item in sorted_technology_groups]

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(technologies, frequencies, color="skyblue")
    ax.set_xlabel("Technology", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title("Frequency of Technologies in Job Descriptions", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Add frequency labels
    ax.bar_label(bars, fmt='%d', padding=3, fontsize=10, color="black")

    plt.savefig(diagram_file, dpi=300)
    plt.close()

    print(f"Diagram saved to: {diagram_file}")
