import re
from difflib import SequenceMatcher
from typing import Any, List, Optional, Sequence, Union

import numpy as np
import pandas as pd


def clean_text(
    text: str,
    lang: str = "english",
) -> List[str]:
    """
    Cleans a text string by lowercasing, removing punctuation,
    and eliminating stopwords.

    Parameters
    ----------
    text : str
        The input text to clean.
    lang : str, optional
        Language for stopwords (default is 'english').

    Returns
    -------
    List[str]
        A list of cleaned tokens without stopwords or punctuation.

    Notes
    -----
    - Requires NLTK's stopwords and tokenizer (`nltk.download('punkt')`, `nltk.download('stopwords')`).
    """
    if pd.isnull(text):
        return []

    import nltk

    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)

    tokens = word_tokenize(text)
    stop_words = set(stopwords.words(lang))

    return [word for word in tokens if word not in stop_words]


def _jaccard_similarity(
    a: Union[str, int],
    b: Union[str, int],
) -> float:
    """
    Compute the Jaccard similarity between two strings or integers.

    Jaccard similarity is defined as the size of the intersection divided
    by the size of the union of the sets of words from each input.

    Parameters
    ----------
    a : str or int
        First value to compare (will be converted to string).
    b : str or int
        Second value to compare (will be converted to string).

    Returns
    -------
    float
        Jaccard similarity score between 0.0 and 1.0.
    """
    set_a = set(str(a).split())
    set_b = set(str(b).split())
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    return len(intersection) / len(union) if union else 0.0


def _similarity_ratio(
    a: Union[str, int],
    b: Union[str, int],
) -> float:
    """
    Compute the similarity ratio between two strings using SequenceMatcher.

    This function uses difflib.SequenceMatcher to compare the similarity
    between the string representations of two inputs. The output is a
    float between 0.0 (completely different) and 1.0 (identical).

    Parameters
    ----------
    a : str or int
        First value to compare (converted to string).
    b : str or int
        Second value to compare (converted to string).

    Returns
    -------
    float
        Similarity ratio between 0.0 and 1.0.
    """
    return SequenceMatcher(None, str(a), str(b)).ratio()


def compare_text_columns(
    df: pd.DataFrame,
    col1: str = "corpus_text",
    col2: str = "lemmas_nltk_text",
) -> pd.DataFrame:
    """
    Compare two text columns in a DataFrame and compute similarity metrics.

    This function creates a new DataFrame comparing the content of two text columns
    using exact match, Jaccard similarity, and sequence similarity ratio. It also
    compares their lengths and returns only the differing rows.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing two text columns.
    col1 : str, default="corpus_text"
        Name of the first text column to compare.
    col2 : str, default="lemmas_nltk_text"
        Name of the second text column to compare.

    Returns
    -------
    pd.DataFrame
        A DataFrame with similarity metrics and length differences,
        filtered to only show rows where the two columns differ.
    """
    result_df = df[[col1, col2]].copy()

    # Check exact match
    result_df["equal"] = df[col1] == df[col2]

    # Compute Jaccard similarity
    result_df["jaccard_similarity"] = df.apply(
        lambda row: _jaccard_similarity(row[col1], row[col2]), axis=1
    )

    # Compute SequenceMatcher similarity ratio
    result_df["similarity_ratio"] = df.apply(
        lambda row: _similarity_ratio(row[col1], row[col2]), axis=1
    )

    # Compute token lengths
    result_df["len_col1"] = df[col1].str.split().str.len()
    result_df["len_col2"] = df[col2].str.split().str.len()

    result_df["length_difference"] = result_df["len_col1"] - result_df["len_col2"]

    # Return only differing rows
    return result_df[result_df[col1] != result_df[col2]].reset_index(drop=True)


def extract_fasttext_features(
    sentence: Union[str, None],
    model: Optional[Any] = None,  # type: ignore # Should be a gensim.models.KeyedVectors
) -> np.ndarray:
    """
    Extract FastText embedding for a sentence by averaging word vectors.

    If no pre-loaded model is provided, it defaults to loading the
    English FastText vectors ("cc.en.300.vec"). Each word in the sentence
    is looked up in the model, and the average vector is returned.

    Parameters
    ----------
    sentence : str or None
        The input sentence to encode. If None, a zero vector is returned.
    model : gensim.models.KeyedVectors, optional
        Pre-loaded FastText word embedding model. If not provided, the
        English FastText vectors are loaded from disk.

    Returns
    -------
    np.ndarray
        A 1D NumPy array of shape (vector_size,) representing the average
        embedding of the sentence. If no words are found, returns a
        zero vector.
    """
    from gensim.models import KeyedVectors

    if model is None:
        model = KeyedVectors.load_word2vec_format("cc.en.300.vec", binary=False)

    if not sentence:
        return np.zeros(model.vector_size)

    tokens = sentence.lower().split()
    vectors = [model[word] for word in tokens if word in model]

    if not vectors:
        return np.zeros(model.vector_size)

    return np.mean(vectors, axis=0)


