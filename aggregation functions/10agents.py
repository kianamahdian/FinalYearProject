import csv


def majority_rule(stances):
    """Majority Rule: Aggregate based on simple vote counts."""
    in_count = stances.count('agree')
    out_count = stances.count('disagree')
    return 'agree' if in_count > out_count else 'disagree' if out_count > in_count else 'neutral'

def borda_count(stances):
    """Borda Count: Assign scores to stances based on ranking."""
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
    """Support First: Prioritize relationships over direct votes."""
    for related_stance, relation in relationships:
        if relation == 'defends' and related_stance == 'agree':
            return 'agree'
        elif relation == 'attacks' and related_stance == 'agree':
            return 'disagree'
    return majority_rule(stances)  # Use majority as fallback

def balanced_function(stances, relationships):
    """Balanced Function: Combine direct votes and relationships equally."""
    direct_result = majority_rule(stances)
    indirect_result = opinion_first(stances, relationships)
    if direct_result == indirect_result:
        return direct_result
    else:
        return 'neutral'


def evaluate_methods(norms, relationships):
    """Evaluate different voting methods using various metrics."""
    methods = {
        "Majority Rule": lambda s, r: majority_rule(s),
        "Borda Count": lambda s, r: borda_count(s),
        "Opinion First": opinion_first,
        "Support First": support_first,
        "Balanced Function": balanced_function,
    }

    metrics = {}
    for method_name, method in methods.items():
        consensus = 0
        total_norms = len(norms)

        for norm, norm_data in norms.items():
            stances = [agent["stance"] for agent in norm_data["arguments"]]
            if method_name in ["Majority Rule", "Borda Count"]:

                method_result = method(stances, None)
            else:

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
            agent = row['Agent']
            stance = row['Stance']
            argument = row['Argument']
            topic = row['Topic']

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
            for i in range(1, 11):  # Adjust to handle 10 agents
                agent_stance = row.get(f'Agent{i}_Stance', 'neutral')
                status = row.get(f'Status_Agent{i}', 'neutral')
                if agent_stance:
                    relationships[norm].append((agent_stance, status))

    return norms, relationships


norms, relationships = load_data(
    '/Users/kiana/Desktop/projectkarshenasi/complex_norms_and_stances.csv',
    '/Users/kiana/Desktop/projectkarshenasi/complex_relationships.csv'
)

metrics = evaluate_methods(norms, relationships)
print("Evaluation Metrics:")
for method, metric_values in metrics.items():
    print(f"{method}: {metric_values}")
