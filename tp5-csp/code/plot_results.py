"""
Plot results for N-Queens experiments: boxplots for time and nodes explored.
Reads: ../tp5-Nreinas.csv
Saves plots to ../images/
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'tp5-Nreinas.csv')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')

os.makedirs(IMAGES_DIR, exist_ok=True)


def main():
    df = pd.read_csv(CSV_PATH)

    # Ensure columns are of correct types
    df['n'] = df['n'].astype(int)
    df['nodes_explored'] = df['nodes_explored'].astype(int)
    df['time_taken'] = df['time_taken'].astype(float)
    df['solution_found'] = df['solution_found'].astype(bool)

    # Filter only successful runs (the user requested plots of nodes explored and time)
    df_success = df[df['solution_found']]

    if df_success.empty:
        print('No successful runs found in CSV. Exiting.')
        return

    # Boxplot: Execution Time by algorithm and board size
    plt.figure(figsize=(12, 7))
    sns.boxplot(data=df_success, x='n', y='time_taken', hue='algorithm', width=0.6)
    plt.title('Tiempo de Ejecución por Algoritmo y Tamaño del Tablero', fontsize=14, fontweight='bold')
    plt.xlabel('Tamaño del Tablero (N)', fontsize=12)
    plt.ylabel('Tiempo (segundos)', fontsize=12)
    plt.legend(title='Algoritmo', title_fontsize=11, fontsize=10)
    plt.grid(True, alpha=0.3)
    out_time = os.path.join(IMAGES_DIR, 'boxplot_time.png')
    plt.tight_layout()
    plt.savefig(out_time, dpi=300, bbox_inches='tight')
    print(f'Saved {out_time}')
    plt.close()

    # Bar plot: Nodes Explored by algorithm and board size
    nodes_summary = df_success.groupby(['n', 'algorithm'])['nodes_explored'].mean().reset_index()
    
    plt.figure(figsize=(12, 7))
    x_pos = np.arange(len(df_success['n'].unique()))
    width = 0.35
    
    algorithms = sorted(df_success['algorithm'].unique())
    colors = ['#8dd3c7', '#fb8072']
    
    for i, algo in enumerate(algorithms):
        algo_data = nodes_summary[nodes_summary['algorithm'] == algo].sort_values('n')
        positions = x_pos + (i - 0.5) * width
        bars = plt.bar(positions, algo_data['nodes_explored'], width, 
                label=algo, color=colors[i], alpha=0.85, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Nodos Explorados por Algoritmo y Tamaño del Tablero', fontsize=14, fontweight='bold')
    plt.xlabel('Tamaño del Tablero (N)', fontsize=12)
    plt.ylabel('Nodos Explorados', fontsize=12)
    plt.xticks(x_pos, sorted(df_success['n'].unique()))
    plt.legend(title='Algoritmo', title_fontsize=11, fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    plt.ylim(bottom=0)
    out_nodes = os.path.join(IMAGES_DIR, 'boxplot_nodes.png')
    plt.tight_layout()
    plt.savefig(out_nodes, dpi=300, bbox_inches='tight')
    print(f'Saved {out_nodes}')
    plt.close()


if __name__ == '__main__':
    main()
