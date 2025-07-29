"""
A :class:`~allennlp.data.dataset_readers.dataset_reader.DatasetReader`
reads a file and converts it to a collection of
:class:`~allennlp.data.instance.Instance` s.
The various subclasses know how to read specific filetypes
and produce datasets in the formats required by specific models.
"""


from radgraph.allennlp.data.dataset_readers.conll2003 import Conll2003DatasetReader
from radgraph.allennlp.data.dataset_readers.dataset_reader import (
    DatasetReader,
    AllennlpDataset,
    AllennlpLazyDataset,
)
from radgraph.allennlp.data.dataset_readers.interleaving_dataset_reader import InterleavingDatasetReader
from radgraph.allennlp.data.dataset_readers.sequence_tagging import SequenceTaggingDatasetReader
from radgraph.allennlp.data.dataset_readers.sharded_dataset_reader import ShardedDatasetReader
from radgraph.allennlp.data.dataset_readers.babi import BabiReader
from radgraph.allennlp.data.dataset_readers.text_classification_json import TextClassificationJsonReader
