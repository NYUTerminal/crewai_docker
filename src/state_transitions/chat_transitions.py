from transitions import Machine

# Define all possible states in the user onboarding workflow
states = ["ask_business_name", "ask_business_url", "ask_intent", "completed"]

class OnboardingFlow:
    def __init__(self):
        self.machine = Machine(model=self, states=states, initial="ask_business_name")

        # Define transitions
        self.machine.add_transition("got_business_name", "ask_business_name", "ask_business_url")
        self.machine.add_transition("got_business_url", "ask_business_url", "ask_intent")
        self.machine.add_transition("got_intent", "ask_intent", "completed")

    def get_next_state(self):
        return self.state

# Initialize FSM
fsm = OnboardingFlow()