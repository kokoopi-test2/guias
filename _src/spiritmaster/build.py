"""Builds the Spiritmaster guide page from the extracted sheet (sheet.json + img/) into the guides repo."""
import html
import re
import json
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\proyectos\guias-kokoop\spiritmaster"
SRC = "https://docs.google.com/spreadsheets/d/1gRJHIrQDmWrcQfCMZqhjQdDhxAON5_HpqiOcaE0KxVo/edit"
import sys
sys.path.insert(0, HERE)
from explain import INTRO, BOX  # noqa: E402
S = {s["sheet"]: s for s in json.load(open(os.path.join(HERE, "sheet.json"), encoding="utf-8"))}
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
e = html.escape


def img(name, cap="", cls="shot", big=1600):
    """WebP copy of an extracted image (max `big` px wide), as a figure that opens full size on tap."""
    src = os.path.join(HERE, "img", name)
    dst = name.rsplit(".", 1)[0] + ".webp"
    p = Image.open(src)
    if p.mode not in ("RGB", "RGBA"):
        p = p.convert("RGBA")
    if p.width > big:
        p = p.resize((big, round(p.height * big / p.width)), Image.LANCZOS)
    p.save(os.path.join(OUT, "img", dst), "WEBP", quality=86, method=6)
    w, h = p.size
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return (f'<figure class="{cls}"><a href="img/{dst}" class="zoom"><img src="img/{dst}" width="{w}" height="{h}" '
            f'loading="lazy" alt="{e(strip(cap)) or "captura"}"></a>{c}</figure>')


def strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s or "")


