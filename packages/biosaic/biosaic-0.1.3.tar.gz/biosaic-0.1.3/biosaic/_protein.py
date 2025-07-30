from itertools import product
import json, pickle
import os, tempfile, urllib, requests
import numpy as np

AMINO_ACIDS = [
  'A','R','N','D','C','Q','E','G','H','I',
  'L','K','M','F','P','S','T','W','Y','V','-'  # 21st for gap/pad
]

class Protein:
  def __init__(self, kmer: int, continuous: bool=True):
    self.kmer = kmer
    self.continuous = continuous
    self._base_chars = AMINO_ACIDS   # upper-case Protein letters
    self._ids_to_taken, self.vocab = {}, {}
 
    # Calculate vocab size:
    #  - continuous: exactly len(base_chars)**k distinct k-mers
    #  - non-continuous: sum of len(base_chars)**i for lengths 1 to k
    if self.continuous:
      self.vocab_size = len(self._base_chars) ** kmer
    else:
      self.vocab_size = sum(len(self._base_chars) ** i for i in range(1, kmer+1))

  def tokenize(self, sequence):
    if any(ch not in self._base_chars for ch in sequence):
      raise ValueError("Invalid character in Protein sequence")

    if self.continuous:
      return [sequence[i : i+self.kmer] for i in range(len(sequence) - self.kmer + 1)]
    else:
      return [sequence[i : i+self.kmer] for i in range(0, len(sequence), self.kmer)]

  def detokenize(self, ids):
    if self.continuous:
      if not ids:
        return ""
      return "".join(ids[i][0] for i in range(len(ids))) + ids[-1][1:]
    else:
      return "".join(i for i in ids)

  def build_vocab(self):
    letters, combos = sorted(self._base_chars), []
    if self.continuous:
      combos = list(product(letters, repeat=self.kmer))
    else:
      for L in range(1, self.kmer + 1):
        combos.extend(product(letters, repeat=L))
    self.vocab = {''.join(c): i for i, c in enumerate(combos)}
    self.ids_to_token = {v: k for k, v in self.vocab.items()}
    self.vocab_size = len(self.vocab)

  def encode(self, sequence):
    sequence = sequence.upper() # ensures sequence entered is upper-cased
    tokenized_data = self.tokenize(sequence)
    return [self.vocab[kmer] for kmer in tokenized_data if kmer in self.vocab]

  def decode(self, ids):
    tokens = self.ids_to_chars(ids)
    print("tokens: ", tokens)
    return self.detokenize(tokens)

  def ids_to_chars(self, ids: list[int]):
    """returns the list containing chars mapped to ids

    Args:
      ids (List[int]): list containing only output tokens from a model or just ids
    Returns:
      List: list with the respective chars
    """
    assert isinstance(ids, list) and len(ids) > 0, "ids must be a non-empty list"
    assert isinstance(ids[0], int), "only accepts encoded ids"
    return [self.ids_to_token[i] for i in ids]

  def chars_to_ids(self, chars: list[str]):
    """returns the list containing ids mapped to chars

    Args:
      chars (List[str]): list containing tokenized chars for id mapping
    Returns:
      List: list with the respective ids
    """
    assert isinstance(chars, list) and len(chars) > 0, "chars must be a non-empty list"
    assert isinstance(chars[0], str), "only accepts tokenized strings"
    return [self.vocab[i] for i in chars]

  def verify(self, ids, file=None):
    """returns a list containing true/false values for respective matching kmers
      also saves them to a file, as needed by user

    Args:
      ids (List[str]): list containing tokenized chars
      file (Optional|None): file path
    Returns:
      dictionary: dictionary containing mapped true/false pairs for verification
    """
    verified = []
    ids = self.ids_to_chars(ids) if isinstance(ids[0], int) else ids
    for i in range(len(ids) - 1):
      match = ids[i][1:] == ids[i + 1][:-1]
      verified.append({"kmer1": ids[i], "kmer2": ids[i + 1], "match": match})
    if file:
      file_path = os.path.join(file, "verify.json")
      with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(verified, f)
    return verified

  def save(self, path, as_json=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
      "kmer": self.kmer,
      "vocab_size": self.vocab_size,
      "trained_vocab": self.vocab
    }
    if as_json:
      with open(path + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    else:
      with open(path + ".model", "wb") as f:
        pickle.dump(data, f)
    print(f"DEBUGG INFO[104] [Saved] Vocabulary saved to {path + ('.json' if as_json else '.model')}")

  def load(self, model_path: str):
    def is_url(path):
      return path.startswith("http://") or path.startswith("https://")

    if is_url(model_path):
      # print(f"DEBUGG INFO[200] Fetching remote model from: {model_path}")
      with tempfile.NamedTemporaryFile(delete=False, suffix=".model" if model_path.endswith(".model") else ".json") as tmp_file:
        try:
          urllib.request.urlretrieve(model_path.replace("blob/", ""), tmp_file.name)
          model_path = tmp_file.name
        except Exception as e:
          raise RuntimeError(f"Failed to download model from {model_path}: {e}")

    if model_path.endswith(".json"):
      with open(model_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    elif model_path.endswith(".model"):
      with open(model_path, "rb") as f:
        data = pickle.load(f)
    else:
      raise TypeError("Only supports vocab file format `.model` & `.json`")

    self.vocab = data["trained_vocab"]
    self.vocab_size = data.get("vocab_size", len(self.vocab))
    self.kmer = data.get("kmer", self.kmer)
    self.ids_to_token = {v: k for k, v in self.vocab.items()}

  def one_hot_encode(self, sequence):
    tokens = self.tokenize(sequence.upper())
    one_hot = np.zeros((len(tokens), len(self.vocab)), dtype=int)
    for i, token in enumerate(tokens):
      if token in self.vocab:
        one_hot[i, self.vocab[token]] = 1
    return one_hot

  def pad_sequence(self, sequence, target_length, pad_char='-'):
    if len(sequence) >= target_length:
      return sequence[:target_length]
    return sequence + pad_char * (target_length - len(sequence))

  def reverse_complement(self, sequence):
    raise NotImplementedError("Proteins don't have reverse complement! You dumbass!!!")