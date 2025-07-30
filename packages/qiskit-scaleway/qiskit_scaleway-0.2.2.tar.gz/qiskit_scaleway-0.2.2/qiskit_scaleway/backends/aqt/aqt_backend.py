# Copyright 2025 Scaleway
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import randomname
import warnings

from typing import Union, List

from qiskit.circuit import QuantumCircuit
from qiskit.providers import Options
from qiskit.transpiler import Target, PassManager

from qiskit_aqt_provider.aqt_resource import make_transpiler_target
from qiskit_aqt_provider.transpiler_plugin import bound_pass_manager

from qiskit_scaleway.backends import BaseBackend
from qiskit_scaleway.backends.aqt.aqt_job import AqtJob
from qiskit_scaleway.api import QaaSClient, QaaSPlatform


class AqtBackend(BaseBackend):
    def __init__(self, provider, client: QaaSClient, platform: QaaSPlatform):
        super().__init__(
            provider=provider,
            client=client,
            platform=platform,
        )

        self._options = self._default_options()
        self._target = make_transpiler_target(Target, platform.max_qubit_count)

        self._options.set_validator("shots", (1, platform.max_shot_count))

    def __repr__(self) -> str:
        return f"<AqtBackend(name={self.name},num_qubits={self.num_qubits},platform_id={self.id})>"

    def get_scheduling_stage_plugin(self) -> str:
        return "aqt"

    def get_translation_stage_plugin(self) -> str:
        return "aqt"

    def get_pass_manager(self) -> PassManager:
        return bound_pass_manager()

    @property
    def target(self):
        return self._target

    @property
    def num_qubits(self) -> int:
        return self._target.num_qubits

    @property
    def max_circuits(self):
        return 50

    def run(
        self, circuits: Union[QuantumCircuit, List[QuantumCircuit]], **run_options
    ) -> AqtJob:
        if not isinstance(circuits, list):
            circuits = [circuits]

        job_config = dict(self._options.items())

        for kwarg in run_options:
            if not hasattr(self.options, kwarg):
                warnings.warn(
                    f"Option {kwarg} is not used by this backend",
                    UserWarning,
                    stacklevel=2,
                )
            else:
                job_config[kwarg] = run_options[kwarg]

        job_name = f"qj-aqt-{randomname.get_name()}"

        session_id = job_config.get("session_id", None)

        job_config.pop("session_id")
        job_config.pop("session_name")
        job_config.pop("session_deduplication_id")
        job_config.pop("session_max_duration")
        job_config.pop("session_max_idle_duration")

        job = AqtJob(
            backend=self,
            client=self._client,
            circuits=circuits,
            config=job_config,
            name=job_name,
        )

        if session_id in ["auto", None]:
            session_id = self.start_session(name=f"auto-{self._options.session_name}")
            assert session_id is not None

        job.submit(session_id)

        return job

    @classmethod
    def _default_options(self):
        return Options(
            session_id="auto",
            session_name="aqt-session-from-qiskit",
            session_deduplication_id="aqt-session-from-qiskit",
            session_max_duration="1h",
            session_max_idle_duration="20m",
            shots=100,
            max_shots=2000,
            memory=True,
            open_pulse=False,
            description="AQT trapped-ion device",
            conditional=False,
            max_experiments=1,
            simulator=False,
            local=False,
            url="api.scaleway.com",
            basis_gates=["r", "rz", "rxx"],
            gates=[
                {"name": "rz", "parameters": ["theta"], "qasm_def": "TODO"},
                {"name": "r", "parameters": ["theta", "phi"], "qasm_def": "TODO"},
                {"name": "rxx", "parameters": ["theta"], "qasm_def": "TODO"},
            ],
        )
