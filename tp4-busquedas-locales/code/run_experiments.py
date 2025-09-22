#!/usr/bin/env python3
import argparse
import csv
import os
from glob import glob
from statistics import mean, pstdev
from typing import Dict, List

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False

from algorithms import hill_climbing, simulated_annealing, genetic_algorithm, random_search, AlgoResult


def ensure_dirs(base_dir: str):
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "code"), exist_ok=True)


def run_one(algorithm: str, n: int, max_states: int, seed: int, record_history: bool) -> AlgoResult:
    if algorithm == "HC":
        return hill_climbing(n=n, max_states=max_states, seed=seed, record_history=record_history)
    if algorithm == "SA":
        # geometric cooling schedule: T_k = T0 * alpha^k
        return simulated_annealing(n=n, max_states=max_states, seed=seed, T0=1.0, alpha=0.995, Tmin=1e-4, record_history=record_history)
    if algorithm == "GA":
        return genetic_algorithm(n=n, max_states=max_states, seed=seed, pop_size=120, tournament_k=3, crossover_rate=0.9, mutation_rate=0.25, elitism=2, record_history=record_history)
    if algorithm == "random":
        return random_search(n=n, max_states=max_states, seed=seed, record_history=record_history)
    raise ValueError(f"Unknown algorithm: {algorithm}")


def write_csv(rows: List[Dict], out_csv: str):
    fieldnames = [
        "algorithm_name",
        "env_n",
        "size",
        "best_solution",
        "H",
        "states",
        "time",
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def read_csv(csv_path: str) -> List[Dict]:
    rows: List[Dict] = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({
                    "algorithm_name": row["algorithm_name"],
                    "env_n": int(row["env_n"]),
                    "size": int(row["size"]),
                    "best_solution": row["best_solution"],
                    "H": float(row["H"]),
                    "states": int(float(row["states"])),
                    "time": float(row["time"]),
                })
    except FileNotFoundError:
        print(f"[ERROR] CSV no encontrado: {csv_path}")
    return rows


def plot_history(history: List[int], title: str, outpath: str):
    if not history or not HAS_MPL:
        return
    plt.figure(figsize=(6, 4))
    plt.plot(range(len(history)), history, marker='o', markersize=2)
    plt.xlabel("iteración")
    plt.ylabel("H(board)")
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()


def boxplots_from_csv(rows: List[Dict], images_dir: str):
    if not HAS_MPL:
        print("[WARN] matplotlib no disponible; se omiten gráficos.")
        return

    sizes = sorted({int(r["size"]) for r in rows})
    algos = sorted({r["algorithm_name"] for r in rows})

    for size in sizes:
        # Boxplot de H final
        H_data = {
            algo: [float(r["H"]) for r in rows if int(r["size"]) == size and r["algorithm_name"] == algo]
            for algo in algos
        }
        H_data = {k: v for k, v in H_data.items() if v}
        if H_data:
            plt.figure(figsize=(6, 4))
            plt.boxplot(list(H_data.values()), patch_artist=True)
            plt.xticks(range(1, len(H_data) + 1), list(H_data.keys()))
            plt.ylabel("H(board)")
            plt.title(f"Distribución H final - N={size}")
            plt.grid(True, axis="y", linestyle="--", alpha=0.4)
            plt.tight_layout()
            out = os.path.join(images_dir, f"box_H_N{size}.png")
            plt.savefig(out, dpi=160)
            plt.close()

        # Boxplot de tiempos sólo para ejecuciones exitosas (H == 0)
        time_success_data = {
            algo: [float(r["time"]) for r in rows if int(r["size"]) == size and r["algorithm_name"] == algo and float(r["H"]) == 0.0]
            for algo in algos
        }
        if any(time_success_data.values()):
            fig, ax = plt.subplots(figsize=(6, 4))
            labels: List[str] = []
            empty_positions: List[int] = []
            pos = 1
            for algo in algos:
                vals = time_success_data.get(algo, [])
                labels.append(algo)
                if vals:
                    ax.boxplot(vals, positions=[pos], patch_artist=True)
                else:
                    empty_positions.append(pos)
                pos += 1

            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels)
            ax.set_ylabel("tiempo (s)")
            ax.set_title(f"Tiempo (soluciones) - N={size}")
            ax.grid(True, axis="y", linestyle="--", alpha=0.4)
            ax.set_xlim(0.5, len(labels) + 0.5)

            ylim = ax.get_ylim()
            y_text = ylim[1] * 0.9 if ylim[1] > 0 else 0.1
            for pos in empty_positions:
                ax.text(pos, y_text, "0 éxitos", ha="center", va="top", fontsize=8, color="red")

            plt.tight_layout()
            out = os.path.join(images_dir, f"box_time_success_N{size}.png")
            fig.savefig(out, dpi=160)
            plt.close(fig)


