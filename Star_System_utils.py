from typing import NamedTuple, List, TypedDict, Dict, Callable

from utils import Pointer, alphabetic_to_numeric_column

acell_relative_reference = {
    "AP net": Pointer("K", 15),
    "AP Budget": Pointer("H", 11),
    "WU Progress": Pointer("G", 13),
    "WU Progress next T": Pointer("H", 13),
    "SF Unit count": Pointer("P", 13),
    "System q": Pointer("B", 2),
    "System r": Pointer("C", 2),
    "System Name": Pointer("F", 2),
    "Fleet q": Pointer("B", 2),
    "Fleet r": Pointer("C", 2),
    "Fleet Name": Pointer("F", 2),
    "Fleet Unit count": Pointer("F", 5),
    "Fleet Jump range": Pointer("K", 5),
    "Fleet Turn Last Moved": Pointer("J", 7),
}

cell_relative_reference = {
    cell_name: Pointer(
        row=cell_pointer.row,
        column=alphabetic_to_numeric_column(cell_pointer.column)
    )
    for cell_name, cell_pointer in acell_relative_reference.items()
}


class SheetDelta(TypedDict):
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
    validate_data: Dict[str, object]
    validate_func: Callable[[Dict[str, object]], int]

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


def custom():
    pass

#
# def explore(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_sus_dev(civ, project: Project, investment: Dict[str, int]) -> ActionResponse:
#     pass
#
#
# def build_ind_dev(civ, project: Project, investment: List[Resourse]) -> ActionResponse:
#     pass
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