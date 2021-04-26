from scipy import sparse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_similarity_n_space(m1, m2, batch_size=100):

    '''
        function to calculate cosine similarity without memory outages
    '''
    assert m1.shape[1] == m2.shape[1] and isinstance(batch_size, int) == True

    ret = np.ndarray((m1.shape[0], m2.shape[0]))

    batches = m1.shape[0] // batch_size
    
    if m1.shape[0]%batch_size != 0:
        batches = batches + 1  

    for row_i in range(0, batches):
        start = row_i * batch_size
        end = min([(row_i + 1) * batch_size, m1.shape[0]])        
        rows = m1[start: end]
        sim = cosine_similarity(rows, m2)  
        ret[start: end] = sim
    
    return ret


A = np.array([[0, 1, 0, 0, 1], [0, 0, 1, 1, 1], [1, 1, 0, 1, 0]])
A_sparse = sparse.csr_matrix(A)

similarities = cosine_similarity(A_sparse)
chunk_wise_similarity = cosine_similarity_n_space(A_sparse, A_sparse)

comparison = similarities == chunk_wise_similarity
equal_arrays = comparison.all()

print(equal_arrays)
