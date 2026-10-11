mkdir out | Out-Null; if ($?) { "created" } else { "failed" }
mkdir out 2>$null | Out-Null; if ($?) { "created" } else { "failed" }
