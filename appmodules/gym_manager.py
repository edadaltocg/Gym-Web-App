import gym
import numpy as np

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
        print(filter)
        return [self.env_ids[id] for id in filter]

    def get_name(self):
        pass

class Game:
    def __init__(self, id):
        self.id = id

####
# Debug
####
#
# games = Games()
# dict_name = games.dict_names()
# for test in dict_name:
#     print(test, dict_name[test])