def cleanup_image_dir(images_dir: str, keep_history: bool) -> None:
    os.makedirs(images_dir, exist_ok=True)
    if not keep_history:
        for path in glob(os.path.join(images_dir, "H_history_*.png")):
            try:
                os.remove(path)
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description="Experimentos N-Queens (HC, SA, GA, random)")
    parser.add_argument("--sizes", nargs="*", type=int, default=[4, 8, 10], help="Tamaños de tablero N")
    parser.add_argument("--seeds", type=int, default=30, help="Cantidad de semillas (ejecuciones) por algoritmo y tamaño")
    parser.add_argument("--max_states", type=int, default=20000, help="Máximo de estados evaluados por corrida (mismo para todos)")
    parser.add_argument("--base_dir", type=str, default=os.path.dirname(os.path.dirname(__file__)), help="Directorio base tp4-busquedas-locales")
    parser.add_argument("--record_hist", action="store_true", help="Guardar historia H() para un caso por algoritmo")
    parser.add_argument("--csv_path", type=str, help="Ruta personalizada del CSV con resultados")
    parser.add_argument("--only_plots", action="store_true", help="Solo generar gráficos y resumen a partir del CSV existente")
    parser.add_argument("--hist_plots", action="store_true", help="Guardar gráficos H_history además de los boxplots")
    args = parser.parse_args()

    base_dir = args.base_dir
    ensure_dirs(base_dir)
    images_dir = os.path.join(base_dir, "images")
    out_csv = args.csv_path if args.csv_path else os.path.join(base_dir, "tp4-Nreinas.csv")
    cleanup_image_dir(images_dir, keep_history=args.hist_plots)

    algorithms = ["random", "HC", "SA", "GA"]
    rows: List[Dict] = []

    if args.only_plots:
        rows = read_csv(out_csv)
        if not rows:
            return
        print(f"[OK] Resultados cargados desde CSV: {out_csv}")
    else:
        # For requirement 6: pick the first seed to record history per algorithm
        hist_seed = 0
        for n in args.sizes:
            for algo in algorithms:
                for env_n in range(args.seeds):
                    record_history = args.record_hist and env_n == hist_seed
                    res = run_one(algo, n, args.max_states, seed=env_n, record_history=record_history)
                    rows.append({
                        "algorithm_name": algo,
                        "env_n": env_n,
                        "size": n,
                        "best_solution": str(res.best_solution),
                        "H": int(res.H),
                        "states": int(res.states),
                        "time": float(res.time),
                    })
                    if args.hist_plots and record_history and res.history:
                        title = f"H por iteración - {algo} - N={n} (seed={env_n})"
                        out = os.path.join(images_dir, f"H_history_{algo}_N{n}.png")
                        plot_history(res.history, title, out)

        write_csv(rows, out_csv)
        print(f"[OK] CSV guardado en: {out_csv}")

    # Basic stats printed to console
    for n in sorted({int(r["size"]) for r in rows}):
        print(f"\n== Resumen N={n} ==")
        for algo in ["random", "HC", "SA", "GA"]:
            subset = [r for r in rows if int(r["size"]) == n and r["algorithm_name"] == algo]
            if not subset:
                continue
            optimal = sum(1 for r in subset if float(r["H"]) == 0)
            pct_opt = 100.0 * optimal / len(subset)
            H_vals = [float(r["H"]) for r in subset]
            T_vals = [float(r["time"]) for r in subset]
            S_vals = [float(r["states"]) for r in subset]
            print(f"{algo:>7} | óptimos: {pct_opt:5.1f}% | H prom: {mean(H_vals):6.2f} ± {pstdev(H_vals):.2f} | tiempo: {mean(T_vals):.3f}s ± {pstdev(T_vals):.3f} | estados: {mean(S_vals):.0f} ± {pstdev(S_vals):.0f}")

    # Generate boxplots
    boxplots_from_csv(rows, images_dir)
    if HAS_MPL:
        print(f"[OK] Gráficos en: {images_dir}")
    else:
        print("[INFO] matplotlib no disponible; no se generaron gráficos.")


if __name__ == "__main__":
    main()
