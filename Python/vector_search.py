#!/usr/bin/env python3
# Adapted from: Learn Vector Search By Building Simple Example from Scratch --> https://medium.com/@learn-simplified/learn-vector-search-by-building-simple-example-from-scratch-8e978d56eb40
import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd
import time
from collections import defaultdict
from matplotlib import rcParams
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer as TfidfVectoriser
from sklearn.metrics.pairwise import cosine_similarity

# Monkey patching NumPy for compatibility with version >= 1.24
np.float = np.float64
np.int = np.int_
np.object = np.object_
np.bool = np.bool_

# Define constants
GOLDEN_RATIO = 1.618033989
FIG_WIDTH = 12
FIG_HEIGHT = FIG_WIDTH / GOLDEN_RATIO
FIG_SIZE = (FIG_WIDTH, FIG_HEIGHT)
FIG_DPI = 96
RANDOM_SAMPLE_SIZE = 13
RANDOM_SEED = 42
ALPHA_VALUE = 0.05

# Plotting parameters
rcParams["figure.figsize"] = FIG_SIZE
rcParams["figure.dpi"] = FIG_DPI
rcParams["savefig.format"] = "svg"

class SimpleVectorSearch:
    def __init__(self):
        self.documents = []
        self.vectors = None
        self.vectoriser = TfidfVectoriser(
            stop_words="english",
            lowercase=True,
            max_features=1000,
        )

    def add_documents(self, docs):
        """
        Add documents to the collection of documents.

        Parameters
        ----------
        docs : list of str
            List of documents to add to the collection.

        Returns
        -------
        None
        """
        self.documents.extend(docs)
        self.vectors = self.vectoriser.fit_transform(self.documents)
        print(f"Added {len(docs)} documents. Total documents: {len(self.documents)}")
        print(f"Shape of vectors: {self.vectors.shape}")

    def search(self, query, top_k=5):
        """
        Search for documents that are similar to the query.

        Parameters
        ----------
        query : str
            The query string to search for.
        top_k : int, optional
            The number of top results to return. Default is 5.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains the
            document string, the similarity score, and the index of the document.
        """
        if self.vectors is None:
            return []

        # Transform query to vector space
        query_vector = self.vectoriser.transform([query])

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(query_vector, self.vectors)[0]

        # Get top k results
        top_indices = similarity_scores.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "similarity": similarity_scores[idx],
                "index": idx,
            })

        return results


# Create our test documents
documents = [
    "Python is a powerful programming language for data science and machine learning",
    "Machine learning algorithms can identify patterns in large datasets",
    "Deep learning uses neural networks with multiple layers",
    "Data visualisation helps understand complex datasets and patterns",
    "Natural language processing enables computers to understand human language",
    "Computer vision allows machines to interpret and analyse visual information",
    "Web development with Python involves frameworks like Django and Flask",
    "Database management is crucial for storing and retrieving data efficiently",
    "Cloud computing provides scalable infrastructure for modern applications",
    "Artificial intelligence is transforming various industries and applications"
]

# Initialise search engine
search_engine = SimpleVectorSearch()
search_engine.add_documents(documents)


def demonstrate_search(search_engine, query, top_k=3):
    """
    Demonstrate how to search for documents that are similar to the query.

    Parameters
    ----------
    search_engine : SimpleVectorSearch
        The search engine object to use for searching.
    query : str
        The query string to search for.
    top_k : int, optional
        The number of top results to return. Default is 3.

    Returns
    -------
    None
    """
    print(f"\n🔍 Searching for: '{query}'")
    print("=" * 50)

    results = search_engine.search(query, top_k=top_k)

    for i, result in enumerate(results, 1):
        print(f"{i}: Similarity: {result['similarity']:.4f}")
        print(f"Document: {result['document']}")
        print()


# Test different queries
demonstrate_search(search_engine, "neural networks and deep learning")
demonstrate_search(search_engine, "python web frameworks")
demonstrate_search(search_engine, "data analysis and visualisation")


def visualise_vector_space(search_engine, query=None):
    """
    Visualise the vector space of the search engine.

    Reduce the dimensionality of the search engine's vector space to 2D using PCA.
    Plot the documents and their corresponding labels.
    If a query is provided, plot the query vector in addition to the document vectors.

    Parameters
    ----------
    search_engine : SimpleVectorSearch
        The search engine object to visualise.
    query : str, optional
        The query string to visualise. Default is None.

    Returns
    -------
    vectors_2d : numpy.ndarray
        The 2D vector representation of the search engine's vector space.
    """
    # Reduce dimensions to 2D for visualisation
    pca = PCA(n_components=2)
    vectors_2d = pca.fit_transform(search_engine.vectors.toarray())

    # Plot documents
    plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], c="lightblue", s=100, alpha=0.7, label="Documents")

    # Add document labels
    for i, (x, y) in enumerate(vectors_2d):
        plt.annotate(f"Doc {i + 1}", (x, y), xytext=(5, 5), textcoords="offset points", fontsize=9, alpha=0.8)

    # If query provided, show query vector
    if query:
        query_vector = search_engine.vectoriser.transform([query])
        query_vector_2d = pca.transform(query_vector.toarray())
        plt.scatter(query_vector_2d[0, 0], query_vector_2d[0, 1], c="red", s=100, marker="*", label=f"Query: '{query}'")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return vectors_2d


