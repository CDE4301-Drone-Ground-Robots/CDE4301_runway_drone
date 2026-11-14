class ThermalDetector:

    def __init__(self):

        print(
            "Thermal detector initialized "
            "(TEMPORARY BYPASS)"
        )


    def check(self, key):

        """
        TEMPORARY THERMAL BYPASS

        Press '1' to simulate:

        Thermal → OBSTACLE
        """

        if key == ord("1"):

            return True


        return False