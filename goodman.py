"""modified Goodman's Plot"""
"""import pylab for plotting"""
from pylab import*


"""Sut-ultimate tensile strength, Se-endurance strength,
Syt-tensile yield strength"""
def goodman(Sut, Se, Syt):
    figure()
    l1 = [Syt, 0]
    l2 = [0, Syt]
    l3 = [Sut, 0]
    l4 = [0, Se]
    """plot line to define failure by yielding"""
    plot(l1, l2)
    """plot line to define fatigue failure"""
    plot(l3, l4)
    """plot line at theta"""
    #plot((0, 774.97),(0, 198.28) , '--')
    plot((Se,Se), (Syt, Syt), '--')
    title("Modified Goodman Diagram\n(region shaded in yellow is safe)")
    legend(["yield line", "goodman line", "line at theta"], loc = "best")
    xlabel("Sm")
    ylabel("Sa")
    """find intersection points of yield and goodman line"""
    x = (Se - Syt) * Sut / (Se - Sut)
    y = (Syt - Sut) * Se/(Se - Sut)
    fill([0, Syt, x, 0], [0, 0, y, Se], facecolor = 'yellow', alpha = 0.3)
    show()

"""add Sut, Se and Syt in the given order and run the program"""
goodman(400, 154.66, 250)
    
    
