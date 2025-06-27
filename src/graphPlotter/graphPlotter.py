import matplotlib.pyplot as plt

COLORS = ['blue', 'red', 'green', 'purple', 'white', 'black', 'orange']

def plot_results(voters, candidates, results):
    candidates_colors = {candidate: None for candidate in candidates}
    fig, ax = plt.subplots(figsize=(10, 2))

    # Plot candidates (as triangles)
    index = 0
    for candidate in candidates:
        color = COLORS[index % len(COLORS)]
        ax.plot(candidate.get_political_affiliation(), 0, '^', color=color, markersize=10)
        # ax.text(candidate.get_political_affiliation(), -0.3, candidate.id, ha='center', color='red')
        index += 1
        candidates_colors[candidate] = color

    # Plot voters (as circles)
    for voter in voters:
        voter_color = candidates_colors[voter.voted_for]
        ax.plot(voter.get_political_affiliation(), 0, 'o', color=voter_color)
        # ax.text(voter.get_political_affiliation(), 0.1, voter.id, ha='center', color='blue')

    # Styling
    ax.set_yticks([])  # Hide y-axis
    ax.set_xlabel("Position on 1D Spectrum")
    ax.set_xlim(min(v.get_political_affiliation() for v in voters + candidates) - 1,
                max(v.get_political_affiliation() for v in voters + candidates) + 1)
    ax.set_title("Voters and Candidates on 1D Plane")
    plt.tight_layout()

    # Show the plot in a new window
    plt.show()