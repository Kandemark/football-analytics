# analysis/heatmap.py

import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

def draw_pitch(ax=None):
    if ax is None:
        ax = plt.gca()

    ax.set_xlim(0, 1280)
    ax.set_ylim(720, 0)
    ax.set_facecolor("green")

    # Outline
    ax.plot([0, 0, 1280, 1280, 0], [0, 720, 720, 0, 0], color="white")

    # Center line
    ax.axvline(1280 / 2, color="white")

    # Center circle
    center = (1280 / 2, 720 / 2)
    circle = plt.Circle(center, 90, color="white", fill=False)
    ax.add_patch(circle)

    # Penalty areas
    ax.add_patch(plt.Rectangle((0, 270), 120, 180, edgecolor='white', fill=False))
    ax.add_patch(plt.Rectangle((1160, 270), 120, 180, edgecolor='white', fill=False))

def plot_player_heatmap(track_history, player_id):
    if player_id not in track_history:
        print(f"❌ Player ID {player_id} not found.")
        return

    positions = np.array(track_history[player_id])
    x = positions[:, 0]
    y = positions[:, 1]

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    draw_pitch(ax)

    # Plot heatmap
    plt.hexbin(x, y, gridsize=40, cmap='hot', alpha=0.6)
    plt.colorbar(label='Frequency')
    plt.title(f"Heatmap: Player ID {player_id}")
    plt.savefig(f"output/heatmap_player_{player_id}.png")
    plt.close()

def generate_heatmap(track_history, frame_height, frame_width, teams=None):
    os.makedirs('output', exist_ok=True)

    team_points = {}

    for track_id, points in track_history.items():
        team = teams.get(track_id, 'Unknown') if teams else 'Unknown'
        if team not in team_points:
            team_points[team] = []
        team_points[team].extend(points)

    for team, points in team_points.items():
        heatmap = np.zeros((frame_height, frame_width), dtype=np.float32)

        for x, y in points:
            if 0 <= int(y) < frame_height and 0 <= int(x) < frame_width:
                heatmap[int(y), int(x)] += 1

        heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=25, sigmaY=25)
        heatmap = np.minimum(heatmap / heatmap.max(), 1.0)

        plt.figure(figsize=(10, 6))
        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.axis('off')
        plt.title(f'Heatmap - Team {team}')
        plt.savefig(f'output/heatmap_{team.lower()}.png', bbox_inches='tight', pad_inches=0)
        plt.close()