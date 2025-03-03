import csv


def majority_rule(stances):

    in_count = stances.count('agree')
    out_count = stances.count('disagree')
    return 'agree' if in_count > out_count else 'disagree' if out_count > in_count else 'neutral'

def borda_count(stances):

    scores = {"agree": 0, "disagree": 0, "neutral": 0}
    rank_values = {"agree": 3, "neutral": 2, "disagree": 1}
    for stance in stances:
        scores[stance] += rank_values[stance]
    return max(scores, key=scores.get)

def opinion_first(stances, relationships):
    """Opinion First: Prioritize direct votes, use relationships as tie-breakers."""
    result = majority_rule(stances)
    if result == 'neutral':
        for related_stance, relation in relationships:
            if relation == 'defends' and related_stance == 'agree':
                return 'agree'
            elif relation == 'attacks' and related_stance == 'agree':
                return 'disagree'
    return result

def support_first(stances, relationships):

    for related_stance, relation in relationships:
        if relation == 'defends' and related_stance == 'agree':
            return 'agree'
        elif relation == 'attacks' and related_stance == 'agree':
            return 'disagree'
    return majority_rule(stances)

def balanced_function(stances, relationships):

    direct_result = majority_rule(stances)
    indirect_result = opinion_first(stances, relationships)
    if direct_result == indirect_result:
        return direct_result
    else:
        return 'neutral'

def weighted_influence_voting(stances, relationships):


    agents = [f"Agent{i}" for i in range(len(stances))]
    agent_reputations = {agent: 1.0 for agent in agents}

    for related_stance, relation in relationships:
        if relation == 'defends':

            for agent in agents:
                if stances[agents.index(agent)] == related_stance:
                    agent_reputations[agent] += 2.0
        elif relation == 'attacks':

            for agent in agents:
                if stances[agents.index(agent)] == related_stance:
                    agent_reputations[agent] -= 1.5


    min_reputation = min(agent_reputations.values())
    if min_reputation < 0:
        for agent in agents:
            agent_reputations[agent] += abs(min_reputation) + 1.0


    scores = {"agree": 0.0, "disagree": 0.0, "neutral": 0.0}
    for agent, stance in zip(agents, stances):
        scores[stance] += agent_reputations[agent]


    max_score = max(scores.values())
    collective_stances = [s for s, score in scores.items() if score == max_score]


    if len(collective_stances) > 1:

        if 'agree' in collective_stances:
            return 'agree'
        elif 'disagree' in collective_stances:
            return 'disagree'
        else:
            return 'neutral'
    return collective_stances[0]




def evaluate_methods(norms, relationships):
    """Evaluate different voting methods using various metrics."""
    methods = {
        "Majority Rule": lambda s, r: majority_rule(s),
        "Borda Count": lambda s, r: borda_count(s),
        "Opinion First": opinion_first,
        "Support First": support_first,
        "Balanced Function": balanced_function,
        "Weighted Influence Voting": weighted_influence_voting,
    }

    metrics = {}
    for method_name, method in methods.items():
        consensus = 0
        total_norms = len(norms)

        for norm, norm_data in norms.items():
            stances = [agent["stance"] for agent in norm_data["arguments"]]
            if method_name in ["Majority Rule", "Borda Count"]:
                # Methods that only use stances
                method_result = method(stances, None)
            else:
                # Methods that use both stances and relationships
                method_result = method(stances, relationships.get(norm, []))
            if method_result != "neutral":
                consensus += 1

        metrics[method_name] = {
            "Consensus Ratio": consensus / total_norms
        }
    return metrics



def load_data(agents_file, relationships_file):
    """Load norms and relationships."""
    norms = {}
    relationships = {}


    with open(agents_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            norm = row['Norm']
            topic = row['Topic']
            agent = row['Agent']
            stance = row['Stance']
            argument = row['Argument']

            if norm not in norms:
                norms[norm] = {"topic": topic, "arguments": []}
            norms[norm]["arguments"].append({
                "agent": agent,
                "stance": stance,
                "argument": argument
            })


    with open(relationships_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            norm = row['Norm']
            if norm not in relationships:
                relationships[norm] = []
            agent1_stance = row['Agent1_Stance']
            agent2_stance = row['Agent2_Stance']
            status = row['Status']
            relationships[norm].append((agent1_stance, status))
            relationships[norm].append((agent2_stance, status))

    return norms, relationships


norms, relationships = load_data(
    '/Users/kiana/Desktop/projectkarshenasi/complex_norms_and_stances.csv',
    '/Users/kiana/Desktop/projectkarshenasi/complex_relationships.csv'
)

metrics = evaluate_methods(norms, relationships)
print("Evaluation Metrics:")
for method, metric_values in metrics.items():
    print(f"{method}: {metric_values}")
