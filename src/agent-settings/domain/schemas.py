from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class AgentSettingBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_max_length=1,
        alias_generator=to_camel
    )




