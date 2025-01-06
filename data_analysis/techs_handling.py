from data_analysis.diagram import diagram
from data_analysis.techs_counting import TechnologyCounting


def techs_handling(file_name: str) -> None:
    """Count technologies, save to csv and create diagram"""
    techs = TechnologyCounting(file_name)
    techs.save_to_csv()
    diagram(techs.technology_counter)
