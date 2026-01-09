from dataclasses import dataclass

@dataclass
class DummyDesktopState:
    tree: dict
    screenshot: bytes | None = None

class Simulator:
    """Simple deterministic simulator harness for unit tests."""
    def __init__(self):
        self.state = DummyDesktopState(tree={"apps":[],"interactive":[]}, screenshot=None)

    def step_click(self, target_id: str):
        # deterministic behavior: if target exists, return success
        for el in self.state.tree.get("interactive",[]):
            if el.get("id") == target_id:
                return {"status":"ok","evidence":{"clicked":target_id},"confidence":1.0}
        return {"status":"error","details":"element_not_found","confidence":0.0}

    def add_element(self, el: dict):
        self.state.tree.setdefault("interactive",[]).append(el)

    def get_state(self):
        return self.state
