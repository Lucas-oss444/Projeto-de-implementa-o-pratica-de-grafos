import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from rede_transporte import LINHAS

POS = {
    "Ver-o-Peso": (0.0, 0.0),
    "Cidade Velha": (0.5, -1.3),
    "Batista Campos": (2.2, -1.4),
    "Nazare": (1.5, 0.3),
    "Sao Bras": (3.1, 0.7),
    "Guama": (4.4, -1.5),
    "UFPA": (3.6, -2.7),
    "Pedreira": (3.0, 2.2),
    "Telegrafo": (4.3, 3.1),
    "Entroncamento": (5.0, 1.1),
    "Marambaia": (6.3, 1.7),
    "Aguas Lindas": (8.0, 2.1),
    "Coqueiro": (6.0, 3.5),
    "Icoaraci": (5.5, 5.0),
    "Distrito Industrial": (9.6, 2.8),
}

NOMES = {
    "Ver-o-Peso": "Ver-o-Peso",
    "Cidade Velha": "Cidade Velha",
    "Batista Campos": "Batista Campos",
    "Nazare": "Nazaré",
    "Sao Bras": "São Brás",
    "Guama": "Guamá",
    "UFPA": "UFPA",
    "Pedreira": "Pedreira",
    "Telegrafo": "Telégrafo",
    "Entroncamento": "Entroncamento",
    "Marambaia": "Marambaia",
    "Aguas Lindas": "Águas Lindas",
    "Coqueiro": "Coqueiro",
    "Icoaraci": "Icoaraci",
    "Distrito Industrial": "Distrito Industrial",
}

CORES = {
    "L1 - BRT Almirante Barroso": "#1B3A4B",
    "L2 - Augusto Montenegro": "#2E8B8B",
    "L3 - Circular Centro": "#E8743B",
    "L4 - Universitario": "#7A5195",
    "L5 - Pedreira": "#BC5090",
    "L6 - Expresso Industrial": "#C1272D",
}

RAD = {"L3 - Circular Centro": 0.22, "L6 - Expresso Industrial": 0.0}

LABEL_OFF = {
    "Icoaraci": (0, 0.30),
    "Coqueiro": (0.55, 0.10),
    "Telegrafo": (-0.15, 0.28),
    "Aguas Lindas": (0, 0.30),
    "Distrito Industrial": (0, -0.36),
    "Pedreira": (-0.60, 0.10),
    "Marambaia": (0, 0.30),
    "Entroncamento": (0.30, -0.32),
    "Sao Bras": (-0.55, 0.22),
    "Nazare": (-0.45, 0.22),
    "Ver-o-Peso": (-0.35, 0.28),
    "Cidade Velha": (0, -0.34),
    "Batista Campos": (0, -0.34),
    "Guama": (0.55, 0.10),
    "UFPA": (0, -0.34),
}


def perpendicular(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    norma = (dx ** 2 + dy ** 2) ** 0.5
    return -dy / norma, dx / norma


def desenhar():
    fig, ax = plt.subplots(figsize=(14, 9))

    for nome, paradas, tempos, mao_dupla in LINHAS:
        cor = CORES[nome]
        rad = RAD.get(nome, 0.0)
        for i in range(len(paradas) - 1):
            p, q = POS[paradas[i]], POS[paradas[i + 1]]
            estilo = "-|>" if not mao_dupla else "-"
            ax.add_patch(FancyArrowPatch(
                p, q,
                connectionstyle=f"arc3,rad={rad}",
                arrowstyle=estilo,
                mutation_scale=22,
                linewidth=2.6,
                color=cor,
                shrinkA=13, shrinkB=13,
                zorder=1,
            ))
            px, py = perpendicular(p, q)
            mx = (p[0] + q[0]) / 2 + rad * px * 0.9
            my = (p[1] + q[1]) / 2 + rad * py * 0.9
            ax.text(mx, my, str(tempos[i]), fontsize=9, color=cor,
                    ha="center", va="center", zorder=3,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                              edgecolor="none", alpha=0.92))

    for parada, (x, y) in POS.items():
        isolada = parada == "Distrito Industrial"
        ax.scatter([x], [y], s=230, zorder=4,
                   facecolor="#C1272D" if isolada else "white",
                   edgecolor="#C1272D" if isolada else "#1B3A4B",
                   linewidth=2.2)
        dx, dy = LABEL_OFF[parada]
        ax.text(x + dx, y + dy, NOMES[parada], fontsize=10.5, zorder=5,
                ha="center", va="center", color="#1B3A4B",
                fontweight="bold" if isolada else "normal",
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                          edgecolor="none", alpha=0.88))

    ax.annotate("componente fortemente conexa isolada:\nchega-se, mas não se retorna",
                xy=(9.6, 2.8), xytext=(9.0, 4.3), fontsize=9.5, color="#C1272D",
                ha="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color="#C1272D", linewidth=1.4))

    legenda = [Line2D([0], [0], color=CORES[n], linewidth=3,
                      label=n.replace("Universitario", "Universitário")) for n, _, _, _ in LINHAS]
    legenda.append(Line2D([0], [0], color="#555555", linewidth=3, label="sem seta: mão dupla"))
    legenda.append(Line2D([0], [0], color="#555555", linewidth=3,
                          marker=">", markersize=8, label="com seta: sentido único"))
    ax.legend(handles=legenda, loc="lower right", fontsize=10, frameon=True,
              framealpha=0.95, edgecolor="#CCCCCC")

    ax.set_title("Rede de transporte modelada como dígrafo ponderado  |  |V| = 15, |A| = 31",
                 fontsize=15, color="#1B3A4B", pad=18)
    ax.text(0.0, 5.4, "pesos em minutos", fontsize=10, color="#666666")
    ax.set_xlim(-1.2, 11.0)
    ax.set_ylim(-3.5, 5.8)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig("rede_transporte.png", dpi=200, facecolor="white")


if __name__ == "__main__":
    desenhar()
