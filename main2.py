import copy
import json


def choice(query, choices):
    choices_str = ''
    for i, x in enumerate(choices):
        choices_str += f"{i + 1}. {x}\n"
    got = "-1"
    while not got.isdigit() or int(got) not in range(1, len(choices) + 1):
        got = input(f"{query}\nChoose one:\n{choices_str}\n")
    return choices[int(got) - 1]


def prettify(lst):
    if len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return ' and '.join(lst)
    else:
        return ', '.join(lst[:-1]) + ', and ' + lst[-1]


class ExpertSystem:

    def __init__(self, display_rules=False):
        self.display_rules = display_rules
        self.facts = {}

        # read facts and rules
        with open('logic.json', 'r') as f:
            data = json.load(f)
        self.facts = {string: False for string in data['facts']}
        self.initial_questions = [string for string in data['facts']]
        self.future_questions = [string for string in data['facts']]
        self.filtered_rules = copy.deepcopy(data['rules'])
        self.initial_rules = copy.deepcopy(data['rules'])
        self.derived_facts = data['derived_facts']

        derived_facts = set()
        for key in self.derived_facts:
            for fact in self.derived_facts[key]:
                derived_facts.add(fact)

        for fact in derived_facts:
            self.facts[fact] = False

        self.no_more_questions = False
        self.exit = False

    def question(self):
        """
            Ask question according to current state. Update the state
        :return: None
        """

        chosen = choice("""
        Choose any ailment from below. Remember to choose only one at the time.
        If you want to address more conditions, you'll need to start it again.
        """, self.future_questions + ['None from the above'])
        if chosen == 'None from the above':
            self.no_more_questions = True
        else:
            self.facts[chosen] = True

            # remove unmatched rules
            to_remove = []
            for rule in self.filtered_rules:
                if chosen not in rule['conditions']:
                    to_remove.append(rule)

            for rm in to_remove:
                self.filtered_rules.remove(rm)

            # update potentially needed facts:
            future_questions = set()
            if chosen in self.derived_facts:
                for derived_fact in self.derived_facts[chosen]:
                    future_questions.add(derived_fact)
            for rule in self.filtered_rules:
                for fact in rule['conditions']:
                    if not self.facts[fact]:
                        future_questions.add(fact)

            self.future_questions = [x for x in future_questions]


    def format_answer(self, answer):
        return "#"*40+'\n'+answer+'#'*40
    def provide_answer(self):
        if len(self.filtered_rules) == 0:
            return "Couldn't find solution to your ailment. Please seek proper medical attention by calling 911."
        if self.no_more_questions or len(self.future_questions) == 0:
            total_output = ''
            for rule in self.filtered_rules[:-1]:
                if self.display_rules:
                    total_output += f"\tIn case of {prettify(rule['conditions'])}:\n\t\t{rule['output']}\n" + "-"*40+ '\n'
                else:
                    total_output += rule['output'] + '\n' + "-"*40+ '\n'

            if self.display_rules:
                total_output += f"\tIn case of {prettify(self.filtered_rules[-1]['conditions'])}:\n\t\t{self.filtered_rules[-1]['output']}\n"
            else:
                total_output += self.filtered_rules[-1]['output'] + '\n'

            return total_output

        if len(self.filtered_rules) == 1:
            if self.display_rules:
                return f"\tIn case of {prettify(self.filtered_rules[0]['conditions'])}:\n\t\t{self.filtered_rules[0]['output']}\n"
            else:
                return self.filtered_rules[0]['output']
        return None

    def reset_variables(self):
        for key in self.facts:
            self.facts[key] = False
        self.future_questions = copy.deepcopy(self.initial_questions)
        self.filtered_rules = copy.deepcopy(self.initial_rules)
        self.no_more_questions = False
        self.exit = False

    def start(self):
        while not self.exit:
            answer = None
            while answer is None:
                # ask question
                self.question()

                # check if there's answer:
                answer = self.provide_answer()
            print(self.format_answer(answer))
            ask_again = choice("Do you want to ask again?", ['yes', 'no'])
            if ask_again == 'no':
                self.exit = True

            # reset variables
            self.reset_variables()


expert_system = ExpertSystem()

expert_system.start()
