WITH search_vector AS (
    SELECT VECTOR_EMBEDDING(
        ALL_MINILM_L12_V2 USING 'Given the symptoms of sudden weakness in the left arm and leg, recent long-distance travel, and the presence of swollen and tender right lower leg, what specific cardiac abnormality is most likely to be found upon further evaluation that could explain these findings?g' AS data
    ) AS vec FROM DUAL
)
SELECT
    -- This line is updated to retrieve only the 'Response' field.
    JSON_VALUE(m.doc_json, '$.Response') AS response_text,
    L2_DISTANCE(
        m.doc_vector,
        v.vec
    ) AS distance
FROM
    medical_qa_data m,
    search_vector v
ORDER BY
    distance
FETCH FIRST 10 ROWS ONLY;
