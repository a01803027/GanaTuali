import pandas as pd
import glob

# Step 1: Load all sales files (update path as needed)
file_paths = glob.glob("Databases/*.csv")  # Adjust to your local directory

# Step 2: Define standard column names for consistency
standard_columns = {
    'Venta USD': 'Sales_USD',
    'Venta Cajas': 'Sales_Boxes',
    'ID Cliente': 'Client_ID',
    'Tamaño de Cliente': 'Client_Size',
    'Categoría': 'Category',
    'Producto': 'Product',
    'Año': 'Year',
    'Mes': 'Month'
    # Add more if your columns vary
}

all_data = []

for file in file_paths:
    df = pd.read_csv(file, encoding='ISO-8859-1')  # Change encoding if needed

    # Step 3: Rename columns to standard format
    df.rename(columns=standard_columns, inplace=True)

    # Step 4: Drop duplicates and rows with nulls in critical fields
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['Client_ID', 'Product', 'Sales_USD'], inplace=True)

    # Step 5: Add or correct Year and Month if necessary
    if 'Year' not in df.columns or 'Month' not in df.columns:
        # Attempt to infer from filename if missing
        # (Assumes file name like "Ventas 2022 ENE-MAR")
        print(f"Warning: Missing Year/Month in {file}")
    
    all_data.append(df)

# Step 6: Merge all data into a single DataFrame
merged_df = pd.concat(all_data, ignore_index=True)

# Step 7: Convert date fields to standard format if needed
# If you have a 'Fecha' column, parse it:
# merged_df['Fecha'] = pd.to_datetime(merged_df['Fecha'], errors='coerce')

# Step 8: Sort by Year and Month
merged_df['Year'] = merged_df['Year'].astype(int)
merged_df['Month'] = pd.Categorical(merged_df['Month'], categories=[
    'Enero','Febrero','Marzo','Abril','Mayo','Junio',
    'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'
], ordered=True)
merged_df.sort_values(['Year', 'Month'], inplace=True)

# Step 9: Export cleaned file
merged_df.to_csv("Cleaned_Sales_2022_2023.csv", index=False)

print("✅ Cleaning complete. Output file: Cleaned_Sales_2022_2023.csv")
