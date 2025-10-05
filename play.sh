# MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run play \
#   --task Mjlab-Velocity-Flat-Unitree-Go1-Play \
#   --checkpoint-file logs/rsl_rl/go1_velocity/2025-09-30_22-12-13/model_150.pt \
#   --viewer viser \
  # --export \
  # --motion-file not-a-real-file.npz \

  # MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run play \
  # --task Mjlab-Velocity-Flat-CCBR-Dummy-Play \
  # --checkpoint-file logs/rsl_rl/dummy_velocity/2025-10-02_12-39-18/model_0.pt \
  # --viewer viser \

  MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 mjpython -m mjlab.scripts.play \
  --task Mjlab-Velocity-Flat-CCBR-Dummy-Play \
  --checkpoint-file logs/rsl_rl/dummy_velocity/2025-10-02_14-52-54/model_300.pt \
  --viewer native \
