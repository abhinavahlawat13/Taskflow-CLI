from pathlib import Path
class Settings:
    project_name: str = "taskflow cli"
    version: str = "0.1.0"
    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    data_dir: Path = base_dir / "data"
    db_name: str = "taskflow.db"

    @property
    def db_path(self) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        return self.data_dir / self.db_name


settings = Settings()