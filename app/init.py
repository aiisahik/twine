#!/usr/bin/env python
import os
import sys
from account.models import *
from battle.models import *

p1 = Profile.objects.get(user_id=5)
p2 = Profile.objects.get(user_id=4)
p3 = Profile.objects.get(user_id=7)
g = Group.objects.get(id=1)