def lemmatize_tokens_nltk(
    text: str,
) -> List[str]:
    """
    Tokenize and lemmatize a text string using NLTK.

    This function tokenizes the input text into words and applies WordNet-based
    lemmatization to each token. It also ensures necessary NLTK resources are downloaded.

    Parameters
    ----------
    text : str
        The input text to tokenize and lemmatize.

    Returns
    -------
    List[str]
        A list of lemmatized tokens.
    """
    import nltk

    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)

    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())

    return [lemmatizer.lemmatize(token) for token in tokens]


def lemmatize_tokens_spacy(
    text: str,
    nlp_spacy: Optional[Any] = None,  # type: ignore # Should be a spacy.language.Language
) -> List[str]:
    """
    Tokenize and lemmatize text using spaCy.

    If no spaCy language model is provided, the function loads the English
    small model with parser and named entity recognition disabled for speed.

    Parameters
    ----------
    text : str
        The input text to tokenize and lemmatize.
    nlp_spacy : spacy.language.Language, optional
        A preloaded spaCy language model. If None, 'en_core_web_sm' is loaded.

    Returns
    -------
    List[str]
        A list of lemmatized tokens.
    """
    import spacy

    if nlp_spacy is None:
        nlp_spacy = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    doc = nlp_spacy(text)
    return [token.lemma_ for token in doc]


def lemmatize_tokens_stanza(
    text: str,
    batch_size: int = 64,
    nlp_stanza: Optional[Any] = None,  # type: ignore # Should be a stanza.Pipeline
) -> List[str]:
    """
    Tokenize and lemmatize text using the Stanza NLP pipeline.

    If no Stanza pipeline is provided, one is created with English language
    and appropriate processors enabled (tokenize, MWT, POS, lemma).

    Parameters
    ----------
    text : str
        The input text to process.
    batch_size : int, optional
        Batch size used during pipeline construction (default is 64).
    nlp_stanza : stanza.Pipeline, optional
        A pre-loaded Stanza pipeline. If None, a new English pipeline is initialized.

    Returns
    -------
    List[str]
        A list of lemmatized tokens.
    """
    import stanza

    if nlp_stanza is None:
        nlp_stanza = stanza.Pipeline(
            lang="en",
            processors="tokenize,mwt,pos,lemma",
            tokenize_batch_size=batch_size,
            ner_batch_size=batch_size,
            verbose=False,
        )

    doc = nlp_stanza(text)
    return [word.lemma for sentence in doc.sentences for word in sentence.words]


def list_pred_text(
    df: pd.DataFrame,
    incorrect_only: bool = True,
    limit: int = 5,
    limit_incorrect: int = 1,
    text_col: str = "text",
    y_pred_col: str = "y_pred",
    y_true_col: str = "category_encoded",
    y_true_only_list: Optional[Sequence[Union[int, str]]] = None,
    y_mapping: Optional[dict] = None,
) -> None:
    """
    Print a summary of predicted vs. true labels by text, optionally highlighting incorrect predictions.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing prediction and text data.
    incorrect_only : bool, optional
        If True, only print incorrect predictions. Otherwise, also show correct examples (default: True).
    limit : int, optional
        Max number of texts to display per category/prediction group (default: 5).
    limit_incorrect : int, optional
        Max number of distinct incorrect predicted categories to display per true label (default: 1).
    text_col : str, optional
        Name of the column containing the text (default: "text").
    y_pred_col : str, optional
        Name of the column containing predicted labels (default: "y_pred").
    y_true_col : str, optional
        Name of the column containing true labels (default: "category_encoded").
    y_true_only_list : list, optional
        List of true label values to include in the output (default: None = include all).
    y_mapping : dict, optional
        Optional dictionary mapping class IDs to human-readable labels.

    Returns
    -------
    None
    """

    def _print_text_subset(sub_df: pd.DataFrame, count: int = limit):
        for _, row in sub_df.head(count).iterrows():
            print(f"- {row[text_col]}\n")

    for true_label in sorted(df[y_true_col].unique()):
        if y_true_only_list is not None and true_label not in y_true_only_list:
            continue

        subset = df[df[y_true_col] == true_label]
        correct = subset[subset[y_true_col] == subset[y_pred_col]]
        incorrect = subset[subset[y_true_col] != subset[y_pred_col]]

        label_display = (
            f"{true_label} - {y_mapping[true_label]}" if y_mapping else str(true_label)
        )
        print(label_display + "\n")

        if not incorrect_only and not correct.empty:
            _print_text_subset(correct)
            print()

        if not incorrect.empty:
            top_incorrect_preds = (
                incorrect[y_pred_col].value_counts().head(limit_incorrect).index
            )

            for pred in top_incorrect_preds:
                pred_label = f"{pred} - {y_mapping[pred]}" if y_mapping else str(pred)
                print(f"→ Incorrectly predicted as: {pred_label}\n")

                _print_text_subset(incorrect[incorrect[y_pred_col] == pred])
                print()
