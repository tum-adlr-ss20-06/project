import os
import sys
import numpy as np
import tensorflow as tf
import glob

import gym
import gym_pointrobo

from hwr.agents.pointrobo_ddpg import DDPG

from hwr.cae.cae import CAE
from hwr.training.pointrobot_trainer import PointrobotTrainer


train_from_scratch = True

parser = PointrobotTrainer.get_argument()
parser = DDPG.get_argument(parser)
parser.add_argument('--env-name', type=str, default="pointrobo-v0")
parser.set_defaults(batch_size=100)
parser.set_defaults(n_warmup=1000)
parser.set_defaults(update_interval=10)

args = parser.parse_args()

# workspace args:
args.num_obj_max = 0
max_goal_dist = 4
# training args:
args.max_steps = 5e5
args.test_interval = 10000
args.episode_max_steps = 5
args.test_episodes = 100
args.save_test_path_sep = False
args.save_test_movie = False
args.show_progress = True
# agent args:
args.max_grad = 1
args.memory_capacity = 1e5
lr_actor = 1e-4
lr_critic = 1e-4

if train_from_scratch:
    # deleting the previous checkpoints:
    ckp_files = glob.glob('../models/agents/*')
    for f in ckp_files:
        os.remove(f)
    print('-' * 5 + 'TRAINING FROM SCRATCH!! --> DELETED CHECKPOINTS!' + '-' * 5)

#Initialize the environment
env = gym.make(
    args.env_name,
    goal_reward=10,
    collision_reward=-1,
    step_reward=-0.05,
    buffer_size=1000,
    grid_size=32,
    num_obj_max=args.num_obj_max,
    obj_size_avg=args.obj_size_avg,
    max_goal_dist=max_goal_dist,
    )
test_env = gym.make(
    args.env_name,
    goal_reward=10,
    collision_reward=-1,
    step_reward=-0.05,
    buffer_size=1000,
    grid_size=32,
    num_obj_max=args.num_obj_max,
    obj_size_avg=args.obj_size_avg,
    max_goal_dist=max_goal_dist,
    )

# initialize the agent:
policy = DDPG(
    state_shape=env.observation_space.shape,
    action_dim=env.action_space.high.size,
    gpu=args.gpu,
    memory_capacity=args.memory_capacity,
    update_interval=args.update_interval,
    #max_action=env.action_space.high[0], #max action =1
    lr_actor=lr_actor, #0.001 hyperparamter learning rate actor network
    lr_critic=lr_critic, #hyperparamter learning rate critic network
    max_grad=args.max_grad,
    actor_units=[400, 300],
    critic_units=[400, 300],
    batch_size=args.batch_size,
    n_warmup=args.n_warmup)

trainer = PointrobotTrainer(policy, env, args, test_env=test_env)

print('-' * 5 + "Let's start training" + '-' * 5)

trainer()

print('-' * 5 + "We succeeeeeded!!!!!!!!!!!!!" + '-' * 5)