# colav-proto

[![PyPI - Version](https://img.shields.io/pypi/v/colav-proto.svg)](https://pypi.org/project/colav-proto)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/colav-proto.svg)](https://pypi.org/project/colav-proto)

A project for generating, serializing and deserializing COLAV protobuf interfaces. Providing interfaces for generation of all the different protos required as well as different types and constants related.

-----

## Table of Contents

- [Installation](#installation)
- [Structure](#structure)
- [Usage](#usage)
- [License](#license)

## Installation

```bash
pip install colav-proto
```

## Structure

The source code in [colav_proto](https://github.com/RyanMcKeeQUB/colav-proto) is organized into the following main directories:


## Usage

Once the package has been installed into your environment, usage is simple.

### Imports

```python
```

### Sample Mission Request Creation

```python
```

### Sample Serialization

```python
serialized_msg = serialize_protobuf(mission_req_proto)
```

### Sample Deserialization

```python
deserialized_msg = deserialize_protobuf(serialized_msg)
```

## License

`colav-proto` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
