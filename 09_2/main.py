import numpy as np
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology
from skimage.segmentation import flood_fill
import matplotlib.pyplot as plt

def detect_local_minima(arr):
    # https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
    """
    Takes an array and detects the troughs using the local maximum filter.
    Returns a boolean mask of the troughs (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    # define an connected neighborhood
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#generate_binary_structure
    neighborhood = morphology.generate_binary_structure(len(arr.shape),2)
    # apply the local minimum filter; all locations of minimum value 
    # in their neighborhood are set to 1
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.filters.html#minimum_filter
    local_min = (filters.minimum_filter(arr, footprint=neighborhood)==arr)
    # local_min is a mask that contains the peaks we are 
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.
    # 
    # we create the mask of the background
    background = (arr==0)
    # 
    # a little technicality: we must erode the background in order to 
    # successfully subtract it from local_min, otherwise a line will 
    # appear along the background border (artifact of the local minimum filter)
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#binary_erosion
    eroded_background = morphology.binary_erosion(
        background, structure=neighborhood, border_value=1)
    # 
    # we obtain the final mask, containing only peaks, 
    # by removing the background from the local_min mask
    detected_minima = local_min ^ eroded_background
    return np.where(detected_minima)

def solve(test_input):
    space = np.array([list(map(int, line)) for line in test_input])

    minima = detect_local_minima(space)

    space[space != 9] = 0
    space[space == 9] = 255

    plt.imshow(space, cmap=plt.cm.gray)
    plt.show()

    areas = []

    for i in range(len(minima[0])):
        p = (minima[0][i], minima[1][i])
        sp = space.copy()
        filled = flood_fill(sp, p, 5, tolerance=1, connectivity=1)
        areas.append(np.sum(filled == 5))

    return np.product(sorted(areas, reverse=True)[:3])

example_input = """
2199943210
3987894921
9856789892
8767896789
9899965678
""".strip().split("\n")

def main():
    with open("09_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()