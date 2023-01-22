class Plan:
    def __init__(self, name, parent, distance, heuristic):
        self.name = name
        self.parent = parent
        self.distance = parent.distance + distance if parent is not None else 0 + distance
        self.heuristic = heuristic

    def __str__(self):
        string = ""
        plan = self
        while plan is not None:
            string = f"{plan.name}" + string
            if plan.parent is not None:
                string = f" <- " + string
            plan = plan.parent
        string = f"({string}, g={self.distance}, h={self.heuristic})"
        return string

    def __lt__(self, other):
        return (self.distance + self.heuristic) < (other.distance + other.heuristic)

class PriorityQueue:
    def __init__(self):
        self.queue = []

    # Parent -> floor(node / 2)
    def bubble_up(self):
        index = len(self.queue) - 1
        while 0 < index:
            parent = ((index + 1) // 2) - 1
            if self.queue[index] < self.queue[parent]:
                self.swap(index,parent)
                index = parent
            else:
                break

    def bubble_down(self):
        index = 0
        while index < len(self.queue):
            child1 = ((index + 1) * 2) -1
            child2 = ((index + 1) * 2)
            if child1 < len(self.queue) and self.queue[child1] < self.queue[index]:
                self.swap(child1, index)
                index = child1
            elif child2 < len(self.queue) and self.queue[child2] < self.queue[index]:
                self.swap(child2, index)
                index = child2
            else:
                break

    def swap(self, index1, index2):
        hulp = self.queue[index1]
        self.queue[index1] = self.queue[index2]
        self.queue[index2] = hulp

    def print_queu(self):
        string = ""
        for item in self.queue:
            string += f"{item}"
            if item != self.queue[len(self.queue)-1]:
                string += ", "
        print(string)

    def add_plan(self, plan):
        self.queue.append(plan)
        self.bubble_up()

    def pop_plan(self):
        plan = self.queue[0]
        self.queue[0] = self.queue[len(self.queue) - 1]
        self.queue = self.queue[:-1]
        self.bubble_down()
        return plan


queue = PriorityQueue()

arad = Plan(name="Arad", distance=0, parent=None, heuristic=366)
zerind = Plan(name="Zerind", distance=75, parent=arad, heuristic=374)
timisoara = Plan(name="Timisoara", distance=140, parent=arad, heuristic=329)
sibiu = Plan(name="Sibiu", distance=118, parent=arad, heuristic=253)

queue.add_plan(plan=arad)
queue.pop_plan()
queue.add_plan(plan=zerind)
queue.add_plan(plan=timisoara)
queue.add_plan(plan=sibiu)
queue.print_queu()
print(queue.pop_plan())
oradea = Plan("Oradea", sibiu, 151, 380)
faragas = Plan("Faragas", sibiu, 99, 176)
rimieu = Plan("Rimmieu", sibiu, 80, 193)
arad = Plan("Arad", sibiu, 140, 366)
queue.add_plan(oradea);queue.add_plan(faragas);queue.add_plan(rimieu);queue.add_plan(arad)
queue.print_queu()
print(queue.pop_plan())

arad = Plan(name="Arad", distance=0, parent=None, heuristic=366)
arad = Plan(name="Arad", distance=0, parent=None, heuristic=366)
arad = Plan(name="Arad", distance=0, parent=None, heuristic=366)