# Visualise the vector space
vectors_2d = visualise_vector_space(search_engine, "machine learning algorithms")



def explain_cosine_similarity(vector_a, vector_b, num_dp=3, messages=True):
    """
    Explain how cosine similarity is calculated between two vectors.

    Parameters
    ----------
    vector_a : numpy.ndarray
        The first vector to calculate cosine similarity for.
    vector_b : numpy.ndarray
        The second vector to calculate cosine similarity for.
    num_dp : int, optional
        The number of decimal places to round the results to. Default is 3.
    messages : bool, optional
        Whether to print out the calculations and results. Default is True.

    Returns
    -------
    float
        The cosine similarity between the two vectors.
    """
    # Calculate dot product
    dot_product = np.dot(vector_a, vector_b)

    # Calculate magnitude of vectors
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    # Calculate cosine similarity
    cosine_sim = dot_product / (magnitude_a * magnitude_b)

    if messages:
        print(f"Vector A: {vector_a}")
        print(f"Vector B: {vector_b}")
        print(f"Dot Product: {dot_product:.{num_dp}f}")
        print(f"Magnitude A: {magnitude_a:.{num_dp}f}")
        print(f"Magnitude B: {magnitude_b:.{num_dp}f}")
        print(f"Cosine Similarity: {cosine_sim:.{num_dp}f}")

    return cosine_sim


# Example with simple 3D vectors
vec_a = np.array([1, 2, 3])
vec_b = np.array([2, 3, 4])
explain_cosine_similarity(vec_a, vec_b)


class AdvancedVectorSearch(SimpleVectorSearch):
    def __init__(self):
        super().__init__()
        self.metadata = []

    def add_documents_with_metadata(self, docs_with_meta):
        """
        Add documents with metadata to the search engine.

        Parameters
        ----------
        docs_with_meta : list of dict
            A list of dictionaries where each dictionary contains a "text" key with the document text and a "metadata" key with the document metadata.

        Returns
        -------
        None
        """
        docs = [item["text"] for item in docs_with_meta]
        meta = [item["metadata"] for item in docs_with_meta]

        self.documents.extend(docs)
        self.metadata.extend(meta)

        # Re-fit vectoriser with all documents
        self.vectors = self.vectoriser.fit_transform(self.documents)
        print(f"Added {len(docs)} documents with metadata")

    def search_with_filters(self, query, filters=None, top_k=5):
        """
        Search for documents that are similar to the query, with optional filters.

        Parameters
        ----------
        query : str
            The query string to search for.
        filters : dict, optional
            A dictionary of metadata filters to apply to the search results.
            For example, {"author": "John Doe"} would filter the results to only include documents with the author "John Doe".
        top_k : int, optional
            The number of top results to return. Default is 5.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains the
            document string, the similarity score, the document metadata, and the index of the document.
        """
        if self.vectors is None:
            return []

        # Get basic similarity scores
        query_vector = self.vectoriser.transform([query])
        similarity_scores = cosine_similarity(query_vector, self.vectors)[0]

        # Apply filters if provided
        valid_indices = np.arange(len(self.documents))
        if filters:
            valid_indices = []
            for i, meta in enumerate(self.metadata):
                match = True
                for key, value in filters.items():
                    if meta.get(key) != value:
                        match = False
                        break
                if match:
                    valid_indices.append(i)

        # Filter similarities and get top results
        filtered_similarities = [(i, similarity_scores[i]) for i in valid_indices]
        filtered_similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, (doc_idx, sim) in enumerate(filtered_similarities[:top_k]):
            results.append({
                "document": self.documents[doc_idx],
                "metadata": self.metadata[doc_idx],
                "similarity": sim,
                "index": doc_idx,
            })

        return results



# Test with metadata
advanced_search = AdvancedVectorSearch()

