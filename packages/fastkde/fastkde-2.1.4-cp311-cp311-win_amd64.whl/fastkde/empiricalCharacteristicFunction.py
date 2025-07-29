#!/usr/bin/env python
import numpy as npy
import fastkde.nufft as nufft


class ECF:
    def __init__(
        self,
        input_data,
        tgrids,
        precision=2,
        use_fft_approximation=True,
        be_verbose=False,
    ):
        """
        Calculates the empirical characteristic function of arbitrary sets of
        variables.

        Uses either the direct Fourier transform or nuFFT method (described by
        O'Brien et al. (2014, J. Roy. Stat. Soc. C) to calculate the Fourier transform
        of the data to yield the ECF.


            input:
            ------

                input_data   : The input data.
                              Array like with shape = (nvariables,npoints).

                tgrids      : The frequency-space grids to which to transform the
                              data

                              A list of frequency arrays for each variable dimension.

                use_fft_approximation : Flag whether to use the nuFFT approximation
                                        to the DFT

                be_verbose : Flags whether to be verbose


            output:
            -------

                An ECF object.  The ECF itself is stored in self.ECF

        """

        # Set whether we use the nuFFT approximation
        self.use_fft_approximation = use_fft_approximation

        # Get the data shape (nvariables,ndatapoints)
        dshape = npy.shape(input_data)
        rank = len(dshape)
        if rank != 2:
            raise ValueError(
                "input_data must be a rank-2 array of shape [nvariables,ndatapoints]; "
                "got rank = {}".format(rank)
            )
        # Extract the number of variables
        self.nvariables = dshape[0]
        # Extract the number of data points
        self.ndatapoints = dshape[1]

        # Set the frequency points
        self.tgrids = list(tgrids)

        try:
            gridRank = len(self.tgrids)
        except TypeError:
            raise ValueError("Could not determine the number of tgrids")

        if gridRank != self.nvariables:
            raise ValueError(
                "The rank of tgrids should be {}.  It is {}".format(
                    gridRank, self.nvariables
                )
            )

        # Check for regularity if we are doing nuFFT
        if self.use_fft_approximation:
            for n in range(self.nvariables):
                tpoints = tgrids[n]

                # Get the spacing of the first two points
                dt = tpoints[1] - tpoints[0]
                # Get the spacing of all points
                deltaT = tpoints[1:] - tpoints[:-1]
                # Get the difference between these spacings
                deltaT_diff = deltaT - dt
                tolerance = dt / 1e6
                # Check that all these differences are less than 1/1e6
                if not all(abs(deltaT_diff < tolerance)):
                    raise ValueError(
                        "All grids in tgrids must be regularly spaced if "
                        "use_fft_approximation is True"
                    )

        # Set verbosity
        self.be_verbose = be_verbose

        # Set the precision
        self.precision = precision

        # Set the fill value for the frequency grids
        fill_value = -1e20

        # Get the maximum frequency grid length
        ntmax = npy.amax([len(tgrid) for tgrid in tgrids])
        # Create the frequency grids array
        frequency_grids = fill_value * npy.ones([self.nvariables, ntmax])
        # Fill the frequency grids array
        for v in range(self.nvariables):
            frequency_grids[v, : len(tgrids[v])] = tgrids[v]

        # Simply pass in the input data as provided

        # Calculate the ECF
        if self.use_fft_approximation:
            # Calculate the ECF using the fast method
            myECF = nufft.nuifft(
                abscissas=input_data,
                ordinates=npy.ones([input_data.shape[1]], dtype=npy.complex128),
                frequency_grids=frequency_grids,
                missing_freq_val=fill_value,
                precision=precision,
                be_verbose=int(be_verbose),
            )
        else:
            # Calculate the ECF using the slow (direct, but exact) method
            myECF = nufft.idft(
                abscissas=input_data,
                ordinates=npy.ones([input_data.shape[1]], dtype=npy.complex128),
                frequency_grids=frequency_grids,
                missing_freq_val=fill_value,
            )

        # Ensure that the ECF is normalized
        mid_point_accessor = tuple([int((len(tgrid) - 1) / 2) for tgrid in tgrids])
        if myECF[mid_point_accessor] > 0.0:
            # Save the ECF in the object
            self.ECF = myECF / myECF[mid_point_accessor]
        else:
            raise RuntimeError(
                "Midpoint of ECF is 0.0.  min(ECF) = {}, max(ECF) = {}".format(
                    npy.amin(myECF), npy.amax(myECF)
                )
            )

        return


