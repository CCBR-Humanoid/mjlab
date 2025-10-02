import gymnasium as gym

gym.register(
  id="Mjlab-Velocity-Rough-CCBR-Dummy",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.rough_env_cfg:CCBRDummyRoughEnvCfg",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:CCBRDummyPPORunnerCfg",
  },
)

gym.register(
  id="Mjlab-Velocity-Rough-CCBR-Dummy-Play",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.rough_env_cfg:CCBRDummyRoughEnvCfg_PLAY",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:CCBRDummyPPORunnerCfg",
  },
)

gym.register(
  id="Mjlab-Velocity-Flat-CCBR-Dummy",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.flat_env_cfg:CCBRDummyFlatEnvCfg",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:CCBRDummyPPORunnerCfg",
  },
)

gym.register(
  id="Mjlab-Velocity-Flat-CCBR-Dummy-Play",
  entry_point="mjlab.envs:ManagerBasedRlEnv",
  disable_env_checker=True,
  kwargs={
    "env_cfg_entry_point": f"{__name__}.flat_env_cfg:CCBRDummyFlatEnvCfg_PLAY",
    "rl_cfg_entry_point": f"{__name__}.rl_cfg:CCBRDummyPPORunnerCfg",
  },
)
