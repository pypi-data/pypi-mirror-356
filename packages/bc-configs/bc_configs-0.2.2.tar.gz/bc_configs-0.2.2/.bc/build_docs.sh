SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/../
START_DIR=$PWD
source "$ROOT_DIR/.venv/bin/activate"
cd "$ROOT_DIR/docs" && make clean && make html
cd "$START_DIR"
