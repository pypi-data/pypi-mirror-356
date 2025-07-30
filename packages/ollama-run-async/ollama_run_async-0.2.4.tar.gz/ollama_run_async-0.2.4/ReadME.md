
The functions presented in this package make it simple for researchers in social sciences to run several Large Language Models loaded through Ollama over documents stored in a data frame asynchronously (at once). As such, all models used here have to be downloaded through the Ollama interface (https://ollama.com/). With them you are able to:

1. **Analyze** Text Stored in a Dataframe Column
2. **Extract** Missing Metadata Information from a Text Stored in a Dataframe Column
3. **Create** "Fake" LLM Survey Respondents with given characteristics and make them answer your survey questions 

The functions can do two main things:

1. **Split:** You run several models in parallel on many chunks of documents (the same model several times or different models per chunk). The text documents are stored as rows in a dataframe. This speeds up the computing time.
2. **Fanout:** You run several models in parallel on the same chunks of documents (again, the same model several times or different models per chunk). Again, the text documents are stored as rows in a dataframe. This likewise speeds up the computing time, but primarily allows for convenient comparison of different model outputs.

The three functions of the package that can either split and/or fan out over the dataframe, but do so in slightly different ways and for slightly different purposes:
1. **`run_analysis()`:** Allows you to write one prompt, which then either splits or fans out over the text in the dataframe. The common tasks would be text labeling or sentiment analysis. The answer to the prompt might be conveniently structured in a JSON object, with specifiable keys.
2. **`fill_missing_fields_from_csv()`**: Instead of writing a prompt, the second function is specifically designed for information extraction from the text (with the primary use case being metadata collection). It also allows for an output in a JSON format. Crucially, it also handles existing metadata information in the dataframe, so the model only extracts information that is not yet present. 
3. **`run_survey_responses()`**: The last function, instead of focusing on analysing existing text, creates fake survey responses based on a set of characteristics. The "fake" respondents are generated and stored in a data frame with the helper function `generate_fake_survey_df()`, which allows the creation of a representative (based on the target population) distribution of characteristics over these respondents. The use case is to have a potentially more accurate distribution of responses to survey questions prior to running the actual survey on real-life respondents. 


---

## Installation & model setup

```bash
# 1 · Install the Python package
pip install Ollama-run-async  

# 2 · Have Ollama running and pull the models you plan to use
ollama pull llama3.2            # repeat for other model tags if desired
ollama serve                    # keep this running

# 3 · Python deps
pip install pandas numpy tqdm ollama nest_asyncio
````

If your Ollama server is remote, set  
`export OLLAMA_HOST=http://<ip>:11434` (or `set` on Windows).

---

## Function overview

### 1 · `run_analysis()`

```python
run_analysis(
    df: pd.DataFrame,
    text_column: str = "text",
    workers: int = 3,
    max_concurrent_calls: int | None = None,
    *,                       # keyword-only extras
    chunk_size: int | None = None,
    batch_size: int = 4,
    model_names: str | list[str] = "llama3.2",
    prompt_template: str | None = None,
    json_keys: tuple[str, ...] | None = None,
    fanout: bool = False,
    temperature: float = 0.9,
    max_tokens: int = 128,
) -> pd.DataFrame
```

| Parameter           | Default      | Purpose                                                                                                                                                      |
| ------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `df`, `text_column` | —            | DataFrame and column to process.                                                                                                                             |
| `workers`           | 3            | Number of parallel **`AsyncClient`** workers (row-level sharding).                                                                                           |
| `model_names`       | `"llama3.2"` | Single model for all workers **or** list (one tag per worker).                                                                                               |
| `prompt_template`   | `None`       | Format string; `{text}` is replaced by the row text.                                                                                                         |
| `json_keys`         | `None`       | If set, the model must return **one JSON object** with these keys; a column is added per key (or per key + model when `fanout=True`).                        |
| `batch_size`        | 4            | **Prompts queued per worker before awaiting** the model response. Larger = fewer HTTP round-trips & better GPU utilisation, but more VRAM during generation. |
| `chunk_size`        | `None`       | Stream the DataFrame in outer chunks of this many rows (keeps RAM bounded). `None` → process the whole frame in one pass.                                    |
| `fanout`            | `False`      | `False` → models split the DataFrame. `True` → **every model analyses every row**; output columns are suffixed with `_<model>` (e.g. `label_llama3.2`).      |
| `temperature`       | 0.9          | Sampling temperature for the LLM (higher → more random).                                                                                                     |
| `max_tokens`        | 128          | Maximum number of tokens to generate per row/question.                                                                                                       |

---

### 2 · `fill_missing_fields_from_csv()`

```python
fill_missing_fields_from_csv(
    input_csv: str,
    output_csv: str = "out.csv",
    chunk_size: int = 20_000,
    workers: int = 3,
    batch_size: int = 4,
    title_col: str = "title_en",
    json_fields: tuple[str, ...] = ("Occasion","Institution","City"),
    col_map: dict[str, str] | None = None,
    model_names: str | list[str] = "llama3.2",
    fanout: bool = False,
    temperature: float = 0.9,
    max_tokens: int = 128,
) -> None
```

| Parameter     | Default      | Purpose                                                                                      |
| ------------- | ------------ | -------------------------------------------------------------------------------------------- |
| `chunk_size`  | 20 000       | Rows per streamed chunk.                                                                     |
| `workers`     | 3            | Async workers per chunk.                                                                     |
| `batch_size`  | 4            | Prompts queued *per* worker before awaiting.                                                 |
| `json_fields` | tuple        | Keys expected in JSON answer.                                                                |
| `col_map`     | auto         | Key → column map; omit for `computed_<key>`.                                                 |
| `model_names` | `"llama3.2"` | Tag for all workers **or** list (one per worker).                                            |
| `fanout`      | `False`      | If `True`, every model fills every row and computed columns become `computed_<key>_<model>`. |
| `temperature` | 0.9          | Sampling temperature for the LLM (higher → more random).                                     |
| `max_tokens`  | 128          | Maximum number of tokens to generate per row/record.                                         |

---

## Quick examples

```python
from async_run_ollama import run_analysis, fill_missing_fields_from_csv
import pandas as pd

# 1 · Fan-out sentiment scoring with three models, custom temperature + token limit
df = pd.read_csv("speeches.csv")
df = run_analysis(
    df,
    text_column="speech",
    workers=3,
    model_names=["llama3.2", "mistral", "phi3.5"],
    prompt_template='Return JSON {"label":string,"prob":float} for {text}',
    json_keys=("label", "prob"),
    fanout=True,
    temperature=0.7,    # more deterministic
    max_tokens=50,      # brief responses
)
# adds label_llama3.2, prob_llama3.2, label_mistral, …

# 2 · Classic workload split (no fan-out), higher temperature
scores = run_analysis(
    df,
    prompt_template="Summarise: {text}",
    temperature=1.0,
    max_tokens=100
)

# 3 · CSV enrichment with fan-out, custom token limit
fill_missing_fields_from_csv(
    input_csv="events.csv",
    output_csv="events_filled.csv",
    json_fields=("Occasion", "City"),
    col_map={"Occasion":"occ", "City":"place"},
    workers=2,
    model_names=["llama3.2","mistral"],
    fanout=True,
    temperature=0.8,
    max_tokens=60
)
```


### 3 · Survey‐Agent Simulation

```python
def generate_fake_survey_df(
    n: int,
    *,
    seed: Optional[int] = None,
    characteristics: Dict[str, SpecType],
    fixed_values: Optional[Dict[str, Any]] = None
) -> pd.DataFrame
```

| Parameter         | Default | Purpose                                                                                                                                                                                          |
| ----------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `n`               | —       | Number of synthetic survey takers (rows).                                                                                                                                                        |
| `seed`            | `None`  | Optional `random.seed(…)` for reproducibility.                                                                                                                                                   |
| `characteristics` | —       | Mapping column name → spec. Spec may be:<br>• `list[…], dict{value:weight}` or `callable()` for **unconditional** draws<br>• `{"depends_on":col, "distributions":{…}}` for **conditional** draws |
| `fixed_values`    | `None`  | Mapping col → single value to assign to every row.                                                                                                                                               |

Returns a `DataFrame` with `ID` plus each characteristic (and any fixed columns).

```python
run_survey_responses(
    df: pd.DataFrame,
    questions: Dict[str, Optional[List[str]]],
    workers: int = 3,
    chunk_size: Optional[int] = None,
    batch_size: int = 4,
    max_concurrent_calls: Optional[int] = None,
    max_tokens: int = 256,
    *,                       # keyword-only extras
    model_names: str | list[str] = "llama3.2",
    temperature: float = 0.9,
) -> pd.DataFrame
```

| Parameter              | Default      | Purpose                                                                                        |
| ---------------------- | ------------ | ---------------------------------------------------------------------------------------------- |
| `df`, `questions`      | —            | Input respondents and survey items mapping question → options (list) or `None` (open).         |
| `workers`              | 3            | Number of parallel `AsyncClient` workers (row‐level sharding).                                 |
| `max_concurrent_calls` | `None`       | Caps the simultaneous in-flight LLM calls (defaults to `workers`).                                 |
| `model_names`          | `"llama3.2"` | Single model or list of length `workers` (one per client).                                     |
| `batch_size`           | 4            | Prompts queued per worker before awaiting; larger → fewer HTTP round-trips but more VRAM used. |
| `chunk_size`           | `None`       | Outer chunk size for streaming the DataFrame; `None` → one big batch.                          |
| `max_tokens`           | 256          | Maximum tokens to generate per question.                                                       |
| `temperature`          | 0.9          | LLM sampling temperature.                                                                      |

---

## Quick Examples

```python
from async_run_ollama import (
    generate_fake_survey_df,
    run_survey_responses
)
import pandas as pd

# 1a · Build 200 fake respondents with conditional age by gender and unconditional education
characteristics = {
    "Gender": {"Man": 0.5, "Woman": 0.45, "Nonbinary": 0.05},
    "Age_Group": {
        "depends_on": "Gender",
        "distributions": {
            "Man":   {"18-24":0.2, "25-34":0.3, "35-44":0.3, "45+":0.2},
            "Woman": {"18-24":0.3, "25-34":0.3, "35-44":0.2, "45+":0.2},
            "Nonbinary": ["18-24","25-34","35-44"]
        }
    },
    "Education": ["High School","College","Graduate"], #will be split evenly
}
# 1b. Purely Unconditional 
characteristics = {
    "Gender": {"Man": 0.5, "Woman": 0.45, "Nonbinary": 0.05},
    "Age_Group": ["18-24", "25-34", "35-44", "45-54", "55+"],
    "Education": {"High School": 0.3, "Graduate": 0.5, "MA": 0.2},
}
df = generate_fake_survey_df(
    n=200,
    seed=42,
    characteristics=characteristics,
    fixed_values={"Nationality":"Palestine"}
)

# 2 · Define your survey (MC + open)
questions = {
    "How satisfied are you with your job?": [
        "Very satisfied",
        "Somewhat satisfied",
        "Neutral",
        "Somewhat dissatisfied",
        "Very dissatisfied",
    ],
    "What is your preferred work environment?": None,
    "Which benefit matters most to you?": [
        "Salary",
        "Work-life balance",
        "Career growth",
        "Health benefits",
        "Other"
    ],
}

# 3 · Simulate across 4 workers, batching, with progress bars
filled = run_survey_responses(
    df,
    questions,
    workers=4,
    chunk_size=50,
    batch_size=8,
    max_concurrent_calls=10,
    max_tokens=128,
    model_names="llama3.2",
    temperature=0.7
)

print(filled.head())
```

## How parallelisation works in the code

### One worker ≈ one Ollama “session”

Internally, each worker creates its own `AsyncClient`, which translates to an
independent streaming connection and an independent copy of the model held in
GPU (or CPU) memory:

```

worker-0 ─┐ ┌─▶ llama3.2-1B (GPU slot 0)  
worker-1 ─┤ Async → ─┤─▶ llama3.2-1B (GPU slot 0) ← might be shared if the  
worker-2 ─┘ └─▶ llama3.2-1B (GPU slot 0)             model fits multiple

````

* **VRAM footprint per model copy** (≈ numbers for Llama 3.2 1B Instruct variant):
  * **Loaded**: ~2 GB
  * **During generation** (activations): +0.5 GB
* Ollama automatically *re-uses* a loaded model across sessions **as long as it
  fits**, so three workers hitting **llama3.2-1B** typically keep **one** 2 GB
  copy in VRAM, not three. Activations, however, are per-worker, so generation
  spikes can add ~0.5 GB × workers.

### Fan-out vs. split

| Mode | What happens | Memory | When to use |
|------|--------------|--------|-------------|
| **Split** (`fanout=False`) | Each worker/model gets a distinct slice of the DataFrame/CSV. | ① One model copy *per different tag*.<br>② Activations scale with `workers`. | Max throughput when you have *many* rows. |
| **Fan-out** (`fanout=True`) | Every model analyses **every** row – workers loop through rows multiple times. | Same as split, but activations stack for each model on the same row (so memory ≈ *models* × 0.5 GB during generation). | Comparing answers from several models side-by-side. |

### *Split* Parallelism Step-by-step flow 
There are **two inputs** that decide throughput and memory use:

| Lever             | Variable                                               | What it controls                                                                                                   | Analogy                                             |
| ----------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| **1. Workers**    | `workers=`                                             | How the _whole_ dataset/CSV chunk is **sharded** into pieces that run _concurrently_ (independent `AsyncClient`s). | Number of checkout lanes in a supermarket           |
| **2. Batch size** | `batch_size=` (only in `fill_missing_fields_from_csv`) | How many prompts a **single worker** queues before awaiting the model’s response.                                  | Customer “basket” per lane before the cashier scans |

---

#### 1. Outer chunking _(streaming only for huge CSVs)_

Reads `chunk_size` rows at a time so RAM stays bounded. In `run_analysis()` defaults to whole dataset in `fill_missing_fields_from_csv` 20 000 rows.

#### 2. Split that chunk among **W workers**

```python
parts = np.array_split(chunk, workers)
```

_If `workers = 3` and the chunk has 90 000 rows → 30 000 rows each._

Each worker:

1. Instantiates its own `AsyncClient(model_tag)`.
    
2. Iterates over its slice row-by-row.
    

#### 3. Inner batching 

```python
buf_prompts.append(prompt)
if len(buf_prompts) == batch_size:
    responses = model.generate(buf_prompts)
```

_If `batch_size = 4` the worker fires 4 prompts at once, then awaits the single streaming response that contains 4 completions._

_Pros:_ fewer HTTP round-trips, better GPU utilisation.  
_Cons:_ 4× token activations in VRAM for that worker during generation.

#### 4. Global semaphore

```python
async with semaphore:   # semaphore size = workers
    await client.chat(...)
```

Keeps __at most `workers` simultaneous_ requests_* across all workers.  
That protects your single-GPU Ollama from overload if you accidentally set  
`workers` very high.

---

### How to reason about the two inputs

|Goal|Raise:|Lower:|
|---|---|---|
|**Throughput** (lots of rows)|`workers` first, then `batch_size`|—|
|**GPU memory OK, but HTTP latency high**|`batch_size`|—|
|**GPU VRAM limited**|—|`workers` and/or `batch_size`|
|**CPU-bound (no GPU)**|`batch_size` (more efficient streaming)|keep `workers` modest (2-3)|

> **Rule of thumb**  
> _Workers_ scale with **number of CPU cores**; _batch size_ scales with **model size & VRAM**.  
> For a 24 GB GPU: Llama-3-Instruct-8B can usually handle `batch_size=6` × `workers=4` without OOM.


### Example 1: Simple Illustration without batch_size

Suppose you run:

```python
run_analysis(
    df,
    workers=4,
    model_names=["llama3.2-1B"]*4,
)
````

- **VRAM baseline**: ~2 GB (one shared copy of the 1 B weights)
    
- **During peak generation**: 2 GB + 4 × 0.5 GB ≈ **4 GB**
    
- **CPU load**: 4 asynchronous decoding threads saturating one GPU.
    

Switch to fan-out with two different models:

```python
run_analysis(
    df,
    workers=2,
    model_names=["llama3.2-1B", "mistral-7B"],
    fanout=True,
)
```

- **Models loaded**: 2 GB (1 B) + 13 GB (7 B) ≈ **15 GB VRAM**
    
- **Peak activations**: +2 × 0.5 GB ≈ **1 GB** extra
    
- Every row produces _two_ sets of outputs: `_llama3.2-1B` and `_mistral-7B`.
    

If VRAM is tight, lower `workers`, set `fanout=False`, or choose smaller  
models. You can also instruct Ollama to keep only one model resident at a time:

```bash
export OLLAMA_MAX_LOADED_MODELS=1
```

Ollama will then swap models in-and-out between requests, trading memory for  
slightly lower throughput.

---

### Example 2: Slightly more complex illustration 
Below is a **split-mode** scenario that exercises _both_ levers —  
`workers` **and** `batch_size` — so you can see how they interact.

```python
from ollama_run_async import fill_missing_fields_from_csv

fill_missing_fields_from_csv(
    input_csv="events.csv",       # 120 000 rows total
    output_csv="events_filled.csv",
    chunk_size=40_000,            # 3 outer chunks streamed
    workers=4,                    # 4 AsyncClients ⇒ 10 000 rows each per chunk
    batch_size=6,                 # each worker fires 6 prompts at once
    json_fields=("Occasion", "City"),
    model_names=["llama3.2-1B"]*4,  # same 1 B model on every lane
    fanout=False,                 # pure split
)
```

**At Peak generation:**

```
    4 workers  ×  6-prompt batch  ⇒  24 prompts generating concurrently
```

- **VRAM baseline**  
    One shared copy of Llama 3.2-1B ≈ **2 GB**
    
- **Generation activations**  
    4 workers × 0.5 GB ≈ **2 GB**
    
- **Total peak** ≈ **4 GB** (fits easily on an 8 GB card)
    

CPU load spreads across four decoding threads; HTTP overhead is amortised  
because each request carries six prompts.

---

Switch to **fan-out** with two different models and preserve batching:

```python
fill_missing_fields_from_csv(
    input_csv="events.csv",
    output_csv="events_filled.csv",
    chunk_size=40_000,
    workers=2,
    batch_size=6,
    json_fields=("Occasion", "City"),
    model_names=["llama3.2-1B", "mistral-7B"],  # different tag per worker
    fanout=True,                                # every model handles every row
)
```

- **Models loaded**  
    1 B (2 GB) + 7 B (≈13 GB) = **15 GB** baseline.
    
- **Activations**  
    2 workers × 0.5 GB = **1 GB** extra during generation.
    
- **Outcome**  
    Each row now gets two result columns per key:  
    `computed_occasion_llama3.2-1B`, `computed_occasion_mistral-7B`, etc.
    

If 16 GB VRAM is too tight, you could:

```bash
export OLLAMA_MAX_LOADED_MODELS=1   # keep only one model resident at a time
```

and/or drop `batch_size` to 4.

## Troubleshooting

| Issue                                         | Fix                                                                   |
| --------------------------------------------- | --------------------------------------------------------------------- |
| `ResponseError: model not found`              | `ollama pull <model_tag>` on the Ollama host.                         |
| Notebook raises `RuntimeError: asyncio.run()` | Call the high-level helpers – they auto-detect running loops.         |
| VRAM/CPU overload                             | Lower `workers` or `batch_size`, or set `OLLAMA_MAX_LOADED_MODELS=1`. |
