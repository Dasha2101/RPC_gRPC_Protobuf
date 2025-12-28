import grpc
from concurrent import futures
import time

from protobuf import glossary_pb2_grpc, glossary_pb2
from google.protobuf import empty_pb2

from terms import TERMS

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetAllTerms(self, request, context):
        return glossary_pb2.TermListResponse(terms=list(TERMS.values()))
    
    def GetTerm(self, request, context):
        term = TERMS.get(request.keyword)
        if term:
            return glossary_pb2.TermResponse(term=term)
        context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
    
    def AddTerm(self, request, context):
        TERMS[request.term.keyword] = request.term
        return glossary_pb2.TermResponse(term=request.term)
    
    def UpdateTerm(self, request, context):
        if request.term.keyword in TERMS:
            TERMS[request.term.keyword] = request.term
            return glossary_pb2.TermResponse(term=request.term)
        context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
    
    def DeleteTerm(self, request, context):
        if request.keyword in TERMS:
            del TERMS[request.keyword]
            return empty_pb2.Empty()
        context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()