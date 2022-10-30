from app.utilities import generate_mapkey, base62encode


class TestUtilities:
    @classmethod
    def setup_class(cls):
        global samples
        samples = list()
    
    @classmethod
    def teardown_class(cls):
        global samples
        del samples

    def test_mapkey_generation(self):
        for i in range(100):
            samples.append(generate_mapkey())

    def test_mapkey_invariants(self):
        for mapkey in samples:
            assert type(mapkey) == type(str())
            assert 0 < len(mapkey.strip()) <= 8 
                        
    def test_mapkey_collisions(self):
        assert len(set(samples)) == len(samples)

