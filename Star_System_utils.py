import re
from copy import deepcopy
from typing import NamedTuple, List, TypedDict, Dict, Callable, Union, Tuple, Any

from System_DB_handler import load_systems
from utils import is_integer, is_coordinate_on_map, RangePointer, extract_units_quantity, SheetDelta, acell

all_systems = load_systems()




class Project(NamedTuple):
    name: str
    progress_made: Dict[str, int]  # Key is the resource type, value is the amount
    cost: Dict[str, int]
    validate_data_needed: List[str]
    validate_func: Callable[['Project', Dict[str, object]], int]
    on_completion: List[SheetDelta] = []
    on_completion_custom: bool = False
    validate_data: Dict[str, Any] = {}

    @property
    def can_be_done_times(self):
        return self.validate_func(self, self.validate_data)


    def progress(self, investment: Dict[str, int]) -> int:
        """takes given investment, saves it into the project
        returns how many times it was completed, limiting itself to can_be_done_times value
        subtracts the resources needed to complete project given times"""

        self._add_progress(investment)
        return self.complete()

    def _subtract_completions(self, completions):
        if completions > 0:
            # remove the resources expended on the project
            for resource_type in self.progress_made:
                self.progress_made[resource_type] -= self.cost.get(resource_type, 0) * completions

    def _add_progress(self, investment):
        for res_type, amount in investment.items():
            if res_type in self.cost:
                self.progress_made[res_type] = self.progress_made.get(res_type, 0) + amount

    def complete(self) -> int:

        """returns how many times project is completed with investment that is in it,
        limiting itself to can_be_done_times value
        subtracts the resources needed to complete project given times"""

        completions = self.can_be_done_times
        self._subtract_completions(completions)

        return completions


class LocalAction:

    def __init__(self,
                 system_q: Union[int, str],
                 system_r: Union[int, str],
                 action_type: str,
                 description: str,
                 expenditure: str,
                 turn_sheet_origin: RangePointer,
                 status: str = "",
                 status_explanation: str = "",
                 expenditure_coded: Dict[str, int] = None):
        self.system_r: Union[int, str] = system_r
        self.system_q: Union[int, str] = system_q
        self.action_type: str = action_type
        self.description: str = description
        self.expenditure: str = expenditure
        self.turn_sheet_origin = turn_sheet_origin

        self.status: str = status
        self.status_explanation: str = status_explanation
        if expenditure_coded is None:
            expenditure_coded = extract_units_quantity(self.expenditure)
        self.expenditure_coded: Dict[str, int] = expenditure_coded

        self.validate()

    def validate(self):
        if self.action_type == "":
            self.status = "Executed"
            self.status_explanation = "Action type field is empty, skipping"
            return

        if self.action_type in need_manual_execution:
            self.status = "Need Manual Execution"
            self.status_explanation = f"{self.action_type} is in need_manual_execution list"
            return

        if not (is_integer(self.system_r) or is_integer(self.system_q)):
            self.status = "Invalid"
            self.status_explanation = f"Failed to parse system coordinates: {self.coordinates_s}"
            return
        elif not is_coordinate_on_map((int(self.system_r), int(self.system_q)), all_systems.shape):
            self.status = "Invalid"
            self.status_explanation = f"Parsed coordinate is off the map: {self.coordinates}"
            return
        elif all_systems[(int(self.system_r), int(self.system_q))] is None:
            self.status = "Invalid"
            self.status_explanation = f"Parsed coordinate is of empty space on the map: {self.coordinates}"
            return
        # elif self.action_type not in system_action_project.keys():
        #     self.action_status = "Invalid"
        #     self.action_status_explanation = "Failed to find action type in the list"
        #     return

        self.status = "Valid"
        self.status_explanation = f"Valid for insertion in the execution queue: " \
                                  f"{self.coordinates} [{self.action_type}] {{{self.expenditure_coded}}} "
        return

    @property
    def coordinates(self) -> Tuple[int, int]:
        return int(self.system_q), int(self.system_r)

    @property
    def coordinates_s(self) -> str:
        return f"{self.system_q}, {self.system_r}"

    def __str__(self):
        return f"{self.coordinates}:{self.action_type}:{self.expenditure}"


