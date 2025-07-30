# recordlogger

A simple Python utility for recording variable information during runtime, including type, value, line number, file, and function context. Log entries are stored in a MongoDB collection.

## Features

- Record the name, type, value, line number, file, and function of any variable.
- Automatically detects context when not provided.
- Designed for easy integration into debugging or logging workflows.

## Installation

pip install record

## Requirements

- Python 3.6+
- MongoDB (for the collection object)
- `pymongo` (for MongoDB interaction)

## License

This project is licensed under the MIT License.
