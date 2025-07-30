import logging
import traceback
from types import MappingProxyType
from typing import Any

import fitz
from pyspark import keyword_only
from pyspark.ml import Transformer
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.pandas import DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import Row

from scaledp.params import (
    HasColumnValidator,
    HasInputCol,
    HasKeepInputData,
    HasOutputCol,
    HasPageCol,
    HasPathCol,
    HasResolution,
)
from scaledp.schemas.Box import Box
from scaledp.schemas.Document import Document


class PdfDataToDocument(
    Transformer,
    HasInputCol,
    HasOutputCol,
    HasKeepInputData,
    HasPathCol,
    HasPageCol,
    DefaultParamsReadable,
    DefaultParamsWritable,
    HasColumnValidator,
    HasResolution,
):
    """Extract text with coordinates from PDF file."""

    DEFAULT_PARAMS = MappingProxyType(
        {
            "inputCol": "content",
            "outputCol": "document",
            "pathCol": "path",
            "pageCol": "page",
            "keepInputData": False,
            "resolution": 300,
        },
    )

    @keyword_only
    def __init__(self, **kwargs: Any) -> None:
        super(PdfDataToDocument, self).__init__()
        self._setDefault(**self.DEFAULT_PARAMS)
        self._set(**kwargs)

    def transform_udf(self, input: Row, path: str) -> list[Document]:
        logging.info("Run Pdf Data to Text")
        try:
            doc = fitz.open("pdf", input)
            if len(doc) == 0:
                raise ValueError("Empty PDF document.")

            page = doc[0]
            # Get the page's transformation matrix and dimensions
            ctm = page.transformation_matrix
            dpi = self.getResolution()  # PDF default DPI

            words = page.get_text("words")
            boxes = []
            text_content = []

            for word in words:
                x0, y0, x1, y1, word_text, _, _, _ = word
                # Convert PDF coordinates to pixel coordinates using the transformation matrix
                # and maintain position relative to DPI
                pixel_x0 = x0 * ctm[0] * (dpi / 72)
                pixel_y0 = abs(y0 * ctm[3] * (dpi / 72))
                pixel_x1 = x1 * ctm[0] * (dpi / 72)
                pixel_y1 = abs(y1 * ctm[3] * (dpi / 72))

                boxes.append(
                    Box(
                        x=int(pixel_x0),
                        y=int(pixel_y0),
                        width=int(pixel_x1 - pixel_x0),
                        height=int(pixel_y1 - pixel_y0),
                        text=word_text,
                        score=1.0,
                    ),
                )
                text_content.append(word_text)

            return Document(
                path=path,
                text=" ".join(text_content),
                type="pdf",
                bboxes=boxes,
            )

        except Exception:
            exception = traceback.format_exc()
            exception = (
                f"{self.uid}: Error during extracting text from "
                f"the PDF document: {exception}"
            )
            logging.warning(exception)
            return [
                Document(
                    path=path,
                    text="",
                    type="pdf",
                    bboxes=[],
                    exception=exception,
                ),
            ]

    def _transform(self, dataset: DataFrame) -> DataFrame:
        out_col = self.getOutputCol()
        input_col = self._validate(self.getInputCol(), dataset)
        path_col = dataset[self.getPathCol()]

        result = dataset.withColumn(
            out_col,
            udf(self.transform_udf, Document.get_schema())(
                input_col,
                path_col,
            ),
        )
        if not self.getKeepInputData():
            result = result.drop(self.getInputCol())
        return result
