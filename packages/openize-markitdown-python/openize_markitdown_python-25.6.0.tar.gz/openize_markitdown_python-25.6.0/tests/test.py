import pytest
from pathlib import Path
import os

from ..src.openize.markitdown.converters import WordConverter, PDFConverter, ExcelConverter, PowerPointConverter
from ..src.openize.markitdown.factory import ConverterFactory
from ..src.openize.markitdown.llm_strategy import SaveLocally, LLMFactory, OpenAIClient, ClaudeClient
from ..src.openize.markitdown.processor import DocumentProcessor


@pytest.fixture
def sample_output_dir():
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

@pytest.fixture
def sample_md_file(sample_output_dir):
    md_file = sample_output_dir / "sample.md"
    md_file.write_text("# Sample Markdown File\n\nThis is a test.")
    return md_file


# --------- Converter Tests ---------

def test_word_converter():
    converter = WordConverter()
    assert converter is not None

def test_pdf_converter():
    converter = PDFConverter()
    assert converter is not None

def test_excel_converter():
    converter = ExcelConverter()
    assert converter is not None

def test_ppt_converter():
    converter = PowerPointConverter()
    assert converter is not None


# --------- Factory Tests ---------

def test_converter_factory():
    assert isinstance(ConverterFactory.get_converter(".docx"), WordConverter)
    assert isinstance(ConverterFactory.get_converter(".pdf"), PDFConverter)
    assert isinstance(ConverterFactory.get_converter(".xlsx"), ExcelConverter)
    assert isinstance(ConverterFactory.get_converter(".pptx"), PowerPointConverter)


# --------- Strategy Pattern Tests ---------

def test_save_locally(sample_md_file):
    strategy = SaveLocally()
    strategy.process(sample_md_file)
    assert sample_md_file.exists()

def test_insert_into_llm_openai(mocker, sample_md_file):
    mocker.patch("openai.ChatCompletion.create", return_value={
        "choices": [{"message": {"content": "Mocked OpenAI Response"}}]
    })
    strategy = OpenAIClient(provider="openai")
    strategy.process(sample_md_file)

def test_insert_into_llm_claude(mocker, sample_md_file):
    mock_anthropic = mocker.patch("openize.markitdown.llm_strategy.Anthropic")
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value.content = "Mocked Claude Response"
    strategy = ClaudeClient(provider="claude")
    strategy.process(sample_md_file)


# --------- Document Processor Tests ---------

def test_document_processor_local_conversion(mocker, sample_output_dir):
    mock_converter = mocker.patch("openize.markitdown.factory.ConverterFactory.get_converter", return_value=WordConverter())
    processor = DocumentProcessor(output_dir=sample_output_dir)
    processor.process_document("sample.docx", insert_into_llm=False)
    output_file = sample_output_dir / "sample.md"
    assert output_file.exists()

def test_document_processor_with_llm_openai(mocker, sample_output_dir):
    mock_converter = mocker.patch("openize.markitdown.factory.ConverterFactory.get_converter", return_value=WordConverter())
    mocker.patch("openai.ChatCompletion.create", return_value={
        "choices": [{"message": {"content": "LLM Output"}}]
    })
    processor = DocumentProcessor(output_dir=sample_output_dir)
    processor.process_document("sample.docx", insert_into_llm=True, llm_provider="openai")
    output_file = sample_output_dir / "sample.md"
    assert output_file.exists()

def test_document_processor_with_llm_claude(mocker, sample_output_dir):
    mock_converter = mocker.patch("openize.markitdown.factory.ConverterFactory.get_converter", return_value=WordConverter())
    mock_anthropic = mocker.patch("openize.markitdown.llm_strategy.Anthropic")
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.return_value.content = "LLM Claude Output"
    processor = DocumentProcessor(output_dir=sample_output_dir)
    processor.process_document("sample.docx", insert_into_llm=True, llm_provider="claude")
    output_file = sample_output_dir / "sample.md"
    assert output_file.exists()

