import pathlib
import joblib

from hem.armm.clustering.model.pipelinemodel import pipeline
from hem.armm.clustering.model.gridsearch import gridsearch


def loadmodel(model_address: str):
    file = pathlib.Path(model_address)
    if not file.exists():
        raise FileNotFoundError(f'{file.as_posix()} does not exist!')
    else:
        return joblib.load(model_address)
