import numpy as np
import scipy.io.wavfile

def update_W(W, x, learning_rate):
    """
    Perform a gradient ascent update on W using data element x and the provided learning rate.

    This function should return the updated W.

    Use the laplace distribiution in this problem.

    Args:
        W: The W matrix for ICA
        x: A single data element
        learning_rate: The learning rate to use

    Returns:
        The updated W
    """
    
    # *** START CODE HERE ***
    wx = W.dot(x)
    pos = (wx > 0)
    neg = (wx <= 0)
    sig = np.zeros_like(wx, dtype=float)
    sig[pos] = 1 / (1 + np.exp(-wx[pos]))
    sig[neg] = np.exp(wx[neg]) / (1 + np.exp(wx[neg]))
    propogate = np.matrix(1 - 2 * sig).T * np.matrix(x)
    updated_W = np.array(W + learning_rate * (propogate + np.linalg.inv(W.T)))
    # *** END CODE HERE ***

    return updated_W


def unmix(X, W):
    """
    Unmix an X matrix according to W using ICA.

    Args:
        X: The data matrix
        W: The W for ICA

    Returns:
        A numpy array S containing the split data
    """

    S = np.zeros(X.shape)


    # *** START CODE HERE ***
    S = np.dot(X, W.T)
    # *** END CODE HERE ***

    return S


Fs = 11025

def normalize(dat):
    return 0.99 * dat / np.max(np.abs(dat))

def load_data():
    mix = np.loadtxt('../data/mix.dat')
    return mix

def save_sound(audio, name):
    scipy.io.wavfile.write('output/{}.wav'.format(name), Fs, audio)

def unmixer(X):
    M, N = X.shape
    W = np.eye(N)

    anneal = [0.1 , 0.1, 0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.01 , 0.01, 0.005, 0.005, 0.002, 0.002, 0.001, 0.001]
    print('Separating tracks ...')
    for lr in anneal:
        print(lr)
        rand = np.random.permutation(range(M))
        totalcost = 0.0
        for i in rand:
            x = X[i]
            W = update_W(W, x, lr)

    return W

def main():
    X = normalize(load_data())

    print(X.shape)

    for i in range(X.shape[1]):
        save_sound(X[:, i], 'mixed_{}'.format(i))

    W = unmixer(X)
    print(W)
    S = normalize(unmix(X, W))

    for i in range(S.shape[1]):
        save_sound(S[:, i], 'split_{}'.format(i))

if __name__ == '__main__':
    main()