def custom():
    pass


# v for validate
def v_explore(available_resources: Dict[str, object]) -> int:
    pass


def v_build_dev(project: Project) -> int:
    rhodochrosite = int(project.validate_data["Rhodochrosite Supply"])

    AP_cost_of_dev = Project.cost["AP"] * (1 - 0.1 * min(1, rhodochrosite))
    AP_invested = project.progress_made.get("AP", 0)

    compl = AP_invested // AP_cost_of_dev
    cap = int(project.validate_data[project.validate_data_needed[0]][0][0])

    completions = min(compl, cap)
    return completions


def v_destroy_dev(project: Project) -> int:
    rhodochrosite = int(project.validate_data["Rhodochrosite Supply"])

    AP_cost_of_dev = Project.cost["AP"] * (1 - 0.1 * min(1, rhodochrosite))
    AP_invested = project.progress_made.get("AP", 0)

    compl = AP_invested // AP_cost_of_dev
    cap = int(project.validate_data[project.validate_data_needed[0]][0][0])

    completions = min(compl, cap)
    return completions


def v_build_SF_unit(project: Project) -> int:
    # AP_cost_of_dev = Project.cost["AP"]
    # AP_invested = project.progress_made.get("AP", 0)
    # WU_cost_of_dev = Project.cost["WU"]
    # WU_invested = project.progress_made.get("WU", 0)
    # compl = min(AP_invested // AP_cost_of_dev, WU_invested // WU_cost_of_dev)
    # cap = int(project.validate_data[project.validate_data_needed[0]][0][0])
    # completions = min(compl, cap)
    pass


def v_disband_SF_unit(project: Project, available_resources: Dict[str, Any]) -> int:
    pass


def v_build_fleet_unit(project: Project, available_resources: Dict[str, Any]) -> int:
    pass


def v_disband_fleet_unit(project: Project, available_resources: Dict[str, Any]) -> int:
    pass


# def build_sci_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_mil_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_sus_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_ind_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_sci_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_mil_dev(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_system_force_unit(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_system_force_unit(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_fleet_unit(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_fleet_unit(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def build_system_improvement(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass
#
#
# def destroy_system_improvement(civ, project: Project, available_resources: List[Resourse]) -> ActionResponse:
#     pass


def extract_project(project_string):
    # Extract project name
    project_name_match = re.search(r'\[([^\]]+)\]', project_string)
    project_name = project_name_match.group(1) if project_name_match else None

    # Extract code expenditure progress
    progress_matches = re.findall(r'(\d+/\d+ [A-Z]+)', project_string)
    progress_dict = {}
    for match in progress_matches:
        value, key = match.split()
        progress, goal = value.split('/')
        progress_dict[key] = {
            "progress": int(progress),
            "goal": int(goal)
        }
    result = deepcopy(system_action_project[project_name])
    result.progress_made = {resource: progr["progress"] for resource, progr in progress_dict}
    result.cost = {resource: progr["goal"] for resource, progr in progress_dict}

    return result


def get_project(project_name):
    return deepcopy(system_action_project[project_name])


