from concurrent import futures
import grpc

import glossary_pb2
import glossary_pb2_grpc
from data import TERMS


class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):

    def GetTerm(self, request, context):
        key = request.term.lower()
        term = TERMS.get(key)

        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")

        return glossary_pb2.TermResponse(term=term)

    def ListTerms(self, request, context):
        return glossary_pb2.TermsResponse(terms=TERMS.values())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(
        GlossaryService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Glossary gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
