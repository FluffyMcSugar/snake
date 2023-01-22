from IPython.display import display, Markdown, Latex


class DataKnoop:
    def __init__(self, nummer, data=None, label=None):
        self.nummer = nummer
        self.data = data
        self.label = label


class AdjecentieKnoop:
    def __init__(self, data, volgende, gewicht=None):
        self.data = data
        self.gewicht = gewicht
        self.volgende = volgende

    def geef_nummer(self):
        return self.data.nummer

    def geef_data(self):
        return self.data.data

    def geef_label(self):
        return self.data.label


class LinkedList:
    def __init__(self):
        self.eerste = None

    def voeg_toe(self, data_knoop):
        hulp = self.eerste
        adjecentie_knoop = AdjecentieKnoop(data_knoop, hulp)
        self.eerste = adjecentie_knoop

    def zoek(self, nummer):
        ref = self.eerste
        while ref != None and ref.geef_nummer() != nummer:
            ref = ref.volgende
        return ref

    def _zoek_vorige(self, ref):
        vorige_ref = self.eerste
        while vorige_ref.volgende != ref:
            vorige_ref = vorige_ref.volgende
        return vorige_ref

    def verwijder(self, nummer):
        knoop = self.zoek(nummer)
        if knoop is None:
            return None
        vorige_knoop = self._zoek_vorige(knoop)
        vorige_knoop.volgende = knoop.volgende
        return (knoop.geef_nummer(),knoop.geef_data)

    def geef_lijst(self):
        lijst = []
        ref = self.eerste
        while ref is not None:
            lijst.append(ref)
            ref = ref.volgende
        return lijst


class Adjecentielijst:
    def __init__(self, aantal_knopen):
        self.N = aantal_knopen
        self.knopen = [None for i in range(self.N + 1)]
        self.adjecentielijst = [None for i in range(self.N + 1)]

    def voeg_toe_knoop(self, data_knoop):
        self.knopen[data_knoop.nummer] = data_knoop

    def voeg_toe(self, nummer, knoop):
        if self.adjecentielijst[nummer] is None:
            self.adjecentielijst[nummer] = LinkedList()
        self.adjecentielijst[nummer].voeg_toe(knoop)

    # output: array van adjecentieknopen
    def geef_buren_knoop(self, nummer_knoop):
        lijst = self.adjecentielijst[nummer_knoop]
        if lijst is not None:
            adjacent_array = lijst.geef_lijst()
            return adjacent_array
        return None

    def geef_knopen(self):
        return self.knopen

    def print_adjecentie_lijst(self):
        for i in range(1, len(self.adjecentielijst)):
            output = ""
            output += f"[{i}]"
            adjacent = self.geef_buren_knoop(i)
            if adjacent is not None:
                adjacent = reversed(adjacent)
                for j in adjacent:
                    output += f" --> {j.geef_nummer()}"
            print(output)

    def verwijder(self, nummer_adjecentielijst, nummer_knoop):
        lijst = self.adjecentielijst[nummer_adjecentielijst]
        if lijst is None:
            return None
        return lijst.verwijder(nummer_knoop)

    def generate_mermaid(self):
        output = "```mermaid\nflowchart LR\n"
        first_lines = ""
        last_lines = ""
        end = "```"
        array = [None for i in range(self.N + 1)]
        for i in range(1, len(self.adjecentielijst)):
            lijst = self.adjecentielijst[i]
            if lijst is not None:
                adjacent = lijst.geef_lijst()
                for j in adjacent:
                    if array[j.geef_nummer()] is None:
                        first_lines += f"\t{j.geef_nummer()}({j.geef_data()})\n"
                        array[j.geef_nummer()] = j.geef_nummer()
                    last_lines += f"\t{i} ---> {j.geef_nummer()}\n"
        return output + first_lines + last_lines + end

# knopen
a = DataKnoop(1, "a")
b = DataKnoop(2, "b")
c = DataKnoop(3, "c")
d = DataKnoop(4, "d")
e = DataKnoop(5, "e")
f = DataKnoop(6, "f")

