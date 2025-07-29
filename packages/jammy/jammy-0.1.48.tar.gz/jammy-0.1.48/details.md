# Setup

```shell
git clone https://gitlab.com/zqsh419/jam.git --recursive $HOME/jam
export PATH=$HOME/jam/bin:$PATH
```

## install uv

```shell
curl -sSL https://astral.sh/uv/install.sh | sh

# create a virtual environment
uv venv

# activate the virtual environment
source .venv/bin/activate

# Install the package with all optional dependencies
uv pip install -e ".[all]"
```

## Managing Dependencies

The project uses optional dependency groups to organize different types of dependencies. Here's how to work with them:

### Available Dependency Groups

- **torch**: PyTorch-related packages (torch, torchvision, lightning, pandas, etc.)
- **web**: Web-related packages (tornado, pyzmq)
- **storage**: Data storage packages (h5py, msgpack, pyarrow, lmdb, etc.)
- **pro**: Profiling and debugging tools
- **viz**: Visualization packages (plotly)
- **learn**: Machine learning packages (wandb)
- **all**: All optional dependencies combined
- **dev**: Development tools (pytest, black, pylint, etc.)

### Installing Specific Dependency Groups

```shell
# Install only torch-related dependencies
uv pip install -e ".[torch]"

# Install multiple groups
uv pip install -e ".[torch,viz]"

# Install all optional dependencies
uv pip install -e ".[all]"

# Install with development dependencies
uv pip install -e ".[all,dev]"
```

### Adding New Dependencies

1. **Edit pyproject.toml**: Add the dependency to the appropriate optional dependency group
2. **Update the "all" group**: If you add to any optional group, also add it to the "all" group
3. **Reinstall**: Run `uv pip install -e ".[all]"` to install the new dependency

Example of adding a new dependency:
```toml
# In pyproject.toml
torch = [
    "torch>=2.0.0",
    "pandas>=1.3.0",
    "your-new-package>=1.0.0",  # Add here
]

all = [
    "torch>=2.0.0",
    "pandas>=1.3.0",
    "your-new-package>=1.0.0",  # Also add here
    # ... other dependencies
]
```

## publish to pypi manually

```shell
uv build
uv publish --token $PYPI_TOKEN
```
