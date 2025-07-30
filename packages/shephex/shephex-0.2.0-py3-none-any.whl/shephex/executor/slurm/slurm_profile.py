import json
from pathlib import Path


class SlurmProfileManager:

    def __init__(self) -> None:
        self.settings_directory = Path.home() / '.shephex/'
        self.settings_directory.mkdir(exist_ok=True)
        self.settings_path = self.settings_directory / 'slurm_profile_manager.json'
                
        self.settings = self.load_settings()
        self.profile_directory = Path(self.settings['profile_directory'])
        self.profile_directory.mkdir(exist_ok=True)

    def load_settings(self) -> dict:
        if self.settings_path.exists():
            with open(self.settings_path) as f:
                settings = json.load(f)
        else:
            settings = {"profile_directory": str(Path.home() / '.shephex/slurm_profiles/')}
            with open(self.settings_path, 'w') as f:
                json.dump(settings, f, indent=4)

        return settings
    
    def set_profile_directory(self, path: Path) -> None:
        self.settings['profile_directory'] = str(path)
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_profile_directory(self) -> Path:
        return self.profile_directory
    
    def get_all_profiles(self) -> list[Path]:
        return list(self.profile_directory.glob('*.json'))
    
    def get_profile_path(self, name: str) -> Path:
        if not name.endswith('.json'):
            name = name + '.json'

        path = self.profile_directory / name
        if not path.exists():
            raise FileNotFoundError(f'Profile {name} not found in {self.profile_directory}')
        
        return path
    
    def get_profile(self, name: str) -> dict:
        path = self.get_profile_path(name)
        with open(path) as f:
            return json.load(f)

    

if __name__ == '__main__':

    spm = SlurmProfileManager()

    z = spm.get_all_profiles()

    spm.get_profile('kage')

    