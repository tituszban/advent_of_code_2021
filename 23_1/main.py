from __future__ import annotations


def pos_sign(n):
    if n < 0:
        return -1
    return 1


class Node:
    def __init__(self, occupant=None):
        self.neighbours = set()
        self.occupant = occupant

    def add_neighbour(self, other: Node):
        self.neighbours.add(other)
        other.neighbours.add(self)

    def _repr(self, name):
        return f"{name}({self.occupant or '.'}, {len(self.neighbours)})"

    def __repr__(self) -> str:
        return self._repr("Node")

    def clone(self):
        return self.__class__(self.occupant)

    def clone_with_new_occupant(self, occupant):
        return self.__class__(occupant)


class HallwayNode(Node):
    def __repr__(self) -> str:
        return self._repr("Hallway")


class EntranceNode(Node):
    def __repr__(self) -> str:
        return self._repr("Entrance")


class RoomNode(Node):
    def __init__(self, occupant, target_occupant):
        super().__init__(occupant)
        self.target_occupant = target_occupant

    def __repr__(self) -> str:
        return self._repr("Room")

    def clone(self):
        return self.__class__(self.occupant, self.target_occupant)

    def clone_with_new_occupant(self, occupant):
        return self.__class__(occupant, self.target_occupant)

    @property
    def room_occupants(self):
        other_room_occupants = [
            n.occupant for n in self.neighbours
            if isinstance(n, RoomNode)]
        occupants = [self.occupant, *other_room_occupants]
        return set([o for o in occupants if o])


class Corridor:
    def __init__(self, rooms: list[tuple[Node, Node]], hallway: list[Node]):
        self.rooms = rooms
        self.hallway = hallway

    def __repr__(self):
        rooms = list(map(lambda room: tuple(
            map(lambda r: r.occupant or ".", room)), self.rooms))
        rooms_T = list(zip(*rooms))
        hallways = list(map(lambda room: room.occupant or ".", self.hallway))

        return "{0}\n{1}\n{2}\n  {3}\n  {4}".format(
            "#" * 13,
            f"#{''.join(hallways)}#",
            f"###{'#'.join(rooms_T[0])}###",
            f"#{'#'.join(rooms_T[1])}#",
            "#" * 9
        )

    @property
    def all_nodes(self):
        return set([*self.hallway, *[r for room in self.rooms for r in room]])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def clone_with_move(self, move_from: Node, move_to: Node):
        assert move_from.occupant is not None and move_from in self.all_nodes
        assert move_to.occupant is None and move_to in self.all_nodes

        new_hallway: list[Node] = []
        for hallway in self.hallway:
            if hallway == move_from:
                h = hallway.clone_with_new_occupant(None)
            elif hallway == move_to:
                h = hallway.clone_with_new_occupant(move_from.occupant)
            else:
                h = hallway.clone()

            new_hallway.append(h)

        for h1, h2 in zip(new_hallway, new_hallway[1:]):
            h1.add_neighbour(h2)

        new_rooms = []
        for i, (r_t, r_b) in enumerate(self.rooms):
            new_room = []
            for room in [r_t, r_b]:
                if room == move_from:
                    r = room.clone_with_new_occupant(None)
                elif room == move_to:
                    r = room.clone_with_new_occupant(move_from.occupant)
                else:
                    r = room.clone()
                new_room.append(r)
            new_room[0].add_neighbour(new_hallway[2 + 2 * i])
            new_room[0].add_neighbour(new_room[1])
            new_rooms.append(tuple(new_room))

        return Corridor(new_rooms, new_hallway)

    def get_move_cost(self, dist, occupant):
        assert occupant is not None
        return {
            "A": 1,
            "B": 10,
            "C": 100,
            "D": 1000,
        }[occupant] * dist

    @property
    def is_done(self):
        return all(r.target_occupant == r.occupant for room in self.rooms for r in room)

    def is_path_blocked_home(self, node: Node):
        assert node.occupant
        if isinstance(node, RoomNode) and node.occupant == node.target_occupant:
            return []

        def find_path_home(_node: Node, target, visited=[]):
            for neighbour in _node.neighbours:
                if isinstance(neighbour, RoomNode) and neighbour.target_occupant == target:
                    return [neighbour]
                if neighbour in visited:
                    continue
                if any(path_home := find_path_home(neighbour, target, [*visited, _node])):
                    return [neighbour, *path_home]
            return []

        path_home = find_path_home(node, node.occupant)
        return [node.occupant for node in path_home if node.occupant]

    @property
    def heuristic(self):
        return sum(
            self.get_move_cost(2, h.occupant) for h in self.hallway if h.occupant) \
            + sum(
                self.get_move_cost(4, r.occupant)
            for room in self.rooms for r in room if r.target_occupant != r.occupant and r.occupant) \
            + sum(
                self.get_move_cost(2, blocking)
                for node in self.all_nodes if node.occupant
                for blocking in self.is_path_blocked_home(node)
        )

    def next_states(self):
        nodes_with_occupants = [
            node for node in self.all_nodes if node.occupant]

        def get_possible_moves_from(_node: Node, visited=[]):
            for neighbour in _node.neighbours:
                if not neighbour.occupant and neighbour not in visited:
                    yield (len(visited) + 1, neighbour)
                    yield from get_possible_moves_from(neighbour, [*visited, _node])

        for from_node in nodes_with_occupants:
            if isinstance(from_node, RoomNode) and from_node.occupant == from_node.target_occupant and len(from_node.neighbours) == 1:
                continue

            reachable_nodes = list(get_possible_moves_from(from_node))

            for dist, to_node in reachable_nodes:
                if isinstance(to_node, EntranceNode):
                    continue
                if isinstance(from_node, HallwayNode) and isinstance(to_node, HallwayNode):
                    continue
                if isinstance(to_node, RoomNode) and any(to_node.room_occupants) and from_node.occupant not in to_node.room_occupants:
                    continue
                if isinstance(to_node, RoomNode) and not any(to_node.room_occupants) and len(to_node.neighbours) > 1:
                    continue
                if isinstance(to_node, RoomNode) and to_node.target_occupant != from_node.occupant:
                    continue
                yield self.get_move_cost(dist, from_node.occupant), self.clone_with_move(from_node, to_node)

    @classmethod
    def from_rooms(cls, rooms):
        hallway_nodes = [None for _ in range(11)]
        room_nodes = []
        entries = []

        occupant_types = "ABCD"

        for i, room in enumerate(rooms):
            room_top = RoomNode(room[0], occupant_types[i])
            room_bottom = RoomNode(room[1], occupant_types[i])
            room_top.add_neighbour(room_bottom)
            entrance = EntranceNode()
            room_top.add_neighbour(entrance)
            entries.append(entrance)
            hallway_nodes[2 + i * 2] = entrance
            room_nodes.append((room_top, room_bottom))

        for i, (e1, e2) in enumerate(zip(entries, entries[1:])):
            hallway = HallwayNode()
            hallway.add_neighbour(e1)
            hallway.add_neighbour(e2)
            hallway_nodes[3 + i * 2] = hallway

        for i in [0, -1]:
            e = entries[i]
            hallway1 = HallwayNode()
            hallway2 = HallwayNode()

            hallway2.add_neighbour(hallway1)
            hallway2.add_neighbour(e)

            hallway_nodes[i] = hallway1
            hallway_nodes[i + pos_sign(i)] = hallway2

        return Corridor(room_nodes, hallway_nodes)


