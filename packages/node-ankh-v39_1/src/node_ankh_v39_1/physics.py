"""Optional physics validation synthesized from the ALANARA v39.1 adapter."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List

from .constants import RDOD_GATE
from .rdod import phi_smooth

try:
    from the_well.data import WellDataset

    HAS_THE_WELL = True
except Exception:
    HAS_THE_WELL = False
    WellDataset = None

try:
    import rclpy
    from std_msgs.msg import String

    HAS_ROS2 = True
except Exception:
    HAS_ROS2 = False
    rclpy = None
    String = None


@dataclass
class PhysicsCapabilities:
    """Advertise optional subsystem availability without hard failure."""

    thewell_available: bool
    ros2_available: bool


class PhysicsFoundation:
    """Optional physics-backed task validation."""

    def __init__(self, enable_thewell: bool = True) -> None:
        self.enable_thewell = enable_thewell and HAS_THE_WELL
        self.datasets: Dict[str, Any] = {}
        if self.enable_thewell:
            try:
                self.datasets["active_matter"] = WellDataset(
                    well_base_path="hf://datasets/polymathic-ai/",
                    well_dataset_name="active_matter",
                    well_split_name="train",
                )
            except Exception:
                self.enable_thewell = False
                self.datasets.clear()

    def capabilities(self) -> PhysicsCapabilities:
        return PhysicsCapabilities(
            thewell_available=self.enable_thewell,
            ros2_available=HAS_ROS2,
        )

    def predict_physics_rdod(self, trajectory: List[Dict[str, float]]) -> float:
        """Estimate motion quality from trajectory smoothness."""

        complexity = len(trajectory)
        smoothness = self._calculate_smoothness(trajectory)
        score = phi_smooth((smoothness ** 0.6) * ((1.0 - min(complexity / 100.0, 0.3)) ** 0.4))
        return max(0.0, min(1.0, score))

    def generate_linear_trajectory(self, task: Dict[str, Any], steps: int = 10) -> List[Dict[str, float]]:
        """Generate a simple trajectory used by validation and smoke tests."""

        start = task.get("start", {"x": 0.0, "y": 0.0, "z": 0.0})
        goal = task.get("goal", {"x": 1.0, "y": 1.0, "z": 1.0})
        points: List[Dict[str, float]] = []
        for index in range(steps + 1):
            t = index / steps
            points.append(
                {
                    "x": start["x"] + t * (goal["x"] - start["x"]),
                    "y": start["y"] + t * (goal["y"] - start["y"]),
                    "z": start["z"] + t * (goal["z"] - start["z"]),
                }
            )
        return points

    def plan_and_validate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and validate a task plan without performing external writes."""

        trajectory = self.generate_linear_trajectory(task)
        physics_rdod = self.predict_physics_rdod(trajectory)
        return {
            "trajectory": trajectory,
            "physics_rdod": physics_rdod,
            "execution_ready": physics_rdod >= RDOD_GATE,
        }

    def execute_trajectory(self, motor: Dict[str, Any]) -> Dict[str, Any]:
        """Publish to ROS2 if present; otherwise return a local simulation result."""

        if HAS_ROS2 and rclpy is not None and String is not None:
            rclpy.init()
            node = rclpy.create_node("node_ankh_v39_1_exec")
            publisher = node.create_publisher(String, "/robot/trajectory", 10)
            publisher.publish(String(data=str(motor)))
            rclpy.shutdown()
            return {"status": "PUBLISHED", "ros2": True}
        return {
            "status": "SIMULATED",
            "ros2": False,
            "physics_rdod": self.predict_physics_rdod([motor]) if {"x", "y", "z"} <= set(motor.keys()) else 0.95,
        }

    def _calculate_smoothness(self, trajectory: List[Dict[str, float]]) -> float:
        if len(trajectory) < 3:
            return 1.0

        accelerations: List[float] = []
        for index in range(1, len(trajectory)):
            dx = trajectory[index].get("x", 0.0) - trajectory[index - 1].get("x", 0.0)
            dy = trajectory[index].get("y", 0.0) - trajectory[index - 1].get("y", 0.0)
            dz = trajectory[index].get("z", 0.0) - trajectory[index - 1].get("z", 0.0)
            accelerations.append(math.sqrt(dx ** 2 + dy ** 2 + dz ** 2))

        if not accelerations:
            return 1.0

        mean = sum(accelerations) / len(accelerations)
        variance = sum((value - mean) ** 2 for value in accelerations) / len(accelerations)
        return 1.0 / (1.0 + math.sqrt(variance))
