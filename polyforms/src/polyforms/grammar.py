import re

def replace_rule(arg, rule):
    # Function to be used as the replacement in re.sub
    def repl(match):
        # Extract the matched text without brackets
        key = match.group(1)
        # Return the corresponding replacement from the dict, if exists
        return rule.get(key, match.group(0))

    # Pattern to match text within square brackets
    pattern = r'\[(.*?)\]'
    # Perform the substitution
    replaced_arg = re.sub(pattern, repl, arg)
    return replaced_arg

class Grammar:
    def __init__(self, start, rules):
        self.start = start
        self.rules = rules

    def derive(self, moves):
        current = self.start
        for move in moves:
            rule = self.rules[move]
            current = replace_rule(current, rule)
        current_no_brackets = re.sub(r'\[.*?\]', '', current)
        return current_no_brackets.upper()





