import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# === BASE PATH ===
base_path = '/home/dimi/ros2_ws/src/my_robot_pkg/data/'

ground_truth_path = os.path.join(base_path, 'ground_truth.csv')
noisy_path = os.path.join(base_path, 'noisy_data.csv')
ekf_path = os.path.join(base_path, 'ekf_data.csv')

# === LOAD DATA ===
gt = pd.read_csv(ground_truth_path)
noisy = pd.read_csv(noisy_path)
ekf = pd.read_csv(ekf_path)

# === EXTRACT X, Y ===
gt_x = gt['x'].to_numpy()
gt_y = gt['y'].to_numpy()

noisy_x = noisy['x'].to_numpy()
noisy_y = noisy['y'].to_numpy()

ekf_x = ekf['x'].to_numpy()
ekf_y = ekf['y'].to_numpy()
theta = -0.04
ekf_x = ekf_x * np.cos(theta) - ekf_y * np.sin(theta)
ekf_y = ekf_x * np.sin(theta) + ekf_y * np.cos(theta)
# =========================================================
# 🔵 1. GROUND TRUTH ONLY
# =========================================================
plt.figure()

plt.plot(gt_x, gt_y, linewidth=2)
plt.scatter(gt_x[0], gt_y[0], marker='o')
plt.scatter(gt_x[-1], gt_y[-1], marker='x')

plt.title('Ground Truth Trajectory')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'ground_truth.png'))
plt.close()


# =========================================================
# 🔴 2. NOISY ODOM ONLY
# =========================================================
plt.figure()

plt.plot(noisy_x, noisy_y, linestyle='--')
plt.scatter(noisy_x[0], noisy_y[0], marker='o')
plt.scatter(noisy_x[-1], noisy_y[-1], marker='x')

plt.title('Noisy Odometry Trajectory')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'noisy.png'))
plt.close()


# =========================================================
# 🟢 3. EKF ONLY
# =========================================================
plt.figure()

plt.plot(ekf_x, ekf_y)
plt.scatter(ekf_x[0], ekf_y[0], marker='o')
plt.scatter(ekf_x[-1], ekf_y[-1], marker='x')

plt.title('EKF Trajectory')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'ekf.png'))
plt.close()


# =========================================================
# 🟣 4. ALL TOGETHER
# =========================================================
plt.figure()

plt.plot(gt_x, gt_y, label='Ground Truth', linewidth=2)
plt.plot(noisy_x, noisy_y, linestyle='--', label='Noisy')
plt.plot(ekf_x, ekf_y, label='EKF')

plt.scatter(gt_x[0], gt_y[0], marker='o', label='Start')
plt.scatter(gt_x[-1], gt_y[-1], marker='x', label='End')

plt.title('All Trajectories')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.legend()
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'all_trajectories.png'))
plt.close()


# =========================================================
# 🟡 5. EKF vs NOISY
# =========================================================
plt.figure()

plt.plot(noisy_x, noisy_y, linestyle='--', label='Noisy')
plt.plot(ekf_x, ekf_y, label='EKF')

plt.title('EKF vs Noisy')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.legend()
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'ekf_vs_noisy.png'))
plt.close()


# =========================================================
# 🔵 6. EKF vs GROUND TRUTH
# =========================================================
plt.figure()

plt.plot(gt_x, gt_y, label='Ground Truth', linewidth=2)
plt.plot(ekf_x, ekf_y, label='EKF')

plt.title('EKF vs Ground Truth')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.legend()
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'ekf_vs_gt.png'))
plt.close()


# =========================================================
# 🔴 7. NOISY vs GROUND TRUTH
# =========================================================
plt.figure()

plt.plot(gt_x, gt_y, label='Ground Truth', linewidth=2)
plt.plot(noisy_x, noisy_y, linestyle='--', label='Noisy')

plt.title('Noisy vs Ground Truth')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.legend()
plt.axis('equal')
plt.grid()

plt.savefig(os.path.join(base_path, 'noisy_vs_gt.png'))
plt.close()


print("✅ All plots saved in:", base_path)