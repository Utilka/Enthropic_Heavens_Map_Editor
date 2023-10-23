from typing import NamedTuple, List, TypedDict, Dict, Callable, Union, Tuple

from System_DB_handler import load_systems
from utils import is_integer, is_coordinate_on_map, extract_units, RangePointer

all_systems = load_systems()


class SheetDelta(NamedTuple):
    """
    example of a SheetDelta
    {
        'target': 'AP Budget',
        'changes': -2,
    }
    """
    target: str
    changes: object


class Project(NamedTuple):
    name: str
    progress_made: Dict[str, int]  # Key is the resource type, value is the amount
    cost: Dict[str, int]
    validate_data_needed: List[str]
    validate_func: Callable[[Dict[str, object]], int]
    on_completion: List[SheetDelta] = []
    on_completion_custom: bool = False
    validate_data: Dict[str, object] = {}

    @property
    def can_be_done_times(self):
        return self.validate_func(self.validate_data)

    def progress(self, investment: Dict[str, int]) -> int:
        """takes given investment, saves it into the project
        returns how many times it was completed, limiting itself to can_be_done_times value
        subtracts the resources needed to complete project given times"""

        self._add_progress(investment)
        completions = self.calculate_possible_completions()
        self._subtract_completions(completions)

        return completions

    def calculate_possible_completions(self):
        # get how many times the self cost was fulfilled in order to finish it
        completions = min([(self.progress_made.get(res_type, 0) // res_amount)
                           for res_type, res_amount in self.cost.items()])
        # limit times done
        completions = min(completions, self.can_be_done_times)
        return completions

    def _subtract_completions(self, completions):
        if completions > 0:
            # remove the resources expended on the project
            for resource_type in self.progress_made:
                self.progress_made[resource_type] -= self.cost.get(resource_type, 0) * completions

    def _add_progress(self, investment):
        for res_type, amount in investment.items():
            if res_type in self.cost:
                self.progress_made[res_type] = self.progress_made.get(res_type, 0) + amount


class ActionResponse(NamedTuple):
    project: Project
    sheet_changes: List[SheetDelta]


class LocalAction:

    def __init__(self,
                 system_q: Union[int, str],
                 system_r: Union[int, str],
                 action_type: str,
                 action_description: str,
                 action_expenditure: str,
                 sheet_origin:RangePointer,
                 action_status: str = "",
                 action_status_explanation: str = "",
                 action_expenditure_coded: Dict[str, int] = None):
        self.system_r: Union[int, str] = system_r
        self.system_q: Union[int, str] = system_q
        self.action_type: str = action_type
        self.action_description: str = action_description
        self.action_expenditure: str = action_expenditure
        self.sheet_origin = sheet_origin

        self.action_status: str = action_status
        self.action_status_explanation: str = action_status_explanation
        if action_expenditure_coded is None:
            action_expenditure_coded = extract_units(self.action_expenditure)
        self.action_expenditure_coded: Dict[str, int] = action_expenditure_coded

        self.validate()

    def validate(self):
        if self.action_type == "":
            self.action_status = "Done"
            self.action_status_explanation = "Action type field is empty, skipping"
            return

        if not (is_integer(self.system_r) or is_integer(self.system_q)):
            self.action_status = "Invalid"
            self.action_status_explanation = "Failed to parse system coordinates"
            return
        elif not is_coordinate_on_map((int(self.system_r), int(self.system_q)), all_systems.shape):
            self.action_status = "Invalid"
            self.action_status_explanation = "Parsed coordinate is off the map"
            return
        elif all_systems[(int(self.system_r), int(self.system_q))] is None:
            self.action_status = "Invalid"
            self.action_status_explanation = "Parsed coordinate is of empty space on the map"
            return
        elif self.action_type not in system_action_project.keys():
            self.action_status = "Invalid"
            self.action_status_explanation = "Failed to find action type in the list"
            return

        self.action_status = "Valid"
        self.action_status_explanation = "Valid for insertion in the execution queue"
        return

    @property
    def coordinates(self) -> Tuple[int, int]:
        return int(self.system_q), int(self.system_r)

    def __str__(self):
        return f"{self.coordinates}:{self.action_type}:{self.action_expenditure}"


def custom():
    pass


# v for validate
def v_explore(investment: Dict[str, object]) -> int:
    pass


def v_build_dev(investment: Dict[str, object]) -> int:
    pass


def v_destroy_dev(investment: Dict[str, object]) -> int:
    pass


def v_build_SF_unit(investment: Dict[str, object]) -> int:
    pass


def v_disband_SF_unit(investment: Dict[str, object]) -> int:
    pass


#
#
# def build_sci_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_mil_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_sus_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_ind_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_sci_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_mil_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_system_force_unit(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_system_force_unit(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_fleet_unit(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_fleet_unit(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_system_improvement(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_system_improvement(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass


def do_actions(civ, project: Project, investment: Dict[str, int]):
    # validate projects
    # progress projects
    # compile sheet update
    pass


# system_action_handle = {
#     "custom": custom,
#     "explore": explore,
#     "build sus dev": build_sus_dev,
#     "build ind dev": build_ind_dev,
#     "build sci dev": build_sci_dev,
#     "build mil dev": build_mil_dev,
#     "destroy sus dev": destroy_sus_dev,
#     "destroy ind dev": destroy_ind_dev,
#     "destroy sci dev": destroy_sci_dev,
#     "destroy mil dev": destroy_mil_dev,
#     "build system force unit": build_system_force_unit,
#     "disband system force unit": destroy_system_force_unit,
#     "build fleet unit": build_fleet_unit,
#     "disband fleet unit": destroy_fleet_unit,
#     "build system improvement": build_system_improvement,
#     "destroy system improvement": destroy_system_improvement,
# }

system_action_project = {
                            "custom": custom,
                            "explore": Project("explore", {}, {"AP": 1}, ["AP Budget"], v_explore, [], True),

                            "build sus dev": Project("build sus dev", {}, {"AP": 10},
                                                     ["AP Budget", "Sus Dev Cap", "Rhodochrosite Supply"],
                                                     v_build_dev, [SheetDelta("Sus Dev", 1)]),
                            "build ind dev": Project("build ind dev", {}, {"AP": 10},
                                                     ["AP Budget", "Ind Dev Cap", "Rhodochrosite Supply"],
                                                     v_build_dev, [SheetDelta("Ind Dev", 1)]),
                            "build sci dev": Project("build sci dev", {}, {"AP": 40},
                                                     ["AP Budget", "Sci Dev Cap", "Rhodochrosite Supply"],
                                                     v_build_dev, [SheetDelta("Sci Dev", 1)]),
                            "build mil dev": Project("build mil dev", {}, {"AP": 30},
                                                     ["AP Budget", "Mil Dev Cap", "Rhodochrosite Supply"],
                                                     v_build_dev, [SheetDelta("Mil Dev", 1)]),

                            "destroy sus dev": Project("destroy sus dev", {}, {"AP": 5}, ["AP Budget", "Sus Dev"],
                                                       v_destroy_dev,
                                                       [SheetDelta("Sus Dev", -1)]),
                            "destroy ind dev": Project("destroy ind dev", {}, {"AP": 5}, ["AP Budget", "Ind Dev"],
                                                       v_destroy_dev,
                                                       [SheetDelta("Ind Dev", -1)]),
                            "destroy sci dev": Project("destroy sci dev", {}, {"AP": 5}, ["AP Budget", "Sci Dev"],
                                                       v_destroy_dev,
                                                       [SheetDelta("Sci Dev", -1)]),
                            "destroy mil dev": Project("destroy mil dev", {}, {"AP": 5}, ["AP Budget", "Mil Dev"],
                                                       v_destroy_dev,
                                                       [SheetDelta("Mil Dev", -1)]),

                            "build system force unit": Project("build system force unit", {}, {"AP": 5, "WU": 1},
                                                               ["AP Budget", "WU Progress"],
                                                               v_build_SF_unit, [SheetDelta("SF unit", 1)]),
                            "disband system force unit": Project("disband system force unit", {}, {"AP": 5, "WU": 1},
                                                                 ["AP Budget", "WU Progress"],
                                                                 v_disband_SF_unit, [SheetDelta("SF unit", -1),
                                                                                     SheetDelta("WU Progress", 1)]),

                            "build fleet unit": Project("build fleet unit", {}, {"AP": 5, "WU": 1},
                                                        ["AP Budget", "WU Progress"],
                                                        # TODO add other fleet cost modifiers
                                                        v_build_fleet_unit, [SheetDelta("Fleet unit", 1)]),
                            "disband fleet unit": Project("build fleet unit", {}, {"AP": 5, "WU": 1},
                                                          ["AP Budget", "WU Progress"],
                                                          # TODO add other fleet cost modifiers
                                                          v_disband _fleet_unit, [SheetDelta("Fleet unit", -1),
                                                                                  SheetDelta("WU Progress", 1)]]),

"build system improvement": build_system_improvement,
"destroy system improvement": destroy_system_improvement,
}
