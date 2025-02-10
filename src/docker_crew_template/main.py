# main.py 

# !/usr/bin/env python
import sys
import warnings

from docker_crew_template.crew import DockerCrewTemplate

# from crew import DockerCrewTemplate

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(url):
    """
    Run the crew.
    """
    inputs = {
        "topic": "AI LLMs",
        'url': url
    }
    DockerCrewTemplate().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
    }
    try:
        DockerCrewTemplate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DockerCrewTemplate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DockerCrewTemplate().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


# main.py

# !/usr/bin/env python
import sys
import warnings

from docker_crew_template.crew import DockerCrewTemplate

# from crew import DockerCrewTemplate

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(url):
    """
    Run the crew.
    """
    inputs = {
        "topic": "AI LLMs",
        'url': url
    }
    DockerCrewTemplate().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DockerCrewTemplate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DockerCrewTemplate().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        DockerCrewTemplate().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No arguments provided. Defaulting to 'run' mode.")
        run()
    elif sys.argv[1] == "train":
        train()
    elif sys.argv[1] == "replay":
        replay()
    elif sys.argv[1] == "test":
        test()
    elif sys.argv[1] == "run":
        if len(sys.argv) < 3:
            print("No URL provided for 'run' mode. Exiting.")
        else:
            run(sys.argv[2])
    else:
        print(f"Unknown command '{sys.argv[1]}'. Defaulting to 'run' mode.")
        run(sys.argv[1])
