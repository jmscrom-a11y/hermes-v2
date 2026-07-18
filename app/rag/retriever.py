DEFAULT_TOP_K = 4


def create_retriever(vector_db, k=DEFAULT_TOP_K, search_type="similarity"):
    return vector_db.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k},
    )


def retrieve_documents(retriever, query):
    if hasattr(retriever, "invoke"):
        return retriever.invoke(query)
    return retriever.get_relevant_documents(query)
