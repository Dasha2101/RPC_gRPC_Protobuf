# api-gateway/app.py
from flask import Flask, jsonify, request
import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "glossary"))

from glossary_pb2 import GetTermRequest, ListTermsRequest
from glossary_pb2_grpc import GlossaryServiceStub

app = Flask(__name__)

channel = grpc.insecure_channel("localhost:50053")
stub = GlossaryServiceStub(channel)

@app.route("/")
def index():
    return "<h1>Glossary API Gateway</h1><p>Use /term?name=grpc or /terms</p>"

@app.route("/term")
def get_term():
    term_name = request.args.get("name", "")
    if not term_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    try:
        response = stub.GetTerm(GetTermRequest(term=term_name))
        t = response.term
        return jsonify({
            "term": t.term,
            "definition": t.definition,
            "sources": list(t.sources)
        })
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), e.code().value[0]

@app.route("/terms")
def list_terms():
    response = stub.ListTerms(ListTermsRequest())
    terms = [
        {
            "term": t.term,
            "definition": t.definition,
            "sources": list(t.sources)
        }
        for t in response.terms
    ]
    return jsonify(terms)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
