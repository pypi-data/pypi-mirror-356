"""Midas scenario upgrade module.

This module adds a time simulator to the scenario.
"""

import logging

from midas.scenario.upgrade_module import ModuleParams, UpgradeModule

LOG = logging.getLogger(__name__)


class TimeSimModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="timesim",
            default_scope_name="timesim",
            default_sim_config_name="TimeSim",
            default_import_str=("midas_timesim.simulator:TimeSimulator"),
            default_cmd_str=("%(python)s -m midas_timesim.simulator %(addr)s"),
            log=LOG,
        )
        self.model = "Timegenerator"
        self.attrs: list[str | tuple[str, str]] = [
            "sin_day_time",
            "sin_week_time",
            "sin_year_time",
            "cos_day_time",
            "cos_week_time",
            "cos_year_time",
            "utc_time",
            "local_time",
            "unix_time",
        ]

    def check_module_params(self, mp: ModuleParams):
        """Check module params for this upgrade."""
        mp.setdefault(self.default_scope_name, dict())
        mp.setdefault("start_date", self.scenario.base.start_date)

    def check_sim_params(self, mp: ModuleParams):
        self._simp_from_modulep(mp, "start_date")
        self.sim_params.setdefault("time_schedule", [])

    def start_models(self):
        model_key = self.scenario.generate_model_key(self)

        self.start_model(model_key, self.model, {})

    def connect(self):
        pass

    def connect_to_db(self):
        db_key = self.scenario.find_first_model("store", "database")[0]
        assert db_key is not None, "No db_key found."
        model_key = self.scenario.generate_model_key(self)
        self.connect_entities(model_key, db_key, self.attrs)

    def get_sensors(self):
        model = self.scenario.find_first_model(self.sim_key)[1]
        assert model is not None, f"Model for {self.sim_key} is None."
        full_id = model["full_id"]
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.sin_day_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.sin_week_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.sin_year_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.cos_day_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.cos_week_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.cos_year_time",
                "space": ("Box(low=-1, high=1, shape=(), dtype=np.float32)"),
            }
        )
        self.scenario.sensors.append(
            {
                "uid": f"{full_id}.unix_time",
                "space": {
                    "Box(low=0, high=np.inf, shape=(), dtype=np.float32)"
                },
            }
        )
