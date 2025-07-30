import pufferlib.ocean

env_creator = pufferlib.ocean.env_creator('puffer_breakout')

import pufferlib.vector

for i in range(1000):
    vecenv = pufferlib.vector.make(env_creator, num_envs=16, num_workers=16,
                                   env_kwargs={'num_envs':1024, 'log_interval':1}, backend=pufferlib.vector.Serial)
    vecenv.async_reset()
    for j in range(100):
        vecenv.recv()
        vecenv.send(vecenv.action_space.sample())

    vecenv.close()
    print(i)