alr = Adjecentielijst(6)

alr.voeg_toe_knoop(a)
alr.voeg_toe_knoop(b)
alr.voeg_toe_knoop(c)
alr.voeg_toe_knoop(d)
alr.voeg_toe_knoop(e)
alr.voeg_toe_knoop(f)

alr.voeg_toe(1, b); alr.voeg_toe(1, c)
alr.voeg_toe(2,a); alr.voeg_toe(2, d)
alr.voeg_toe(3, a); alr.voeg_toe(3, d); alr.voeg_toe(3, e)
# alr.voeg_toe(4, b);
alr.voeg_toe(4, c); alr.voeg_toe(4, e); alr.voeg_toe(4, f)
alr.voeg_toe(5, c); alr.voeg_toe(5, d); alr.voeg_toe(5, f)
alr.voeg_toe(6, d); alr.voeg_toe(6, e)

alr.print_adjecentie_lijst()

mermaid = alr.generate_mermaid()
display(Markdown(mermaid))

# Methode gebruikt als hulpmethode voor generiek zoeken (herhalende code)
def _mogelijke_bogen(gemarkeerde_knopen, mogelijke_bogen, graaf, knoop_nummer):
    buren_knoop = graaf.geef_buren_knoop(knoop_nummer)
    if buren_knoop is not None:
        for i in buren_knoop:
            if gemarkeerde_knopen[i.geef_nummer()] is False:
                mogelijke_bogen.append((knoop_nummer, i.geef_nummer()))

# Generiek zoeken
# Invoer Een gerichte of ongerichte graaf 𝐺 = (𝑉,𝐸) met orde 𝑛 > 0. Een knoop𝑠waarvan het zoeken vertrekt. De knopen zijn genummerd van 1 tot𝑛, i.e. 𝑉 = {1,2,...,𝑛}.
# Uitvoer Een array 𝐷 met 𝐷[𝑣] = true als en slechts als er een pad bestaat van 𝑠 naar 𝑣.
def zoek_generiek(graaf, start_knoop):
    # Maak array met n keer false (+ 1)
    gemarkeerde_knopen = [False for i in range (graaf.N+ 1)]
    # Markeer startknoop als True
    gemarkeerde_knopen[start_knoop.nummer] = True

    output_gemarkeerde_knopen = ["gemarkeerde knopen", "---"]
    output_mogelijke_bogen = ["mogelijke bogen", "---"]
    output_gekozen_boog = ["gekozen_boog", "---"]

    teller = 0
    vanuit_knoop = start_knoop.nummer

    # Setup -> mogelijke bogen array en genereer vanuit knoop 1
    mogelijke_bogen_array = []
    _mogelijke_bogen(gemarkeerde_knopen, mogelijke_bogen_array, graaf, start_knoop.nummer)
    print("\n"
          "===============\n"
          "GENERIEK ZOEKEN\n"
          "===============\n"
          f"start knoop: {vanuit_knoop}\n"
          f"start gemarkeerde knopen: {gemarkeerde_knopen}\n")

    # main loop -> blijft loopen zolang er
    # - False waarden zijn in gemarkeerde knopen
    # - Mogelijke bogen array > 0
    # Ook wordt telkens een volgende knoop en boog gekozen, hieruit worden nieuwe connecties bekeken.
    # Als mogelijke boog reeds als bezocht staat, neemt hij de volgende ...
    while False in gemarkeerde_knopen[1:] and 0 < len(mogelijke_bogen_array):
        print(f"Iteratie {teller + 1}")
        teller += 1
        gemarkeerde_knopen_voor_output = [i for i in range(1, len(gemarkeerde_knopen)) if gemarkeerde_knopen[i] is True]
        output_gemarkeerde_knopen.append(f"{gemarkeerde_knopen_voor_output}")
        print(f"mogelijke bogen + nieuwe bogen vanuit knoop {vanuit_knoop}: {mogelijke_bogen_array}")
        output_mogelijke_bogen.append(f"{mogelijke_bogen_array}")
        # code voor gekozen bogen
        volgende = mogelijke_bogen_array.pop(0)

        while gemarkeerde_knopen[volgende[1]] is True and 0 < len(mogelijke_bogen_array):
            volgende = mogelijke_bogen_array.pop(0)

        print(f"Kies tuple: {volgende}")
        output_gekozen_boog.append(f"{volgende}")

        if gemarkeerde_knopen[volgende[1]] is False:
            print(f"Knoop {volgende[1]} werd gemarkeerd")
            gemarkeerde_knopen[volgende[1]] = True
            print(f"Gemarkeerde knopen: {gemarkeerde_knopen}")
        print("")
        vanuit_knoop = volgende[1]
        # genereer nieuwe mogelijke bogen vanuit de nieuwe
        _mogelijke_bogen(gemarkeerde_knopen, mogelijke_bogen_array, graaf, volgende[1])
    print("=======================================================\n"
          "Einde GENERIEK ZOEKEN\n"
          "=====================\n"
          "comments: bij alr wordt hier een 1 indexering gebruikt,\n"
          "ermee dat boolean op index 0 steeds false zal geven\n"
          "=======================================================\n")

    gemarkeerde_knopen_voor_output = [i for i in
                                      range(1, len(gemarkeerde_knopen)) if
                                      gemarkeerde_knopen[i] is True]
    output_gemarkeerde_knopen.append(str(gemarkeerde_knopen_voor_output))
    output_mogelijke_bogen.append(f"geen in theorie (hier wel omdat we loop gestopt zijn bij vinden alle waarden)<br>{mogelijke_bogen_array}")
    output_gekozen_boog.append("geen")
    output_markdown = ""
    for (i,j,k) in zip(output_gemarkeerde_knopen, output_mogelijke_bogen, output_gekozen_boog):
        output_markdown += i + " | " + j + " | " + k + "\n"
    display(Markdown(output_markdown))
    return gemarkeerde_knopen

