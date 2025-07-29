import numpy as np
from scipy import linalg


def list_to_upper_right_triangular_matrix(u):
    """
    Convert a list into an upper-right triangular matrix with inverted descending columns.
    Supports both scalar values and vector-valued inputs.

    Args:
    - u (list): A list of scalars or vectors (e.g., tuples, lists, or numpy arrays)

    Returns:
    - np.ndarray: Upper-right triangular matrix with proper shape and filled zeros
    """
    n = len(u)
    is_vector = isinstance(u[0], (list, tuple, np.ndarray))

    if is_vector:
        # Convert everything to np.array column vectors for consistency
        u = [np.array(vec).reshape(-1, 1) for vec in u]
        vec_dim = u[0].shape[0]
        zero_vec = np.zeros((vec_dim, 1))
        matrix = np.empty((n, n), dtype=object)

        # Initialize entire matrix with zero vectors
        for i in range(n):
            for j in range(n):
                matrix[i, j] = zero_vec.copy()
    else:
        matrix = np.zeros((n, n), dtype=float)

    for j in range(n):
        index = j
        for i in range(j + 1):
            matrix[i, j] = u[index]

            index -= 1

    return matrix

# A flattening function to turn a matrix of vectors into a matrix of scalars

def triangular_object_matrix_to_block(matrix):
    n = matrix.shape[0]
    vec_dim = matrix[0, 0].shape[0]  # should be 2
    block = np.zeros((n * vec_dim, n))  # (2n, n)

    for i in range(n):
        for j in range(n):
            block[i*vec_dim:(i+1)*vec_dim, j] = matrix[i, j].flatten()
    
    return block
def multivector_to_upper_right_triangular_matrix(U):
    
    """
    Create an upper-right block matrix from multiple input vectors.
    
    Args:
    - U (np.ndarray): 2D array of shape (T, m) where T = time steps, m = number of inputs.
    
    Returns:
    - H (np.ndarray): Block Hankel-like matrix of shape (m*T, T)
    """
    
    T, m = U.shape
    H = np.zeros((m * T, T))

    for j in range(T):  # Columns
        for i in range(j + 1):  # Rows to fill
            block = U[j - i]  # The input vector at time j-i (reverse)
            H[i * m:(i + 1) * m, j] = block

    return H



def create_hankel_matrix(data, row_block_size, col_hankel_blocks):
    """
    Creates a block Hankel matrix using time-series input/output data.
    Parameters:
        data : 2D array of shape (n_features, total_time_steps)
        row_block_size : number of block rows (how many stacked time steps)
        col_hankel_blocks : number of columns (how many time shifts to include)
    Returns:
        H : numpy.ndarray of shape (n_features * row_block_size, col_hankel_blocks)
    """
    
    n_features, _ = data.shape
    H = np.zeros((n_features * row_block_size, col_hankel_blocks))

    for i in range(row_block_size):
        H[i * n_features:(i + 1) * n_features, :] = data[:, i:i + col_hankel_blocks]

    return H



def era_method2(markov_parameters, row_block_size, col_hankel_blocks, num_inputs, num_outputs, rank):
    
    # Step 1 Create the two hankel matrices
    # nx is determined by when the output starts approaching a steady state
    #print("Length of input data:", len(inputs))
    #print("Length of output data:", len(outputs))
        
    H0 = create_hankel_matrix(markov_parameters[:, :-1], row_block_size=row_block_size, col_hankel_blocks=col_hankel_blocks)
    
    # 2nd hankel matrix of 1 step in the future compared to the first
    H1 = create_hankel_matrix(markov_parameters[:, 1:], row_block_size=row_block_size, col_hankel_blocks=col_hankel_blocks)
    
    
    #Step 2: Perform SVD
    # Perform Singular Value Decomposition
    
    U, S, Vt = linalg.svd(H0, full_matrices=False)
    
    U_r = U[:, :rank]
    S_r = S[:rank]
    Vt_r = Vt[:rank, :]
    
    Sigma_sqrt = np.diag(S_r**0.5)
    
    A = np.linalg.pinv(Sigma_sqrt) @ U_r.T @ H1 @ Vt_r.T @ np.linalg.pinv(Sigma_sqrt)
    
    
        
    
    num_columns = U_r.shape[0]
    
    I_C = np.zeros((num_outputs, num_columns))

    I_C[:, :num_outputs] = np.eye(num_outputs)  # Set the first num_outputs x num_outputs as identity

    
    C = I_C @ U_r @ np.diag(S_r**0.5)

    num_rows = Vt_r.shape[1]
    
    
    I_B = np.zeros((num_rows, num_inputs))
    I_B[:num_inputs, :] = np.eye(num_inputs)
    
    B = np.diag(S_r**0.5) @ Vt_r @ I_B
    D = markov_parameters[:, [1]].T
    

    return H0, A, B, C, D

def find_truncation_index(S, threshold):
    cumulative_energy = np.cumsum(S**2) / np.sum(S**2)
    return np.argmax(cumulative_energy >= threshold) + 1



def era_method2_truncation(markov_parameters, row_block_size, col_hankel_blocks, num_inputs, num_outputs, rank):
    # Performs ERA method with truncation
    
    # Step 1 Create the two hankel matrices
    
    
    markov_parameters = np.atleast_2d(markov_parameters)
    H0 = create_hankel_matrix(markov_parameters[:, :-1], row_block_size=row_block_size, col_hankel_blocks=col_hankel_blocks)
        
    # 2nd hankel matrix of 1 step in the future compared to the first
    H1 = create_hankel_matrix(markov_parameters[:, 1:], row_block_size=row_block_size, col_hankel_blocks=col_hankel_blocks)
    
    
    
    #Step 2: Perform SVD
    # Perform Singular Value Decomposition
    
    U, S, Vt = linalg.svd(H0, full_matrices=False)
    
    if rank is not None:
        U_r = U[:, :rank]
        S_r = S[:rank]
        Vt_r = Vt[:rank, :]
    else:
        U_r = U
        S_r = S
        Vt_r = Vt   
    
    Sigma_sqrt = np.diag(S_r**0.5)
    
    A = np.linalg.pinv(Sigma_sqrt) @ U_r.T @ H1 @ Vt_r.T @ np.linalg.pinv(Sigma_sqrt)
    
    
        
    
    num_columns = U_r.shape[0]
    
    I_C = np.zeros((num_outputs, num_columns))

    I_C[:, :num_outputs] = np.eye(num_outputs)  # Set the first num_outputs x num_outputs as identity

    
    C = I_C @ U_r @ np.diag(S_r**0.5)

    num_rows = Vt_r.shape[1]
    
    
    I_B = np.zeros((num_rows, num_inputs))
    I_B[:num_inputs, :] = np.eye(num_inputs)
    
    
    B = np.diag(S_r**0.5) @ Vt_r @ I_B
        
    D = markov_parameters[:, [0]]


    return H0, A, B, C, D

# Check if our system matrices are correct by constructing markov parameters and comparing 
# With the markov parameters computed from least squares

def construct_markov_parameters_from_system_matrices(A, B, C, D, num_params):
    
    D = D.item()
    markov_params = [D]  # Initialize our first parameter M0 = D
    CA_power = C  
    
    for i in range(1, num_params):
        markov_params.append((CA_power @ B).item())  # Mi = C*A^(i-1)*B
        CA_power = CA_power @ A  # Update to C*A^i for next iteration
    
    return markov_params

__all__ = ['era_method2', 'create_hankel_matrix', 'construct_markov_parameters_from_system_matrices', 'find_truncation_index', 'era_method2_truncation']
