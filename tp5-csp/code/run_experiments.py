"""
Run experiments for N-Queens CSP algorithms.
"""
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
import os
from nqueens_csp import NQueensCSP, is_valid_solution


def run_experiment(algorithm: str, n: int, num_runs: int = 30) -> List[Dict[str, Any]]:
    """
    Run experiments for a given algorithm and board size.
    
    Args:
        algorithm: 'backtrack' or 'forward_checking'
        n: Board size
        num_runs: Number of runs with different seeds
    
    Returns:
        List of experiment results
    """
    results = []
    
    for seed in range(num_runs):
        # Set random seed for reproducibility
        random.seed(seed)
        
        csp = NQueensCSP(n)
        
        if algorithm == 'backtrack':
            solution, nodes_explored, time_taken = csp.solve_backtrack()
        elif algorithm == 'forward_checking':
            solution, nodes_explored, time_taken = csp.solve_forward_checking()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Record results
        result = {
            'algorithm': algorithm,
            'seed': seed,
            'n': n,
            'solution_found': solution is not None,
            'solution': solution if solution else [],
            'nodes_explored': nodes_explored,
            'time_taken': time_taken,
            'valid_solution': is_valid_solution(solution) if solution else False
        }
        
        results.append(result)
        
        print(f"{algorithm} - N={n} - Seed={seed}: "
              f"{'Found' if solution else 'Not found'} - "
              f"Nodes: {nodes_explored} - "
              f"Time: {time_taken:.6f}s")
    
    return results


def run_all_experiments() -> pd.DataFrame:
    """Run all experiments for both algorithms and all board sizes."""
    algorithms = ['backtrack', 'forward_checking']
    board_sizes = [4, 8, 10]  # Can extend to [4, 8, 10, 12, 15] if desired
    num_runs = 30
    
    all_results = []
    
    for algorithm in algorithms:
        for n in board_sizes:
            print(f"\n{'='*50}")
            print(f"Running {algorithm} for {n}-Queens...")
            print(f"{'='*50}")
            
            results = run_experiment(algorithm, n, num_runs)
            all_results.extend(results)
    
    return pd.DataFrame(all_results)


