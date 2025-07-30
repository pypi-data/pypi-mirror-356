import numpy as np
from .config import BSE_ONE, BSE_TWO, CELL_ONE, CELL_TWO, DENDRITES_ONE, NUCLEATION_ONE

class Microscope:
    SUPPORTED_GROUND_TRUTHS = {
        "bse_one": BSE_ONE,
        "bse_two": BSE_TWO,
        "cell_one": CELL_ONE,
        "cell_two": CELL_TWO,
        "dendrites_one": DENDRITES_ONE,
        "nucleation_one": NUCLEATION_ONE,
    }

    def __init__(self, groundTruthName):
        if groundTruthName not in self.SUPPORTED_GROUND_TRUTHS:
            raise ValueError(
                f"Unsupported groundTruthName: {groundTruthName}. "
                f"Supported: {list(self.SUPPORTED_GROUND_TRUTHS.keys())}"
            )
        self.groundTruthVideo = self.SUPPORTED_GROUND_TRUTHS[groundTruthName]

        if self.groundTruthVideo is None or len(self.groundTruthVideo) == 0:
            raise ValueError(f"Ground truth video for '{groundTruthName}' is not loaded or empty.")

        # Automatically determine image shape from the first frame
        self.imageShape = self.groundTruthVideo[0].shape  # (height, width)

    def sample_image(self, yCoords, xCoords, imageShape, frameNumber):
        frame = self.groundTruthVideo[frameNumber]

        if imageShape[0] > frame.shape[0] or imageShape[1] > frame.shape[1]:
            raise ValueError(
                f"imageShape {imageShape} exceeds frame dimensions {frame.shape}"
            )

        frameCropped = frame[:imageShape[0], :imageShape[1]]
        sampledImage = np.zeros(imageShape, dtype=frame.dtype)

        if np.any(yCoords >= imageShape[0]) or np.any(xCoords >= imageShape[1]):
            raise IndexError("Provided coordinates exceed imageShape bounds.")

        sampledImage[yCoords, xCoords] = frameCropped[yCoords, xCoords]
        return sampledImage
