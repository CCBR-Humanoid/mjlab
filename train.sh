# MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run train \
#   Mjlab-Velocity-Flat-Unitree-Go1 \
#   --env.scene.num-envs 1024 \
#   --device cpu \
#   --agent.logger tensorboard


MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run train \
  Mjlab-Velocity-Flat-CCBR-Dummy \
  --env.scene.num-envs 4096 \
  --agent.logger tensorboard \
  --agent.load-checkpoint logs/rsl_rl/dummy_velocity/2025-10-09_03-19-08/model_9999.pt\
  # --device cpu \

# MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run train \
#   Mjlab-Velocity-Flat-CCBR-Dummy \
#   --env.scene.num-envs 1024 \
#   --device cpu \
#   --agent.logger tensorboard \
#   --agent.load-checkpoint logs/rsl_rl/dummy_velocity/2025-10-02_13-54-03/model_50.pt \

# MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 uv run train \
#   Mjlab-Velocity-Flat-CCBR-Dummy \
#   --env.scene.num-envs 2 \
#   --device cpu \
#   --agent.logger tensorboard \
#   --agent.load-checkpoint logs/rsl_rl/dummy_velocity/2025-10-02_13-54-03/model_50.pt \
#   --video True \
#   --video-interval 50 \
