from statemachine import State, StateMachine
from constants import Routes


class AppStateMachine(StateMachine):
    _route_for_current_state = None

    @property
    def route_for_current_state(self):
        return self._route_for_current_state

    @route_for_current_state.setter
    def route_for_current_state(self, value):
        self._route_for_current_state = value

    initial = State(initial=True)
    first_page = State(enter="entering_first_page", final=True)

    continue_from_initial = initial.to(first_page)

    def entering_first_page(self):
        self.route_for_current_state = Routes.first_page.value
