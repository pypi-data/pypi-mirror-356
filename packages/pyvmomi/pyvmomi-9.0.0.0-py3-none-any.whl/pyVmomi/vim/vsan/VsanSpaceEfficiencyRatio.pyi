# Copyright (c) 2006-2025 Broadcom. All Rights Reserved.
# Broadcom Confidential. The term "Broadcom" refers to Broadcom Inc.
# and/or its subsidiaries.

# ******* WARNING - AUTO GENERATED CODE - DO NOT EDIT *******

from typing import Optional

from pyVmomi.vmodl import DynamicData

class VsanSpaceEfficiencyRatio(DynamicData):
   overallRatio: Optional[float] = None
   compressionRatio: Optional[float] = None
   dedupRatio: Optional[float] = None
