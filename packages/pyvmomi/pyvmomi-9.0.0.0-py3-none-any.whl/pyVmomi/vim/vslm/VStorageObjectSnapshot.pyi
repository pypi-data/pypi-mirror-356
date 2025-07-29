# Copyright (c) 2006-2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

# ******* WARNING - AUTO GENERATED CODE - DO NOT EDIT *******

from typing import Optional

from pyVmomi.VmomiSupport import long

from pyVmomi.vmodl import DynamicData

from pyVmomi.vim.vslm import ID
from pyVmomi.vim.vslm import VClockInfo

class VStorageObjectSnapshot(DynamicData):
   id: ID
   vclock: VClockInfo
   usedCapacity: Optional[long] = None