docs_with_metadata = [
    {
        "text": "Python machine learning with scikit-learn and pandas",
        "metadata": {"category": "programming", "difficulty": "intermediate", "language": "python"}
    },
    {
        "text": "JavaScript web development with React and Node.js",
        "metadata": {"category": "programming", "difficulty": "advanced", "language": "javascript"}
    },
    {
        "text": "Deep learning neural networks using TensorFlow",
        "metadata": {"category": "ai", "difficulty": "advanced", "language": "python"}
    },
    {
        "text": "Database design and SQL optimisation techniques",
        "metadata": {"category": "database", "difficulty": "intermediate", "language": "sql"}
    }
]

advanced_search.add_documents_with_metadata(docs_with_metadata)

# Search with filters
print("\n🔍 Searching for 'machine learning' with Python filter:")
results = advanced_search.search_with_filters(
    "machine learning",
    filters={"language": "python"},
    top_k=3
)

for result in results:
    print(f"Similarity: {result['similarity']:.4f}")
    print(f"Document: {result['document']}")
    print(f"Metadata: {result['metadata']}")
    print()


def benchmark_search(search_engine, num_queries=100, num_dp=3, show_figure=True, messages=True):
    """
    Benchmark the search engine with a given number of queries.

    Parameters
    ----------
    search_engine : SimpleVectorSearch
        The search engine object to benchmark.
    num_queries : int, optional
        The number of queries to run. Default is 100.
    num_dp : int, optional
        The number of decimal places to display the average, standard deviation, min, and max search times. Default is 3.
    show_figure : bool, optional
        Whether to show the search time distribution figure. Default is True.
    messages : bool, optional
        Whether to display the performance analysis messages. Default is True.

    Returns
    -------
    list
        A list of search times in seconds.
    """
    queries = [
        "machine learning algorithms",
        "web development frameworks",
        "data visualisation tools",
        "neural network training",
        "database optimisation"
    ]

    times_ns = []
    times = []

    for i in range(num_queries):
        query = queries[i % len(queries)]
        tic = time.perf_counter_ns()
        results = search_engine.search(query, top_k=5)
        toc = time.perf_counter_ns()
        times_ns.append((toc - tic))
        times.append((toc - tic) / 1e9)

    avg_time_ns, std_time_ns = np.mean(times_ns), np.std(times_ns)

    if messages:
        print(f"Performance Analysis ({num_queries} queries):")
        print(f"Average search time: {avg_time_ns / 1e6:.{num_dp}f} ms")
        print(f"Standard deviation: {std_time_ns / 1e6:.{num_dp}f} ms")
        print(f"Min time: {np.min(times_ns) / 1e6:.{num_dp}f} ms")
        print(f"Max time: {np.max(times_ns) / 1e6:.{num_dp}f} ms")

    if show_figure:
        plt.hist(times, bins=20, alpha=0.7, color="skyblue", edgecolor="black")
        plt.xlabel("Search Time (seconds)")
        plt.ylabel("Frequency")
        plt.title(f"Search Performance Distribution ({num_queries} queries)")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    return times

# Benchmark our search engine
benchmark_times = benchmark_search(search_engine)


class ScalableVectorSearch(SimpleVectorSearch):
    def __init__(self, batch_size=100):
        super().__init__()
        self.batch_size = batch_size
        self.needs_reindex = False

    def add_document_batch(self, new_docs):
        """
        Add a batch of documents to the search engine.

        This method adds the new documents to the collection of documents
        and marks the search engine as needing re-indexing.

        If the number of new documents is greater than or equal to
        the batch size, the search engine is re-indexed immediately.

        Parameters
        ----------
        new_docs : list of str
            The list of new documents to add to the search engine.

        Returns
        -------
        None
        """
        self.documents.extend(new_docs)
        self.needs_reindex = True

        if len(new_docs) >= self.batch_size:
            self.reindex()

    def reindex(self):
        """
        Re-index the search engine.

        This method re-indexes the search engine by fitting the
        vectoriser to the current collection of documents and
        transforming the documents to their corresponding vector
        representations.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.needs_reindex:
            print(f"Re-indexing {len(self.documents)} documents...")
            self.vectors = self.vectoriser.fit_transform(self.documents)
            self.needs_reindex = False
            print("Re-indexing complete!")

    def search(self, query, top_k=5):
        """
        Search for documents that are similar to the query.

        If the search engine needs re-indexing, this method will
        re-index the search engine before searching.

        Parameters
        ----------
        query : str
            The query string to search for.
        top_k : int, optional
            The number of top results to return. Default is 5.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains the
            document string, the similarity score, and the index of the document.
        """
        if self.needs_reindex:
            self.reindex()
        return super().search(query, top_k)

# Example usage
scalable_search = ScalableVectorSearch(batch_size=5)

# Add documents in batches
scalable_search.add_document_batch(["Document 1", "Document 2", "Document 3"])
scalable_search.add_document_batch(["Document 4", "Document 5", "Document 6"])
scalable_search.add_document_batch(["Document 7", "Document 8", "Document 9"])
