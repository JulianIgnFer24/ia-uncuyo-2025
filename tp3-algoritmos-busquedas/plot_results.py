#!/usr/bin/env python3
import csv
import os
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
except Exception as e:  # pragma: no cover
    print("[ERROR] No se pudo importar matplotlib.\n"
          "Instalá matplotlib con: pip install matplotlib\n"
          f"Detalle: {e}")
    raise


CSV_PATH = os.path.join(os.path.dirname(__file__), "results.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "images")


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # normalizar tipos
            r["env_n"] = int(r["env_n"]) if r["env_n"] != "" else None
            r["states_n"] = int(r["states_n"]) if r["states_n"] != "" else None
            r["actions_count"] = int(r["actions_count"]) if r["actions_count"] != "" else None
            r["actions_cost"] = float(r["actions_cost"]) if r["actions_cost"] != "" else None
            r["time"] = float(r["time"]) if r["time"] != "" else None
            r["solution_found"] = (
                True if str(r["solution_found"]).strip().lower() == "true" else False
            )
            rows.append(r)
    return rows


def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def group_meta(rows):
    algorithms = sorted({r["algorithm_name"] for r in rows})
    scenarios = sorted({r["scenario"] for r in rows})
    envs = sorted({r["env_n"] for r in rows})
    return algorithms, scenarios, envs


def plot_metric_by_env(rows, metric, title, filename, filter_found=False, ylabel=None):
    # Estructura: data[scenario][algorithm] -> list of (env_n, metric)
    data = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if filter_found and not r["solution_found"]:
            continue
        if r[metric] is None:
            continue
        data[r["scenario"]][r["algorithm_name"]].append((r["env_n"], r[metric]))

    scenarios = sorted(data.keys())
    if not scenarios:
        print(f"[WARN] No hay datos para {metric} (filter_found={filter_found}).")
        return

    ncols = len(scenarios)
    fig, axes = plt.subplots(1, ncols, figsize=(6 * ncols, 4), sharey=True)
    if ncols == 1:
        axes = [axes]

    colors = plt.cm.get_cmap('tab10')

    for ax, scen in zip(axes, scenarios):
        algos = sorted(data[scen].keys())
        for idx, algo in enumerate(algos):
            pts = sorted(data[scen][algo], key=lambda x: x[0])
            if not pts:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.plot(xs, ys, marker='o', label=algo, color=colors(idx % 10))
        ax.set_title(f"{scen}")
        ax.set_xlabel("env_n")
        ax.grid(True, linestyle='--', alpha=0.4)
        if ylabel:
            ax.set_ylabel(ylabel)

    # leyenda única
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=min(5, len(labels)))
    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    outpath = os.path.join(OUT_DIR, filename)
    fig.savefig(outpath, dpi=160)
    plt.close(fig)
    print(f"[OK] Guardado: {outpath}")


def bar_avg_time_by_algorithm(rows, filename):
    # promedio de tiempo por algoritmo y escenario
    agg = defaultdict(lambda: defaultdict(list))  # scen -> algo -> [times]
    for r in rows:
        if r["time"] is None:
            continue
        agg[r["scenario"]][r["algorithm_name"]].append(r["time"])

    scenarios = sorted(agg.keys())
    if not scenarios:
        print("[WARN] No hay datos de tiempo.")
        return

    ncols = len(scenarios)
    fig, axes = plt.subplots(1, ncols, figsize=(6 * ncols, 4), sharey=True)
    if ncols == 1:
        axes = [axes]

    for ax, scen in zip(axes, scenarios):
        algos = sorted(agg[scen].keys())
        means = [sum(agg[scen][a]) / len(agg[scen][a]) for a in algos]
        ax.bar(algos, means, color=plt.cm.Paired.colors)
        ax.set_title(f"Promedio tiempo - {scen}")
        ax.set_ylabel("tiempo (s)")
        ax.set_xticklabels(algos, rotation=45, ha='right')
        ax.grid(True, axis='y', linestyle='--', alpha=0.4)

    fig.tight_layout()
    outpath = os.path.join(OUT_DIR, filename)
    fig.savefig(outpath, dpi=160)
    plt.close(fig)
    print(f"[OK] Guardado: {outpath}")


