from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

def split_text(text):
    """
    Splits the input text into smaller chunks using RecursiveCharacterTextSplitter.

    Args:
        text (str): The input text to be split.

    Returns:
        List[str]: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)