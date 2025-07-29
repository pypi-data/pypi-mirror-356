## Orbax 🤝 Dataclasses

A convenient way to serialize dataclasses (and for orbax) in an easier to read way (avoid Pickle!)

Usage:

Suppose we have a train state
```python
import flax.linen as nn
import optax
import flax.training.train_state
import flax_orbax

model = nn.Sequential([nn.Dense(10, kernel_init=nn.initializers.ones), nn.Dense(10, kernel_init=nn.initializers.ones)])
params = model.init(jax.random.key(0), jax.numpy.ones((1, 20)))['params']
tx = flax_orbax.wrap(optax.adam)(1e-3) # Add flax_orbax.wrap to keep track of objects that aren't serializable
state = flax.training.train_state.TrainState.create(apply_fn=model, params=params, tx=tx)
```


Now, we can save this easily

```python
import orbax.checkpoint as ocp
path = ocp.test_utils.erase_and_create_empty('/tmp/my-checkpoints/')
ckptr = flax_orbax.Checkpointer()
ckptr.save(path / '0', state)
ckptr.wait_until_finished()
ckptr.restore(path / '0') # Unlike StandardCheckpointer(), this will return a train state! not a dict
```