"""An example config dictionary for the whole summarization pipeline"""

config = {
  'dataset_path':None,
  'dataset':None,

  'extractive': False,
  'device':None,

  'src_vocab_path': None,
  'src_vocab' : None,
  'trg_vocab_path' : None,
  'autoencoder_path': None,
  'autoencoder':None,
  'ae_batchsize': 5000,

  'density_parameter': .04,
  'minimum_samples': 4,
  'min_clusters': 5,
  'max_acceptable_clusters':30,
  'min_num_candidates': 100,

  'BERT_finetune_path':None,
  'BERT_config_path': None,
  'BERT_finetune_model':None,
  'BERT_batchsize': 100,

  'opt_function' : None,
  'opt_dict' = {
    'sentence_cap': 20,
    'n_elite':5,
    'init_pop': 96,

  }
}