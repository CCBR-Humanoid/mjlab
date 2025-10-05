"""CCBR Dummy robot constants."""

from pathlib import Path

import mujoco

from mjlab import MJLAB_SRC_PATH
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.actuator import ElectricActuator, reflected_inertia
from mjlab.utils.os import update_assets
from mjlab.utils.spec_config import ActuatorCfg, CollisionCfg

##
# MJCF and assets.
##

DUMMY_XML: Path = (
  MJLAB_SRC_PATH / "asset_zoo" / "robots" / "ccbr_dummy" / "xmls" / "dummy.xml"
)
assert DUMMY_XML.exists()


def get_assets(meshdir: str) -> dict[str, bytes]:
  assets: dict[str, bytes] = {}
  update_assets(assets, DUMMY_XML.parent / "assets", meshdir)
  return assets


def get_spec() -> mujoco.MjSpec:
  spec = mujoco.MjSpec.from_file(str(DUMMY_XML))
  spec.assets = get_assets(spec.meshdir)
  return spec


##
# Actuator config.
##

# Rotor inertia - using same as Go1 for consistency
ROTOR_INERTIA = 0.000111842

# Gearbox ratios - using same as Go1 for consistency
HIP_GEAR_RATIO = 6
KNEE_GEAR_RATIO = HIP_GEAR_RATIO * 1.5

# Actuator specifications based on dummy.xml classes
# robstride_03: effort_limit=60.0, ctrlrange=-60.0 60.0
# robstride_02: effort_limit=17.0, ctrlrange=-17.0 17.0
HIP_ACTUATOR = ElectricActuator(
  reflected_inertia=reflected_inertia(ROTOR_INERTIA, HIP_GEAR_RATIO),
  velocity_limit=30.1,  # Estimated based on typical servo specs
  effort_limit=60.0,    # From robstride_03 class
)
KNEE_ACTUATOR = ElectricActuator(
  reflected_inertia=reflected_inertia(ROTOR_INERTIA, KNEE_GEAR_RATIO),
  velocity_limit=20.06,  # Estimated based on typical servo specs
  effort_limit=17.0,     # From robstride_02 class
)

NATURAL_FREQ = 10 * 2.0 * 3.1415926535  # 10Hz
DAMPING_RATIO = 2.0

STIFFNESS_HIP = HIP_ACTUATOR.reflected_inertia * NATURAL_FREQ**2
DAMPING_HIP = 2 * DAMPING_RATIO * HIP_ACTUATOR.reflected_inertia * NATURAL_FREQ


STIFFNESS_KNEE = KNEE_ACTUATOR.reflected_inertia * NATURAL_FREQ**2
DAMPING_KNEE = 2 * DAMPING_RATIO * KNEE_ACTUATOR.reflected_inertia * NATURAL_FREQ

# Overriding this because I suspect the link inertias are extremely non-negligible. Check this
STIFFNESS_HIP *= 2.0
STIFFNESS_KNEE *= 2.0

DAMPING_HIP *= 3.0
DAMPING_KNEE *= 3.0

# Actuator configs based on dummy.xml joint structure
# Using regex patterns to match joint groups:
# - "dof_[fb][rl]" matches: dof_fr, dof_br, dof_fl, dof_bl (hip joints)
# - "dof_mid.*" matches: dof_mid, dof_mid_2, dof_mid_3, dof_mid_4 (thigh joints)
# - "dof_bottom.*" matches: dof_bottom, dof_bottom_2, dof_bottom_3, dof_bottom_4 (calf joints)
DUMMY_HIP_ACTUATOR_CFG = ActuatorCfg(
  joint_names_expr=["dof_[fb][rl]", "dof_mid.*"],
  effort_limit=HIP_ACTUATOR.effort_limit,
  stiffness=STIFFNESS_HIP,
  damping=DAMPING_HIP,
  armature=HIP_ACTUATOR.reflected_inertia,
)
DUMMY_KNEE_ACTUATOR_CFG = ActuatorCfg(
  joint_names_expr=["dof_bottom.*"],
  effort_limit=KNEE_ACTUATOR.effort_limit,
  stiffness=STIFFNESS_KNEE,
  damping=DAMPING_KNEE,
  armature=KNEE_ACTUATOR.reflected_inertia,
)

##
# Keyframes.
##


INIT_STATE = EntityCfg.InitialStateCfg(
  pos=(0.0, 0.0, 0.7),  # From dummy.xml base position
  joint_pos={
    "dof_[fb][rl]": 0.0,    # All hip joints (dof_fr, dof_br, dof_fl, dof_bl)
    "dof_mid.*": 0.0,       # All thigh joints (dof_mid, dof_mid_2, dof_mid_3, dof_mid_4)
    "dof_bottom.*": 0.0,    # All calf joints (dof_bottom, dof_bottom_2, dof_bottom_3, dof_bottom_4)
  },
  joint_vel={".*": 0.0},
)

##
# Collision config.
##

# Based on dummy.xml collision geoms - feet are at the deepest leaf nodes
# The deepest collision geoms are: leg_link_9_collision, leg_link_10_collision, 
# leg_link_11_collision, leg_link_12_collision (corresponding to the 4 legs)
_foot_regex = "leg_link_(9|10|11|12)_collision$"

# This disables all collisions except the feet.
# Furthermore, feet self collisions are disabled.
FEET_ONLY_COLLISION = CollisionCfg(
  geom_names_expr=[_foot_regex],
  contype=0,
  conaffinity=1,
  condim=3,
  priority=1,
  friction=(0.6,),
  solimp=(0.9, 0.95, 0.023),
)

# This enables all collisions, excluding self collisions.
# Foot collisions are given custom condim, friction and solimp.
FULL_COLLISION = CollisionCfg(
  geom_names_expr=[".*_collision"],
  condim={_foot_regex: 3, ".*_collision": 1},
  priority={_foot_regex: 1},
  friction={_foot_regex: (0.6,)},
  solimp={_foot_regex: (0.9, 0.95, 0.023)},
  contype=1,
  conaffinity=0,
)

##
# Final config.
##

DUMMY_ARTICULATION = EntityArticulationInfoCfg(
  actuators=(
    DUMMY_HIP_ACTUATOR_CFG,
    DUMMY_KNEE_ACTUATOR_CFG,
  ),
  soft_joint_pos_limit_factor=0.9,
)

DUMMY_ROBOT_CFG = EntityCfg(
  init_state=INIT_STATE,
  collisions=(FULL_COLLISION,),
  spec_fn=get_spec,
  articulation=DUMMY_ARTICULATION,
)

DUMMY_ACTION_SCALE: dict[str, float] = {}
for a in DUMMY_ARTICULATION.actuators:
  e = a.effort_limit
  s = a.stiffness
  names = a.joint_names_expr
  if not isinstance(e, dict):
    e_dict = {n: e for n in names}
  else:
    e_dict = e
  if not isinstance(s, dict):
    s_dict = {n: s for n in names}
  else:
    s_dict = s
  for n in names:
    if n in e_dict and n in s_dict and s_dict[n]:
      DUMMY_ACTION_SCALE[n] = 0.25 * e_dict[n] / s_dict[n]