class LinkedListNode:
    def __init__(self, value, key, next_node):
        self.value = value
        self.next_node = next_node
        self.key = key


class SortedSet:
    def __init__(self, initial, sort_key):
        self.sort_key = sort_key
        s = sorted(initial, key=sort_key)

        head = None
        for v in reversed(s):
            head = LinkedListNode(v, sort_key(v), head)
        self.head = head

    def pop(self):
        if self.head is None:
            return None
        v = self.head.value
        self.head = self.head.next_node
        return v

    @property
    def any(self):
        return self.head is not None

    def insert(self, value):
        n = self.head
        key = self.sort_key(value)
        if self.head is None or key < self.head.key:
            self.head = LinkedListNode(value, key, self.head)
            return

        while n.next_node and key > n.next_node.key:
            n = n.next_node

        n.next_node = LinkedListNode(value, key, n.next_node)

    def to_gen(self):
        n = self.head
        while n:
            yield n.value
            n = n.next_node


def solve(test_input):
    rooms = list(zip(*map(
        lambda line: line.strip().strip("#").split("#"),
        test_input[2:4])))

    corridor = Corridor.from_rooms(rooms)

    to_explore = SortedSet(
        [(0, corridor, [(corridor, 0)])], lambda o: o[0] + o[1].heuristic)
    visited = set()

    min_heuristic = float('inf')

    while to_explore.any:
        score, state, history = to_explore.pop()
        if state in visited:
            continue

        visited.add(state)

        if state.heuristic < min_heuristic:
            print(state, score, state.heuristic)
            min_heuristic = state.heuristic

        if state.is_done:
            print("HISTORY ============================")
            for s, c in history:
                print(s, c, "\n")
            return score

        for cost, next_state in state.next_states():
            if next_state in visited:
                continue
            to_explore.insert(
                (score + cost, next_state, [*history, (next_state, cost)]))

    print(to_explore)


example_input = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".strip().split("\n")


def main():
    with open("23_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()
