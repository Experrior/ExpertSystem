import json
import copy

def choice(query, choices):
    choices_str = ''
    for i, x in enumerate(choices):
        choices_str += f"{i+1}. {x}\n"
    got = "-1"
    while not got.isdigit() or int(got) not in range(1, len(choices)+1):
        got = input(f"{query}\nChoose one:\n{choices_str}\n")
    return choices[int(got)-1]


class ExpertSystem:

    def __init__(self):

        self.facts = {}
        self.rules = {}
        # read facts and rules
        with open('logic.json', 'r') as f:
            data = json.load(f)
        self.facts = {string: False for string in data['facts']}
        self.rules = data['rules']

        self.facts['exit'] = False

        self.filtered_rules = copy.deepcopy(data['rules'])
        self.filtered_facts = [string for string in data['facts']]
        self.no_more_questions = False

    def question(self):
        """
            Ask question according to current state. Update the state
        :return: None
        """

        chosen = choice("""
        Choose any ailment from below. Remember to choose only one at the time.
        If you want to address more conditions, you'll need to start it again.
        """, self.filtered_facts+['None from the above'])
        if chosen == 'None from the above':
            self.no_more_questions = True
        else:
            self.facts[chosen] = True
            # self.filtered_rules = {key:self.facts[key] for key in self.facts if chosen in self.facts[key].conditions}
            to_remove = []
            for rule in self.filtered_rules:
                if chosen not in rule['conditions']:
                    to_remove.append(rule)

            for rm in to_remove:
                self.filtered_rules.remove(rm)
            # update potentially needed facts:
            filtered_facts = set()
            for rule in self.filtered_rules:
                for fact in rule['conditions']:
                    if not self.facts[fact]:
                        filtered_facts.add(fact)

            self.filtered_facts = [x for x in filtered_facts]


    def provide_answer(self):
        if self.no_more_questions or len(self.filtered_facts) == 0:
            return self.filtered_rules
        if len(self.filtered_rules) == 0:
            return "Couldn't find solution to your ailment. Please seek proper medical attention by calling 911."
        return None

    def start(self):
        while not self.facts['exit']:
            answer = None
            while answer is None:
                # ask question
                self.question()

                # check if there's answer:
                answer = self.provide_answer()
            print(answer)
            exit = choice("Do you want to ask again?",['yes', 'no'])
            if exit == 'no':
                self.facts['exit'] = True
            # reset variables

expert_system = ExpertSystem()

expert_system.start()




