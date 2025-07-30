from algorithms.agent import Agent


def write_output(file_path: str, agent: Agent, RES):
    """
    Write the output to the file.

    Args:
        file_path (str): The path to the output file.
        agent (Agent): The Agent object containing the game state.
    """
    with open(file_path, "w") as file:
        for cell in RES:
            file.write(f"({cell[0][0] + 1}, {cell[0][1] + 1}) : {cell[1]}\n")
        file.write("-------------------------\n")
        if (
            RES[len(RES) - 1][0][0] + 1 == 1
            and RES[len(RES) - 1][0][1] + 1 == 1
            and RES[len(RES) - 1][1] == "Climb"
        ):
            file.write("Agent successfully climbs out the cave. You win !!!\n")
            file.write(f"SCORE: {agent.point}\n")
            file.write(f"HEALTH: {agent.current_hp}\n")
        else:
            file.write("Agent dies. You lose !!!\n")
            file.write(f"SCORE: {agent.point}\n")
            file.write(f"HEALTH: {agent.current_hp}\n")
