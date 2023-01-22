class Plan:
    def __init__(self, huidige_toestand, a, voorganger, kost):
        self.huidige_toestand = huidige_toestand
        self.a = a               # laatst_gekozen_actie = None
        self.ouder = voorganger  # ouder_plan = None
        self.g = kost            # totale kost plan

    def get_huidige_toestand(self):
        return self.huidige_toestand

    def get_a(self):
        return self.a

    def get_ouder(self):
        return self.ouder

    def get_kost(self):
        return self.g

    def get_successors(self, mogelijke_acties):
        lijst_successors = []
        for a in mogelijke_acties:
            if a != self.a:
                s = self.bereken_toestand(a)
                lijst_successors.append((s, a))

    def bereken_toestand(self, a):
        pass


class ZoekProbleem:
    def __init__(self, start_plan, doeltoestand, mogelijke_acties):
        self.start_toestand = start_plan
        self.doeltoestand = doeltoestand
        self.mogelijke_acties = mogelijke_acties

    def get_start_toestand(self):
        return self.start_toestand

    def doeltest(self, plan):
        return self.doeltoestand == plan

    def get_mogelijke_acties(self):
        return self.mogelijke_acties


def get_action_sequence(plan):
    action_sequence = []
    huidig_plan = plan
    while huidig_plan.get_ouder() is not None:
        action_sequence.insert(0, huidig_plan.get_a())
        huidig_plan = huidig_plan.get_ouder()
    return action_sequence

# boomgebaseerd zoeken
def tree_search(zoek_probleem):
    open_lijst = []
    open_lijst.append(zoek_probleem.get_start_toestand())
    while 0 < len(open_lijst):
        huidig_plan = open_lijst.pop(0)
        if zoek_probleem.doeltest(huidig_plan.get_huidige_toestand()) is True:
            return get_action_sequence(huidig_plan)
        else:
            for (s,a) in huidig_plan.get_successors(zoek_probleem.get_mogelijke_acties()):
                open_lijst.append(Plan(s, a, huidig_plan, huidig_plan.get_kost + 1))
    return "error: geen oplossing gevonden"

# graafgebaseerd zoeken
def graph_search(zoek_probleem):
    open_lijst = []
    gesloten_lijst = set
    open_lijst.append(zoek_probleem.get_start_toestand())
    while 0 < len(open_lijst):
        huidig_plan = open_lijst.pop(0)
        if zoek_probleem.doeltest(huidig_plan.get_huidige_toestand()) is True:
            return get_action_sequence(huidig_plan)
        else:
            if huidig_plan.get_huidige_toestand() not in gesloten_lijst:
                gesloten_lijst = huidig_plan.get_huidige_toestand() + gesloten_lijst # houd vorige toestanden bij
                for (s,a) in huidig_plan.get_successors(zoek_probleem.get_mogelijke_acties()):
                    open_lijst.append(Plan(s, a, huidig_plan, huidig_plan.get_kost + 1))
    return "error: geen oplossing gevonden"

# depthlimited search
def iterative_deepening(zoekprobleem):
    d = 0
    sol = depth_limited_search(zoekprobleem, d)
    while sol == "hit boundary":
        d += 1
        sol = depth_limited_search(zoekprobleem, d)
    return sol

def depth_limited_search(zoekprobleem, d):
    nieuw_plan = zoekprobleem.get_start_toestand()
    return dls_recursive(nieuw_plan, zoekprobleem, d)

def dls_recursive(plan, zoekprobleem, d):
    if zoekprobleem.doeltest(plan.get_huidige_toestand()):
        return get_action_sequence()
    if d == 0:
        return "hit boundary"

    boundary_hit = False
    for (s, a) in plan.get_successors(zoekprobleem.get_mogelijke_acties()):
        child = Plan(s, a, plan, plan.get_kost() + 1)
        sol = dls_recursive(child, zoekprobleem, d - 1)
        if sol == "hit boundary":
            boundary_hit = True
        else:
            if sol != "error: geen oplossing gevonden":
                return sol
    if boundary_hit is True:
        return "hit boundary"
    else:
        return "error: geen oplossing gevonden"