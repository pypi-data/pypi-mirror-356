# MCP server

A simple MCP server by taikt

## Usage

## Example

cd /home/worker/src/codefun/deepl/mcp_server
rm -rf venv
python3 -m venv venv &&  source venv/bin/activate && pip install -e .

## note
Có, rất cần thiết phải có file __init__.py trong thư mục package (ví dụ: mcp_server/) nếu bạn muốn Python nhận diện đó là một package hợp lệ để import (ví dụ: import mcp_server.server). File này có thể rỗng, chỉ cần tồn tại.

File __main__.py không bắt buộc, trừ khi bạn muốn chạy package đó như một module (python -m mcp_server). Đối với trường hợp sử dụng entry point script như mcp-taikt = "mcp_server.server:main", bạn không cần __main__.py, chỉ cần __init__.py là đủ.

Tóm lại:
- __init__.py: Bắt buộc để Python nhận diện package.
- __main__.py: Chỉ cần nếu muốn chạy python -m <package>. Không bắt buộc cho entry point script.