def merge_project_pools(existing_project_pool: Dict[str, Dict[str, Project]],
                        new_project_pool: Dict[str, Dict[str, Project]]) \
        -> Dict[str, Dict[str, Project]]:
    merged_project_pool = {}

    for system_coordinates, existing_project_types in existing_project_pool.items():
        merged_project_types = {}

        if system_coordinates in new_project_pool:
            new_project_types = new_project_pool[system_coordinates]

            for project_type, existing_project in existing_project_types.items():
                if project_type in new_project_types:
                    matching_new_project = new_project_types[project_type]

                    # Merge progress_made
                    merged_progress = {resource: existing_project.progress_made.get(resource, 0)
                                                 + matching_new_project.progress_made.get(resource, 0)
                                       for resource in
                                       set(existing_project.progress_made) | set(matching_new_project.progress_made)}

                    # Create a merged project
                    merged_project = existing_project._replace(
                        progress_made=merged_progress,
                        on_completion=matching_new_project.on_completion,
                        on_completion_custom=matching_new_project.on_completion_custom
                    )
                    merged_project_types[project_type] = merged_project

                    # Remove the matched project type from the new_project_types dict
                    del new_project_types[project_type]
                else:
                    # If no matching project type is found, just add the existing project to the merged dict
                    merged_project_types[project_type] = existing_project

            # Add remaining project types from the new dict
            merged_project_types.update(new_project_types)
        else:
            # If no matching system coordinates are found,just add the existing project types to the merged project pool
            merged_project_types = existing_project_types

        merged_project_pool[system_coordinates] = merged_project_types

    # Handle system coordinates that only exist in the new project map
    for system_coordinates, project_types in new_project_pool.items():
        if system_coordinates not in merged_project_pool:
            merged_project_pool[system_coordinates] = project_types

    return merged_project_pool


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
#
system_action_project = {
    "custom": custom,
    "explore": Project("explore", {}, {"AP": 1}, ["AP Budget"], v_explore, [], True),

    "build sus dev": Project("build sus dev", {}, {"AP": 10},
                             ["Sus Dev Cap", "Rhodochrosite Supply"],
                             v_build_dev, [SheetDelta("Sus Dev", 1)]),
    "build ind dev": Project("build ind dev", {}, {"AP": 10},
                             ["Ind Dev Cap", "Rhodochrosite Supply"],
                             v_build_dev, [SheetDelta("Ind Dev", 1)]),
    "build sci dev": Project("build sci dev", {}, {"AP": 40},
                             ["Sci Dev Cap", "Rhodochrosite Supply"],
                             v_build_dev, [SheetDelta("Sci Dev", 1)]),
    "build mil dev": Project("build mil dev", {}, {"AP": 30},
                             ["Mil Dev Cap", "Rhodochrosite Supply"],
                             v_build_dev, [SheetDelta("Mil Dev", 1)]),

    "destroy sus dev": Project("destroy sus dev", {}, {"AP": 5},
                               ["Sus Dev"],
                               v_destroy_dev,
                               [SheetDelta("Sus Dev", -1)]),
    "destroy ind dev": Project("destroy ind dev", {}, {"AP": 5},
                               ["Ind Dev"],
                               v_destroy_dev,
                               [SheetDelta("Ind Dev", -1)]),
    "destroy sci dev": Project("destroy sci dev", {}, {"AP": 5},
                               ["Sci Dev"],
                               v_destroy_dev,
                               [SheetDelta("Sci Dev", -1)]),
    "destroy mil dev": Project("destroy mil dev", {}, {"AP": 5},
                               ["Mil Dev"],
                               v_destroy_dev,
                               [SheetDelta("Mil Dev", -1)]),

    # "build system force unit": Project("build system force unit", {}, {"AP": 5, "WU": 1},
    #                                    [],
    #                                    v_build_SF_unit, [SheetDelta("SF unit", 1)]),
    # "disband system force unit": Project("disband system force unit", {}, {"AP": 5, "WU": 1},
    #                                      [],
    #                                      v_disband_SF_unit, [SheetDelta("SF unit", -1),
    #                                                          SheetDelta("WU Progress", 1)]),
    #
    # "build fleet unit": Project("build fleet unit", {}, {"AP": 5, "WU": 1},
    #                             ["AP Budget", "WU Progress"],
    #                             # TODO add other fleet cost modifiers
    #                             v_build_fleet_unit, [SheetDelta("Fleet unit", 1)]),
    # "disband fleet unit": Project("build fleet unit", {}, {"AP": 5, "WU": 1},
    #                               [],
    #                               # TODO add other fleet cost modifiers
    #                               v_disband_fleet_unit, [SheetDelta("Fleet unit", -1),
    #                                                      SheetDelta("WU Progress", 1)]),
    #
    # "build system improvement": build_system_improvement,
    # "destroy system improvement": destroy_system_improvement,
}

need_manual_execution = [
    "custom",
    "explore",
    "build system force unit",
    "disband system force unit",
    "build fleet unit",
    "disband fleet unit",
    "build system improvement",
    "destroy system improvement",
]
