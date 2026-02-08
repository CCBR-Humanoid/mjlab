MUJOCO_GL=glfw MJLAB_WARP_QUIET=1 mjpython src/mjlab/scripts/play.py \
  Mjlab-Velocity-Flat-CCBR-Leo \
  --checkpoint-file model_5000.pt \
  --viewer native
  # --export \
  # --motion-file not-a-real-file.npz \
