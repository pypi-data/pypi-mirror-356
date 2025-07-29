import patronus


patronus.init(
    api_key="sk-4YQh87LeQWJppqfyU1OZaIeNnZ9-Z-9xiXgJYZlDQRc",
    api_url="https://api.dev.patronus.ai",
    # otel_endpoint="http://0.0.0.0:4318",
    # otel_endpoint="https://otel-dev.internal.patronus.ai:4318",
    # otel_endpoint="https://otel-dev.internal.patronus.ai:443",
    otel_endpoint="https://otel-dev.internal.patronus.ai:4317",
    # otel_exporter_otlp_protocol="grpc",
    # otel_exporter_otlp_protocol="http/protobuf",
)


@patronus.traced()
def main(a):
    return f"{a} world"


main("hello")
