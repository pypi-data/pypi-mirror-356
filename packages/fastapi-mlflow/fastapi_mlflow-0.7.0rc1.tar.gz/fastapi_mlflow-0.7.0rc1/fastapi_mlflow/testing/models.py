# -*- coding: utf-8 -*-
"""Dummy MLflow `PythonModel`s for testing.

Copyright (C) 2023, Auto Trader UK
Created 08. Nov 2023

"""
import numpy as np
import pandas as pd
from mlflow.pyfunc import PythonModel, PythonModelContext
from numpy import typing as npt


class DeepThought(PythonModel):
    """A simple PythonModel that returns `42` for each input row."""

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> npt.ArrayLike:
        return np.array([42] * len(model_input))


class DeepThoughtSeries(PythonModel):
    """A PythonModel that returns a DataFrame."""

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.Series:
        return pd.Series([42] * len(model_input))


class DeepThoughtDataframe(PythonModel):
    """A PythonModel that returns a DataFrame."""

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "answer": 42,
                    "question": (
                        "The ultimate question of life, the universe, "
                        "and everything!"
                    ),
                }
            ]
            * len(model_input)
        )


class NaNModel(PythonModel):
    """A PythonModel that returns NaN."""

    def predict(self, context: PythonModelContext, model_input: pd.DataFrame):
        return np.array([np.nan] * len(model_input))


class NaNModelSeries(PythonModel):
    """A PythonModel that returns NaNs in a Series."""

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.Series:
        return pd.Series(NaNModel().predict(context, model_input))


class NaNModelDataFrame(PythonModel):
    """A PythonModel that returns NaNs in a DataFrame."""

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.DataFrame:
        nan_model = NaNModelSeries()
        return pd.DataFrame(
            {
                "a": nan_model.predict(context, model_input),
                "b": nan_model.predict(context, model_input),
            }
        )


class StrModel(PythonModel):
    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> npt.ArrayLike:
        return np.array(["42"] * len(model_input))


class StrModelSeries(PythonModel):
    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.Series:
        return pd.Series(StrModel().predict(context, model_input))


class ExceptionRaiser(PythonModel):
    """A PythonModle that always raises an exception."""

    ERROR_MESSAGE = "I always raise an error!"

    def predict(
        self, context: PythonModelContext, model_input: pd.DataFrame
    ) -> pd.DataFrame:
        raise ValueError(self.ERROR_MESSAGE)
