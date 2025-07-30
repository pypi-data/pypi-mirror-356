# intellif-aihub

Detect Kubernetes pre-stop lifecycle events with a simple sentinel file.

```python
import aihub

while training:
    if aihub.is_stopped():
        save_checkpoint(); break
