#!/usr/bin/env python3

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# setup 0 paramter
i = 0
while i < 64 * 8:
  key = "param" + str(i)
  r.set(key, 0)
  i += 1
# set defaukt patch

# 0
key = "param" + str(0)
r.set(key, 64)

# 1
key = "param" + str(1)
r.set(key, 0)

# 2
key = "param" + str(2)
r.set(key, 127)

# 3
key = "param" + str(3)
r.set(key, 64)

# 4
key = "param" + str(4)
r.set(key, 64)

# 5
key = "param" + str(5)
r.set(key, 64)

# 6
key = "param" + str(6)
r.set(key, 64)

# 7
key = "param" + str(7)
r.set(key, 64)