def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate statistics for each algorithm and board size."""
    stats = []
    
    for algorithm in df['algorithm'].unique():
        for n in df['n'].unique():
            subset = df[(df['algorithm'] == algorithm) & (df['n'] == n)]
            
            # Calculate statistics
            success_rate = (subset['solution_found'].sum() / len(subset)) * 100
            
            # Only calculate stats for successful runs
            successful_runs = subset[subset['solution_found']]
            
            if len(successful_runs) > 0:
                avg_time = successful_runs['time_taken'].mean()
                std_time = successful_runs['time_taken'].std()
                avg_nodes = successful_runs['nodes_explored'].mean()
                std_nodes = successful_runs['nodes_explored'].std()
            else:
                avg_time = std_time = avg_nodes = std_nodes = np.nan
            
            stats.append({
                'algorithm': algorithm,
                'n': n,
                'success_rate': success_rate,
                'avg_time': avg_time,
                'std_time': std_time,
                'avg_nodes': avg_nodes,
                'std_nodes': std_nodes,
                'total_runs': len(subset),
                'successful_runs': len(successful_runs)
            })
    
    return pd.DataFrame(stats)


def create_boxplots(df: pd.DataFrame, output_dir: str):
    """Create boxplots for time and nodes explored."""
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Filter only successful runs
    successful_df = df[df['solution_found']]
    
    if len(successful_df) == 0:
        print("No successful runs to plot!")
        return
    
    # Create boxplot for execution time
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=successful_df, x='n', y='time_taken', hue='algorithm')
    plt.title('Distribution of Execution Time by Algorithm and Board Size')
    plt.xlabel('Board Size (N)')
    plt.ylabel('Execution Time (seconds)')
    plt.legend(title='Algorithm')
    plt.yscale('log')  # Log scale for better visualization
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'boxplot_time_csp.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create boxplot for nodes explored
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=successful_df, x='n', y='nodes_explored', hue='algorithm')
    plt.title('Distribution of Nodes Explored by Algorithm and Board Size')
    plt.xlabel('Board Size (N)')
    plt.ylabel('Nodes Explored')
    plt.legend(title='Algorithm')
    plt.yscale('log')  # Log scale for better visualization
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'boxplot_nodes_csp.png'), dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create separate plots for each board size
    for n in successful_df['n'].unique():
        subset = successful_df[successful_df['n'] == n]
        
        if len(subset) == 0:
            continue
        
        # Time plot for this board size
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=subset, x='algorithm', y='time_taken')
        plt.title(f'Execution Time Distribution - {n}-Queens')
        plt.xlabel('Algorithm')
        plt.ylabel('Execution Time (seconds)')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'boxplot_time_N{n}_csp.png'), dpi=300, bbox_inches='tight')
        plt.show()
        
        # Nodes plot for this board size
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=subset, x='algorithm', y='nodes_explored')
        plt.title(f'Nodes Explored Distribution - {n}-Queens')
        plt.xlabel('Algorithm')
        plt.ylabel('Nodes Explored')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'boxplot_nodes_N{n}_csp.png'), dpi=300, bbox_inches='tight')
        plt.show()


def compare_with_tp4(csp_stats: pd.DataFrame):
    """Compare CSP results with TP4 local search results."""
    print("\n" + "="*60)
    print("COMPARISON WITH TP4 (Local Search Algorithms)")
    print("="*60)
    
    # Load TP4 results if available
    tp4_path = "/home/julian-fernandez/Documents/Facultad/S6/ia1/tp4-busquedas-locales/tp4-Nreinas.csv"
    
    try:
        tp4_df = pd.read_csv(tp4_path)
        
        print("\nTP4 Results Summary (Local Search):")
        for n in [4, 8, 10]:
            tp4_subset = tp4_df[tp4_df['size'] == n]
            if len(tp4_subset) > 0:
                success_rate = (tp4_subset['H'] == 0).mean() * 100
                avg_time = tp4_subset[tp4_subset['H'] == 0]['time'].mean()
                avg_states = tp4_subset[tp4_subset['H'] == 0]['states'].mean()
                
                print(f"\n{n}-Queens (Local Search - Best Algorithm):")
                print(f"  Success Rate: {success_rate:.1f}%")
                print(f"  Avg Time: {avg_time:.6f}s")
                print(f"  Avg States: {avg_states:.1f}")
    
    except FileNotFoundError:
        print("TP4 results file not found. Cannot perform comparison.")
    
    print("\nCSP Results Summary:")
    for _, row in csp_stats.iterrows():
        print(f"\n{row['n']}-Queens ({row['algorithm']}):")
        print(f"  Success Rate: {row['success_rate']:.1f}%")
        print(f"  Avg Time: {row['avg_time']:.6f}s")
        print(f"  Avg Nodes: {row['avg_nodes']:.1f}")
        print(f"  Std Time: {row['std_time']:.6f}s")
        print(f"  Std Nodes: {row['std_nodes']:.1f}")


def main():
    """Main function to run all experiments and generate reports."""
    print("Starting N-Queens CSP Experiments...")
    print("This may take a while for larger board sizes...")
    
    # Run all experiments
    df = run_all_experiments()
    
    # Calculate statistics
    stats_df = calculate_statistics(df)
    
    # Save results to CSV
    output_file = "/home/julian-fernandez/Documents/Facultad/S6/ia1/tp5-csp/tp5-Nreinas.csv"
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Print statistics
    print("\n" + "="*60)
    print("EXPERIMENT RESULTS")
    print("="*60)
    for _, row in stats_df.iterrows():
        print(f"\n{row['algorithm']} - {row['n']}-Queens:")
        print(f"  Success Rate: {row['success_rate']:.1f}%")
        print(f"  Successful Runs: {row['successful_runs']}/{row['total_runs']}")
        if not pd.isna(row['avg_time']):
            print(f"  Avg Time: {row['avg_time']:.6f} ± {row['std_time']:.6f} seconds")
            print(f"  Avg Nodes: {row['avg_nodes']:.1f} ± {row['std_nodes']:.1f}")
    
    # Create visualizations
    images_dir = "/home/julian-fernandez/Documents/Facultad/S6/ia1/tp5-csp/images"
    create_boxplots(df, images_dir)
    
    # Compare with TP4
    compare_with_tp4(stats_df)
    
    print("\nAll experiments completed!")
    print(f"Results saved to: {output_file}")
    print(f"Plots saved to: {images_dir}")


if __name__ == "__main__":
    main()
