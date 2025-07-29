import patronus


patronus.init(
    # otel_endpoint="https://otel.patronus.ai:4318",
    otel_endpoint="http://0.0.0.0:4318",
    otel_exporter_otlp_protocol="http/protobuf",
)


@patronus.traced()
def main(a):
    return f"{a} world"


main("hello")
