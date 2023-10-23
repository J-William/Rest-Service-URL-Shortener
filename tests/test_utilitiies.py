from app.utilities import generate_shortcut


class TestUtilities:
    samples = None

    @classmethod
    def setup_class(cls):
        cls.samples = list()
    
    @classmethod
    def teardown_class(cls):
        del cls.samples

    def test_shortcut_generation(self):
        for i in range(100):
            TestUtilities.samples.append(generate_shortcut())

    def test_shortcut_invariants(self):
        for shortcut in TestUtilities.samples:
            assert type(shortcut) == type(str())
            assert 0 < len(shortcut.strip()) <= 8
                        
    def test_shortcut_collisions(self):
        assert len(set(TestUtilities.samples)) == len(TestUtilities.samples)

