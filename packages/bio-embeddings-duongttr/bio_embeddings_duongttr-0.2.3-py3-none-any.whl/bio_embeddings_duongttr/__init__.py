"""
The functionality of bio_embeddings is split into 5 different modules

.. autosummary::
   bio_embeddings.embed
   bio_embeddings.extract
   bio_embeddings.project
   bio_embeddings.utilities
   bio_embeddings.visualize
"""

import bio_embeddings_duongttr.embed
import bio_embeddings_duongttr.extract
import bio_embeddings_duongttr.project
import bio_embeddings_duongttr.utilities
import bio_embeddings_duongttr.visualize

__all__ = ["embed", "extract", "project", "utilities", "visualize"]
