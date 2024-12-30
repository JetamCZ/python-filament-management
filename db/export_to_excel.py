import pandas as pd


def export_to_excel(output_filename, spools, filaments):
    spools_data = [
        {
            "ID": spool.id,
            "Filament": spool.filament.id,
            "Weight (without spool)": spool.original_filament_weight,
            "Total weight": spool.original_spool_weight,
            "Last weight": spool.last_weight
        }
        for spool in spools
    ]

    spools_data_df = pd.DataFrame(spools_data)

    filaments_data = [
        {
            "ID": filament.id,
            "Name": filament.custom_name,
            "Manufacturer": filament.manufacturer,
            "Type": filament.type,
            "Color": filament.color_name,
        }
        for filament in filaments
    ]

    filaments_data_df = pd.DataFrame(filaments_data)

    with pd.ExcelWriter(output_filename) as writer:
        spools_data_df.to_excel(writer, sheet_name="Spools", index=False)
        filaments_data_df.to_excel(writer, sheet_name="Filaments", index=False)

    print(f"Data has been saved to {output_filename}")
