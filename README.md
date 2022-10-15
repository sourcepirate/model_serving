## Model Serving

Simple flask API to serve sklearn model.

## Example Usage

```bash
export MODEL_PATH="iris.sav"
export COLUMNS="sepal.length,sepal.width,petal.length,petal.width"

python cli.py -m ${MODEL_PATH} -c ${COLUMNS}
```

## Building Docker Image

```
docker build -t model_serving:latest .
```