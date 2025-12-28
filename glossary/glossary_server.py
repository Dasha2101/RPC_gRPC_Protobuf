import grpc
from concurrent import futures
import time

from . import glossary_pb2
from . import glossary_pb2_grpc


TERMS = {
    "grpc": {
        "definition": "A high-performance remote procedure call (RPC) framework developed by Google",
        "sources": ["https://grpc.io"],
    },
    "rpc": {
        "definition": "A protocol that allows a program to execute a procedure on a remote server as if it were local",
        "sources": ["https://en.wikipedia.org/wiki/Remote_procedure_call"],
    },
    "protobuf": {
        "definition": "A language-neutral, platform-neutral mechanism for serializing structured data",
        "sources": ["https://protobuf.dev"],
    },
    "api": {
        "definition": "An interface that allows different software applications to communicate with each other",
        "sources": ["https://en.wikipedia.org/wiki/API"],
    },
    "web_api": {
        "definition": "An API that is accessed over the web using HTTP or similar protocols",
        "sources": ["https://developer.mozilla.org/en-US/docs/Web/API"],
    },
    "python": {
        "definition": "A high-level programming language known for its readability and wide ecosystem",
        "sources": ["https://www.python.org"],
    },
    "docker": {
        "definition": "A platform for developing, shipping, and running applications in containers",
        "sources": ["https://www.docker.com"],
    },
    "container": {
        "definition": "A lightweight, standalone executable package that includes software and its dependencies",
        "sources": ["https://www.docker.com/resources/what-container"],
    },
    "microservice": {
        "definition": "An architectural style that structures an application as a collection of small independent services",
        "sources": ["https://microservices.io"],
    },
    "client_server_model": {
        "definition": "A distributed application structure that divides tasks between service providers and requesters",
        "sources": ["https://en.wikipedia.org/wiki/Client%E2%80%93server_model"],
    },
    "serialization": {
        "definition": "The process of converting data structures into a format suitable for storage or transmission",
        "sources": ["https://en.wikipedia.org/wiki/Serialization"],
    },
    "http": {
        "definition": "An application-layer protocol for transmitting hypermedia documents on the web",
        "sources": ["https://developer.mozilla.org/en-US/docs/Web/HTTP"],
    },
    "rest": {
        "definition": "An architectural style for designing networked applications based on stateless communication",
        "sources": ["https://restfulapi.net"],
    },
    "backend": {
        "definition": "The server-side part of an application responsible for business logic and data processing",
        "sources": ["https://en.wikipedia.org/wiki/Front_end_and_back_end"],
    },
    "frontend": {
        "definition": "The client-side part of an application responsible for user interaction and presentation",
        "sources": ["https://en.wikipedia.org/wiki/Front_end_and_back_end"],
    },
}

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetTerm(self, request, context):
        if request.term in TERMS:
            data = TERMS[request.term]
            return glossary_pb2.GetTermResponse(
                term=glossary_pb2.Term(
                    term=request.term,
                    definition=data["definition"],
                    sources=data["sources"],
                )
            )

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Term not found")
        return glossary_pb2.GetTermResponse()

    def ListTerms(self, request, context):
        return glossary_pb2.ListTermsResponse(
            terms=[
                glossary_pb2.Term(
                    term=k,
                    definition=v["definition"],
                    sources=v["sources"],
                )
                for k, v in TERMS.items()
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(
        GlossaryService(), server
    )
    server.add_insecure_port("[::]:50053")
    server.start()
    print("✅ gRPC server started on port 50053")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
