"""
BaseBuilder.py
--------------
An abstract base class for building and validating data objects using a Pydantic schema.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type
from pydantic import BaseModel, ValidationError
from isloth_python_common_lib.errors.BadRequestError import BadRequestError

TModel = TypeVar('TModel', bound=BaseModel)


class BaseBuilder(ABC, Generic[TModel]):
    """
    Abstract builder class for creating and validating Pydantic-based data models.

    Attributes
    ----------
    data : dict
        A dictionary holding partial input data.
    model_cls : Type[TModel]
        The Pydantic model class used for validation and instantiation.
    """

    def __init__(self, model_cls: Type[TModel]) -> None:
        self.data: dict = {}
        self.model_cls: Type[TModel] = model_cls

    @abstractmethod
    def validate(self, model: TModel) -> None:
        """
        Hook method for custom validation logic.

        Parameters
        ----------
        model : TModel
            The validated Pydantic model instance.
        """
        pass

    def build(self) -> TModel:
        """
        Validates and builds the final model instance.

        Returns
        -------
        TModel
            The validated data model.

        Raises
        ------
        BadRequestError
            If validation fails, raises with detailed input errors.
        """
        try:
            model = self.model_cls(**self.data)
            self.validate(model)
            return model
        except ValidationError as ve:
            raise BadRequestError('Validation failed').add_validation_errors([dict(e) for e in ve.errors()])

    def to_json(self) -> dict:
        """
        Converts the current data into a JSON-compatible dictionary.

        Returns
        -------
        dict
            Partial representation of the input data.
        """
        return dict(self.data)
