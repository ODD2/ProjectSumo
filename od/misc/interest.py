class InterestConfig:
    def __init__(self, oma_only, rsu, appdata_poisson):
        self.oma_only = oma_only
        self.rsu = rsu
        self.appdata_poisson = appdata_poisson

    def __str__(self):
        return (
            "oma_only({}) rsu({}) appdata_poisson({})".format(
                self.oma_only,
                self.rsu,
                self.appdata_poisson
            )
        )
