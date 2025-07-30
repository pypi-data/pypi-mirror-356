# Copyright (C) 2022 Rainer Garus
#
# This file is part of the ooresults Python package, a software to
# compute results of orienteering events.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Optional

from ooresults.repo.repo import Repo

from . import classes
from . import clubs
from . import competitors
from . import courses
from . import entries
from . import events
from . import results
from . import series


__all__ = [
    "classes",
    "clubs",
    "competitors",
    "courses",
    "entries",
    "events",
    "results",
    "series",
]


db: Optional[Repo] = None
