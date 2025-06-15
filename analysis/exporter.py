import csv
import os

def save_tracking_data(track_history, output_path='output/tracking_data.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Player ID', 'X', 'Y'])

        for player_id, points in track_history.items():
            for x, y in points:
                writer.writerow([player_id, x, y])

    print(f"✅ Player position data saved to {output_path}")


def export_summary_stats(distances, avg_speeds, max_speeds, teams=None, output_path='output/player_summary.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Player ID', 'Team', 'Total Distance (m)', 'Average Speed (m/s)', 'Max Speed (m/s)'])

        all_ids = sorted(set(distances.keys()) | set(avg_speeds.keys()) | set(max_speeds.keys()))

        for player_id in all_ids:
            team = teams.get(player_id, "Unknown") if teams else "Unknown"
            distance = round(distances.get(player_id, 0), 2)
            avg_speed = round(avg_speeds.get(player_id, 0), 2)
            max_speed = round(max_speeds.get(player_id, 0), 2)

            writer.writerow([player_id, team, distance, avg_speed, max_speed])

    print(f"✅ Summary stats saved to {output_path}")
