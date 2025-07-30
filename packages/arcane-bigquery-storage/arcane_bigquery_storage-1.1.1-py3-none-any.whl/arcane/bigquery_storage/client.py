import backoff
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types, writer
from google.protobuf import descriptor_pb2
from google.api_core.exceptions import (
    Unknown,
    InternalServerError,
    ServiceUnavailable,
    ServerError,
    GatewayTimeout,
)

from .proto import feed_boost_statistic_pb2
from .proto import feed_boost_result_pb2


class Client(bigquery_storage_v1.BigQueryWriteClient):
    def __init__(self, credentials=None):
        super().__init__(credentials=credentials)

    def create_application_stream(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        stream_type: types.WriteStream.Type = types.WriteStream.Type.COMMITTED,
    ) -> types.WriteStream:
        """Create an application stream for a table.
        By default, the stream type is COMMITTED, it will use exactly-once semantics.
        Warning : there is a limit of 10k created streams per hour per region per project.
        Check the doc for more info on the stream types: https://cloud.google.com/bigquery/docs/write-api#application-created_streams

        Args:
            project_id (str): the project id of the destination table
            dataset_id (str): the dataset id of the destination table
            table_id (str): the table id of the destination table
            stream_type (types.WriteStream.Type, optional): the type of stream to use. Defaults to types.WriteStream.Type.COMMITTED.

        Returns:
            types.WriteStream: the created write stream
        """
        parent = self.table_path(project_id, dataset_id, table_id)
        write_stream = types.WriteStream()
        write_stream.type_ = stream_type
        write_stream = self.create_write_stream(
            parent=parent, write_stream=write_stream
        )
        return write_stream

    def create_default_stream_name(self,
        project_id: str,
        dataset_id: str,
        table_id: str,
    ) -> str:
        """Create a default stream name for a table. Use at-least-once semantics. No limit on the number of streams.
        Check the doc for more info on the default stream: https://cloud.google.com/bigquery/docs/write-api#default_stream

        Args:
            project_id (str): the project id of the destination table
            dataset_id (str): the dataset id of the destination table
            table_id (str): the table id of the destination table

        Returns:
            str: the default stream name
        """
        parent = self.table_path(project_id, dataset_id, table_id)
        stream_name = f"{parent}/_default"
        return stream_name

    @backoff.on_exception(
        backoff.expo,
        (Unknown, InternalServerError, ServiceUnavailable, ServerError, GatewayTimeout),
        max_tries=5,
    )
    def write_rows(
        self,
        stream_name: str,
        proto_descriptor: descriptor_pb2.DescriptorProto,
        rows: list[bytes],
    ):
        """Write rows to a stream. This function assume you are only writing one time to the stream.
        If you want to write multiple requests to the stream, you should consider adding an offset parameter to the function.
        See for detailed implementation: https://github.com/googleapis/python-bigquery-storage/blob/main/samples/snippets/append_rows_pending.py

        Args:
            stream (types.WriteStream): the stream to write to
            rows (list): the rows to write
        """
        request_template = types.AppendRowsRequest()
        request_template.write_stream = stream_name

        proto_schema = types.ProtoSchema()

        proto_schema.proto_descriptor = proto_descriptor
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.writer_schema = proto_schema
        request_template.proto_rows = proto_data

        append_rows_stream = writer.AppendRowsStream(self, request_template)
        proto_rows = types.ProtoRows()
        for row in rows:
            proto_rows.serialized_rows.append(row)

        request = types.AppendRowsRequest()

        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        request.proto_rows = proto_data
        response_future_1 = append_rows_stream.send(request)
        response_future_1.result()
        append_rows_stream.close()

    def create_feed_boost_result_proto_descriptor(self) -> descriptor_pb2.DescriptorProto:
        proto_descriptor = descriptor_pb2.DescriptorProto()
        feed_boost_result_pb2.FeedBoostResult.DESCRIPTOR.CopyToProto(proto_descriptor)
        return proto_descriptor

    def create_feed_boost_statistic_proto_descriptor(
        self,
    ) -> descriptor_pb2.DescriptorProto:
        proto_descriptor = descriptor_pb2.DescriptorProto()
        feed_boost_statistic_pb2.FeedBoostStatistic.DESCRIPTOR.CopyToProto(
            proto_descriptor
        )
        return proto_descriptor

    def create_feed_boost_result_row(self, identifier_field: str, response: str) -> bytes:
        """Create a row for the feed boost result table. Result is serialized to bytes.

        Args:
            identifier_field (str): the identifier field
            response (str): the response as a JSON string

        Returns:
            bytes: the serialized row
        """
        feed_boost_result = feed_boost_result_pb2.FeedBoostResult(
            identifier_field=identifier_field, response=response
        )
        return feed_boost_result.SerializeToString()

    def create_feed_boost_statistic_row(
        self,
        task_id: str,
        timestamp: str,
        cached_tokens: int,
        prompt_tokens: int,
        completion_tokens: int,
        execution_time: float,
        optimized_products: int,
        total_input_products: int,
    ) -> bytes:
        """Create a row for the feed boost statistic table. Result is serialized to bytes.

        Args:
            task_id (str): the task id
            timestamp (str): the timestamp
            cached_tokens (int): the number of cached tokens
            prompt_tokens (int): the number of prompt tokens
            completion_tokens (int): the number of completion tokens
            execution_time (float): the execution time
            optimized_products (int): the number of optimized products
            total_input_products (int): the total number of input products

        Returns:
            bytes: the serialized row
        """
        feed_boost_statistic = feed_boost_statistic_pb2.FeedBoostStatistic(
            task_id=task_id,
            timestamp=timestamp,
            cached_tokens=cached_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            execution_time=execution_time,
            optimized_products=optimized_products,
            total_input_products=total_input_products,
        )
        return feed_boost_statistic.SerializeToString()
