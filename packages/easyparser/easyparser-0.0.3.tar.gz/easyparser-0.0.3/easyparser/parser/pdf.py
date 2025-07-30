import io
import logging
from concurrent.futures import ProcessPoolExecutor

from easyparser.base import BaseOperation, Chunk, ChunkGroup, CType
from easyparser.mime import MimeType, mime_pdf
from easyparser.parser.fastpdf.util import OCRMode, ParserPreset

logger = logging.getLogger(__name__)


class SycamorePDF(BaseOperation):
    """Parsing PDF using sycamore

    Pros:
        - Maintain smaller semantic elements, don't lump into text
        - Have dedicated types for formulas, images, tables
    Cons:
        - Cannot specify extracting images for formulas and tables (data types that
        are easy to misrepresented in text)
    Need:
    """

    supported_mimetypes = ["application/pdf"]
    text_types = {
        "Page-header",
        "Section-header",
        "Title",
        "Caption",
        "Page-footer",
        "List-item",
        "Text",
        "Footnote",
        "table",
        "Table",
    }
    image_types = {"Formula", "Image"}
    _label_mapping = {
        "Formula": CType.Fomula,
        "Page-header": CType.Header,
        "Section-header": CType.Header,
        "Title": CType.Header,
        "Image": CType.Figure,
        "table": CType.Table,
        "Table": CType.Table,
    }

    @classmethod
    def run(
        cls,
        chunk: Chunk | ChunkGroup,
        use_partitioning_service: bool = False,
        extract_table_structure: bool = True,
        use_ocr: bool = True,
        extract_images: bool = True,
        **kwargs,
    ) -> ChunkGroup:
        """Load the PDF with Sycamore PDF extractor.

        This extractor parses all elements in the PDF and return them as chunks. They
        don't lump all text into a single text chunk, but instead maintain the original
        structure of the PDF. It also has dedicated types for formulas, images, and
        tables.

        Args:
            use_partitioning_service: If true, uses the online Aryn
                partitioning service to extract the text from the PDF.
            extract_table_structure: If true, runs a separate table extraction
                model to extract cells from regions of the document identified as
                tables.
            use_ocr: Whether to use OCR to extract text from the PDF. If false,
                we will attempt to extract the text from the underlying PDF.
            extract_images: If true, crops each region identified as an image.
        """
        import sycamore
        from sycamore.data.element import ImageElement
        from sycamore.transforms.partition import ArynPartitioner

        partitioner = ArynPartitioner(
            use_partitioning_service=use_partitioning_service,
            extract_table_structure=extract_table_structure,
            use_ocr=use_ocr,
            extract_images=extract_images,
        )
        context = sycamore.init(exec_mode=sycamore.ExecMode.LOCAL)

        if isinstance(chunk, Chunk):
            chunk = ChunkGroup(chunks=[chunk])

        output = ChunkGroup()
        for pdf_root in chunk:
            logger.info(f"Parsing {pdf_root.origin.location}")
            result = []
            if pdf_root.origin is None:
                raise ValueError("Origin is not defined")
            docset = context.read.binary(
                paths=str(pdf_root.origin.location), binary_format="pdf"
            ).partition(partitioner=partitioner)
            doc = docset.take_all()[0]
            for e in doc.elements:
                origin = None
                if e.bbox:
                    origin = mime_pdf.to_origin(
                        pdf_root,
                        e.bbox.x1,
                        e.bbox.x2,
                        e.bbox.y1,
                        e.bbox.y2,
                        e.properties["page_number"],
                    )

                text = e.text_representation.strip() if e.text_representation else ""
                if e.type in SycamorePDF.text_types:
                    mimetype = MimeType.text
                    content = e.text_representation
                elif isinstance(e, ImageElement):
                    pil_img = e.as_image()
                    if pil_img is None:
                        if not text:
                            continue
                        mimetype = MimeType.text
                        content = text
                    else:
                        mimetype = "image/png"
                        bytes_io = io.BytesIO()
                        pil_img.save(bytes_io, format="PNG")
                        content = bytes_io.getvalue()
                elif e.type in SycamorePDF.image_types:
                    mimetype = "image/png"
                    content = e.binary_representation
                else:
                    raise ValueError(f"Unknown type: {e.type}")

                r = Chunk(
                    mimetype=mimetype,
                    ctype=cls._label_mapping.get(e.type, CType.Para),
                    content=content,
                    # if mimetype is text, it is already in content
                    # content is None will allow .render("markdown")
                    # to work correctly
                    text=text if mimetype != MimeType.text else None,
                    parent=pdf_root,
                    origin=origin,
                )
                result.append(r)

            pdf_root.add_children(result)
            output.append(pdf_root)

        return output

    @classmethod
    def py_dependency(cls) -> list[str]:
        return ["sycamore-ai[local-inference]"]


