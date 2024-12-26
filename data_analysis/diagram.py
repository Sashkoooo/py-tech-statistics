from pathlib import Path

import matplotlib.pyplot as plt
from datetime import datetime

def diagram(technology_groups: dict) -> None:
    # Створення папки diagrams, якщо вона не існує
    diagrams_dir = Path.cwd().parent / "data" / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)

    # Поточна дата й час
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diagram_file = f"technology_frequencies_chart_{current_time}.png"

    technologies = list(technology_groups.keys())
    frequencies = list(technology_groups.values())

    # Створення стовпчикової діаграми
    plt.figure(figsize=(10, 6))
    plt.bar(technologies, frequencies, color="skyblue")
    plt.xlabel("Technology", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Frequency of Technologies in Job Descriptions", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Збереження діаграми у файл із зазначенням дати й часу
    plt.savefig(str(diagram_file))
    plt.close()

    print(f"Діаграма збережена у файл: {diagram_file}")
