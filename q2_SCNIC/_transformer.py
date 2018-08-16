# TODO: Move all this to q2-network and split functionality

import pandas as pd
import networkx as nx

from .plugin_setup import plugin
from ._format import PairwiseFeatureDataFormat, GraphModelingLanguageFormat


@plugin.register_transformer
def _1(data: pd.DataFrame) -> PairwiseFeatureDataFormat:
    ff = PairwiseFeatureDataFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t', index_label=('feature1', 'feature2'))
    return ff


@plugin.register_transformer
def _2(ff: PairwiseFeatureDataFormat) -> pd.DataFrame:
    df =  pd.read_table(str(ff), index_col=(0, 1), sep='\t')
    new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in df.index])
    df.index = new_index
    return df


@plugin.register_transformer
def _3(data: nx.Graph) -> GraphModelingLanguageFormat:
    ff = GraphModelingLanguageFormat()
    nx.write_gml(data, str(ff.path))
    return ff


@plugin.register_transformer
def _4(ff: GraphModelingLanguageFormat) -> nx.Graph:
    return nx.read_gml(str(ff))
