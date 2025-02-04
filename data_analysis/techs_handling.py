from data_analysis.diagram import diagram
from data_analysis.techs_counting import TechnologyCounting


def python_techs_handling(
        source_file_name: str,
        category: str = "Python",
        site_name: str = "Dou.ua",
    ) -> None:
    """Count technologies, save to csv and create diagram"""
    techs = TechnologyCounting(source_file_name)
    techs.save_to_csv()
    diagram(techs.technology_counter, category, site_name)
