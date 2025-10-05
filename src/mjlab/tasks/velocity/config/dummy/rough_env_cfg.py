import math
from dataclasses import dataclass, field, replace

from mjlab.asset_zoo.robots.ccbr_dummy.dummy_constants import (
  DUMMY_ACTION_SCALE,
  DUMMY_ROBOT_CFG,
)
from mjlab.managers.manager_term_config import TerminationTermCfg as DoneTerm
from mjlab.managers.manager_term_config import term
from mjlab.tasks.velocity import mdp
from mjlab.tasks.velocity.velocity_env_cfg import (
  LocomotionVelocityEnvCfg,
  TerminationCfg,
)
from mjlab.utils.spec_config import ContactSensorCfg


@dataclass
class CCBRDummyTerminationCfg(TerminationCfg):
  time_out: DoneTerm = term(DoneTerm, func=mdp.time_out, time_out=True)
  fell_over: DoneTerm = term(
    DoneTerm, func=mdp.bad_orientation, params={"limit_angle": math.radians(70.0)}
  )
  bad_height: DoneTerm = term(DoneTerm, func=mdp.root_height_below_minimum, params={"minimum_height": 0.2})

@dataclass
class CCBRDummyRoughEnvCfg(LocomotionVelocityEnvCfg):

  def __post_init__(self):
    super().__post_init__()

    self.terminations = CCBRDummyTerminationCfg()

    # Foot contact sensors for dummy robot - using deepest collision geoms
    foot_contact_sensors = [
      ContactSensorCfg(
        name=f"{leg}_foot_ground_contact",
        geom1=f"leg_link_{geom_id}_collision",
        body2="terrain",
        num=1,
        data=("found",),
        reduce="netforce",
      )
      for leg, geom_id in [("FR", "9"), ("FL", "12"), ("RR", "10"), ("RL", "11")]
    ]
    dummy_cfg = replace(DUMMY_ROBOT_CFG, sensors=tuple(foot_contact_sensors))
    self.scene.entities = {"robot": dummy_cfg}

    self.actions.joint_pos.scale = DUMMY_ACTION_SCALE

    foot_names = ["FR", "FL", "RR", "RL"]
    sensor_names = [f"{name}_foot_ground_contact" for name in foot_names]
    geom_names = [f"leg_link_{geom_id}_collision" for geom_id in ["9", "12", "10", "11"]]

    self.rewards.air_time.params["sensor_names"] = sensor_names
    self.rewards.pose.params["std"] = {
      r"dof_[fb][rl]": 0.3,        # Hip joints
      r"dof_mid.*": 0.3,           # Thigh joints  
      r"dof_bottom.*": 0.6,        # Calf joints
    }

    self.rewards.action_rate_l2.weight = -0.001

    self.events.foot_friction.params["asset_cfg"].geom_names = geom_names

    self.viewer.body_name = "torso"
    self.viewer.distance = 1.5
    self.viewer.elevation = -10.0


@dataclass
class CCBRDummyRoughEnvCfg_PLAY(CCBRDummyRoughEnvCfg):
  def __post_init__(self):
    super().__post_init__()

    # Effectively infinite episode length.
    self.episode_length_s = int(1e9)

    if self.scene.terrain is not None:
      if self.scene.terrain.terrain_generator is not None:
        self.scene.terrain.terrain_generator.curriculum = False
        self.scene.terrain.terrain_generator.num_cols = 5
        self.scene.terrain.terrain_generator.num_rows = 5
        self.scene.terrain.terrain_generator.border_width = 10.0

    self.curriculum.command_vel = None
    self.commands.twist.ranges.lin_vel_x = (-3.0, 3.0)
    self.commands.twist.ranges.ang_vel_z = (-3.0, 3.0)
