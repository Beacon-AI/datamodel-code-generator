from __future__ import annotations

from typing import Any, ClassVar, Literal, Optional

from datamodel_code_generator.model.pydantic_v2.base_model import BaseModel


class RootModel(BaseModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic_v2/RootModel.jinja2'
    BASE_CLASS: ClassVar[str] = 'pydantic.RootModel'

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        # Remove custom_base_class for Pydantic V2 models; behaviour is different from Pydantic V1 as it will not
        # be treated as a root model. custom_base_class cannot both implement BaseModel and RootModel!
        if 'custom_base_class' in kwargs:
            kwargs.pop('custom_base_class')

        super().__init__(**kwargs)

    def _get_config_extra(self) -> Optional[Literal["'allow'", "'forbid'"]]:
        # PydanticV2 RootModels cannot have extra fields
        return None

    def render(self, *, class_name: Optional[str] = None) -> str:
        # RootModel cannot have 'extra' in model_config. The extra_template_data dict may be
        # shared with a BaseModel that has the same name (e.g. when a schema definition and
        # the top-level anyOf schema share a title), which sets 'extra' after __init__ completes.
        # Strip 'extra' at render time without mutating the shared dict.
        extra_data = dict(self.extra_template_data)
        config = extra_data.get('config')
        if config is not None:
            config_dict = config.dict(exclude_unset=True)
            if 'extra' in config_dict:
                config_dict.pop('extra')
                from datamodel_code_generator.model.pydantic_v2 import ConfigDict
                extra_data['config'] = ConfigDict.parse_obj(config_dict) if config_dict else None
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            decorators=self.decorators,
            base_class=self.base_class,
            methods=self.methods,
            description=self.description,
            keyword_only=self.keyword_only,
            **extra_data,
        )
