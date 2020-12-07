from __future__ import annotations
from typing import Dict, List, Set, Tuple, Union
import re


def main():
    graph = Parser.parse("07.in")
    unique_colors = graph.find_unique_containers("shiny gold")
    print(f"Part 1, unique colors: {unique_colors}")
    bag_count = graph.get_containing_bag_count("shiny gold")
    print(f"Part 2, bags inside: {bag_count}")


class Relationship:
    def __init__(self, node: Node, amount: int) -> None:
        self.node = node
        self.amount = amount


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.parents: List[Node] = []
        self.children: List[Relationship] = []
    
    def add_child(self, child: Node, amount: int) -> None:
        self.children.append(Relationship(child, amount))
        
    def add_parent(self, parent: Node) -> None:
        self.parents.append(parent)
        
        
class Graph:
    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        
    def add_relationship(self, container: str, children: List[Tuple[str, int]]):
        containerNode = self._get_or_create_node(container)
        
        # Add parent <-> child relationship
        for childName, childAmount in children:
            childNode = self._get_or_create_node(childName)
            containerNode.add_child(childNode, childAmount)
            childNode.add_parent(containerNode)
        
    def _get_or_create_node(self, name: str) -> Node:
        """Get an existing node with the specified name, or create one.
        The created one is also added to the node list

        Args:
            name (str): Name of the node

        Returns:
            Node: An existing node in the graph
        """
        if name in self._nodes:
            return self._nodes[name]
        else:
            node = Node(name)
            self._nodes[name] = node
            return node
        
    def find_unique_containers(self, bag: str) -> int:
        node = self._nodes[bag]
        parents = set()
        Graph._find_unique_containers(node, parents)
        return len(parents)
    
    @staticmethod
    def _find_unique_containers(child: Node, parents: set) -> None:
        for parent in child.parents:
            parents.add(parent.name)
            Graph._find_unique_containers(parent, parents)
            
    def get_containing_bag_count(self, bag: str) -> int:
        node = self._nodes[bag]
        return Graph._get_containing_bag_count(node) - 1
    
    @staticmethod
    def _get_containing_bag_count(bag: Node) -> int:
        total = 1
        for child in bag.children:
            total += child.amount * Graph._get_containing_bag_count(child.node)
        
        return total

class Parser:
    END = 'no other'
    LINE_REGEX = r"(?:(\d) )?(\w+ \w+) bag"
    
    @staticmethod
    def parse(filename: str) -> Graph:
        graph = Graph()
        
        with open(filename, "r") as file:
            for line in file.readlines():
                parent, children = Parser._parse_line(line)
                if len(children) > 0:
                    graph.add_relationship(parent, children)
        
        return graph
                
    @staticmethod
    def _parse_line(line: str) -> Tuple[str, List[Tuple[str, int]]]:
        parent = ""
        children: List[Tuple[str, int]] = []
        for match in re.finditer(Parser.LINE_REGEX, line):
            amount, name = match.groups()
            if parent == "":
                parent = name
            elif name != Parser.END:
                children.append((name, int(amount)))
        
        return (parent, children)
    
main()