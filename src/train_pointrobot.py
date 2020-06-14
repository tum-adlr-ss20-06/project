import os
import sys
import numpy as np
import tensorflow as tf

import gym
import gym_pointrobo

from tf2rl.algos.ddpg import DDPG

from hwr.cae.cae import CAE
from hwr.training.pointrobot_trainer import PointrobotTrainer


parser = PointrobotTrainer.get_argument()
parser = DDPG.get_argument(parser)
parser.add_argument('--env-name', type=str, default="pointrobo-v0")
parser.set_defaults(batch_size=100)
parser.set_defaults(n_warmup=1000)
parser.set_defaults(update_interval=2)

args = parser.parse_args()

args.max_steps = 1e6
args.test_interval = 50

#Initialize the environment
env = gym.make(args.env_name)
test_env = gym.make(args.env_name)

policy = DDPG(
    state_shape=env.observation_space.shape,
    action_dim=env.action_space.high.size,
    gpu=args.gpu,
    memory_capacity=args.memory_capacity,
    update_interval=args.update_interval,
    max_action=env.action_space.high[0],
    batch_size=args.batch_size,
    n_warmup=args.n_warmup)
trainer = PointrobotTrainer(policy, env, args, test_env=test_env)

print('-' * 5 + "Let's start training" + '-' * 5)

trainer()