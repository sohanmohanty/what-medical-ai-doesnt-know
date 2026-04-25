import { ExplorerClient } from "@/components/explorer/explorer-client";
import { loadExplorerData } from "@/lib/load-explorer-data";

export default async function ExplorerPage() {
  const data = await loadExplorerData();

  return (
    <div className="space-y-10 pb-20">
      <section className="max-w-4xl">
        <p className="eyebrow">Explorer</p>
        <h1 className="mt-6 text-4xl font-semibold leading-[0.98] text-ink sm:text-6xl">
          Explore how missing data changes both prediction and trust.
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-9 text-muted">
          Compare datasets, model families, missingness patterns, and severity levels side by side.
          Each selection shows how incomplete information can change both predictive performance and
          the trustworthiness of the reported probability.
        </p>
      </section>
      <ExplorerClient data={data} />
    </div>
  );
}
