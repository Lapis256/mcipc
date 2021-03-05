# mcipc
Made query compatible with asyncio.
Other than that, refer to the fork source.

## Install
```
pip install git+https://github.com/Lapis256/mcipc.git@async_query
```

### Query protocol
See fork source for an overview

```python
import asyncio
from mcipc.query import Client

async def print_stats():
    async with Client('127.0.0.1', 25565) as client:
        basic_stats = await client.stats()            # Get basic stats.
        full_stats = await client.stats(full=True)    # Get full stats.

    print(basic_stats)
    print(full_stats)

asyncio.run(print_stats())
```

## License
Copyright (C) 2018-2020 Richard Neumann <mail at richard dash neumann period de>

mcipc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mcipc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with mcipc.  If not, see <http://www.gnu.org/licenses/>.

## Legal
Minecraft content and materials are trademarks and copyrights of
Mojang and its licensors. All rights reserved.
This program is free software and is not affiliated with Mojang.
