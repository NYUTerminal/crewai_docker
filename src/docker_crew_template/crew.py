from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

from dotenv import load_dotenv

load_dotenv


# Uncomment the following line to use an example of a custom tool
# from docker_crew_template.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class DockerCrewTemplate():
    """DockerCrewTemplate crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def web_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraper'],
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )

    @task
    def web_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scraping_task'],
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DockerCrewTemplate crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
