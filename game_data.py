"""CSC111 Project 1: Text Adventure Game Classes


Instructions (READ THIS FIRST!)
===============================


This Python module contains the main classes for Project 1, to be imported and used by
the `adventure` module.
Please consult the project handout for instructions and details.


Copyright and Usage Information
===============================


This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.


This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Item:
    """An item in our text adventure game world.
    This is an abstract class."""

    def get_info(self) -> str:
        """Print the main information of this item."""
        raise NotImplementedError


class Item1(Item):
    """An item in our text adventure game world.

    Instance Attributes:
        - name: Name of the item
        - start_position: Position on grid where item is initially found
        - target_position: Position on grid where item has to be deposited to get points
        - target_points: Points recieved for dropping item in current location
        - current_location: ???
        - point_scored: States whether the player scored the points

    Representation Invariants:
        - self.name != ''
        - self.start_position >= 0
        - self.start_position >= 0
        - self.start_position <= self.target_position
        - isinstance(self.point_scored, bool)
    """

    name: str
    start_position: int
    target_position: int
    target_points: int
    current_location: int
    point_scored: bool

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.current_location = start
        self.point_scored = False

    def get_info(self) -> str:
        return self.name


class Item2(Item):
    """An item in our text adventure game world.
    TODO: add more rep invariants and instance attributes

    Instance Attributes:
        - name: Name of the item
        - start_position: Position on grid where item is initially found
        - target_position: Position on grid where item has to be deposited to get points
        - target_points: Points recieved for dropping item in current location
        - current_location: Item's current location
        - point_scored: States whether the player scored the points
        - weight: Item's weight

    Representation Invariants:
        - self.name != ''
        - self.start_position >= 0
        - self.start_position >= 0
        - self.start_position <= self.target_position
        - isinstance(self.point_scored, bool)
    """

    name: str
    start_position: int
    target_position: int
    target_points: int
    current_location: int
    point_scored: int
    weight: float
    description: str

    def __init__(self, name: str, start: int, target: int, target_points: int, weight: float, description: str) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.current_location = start
        self.point_scored = False
        self.weight = weight
        self.description = description

    def get_info(self) -> str:
        return self.name + ", Weight: " + str(self.weight) + ", Description: " + self.description


class Location:
    """A location in our text adventure game world.


    Instance Attributes:
        - num: Number associated with the location
        - points: Points associated with player making it to the location
        - short: Brief description of the location
        - long: Long description of the location
        - map: Nested list respresentation of the whole map
        - items: Items available at the location
        - actions: Available actions at the location
        - visits: Number of visits to the location

    Representation Invariants:
        - self.points >= 0
        - len(self.long) >= len(self.short)
        - self.visits >= 0
    """

    num: int
    points: int
    short: str
    long: str
    map: list[list[int]]
    items: list[Item]
    actions: list[str]
    visits: int

    def __init__(self, num: str, points: str, short: str, long: str, a_map: list[list[int]], items: list[Item]) -> None:
        """Initialize a new location.


        """
        self.num = int(num[-2:])
        self.points = int(points)
        self.short = short
        self.long = long
        self.map = a_map
        self.items = self.get_items(items)
        self.actions = self.available_actions()
        self.visits = 0

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.
    def get_items(self, items: list) -> list:
        """
        Goes through all items and returns a list of the items available at the specific location
        """
        items_at_location = []
        for item in items:
            if item.current_location == self.num:
                items_at_location.append(item)
        return items_at_location

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        loc_x, loc_y = -1, -1
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == self.num:
                    loc_x = x
                    loc_y = y
        moves = []
        if loc_y >= 1 and self.map[loc_y - 1][loc_x] != -1:
            moves.append('N')
        if loc_y <= len(self.map) - 2 and self.map[loc_y + 1][loc_x] != -1:
            moves.append('S')
        if loc_x >= 1 and self.map[loc_y][loc_x - 1] != -1:
            moves.append('W')
        if loc_x <= len(self.map) - 2 and self.map[loc_y][loc_x + 1] != -1:
            moves.append('E')
        return moves


class Player:
    """
    A Player in the text adventure game.


    Instance Attributes:
        - x: X coordinate of location
        - y: Y coordinate of location
        - inventory: Items in player's inventory
        - victory: Boolean of whether the player has won the game or not
        - score: Player's score
        - previous_actions: Actions the player has already done
        - total_moves: Number of moves made by player
        - current_choice: String representation of what player chooses to do next

    Representation Invariants:
        - self.x >= 0
        - self.y >= 0
        - isinstance(victory, bool)
        - self.total_moves >= 0
    """

    x: int
    y: int
    inventory: list
    victory: bool
    score: int
    previous_actions: list
    total_moves: int
    current_choice: str
    weight: float

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.previous_actions = []
        self.total_moves = 0
        self.current_choice = ''
        self.weight = 0


class World:
    """A text adventure game world storing all location, item and map data.


    Instance Attributes:
        - map: A nested list representation of this world's map
        - items: Items available
        - location: All locations in the world

    Representation Invariants:
        - ???
    """

    map: list[list[int]]
    items: list[Item]
    location: list[Location]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.


        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.items = self.load_items(items_data)
        self.location = self.load_location(location_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:


        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].


        Return this list representation of the map.
        """
        map_raw = map_data.readlines()
        the_map = []
        for element in map_raw:
            cur_list = []
            raw_line = element.split()
            for i in raw_line:
                cur_list.append(int(i))
            the_map.append(cur_list)
        return the_map

    def load_location(self, location_data: TextIO) -> list[Location]:
        """
        Reads in locations.txt and returns a list of the locations available in the map where each element is of the
        Location class.
        """
        location_raw = location_data.readlines()
        the_location = [[] for _ in range(41)]
        cur_location = 0
        for i in range(len(location_raw)):
            location_raw[i] = location_raw[i][:-1]
            if location_raw[i] == 'END':
                cur_location += 1
            else:
                the_location[cur_location].append(location_raw[i])
        final_location = []
        for element in the_location:
            while len(element) > 4:
                element[-2] += ' ' + element[-1]
                element.pop()
            final_location.append(Location(element[0], element[1], element[2], element[3], self.map, self.items))
        return final_location

    def load_items(self, items_data: TextIO) -> list[Item]:
        """
        Reads in the items.txt file and returns a list of the items where each element is of the Item class.
        """
        items_raw = items_data.readlines()
        the_items = []
        for element in items_raw:
            item = element.split()
            # different Item child class depending on whether the item has weight and description associated with it
            if len(item) > 4:
                item[5] = ' '.join(item[5:])
                the_items.append(Item2(item[3], int(item[0]), int(item[1]), int(item[2]), float(item[4]), item[5]))
            else:
                the_items.append(Item1(item[3], int(item[0]), int(item[1]), int(item[2])))
        return the_items

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if self.map[y][x] == -1:
            return None
        else:
            return self.location[self.map[y][x]]

    if __name__ == '__main__':
        import doctest
        doctest.testmod(verbose=True)

        import python_ta
        python_ta.check_all('game_data.py', config={
            'max-line-length': 120,
        })