# Generiek zoeken under test
print("resultaat generiek zoeken:",zoek_generiek(alr, a))


# BFS
def breedte_eerst(graaf, start_knoop):
    gemarkeerde_knopen = [False for i in range(graaf.N + 1)]
    # start knoop markeren
    gemarkeerde_knopen[start_knoop.nummer] = True
    queue = []
    queue.append(start_knoop.nummer)
    teller = 0
    # code met output vooraan negeren
    output_iteratie = ["Iteratie", "---"]
    output_knoop = ["Gepopte knoop", "---", "/"]
    output_queue = ["Queue", "---"]
    output_gemarkeerde_knopen = ["D - Gemarkeerde knopen", "---"]
    output_iteratie.append(f"start toestand")
    output_queue.append(f"{queue}")
    output_gemarkeerde_knopen.append(f"{gemarkeerde_knopen[1:]}")
    output_mermaid = "```mermaid\nflowchart LR\n"

    # zolang er knopen in de queue zitten ...
    while 0 < len(queue):
        output_mermaid_loop = ""
        teller += 1
        knoop = queue.pop(0)
        output_knoop.append(f"{knoop}")
        buren_knoop = graaf.geef_buren_knoop(knoop)
        for i in buren_knoop:
            if gemarkeerde_knopen[i.geef_nummer()] is False:
                gemarkeerde_knopen[i.geef_nummer()] = True
                queue.append(i.geef_nummer())
                output_mermaid_loop += f"\t{knoop} --> {i.geef_nummer()}\n"
        output_iteratie.append(f"{teller}")
        output_queue.append(f"{queue}")
        output_gemarkeerde_knopen.append(f"{gemarkeerde_knopen[1:]}")
        output_mermaid += f"{output_mermaid_loop}\n"

    # markdown output
    output_markdown = ""
    output_mermaid += "```"
    for (i, j, k, l) in zip(output_iteratie, output_knoop, output_queue,
                         output_gemarkeerde_knopen):
        output_markdown += i + " | " + j + " | " + k + " | " + l + "\n"
    display(Markdown(output_markdown))
    display(Markdown(output_mermaid))

    return gemarkeerde_knopen

