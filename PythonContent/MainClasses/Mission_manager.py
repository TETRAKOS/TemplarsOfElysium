import os
import json

class Mission:
    def __init__(self, game, mapgen, mission):
        self.mission = mission
        self.game = game
        self.mapgen = mapgen

    def generate_mission(self):
        missions_list = self.read_mission()
        mission_data = next((m for m in missions_list if m["mission"] == self.mission), None)
        if mission_data:
            name = mission_data["mission"]
            basic = mission_data["basic"]
            danger = mission_data["danger"]
            loot = mission_data["loot"]
            final = mission_data["final"]
            return name,basic,danger,loot,final

    def read_mission(self):
        missions_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path_file = os.path.join(missions_dir, 'Assets', 'dicts', 'mission_types.js')
        with open(asset_path_file, 'r') as f:
            return json.load(f)
    def deploy_mission(self):
        pass


    def complete_mission(self):
        pass


    def end(self, result):
        pass