def table(head, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in head)
    lab = [re.sub(r"<[^>]+>", "", h) for h in head]  # each cell knows its column: on a phone a row becomes a card
    tr = "".join("<tr>" + "".join(f'<td data-l="{e(lab[k])}">{c}</td>' for k, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tw {cls}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def cells(sheet):
    g = {}
    for c in S[sheet]["cells"]:
        g.setdefault(c["r"], {})[c["c"]] = c
    return g


def v(c):
    x = c["v"] if c else ""
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x)


def grid_rows(sheet, r0, r1, ncol, fix=lambda s: s, first=None):
    g = cells(sheet)
    out = []
    for r in range(r0, r1 + 1):
        if r not in g:
            continue
        row = [fix(v(g[r].get(k))) for k in range(1, ncol + 1)]
        if first:
            row[0] = first(row[0])
        out.append([e(x) for x in row])
    return out


TYPO = {"Damage Toleraance": "Damage Tolerance", "Criticaal Damage Tolerance": "Critical Damage Tolerance",
        "Critical Damabe Boost": "Critical Damage Boost", "Weapon Damage boost": "Weapon Damage Boost",
        "Damage boost": "Damage Boost", "Attack increase": "Attack Increase", "Combat speed": "Combat Speed",
        "Move speed": "Move Speed", "Critical hit": "Critical Hit", "Damage Tolerance(3%)": "Damage Tolerance (3%)",
        "PvE Damage Tolerance(4%)": "PvE Damage Tolerance (4%)", "Weapon Damage Tolerance(3%)": "Weapon Damage Tolerance (3%)",
        "Skill (optional)": "Skill (opcional)"}


def fix(s):
    for a, b in TYPO.items():
        s = s.replace(a, b)
    return s.replace("(skill)", "(skill)")


def slot(s):
    return {"6 (Philosopher)": "6 · con Philosopher's Stone", "7 (Red item)": "7 · solo en objeto rojo",
            "5 (Philosopher)": "5 · con Philosopher's Stone", "6 (Red item)": "6 · solo en objeto rojo"}.get(s, s)


sections = []


def section(id_, title, sub, body, tag=""):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    box = f'<div class="box"><span>Qué es y para qué te sirve</span>{BOX[id_]}</div>' if id_ in BOX else ""
    sections.append((id_, title, f'<section id="{id_}"><h2>{t}{title}</h2>' + (f'<p class="lead">{sub}</p>' if sub else "") + box + body + "</section>"))


# ---------------------------------------------------------------- 1. links
L = []
def link(name, url, label=None, note=""):
    n = f'<p class="note">{note}</p>' if note else ""
    return f'<div class="lk"><div><b>{name}</b>{n}</div><a class="btn" href="{e(url)}" target="_blank" rel="noopener">{label or "Abrir"}</a></div>'

body = ('<h3>Webs y herramientas</h3><div class="links">'
        + link("Quest Log TW · build inicial (extend start build)", "https://questlog.gg/aion-2/en/character-builder/TheGhostTeamAndLuckOfFrost", "questlog.gg")
        + link("Buscar personajes de TW y KR", "https://shugo.gg/", "shugo.gg")
        + link("Base de personajes de TW con rankings", "https://aion2.bnshive.com/ranking/abyss", "Aion2 BnsHive")
        + link("Medidor de DPS con muchísimas funciones", "https://notmeter.com/", "NotMeter",
               "En la beta funcionaba, pero tiene problemas para mostrar personajes con el nick en cirílico.")
        + link("Otra web con estadísticas PvE y medidor de DPS", "https://aion.ing/aion2/stats.php", "aion.ing",
               "En TW empezó a ir mal; en Global seguramente su medidor de DPS no funcione.")
        + link("Otro medidor de DPS, lo están adaptando a Global", "https://aion2t.com/dps-meter", "aion2t.com",
               "También tiene bugs, sobre todo con el Spiritmaster: puede partir al personaje en 2 líneas y el DPS total sale raro.")
        + '</div><h3>Global</h3><div class="links">'
        + link("Build para subir de nivel (Leveling SM)", "https://questlog.gg/aion-2/en/character-builder/TheParalyzingBurnOfSpring", "questlog.gg",
               "Se actualizará cuando salga Global.")
        + link("Build de prueba para Global (en proceso)", "https://questlog.gg/aion-2/en/character-builder/BloodyGlovesJumpOrigin", "questlog.gg",
               "Teoría para Global, todavía en proceso.")
        + link("Personaje de referencia en shugo.gg (WinSwin, servidor 1305, Global)",
               "https://shugo.gg/character?id=GXf_uDNlKcYJYIHNvVUVBQWGY85op-37E6MEnLiQKGE%3D&server=1305&region=GLOBAL&name=WinSwin",
               "Shugo Link",
               "Se salta por completo las mazmorras T1. Eso sí, necesita los Daevanion Crystal de PvP que da el monolito del Abismo (nivel 16).")
        + "</div>" + img("s00_000.png", "La captura que acompaña a la build: personaje en el mundo con el inventario abierto."))
section("enlaces", "Enlaces", "Todo lo que la hoja original enlaza, con lo que dice de cada web.", body)

# ---------------------------------------------------------------- 2. Global
ins_head = ["Casilla", "Cogni Insight", "Fera Insight", "Natura Insight", "Varian Insight", "Special Insight"]
gear_head = ["Línea", "Weapon", "Guard", "Helm", "Pauldrons", "Breastplate", "Greaves", "Gloves", "Cloak", "Boots"]
acc_head = ["Línea", "Earrings 1", "Earrings 2", "Necklace", "Ring 1", "Ring 2", "Bracelet 1", "Bracelet 2"]
body = ('<p>Qué estadística poner en cada casilla según el tipo de Insight.</p><div class="grid2">'
        + '<div><h3>Pet Insight (Genus Insight) · PvE</h3>' + table(ins_head, grid_rows("Global", 3, 11, 6, fix), "ins") + '</div>'
        + '<div><h3>Pet Insight (Genus Insight) · PvP</h3>' + table(ins_head, grid_rows("Global", 16, 24, 6, fix), "ins") + '</div></div>'
        + '<h3>Estadísticas del equipo · tabla 1 (daño: para PvE)</h3><p>Qué estadística buscar en cada línea de cada pieza. La línea marcada «Philosopher\'s Stone» solo sale usando esa piedra en la pieza, y la marcada «objeto rojo», solo en piezas rojas. La hoja no titula estas tablas: por sus estadísticas, la primera es de daño (PvE) y la segunda de resistencias (PvP).</p>'
        + table(gear_head, grid_rows("Global", 34, 40, 10, fix, slot), "wide")
        + '<h3>Accesorios · tabla 1 (PvE)</h3><p class="note">Ojo: Focused Eye, Hunter\'s Resolve y Concentrated Fire son habilidades de Ranger. La hoja original las pone así en esta tabla; si juegas Spiritmaster, en esas líneas busca tus habilidades.</p>'
        + table(acc_head, grid_rows("Global", 43, 49, 8, fix, slot), "wide")
        + '<h3>Estadísticas del equipo · tabla 2 (resistencias: para PvP)</h3>'
        + table(gear_head, grid_rows("Global", 54, 59, 10, fix, slot), "wide")
        + '<h3>Accesorios · tabla 2 (PvP)</h3>'
        + table(acc_head, grid_rows("Global", 62, 67, 8, fix, slot), "wide")
        + '<p class="note">En los brazaletes, cada estadística lleva el nombre de un dios: Justice [Nezekan], Freedom [Vaizel], Time [Siel], '
          'Destruction [Zikel], Life [Yustiel], Illusion [Kaisinel], como se ve en el tooltip del brazalete de la sección de equipo PvP.</p>'
        + '<h3>Prioridad para subir las estigmas</h3><ol class="steps">'
          '<li><b>Al nivel 45</b>Summon: Ancient Spirit (el «gólem»), Enhance: Spirit\'s Benediction y Jointstrike: Corrode a nivel 5; Jointstrike: Destructive Attack a nivel 7.</li>'
          '<li><b>Después</b>Sube Jointstrike: Destructive Attack hasta nivel 10.</li>'
          '<li><b>Según vayas comprando estigmas</b>Summon: Ancient Spirit hasta nivel 15, Enhance: Spirit\'s Benediction a nivel 10 y Jointstrike: Destructive Attack hasta nivel 15.</li>'
          '<li><b>Siguiente etapa</b>Summon: Ancient Spirit a nivel 20 y Jointstrike: Destructive Attack a nivel 20. Solo después, Enhance: Spirit\'s Benediction a nivel 20: su nivel 15 no da nada de ataque.</li>'
          '<li><b>Lo último</b>Jointstrike: Corrode del nivel 5 al 20.</li></ol>')
section("global", "Global", "Insight de la mascota, estadísticas de cada pieza y el orden para subir las estigmas.", body, "GLOBAL")

sections.append(("tw", "Datos de TW", '<div class="divider"><b>A partir de aquí, datos de TW (Taiwán)</b><span>La hoja original avisa: en parte van perdiendo actualidad respecto a Global.</span></div>'))

# ---------------------------------------------------------------- 3. skills
SK = ["Cold Shock", "Combustion", "Summon: Fire Spirit", "Summon: Water Spirit", "Jointstrike: Curse", "Rapid Scattershot",
      "Summon: Earth Spirit", "Dimensional Control", "Summon: Wind Spirit", "Soul's Cry", "Elemental Fusion", "Defiance",
      "Spirit Strike", "Spirit Protection", "Spirit's Descent", "Corrode", "Spirit Revitalization", "Mental Focus",
      "Consecutive Countercurrent", "Spirit Communion", "Revitalization Contract", "Element Unification"]
g = cells("Skills, Manastones, etc")


def tri(s):
    """The sheet's level and Specialty notes in Spanish («Триподы» are the Specialty picks inside a skill)."""
    import re
    s = s.strip()
    if s.lower() == "don't use":
        return "No se usa"
    s = re.sub(r"На 20 лвл,?", "a nivel 20:", s)
    s = re.sub(r"если (\d+) LVL\.?", r"si es nivel \g<1>:", s)
    s = re.sub(r"LVL \+- ?(\d+)", r"nivel ±\g<1>", s)
    s = re.sub(r"LVL (\d+(?:-\d+)?\+?)", r"nivel \g<1>", s)
    s = re.sub(r"(\d+\+?) LVL\.?", r"nivel \g<1> ·", s)
    s = re.sub(r"[Тт]риподы:?", "Specialty", s)
    s = s.replace("для масс пвп", "para PvP masivo:").replace(" или ", " o ")
    s = re.sub(r"·\s*,", "·", s)
    parts = [x.strip(" ., ") for x in s.split(" / ")]
    parts = [x[0].upper() + x[1:] if x else x for x in parts]
    return "<br>".join(e(x) for x in parts)


rows = []
for i, name in enumerate(SK):
    r = i + 2
    ic = img(f"s03_{i:03d}.png", "", "icon")
    kind = "Activa" if i < 12 else "Pasiva"
    rows.append([ic, f"<b>{name}</b> <small>+1</small><br><span class='k'>{kind}</span>", tri(v(g[r].get(3))), tri(v(g[r].get(4)))])
legend = {2: "Estigmas PvE principales", 3: "Estigmas PvE adicionales", 5: "Estigmas PvP principales", 6: "Estigmas PvP adicionales"}
groups = {}
for im in S["Skills, Manastones, etc"]["images"][22:]:
    groups.setdefault(im["r"], []).append(im["file"][4:])
leg = ""
for r, title in legend.items():
    leg += f'<div class="leg"><b>{title}</b><div class="icons">' + "".join(img(f, "", "icon") for f in groups.get(r, [])) + "</div></div>"
mana = (f'<div class="leg"><b>Manastones PvE · tiers de estadísticas</b><div class="icons">' + "".join(img(f, "", "icon") for f in groups.get(8, [])) + "</div>"
        '<ul class="tiers"><li><i>S</i>Damage Boost · Attack · Accuracy · Front Attack Damage Boost</li>'
        '<li><i>A</i>Critical Damage Boost · Weapon Damage Boost · Front Attack</li>'
        '<li><i>B</i>Lo que quede que se pueda aprovechar; Critical Hit solo para muy poco tiempo</li></ul></div>'
        f'<div class="leg"><b>Manastones PvP · tiers de estadísticas</b><div class="icons">' + "".join(img(f, "", "icon") for f in groups.get(13, [])) + "</div>"
        '<ul class="tiers"><li><i>S</i>PvP Damage Boost · PvP Accuracy · Accuracy</li><li><i>A</i>PvP Attack · Attack</li></ul></div>')
body = ('<p>«Specialty» son las mejoras que eliges dentro de cada habilidad: los números dicen cuáles marcar. «Nivel» es el nivel al que subir la habilidad. El «+1» junto al nombre es como sale en el equipo, que sube esa habilidad +1 de nivel.</p>'
        + table(["", "Habilidad", "PvE · nivel y Specialty", "PvP · nivel y Specialty"], rows, "skills")
        + '<h3>Qué estigmas llevar</h3><div class="legs">' + leg + "</div><h3>Manastones</h3><div class='legs'>" + mana + "</div>")
section("habilidades", "Habilidades, estigmas y manastones", "Cada habilidad del Spiritmaster con su nivel y sus Specialty para PvE y para PvP.", body, "TW")

# ---------------------------------------------------------------- 4. red PvP gear
PVP = ["Guard", "Helm", "Pauldrons", "Breastplate", "Greaves", "Gloves", "Cloak", "Boots", "Earrings", "Earrings",
       "Necklace", "Ring", "Ring", "Bracelet", "Brooch"]
NAMEP = ["+20 Archon High Commander"] * 13 + ["+20 Faded Shadow Bracelet", "+15 Kaldrix Brooch"]
body = '<p class="warn">Estos objetos son de TW y todavía no existen en Global: el nombre es el que sale en la captura.</p>' + '<div class="gear">' + "".join(
    img(f"s04_{i:03d}.png", f"<b>{PVP[i]}</b>{NAMEP[i] if i > 12 else NAMEP[i] + ' ' + PVP[i]}", "tip") for i in range(15)) + "</div>"
section("pvp", "Equipo rojo PvP", "El set completo, pieza a pieza, con sus estadísticas, habilidades y manastones. Toca una pieza para verla en grande.", body, "TW")

# ---------------------------------------------------------------- 5. red PvE gear
PVE = [("Helm", "+20 Splendent Nemesis Dragon"), ("Pauldrons", "+20 Splendent Horned Dragon Lord"), ("Top", "+20 Splendent Nemesis Dragon"),
       ("Legs", "+20 Splendent Nemesis Dragon"), ("Gloves", "+20 Splendent Nemesis Dragon"), ("Cloak", "+20 Splendent Nemesis Dragon"),
       ("Shoes", "+20 Horned Dragon Lord Boots"), ("Earrings", "+20 Horned Dragon Lord Earrings"), ("Earrings", "+20 Horned Dragon Lord Earrings"),
       ("Necklace", "+20 Horned Dragon Lord Necklace"), ("Ring", "+20 Horned Dragon Lord Ring"), ("Ring", "+20 Splendent Horned Dragon Lord Ring")]
info = ('<div class="info"><h3>Notas de la hoja</h3>'
        '<p>Cambia Corrode por <b>Element Unification</b>.</p>'
        '<p>Si la pieza no es roja, sáltate Critical Hit y con la Philosopher\'s Stone consigue <b>Spirit Revitalization</b> (o al revés, lo que te salga antes).</p>'
        '<p><b>Estadísticas que SÍ o SÍ tienen que estar en el equipo:</b></p>'
        '<ul class="chips"><li>Attack Increase</li><li>Smite</li><li>Perfect Chance</li><li>Combat Speed <small>(la hoja pone «Attack Speed»)</small></li><li>Move Speed</li>'
        '<li>Damage Boost</li><li>Critical Damage Boost</li><li>Attack</li></ul>'
        '<p>En las piezas rojas donde ya tengas Spirit Strike, Mental Focus y las 2 habilidades de arriba, la casilla que queda puedes rematarla con Mental Focus.</p>'
        '<p><b>Spirit Strike y Mental Focus tienen que estar siempre.</b></p>'
        '<p><b>Prioridad en los manastones de nivel alto:</b></p>'
        '<ol class="prio"><li>Damage Boost</li><li>Front Attack Damage Boost</li><li>Attack</li><li>Accuracy</li><li>Critical Damage Boost</li>'
        '<li>Weapon Damage Boost</li><li>Front Attack</li><li>Critical Hit</li></ol>'
        '<p>Lo ideal: 2 estadísticas amarillas de las 4 primeras.</p></div>')
body = '<p class="warn">Estos objetos son de TW y todavía no existen en Global: el nombre es el que sale en la captura.</p>' + info + '<div class="gear">' + "".join(img(f"s05_{i:03d}.png", f"<b>{s}</b>{n}", "tip") for i, (s, n) in enumerate(PVE)) + "</div>"
section("pve", "Equipo rojo PvE", "El set PvE pieza a pieza y qué estadísticas tiene que llevar.", body, "TW")

# ---------------------------------------------------------------- 6. DPS meter
def fig(i, cap):
    return img(f"s06_{i:03d}.png", cap, "shot")
body = ('<p>Todas las mediciones son contra el muñeco de entrenamiento (Melee Training Scarecrow) con la ventana Combat Analysis del juego. '
        '«Con el personaje» es tu daño total con el espíritu mientras tú también atacas (3 minutos); «solo el espíritu» es él sin ti (1 minuto).</p>'
        + table(["Prueba", "Tiempo", "Daño total", "Qué te dice"], [
            ["Solo el espíritu: Earth / Fire / Water / Wind", "1:00", "11,44M / 11,01M / 8,96M / 7,05M", "Earth y Fire son los que más pegan solos; Wind, el que menos"],
            ["Con el personaje: Fire / Earth / Water / Wind", "3:00", "90,48M / 87,28M / 87,08M / 77,07M", "Con Fire sacas más daño total; con Wind, menos"],
            ["Ancient Spirit + Fire Spirit", "3:02", "152,59M", "Los dos juntos rinden mucho más: 152M frente a unos 90M con uno solo"],
            ["Con todas las habilidades", "3:01", "230,32M (1,26M de DPS)", "La referencia de la rotación completa"],
            ["Combo 1 / Combo 2", "3:30 / 3:26", "259,58M / 257,14M", "Los dos combos rinden casi igual"],
            ["De frente / por detrás / de lado", "2:44", "290,37M / 291,96M / 285,68M", "En estas pruebas, la posición apenas cambia el daño"],
            ["Semana anterior → 02/09 → 04/09", "2:44-2:45", "346,11M → 372,35M → 388,96M", "De una semana a otra, el daño fue subiendo"],
            ["Antes del parche del 08/09", "2:44", "410,13M (2,49M de DPS)", "La medición más alta de la hoja"]], "sum")
        + '<div class="cards">'
        + f'<div class="card"><h4>Water Spirit</h4>{fig(5, "Con el personaje · 3 min · 87,08M")}{fig(1, "Solo el espíritu · 1 min · 8,96M")}</div>'
        + f'<div class="card"><h4>Fire Spirit</h4>{fig(6, "Con el personaje · 3 min · 90,48M")}{fig(3, "Solo el espíritu · 1 min · 11,01M")}</div>'
        + f'<div class="card"><h4>Earth Spirit</h4>{fig(7, "Con el personaje · 3 min · 87,28M")}{fig(2, "Solo el espíritu · 1 min · 11,44M")}</div>'
        + f'<div class="card"><h4>Wind Spirit</h4>{fig(4, "Con el personaje · 3 min · 77,07M")}{fig(0, "Solo el espíritu · 1 min · 7,05M")}</div>'
        + f'<div class="card"><h4>Ancient Spirit + Fire Spirit</h4>{fig(9, "3 min · 152,59M")}</div>'
        + f'<div class="card"><h4>Con todas las habilidades</h4>{fig(10, "3 min · 230,32M (1,26M de DPS)")}</div>'
        + f'<div class="card"><h4>Habilidades en la macro (medición)</h4>{fig(8, "Las habilidades que van en la macro, en este orden")}</div>'
        + f'<div class="card"><h4>Combo 1 · macro T → clic derecho → E</h4>{fig(15, "Barra de habilidades del combo 1")}{fig(13, "Resultado · 3:30 · 259,58M")}</div>'
        + f'<div class="card"><h4>Combo 2 · macro T → clic derecho</h4>{fig(16, "Barra de habilidades del combo 2")}{fig(14, "Resultado · 3:26 · 257,14M")}</div>'
        + f'<div class="card wide2"><h4>Rotación</h4>{fig(12, "Desglose por habilidad de la rotación")}{fig(11, "Final del desglose: el resto de habilidades")}</div>'
        + f'<div class="card"><h4>Tras la actualización del 26 de agosto</h4>{fig(17, "1:06 · 115,07M · 1,74M de DPS")}</div>'
        + f'<div class="card"><h4>De frente</h4>{fig(18, "2:44 · 290,37M")}{fig(21, "Otra medición de frente · 2:45 · 307,19M")}</div>'
        + f'<div class="card"><h4>Por detrás</h4>{fig(19, "2:44 · 291,96M")}</div>'
        + f'<div class="card"><h4>De lado</h4>{fig(20, "2:44 · 285,68M")}</div>'
        + f'<div class="card"><h4>Semana anterior (ping 130)</h4>{fig(22, "2:45 · 346,11M")}</div>'
        + f'<div class="card"><h4>Esta semana, 02/09 (ping 130)</h4>{fig(23, "2:44 · 372,35M")}</div>'
        + f'<div class="card"><h4>Esta semana, 04/09, tras un mantenimiento corto</h4>{fig(25, "2:44 · 388,96M")}{fig(24, "Barra de habilidades usada en estas mediciones")}</div>'
        + f'<div class="card"><h4>Antes del parche del 08/09</h4>{fig(26, "2:44 · 410,13M · 2,49M de DPS")}</div>'
        + '</div>')
section("dps", "Medidor de DPS", "Mediciones del daño del Spiritmaster: cada espíritu, combos, rotación y su evolución con los parches.", body, "TW")

# ---------------------------------------------------------------- 7. spirits attack speed
body = ('<div class="pairs">'
        + img("s07_000.png", "<b>Earth Spirit</b>228.617 de DPS · 4,69M en 20 s · 42 golpes de ataque básico", "shot")
        + img("s07_001.png", "<b>Wind Spirit</b>127.413 de DPS · 2,62M en 20 s · 33 golpes de ataque básico", "shot")
        + img("s07_002.png", "<b>Water Spirit</b>227.487 de DPS · 4,63M en 20 s · 25 golpes de ataque básico", "shot")
        + img("s07_003.png", "<b>Fire Spirit</b>254.909 de DPS · 5,22M en 20 s · 47 golpes de ataque básico", "shot") + "</div>")
section("espiritus", "Velocidad de ataque de los espíritus", "Qué espíritu pega más rápido y más fuerte.", body, "TW")

# ---------------------------------------------------------------- 8. field bosses
EL = [("Western Cantas Valley", "Kernon of the West", "1 h", "30 min"), ("Eastern Cantas Valley", "Neikel of the East", "1 h", "30 min"),
      ("Ellun River Marsh", "Rotten Kutar", "1 h", "30 min"), ("Ellun River Midstream", "Blooming Korin", "2 h", "1 h"),
      ("Destroyed Abyss Gate", "Bodyguard Teegant", "3 h", "1 h 30 min"), ("Verteron Fortress Ruins", "Kusan the Mad Gladiator", "4 h", "2 h"),
      ("Verteron Fortress Ruins", "Ritualist Garshim", "4 h", "2 h"), ("Northern Tolbas Forest", "Bloodfang Pnyn", "6 h", "3 h"),
      ("Night Dew Cave", "Furious Saursus", "6 h", "3 h"), ("Aullaeu Village", "Scholar Aulla", "4 h", "2 h"),
      ("Forest of Exiles", "Chaser Taulo", "4 h", "2 h"), ("Aullaeu Village", "Forest Warrior Aullamu", "8 h", "4 h"),
      ("Rock Tomb Hill", "Heretic Layla", "6 h", "3 h"), ("Altamia Canyon", "Black Tentacle Lawa", "8 h", "4 h"),
      ("Destroyed Temple Site", "Centurion Demiros", "8 h", "4 h"), ("Contaminated Sanctum", "Divine Ansas", "12 h", "6 h"),
      ("Drana Processing Area", "Harvest Manager Moshav", "6 h", "3 h"), ("Drana Processing Area", "Sentinel K'nash", "8 h", "4 h"),
      ("Nahid Brigade Fortress", "Researcher Setram", "12 h", "6 h"), ("Garden of the Illusion God", "Phantasm Kasia", "12 h", "6 h"),
      ("Southern Altamia Highland", "Silent Dartan", "12 h", "6 h"), ("Eastern Altamia Highland", "Soul Ruler Kashapa", "12 h", "6 h"),
      ("Drana Plantation", "High Commander Lagta", "24 h", "12 h"), ("Eternal Isle", "Eternal Gartua", "24 h", "12 h")]
AS = [("Dredgion Crash Site", "Melted Danar", "1 h", "30 min"), ("Nameless Cemetery", "Black Warrior Aed", "1 h", "30 min"),
      ("Sanctum Outpost", "Faithful Rajit", "1 h", "30 min"), ("Sanctum Outpost", "Berserker Vargor", "2 h", "1 h"),
      ("Moslan Forest", "Blood Warrior Lannar", "3 h", "1 h 30 min"), ("Moslan Forest", "Predator Garsan", "4 h", "2 h"),
      ("Uruthumheim", "Deceiver Trid", "4 h", "2 h"), ("Purifying Forest", "Blue Wave Kelpina", "4 h", "2 h"),
      ("Dranactus", "Advisor Resana", "6 h", "3 h"), ("Dranactus", "High Overseer Nutah", "4 h", "2 h"),
      ("Basfelt Ruins", "Special Operations Leader Linx", "6 h", "3 h"), ("Legion Base Ruins", "Desecrator Newbold", "8 h", "4 h"),
      ("Basfelt Ruins", "Specter Archon Axios", "8 h", "4 h"), ("Fafnite Deposit", "Addicted Hardirun", "6 h", "3 h"),
      ("Western Gribade Highland", "Executioner Barthien", "8 h", "4 h"), ("Eastern Gribade Highland", "Drakan Battalion Weapon Guruta", "12 h", "6 h"),
      ("Black Claw Village", "Veteran Shujakan", "6 h", "3 h"), ("Black Claw Village", "Visionary Karuka", "8 h", "4 h"),
      ("Lagta Fortress", "Dark Shadow Vishwada", "12 h", "6 h"), ("Impetusium Square", "Sharp Shylak", "12 h", "6 h"),
      ("Purifying Forest*", "Silent Dartan*", "12 h", "6 h"), ("Fafnite Deposit*", "Soul Ruler Kashapa*", "12 h", "6 h"),
      ("Lagta Fortress*", "High Commander Lagta*", "24 h", "12 h"), ("Immortal Isle", "Immortal Gartua", "24 h", "12 h")]
AB = [("Lower Reshanta", "Watcher Kaira", "1 h", "1 h"),
      ("Archipelago of Siel's Wings · Siel's Right Wing", "Argo, the Spirit King", "24 h", "12 h"),
      ("Reshanta's Root", "Guardian Lord Nahma", "Domingo", "Sábado y domingo")]
H = ["Zona", "Jefe", "Antes", "Ahora"]
body = ('<h3>Elyos · Verteron</h3>' + table(H, [[e(a), f"<b>{e(b)}</b>", c, f"<b class='new'>{d}</b>"] for a, b, c, d in EL], "boss")
        + '<h3>Asmodians · Altgard</h3>' + table(H, [[e(a), f"<b>{e(b)}</b>", c, f"<b class='new'>{d}</b>"] for a, b, c, d in AS], "boss")
        + '<p class="note">* Sin confirmar en Global: la hoja pone en Altgard estos tres nombres, que también salen en Verteron. Lagta Fortress sí es una zona de Altgard.</p>'
        + '<h3>Abismo</h3>' + table(H, [[e(a), f"<b>{e(b)}</b>", c, f"<b class='new'>{d}</b>"] for a, b, c, d in AB], "boss")
        + '<p class="note">※ La probabilidad de que aparezca Watcher Kaira se ha duplicado.</p>')
section("jefes", "Jefes de campo", "Todos los jefes de campo con su zona y su tiempo de reaparición.", body, "TW")

# ---------------------------------------------------------------- 9. Daevanion (old)
body = (img("s09_000.png", "Progreso de cada tablero: Nezekan 86/88, Zikel 85/88, Vaizel 82/88, Triniel 108/116, Ariel 21/152, Azphel 42/152 (en la imagen salen con los nombres de TW).", "shot")
        + '<div class="pairs">'
        + "".join(f'<div>{img(tag, "", "label")}{img(board, cap, "shot")}</div>' for tag, board, cap in (
            ("s09_002.png", "s09_001.png", "<b>Nezekan</b>86/88 nodos (en la imagen, «Nessaken»)"),
            ("s09_003.png", "s09_004.png", "<b>Zikel</b>85/88 nodos (en la imagen, «Gikair»)"),
            ("s09_005.png", "s09_006.png", "<b>Vaizel</b>82/88 nodos (en la imagen, «Bai Jieer»)"),
            ("s09_007.png", "s09_008.png", "<b>Triniel</b>108/116 nodos (en la imagen, «Trinelle»)"),
            ("s09_010.png", "s09_009.png", "<b>Ariel</b>21/152 nodos"),
            ("s09_012.png", "s09_011.png", "<b>Azphel</b>42/152 nodos (en la imagen, «Aspel»)"))) + "</div>")
section("daevanion", "Daevanion (antiguo)", "Los tableros Daevanion de la hoja, nodo a nodo.", body, "TW")

# ---------------------------------------------------------------- 10. craft
C1 = [("Guard", 5, 2262000), ("Artisan's Refining Stone*", 50, 2300000), ("Robust Balaur Scale*", 122, 70000), ("Wrathful Mind", 18, 3630000),
      ("Wrathful Will", 27, 3700000), ("Wrathful Ego", 42, 140000), ("Maddened Wrathful Curse / Heartblood*", 19, 49000), ("Orichalcum Ingot*", 121, 345000),
      ("Odyle", 70, 312000)]
C2 = [("T5 Guard", 1, 0), ("Artisan's Refining Stone*", 18, 2300000), ("Robust Balaur Scale*", 122, 70000), ("Wrathful Belief", 40, 254000),
      ("Wrathful Flame", 40, 2200000), ("Kinah", 50000000, 1), ("Maddened Wrathful Curse / Heartblood*", 19, 49000), ("Orichalcum Ingot*", 46, 345000), ("Odyle", 26, 312000)]


def fmt(n):
    return f"{n:,}".replace(",", ".")


def craft(rows, title):
    body = [[f"<b>{e(a)}</b>", fmt(b), fmt(c), fmt(b * c)] for a, b, c in rows]
    tot = sum(b * c for _, b, c in rows)
    body.append(["<b>Total</b>", "", "", f"<b>{fmt(tot)}</b>"])
    return f"<h3>{title}</h3>" + table(["Material", "Cantidad", "Precio (Kinah)", "Total (Kinah)"], body, "num")


body = (craft(C1, "Opción A · fabricando 5 Guard") + craft(C2, "Opción B · partiendo de un Guard T5")
        + '<p class="note">* La hoja solo da el nombre corto («Артисан», «Робуст», «Maddened», «Orichalum», mal escrito). En el cliente de Global son: Artisan\'s Refining Stone (o Artisan\'s Ultimate Refining Stone, la hoja no dice cuál), Robust Balaur Scale (o Enhanced Robust Balaur Scale), Maddened Wrathful Curse o Maddened Wrathful Heartblood (no se sabe cuál de los dos) y Orichalcum Ingot (u Orichalcum Ore).</p>')
section("crafteo", "Crafteo", "Lo que cuesta fabricar el Guard, material a material.", body, "TW")

# ---------------------------------------------------------------- 11-12. other classes
BR = [("Pauldrons", "+15 Soaring Daeva"), ("Breastplate", "+15 Soaring Daeva"), ("Greaves", "+15 Soaring Daeva"), ("Gloves", "+15 Soaring Daeva"),
      ("Boots", "+15 Soaring Daeva"), ("Cloak", "+15 Soaring Daeva"), ("Earrings", "+15 Soaring Daeva"),
      ("Ring", "+15 Splendent Ebony Dragon Lord"), ("Ring", "+15 Ebony Dragon Lord")]
body = '<p class="warn">El Brawler es una clase de KR y TW que todavía no ha llegado a Global, y estos objetos tampoco existen allí: el nombre es el que sale en la captura.</p>' + '<div class="gear">' + "".join(img(f"s11_{i:03d}.png", f"<b>{s}</b>{n} {s}", "tip") for i, (s, n) in enumerate(BR)) + "</div>"
section("brawler", "Brawler", "Equipo de referencia de un Brawler, pieza a pieza.", body, "TW")
AS2 = [("Helm", "+15 Durvati Helm"), ("Pauldrons", "+15 Durvati Pauldrons"), ("Breastplate", "+15 Durvati Breastplate"),
       ("Greaves", "+15 Durvati Greaves"), ("Gloves", "+10 Faded Shadow Gloves"), ("Boots", "+12 Lava Heart Boots"),
       ("Cloak", "+15 Durvati Cloak"), ("Earrings", "+15 Scattered Radiance Earrings"), ("Necklace", "+15 Ebony Dragon Lord Necklace"),
       ("Ring", "+15 Ebony Dragon Lord Ring"), ("Ring", "+15 Ebony Dragon Lord Ring")]
body = '<p class="warn">Estos objetos son de TW y todavía no existen en Global: el nombre es el que sale en la captura.</p>' + '<div class="gear">' + "".join(img(f"s12_{i:03d}.png", f"<b>{s}</b>{n}", "tip") for i, (s, n) in enumerate(AS2)) + "</div>"
section("assassin", "Assassin", "Equipo de referencia de un Assassin, pieza a pieza.", body, "TW")

# ---------------------------------------------------------------- page
nav = "".join(f'<a href="#{i}">{t}</a>' for i, t, _ in sections if i != "tw")
page = open(os.path.join(HERE, "page.html"), encoding="utf-8").read()
page = page.replace("{{INTRO}}", INTRO).replace("{{NAV}}", nav).replace("{{BODY}}", "\n".join(s for _, _, s in sections)).replace("{{SRC}}", SRC)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
print("ok", len(os.listdir(os.path.join(OUT, "img"))), "images")
