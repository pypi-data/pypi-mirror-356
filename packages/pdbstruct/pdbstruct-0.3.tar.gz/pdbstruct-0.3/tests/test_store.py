import os
import sys
import unittest

# Add src directory to Python path
this_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(this_dir, '..', 'src'))

from pdbstruct.store import Store


class TestStore(unittest.TestCase):
    """Test cases for the Store class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.fields = [
            ("x", "float32"),  # x coordinate
            ("y", "float32"),  # y coordinate
            ("z", "float32"),  # z coordinate
            ("r", "uint8"),  # red value
            ("g", "uint8"),  # green value
            ("b", "uint8"),  # blue value
            ("a", "uint8"),  # alpha value
            ("id", "int32"),  # id value
        ]

    def test_initialization_with_size(self):
        """Test Store initialization with a specific size"""
        store = Store(self.fields, 10)

        self.assertEqual(store.capacity, 10)
        self.assertEqual(store.count, 0)
        self.assertEqual(len(store._fields), 8)

        # Check if fields are properly initialized
        self.assertTrue(hasattr(store, "x"))
        self.assertTrue(hasattr(store, "y"))
        self.assertTrue(hasattr(store, "z"))
        self.assertTrue(hasattr(store, "r"))
        self.assertTrue(hasattr(store, "g"))
        self.assertTrue(hasattr(store, "b"))
        self.assertTrue(hasattr(store, "a"))
        self.assertTrue(hasattr(store, "id"))

        # Check array sizes - each field has one value per entry
        self.assertEqual(len(store.x), 10)
        self.assertEqual(len(store.y), 10)
        self.assertEqual(len(store.z), 10)
        self.assertEqual(len(store.r), 10)
        self.assertEqual(len(store.g), 10)
        self.assertEqual(len(store.b), 10)
        self.assertEqual(len(store.a), 10)
        self.assertEqual(len(store.id), 10)

    def test_initialization_without_size(self):
        """Test Store initialization without size"""
        store = Store(self.fields)

        self.assertEqual(store.capacity, 0)
        self.assertEqual(store.count, 0)
        self.assertEqual(len(store.x), 0)
        self.assertEqual(len(store.r), 0)
        self.assertEqual(len(store.id), 0)

    def test_add_field(self):
        """Test adding a field to the store"""
        store = Store(self.fields, 5)
        initial_field_count = len(store._fields)

        store.add_field("velocity", "float32")

        self.assertEqual(len(store._fields), initial_field_count + 1)
        self.assertTrue(hasattr(store, "velocity"))
        self.assertEqual(len(store.velocity), 5)

    def test_resize_larger(self):
        """Test resizing store to a larger size"""
        store = Store(self.fields, 5)

        # Set some data
        store.x[0] = 1.0
        store.r[0] = 255
        store.id[0] = 42

        store.resize(10)

        self.assertEqual(store.capacity, 10)
        self.assertEqual(len(store.x), 10)
        self.assertEqual(len(store.r), 10)
        self.assertEqual(len(store.id), 10)

        # Check that data is preserved
        self.assertEqual(store.x[0], 1.0)
        self.assertEqual(store.r[0], 255)
        self.assertEqual(store.id[0], 42)

    def test_resize_smaller(self):
        """Test resizing store to a smaller size"""
        store = Store(self.fields, 10)
        store.count = 8

        # Set some data
        store.x[0] = 1.0
        store.r[0] = 255

        store.resize(5)

        self.assertEqual(store.capacity, 5)
        self.assertEqual(store.count, 5)  # Should be clamped to new length
        self.assertEqual(len(store.x), 5)

        # Check that data is preserved
        self.assertEqual(store.x[0], 1.0)
        self.assertEqual(store.r[0], 255)

    def test_grow_if_full(self):
        """Test automatic growth when store is full"""
        store = Store(self.fields, 2)
        store.count = 2  # Make it full

        store.grow_if_full()

        self.assertEqual(store.capacity, 256)  # 256 if size is too small

    def test_grow_if_full_empty_store(self):
        """Test growth of empty store"""
        store = Store(self.fields, 0)
        store.count = 0

        store.grow_if_full()

        self.assertEqual(store.capacity, 256)  # Should grow to minimum 256

    def test_increment(self):
        """Test increment method"""
        store = Store(self.fields, 2)

        store.increment()
        self.assertEqual(store.count, 1)
        self.assertEqual(store.capacity, 2)

        store.increment()
        self.assertEqual(store.count, 2)
        self.assertEqual(store.capacity, 256)

        # This should trigger growth
        store.increment()
        self.assertEqual(store.count, 3)
        self.assertEqual(store.capacity, 256)

    def test_copy_from(self):
        """Test copying data from another store"""
        store1 = Store(self.fields, 5)
        store2 = Store(self.fields, 5)

        # Set data in store1
        store1.x[0] = 1.0
        store1.y[0] = 2.0
        store1.z[0] = 3.0
        store1.r[0] = 255
        store1.g[0] = 128
        store1.b[0] = 64
        store1.a[0] = 32
        store1.id[0] = 42

        # Copy from store1 to store2
        store2.copy_from(store1, 0, 0, 1)

        # Check that data was copied
        self.assertEqual(store2.x[0], 1.0)
        self.assertEqual(store2.y[0], 2.0)
        self.assertEqual(store2.z[0], 3.0)
        self.assertEqual(store2.r[0], 255)
        self.assertEqual(store2.g[0], 128)
        self.assertEqual(store2.b[0], 64)
        self.assertEqual(store2.a[0], 32)
        self.assertEqual(store2.id[0], 42)

    def test_copy_within(self):
        """Test copying data within the same store"""
        store = Store(self.fields, 5)

        # Set data at index 0
        store.x[0] = 1.0
        store.y[0] = 2.0
        store.z[0] = 3.0
        store.r[0] = 255
        store.id[0] = 42

        # Copy from index 0 to index 1
        store.copy_within(1, 0, 1)

        # Check that data was copied to index 1
        self.assertEqual(store.x[1], 1.0)
        self.assertEqual(store.y[1], 2.0)
        self.assertEqual(store.z[1], 3.0)
        self.assertEqual(store.r[1], 255)
        self.assertEqual(store.id[1], 42)

    def test_sort(self):
        """Test sorting functionality"""
        store = Store([("value", "int32")], 5)
        store.count = 5

        # Set values: [5, 2, 8, 1, 9]
        store.value[0] = 5
        store.value[1] = 2
        store.value[2] = 8
        store.value[3] = 1
        store.value[4] = 9

        # Sort by value (ascending)
        def compare_func(i, j):
            return store.value[i] - store.value[j]

        store.sort(compare_func)

        # Check if sorted: [1, 2, 5, 8, 9]
        expected_values = [1, 2, 5, 8, 9]
        for i in range(5):
            self.assertEqual(store.value[i], expected_values[i])


if __name__ == "__main__":
    # Run tests instead of main when script is executed
    unittest.main()
