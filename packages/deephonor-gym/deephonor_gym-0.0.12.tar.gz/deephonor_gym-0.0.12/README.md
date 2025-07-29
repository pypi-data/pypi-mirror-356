# deephonor_gym Package

This package is part of the RL (Reinforcement Learning) project.  
You can call this tool DHG or DHGym.

## Overview

The development purpose of deephonor-gym is to significantly lower the barriers to reinforcement learning and physical simulation.   
Based on this library, users can very quickly view and train robots.  
While this simulation platform has limited performance, it offers high accuracy, making it well-suited for algorithm validation by students, companies, and individual enthusiasts.

翻译：易用，好用，免费

## Installation

The recommended way to install this package is via PyPI:

`pip install deephonor-gym --no-cache-dir`

or

`pip install deephonor-gym`

## License

This project is licensed under the **GNU Affero General Public License v3.0**.  
See [LICENSE](LICENSE) for the full text.

## Detail
- explain_action
    - 'ball' is link name. -> 'Impulse.ball' = direction array
    - 'KP1' is joint name. -> 'joint.ball' = angle

- explain_reset
    - 'ball' is link name.
    - 'KP1' is joint name.

```bash
   Y 
   |     Z screen 
   |  ／
   .—— —— X
``` 

## Usage

Once installed, the package can be imported via `from deephonor_gym import DHgym, DHgym_VecEnv, open_browser, Upload`
Or, you can read the source code to access additional details.

- step1:
```py
# open DHgym

from deephonor_gym import open_browser,Upload
open_browser() 
# Upload('models','models') # This only needs to be done once
```

- step2
```py
# make your own env
# a ball Game (Being close to (0,0) denote success.)

import gymnasium as gym
import numpy as np
from deephonor_gym import DHgym,DHgym_VecEnv

class myEnv(DHgym) :
    """用户自己写的代码"""
    def init(self):
        self.num_envs = 1
        self.render_fps = 20

        self.action_space = gym.spaces.Discrete(5) # 0, 1, 2，3，4:

        # x,z,vx,vz
        low = [-10 , -10 ,-200,-200]
        high = [10 , 10, 200, 200]
        self.observation_space = gym.spaces.Box(
            low  = np.array(low ,dtype=np.float32),
            high = np.array(high,dtype=np.float32)
            )# 确定上下界

        add_obj = {} # 以下参数均可选，除了path
        add_obj['world'] = {'gravity':[0, -9.81, 0],'speed':1 } # optional 可选 speed > 0.01
        # add_obj['Heightground'] = {'size':[30,30,10],'position':[0,0,0],'path': '/models/heightground.jpeg', 'detail': 100 } # optional 可选 detail >= 1
        add_obj['urdf'] = [
                            {'scale':1,'position':[2,1,0],'path': '/models/ball.urdf','debug':False },
                            # {'scale':1,'position':[0,1,0],'path': '/models/a1_description/urdf/a1.urdf','debug':True, 'JointDamping': 1000}, 如果有的话
                          ]
        add_obj['Ground'] = {'size':[20,20] ,'position':[0,0,0]} # optional 可选 如果 不用 Heightground
        
        obs_target = []
        obs_target.append('Link.ball') # (x,y,z,vx,vy,vz)

        return add_obj, obs_target
        
    def explain_obs(self,obs):
        state = np.zeros((self.num_envs,4),dtype=np.float32)
        for i in range( self.num_envs):
            x,_,y,vx,_,vy = obs[i]
            state[i][0] = x  
            state[i][1] = y  
            state[i][2] = vx  
            state[i][3] = vy  
        return state
    
    def explain_action(self,action):
        explain = []
        for i in range(self.num_envs):
            force = {}
            if action[i]==0:
                force['Impulse.ball'] = [10,0,0]
            elif action[i]==1:
                force['Impulse.ball'] = [-10,0,0]
            elif action[i]==2:
                force['Impulse.ball'] = [0,0,10]
            elif action[i]==3:
                force['Impulse.ball'] = [0,0,-10]
            elif action[i]==4:
                force['Impulse.ball'] = [0,0,0]
            explain.append(force)

        # for i in range(self.num_envs):
        #     force = {}
        #     force['Joint.KP1'] = action[i]/3
        
            explain.append(force)
        return explain

    
    def reward(self,state):
        reward_array  = np.full(self.num_envs,0,dtype=np.float32)
        terminated = np.full(self.num_envs,False,dtype=bool)
        truncated  = np.full(self.num_envs,False,dtype=bool)
        reset_array = np.full(self.num_envs,False,dtype=bool)
        
        for i in range( self.num_envs):
            info = self.info_array[i]

            x,y,vx,vy = state[i]
            info["counts"] += 1 
            
            distance = np.abs(np.array([x, y])).sum()
            Done = (distance<=1) or (distance >= 20) 
            if not Done:
                reward =  -1*distance
                info["is_success"] = False
            else:
                if distance<=1:
                    reward = 10
                    info["is_success"] = True
                else:
                    reward = -40 # 超界扣大分 或 超步数
                    info["is_success"] = False
            if Done:
                info["TimeLimit.truncated"]= False # PPO等ReplayBuffer算法专属
                info["terminal_observation"]= state[i]
                reset_array[i] = True
                info["counts"] = 0
            
            terminated[i] = Done 
            reward_array[i] = reward
        return  reward_array, terminated, truncated, reset_array
    
    def explain_reset(self,reset_array):
        position = {}
        random_uniform: np.ndarray = np.random.uniform(size=(self.num_envs, 3))* 2 * 10 - 10
        random_uniform.astype(int)
        random_uniform[:,1] = 1
        position['sphere_robot'] = random_uniform # robot name

        angle = {}
        # angle['KP1'] = np.zeros(self.num_envs).fill(1.5)

        return [position, angle]
```

- step3:
```py
# test your RL env

env = DHgym_VecEnv( [lambda : myEnv()]) # 查看 env
obs = env.reset()
for i in range(10):
    obs, reward,done , infomation  = env.step( np.array([env.action_space.sample()]))
    print(obs, reward, done , infomation )
```

- step4:
```py
# train your RL env
# stable_baselines3 example

from stable_baselines3 import  DQN

env = DHgym_VecEnv( [lambda : myEnv()]) # 查看 env
model = DQN("MlpPolicy", env=env, verbose=1)
model.learn(total_timesteps=10000 ,log_interval=10,progress_bar=True)
```



