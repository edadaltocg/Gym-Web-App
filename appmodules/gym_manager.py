import gym
import numpy as np
import cv2
import json

class Games:
    def __init__(self):
        self.game_list = ['adventure', 'air_raid', 'alien', 'amidar', 'assault', 'asterix', 'asteroids', 'atlantis',
                     'bank_heist', 'battle_zone', 'beam_rider', 'berzerk', 'bowling', 'boxing', 'breakout', 'carnival',
                     'centipede', 'chopper_command', 'crazy_climber', 'defender', 'demon_attack', 'double_dunk',
                     'elevator_action', 'enduro', 'fishing_derby', 'freeway', 'frostbite', 'gopher', 'gravitar',
                     'hero', 'ice_hockey', 'jamesbond', 'journey_escape', 'kangaroo', 'krull', 'kung_fu_master',
                     'montezuma_revenge', 'ms_pacman', 'name_this_game', 'phoenix', 'pitfall', 'pong', 'pooyan',
                     'private_eye', 'qbert', 'riverraid', 'road_runner', 'robotank', 'seaquest', 'skiing',
                     'solaris', 'space_invaders', 'star_gunner', 'tennis', 'time_pilot', 'tutankham', 'up_n_down',
                     'venture', 'video_pinball', 'wizard_of_wor', 'yars_revenge', 'zaxxon']
        self.not_supported_games = ['defender']
        [self.game_list.remove(elem) for elem in self.not_supported_games]
        self.all_envs = gym.envs.registry.all()
        self.env_ids = [env_spec.id for env_spec in self.all_envs]

    def dict_names(self):
        pretty_game_list = []
        for game in self.game_list:
            pretty_game_list.append(''.join([g.capitalize() for g in game.split('_')]))
        return dict(zip(self.game_list, pretty_game_list))

    def unzip_list(self):
        pass

    def get_games_from_key(self, key):
        name = self.dict_names()[key]
        filter = np.argwhere(np.array([name in id for id in self.env_ids]) == True).reshape(-1)
        return [self.env_ids[id] for id in filter]

    def get_name(self):
        pass

class Game:
    def __init__(self, game_type, agent_id='random'):
        self.env = gym.make(game_type)
        self.agent = self.choose_agent(agent_id)
        self.human_wants_restart = False
        self.human_sets_pause = False

    def play(self, NUM_EPISODES=1000):
        # Main method
        state_n = self.env.reset()
        reward_n = 0

        for episode in range(NUM_EPISODES):
            action_n = self.agent.get_action(state_n, reward_n)
            state_n, reward_n, done, info = self.env.step(action_n)

            if done:
                break

            # Render game image
            frame = state_n
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
            # yield the output frame in the byte format
            # serve the encoded JPEG frame as a byte array that can be consumed
            # by a web browser.
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

        self.env.close()


    def choose_agent(self, agent):
        if agent == 'random':
            return RandomAgent(self.env)

    def show_frame(self):
        # cv2.imshow("", frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        self.env.reset()
        frame, _, _, _ = self.env.step(self.env.action_space.sample())
        return frame

    def get_static_image(self):
        self.env.reset()
        frame, _, _, _ = self.env.step(self.env.action_space.sample())
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        return flag, encodedImage

    def frame_dimensions(self, frame):
        im = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        height, width = im.shape
        return json.dumps({"width": width, "height": height})

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

# Parent agent class
class Agent:
    def __init__(self, env):
        self.env = env
        self.ACTIONS = self.get_action_space()

    def get_action_space(self):
        if not hasattr(self.env.action_space, 'n'):
            raise Exception('Keyboard agent only supports discrete action spaces')
        return self.env.action_space.n

class RandomAgent(Agent):
    def __init__(self, env):
        super().__init__(env)

    def get_action(self, state_n, reward_n):
        return self.env.action_space.sample()

class KeyboardAgent(Agent):
    def __init__(self, env):
        super().__init__(env)


####
# Debug
####
#
# games = Games()
# dict_name = games.dict_names()
# for test in dict_name:
#     print(test, dict_name[test])