def boxplot_metric_by_algorithm(rows, metric, title, filename, filter_found=False, ylabel=None):
    # Agrupar valores por algoritmo dentro de cada escenario
    agg = defaultdict(lambda: defaultdict(list))  # scen -> algo -> [vals]
    for r in rows:
        if filter_found and not r["solution_found"]:
            continue
        if r[metric] is None:
            continue
        agg[r["scenario"]][r["algorithm_name"]].append(r[metric])

    scenarios = sorted(agg.keys())
    if not scenarios:
        print(f"[WARN] No hay datos para {metric} (boxplot)")
        return

    ncols = len(scenarios)
    fig, axes = plt.subplots(1, ncols, figsize=(6 * ncols, 4), sharey=True)
    if ncols == 1:
        axes = [axes]

    for ax, scen in zip(axes, scenarios):
        algos = sorted(agg[scen].keys())
        data = [agg[scen][a] for a in algos]
        if not data:
            continue
        bp = ax.boxplot(data, patch_artist=True)
        # Colorear boxplots ligeramente
        colors = plt.colormaps.get_cmap('Pastel1')
        for i, box in enumerate(bp['boxes']):
            box.set(facecolor=colors(i % colors.N), alpha=0.8)
        ax.set_title(f"{scen}")
        ax.set_xlabel("algoritmo")
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.grid(True, axis='y', linestyle='--', alpha=0.4)
        ax.set_xticks(range(1, len(algos) + 1))
        ax.set_xticklabels(algos, rotation=45, ha='right')

    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    outpath = os.path.join(OUT_DIR, filename)
    fig.savefig(outpath, dpi=160)
    plt.close(fig)
    print(f"[OK] Guardado: {outpath}")


def main():
    ensure_out_dir()
    if not os.path.exists(CSV_PATH):
        raise SystemExit(f"No se encontró el archivo CSV en: {CSV_PATH}")

    rows = load_rows(CSV_PATH)

    # Line plots por escenario: tiempo, estados explorados
    plot_metric_by_env(
        rows,
        metric="time",
        title="Tiempo vs env_n por algoritmo",
        filename="time_vs_env_por_escenario.png",
        filter_found=False,
        ylabel="tiempo (s)",
    )

    plot_metric_by_env(
        rows,
        metric="states_n",
        title="Estados explorados vs env_n",
        filename="states_vs_env_por_escenario.png",
        filter_found=False,
        ylabel="estados explorados",
    )

    # Para acciones y costo de acciones, usamos solo soluciones encontradas
    plot_metric_by_env(
        rows,
        metric="actions_count",
        title="Longitud del plan vs env_n (solo soluciones)",
        filename="actions_count_vs_env_solo_soluciones.png",
        filter_found=True,
        ylabel="acciones en el plan",
    )

    plot_metric_by_env(
        rows,
        metric="actions_cost",
        title="Costo del plan vs env_n (solo soluciones)",
        filename="actions_cost_vs_env_solo_soluciones.png",
        filter_found=True,
        ylabel="costo acumulado",
    )

    # Barras con promedios de tiempo por algoritmo y escenario
    bar_avg_time_by_algorithm(rows, filename="avg_tiempo_por_algoritmo.png")

    # Boxplots por algoritmo en cada escenario
    boxplot_metric_by_algorithm(
        rows,
        metric="time",
        title="Boxplot Tiempo por algoritmo (por escenario)",
        filename="boxplot_time_por_algoritmo.png",
        ylabel="tiempo (s)",
    )

    boxplot_metric_by_algorithm(
        rows,
        metric="states_n",
        title="Boxplot Estados explorados por algoritmo (por escenario)",
        filename="boxplot_states_por_algoritmo.png",
        ylabel="estados explorados",
    )

    boxplot_metric_by_algorithm(
        rows,
        metric="actions_count",
        title="Boxplot Longitud del plan (solo soluciones)",
        filename="boxplot_actions_count_solo_soluciones.png",
        filter_found=True,
        ylabel="acciones en el plan",
    )

    boxplot_metric_by_algorithm(
        rows,
        metric="actions_cost",
        title="Boxplot Costo del plan (solo soluciones)",
        filename="boxplot_actions_cost_solo_soluciones.png",
        filter_found=True,
        ylabel="costo acumulado",
    )

    print(f"Listo. Gráficos en: {OUT_DIR}")


if __name__ == "__main__":
    main()
