from data_analysis.diagram import diagram
from data_analysis.data_counting import VacanciesDataCounting


def python_techs_handling(
        source_file_name: str,
        category: str = "Python",
        site_name: str = "Dou.ua",
    ) -> None:
    """Count technologies, save to csv and create diagram"""
    vacancies = VacanciesDataCounting(source_file_name)
    vacancies.save_to_csv()
    vacancies.count_positions()
    diagram(
        technology_groups=vacancies.technology_counter,
        category=category,
        site_name=site_name,
        vacancies=vacancies.titles_number(),
        seniors_number=vacancies.senior,
        middles_number=vacancies.middle,
        juniors_number=vacancies.junior,
        not_specified_number=vacancies.not_specified
    )
