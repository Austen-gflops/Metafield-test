import streamlit as st
import pinecone

st.title('Pinecone Metadata Query App')

# User inputs for Pinecone API key and Index name
api_key = st.text_input("Enter your Pinecone API key:", type="password")
index_name = st.text_input("Enter your Pinecone Index name:")

# Initialize Pinecone
def init_pinecone(api_key, index_name):
    try:
        pinecone.init(api_key=api_key, environment='asia-northeast1-gcp')
        index = pinecone.Index(index_name)
        st.success("Connected to Pinecone successfully.")
        return index
    except Exception as e:
        st.error(f"Failed to connect to Pinecone: {e}")
        return None

# Function to query vectors based on metadata
def query_vectors(index, filter_criteria):
    query_response = index.query(
        vector=[0.1]*1536,  # Placeholder vector with length 1536
        filter=filter_criteria,
        top_k=10,  # Adjust top_k based on your needs
        include_metadata=True
    )
    return query_response

# Streamlit UI components for metadata-based vector querying
st.header("Query Vectors Based on Metadata")

# User inputs for filters
metafield1_key = st.text_input("Enter key for Metafield 1:")
metafield1_value = st.text_input("Enter value for Metafield 1:")
metafield2_key = st.text_input("Enter key for Metafield 2:")
metafield2_value = st.text_input("Enter value for Metafield 2:")
metafield3_key = st.text_input("Enter key for Metafield 3:")
metafield3_value = st.text_input("Enter value for Metafield 3:")

if st.button('Query Vectors'):
    if api_key and index_name:
        index = init_pinecone(api_key, index_name)
        if index:
            filter_criteria = []
            if metafield1_key and metafield1_value:
                filter_criteria.append({metafield1_key: {"$eq": metafield1_value}})
            if metafield2_key and metafield2_value:
                filter_criteria.append({metafield2_key: {"$eq": metafield2_value}})
            if metafield3_key and metafield3_value:
                filter_criteria.append({metafield3_key: {"$eq": metafield3_value}})

            if filter_criteria:
                query_filter = {"$and": filter_criteria}
                response = query_vectors(index, query_filter)
                st.write(response)
            else:
                st.error('No filters provided for query.')
    else:
        st.error('Please provide both API Key and Index Name.')

