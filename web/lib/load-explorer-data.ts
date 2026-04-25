import { promises as fs } from "fs";
import path from "path";

import { ExplorerArtifact } from "@/lib/types";

export async function loadExplorerData(): Promise<ExplorerArtifact> {
  const deployableArtifactPath = path.join(process.cwd(), "data", "paper_core_explorer.json");
  const repoArtifactPath = path.join(
    process.cwd(),
    "..",
    "artifacts",
    "frontend",
    "paper_core_explorer.json",
  );
  const artifactPath = await fs
    .access(deployableArtifactPath)
    .then(() => deployableArtifactPath)
    .catch(() => repoArtifactPath);

  const raw = await fs.readFile(artifactPath, "utf8");
  return JSON.parse(raw) as ExplorerArtifact;
}