class FastPDF(BaseOperation):
    """Parsing PDF using a fast and efficient parser"""

    supported_mimetypes = ["application/pdf"]
    _label_mapping = {
        "heading": CType.Header,
        "image": CType.Figure,
        "table": CType.Table,
        "formula": CType.Fomula,
        "text": CType.Para,
    }

    @classmethod
    def run(
        cls,
        chunk: Chunk | ChunkGroup,
        use_layout_parser: bool = True,
        render_full_page: bool = False,
        render_2d_text_paragraph: bool = True,
        render_scale: float = 1.5,
        extract_table: bool = True,
        extract_image: bool = True,
        extract_page: bool = False,
        ocr_mode: OCRMode = OCRMode.AUTO,
        preset: ParserPreset | None = None,
        multiprocessing_executor: ProcessPoolExecutor | None = None,
        debug_path: str | None = None,
        **kwargs,
    ) -> ChunkGroup:
        """Load the PDF with a custom easyparser FastPDF parser.
        This extractor uses efficient models / heuristics to understand
        the layout structure of the PDF and extract text from it. The main
        idea is to balance the speed and accuracy of the extraction process.
        Also, a custom 2D layout text rendering engine is used to export
        the text in a way that preserve original PDF layout,
        which is useful for downstream RAG application.

        Should be used as default parser for PDF files.

        Args:
            chunk: The input chunk to process.
            use_layout_parser: If true, uses the layout parser to extract text.
                Otherwise, uses the heuristic parser based on the PDF metadata
                and image-based processing.
            render_full_page: If true, renders the full page as 2D layout text.
            render_2d_text_paragraph: If true, auto-detects text paragraphs that
                should be represented as 2D layout and render them.
            render_scale: The scale factor for rendering image content
                (table / figure).
            extract_table: If true, extracts tables from the PDF.
                Only used in non-layout parser mode.
            extract_image: If true, extracts images from the PDF.
            extract_page: If true, extracts the page image from the PDF
                as a parent chunk of other elements.
                Useful for app which requires indexing full page
                as well as child elements.
            ocr_mode: The OCR mode to use. Can be "auto", "off", or "on".
                "auto" will use OCR only if the text is not extractable from the PDF.
                "off" will not use OCR at all.
                "on" will always use OCR instead of current embedded text.
            preset: The quick config preset to use for the parser e.g: "best", "fast".
            multiprocessing_executor: The executor to use for multiprocessing.
                Only used in non-layout parser mode.
            debug_path: The path to save the debug images.
                If None, no debug images will be generated.
        """
        from .fastpdf.pdf_heuristic_parser import parition_pdf_heuristic
        from .fastpdf.pdf_layout_parser import partition_pdf_layout

        if isinstance(chunk, Chunk):
            chunk = ChunkGroup(chunks=[chunk])

        # resolve parser preset if specified
        if preset == ParserPreset.BEST:
            render_full_page = False
            use_layout_parser = True
            extract_image = True
            ocr_mode = OCRMode.AUTO
        elif preset == ParserPreset.BEST_NO_OCR:
            render_full_page = False
            use_layout_parser = True
            extract_image = True
            ocr_mode = OCRMode.OFF
        elif preset == ParserPreset.FAST:
            render_full_page = False
            use_layout_parser = False
            extract_image = False
            extract_table = False
            ocr_mode = OCRMode.OFF
        elif preset == ParserPreset.FAST_2D:
            render_full_page = True
            ocr_mode = OCRMode.AUTO

        logger.debug(
            f"Using preset: {preset}, "
            f"Parser settings: "
            f"render_full_page={render_full_page}, "
            f"use_layout_parser={use_layout_parser}, "
            f"extract_image={extract_image}, "
            f"extract_table={extract_table}, "
            f"ocr_mode={ocr_mode}, "
        )

        output = ChunkGroup()
        for pdf_root in chunk:
            logger.info(f"Parsing {pdf_root.origin.location}")
            result = []
            if pdf_root.origin is None:
                raise ValueError("Origin is not defined")

            # call the main function to partition the PDF
            if use_layout_parser or render_full_page:
                pages = partition_pdf_layout(
                    str(pdf_root.origin.location),
                    render_scale=render_scale,
                    render_full_page=render_full_page,
                    render_2d_text_paragraph=render_2d_text_paragraph,
                    extract_image=extract_image,
                    extract_page=extract_page,
                    ocr_mode=ocr_mode,
                    debug_path=debug_path,
                )
            else:
                pages = parition_pdf_heuristic(
                    str(pdf_root.origin.location),
                    render_scale=render_scale,
                    executor=multiprocessing_executor,
                    extract_table=extract_table,
                    extract_image=extract_image,
                    extract_page=extract_page,
                )

            for page in pages:
                page_label = page["page"] + 1
                page_chunks = []
                for block in page["blocks"]:
                    text = block["text"]
                    image_content = block.get("image")
                    if image_content:
                        mimetype = "image/png"
                        content = image_content
                    else:
                        mimetype = MimeType.text
                        content = text
                    x1, y1, x2, y2 = block["bbox"]

                    origin = mime_pdf.to_origin(
                        pdf_root,
                        x1,
                        x2,
                        y1,
                        y2,
                        page_label,
                    )
                    c = Chunk(
                        ctype=cls._label_mapping.get(block["type"], CType.Para),
                        mimetype=mimetype,
                        content=content,
                        text=text if mimetype != MimeType.text else None,
                        parent=pdf_root,
                        origin=origin,
                    )
                    page_chunks.append(c)

                if extract_page:
                    page_image = page.get("page_image")
                    page_text = page.get("page_text")
                    if page_image:
                        mimetype = "image/png"
                        page_content = page_image
                    else:
                        mimetype = MimeType.text
                        page_content = page_text
                    origin = mime_pdf.to_origin(
                        pdf_root,
                        0,
                        0,
                        1,
                        1,
                        page_label,
                    )
                    c = Chunk(
                        ctype=CType.Page,
                        mimetype=mimetype,
                        content=page_content,
                        text=page_text,
                        parent=pdf_root,
                        origin=origin,
                    )
                    c.add_children(page_chunks)
                    result.append(c)
                else:
                    result.extend(page_chunks)

            pdf_root.add_children(result)
            output.append(pdf_root)

        return output

    @classmethod
    def py_dependency(cls) -> list[str]:
        return [
            "chunking-pdftext",
            "img2table",
            "Pillow",
            "rapid-layout",
        ]


