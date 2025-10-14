import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class PerformanceAnalyzer:
    """
    Clase para analizar y visualizar la performance de los agentes.
    """
    
    def __init__(self, csv_file_path, reward_per_clean=10, penalty_per_action=1):
        """
        Inicializa el analizador de performance.
        
        Args:
            csv_file_path: Ruta al archivo CSV con los datos experimentales
            reward_per_clean: Puntos por cada celda limpiada (default: 10)
            penalty_per_action: Penalización por cada acción (default: 1)
        """
        self.csv_file = csv_file_path
        self.reward_per_clean = reward_per_clean
        self.penalty_per_action = penalty_per_action
        self.df = None
        self.use_efficiency_metric = False
        
    def load_data(self):
        """Carga los datos del CSV."""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Datos cargados: {len(self.df)} filas")
            print(f"Columnas: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return False
    
    def calculate_performance(self, cleaned_cells, total_actions):
        """
        Calcula la performance según la métrica:
        Performance = (Celdas limpiadas × reward) - (Acciones × penalización)
        
        Args:
            cleaned_cells: Número de celdas limpiadas
            total_actions: Número total de acciones realizadas
            
        Returns:
            Performance calculada
        """
        return (cleaned_cells * self.reward_per_clean) - (total_actions * self.penalty_per_action)
    
    def add_performance_column(self):
        """Agrega una columna de performance calculada al DataFrame."""
        if self.df is None:
            print("Error: Primero debes cargar los datos")
            return False
        
        # Calcular la suciedad realmente limpiada
        self.df['dirt_cleaned'] = self.df['initial_dirt'] - self.df['final_dirt']
        
        # Verificar si hay datos de limpieza
        total_cleaned = self.df['dirt_cleaned'].sum()
        
        if total_cleaned == 0:
            print("\n⚠️  ADVERTENCIA: No hay datos de limpieza en el CSV (dirt_cleaned = 0)")
            print("    Usando métrica alternativa basada en eficiencia de acciones")
            self.use_efficiency_metric = True
            
            # Métrica alternativa: Penalizar menos las acciones
            # Cuantas menos acciones, mejor performance
            # Normalizamos para que el mejor agente tenga valores positivos
            max_actions = self.df['actions_taken'].max()
            self.df['performance_calculated'] = self.df['actions_taken'].apply(
                lambda x: (max_actions - x) / 10  # Escalamos para que sea visible
            )
            
            print(f"\n  Nueva métrica: Performance = (max_actions - actions_taken) / 10")
            print(f"  Donde max_actions = {max_actions}")
            print(f"  Valores más altos = menos acciones = mejor eficiencia")
        else:
            # Calcular la performance normal usando la suciedad limpiada
            self.df['performance_calculated'] = self.df.apply(
                lambda row: self.calculate_performance(row['dirt_cleaned'], row['actions_taken']),
                axis=1
            )
            
            print(f"\nPerformance calculada usando:")
            print(f"  Recompensa por limpieza: +{self.reward_per_clean} puntos")
            print(f"  Penalización por acción: -{self.penalty_per_action} punto")
            print(f"  Fórmula: Performance = (dirt_cleaned × {self.reward_per_clean}) - (actions_taken × {self.penalty_per_action})")
            print(f"  donde dirt_cleaned = initial_dirt - final_dirt")
        
        return True
    
    def plot_performance_by_dirt_rate(self, save_path=None):
        """
        Genera un gráfico de performance promedio por dirt_rate para cada agente.
        
        Args:
            save_path: Ruta donde guardar el gráfico (opcional)
        """
        if self.df is None:
            print("Error: Primero debes cargar los datos")
            return
        
        # Agrupar por agente y dirt_rate, calcular promedio de performance
        grouped = self.df.groupby(['agent_name', 'dirt_rate'])['performance_calculated'].agg(['mean', 'std']).reset_index()
        
        plt.figure(figsize=(10, 6))
        
        # Graficar cada tipo de agente
        for agent_name in grouped['agent_name'].unique():
            agent_data = grouped[grouped['agent_name'] == agent_name]
            
            # Línea principal
            plt.plot(agent_data['dirt_rate'], agent_data['mean'], 
                    marker='o', label=agent_name, linewidth=2, markersize=8)
            
            # Rango de variación (desviación estándar)
            plt.fill_between(agent_data['dirt_rate'], 
                           agent_data['mean'] - agent_data['std'],
                           agent_data['mean'] + agent_data['std'],
                           alpha=0.2)
        
        plt.xlabel('Dirt rate', fontsize=12)
        plt.ylabel('Performance', fontsize=12)
        plt.title('Performance promedio con rango de variación', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado en: {save_path}")
        
        plt.show()
    
    def plot_distribution_boxplot(self, save_path=None):
        """
        Genera un boxplot de la distribución de performance por agente.
        
        Args:
            save_path: Ruta donde guardar el gráfico (opcional)
        """
        if self.df is None:
            print("Error: Primero debes cargar los datos")
            return
        
        plt.figure(figsize=(10, 6))
        
        # Preparar datos para boxplot
        agents = self.df['agent_name'].unique()
        performance_data = [self.df[self.df['agent_name'] == agent]['performance_calculated'].values 
                           for agent in agents]
        
        # Crear boxplot
        bp = plt.boxplot(performance_data, tick_labels=agents, patch_artist=True)
        
        # Personalizar colores
        colors = ['#ff9999', '#66b3ff']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        plt.ylabel('Performance', fontsize=12)
        plt.xlabel('Agente', fontsize=12)
        plt.title('Distribución de Performance por Agente', fontsize=14)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado en: {save_path}")
        
        plt.show()
    
    def plot_comparison(self, save_path=None):
        """
        Genera múltiples gráficos de comparación.
        
        Args:
            save_path: Ruta base donde guardar los gráficos (opcional)
        """
        if self.df is None:
            print("Error: Primero debes cargar los datos")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Performance por dirt_rate
        for agent_name in self.df['agent_name'].unique():
            agent_data = self.df[self.df['agent_name'] == agent_name].groupby('dirt_rate')['performance_calculated'].mean()
            axes[0, 0].plot(agent_data.index, agent_data.values, marker='o', label=agent_name, linewidth=2)
        axes[0, 0].set_xlabel('Dirt Rate')
        axes[0, 0].set_ylabel('Performance Promedio')
        axes[0, 0].set_title('Performance vs Dirt Rate')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Celdas limpiadas vs Acciones
        for agent_name in self.df['agent_name'].unique():
            agent_data = self.df[self.df['agent_name'] == agent_name]
            axes[0, 1].scatter(agent_data['actions_taken'], agent_data['cells_cleaned'], 
                             alpha=0.5, label=agent_name)
        axes[0, 1].set_xlabel('Acciones')
        axes[0, 1].set_ylabel('Celdas Limpiadas')
        axes[0, 1].set_title('Eficiencia: Celdas Limpiadas vs Acciones')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Distribución de performance
        for agent_name in self.df['agent_name'].unique():
            agent_data = self.df[self.df['agent_name'] == agent_name]['performance_calculated']
            axes[1, 0].hist(agent_data, alpha=0.5, bins=20, label=agent_name)
        axes[1, 0].set_xlabel('Performance')
        axes[1, 0].set_ylabel('Frecuencia')
        axes[1, 0].set_title('Distribución de Performance')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Boxplot de performance por agente
        performance_by_agent = [self.df[self.df['agent_name'] == agent]['performance_calculated'].values 
                               for agent in self.df['agent_name'].unique()]
        axes[1, 1].boxplot(performance_by_agent, labels=self.df['agent_name'].unique())
        axes[1, 1].set_ylabel('Performance')
        axes[1, 1].set_title('Distribución de Performance por Agente')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            base, ext = os.path.splitext(save_path)
            comparison_path = f"{base}_comparison{ext}"
            plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico de comparación guardado en: {comparison_path}")
        
        plt.show()
    
    def print_statistics(self):
        """Imprime estadísticas descriptivas de la performance."""
        if self.df is None:
            print("Error: Primero debes cargar los datos")
            return
        
        print("\n" + "="*50)
        print("ESTADÍSTICAS DE PERFORMANCE")
        print("="*50)
        
        for agent_name in self.df['agent_name'].unique():
            agent_data = self.df[self.df['agent_name'] == agent_name]['performance_calculated']
            print(f"\n{agent_name}:")
            print(f"  Media: {agent_data.mean():.2f}")
            print(f"  Mediana: {agent_data.median():.2f}")
            print(f"  Desviación estándar: {agent_data.std():.2f}")
            print(f"  Mínimo: {agent_data.min():.2f}")
            print(f"  Máximo: {agent_data.max():.2f}")


def main():
    """Función principal para ejecutar el análisis."""
    # Ruta al archivo CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(os.path.dirname(script_dir), 'vacuum_experiments.csv')
    
    print(f"Buscando CSV en: {csv_path}")
    
    # Crear analizador con métricas personalizadas
    analyzer = PerformanceAnalyzer(
        csv_file_path=csv_path,
        reward_per_clean=10,  # 10 puntos por celda limpiada
        penalty_per_action=1   # 1 punto de penalización por acción
    )
    
    # Cargar datos
    if not analyzer.load_data():
        return
    
    # Calcular performance
    if not analyzer.add_performance_column():
        return
    
    # Mostrar estadísticas
    analyzer.print_statistics()
    
    # Generar gráficos
    images_dir = os.path.join(os.path.dirname(script_dir), 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("GENERANDO GRÁFICOS")
    print("="*60)
    
    print("\n1. Generando gráfico de Performance vs Dirt Rate...")
    analyzer.plot_performance_by_dirt_rate(
        save_path=os.path.join(images_dir, 'performance_vs_dirt_rate.png')
    )
    
    print("\n2. Generando gráfico de Distribución de Performance...")
    analyzer.plot_distribution_boxplot(
        save_path=os.path.join(images_dir, 'performance_distribution.png')
    )
    
    print("\n" + "="*60)
    print("✓ Gráficos generados exitosamente en:")
    print(f"  - {os.path.join(images_dir, 'performance_vs_dirt_rate.png')}")
    print(f"  - {os.path.join(images_dir, 'performance_distribution.png')}")
    print("="*60)


if __name__ == "__main__":
    main()
