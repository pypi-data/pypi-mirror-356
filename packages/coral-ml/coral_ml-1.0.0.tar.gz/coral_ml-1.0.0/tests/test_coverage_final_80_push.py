"""Final push to 80% - targeting specific uncovered lines."""

import argparse
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

# Target the less covered modules
from coral.cli.main import CoralCLI
from coral.core.weight_tensor import WeightMetadata, WeightTensor
from coral.integrations.pytorch import PyTorchIntegration
from coral.storage.hdf5_store import HDF5Store
from coral.version_control.commit import Commit, CommitMetadata
from coral.version_control.repository import Repository
from coral.version_control.version import Version


class TestFinalPush80Coverage:
    """Final targeted tests to reach 80%."""

    def test_cli_all_command_parsers(self):
        """Test all CLI command parsers are properly set up."""
        cli = CoralCLI()

        # Test that all expected commands can be parsed
        commands = [
            ["init"],
            ["add", "file.pth"],
            ["commit", "-m", "message"],
            ["status"],
            ["log"],
            ["checkout", "branch"],
            ["branch"],
            ["merge", "feature"],
            ["diff"],
            ["tag", "v1.0"],
            ["show", "weight"],
            ["gc"],
        ]

        for cmd in commands:
            args = cli.parser.parse_args(cmd)
            assert args.command == cmd[0]

    def test_hdf5_store_compression_levels(self):
        """Test HDF5Store with different compression levels."""
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
            store_path = tmp.name

        try:
            # Test with compression level
            store = HDF5Store(store_path, compression="gzip", compression_opts=9)

            # Store data
            weight = WeightTensor(
                data=np.random.randn(100, 100).astype(np.float32),
                metadata=WeightMetadata(
                    name="large", shape=(100, 100), dtype=np.float32
                ),
            )

            hash_key = weight.compute_hash()
            store.store(hash_key, weight)

            # Verify storage info
            info = store.get_storage_info()
            assert info["compression"] == "gzip"

            store.close()

        finally:
            Path(store_path).unlink(missing_ok=True)

    def test_repository_merge_scenarios(self):
        """Test Repository merge scenarios."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir, init=True)

            # Create initial commit
            weight1 = WeightTensor(
                data=np.array([1, 2, 3], dtype=np.float32),
                metadata=WeightMetadata(name="w1", shape=(3,), dtype=np.float32),
            )
            repo.stage_weights({"w1": weight1})
            repo.commit("Initial")

            # Create feature branch
            repo.create_branch("feature")
            repo.checkout("feature")

            # Add weight on feature branch
            weight2 = WeightTensor(
                data=np.array([4, 5, 6], dtype=np.float32),
                metadata=WeightMetadata(name="w2", shape=(3,), dtype=np.float32),
            )
            repo.stage_weights({"w2": weight2})
            repo.commit("Feature commit")

            # Back to main
            repo.checkout("main")

            # Test merge
            merge_commit = repo.merge("feature")
            assert merge_commit is not None

    def test_commit_to_from_json(self):
        """Test Commit JSON serialization."""
        metadata = CommitMetadata(
            message="Test commit",
            author="Test Author",
            email="test@example.com",
            tags=["v1", "release"],
        )

        commit = Commit(
            commit_hash="abc123",
            parent_hashes=["parent1"],
            weight_hashes={"w1": "h1", "w2": "h2"},
            metadata=metadata,
        )

        # To JSON
        json_str = commit.to_json()
        assert isinstance(json_str, str)

        # From JSON
        commit2 = Commit.from_json(json_str)
        assert commit2.commit_hash == commit.commit_hash
        assert commit2.metadata.message == commit.metadata.message

    def test_version_timestamp_handling(self):
        """Test Version with timestamp."""
        import datetime

        # Without timestamp
        v1 = Version("v1.0", "id1", "hash1", "Test")
        assert v1.timestamp is not None

        # With timestamp
        ts = datetime.datetime.now()
        v2 = Version("v2.0", "id2", "hash2", "Test", timestamp=ts)
        assert v2.timestamp == ts

    def test_pytorch_integration_weights_to_model(self):
        """Test PyTorchIntegration weights_to_model."""
        with patch("coral.integrations.pytorch.torch") as mock_torch:
            with patch("coral.integrations.pytorch.TORCH_AVAILABLE", True):
                integration = PyTorchIntegration()

                # Mock model
                mock_model = Mock()
                mock_state_dict = {}
                mock_model.state_dict.return_value = mock_state_dict

                # Create weights
                weights = {
                    "layer1.weight": WeightTensor(
                        data=np.ones((10, 5), dtype=np.float32),
                        metadata=WeightMetadata(
                            name="layer1.weight", shape=(10, 5), dtype=np.float32
                        ),
                    )
                }

                # Mock tensor creation
                mock_tensor = Mock()
                mock_torch.from_numpy.return_value = mock_tensor

                # Load weights
                integration.weights_to_model(mock_model, weights)

                # Verify
                mock_model.load_state_dict.assert_called_once()

    def test_repository_status_detailed(self):
        """Test Repository status with various states."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir, init=True)

            # Initial status
            status = repo.status()
            assert status["branch"] == "main"
            assert len(status["staged"]) == 0

            # Stage a weight
            weight = WeightTensor(
                data=np.array([1, 2, 3], dtype=np.float32),
                metadata=WeightMetadata(name="w1", shape=(3,), dtype=np.float32),
            )
            repo.stage_weights({"w1": weight})

            # Status with staged
            status = repo.status()
            assert len(status["staged"]) == 1
            assert "w1" in status["staged"]

    def test_hdf5_store_batch_operations(self):
        """Test HDF5Store batch operations."""
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
            store_path = tmp.name

        try:
            store = HDF5Store(store_path)

            # Create multiple weights
            weights = {}
            for i in range(5):
                data = np.random.randn(10, 10).astype(np.float32)
                weight = WeightTensor(
                    data=data,
                    metadata=WeightMetadata(
                        name=f"w{i}", shape=data.shape, dtype=data.dtype
                    ),
                )
                weights[weight.compute_hash()] = weight

            # Batch store
            store.store_batch(weights)

            # Batch load
            loaded = store.load_batch(list(weights.keys()))
            assert len(loaded) == 5

            # Verify each weight
            for hash_key, weight in weights.items():
                assert hash_key in loaded
                np.testing.assert_array_equal(loaded[hash_key].data, weight.data)

            store.close()

        finally:
            Path(store_path).unlink(missing_ok=True)

    def test_cli_branch_delete(self):
        """Test CLI branch delete command."""
        cli = CoralCLI()

        with patch("coral.cli.main.Repository") as mock_repo_class:
            mock_repo = Mock()
            mock_repo_class.return_value = mock_repo

            with patch("sys.exit") as mock_exit:
                args = argparse.Namespace(
                    command="branch", name=None, delete="old-feature", list=False
                )

                # Import argparse for Namespace

                cli._run_branch(args)

                mock_repo.delete_branch.assert_called_once_with("old-feature")
                mock_exit.assert_called_once_with(0)