class UnstructuredPDF(BaseOperation):
    supported_mimetypes = ["application/pdf"]
    text_types = {
        "Title",
        "Text",
        "UncategorizedText",
        "NarrativeText",
        "BulletedText",
        "Paragraph",
        "Abstract",
        "Threading",
        "Form",
        "Field-Name",
        "Value",
        "Link",
        "CompositeElement",
        "FigureCaption",
        "Caption",
        "List",
        "ListItem",
        "List-item",
        "Checked",
        "Unchecked",
        "CheckBoxChecked",
        "CheckBoxUnchecked",
        "RadioButtonChecked",
        "RadioButtonUnchecked",
        "Address",
        "EmailAddress",
        "PageBreak",
        "Header",
        "Headline",
        "Subheadline",
        "Page-header",
        "Section-header",
        "Footer",
        "Footnote",
        "Page-footer",
        "PageNumber",
        "CodeSnippet",
        "FormKeysValues",
    }
    image_types = {
        "Image",
        "Picture",
        "Figure",
        "Formula",
        "Table",
    }
    _label_mapping = {
        "Title": CType.Header,
        "Checked": CType.Inline,
        "Unchecked": CType.Inline,
        "CheckBoxChecked": CType.Inline,
        "CheckBoxUnchecked": CType.Inline,
        "RadioButtonChecked": CType.Inline,
        "RadioButtonUnchecked": CType.Inline,
        "Header": CType.Header,
        "Headline": CType.Header,
        "Subheadline": CType.Header,
        "Section-header": CType.Header,
        "Image": CType.Figure,
        "Picture": CType.Figure,
        "Figure": CType.Figure,
        "Formula": CType.Fomula,
        "Table": CType.Table,
    }

    @classmethod
    def run(
        cls, chunk: Chunk | ChunkGroup, strategy: str = "hi_res", **kwargs
    ) -> ChunkGroup:
        """Parse the PDF using the unstructured partitioning service.

        Args:
            strategy: The strategy to use for partitioning the PDF. Valid
                strategies are "hi_res", "ocr_only", and "fast". When using the
                "hi_res" strategy, the function uses a layout detection model to
                identify document elements. When using the "ocr_only" strategy,
                partition_pdf simply extracts the text from the document using OCR
                and processes it. If the "fast" strategy is used, the text is
                extracted directly from the PDF. The default strategy `auto` will
                determine when a page can be extracted using `fast` mode, otherwise
                it will fall back to `hi_res`.
        """
        import base64

        from unstructured.partition.pdf import partition_pdf

        if isinstance(chunk, Chunk):
            chunk = ChunkGroup(chunks=[chunk])

        output = ChunkGroup()
        for pdf_root in chunk:
            logger.info(f"Parsing {pdf_root.origin.location}")
            result = []
            if pdf_root.origin is None:
                raise ValueError("Origin is not defined")

            file_path = pdf_root.origin.location
            elements = partition_pdf(
                file_path,
                strategy=strategy,
                infer_table_structure=True,
                extract_image_block_types=list(UnstructuredPDF.image_types),
                extract_image_block_to_payload=True,
                **kwargs,
            )
            for e in elements:
                origin = None
                if coord := e.metadata.coordinates:
                    x1, y1 = coord.points[0]
                    x2, y2 = coord.points[2]
                    width, height = coord.system.width, coord.system.height
                    origin = mime_pdf.to_origin(
                        pdf_root,
                        float(x1 / width),
                        float(x2 / width),
                        float(y1 / height),
                        float(y2 / height),
                        e.metadata.page_number,
                    )
                if e.category == "Table":
                    text = e.metadata.text_as_html
                    if text is None:
                        text = e.text
                else:
                    text = e.text
                if e.category in UnstructuredPDF.text_types:
                    mimetype = MimeType.text
                    content = e.text
                elif e.category in UnstructuredPDF.image_types:
                    if not e.metadata.image_base64 or not e.metadata.image_mime_type:
                        continue
                    mimetype = e.metadata.image_mime_type
                    content = base64.b64decode(e.metadata.image_base64)
                else:
                    raise ValueError(f"Unknown type: {e.category}")

                result.append(
                    Chunk(
                        ctype=cls._label_mapping.get(e.category, CType.Para),
                        mimetype=mimetype,
                        content=content,
                        text=text if mimetype != MimeType.text else None,
                        parent=pdf_root,
                        origin=origin,
                        metadata={"lang": e.metadata.languages},
                    )
                )

            pdf_root.add_children(result)
            output.append(pdf_root)

        return output

    @classmethod
    def py_dependency(cls) -> list[str]:
        return ["unstructured[pdf]"]