# *******************************************************************************
# *******************************************************************************
# ******************** Unit testing code ****************************************
# *******************************************************************************
# *******************************************************************************
if __name__ == "__main__":
    # Set the random seed to 0 so the results are repetable
    npy.random.seed(0)

    # Flag whether to do the 1-D test
    doOneDimensionalTest = False
    if doOneDimensionalTest:
        import matplotlib.pyplot as plt

        def mySTDGaus1D(x):
            return 1.0 / npy.sqrt(2 * npy.pi) * npy.exp(-(x**2) / 2)

        # Set the real-space/frequency points (Hermitian FFT-friendly)
        numXPoints = 513
        xpoints = npy.linspace(-20, 20, numXPoints)
        tpoints = nufft.calcTfromX(xpoints)

        # Calculate the FFT of an actual gaussian; use
        # this as the empirical characteristic function standard
        mygaus1d = mySTDGaus1D(xpoints)
        mygauscf = npy.fft.fftshift(npy.fft.ifftn(npy.fft.ifftshift(mygaus1d)))
        nh = (len(tpoints) - 1) / 2
        mygauscf /= mygauscf[nh]

        # Set the number of data points
        ndatapoints = 2**10
        # Set the number of variables
        nvariables = 1
        # Randomly sample from a normal distribution
        xyrand = npy.random.normal(loc=0.0, scale=1.0, size=[nvariables, ndatapoints])

        # Calculat the ECF using the fast method
        ecfFFT = ECF(xyrand, tpoints[npy.newaxis, :], use_fft_approximation=True).ECF
        # Calculat the ECF using the slow method
        ecfDFT = ECF(xyrand, tpoints[npy.newaxis, :], use_fft_approximation=False).ECF

        # Print the 0-frequencies (should be 1 for all)
        print(ecfFFT[nh], ecfDFT[nh], mygauscf[nh])

        plt.subplot(121, xscale="log", yscale="log")
        # Plot the magnitude of the fast and slow ECFs
        # (these should overlap for all but the highest half of the frequencies)
        plt.plot(tpoints, abs(ecfFFT), "r-")
        plt.plot(tpoints, abs(ecfDFT), "b-")
        # Plot the gaussian characteristic function standard
        plt.plot(tpoints, abs(mygauscf), "k-")

        plt.subplot(122, xscale="log", yscale="log")

        ihalf = len(ecfDFT) / 2
        ithreequarters = ihalf + ihalf / 2
        sh = slice(ihalf, ithreequarters)
        plt.plot(tpoints[sh], abs(ecfDFT[sh] - ecfFFT[sh]), "k-")
        plt.show()

    doTwoDimensionalTest = True  # Flag whether to do 2D tests
    if doTwoDimensionalTest:
        import matplotlib.pyplot as plt

        def std_norm_2d(x, y):
            return 1.0 / (2 * npy.pi) * npy.exp(-(x**2 + y**2) / 2)

        # Set the frequency points (Hermitian FFT-friendly)
        numXPoints = 127
        xpoints = npy.linspace(-20, 20, numXPoints)
        tpoints = nufft.calcTfromX(xpoints)

        # Calculate points from a 2D gaussian, and take their 2D FFT
        # to estimate the characteristic function standard
        xp2d, yp2d = npy.meshgrid(xpoints, xpoints)
        mygaus2d = std_norm_2d(xp2d, yp2d)
        mygauscf = npy.fft.fftshift(npy.fft.ifftn(npy.fft.ifftshift(mygaus2d)))
        nh = (len(tpoints) - 1) / 2
        mid_point_accessor = tuple(2 * [nh])
        mygauscf /= mygauscf[mid_point_accessor]

        # Sample points from a gaussian distribution
        ndatapoints = 2**5
        nvariables = 2
        xyrand = npy.random.normal(loc=0.0, scale=1.0, size=[nvariables, ndatapoints])

        tpointgrids = npy.concatenate(2 * (tpoints[npy.newaxis, :],), axis=0)
        # Calculate the ECF using the fast method
        CecfFFT = ECF(xyrand, tpointgrids, use_fft_approximation=True, be_verbose=True)
        ecfFFT = CecfFFT.ECF
        # Calculate the ECF using the slow method
        CecfDFT = ECF(xyrand, tpointgrids, use_fft_approximation=False, be_verbose=True)
        ecfDFT = CecfDFT.ECF

        # Use meshgrid to generate 2D arrays of the frequency points
        tp2d, wp2d = npy.meshgrid(tpoints, tpoints)

        # Create a figure
        fig = plt.figure()

        # Create a 3D set of axes
        ax = fig.add_subplot(221, projection="3d")

        # ax.plot_wireframe(tp2d[::4,::4],wp2d[::4,::4],(abs(mygauscf)**2)[::4,::4],color='k')
        # plot the fast and slow ECFs using a wireframe (they should overlap to the eye)
        ax.plot_wireframe(
            tp2d[::4, ::4], wp2d[::4, ::4], (abs(ecfFFT) ** 2)[::4, ::4], color="r"
        )
        ax.plot_wireframe(
            tp2d[::4, ::4], wp2d[::4, ::4], (abs(ecfDFT) ** 2)[::4, ::4], color="b"
        )

        # Create a 2D set of axes
        ax2 = fig.add_subplot(222, xscale="log", yscale="log")

        # Print the normalization constants (should be 1)
        print(
            ecfFFT[mid_point_accessor],
            ecfDFT[mid_point_accessor],
            mygauscf[mid_point_accessor],
        )

        # plot the magnitudes of the fast and slow ECFs along
        # an aribtrary slice (they should overlap except in the high frequency range)
        ax2.plot(tpoints, abs(ecfFFT[nh + 5, :]), "r-")
        ax2.plot(tpoints, abs(ecfDFT[nh + 5, :]), "b-")
        # Plot the magnitude of the gaussian characteristic function
        ax2.plot(tpoints, abs(mygauscf[nh + 5, :]), "k-")

        # Plot the average difference between the slow and fast ECFs
        # (will be relatively high because I use a coarse X grid, so that
        # the slow calculation will finish in my lifetime)
        errorK = npy.average(abs(ecfFFT - ecfDFT), 0)
        ax3 = fig.add_subplot(223, xscale="log", yscale="log")
        ax3.plot(
            tpoints[len(tpoints) / 2 : 3 * len(tpoints) / 4],
            errorK[len(tpoints) / 2 : 3 * len(tpoints) / 4],
            "k-",
        )

        plt.show()
