import matplotlib.pyplot as plt

COLORS = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan', 'magenta', 'yellow']

def plot_results_1D(voters, candidates, results, winner):
    candidates_colors = {candidate: None for candidate in candidates}
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.axhline(y=0, color='gray', linewidth=1)

    # Plot candidates (as triangles)
    index = 0
    for candidate in candidates:
        color = COLORS[index % len(COLORS)]
        ax.plot(candidate.get_political_affiliation(), 0, '^', color=color, markersize=20)
        ax.text(candidate.get_political_affiliation(), 0.5, candidate.id, color='black', fontsize=8, ha='center')
        index += 1
        candidates_colors[candidate] = color

    # Plot voters (as circles)
    for voter in voters:
        voter_color = 'grey'
        if voter.has_voted:
            voter_color = candidates_colors[voter.voted_for]
        ax.plot(voter.get_political_affiliation(), 0, 'o', color=voter_color, markersize=1)
        # ax.text(voter.get_political_affiliation(), 0.1, voter.id, ha='center', color='blue')

    # Styling
    ax.set_yticks([])  # Hide y-axis
    ax.set_xlabel("Position on 1D Spectrum")
    ax.set_xlim(min(v.get_political_affiliation() for v in voters + candidates) - 1,
                max(v.get_political_affiliation() for v in voters + candidates) + 1)
    ax.set_title("Winner - " + winner.id)
    ax.set_ylim(-1, 1)
    plt.tight_layout()

    # Show the plot in a new window
    plt.show()

def plot_approvals_2D(voters, candidates, results, winner, approval_distance):
    candidates_colors = {candidate: None for candidate in candidates}
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot candidates and their approval distances as circles
    index = 0
    for candidate in candidates:
        color = COLORS[index % len(COLORS)]
        candidate_political = candidate.get_political_affiliation()
        ax.plot(candidate_political[0], candidate_political[1], '^', color=color, markersize=20)
        ax.text(candidate_political[0], candidate_political[1] + 1, candidate.id, color='black', fontsize=8, ha='center')
        index += 1
        candidates_colors[candidate] = color
    # Plot voters and their approval distances as circles
    for voter in voters:
        voter_color = 'grey'
        ax.plot(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1], 'o', color=voter_color, markersize=5)
        # ax.text(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1] + 1, voter.id, ha='center', color='blue')
    # Plot approval distances as circles around candidates
    for candidate in candidates:
        candidate_political = candidate.get_political_affiliation()
        circle = plt.Circle(candidate_political, approval_distance, color=candidates_colors[candidate], fill=False, linestyle='--')
        ax.add_artist(circle)
    # Styling
    ax.set_xlabel("Political Affiliation X")
    ax.set_ylabel("Political Affiliation Y")
    ax.set_title("Winner - " + winner.id)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.tight_layout() 
    # Show the plot in a new window
    plt.show()

def plot_scores_2D(voters, candidates, results, winner, score_distances):
    candidates_colors = {candidate: None for candidate in candidates}
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot candidates and their approval distances as circles
    index = 0
    for candidate in candidates:
        color = COLORS[index % len(COLORS)]
        candidate_political = candidate.get_political_affiliation()
        ax.plot(candidate_political[0], candidate_political[1], '^', color=color, markersize=20)
        ax.text(candidate_political[0], candidate_political[1] + 1, candidate.id, color='black', fontsize=8, ha='center')
        index += 1
        candidates_colors[candidate] = color
    # Plot voters and their approval distances as circles
    for voter in voters:
        voter_color = 'grey'
        ax.plot(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1], 'o', color=voter_color, markersize=5)
        # ax.text(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1] + 1, voter.id, ha='center', color='blue')
    # Plot approval distances as circles around candidates
    for candidate in candidates:
        candidate_political = candidate.get_political_affiliation()
        circle = plt.Circle(candidate_political, score_distances[0], color=candidates_colors[candidate], fill=False, linestyle='--')
        ax.add_artist(circle)
        circle = plt.Circle(candidate_political, score_distances[1], color=candidates_colors[candidate], fill=False, linestyle='--')
        ax.add_artist(circle)
    # Styling
    ax.set_xlabel("Political Affiliation X")
    ax.set_ylabel("Political Affiliation Y")
    ax.set_title("Winner - " + winner.id)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.tight_layout() 
    # Show the plot in a new window
    plt.show()

def plot_results_2D(voters, candidates, results, winner):
    candidates_colors = {candidate: None for candidate in candidates}
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot candidates (as triangles)
    index = 0
    for candidate in candidates:
        color = COLORS[index % len(COLORS)]
        candidate_political = candidate.get_political_affiliation()
        ax.plot(candidate_political[0], candidate_political[1], '^', color=color, markersize=20)
        ax.text(candidate_political[0], candidate_political[1] + 1, candidate.id, color='black', fontsize=8, ha='center')
        index += 1
        candidates_colors[candidate] = color

    # Plot voters (as circles)
    for voter in voters:
        voter_color = 'grey'
        if voter.has_voted:
            voter_color = candidates_colors[voter.voted_for]
        ax.plot(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1], 'o', color=voter_color, markersize=5)
        # ax.text(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1] + 1, voter.id, ha='center', color='blue')

    # Styling
    ax.set_xlabel("Political Affiliation X")
    ax.set_ylabel("Political Affiliation Y")
    ax.set_title("Winner - " + winner.id)
    plt.tight_layout()

    # Show the plot in a new window
    plt.show()

def plot_results_per_rounds_2D(voters, candidates, results, winner):
    counter = 0
    for rnd in results:
        counter += 1
        round_candidates = list(rnd.keys())
        candidates_colors = {candidate: None for candidate in round_candidates}
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Plot candidates (as triangles)
        index = 0
        for candidate in round_candidates:
            color = COLORS[index % len(COLORS)]
            candidate_political = candidate.get_political_affiliation()
            ax.plot(candidate_political[0], candidate_political[1], '^', color=color, markersize=20)
            ax.text(candidate_political[0], candidate_political[1] + 1, candidate.id, color='black', fontsize=8, ha='center')
            index += 1
            candidates_colors[candidate] = color

        # Plot voters (as circles)
        for voter in voters:
            voter_color = 'grey'
            if voter.has_voted:
                voted_for = None
                for cand in voter.ranked_candidates:
                    if cand["candidate"] in round_candidates:
                        voted_for = cand["candidate"]
                        break
                # print("voted for " + str(voted_for) + " in round " + str(counter))
                voter_color = candidates_colors[voted_for]
            ax.plot(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1], 'o', color=voter_color, markersize=5)
            # ax.text(voter.get_political_affiliation()[0], voter.get_political_affiliation()[1] + 1, voter.id, ha='center', color='blue')

        # Styling
        ax.set_xlabel("Political Affiliation X")
        ax.set_ylabel("Political Affiliation Y")
        title = "Round " + str(counter)
        is_winner = max(rnd.values()) > sum(rnd.values()) / 2
        if not is_winner:
            eliminated_candidate = min(round_candidates, key=lambda x: rnd[x])
            title += " - Eliminate: " + eliminated_candidate.id
        else:
            title += " - Winner: " + max(round_candidates, key=lambda x: rnd[x]).id

        ax.set_title(title)
        plt.tight_layout()

        # Show the plot in a new window
        plt.show()