breedte_eerst(alr, a)

# DFS
def diepte_eerst_zoeken(graaf, start_knoop):
    output_list = []
    mermaid_list = ["```mermaid","flowchart LR"]
    gemarkeerde_knopen = [False for i in range(graaf.N + 1)]
    diepte_eerst_recursief(graaf, start_knoop.nummer, gemarkeerde_knopen, output_list, mermaid_list)
    output_list.append(f"einde {gemarkeerde_knopen[1:]}")
    mermaid_list.append("```")
    mermaid_output = ""
    for i in mermaid_list:
        mermaid_output += i + "\n"
    display(Markdown(mermaid_output))
    output = ""
    for i in output_list:
        output += i + "\n"
    print(output)
    return gemarkeerde_knopen

def diepte_eerst_recursief(graaf, knoop, gemarkeerde_knopen, output, mermaid):
    iteration = 0
    output.append(f"G, {knoop}, {gemarkeerde_knopen[1:]}")
    gemarkeerde_knopen[knoop] = True
    buren_knoop = graaf.geef_buren_knoop(knoop)
    local_mermaid = f"\t{knoop}"
    for i in buren_knoop:
        nummer_i = i.geef_nummer()
        if gemarkeerde_knopen[nummer_i] is False:
            iteration += 1
            mermaid.append(local_mermaid + f" --\"#{iteration}\"--> {nummer_i}")
            diepte_eerst_recursief(graaf, nummer_i, gemarkeerde_knopen, output, mermaid)

print(diepte_eerst_zoeken(alr, a))


# Topologisch sorteren
def sorteer_topologisch(graaf):
    global cycle_detected
    cycle_detected = False
    lijst_d = [0 for i in range(graaf.N + 1)]
    lijst_s = []
    flowchart = []; flowchart.append("```mermaid"); flowchart.append("flowchart LR")
    for knoop in range(1, graaf.N):
        if lijst_d[knoop] == 0:
            dfs_topo(graaf, knoop, lijst_d, lijst_s, flowchart)
            if cycle_detected is True:
                return False
    flowchart.append("```")
    flowchart_ouput = ""
    for i in flowchart:
        flowchart_ouput += i + "\n"
    display(Markdown(flowchart_ouput))
    return lijst_s


def dfs_topo(graaf, knoop_nummer, lijst_d, lijst_s,flowchart):
    global cycle_detected
    lijst_d[knoop_nummer] = 1
    flowchart_local = f"\t{knoop_nummer}"
    if graaf.geef_buren_knoop(knoop_nummer) is not None:
        for w in graaf.geef_buren_knoop(knoop_nummer):
            if lijst_d[w.geef_nummer()] == 0 and cycle_detected is False:
                dfs_topo(graaf, w.geef_nummer(), lijst_d, lijst_s, flowchart)
                flowchart.append(flowchart_local + f" ---> {w.geef_nummer()}")
            elif lijst_d[w.geef_nummer()] == 1:
                cycle_detected = True
    lijst_d[knoop_nummer] = 2
    lijst_s.insert(0, knoop_nummer)

graaf_topologisch = Adjecentielijst(4)
a = DataKnoop(1, "a")
b = DataKnoop(2, "b")
c = DataKnoop(3, "c")
d = DataKnoop(4, "d")

graaf_topologisch.voeg_toe_knoop(a)
graaf_topologisch.voeg_toe_knoop(b)
graaf_topologisch.voeg_toe_knoop(c)
graaf_topologisch.voeg_toe_knoop(d)

graaf_topologisch.voeg_toe(1, b); graaf_topologisch.voeg_toe(1, c)
graaf_topologisch.voeg_toe(2,d)
graaf_topologisch.voeg_toe(3,d)


print(sorteer_topologisch(graaf_topologisch))
