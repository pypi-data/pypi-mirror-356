from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import find_text_in_pdf, find_table_in_pdf
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool(name="find_text")
async def find_text(
    url: str = Field(
        description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    searchString: str = Field(
        description="Text to search. Can support regular expressions if regexSearch is set to True."
    ),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    pages: str = Field(
        description="Comma-separated list of page indices (or ranges) to process. Leave empty for all pages. Example: '0,2-5,7-'. The first-page index is 0. (Optional)",
        default="",
    ),
    wordMatchingMode: str = Field(
        description="Values can be either SmartMatch, ExactMatch, or None. (Optional)",
        default=None,
    ),
    password: str = Field(
        description="Password of the PDF file. (Optional)", default=""
    ),
    regexSearch: bool = Field(
        description="Set to True to enable regular expressions in the search string. (Optional)",
        default=False,
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    Find text in PDF and get coordinates. Supports regular expressions.
    Ref: https://developer.pdf.co/api-reference/pdf-find/basic.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        pages=pages,
        password=password,
    )

    return await find_text_in_pdf(
        params, searchString, regexSearch, wordMatchingMode, api_key=api_key
    )


@mcp.tool(name="find_table")
async def find_table(
    url: str = Field(
        description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    pages: str = Field(
        description="Comma-separated list of page indices (or ranges) to process. Leave empty for all pages. Example: '0,2-5,7-'. The first-page index is 0. (Optional)",
        default="",
    ),
    password: str = Field(
        description="Password of the PDF file. (Optional)", default=""
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    Find tables in PDF and get their coordinates.
    Ref: https://developer.pdf.co/api-reference/pdf-find/table.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        pages=pages,
        password=password,
    )

    return await find_table_in_pdf(params, api_key=api_key)
