import time

import torch

from pufferlib.models import Default, LSTMWrapper
from pufferlib.ocean import env_creator

def test_net_speed(batch_size=8192, hidden_size=512):
    env = env_creator('puffer_breakout')()
    input_size = env.single_observation_space.shape[0]

    observations = torch.randn(batch_size, input_size).cuda()
    state = {
        'lstm_h': torch.zeros(batch_size, hidden_size).cuda(),
        'lstm_c': torch.zeros(batch_size, hidden_size).cuda(),
    }

    model = Default(env, hidden_size=hidden_size)
    model = LSTMWrapper(env, policy=model, input_size=hidden_size, hidden_size=hidden_size)
    model = model.cuda()

    step = 0
    start = time.time()
    while (time.time() - start) < 10:
        with torch.no_grad():
            output = model.forward_eval(observations, state)

        step += batch_size

    end = time.time()
    sps = step / (end - start)
    print(f'Speed: {sps:,.2f} steps/s')

def test_lstm_speed(batch_size=8192, hidden_size=8192):
    observations = torch.randn(batch_size, hidden_size).cuda()
    state = (
        torch.zeros(batch_size, hidden_size).cuda(),
        torch.zeros(batch_size, hidden_size).cuda(),
    )
    model = torch.nn.LSTMCell(hidden_size, hidden_size)
    model = model.cuda()

    torch.cuda.synchronize()
    step = 0
    start = time.time()
    while (time.time() - start) < 10:
        with torch.no_grad():
            output = model(observations, state)

        step += batch_size
        torch.cuda.synchronize()

    end = time.time()
    sps = step / (end - start)
    tflops = 8*hidden_size*hidden_size*sps / 1e12
    print(f'Speed: {sps:,.2f} steps/s')
    print(f'TFLOPS: {tflops:,.2f}')


if __name__ == '__main__':
    test_lstm_speed()
