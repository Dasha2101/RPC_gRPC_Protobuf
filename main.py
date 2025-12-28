from fastapi import FastAPI, HTTPException
import grpc
from glossary.protobuf import glossary_pb2, glossary_pb2_grpc
from google.protobuf import empty_pb2

from pydantic import BaseModel

class TermModel(BaseModel):
    keyword: str
    description: str

class UpdateTermModel(BaseModel):
    description: str

app = FastAPI()


def get_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return glossary_pb2_grpc.GlossaryServiceStub(channel)

@app.get("/terms")
def get_all_terms():
    stub = get_stub()
    response = stub.GetAllTerms(empty_pb2.Empty())
    return [ {"keyword": t.keyword, "description": t.description} for t in response.terms]

@app.get("/terms/{keyword}")
def get_term(keyword: str):
    stub = get_stub()
    try:
        response = stub.GetTerm(glossary_pb2.TermRequest(keyword=keyword))
        return {"keyword": response.term.keyword, "description": response.term.description}
    except grpc.RpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

@app.post("/terms")
def add_term(term: TermModel):
    stub = get_stub()
    request = glossary_pb2.AddTermRequest(
        term=glossary_pb2.Term(keyword=term.keyword, description=term.description)
    )
    try:
        response = stub.AddTerm(request, timeout=5)
        return {"keyword": response.term.keyword, "description": response.term.description}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.put("/terms/{keyword}")
def update_term(keyword: str, term: UpdateTermModel):
    stub = get_stub()
    request = glossary_pb2.UpdateTermRequest(
        term=glossary_pb2.Term(keyword=keyword, description=term.description)
    )
    try:
        response = stub.UpdateTerm(request, timeout=5)
        return {"keyword": response.term.keyword, "description": response.term.description}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.delete("/terms/{keyword}")
def delete_term(keyword: str):
    stub = get_stub()
    try:
        stub.DeleteTerm(glossary_pb2.DeleteTermRequest(keyword=keyword))
        return {"status": "deleted"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=404, detail=e.details())