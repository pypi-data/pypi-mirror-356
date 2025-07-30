import mvupkg_rstanic
import matlab
import numpy as np
import time

class Mvu:
    # Statički članovi
    
    # Instanca preko koje pristupamo funkcijama implementiranima u MATLAB-u.
    _library_instance=None

    # Incijalizacija instance biblioteke.
    def initialize():
        if not Mvu._library_instance:
            print("Initializing Mvu library...")
            Mvu._library_instance=mvupkg_rstanic.initialize()
            print("Mvu library initialized.")

    # Uništavanje instance biblioteke. Ovu metodu pozivamo kad ne trebamo više
    # Mvu.
    def terminate():
        if Mvu._library_instance:
            print("Terminating library instance...")
            Mvu._library_instance.terminate()
            Mvu._library_instance=None
            print("Mvu library instance terminated.")

    # Članovi instanci
    def __init__(self, n_neighbors=5, n_components=2, maxiter=50, eps=1e-09, \
                 verbose=True):
        self.n_neighbors=n_neighbors
        self.n_components=n_components
        self.maxiter=maxiter
        self.eps=eps
        self.verbose=verbose

        self.n_samples=None
        self.n_features=None
        self.kernel=None
        self.eigenvalues=None
        self.embedding=None
        self.cost=None
        self.reconstruction_error=None
        self.reconstruction_error_rel=None

        self.iter=None
        self.feasratio=None
        self.pinf=None
        self.dinf=None
        self.numerr=None

    def fit_transform(self, X):
        print("============================== Mvu ==============================")
        start=time.time()

        # Ako je statička instanca biblioteke definirana koristimo nju, dok u
        # protivnom stvaramo instancu samo za potrebe ove metode.
        lib=None
        if Mvu._library_instance:
            lib=Mvu._library_instance
        else:
            print("Initializing Mvu library...")
            lib=mvupkg_rstanic.initialize()
            print("Mvu library initialized.")

        n, d=X.shape
        self.n_samples=n
        self.n_features=d

        if self.verbose:
            print("Prameters:")
            print(f"n_samples={n}", f"n_features={d}", sep="\n")

        # Definicija parametara koja prosljeđujemo MATLAB funkciji.
        XIn=matlab.double(X, size=(n,d))
        kIn=matlab.double([self.n_neighbors], size=(1,1))
        pIn=matlab.double([self.n_components], size=(1,1))
        maxIterStrIn="maxiter"
        maxIterIn=matlab.double([self.maxiter], size=(1,1))
        epsStrIn="eps"
        epsIn=matlab.double([self.eps], size=(1,1))

        if self.verbose:
            print("Calling Mvu library for solution to the problem...")

        YOut, infoOut=lib.mvu(XIn, kIn, pIn, maxIterStrIn, maxIterIn, epsStrIn, epsIn, nargout=2)

        if self.verbose:
            print("Problem solved!")
        
        self.kernel=np.array(infoOut["kernel"])
        self.eigenvalues=np.array(infoOut["eigvals"])
        self.embedding=np.array(YOut)
        self.cost=infoOut["cost"]
        self.reconstruction_error=infoOut["reconstruction_error"]
        self.reconstruction_error_rel=infoOut["reconstruction_error_rel"]
        self.iter=infoOut["iter"]
        self.feasratio=infoOut["feasratio"]
        self.pinf=infoOut["pinf"]
        self.dinf=infoOut["dinf"]
        self.numerr=infoOut["numerr"]

        if not Mvu._library_instance:
            print("Terminating library instance...")
            lib.terminate()
            print("Mvu library instance terminated.")

        finish=time.time()
        time_taken=round(finish-start, 2)

        if self.verbose:
            print(f"Mvu took total of {time_taken} seconds.")
            print("=================================================================")

        return self.embedding