class DoclingPDF(BaseOperation):
    supported_mimetypes = ["application/pdf"]
    _label_mapping = {  # taken from docling.types.doc.labels.DocItemLabel
        "caption": CType.Para,
        "footnote": CType.Para,
        "formula": CType.Fomula,
        "list_item": CType.List,
        "page_footer": CType.Para,
        "page_header": CType.Para,
        "picture": CType.Figure,
        "section_header": CType.Header,
        "table": CType.Table,
        "text": CType.Para,
        "title": CType.Header,
        "document_index": CType.Para,
        "code": CType.Code,
        "checkbox_selected": CType.List,
        "checkbox_unselected": CType.List,
        "form": CType.Div,
        "key_value_region": CType.Inline,
    }

    @classmethod
    def run(
        cls,
        chunk: Chunk | ChunkGroup,
        do_ocr: bool = True,
        do_table_structure: bool = True,
        generate_picture_images: bool = True,
        images_scale: float = 2.0,
        num_thread: int = 8,
        device: str = "auto",
        **kwargs,
    ) -> ChunkGroup:
        """Load the PDF with Docling PDF extractor.

        This extractor parses all elements in the PDF and return them as chunks. They
        don't lump all text into a single text chunk, but instead maintain the original
        structure of the PDF.

        It has dedicated types for formulas, images, tables and headers.

        It can build hierarchical structure of the chunks based on the layout of the
        PDF (e.g. headers, sections, subsections).

        Args:
            do_ocr: if True, perform OCR on the PDF, otherwise extract text from the
                PDF programmatically.
            do_table_structure: if True, extract the table structure from the PDF.
            generate_picture_images: if True, generate images for pictures in the PDF.
            images_scale: the scale factor for the images generated from the PDF.
            num_thread: the number of threads to use for processing the PDF.
            device: the device to use for processing the PDF, can be "auto", "cpu",
                "cuda", or "mps".
        """
        from io import BytesIO

        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import (
            AcceleratorOptions,
            PdfPipelineOptions,
        )
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling_core.types.doc.document import GroupItem, PictureItem, TableItem

        accelerator_options = AcceleratorOptions(num_threads=num_thread, device=device)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.accelerator_options = accelerator_options
        pipeline_options.do_ocr = do_ocr
        pipeline_options.do_table_structure = do_table_structure
        pipeline_options.generate_picture_images = generate_picture_images
        pipeline_options.images_scale = images_scale

        docling_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                )
            }
        )

        if isinstance(chunk, Chunk):
            chunk = ChunkGroup(chunks=[chunk])

        output = ChunkGroup()
        for pdf_root in chunk:
            logger.info(f"Parsing {pdf_root.origin.location}")
            result = []
            doc = docling_converter.convert(pdf_root.origin.location).document
            parent_chunk_stacks = []
            last_chunk = pdf_root
            prev_lvl = 0
            for idx, (e, lvl) in enumerate(
                doc.iterate_items(doc.body, with_groups=True)
            ):
                if isinstance(e, GroupItem):
                    continue
                if lvl > prev_lvl:
                    # move down a hirearchy
                    parent_chunk_stacks.append(last_chunk)
                elif lvl < prev_lvl:
                    # move up a hirearchy
                    last_chunk = parent_chunk_stacks[-1]
                    parent_chunk_stacks = parent_chunk_stacks[:-1]

                # track the lvl
                prev_lvl = lvl
                if isinstance(e, PictureItem):
                    mimetype = "image/png"
                    pil_image = e.get_image(doc)
                    if pil_image is None:
                        continue
                    buffered = BytesIO()
                    pil_image.save(buffered, format="PNG")
                    content = buffered.getvalue()
                    text = e.caption_text(doc)
                elif isinstance(e, TableItem):
                    mimetype = MimeType.text
                    content = e.export_to_markdown()
                    text = content
                else:
                    mimetype = MimeType.text
                    content = e.text
                    text = e.text

                prov = e.prov[0]
                page_no = prov.page_no
                w, h = doc.pages[page_no].size.width, doc.pages[page_no].size.height
                x1, x2 = prov.bbox.l / w, prov.bbox.r / w
                t, b = prov.bbox.t, prov.bbox.b
                y1, y2 = (h - t) / h, (h - b) / h
                c = Chunk(
                    ctype=cls._label_mapping.get(e.label, CType.Para),
                    mimetype=mimetype,
                    content=content,
                    text=text if mimetype != MimeType.text else None,
                    parent=parent_chunk_stacks[-1],
                    origin=mime_pdf.to_origin(pdf_root, x1, x2, y1, y2, page_no),
                )
                result.append(c)

            pdf_root.add_children(result)
            output.append(pdf_root)

        return output

    @classmethod
    def py_dependency(cls) -> list[str]:
        return ["docling"]


# def pdf_by_extractous(file_path: Path | str) -> list[Snippet]:
#     try:
#         from extractous import Extractor
#     except ImportError:
#         raise ImportError("Please install `pip install extractous`")

#     file_path = Path(file_path)
#     extr = Extractor()
#     result, metadata = extr.extract_file_to_string(str(file_path))
#     return [
#         Snippet(
#             id=Path(file_path).stem,
#             text=result,
#             content=result,
#             dtype="text",
#             origin=Origin(
#                 source_id=file_path.as_posix(),
#                 location={},
#                 getter="",
#                 file_type="pdf",
#             ),
#             metadata=metadata,
#         )
#     ]


# def pdf_by_vlm(file_path: Path | str, **kwargs) -> list[Snippet]: ...
