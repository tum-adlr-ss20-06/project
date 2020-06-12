import os
import sys
import numpy as np
import tensorflow as tf

import gym
import gym_pointrobo

from tf2rl.algos.ddpg import DDPG

from hwr.cae.cae import CAE
from hwr.training.pointrobot_trainer import PointrobotTrainer


def test_pointrobot_trainer_init():
    print('-' * 5 + 'test_pointrobot_trainer_init' + '-' * 5)

    parser = PointrobotTrainer.get_argument()
    parser = DDPG.get_argument(parser)
    parser.add_argument('--env-name', type=str, default="pointrobo-v0")
    args = parser.parse_args()

    #Initialize the environment
    env = gym.make(args.env_name)
    test_env = gym.make(args.env_name)

    policy = DDPG(
        state_shape=env.observation_space.shape,
        action_dim=env.action_space.high.size,
        gpu=args.gpu,
        memory_capacity=args.memory_capacity,
        max_action=env.action_space.high[0],
        batch_size=args.batch_size,
        n_warmup=args.n_warmup)
    trainer = PointrobotTrainer(policy, env, args, test_env=test_env)


def test_state_concatenation():
    print('-' * 5 + 'test_state_concatenation' + '-' * 5)

    model = CAE(pooling='max',
                latent_dim=16,
                input_shape=(32, 32),
                conv_filters=[4, 8, 16])
    model.build(input_shape=(1, 32, 32, 1))
    model.load_weights(filepath='../models/cae/model_num_5_size_8.h5')

    for layer, _ in model._get_trainable_state().items():
        layer.trainable = False

    env = gym.make("pointrobo-v0")
    workspace, goal, obs = env.reset()
    print('ws type: {}, dtype: {}, shape: {}'.format(type(workspace), workspace.dtype, workspace.shape))
    print('goal type: {}, dtype: {}, shape: {}'.format(type(goal), goal.dtype, goal.shape))
    print('obs type: {}, dtype: {}, shape: {}'.format(type(obs), obs.dtype, obs.shape))

    reduced_ws = model.evaluate(workspace)
    complete_state = np.concatenate((obs, goal, reduced_ws))
    print('complete_state type: {}, dtype: {}, shape: {}'.format(type(complete_state), complete_state.dtype, complete_state.shape))


if __name__ == '__main__':

    test_pointrobot_trainer_init()
    test_state_concatenation()
    print('All tests have run successfully!')

    

    