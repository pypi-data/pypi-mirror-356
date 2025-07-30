#  Copyright (c) 2024. Rapida
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
#  Author: Prashant <prashant@rapida.ai>

from enum import Enum
import logging

from rapida.artifacts.protos import common_pb2, common_pb2_grpc


class RapidaSource(Enum):
    """
    Rapida Source
    """

    WEB_PLUGIN = "web-plugin"
    RAPIDA_APP = "rapida-app"
    DEBUGGER = "debugger"

    # language SDKs
    PYTHON_SDK = "python-sdk"
    NODE_SDK = "node-sdk"
    GO_SDK = "go-sdk"
    JAVA_SDK = "java-sdk"
    PHP_SDK = "php-sdk"
    RUST_SDK = "rust-sdk"
    REACT_SDK = "react-sdk"

    # extensions
    TWILIO_CALL = "twilio-call"

    MAPPING = {
        WEB_PLUGIN: common_pb2.Source.WEB_PLUGIN,
        RAPIDA_APP: common_pb2.Source.RAPIDA_APP,
        PYTHON_SDK: common_pb2.Source.PYTHON_SDK,
        NODE_SDK: common_pb2.Source.NODE_SDK,
        GO_SDK: common_pb2.Source.GO_SDK,
        JAVA_SDK: common_pb2.Source.JAVA_SDK,
        PHP_SDK: common_pb2.Source.PHP_SDK,
        RUST_SDK: common_pb2.Source.RUST_SDK,
        REACT_SDK: common_pb2.Source.REACT_SDK,
        TWILIO_CALL: common_pb2.Source.TWILIO_CALL,
    }

    def get(self) -> str:
        return str(self.value)

    def source(self) -> common_pb2.Source:
        mapping = {
            RapidaSource.WEB_PLUGIN: common_pb2.Source.WEB_PLUGIN,
            RapidaSource.RAPIDA_APP: common_pb2.Source.RAPIDA_APP,
            RapidaSource.PYTHON_SDK: common_pb2.Source.PYTHON_SDK,
            RapidaSource.NODE_SDK: common_pb2.Source.NODE_SDK,
            RapidaSource.GO_SDK: common_pb2.Source.GO_SDK,
            RapidaSource.JAVA_SDK: common_pb2.Source.JAVA_SDK,
            RapidaSource.PHP_SDK: common_pb2.Source.PHP_SDK,
            RapidaSource.RUST_SDK: common_pb2.Source.RUST_SDK,
            RapidaSource.REACT_SDK: common_pb2.Source.REACT_SDK,
            RapidaSource.TWILIO_CALL: common_pb2.Source.TWILIO_CALL,
        }
        return mapping.get(self)

    @staticmethod
    def from_str(label: str):
        source_map = {
            "web-plugin": RapidaSource.WEB_PLUGIN,
            "rapida-app": RapidaSource.RAPIDA_APP,
            "debugger": RapidaSource.DEBUGGER,
            "python-sdk": RapidaSource.PYTHON_SDK,
            "node-sdk": RapidaSource.NODE_SDK,
            "go-sdk": RapidaSource.GO_SDK,
            "java-sdk": RapidaSource.JAVA_SDK,
            "php-sdk": RapidaSource.PHP_SDK,
            "rust-sdk": RapidaSource.RUST_SDK,
            "twilio-call": RapidaSource.TWILIO_CALL,
        }

        result = source_map.get(label.lower(), RapidaSource.WEB_PLUGIN)
        if result == RapidaSource.WEB_PLUGIN:
            logging.warning(
                f"{label} is not supported. Supported sources are: "
                "'web-plugin', 'rapida-app', 'debugger', 'python-sdk', 'node-sdk', "
                "'go-sdk', 'typescript-sdk', 'java-sdk', 'php-sdk', 'rust-sdk', 'twilio-call'."
            )
        return result

