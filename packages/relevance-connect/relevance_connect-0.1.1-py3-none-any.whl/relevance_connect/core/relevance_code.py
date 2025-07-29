import requests
from relevance_connect.core.auth import Auth, config

def handle_response(response):
    try:
        return response.json()
    except:
        return response.text

class RelevanceCode:
    def __init__(
        self,
        code: str,
        name: str,
        requirements: list[str] = [],
        required: list[str] = [],
        description: str = "",
        inputs={},
        code_type: str = "python",
        long_output_mode: bool = False,
        timeout: int = 300,
        id: str = None,
        icon: str = None,
        auth: Auth = None,
    ):
        """
        :param name: name of the integration
        :param description: description of the integration
        :param inputs: inputs of the integration
        :param id: id of the integration
        :param auth: auth object
        """
        self.code = code
        self.name = name
        self.description = description
        self._inputs = inputs
        self.steps = []
        # generate random id if none provided
        self.random_id = False
        if id is None:
            import uuid
            id = str(uuid.uuid4())
            self.random_id = True
        self.id = id
        self.code_type = code_type
        self.long_output_mode = long_output_mode
        self.timeout = timeout
        self.requirements = requirements
        self.required = required
        self.icon = icon
        self.auth: Auth = config.auth if auth is None else auth
        self.steps.append(
            self._add_code_step(code, requirements, code_type, long_output_mode, timeout)
        )

    def _add_code_step(self, code: str, requirements: list[str] = [], code_type: str = "python", long_output_mode: bool = False, timeout: int = 300):
        if code_type == "python":
            step_json = {
                "transformation": "python_code_transformation",
                "name": "code_block",
                "params": {
                    "code": code,
                    "packages": requirements,
                }
            }
            if long_output_mode:
                step_json["params"]["long_output_mode"] = long_output_mode
            if timeout:
                step_json["params"]["timeout"] = timeout
            return step_json
        elif code_type == "javascript":
            step_json = {
                "transformation": "js_code_transformation",
                "name": "code_block",
                "params": {
                    "code": code,
                }
            }
            return step_json

    def _state_mapping(self):
        state_mapping = {}
        for inp in self._inputs:
            state_mapping[inp['input_name']] = f"params.{inp['input_name']}"
        for step in self.steps:
            state_mapping[step['name']] = f"steps.{step['name']}.output"
        return state_mapping

    def _params_schema(self):
        return {
            "properties": { inp['input_name'] : {k: v for k, v in inp.items() if k != 'input_name'} for inp in self._inputs }
        }

    def _trigger_json(
        self, values: dict = {}, return_state: bool = True, public: bool = False
    ):
        data = {
            "return_state": return_state,
            "studio_override": {
                "public": public,
                "state_mapping" : self._state_mapping(),
                "params_schema": self._params_schema(),
                "transformations": {
                    "steps": self.steps,
                    "output": {
                        "results": "{{code_block.transformed}}"
                    }
                },
            },
            "params": values,
        }
        data["studio_id"] = self.id
        data["studio_override"]["studio_id"] = self.id
        return data


    def tool_json(self):
        data = {
            "title": self.name,
            "description": self.description,
            "version": "latest",
            "project": self.auth.project,
            "public": False,
            "state_mapping" : self._state_mapping(),
            "params_schema": self._params_schema(),
            "transformations": {
                "steps": self.steps,
                "output": {
                    "results": "{{code_block.transformed}}"
                }
            },
        }
        if self.icon:
            data["emoji"] = self.icon
        data["studio_id"] = self.id
        return data

    def run(self, inputs={}, full_response: bool = False):
        url = f"{self.auth.url}/latest/studios/{self.auth.project}"
        response = requests.post(
            f"{url}/trigger",
            json=self._trigger_json(inputs),
            headers=self.auth.headers,
        )
        res = handle_response(response)
        if isinstance(res, dict):
            if ("errors" in res and res["errors"]) or full_response:
                return res
            elif "output" in res:
                return res["output"]
        return res


    def save(self):
        url = f"{self.auth.url}/latest/studios"
        print(self.tool_json())
        print(self.icon)
        response = requests.post(
            f"{url}/bulk_update",
            json={"updates": [self.tool_json()]},
            headers=self.auth.headers,
        )
        res = handle_response(response)
        print(res)
        print("Tool deployed successfully to id ", self.id)
        return self.id