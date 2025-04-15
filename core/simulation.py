from agents.agent_setup import create_agents
from game.game_loop import rooms
from config.settings import NUM_ROUNDS
from data.database import log_round_metadata, write_csv, log_game_model_selection
import random

NUM_ROUNDS = 10  # increased to 10 rounds for a clearer end condition
_current_game = {}

def setup_game(game_id, selected_model="All"):
    agents, agents_state = create_agents(game_id, selected_model)
    all_rooms = list(rooms.keys())
    state = {
        agent.name: {
            "room": random.choice(all_rooms),
            "killed": False,
            "room_body": None,
            "perception": [],
            "task_room": random.choice(all_rooms) if agent.__class__.__name__ == "HonestAgent" else None,
            "task_done": False,
            "doing_task": False,
            "ejected": False
        } for agent in agents
    }

    state["_reported_bodies"] = set()

    alive = sum(1 for v in state.values() if isinstance(v, dict) and not v.get("killed"))
    dead = sum(1 for v in state.values() if isinstance(v, dict) and v.get("killed"))

    log_round_metadata(game_id, 0, alive, dead)
    log_game_model_selection(game_id, selected_model)

    _current_game.update({"state": state, "agents": agents, "agents_state": agents_state, "round": 0})
    return agents, agents_state, state

def get_current_state():
    return _current_game.get("agents", []), _current_game.get("state", {})
