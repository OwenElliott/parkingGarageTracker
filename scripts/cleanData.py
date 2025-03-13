import polars as pl

# Read the CSV file into a Polars DataFrame
df = pl.read_csv("data/raw/parking_status.csv", separator="\n", has_header=False, new_columns=["raw_data"])

# Define a function to parse each row
def parse_row(row):
    parts = row.split(",")
    # Ensure there are enough parts in the row
    if len(parts) < 8:
        print(f"Skipping malformed row: {row}")
        return None

    try:
        date_time = parts[0].strip()
        # Handle 'FULL' by replacing it with '100'
        south = parts[2].replace("%", "").strip()
        south = "100" if south == "Full" else south

        west = parts[4].replace("%", "").strip()
        west = "100" if west == "Full" else west

        north = parts[6].replace("%", "").strip()
        north = "100" if north == "Full" else north

        south_campus = parts[8].replace("%", "").strip()
        south_campus = "100" if south_campus == "Full" else south_campus

        return {
            "dateTime": date_time,
            "south%": int(south),
            "west%": int(west),
            "north%": int(north),
            "southcampus%": int(south_campus)
        }
    except (ValueError, IndexError) as e:
        print(f"Error parsing row: {row}. Error: {e}")
        return None
# Apply the parsing function to each row
parsed_data = [parse_row(row) for row in df["raw_data"]]
# Filter out None values (invalid rows)
parsed_data = [row for row in parsed_data if row is not None]
# Create a new DataFrame from the parsed data
df_parsed = pl.DataFrame(parsed_data)
df = df.with_columns(pl.col("dateTime").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M"))
# Optionally, write the DataFrame to a new CSV file
df_parsed.write_csv("data/transformed/transformed_parking_status.csv")