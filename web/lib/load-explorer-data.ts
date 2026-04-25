import { promises as fs } from "fs";
import path from "path";

import { ExplorerArtifact } from "@/lib/types";

export async function loadExplorerData(): Promise<ExplorerArtifact> {
  const artifactPath = path.join(
    process.cwd(),
    "..",
    "artifacts",
    "frontend",
    "paper_core_explorer.json",
  );

  const raw = await fs.readFile(artifactPath, "utf8");
  return JSON.parse(raw) as ExplorerArtifact;
}
