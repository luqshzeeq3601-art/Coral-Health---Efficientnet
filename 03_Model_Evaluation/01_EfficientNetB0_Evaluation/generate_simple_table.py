import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import os

# Define paths
csv_path = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\02_Deployment_Phase\classification_report.csv'
output_path = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\02_Deployment_Phase\classification_report_simple_table.png'

def generate_table():
    # Load the CSV
    df = pd.read_csv(csv_path, index_col=0)
    
    # Rename columns and index if necessary (CSV has an empty first column name)
    df.index.name = 'Class'
    
    # Format numeric values to 4 decimal places, keeping support as integer if possible
    for col in df.columns:
        if col != 'support':
            df[col] = df[col].map(lambda x: f'{x:.4f}' if isinstance(x, (float, int)) else x)
        else:
            df[col] = df[col].map(lambda x: int(x) if isinstance(x, (float, int)) else x)

    # Reset index to make it a column for the table
    df_reset = df.reset_index()

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    ax.axis('tight')

    # Create the table
    table = ax.table(cellText=df_reset.values, 
                     colLabels=df_reset.columns, 
                     cellLoc='center', 
                     loc='center')

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    # Make header bold and highlight first column
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
        if col == 0:
            cell.set_text_props(weight='bold')

    plt.title('Classification Report - Deployment Audit', fontsize=14, weight='bold', pad=20)
    
    # Save the figure
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"Successfully generated simple table image at: {output_path}")

if __name__ == "__main__":
    if os.path.exists(csv_path):
        generate_table()
    else:
        print(f"Error: CSV file not found at {csv_path}")
