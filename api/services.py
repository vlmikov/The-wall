from concurrent.futures import ThreadPoolExecutor
import concurrent
from .constants import max_height, cubic_ice_per_foot, price_per_cubic, workers_th, available_teams


class Section:
    max_height = max_height
    cubic_ice_per_foot = cubic_ice_per_foot
    price_per_cubic = price_per_cubic

    def __init__(self, section_height, day):
        self.section_height = section_height
        self.day = day
        self.ice_amount = 0
        self.cost = 0
        if self.section_height >= self.max_height:
            self.team = False
        else:
            self.team = True

    @property
    def section_height(self):
        """
        Get section height
        """
        return self._section_height

    @section_height.setter
    def section_height(self, new_height):
        """
        Set section height
        """
        if new_height > self.max_height or new_height < 0:
            raise ValueError(f'The height must be between 0 and {self.max_height}')
        else:
            self._section_height = new_height

    def increase_height(self):
        """
        Increase section height if section height is less than max_height
        Else release the team
        """
        if self.section_height < self.max_height:
            self.section_height += 1
            self.ice_amount += self.cubic_ice_per_foot
            self.cost += self.cubic_ice_per_foot * self.price_per_cubic
        elif self.section_height == self.max_height:
            self.team = False

    def calculate_ice_cost(self) -> tuple:
        """
        Calculate ice cost
        return : ice_amount, cost, team
        """
        if self.day is None:
            while self.team:
                self.increase_height()
        else:

            for _ in range(self.day):
                if self.team:
                    self.increase_height()

        return self.ice_amount, self.cost, self.team


class Wall:
    workers_th = workers_th
    available_teams = available_teams

    def __init__(self, input_data):
        self.input_data = input_data
        self.profiles = self.get_profiles()

    @property
    def input_data(self):
        """
        Get input data
        """
        return self._input_data

    @input_data.setter
    def input_data(self, input_data: str):
        """
        Set input data
        """
        if isinstance(input_data, str):
            self._input_data = input_data
        else:
            raise ValueError('Wrong input. Expects string')

    def get_profiles(self):
        """
        get all profiles from input data
        """
        # get profiles
        profiles = [list(map(int, x.split(' '))) for x in self.input_data.split('\n')]
        return profiles

    def create_section(self, *args) -> tuple:
        """
        Create section
        input data :
        args : tuple (height, day)
        return: tuple (ice_amount, cost)
        """
        height = list(args)[0][0]
        day = list(args)[0][1]
        if self.available_teams != 0:
            s = Section(height, day)
            self.available_teams -= 1
            ice_amount, cost, team_ = s.calculate_ice_cost()
            if not team_:
                self.available_teams += 1

            return ice_amount, cost
        return 0, 0

    def create_execute_pool(self, profiles: list) -> list:
        """
        create and execute Thread and return result of all sections
        input profiles : list
        return result : list
        """
        # Create a thread pool with a maximum of 3 worker threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers_th) as executor:
            # Submit each data item to the executor and store the Future object
            futures = [executor.submit(self.create_section, d) for d in profiles]
            # Retrieve the results from the completed threads
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results

    def wall_overview(self, day=None) -> tuple:
        """
        Wall overview accepts day and return tuple
        Calculate cost needed to complete all sections to size of wall_length : default 30
        input day
        return tuple => day, ice_amount, cost
        """
        # Prepare profiles shape for process
        profiles = [(height, day) for sublist in self.profiles for height in sublist]
        # Create a thread pool with a worker threads
        results = self.create_execute_pool(profiles)
        ice_amount = sum([x[0] for x in results])
        cost = sum([x[1] for x in results])
        return day, ice_amount, cost

    def get_profiles_day(self, profile_number: int, day: int):
        """
        get_profile_day accepts profile number and day and returns
        day, ice_amount for the input profile till the provided day.

        """
        indx_profile = profile_number - 1
        profile = self.profiles[indx_profile]
        profile = [(x, day) for x in profile]
        # Create a thread pool with a maximum of 3 worker threads
        results = self.create_execute_pool(profile)
        ice_amount = sum([x[0] for x in results])
        cost = sum([x[1] for x in results])
        return day, ice_amount, cost
