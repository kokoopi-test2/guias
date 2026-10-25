"""Kala's words for each section: what it is and how to use it, in plain Spanish (AMO 2026-10-25: «una guía para
monos, que lo entienda todo el mundo sin perder ni un solo detalle»)."""

INTRO = """
<div class="kala"><div class="av">K</div><div>
<p><b>Holiii 🤍 Soy Kala.</b> Esta es una hoja de Spiritmaster de la comunidad rusa, muy completa, pero venía en ruso y era un lío de pestañas.
Te la he dejado en español y ordenada, sin quitar nada de lo que cuenta: cada tabla, cada nota y cada captura siguen aquí.</p>
<p>Los nombres del juego (habilidades, estadísticas, objetos, jefes) los dejo <b>en inglés, tal cual salen en tu cliente de Global</b>,
para que los busques en el juego sin traducir nada. Lo que te explico, en español. Las partes marcadas <b>TW</b> son del servidor de Taiwán: ahí algunos objetos aún no existen en Global y llevan el nombre de su captura.</p>
</div></div>
<div class="how"><h3>Cómo leer esta guía en 2 minutos</h3><dl>
<dt>PvE y PvP</dt><dd>PvE es contra monstruos (mazmorras, jefes). PvP es contra otros jugadores. Muchas cosas cambian según a qué vayas.</dd>
<dt>Global y TW</dt><dd>Global es nuestro servidor. TW es el de Taiwán, que va por delante en parches: lo de TW sirve para ver por dónde van los tiros, pero puede cambiar.</dd>
<dt>Stigma</dt><dd>Habilidades extra que equipas en sus casillas y que subes de nivel.</dd>
<dt>Specialty</dt><dd>Las mejoras numeradas que eliges dentro de cada habilidad. Cuando leas «Specialty 2, 4», marca la 2 y la 4.</dd>
<dt>Manastone</dt><dd>Las piedras que engarzas en el equipo para sumarle estadísticas.</dd>
<dt>Pet Insight</dt><dd>Las estadísticas que da tu mascota según su tipo (Cogni, Fera, Natura, Varian o Special), casilla a casilla.</dd>
<dt>Soul Binding</dt><dd>Las estadísticas extra de cada pieza, las que salen bajo «Soul Binding Rate» en el tooltip. Las tablas de «Línea» te dicen cuál buscar en cada una.</dd><dt>Philosopher's Stone</dt><dd>Philosopher's Stone: Revelation o Power. Se usa en una pieza y da una de esas líneas que no sale de otra forma (el tooltip la enseña como «Soul Fuse Philosopher's Stone…»).</dd>
<dt>Objeto rojo</dt><dd>Las piezas de cabecera roja (Heroic). Las capturas son de TW: en Global todavía no hay equipo rojo.</dd><dt>Smite</dt><dd>Es lo mismo que Double Chance: probabilidad de pegar doble. El equipo la llama Smite.</dd><dt>Kina</dt><dd>El dinero del juego.</dd>
<dt>Summon (espíritus)</dt><dd>El Spiritmaster invoca espíritus que pelean contigo: Fire, Water, Earth, Wind y Ancient.</dd>
<dt>Combat Analysis</dt><dd>La ventana del juego que mide tu daño. Las mediciones de la hoja son contra el muñeco de entrenamiento.</dd>
</dl><p><b>Si eres nuevo, por dónde empezar:</b> 1) <a href="#global">Global</a>: lo pensado para nuestro servidor, qué estadísticas buscar en tu equipo y el orden de las Stigma. 2) <a href="#habilidades">Habilidades</a>: qué subir y qué Specialty marcar (es de TW, pero las habilidades son las mismas). 3) El resto es consulta: equipo de referencia, daño, jefes y crafteo.</p><p class="note">Pulsa cualquier imagen para verla en grande. La barra de arriba te lleva a cada parte.</p></div>
"""

BOX = {
    "enlaces": "Webs para buscar personajes, mirar rankings y medir tu daño, más las builds de referencia. Si solo vas a mirar una, "
               "mira la <b>build de prueba para Global</b>.",
    "global": "Lo más actual de la hoja, pensado para nuestro servidor. Primero las estadísticas de tu mascota (Pet Insight), luego "
              "qué estadística buscar en cada línea de cada pieza de equipo y, al final, en qué orden subir las Stigma. "
              "<b>Cómo usarlo:</b> busca tu pieza en la columna y lee hacia abajo, línea a línea.",
    "habilidades": "Cada habilidad del Spiritmaster con el nivel al que subirla y qué Specialty marcar, para PvE y para PvP. "
                   "Debajo, qué Stigma llevar y qué estadísticas buscar en las Manastones, por tiers (S es lo mejor). "
                   "<b>Cómo usarlo:</b> abre tu ventana de habilidades y copia fila a fila.",
    "pvp": "El equipo completo de un Spiritmaster preparado para PvP, pieza a pieza, con sus estadísticas, las habilidades que sube "
           "cada pieza y sus Manastones. <b>Cómo usarlo:</b> compara tu pieza con la de la foto y busca las mismas líneas.",
    "pve": "Lo mismo para PvE, con las notas de la hoja sobre qué estadísticas son obligatorias y en qué orden priorizar las "
           "Manastones.",
    "dps": "Las pruebas de daño del autor de la hoja contra el muñeco de entrenamiento: cuánto pega cada espíritu, qué combo rinde "
           "más, si importa atacar de frente o por detrás y cómo cambió todo con cada parche. <b>Para qué te sirve:</b> elegir "
           "espíritu, combo y rotación con números, no a ojo.",
    "espiritus": "Cuánto pega cada espíritu en 20 segundos pegando solo él al muñeco, y cuántos golpes da. Es lo que dice qué espíritu es el más rápido y el que "
                 "más daño hace.",
    "jefes": "Cada jefe de campo con su zona y cada cuánto vuelve a aparecer en TW: «Antes» es el tiempo viejo y «Ahora» el de después "
             "del cambio (la mitad en casi todos).",
    "daevanion": "Los tableros Daevanion (los árboles de nodos de cada dios) que tenía el autor: los nodos que brillan son los activados y los oscuros, los que faltan. La hoja los marca como <b>antiguos, ya no actuales</b>: "
                 "míralos solo como referencia.",
    "crafteo": "Cuánto cuesta fabricar el escudo (Guard), material a material, con los precios de mercado que apuntó el autor. Yo he "
               "hecho las cuentas: cantidad por precio y el total.",
    "brawler": "Bonus de la hoja: el equipo de un Brawler (la clase de puños), pieza a pieza.",
    "assassin": "Bonus de la hoja: el equipo de un Assassin, pieza a pieza.",
}
